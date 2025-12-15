"""
Decision Moment - Analyze trade decisions with ELFA narrative integration.
"""
from typing import Dict, Any, Optional
from strategies import evaluate_strategy


class DecisionMoment:
    """Analyze trade decisions using strategy evaluation and ELFA narratives."""
    
    def __init__(self):
        """Initialize Decision Moment analyzer."""
        pass
    
    def analyze_with_elfa(self, strategy: str, narratives: Dict[str, Any], 
                         market_combo: Optional[Dict[str, Any]] = None,
                         user_view: str = 'neutral',
                         thoughts: str = '') -> Dict[str, Any]:
        """
        Analyze a trade decision using strategy evaluation and ELFA narratives.
        
        Parameters:
        -----------
        strategy : str
            Strategy name
        narratives : dict
            ELFA narratives dictionary
        market_combo : dict, optional
            Market combo data (if None, will be derived from narratives)
        user_view : str
            User's market view: 'bullish', 'bearish', 'neutral', 'hedge'
        thoughts : str
            User's rationale
        
        Returns:
        --------
        dict
            Decision analysis with keys: score, reasoning, alignment, riskNotes, etc.
        """
        # Extract market data from narratives (default to BTC)
        if market_combo is None:
            market_combo = self._extract_market_combo(narratives)
        
        # Get strategy evaluation
        verdict = evaluate_strategy(strategy, market_combo, user_view, thoughts)
        
        # Calculate alignment score
        alignment_score = self._calculate_alignment_score(strategy, narratives, market_combo)
        
        # Generate reasoning
        reasoning = self._generate_reasoning(strategy, narratives, verdict, alignment_score)
        
        return {
            'score': alignment_score,
            'reasoning': reasoning,
            'alignment': verdict['correct'],
            'reason': verdict['reason'],
            'alternatives': verdict['alt'],
            'riskNotes': verdict['riskNotes'],
            'growthNotes': verdict['growthNotes'],
            'narrativeContext': self._get_narrative_context(narratives)
        }
    
    def _extract_market_combo(self, narratives: Dict[str, Any], asset: str = 'BTC') -> Dict[str, Any]:
        """
        Extract market combo data from narratives.
        
        Parameters:
        -----------
        narratives : dict
            Narratives dictionary
        asset : str
            Asset symbol (default: 'BTC')
        
        Returns:
        --------
        dict
            Market combo with deltaLike, vegaLike, etc.
        """
        if asset not in narratives:
            # Default fallback
            return {
                'deltaLike': 0.0,
                'vegaLike': 0.5,
                'gammaLike': 0.5,
                'thetaLike': 0.2,
                'pcr': 1.5,
                'iv': 0.6,
                'rv': 0.45
            }
        
        data = narratives[asset]
        momentum = data.get('momentum', 0.0)
        sentiment = data.get('sentiment', 'neutral')
        vol_data = data.get('volatility', {})
        iv = vol_data.get('implied', 0.6) if isinstance(vol_data, dict) else 0.6
        rv = vol_data.get('realized', 0.45) if isinstance(vol_data, dict) else 0.45
        
        # Map momentum to delta-like (directional bias)
        delta_like = (momentum - 0.5) * 2.0  # Convert 0-1 to -1 to 1
        
        # Map sentiment
        if sentiment == 'bearish':
            delta_like = min(delta_like, -0.25)
        elif sentiment == 'bullish':
            delta_like = max(delta_like, 0.25)
        
        # Gamma-like based on volatility
        gamma_like = min(iv, 1.0) if iv > 0.5 else 0.3
        
        # Vega-like based on IV-RV spread
        vega_like = min(max(iv - rv + 0.4, 0.0), 1.0)
        
        # Theta-like
        theta_like = 0.3 if (iv - rv) > 0.05 else 0.15
        
        return {
            'deltaLike': delta_like,
            'vegaLike': vega_like,
            'gammaLike': gamma_like,
            'thetaLike': theta_like,
            'pcr': 1.8,  # Default, could be extracted from data if available
            'iv': iv,
            'rv': rv
        }
    
    def _calculate_alignment_score(self, strategy: str, narratives: Dict[str, Any],
                                  market_combo: Dict[str, Any]) -> float:
        """
        Calculate alignment score between strategy and narratives.
        
        Parameters:
        -----------
        strategy : str
            Strategy name
        narratives : dict
            Narratives dictionary
        market_combo : dict
            Market combo data
        
        Returns:
        --------
        float
            Alignment score (0-1)
        """
        # Base score from strategy evaluation
        base_score = 0.5
        
        # Adjust based on market conditions
        delta_like = market_combo.get('deltaLike', 0.0)
        vega_like = market_combo.get('vegaLike', 0.5)
        
        # Strategy-specific adjustments
        if strategy in ['call', 'covered_call']:
            if delta_like > 0.2:
                base_score += 0.2
            elif delta_like < -0.2:
                base_score -= 0.2
        elif strategy in ['put', 'protective_put']:
            if delta_like < -0.2:
                base_score += 0.2
            elif delta_like > 0.2:
                base_score -= 0.2
        elif strategy in ['iron_condor', 'short_straddle']:
            if abs(delta_like) < 0.2 and vega_like > 0.5:
                base_score += 0.3
        
        # Narrative momentum boost
        if 'BTC' in narratives:
            momentum = narratives['BTC'].get('momentum', 0.5)
            base_score += (momentum - 0.5) * 0.1
        
        return max(0.0, min(1.0, base_score))
    
    def _generate_reasoning(self, strategy: str, narratives: Dict[str, Any],
                           verdict: Dict[str, Any], score: float) -> str:
        """
        Generate human-readable reasoning for the decision.
        
        Parameters:
        -----------
        strategy : str
            Strategy name
        narratives : dict
            Narratives dictionary
        verdict : dict
            Strategy evaluation verdict
        score : float
            Alignment score
        
        Returns:
        --------
        str
            Reasoning text
        """
        reasoning_parts = [verdict['reason']]
        
        # Add narrative context
        if 'BTC' in narratives:
            btc_data = narratives['BTC']
            sentiment = btc_data.get('sentiment', 'neutral')
            momentum = btc_data.get('momentum', 0.5)
            
            if momentum > 0.6:
                reasoning_parts.append(f"Strong momentum ({momentum:.2f}) supports directional strategies.")
            elif momentum < 0.4:
                reasoning_parts.append(f"Weak momentum ({momentum:.2f}) favors neutral/hedging strategies.")
            
            if sentiment != 'neutral':
                reasoning_parts.append(f"Market sentiment is {sentiment}.")
        
        # Add score interpretation
        if score > 0.7:
            reasoning_parts.append("High alignment with current market narratives.")
        elif score < 0.4:
            reasoning_parts.append("Low alignment - consider alternative strategies.")
        
        return " ".join(reasoning_parts)
    
    def _get_narrative_context(self, narratives: Dict[str, Any]) -> Dict[str, Any]:
        """
        Extract narrative context for display.
        
        Parameters:
        -----------
        narratives : dict
            Narratives dictionary
        
        Returns:
        --------
        dict
            Context summary
        """
        context = {}
        
        for asset, data in narratives.items():
            context[asset] = {
                'sentiment': data.get('sentiment', 'neutral'),
                'momentum': data.get('momentum', 0.0),
                'theme_count': len(data.get('themes', []))
            }
        
        return context

