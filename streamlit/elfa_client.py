"""
ELFA API client for fetching market narratives and data.
"""
import requests
from typing import Dict, Any, Optional


class ElfaClient:
    """Client for interacting with ELFA API."""
    
    def __init__(self, api_key: str):
        """
        Initialize ELFA client.
        
        Parameters:
        -----------
        api_key : str
            ELFA API key
        """
        self.api_key = api_key
        self.base_url = "https://app.elfa.ai/api"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    def get_narratives(self) -> Dict[str, Any]:
        """
        Get market narratives for various assets.
        
        Returns:
        --------
        dict
            Dictionary mapping asset names to narrative data:
            {
                'BTC': {
                    'momentum': float,
                    'sentiment': str,
                    'themes': list,
                    'price': float,
                    ...
                },
                ...
            }
        """
        try:
            # Try to fetch from ELFA API
            url = f"{self.base_url}/narratives"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_narratives(data)
            else:
                # Fallback to synthetic data
                return self._get_synthetic_narratives()
        except Exception as e:
            # Fallback to synthetic data on error
            print(f"Error fetching ELFA narratives: {e}")
            return self._get_synthetic_narratives()
    
    def get_btc_summary(self) -> Dict[str, Any]:
        """
        Get BTC market summary.
        
        Returns:
        --------
        dict
            BTC market data with price, volatility, sentiment, etc.
        """
        try:
            url = f"{self.base_url}/btc/summary"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            if response.status_code == 200:
                return response.json()
            else:
                return self._get_synthetic_btc_data()
        except Exception as e:
            print(f"Error fetching BTC summary: {e}")
            return self._get_synthetic_btc_data()
    
    def _parse_narratives(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse ELFA API response into standardized format.
        
        Parameters:
        -----------
        data : dict
            Raw API response
        
        Returns:
        --------
        dict
            Parsed narratives dictionary
        """
        narratives = {}
        
        # Handle different possible API response formats
        if isinstance(data, dict):
            if 'assets' in data:
                for asset_data in data['assets']:
                    asset_name = asset_data.get('symbol', 'UNKNOWN')
                    narratives[asset_name] = {
                        'momentum': asset_data.get('momentum', 0.0),
                        'sentiment': asset_data.get('sentiment', 'neutral'),
                        'themes': asset_data.get('themes', []),
                        'price': asset_data.get('price', 0.0),
                        'volatility': asset_data.get('volatility', {}),
                        'trend': asset_data.get('trend', {})
                    }
            elif 'BTC' in data or 'btc' in data:
                # Single asset response
                btc_data = data.get('BTC') or data.get('btc') or data
                narratives['BTC'] = {
                    'momentum': btc_data.get('momentum', 0.0),
                    'sentiment': btc_data.get('sentiment', 'neutral'),
                    'themes': btc_data.get('themes', []),
                    'price': btc_data.get('price', 90000),
                    'volatility': btc_data.get('volatility', {}),
                    'trend': btc_data.get('trend', {})
                }
        
        # If no narratives found, return synthetic
        if not narratives:
            return self._get_synthetic_narratives()
        
        return narratives
    
    def _get_synthetic_narratives(self) -> Dict[str, Any]:
        """
        Generate synthetic narrative data for fallback.
        
        Returns:
        --------
        dict
            Synthetic narratives
        """
        return {
            'BTC': {
                'momentum': 0.65,
                'sentiment': 'bullish',
                'themes': [
                    'Institutional adoption',
                    'ETF inflows',
                    'Halving narrative',
                    'Macro risk-on'
                ],
                'price': 90000,
                'volatility': {
                    'implied': 0.6,
                    'realized': 0.45
                },
                'trend': {
                    'slope': 0.3,
                    'strength': 0.7
                }
            },
            'ETH': {
                'momentum': 0.55,
                'sentiment': 'neutral',
                'themes': [
                    'Layer 2 scaling',
                    'Staking yields',
                    'DeFi activity'
                ],
                'price': 3000,
                'volatility': {
                    'implied': 0.55,
                    'realized': 0.40
                },
                'trend': {
                    'slope': 0.1,
                    'strength': 0.5
                }
            }
        }
    
    def _get_synthetic_btc_data(self) -> Dict[str, Any]:
        """
        Generate synthetic BTC summary data.
        
        Returns:
        --------
        dict
            Synthetic BTC data
        """
        return {
            'price': 90000,
            'vol': {
                'implied': 0.6,
                'realized': 0.45
            },
            'putCallRatio': 1.8,
            'sentiment': 'neutral',
            'trend': {
                'slope': 0.05
            }
        }

