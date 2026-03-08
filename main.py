import asyncio
import time
from web3 import Web3
from firebase_setup import get_firestore_client
from config import BASE_RPC_URL, PRIVATE_RELAY_URLS, MIN_PROFIT_PCT, TARGET_PROFIT_PCT
from wallet_manager import WalletManager
from flow_generator import FlowGenerator
from simulator import OnChainSimulator
from bundle_propagator import BundlePropagator
from regime_detector import RegimeDetector
import pandas as pd

class Orchestrator:
    def __init__(self):
        self.w3 = Web3(Web3.HTTPProvider(BASE_RPC_URL))
        self.db = get_firestore_client()
        self.wallet_manager = WalletManager(self.w3)
        self.flow_generator = FlowGenerator(self.w3, self.wallet_manager)
        self.simulator = OnChainSimulator(self.w3)
        self.bundle_propagator = BundlePropagator(PRIVATE_RELAY_URLS)
        self.regime_detector = RegimeDetector()
        
        # State
        self.total_profit = 0
        self.trade_count = 0
        
    async def run_flow_generation(self):
        """Generate flow events at random intervals (every 2-5 minutes)"""
        while True:
            # Wait for a random time between 120 and 300 seconds
            wait_time = random.randint(120, 300)
            await asyncio.sleep(wait_time)
            
            # Generate a flow event on a random pair
            pairs = ["WETH/USDC", "WETH/USDT", "USDC/USDT"]
            pair = random.choice(pairs)
            amount = random.uniform(0.1, 1.0)  # 0.1 to 1 ETH
            
            try:
                tx_hash = await self.flow_generator.generate_flow_event(pair, amount)
                print(f"Generated flow event: {tx_hash.hex()} for {pair} with {amount} ETH")
            except Exception as e:
                print(f"Error generating flow event: {e}")
    
    async def run_opportunity_detection(self):
        """Continuously look for arbitrage opportunities"""
        while True:
            # Check for recent flow events (last 10 blocks)
            latest_block = self.w3.eth.block_number
            from_block = latest_block - 10
            
            # Query Firestore for flow events in the last 10 blocks (or use on-chain events)
            # For now, we'll simulate by checking a fixed set of paths
            # In production, we would dynamically generate paths based on flow events
            
            # Example path (placeholder)
            path = [
                {
                    'contract': '0x...',  # Uniswap V3 router
                    'calldata': '0x...',  # Swap WETH for USDC
                    'value': 0
                },
                {
                    'contract': '0x...',  # Curve V2 pool
                    'calldata': '0x...',  # Swap USDC for USDT
                    'value': 0
                },
                {
                    'contract': '0x...',  # Uniswap V3 router
                    'calldata': '0x...',  # Swap USDT for WETH
                    'value': 0
                }
            ]
            
            # Simulate with a fixed amount (e.g., 1 ETH)
            amount_in = self.w3.to_wei(1, 'ether')
            simulation_result = await self.simulator.simulate_arbitrage(path, amount_in)
            
            if simulation_result['feasible'] and simulation_result['profit'] > 0:
                # Check if profit percentage meets minimum
                profit_pct = simulation_result['profit'] / amount_in
                if profit_pct >= MIN_PROFIT_PCT:
                    print(f"Arbitrage opportunity detected with profit: {profit_pct*100}%")
                    # TODO: Construct and propagate bundle
                    # For now, we just log the opportunity
                    trade = {
                        'timestamp': time.time(),
                        'pair': 'WETH/USDC/USDT',
                        'profit_wei': simulation_result['profit'],
                        'profit_pct': profit_pct,
                        'gas_used': 0,  # placeholder
                        'regime': self.regime_detector.last_regime,
                        'simulation_accurate': True
                    }
                    self.db.collection('trades').add(trade)
            
            # Wait for a short time before next check
            await asyncio.sleep(1)
    
    async def run_regime_detection(self):
        """Periodically update the market regime"""
        while True:
            # Wait for 1 hour
            await asyncio.sleep(3600)
            
            # Fetch recent trades from Firestore
            trades_ref = self.db.collection('trades')
            trades = trades_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).limit(100).get()
            trade_data = []
            for trade in trades:
                trade_dict = trade.to_dict()
                trade_data.append(trade_dict)
            
            if trade_data:
                df = pd.DataFrame(trade_data)
                regime = self.regime_detector.analyze_market_regime(df)
                print(f"Current market regime: {regime}")
                
                # Update system state in Firestore
                state = {
                    'current_regime': regime,
                    'timestamp': time.time()
                }
                self.db.collection('system_state').add(state)
    
    async def main(self):
        """Main orchestration loop"""
        # Start background tasks
        flow_task = asyncio.create_task(self.run_flow_generation())
        detection_task = asyncio.create_task(self.run_opportunity_detection())
        regime_task