import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

class RegimeDetector:
    def __init__(self, n_clusters=3):
        self.scaler = StandardScaler()
        self.kmeans = KMeans(n_clusters=n_clusters)
        self.last_regime = None
        
    def analyze_market_regime(self, trade_data: pd.DataFrame) -> str:
        """Classify current market regime"""
        # We expect trade_data to have at least the following columns:
        # 'profit_pct', 'gas_cost', 'execution_speed', 'liquidity_depth'
        # If there's not enough data, return a default regime.
        if len(trade_data) < 10:
            return "INSUFFICIENT_DATA"
        
        features = trade_data[['profit_pct', 'gas_cost', 'execution_speed', 'liquidity_depth']]
        scaled = self.scaler.fit_transform(features)
        regime = self.kmeans.predict(scaled[-1:])[0]
        
        regimes = {
            0: 'HIGH_VOLATILITY',
            1: 'LOW_LIQUIDITY', 
            2: 'STABLE_ARB'
        }
        current_regime = regimes.get(regime, 'UNKNOWN')
        self.last_regime = current_regime
        return current_regime