"""farcaster_client.py - Farcaster integration for Temple of Greeks

Handles casting trade results to Farcaster using Neynar API
"""
import requests
import os
from typing import Dict, Optional
from chorus import cult_rank


class FarcasterClient:
    """Client for posting casts to Farcaster via Neynar API."""
    
    def __init__(self, api_key: Optional[str] = None, signer_uuid: Optional[str] = None):
        """Initialize Farcaster client.
        
        Args:
            api_key: Neynar API key (get from neynar.com)
            signer_uuid: Signer UUID for posting casts
        """
        self.api_key = api_key or os.getenv('NEYNAR_API_KEY', '')
        self.signer_uuid = signer_uuid or os.getenv('FARCASTER_SIGNER_UUID', '')
        self.base_url = 'https://api.neynar.com/v2/farcaster'
        
    def generate_cast_text(
        self,
        strategy: str,
        user_view: str,
        score: float,
        philosopher_quote: str,
        cult_rank_name: str,
        favor_score: int,
        streak: int,
        underlying: float,
        strike: float,
        expiry_days: int,
        volatility: float,
        app_url: str = "https://temple-of-greeks.streamlit.app"
    ) -> str:
        """Generate cast text for trade result.
        
        Args:
            strategy: Trading strategy name
            user_view: Market view (bullish/bearish/neutral/hedge)
            score: Decision quality score (0-1)
            philosopher_quote: The absurd commentary
            cult_rank_name: Current cult rank
            favor_score: Cumulative favor points
            streak: Current win streak
            underlying: Underlying asset price
            strike: Strike price
            expiry_days: Days to expiration
            volatility: Implied volatility
            app_url: URL to the Streamlit app
        
        Returns:
            Formatted cast text
        """
        # Determine score emoji
        if score > 0.75:
            score_emoji = "🟢"
            judgment = "BLESSED"
        elif score > 0.5:
            score_emoji = "🟡"
            judgment = "ACCEPTABLE"
        else:
            score_emoji = "🔴"
            judgment = "CONDEMNED"
        
        # Format strategy name
        strategy_display = strategy.replace('_', ' ').title()
        
        # Build cast
        cast_text = f"🏛️ JUDGMENT IN THE AGORA\n\n"
        cast_text += f"Trade: {strategy_display} | {user_view.upper()}\n"
        cast_text += f"Setup: ${underlying:,.0f} → ${strike:,.0f} | {expiry_days}d | σ={volatility:.0%}\n\n"
        cast_text += f"Score: {score:.2f} {score_emoji} ({judgment})\n\n"
        
        # Truncate quote if too long (Farcaster has 320 char limit)
        max_quote_len = 120
        if len(philosopher_quote) > max_quote_len:
            philosopher_quote = philosopher_quote[:max_quote_len] + "..."
        
        cast_text += f"{philosopher_quote}\n\n"
        cast_text += f"🏛️ Rank: {cult_rank_name} ({favor_score} favor)"
        
        if streak > 0:
            cast_text += f" | {streak} 🔥"
        
        cast_text += f"\n\n{app_url}"
        
        return cast_text
    
    def post_cast(
        self,
        text: str,
        channel_id: Optional[str] = "greeks",
        parent_hash: Optional[str] = None
    ) -> Dict:
        """Post a cast to Farcaster.
        
        Args:
            text: Cast text content
            channel_id: Channel to post in (e.g., "greeks", "options")
            parent_hash: Hash of parent cast if replying
        
        Returns:
            API response dict
        """
        if not self.api_key or not self.signer_uuid:
            return {
                'success': False,
                'error': 'Farcaster credentials not configured',
                'message': 'Set NEYNAR_API_KEY and FARCASTER_SIGNER_UUID in secrets'
            }
        
        url = f"{self.base_url}/cast"
        headers = {
            'api_key': self.api_key,
            'Content-Type': 'application/json'
        }
        
        payload = {
            'signer_uuid': self.signer_uuid,
            'text': text
        }
        
        if channel_id:
            payload['channel_id'] = channel_id
        
        if parent_hash:
            payload['parent'] = parent_hash
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            return {
                'success': True,
                'cast': response.json()
            }
        except requests.exceptions.RequestException as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def share_trade_result(
        self,
        strategy: str,
        user_view: str,
        score: float,
        philosopher_quote: str,
        favor_score: int,
        streak: int,
        underlying: float,
        strike: float,
        expiry_days: int,
        volatility: float,
        app_url: str = "https://temple-of-greeks.streamlit.app",
        channel_id: str = "greeks"
    ) -> Dict:
        """Share trade result to Farcaster.
        
        Convenience method that generates cast text and posts it.
        
        Returns:
            API response dict
        """
        rank_name = cult_rank(favor_score)
        
        cast_text = self.generate_cast_text(
            strategy=strategy,
            user_view=user_view,
            score=score,
            philosopher_quote=philosopher_quote,
            cult_rank_name=rank_name,
            favor_score=favor_score,
            streak=streak,
            underlying=underlying,
            strike=strike,
            expiry_days=expiry_days,
            volatility=volatility,
            app_url=app_url
        )
        
        return self.post_cast(cast_text, channel_id=channel_id)
    
    def get_warpcast_url(self, cast_hash: str) -> str:
        """Generate Warpcast URL for a cast.
        
        Args:
            cast_hash: The cast hash from API response
        
        Returns:
            Warpcast URL
        """
        return f"https://warpcast.com/~/conversations/{cast_hash}"
