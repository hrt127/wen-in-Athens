"""
Narrative Radar - Analyze market narratives from ELFA data.
"""
from typing import Dict, Any, List


class NarrativeRadar:
    """Analyze and extract insights from market narratives."""
    
    def __init__(self):
        """Initialize Narrative Radar."""
        pass
    
    def extract_themes(self, narratives: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Extract themes from narratives for each asset.
        
        Parameters:
        -----------
        narratives : dict
            Narratives dictionary from ElfaClient
        
        Returns:
        --------
        dict
            Dictionary mapping asset names to lists of themes
        """
        themes_by_asset = {}
        
        for asset, data in narratives.items():
            themes = data.get('themes', [])
            if isinstance(themes, list):
                themes_by_asset[asset] = themes
            elif isinstance(themes, str):
                # If themes is a string, split it
                themes_by_asset[asset] = [t.strip() for t in themes.split(',')]
            else:
                themes_by_asset[asset] = []
        
        return themes_by_asset
    
    def get_momentum_score(self, narratives: Dict[str, Any], asset: str = 'BTC') -> float:
        """
        Get momentum score for an asset.
        
        Parameters:
        -----------
        narratives : dict
            Narratives dictionary
        asset : str
            Asset symbol (default: 'BTC')
        
        Returns:
        --------
        float
            Momentum score (0-1)
        """
        if asset in narratives:
            return narratives[asset].get('momentum', 0.0)
        return 0.0
    
    def get_sentiment(self, narratives: Dict[str, Any], asset: str = 'BTC') -> str:
        """
        Get sentiment for an asset.
        
        Parameters:
        -----------
        narratives : dict
            Narratives dictionary
        asset : str
            Asset symbol (default: 'BTC')
        
        Returns:
        --------
        str
            Sentiment: 'bullish', 'bearish', 'neutral'
        """
        if asset in narratives:
            return narratives[asset].get('sentiment', 'neutral')
        return 'neutral'
    
    def analyze_narrative_strength(self, narratives: Dict[str, Any], asset: str = 'BTC') -> Dict[str, Any]:
        """
        Analyze overall narrative strength for an asset.
        
        Parameters:
        -----------
        narratives : dict
            Narratives dictionary
        asset : str
            Asset symbol (default: 'BTC')
        
        Returns:
        --------
        dict
            Analysis with keys: strength, direction, confidence
        """
        if asset not in narratives:
            return {
                'strength': 0.0,
                'direction': 'neutral',
                'confidence': 0.0
            }
        
        data = narratives[asset]
        momentum = data.get('momentum', 0.0)
        sentiment = data.get('sentiment', 'neutral')
        themes_count = len(data.get('themes', []))
        
        # Calculate strength based on momentum and theme count
        strength = (momentum * 0.7) + (min(themes_count / 5.0, 1.0) * 0.3)
        
        # Determine direction from sentiment
        direction_map = {
            'bullish': 'up',
            'bearish': 'down',
            'neutral': 'sideways'
        }
        direction = direction_map.get(sentiment, 'sideways')
        
        # Confidence based on data completeness
        confidence = min(strength, 1.0)
        
        return {
            'strength': strength,
            'direction': direction,
            'confidence': confidence
        }

