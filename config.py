import os
from dotenv import load_dotenv

load_dotenv()

# RPC endpoints
BASE_RPC_URL = os.getenv("BASE_RPC_URL", "https://mainnet.base.org")
PRIVATE_RELAY_URLS = [
    os.getenv("PRIVATE_RELAY_URL_1", "https://relay.flashbots.net"),
    os.getenv("PRIVATE_RELAY_URL_2", "https://rpc.titanbuilder.xyz"),
    os.getenv("PRIVATE_RELAY_URL_3", "https://protect.flashbots.net")
]

# Firebase credentials
FIREBASE_CREDENTIALS_PATH = os.getenv("FIREBASE_CREDENTIALS_PATH", "./firebase-credentials.json")

# Wallet private keys (should be stored securely, here for demonstration)
# In production, use hardware signers or secure env variables
FLOW_WALLET_PRIVATE_KEYS = [
    os.getenv("FLOW_WALLET_PRIVATE_KEY_1"),
    os.getenv("FLOW_WALLET_PRIVATE_KEY_2"),
    os.getenv("FLOW_WALLET_PRIVATE_KEY_3"),
]

# Contract addresses (example for Base)
UNISWAP_V3_ROUTER = "0xE592427A0AEce92De3Edee1F18E0157C05861564"
CURVE_V2_ROUTER = "0x...",  # TODO: Fill in actual Curve V2 router on Base
SNX_PERPS_V2 = "0x..."      # TODO: Fill in actual Synthetix Perps V2 on Base

# Trading parameters
MIN_PROFIT_PCT = 0.0015  # 0.15%
TARGET_PROFIT_PCT = 0.003  # 0.3%
MAX_SLIPPAGE = 0.001  # 0.1%

# Gas settings
MAX_GAS_GWEI = 50
PRIORITY_FEE_GWEI = 2

# Firestore collection names
FIRESTORE_COLLECTION_TRADES = "trades"
FIRESTORE_COLLECTION_FLOW_EVENTS = "flow_events"
FIRESTORE_COLLECTION_SYSTEM_STATE = "system_state"