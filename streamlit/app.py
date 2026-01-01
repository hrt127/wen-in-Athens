"""
Greeks Orgy - Streamlit v2 Application
Interactive Options Greeks Playground with ELFA Integration
"""
import streamlit as st
import plotly.graph_objects as go
from blackscholes import calculate_option_price, calculate_greeks, to_years
from strategies import get_strategy_template, simulate_strategy_pnl, evaluate_strategy, calculate_exposure_table
from charts import create_greeks_chart, create_price_chart, create_pnl_chart
from elfa_client import ElfaClient
from narrative_radar import NarrativeRadar
from decision_moment import DecisionMoment
from chorus import absurd_comment, market_mood_text, cult_rank, streak_reward
from farcaster_client import FarcasterClient

# Page configuration
st.set_page_config(
    page_title="Wen in Athens: Temple of Greeks 🔥",    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state
if 'narratives' not in st.session_state:
    st.session_state.narratives = {}
if 'market_combo' not in st.session_state:
    st.session_state.market_combo = None
if 'strategy_template' not in st.session_state:
    st.session_state.strategy_template = None
if 'chart_view' not in st.session_state:
    st.session_state.chart_view = 'greeks'
    if 'score' not in st.session_state:
        st.session_state.score = 0
    if 'streak' not in st.session_state:
        st.session_state.streak = 0
if 'trades' not in st.session_state:
        st.session_state.trades = []

# Sidebar for strategy selection and inputs
with st.sidebar:
    st.title("🏛️ Order of Delta-Dionysus")    
    # Strategy selection
    strategy_options = {
        'Call': 'call',
        'Put': 'put',
        'Covered Call': 'covered_call',
        'Protective Put': 'protective_put',
        'Short Straddle': 'short_straddle',
        'Iron Condor': 'iron_condor',
        'Long Straddle': 'long_straddle',
        'Strangle': 'strangle'
    }
    
    strategy_display = st.selectbox(
        "Pick Strategy",
        options=list(strategy_options.keys()),
        index=0
    )
    strategy = strategy_options[strategy_display]
    
    st.divider()
    
    # Option parameters
    st.subheader("Option Parameters")
    underlying = st.number_input(
        "Underlying Price (S)",
        min_value=1000.0,
        max_value=200000.0,
        value=90000.0,
        step=1000.0,
        format="%.0f"
    )
    
    strike = st.slider(
        "Strike (K)",
        min_value=20000,
        max_value=100000,
        value=90000,
        step=1000
    )
    
    expiry = st.slider(
        "Days to Expiry",
        min_value=1,
        max_value=365,
        value=30,
        step=1
    )
    
    volatility = st.slider(
        "Volatility σ",
        min_value=0.01,
        max_value=2.00,
        value=0.6,
        step=0.01,
        format="%.2f"
    )
    
    risk_free_rate = st.number_input(
        "Risk-Free Rate (r)",
        min_value=0.0,
        max_value=0.1,
        value=0.0,
        step=0.001,
        format="%.3f"
    )
    
    position = st.selectbox(
        "Position",
        options=['long', 'short'],
        index=0
    )
    
    st.divider()
    
    # Chart view selector
    st.subheader("Chart View")
    chart_view = st.radio(
        "Select View",
        options=['greeks', 'price', 'pnl'],
        index=0 if st.session_state.chart_view == 'greeks' else (1 if st.session_state.chart_view == 'price' else 2),
        format_func=lambda x: {
            'greeks': 'Greeks vs S',
            'price': 'Option Price vs S',
            'pnl': 'Strategy PnL vs S'
        }[x]
    )
    st.session_state.chart_view = chart_view

# Main content area - 3 columns
col1, col2, col3 = st.columns([2, 2, 1])

# Prepare inputs dictionary
inputs = {
    'S': underlying,
    'K': strike,
    'days': expiry,
    'sigma': volatility,
    'r': risk_free_rate
}

# Column 1: Greeks Visualization
with col1:
    st.subheader("🏛️ Oracle of Greeks")
    
    # Get option side from strategy
    if strategy in ['call', 'covered_call']:
        side = 'call'
    elif strategy in ['put', 'protective_put']:
        side = 'put'
    else:
        side = 'call'  # Default for multi-leg strategies
    
    # Create appropriate chart based on view
    if chart_view == 'greeks':
        fig = create_greeks_chart(
            underlying, strike, risk_free_rate, volatility, expiry, side
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Display current Greeks values
        current_greeks = calculate_greeks(underlying, strike, risk_free_rate, volatility, to_years(expiry), side)
        
        greeks_cols = st.columns(4)
        with greeks_cols[0]:
            st.metric("Delta (Δ)", f"{current_greeks['delta']:.4f}")
        with greeks_cols[1]:
            st.metric("Gamma (Γ)", f"{current_greeks['gamma']:.6f}")
        with greeks_cols[2]:
            st.metric("Vega (1%)", f"{current_greeks['vegaPer1Pct']:.4f}")
        with greeks_cols[3]:
            st.metric("Theta/day", f"{current_greeks['thetaPerDay']:.6f}")
            
    elif chart_view == 'price':
        fig = create_price_chart(
            underlying, strike, risk_free_rate, volatility, expiry, side
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Display current option price
        current_price = calculate_option_price(underlying, strike, risk_free_rate, volatility, to_years(expiry), side)
        st.metric("Option Price", f"${current_price:.2f}")
        
    elif chart_view == 'pnl':
        # Get strategy template
        template = get_strategy_template(strategy, inputs)
        st.session_state.strategy_template = template
        
        fig = create_pnl_chart(template, inputs)
        st.plotly_chart(fig, use_container_width=True)
        
        # Display exposure table
        exposure = calculate_exposure_table(template, inputs)
        
        st.subheader("Exposure Table")
        exposure_data = {
            'Leg': [leg['leg'] for leg in exposure['legs']],
            'Qty': [leg['qty'] for leg in exposure['legs']],
            'Δ': [f"{leg['delta']:.3f}" for leg in exposure['legs']],
            'Γ': [f"{leg['gamma']:.3e}" for leg in exposure['legs']],
            'Vega (1%)': [f"{leg['vega']:.3f}" for leg in exposure['legs']],
            'Θ/day': [f"{leg['theta']:.4f}" for leg in exposure['legs']]
        }
        
        # Add net row
        exposure_data['Leg'].append('**Net**')
        exposure_data['Qty'].append('')
        exposure_data['Δ'].append(f"**{exposure['net']['delta']:.3f}**")
        exposure_data['Γ'].append(f"**{exposure['net']['gamma']:.3e}**")
        exposure_data['Vega (1%)'].append(f"**{exposure['net']['vega']:.3f}**")
        exposure_data['Θ/day'].append(f"**{exposure['net']['theta']:.4f}**")
        
        st.dataframe(exposure_data, use_container_width=True, hide_index=True)

# Column 2: Live ELFA Narratives
with col2:
    st.subheader("🔥 Chorus of Market Furies")
    
    # Initialize ELFA client
    try:
        api_key = st.secrets.get("ELFA_API_KEY", "")
        if api_key:
            client = ElfaClient(api_key=api_key)
            
            # Refresh button
            if st.button("🔄 Refresh Narratives", use_container_width=True):
                st.session_state.narratives = {}
            
            # Fetch narratives
            if not st.session_state.narratives:
                with st.spinner("Fetching narratives..."):
                    st.session_state.narratives = client.get_narratives()
                    # Also get BTC summary for market combo
                    btc_data = client.get_btc_summary()
                    # Convert to market combo format
                    iv = btc_data.get('vol', {}).get('implied', 0.6) if isinstance(btc_data.get('vol'), dict) else 0.6
                    rv = btc_data.get('vol', {}).get('realized', 0.45) if isinstance(btc_data.get('vol'), dict) else 0.45
                    pcr = btc_data.get('putCallRatio', 1.8)
                    sentiment = btc_data.get('sentiment', 'neutral')
                    trend_slope = btc_data.get('trend', {}).get('slope', 0.0) if isinstance(btc_data.get('trend'), dict) else 0.0
                    
                    st.session_state.market_combo = {
                        'deltaLike': max(-1, min(1, trend_slope * 0.7)),
                        'gammaLike': min(1.0, iv) if iv > 0.5 else 0.3,
                        'vegaLike': max(0, min(1, iv - rv + 0.4)),
                        'thetaLike': 0.3 if (iv - rv) > 0.05 else 0.15,
                        'pcr': pcr,
                        'iv': iv,
                        'rv': rv,
                        'sentiment': sentiment
                    }
        else:
            st.warning("ELFA API key not configured. Using synthetic data.")
            # Use synthetic data
            client = ElfaClient(api_key="")
            st.session_state.narratives = client.get_narratives()
    except Exception as e:
        st.error(f"Error initializing ELFA client: {e}")
        # Fallback to synthetic
        client = ElfaClient(api_key="")
        st.session_state.narratives = client.get_narratives()
    
    # Display narratives
    if st.session_state.narratives:
        narrative_radar = NarrativeRadar()
        
        for asset, data in st.session_state.narratives.items():
            with st.expander(f"{asset} - Momentum: {data.get('momentum', 0.0):.2f}"):
                # Sentiment
                sentiment = data.get('sentiment', 'neutral')
                sentiment_color = {
                    'bullish': '🟢',
                    'bearish': '🔴',
                    'neutral': '🟡'
                }.get(sentiment, '⚪')
                
                st.write(f"**Sentiment:** {sentiment_color} {sentiment.capitalize()}")
                
                # Themes
                themes = data.get('themes', [])
                if themes:
                    st.write("**Themes:**")
                    if isinstance(themes, list):
                        for theme in themes:
                            st.write(f"• {theme}")
                    else:
                        st.write(f"• {themes}")
                
                # Price
                price = data.get('price', 0)
                if price:
                    st.metric("Price", f"${price:,.0f}" if price > 1000 else f"${price:.2f}")
                
                # Volatility info
                vol_data = data.get('volatility', {})
                if isinstance(vol_data, dict):
                    iv = vol_data.get('implied', 0)
                    rv = vol_data.get('realized', 0)
                    if iv and rv:
                        st.write(f"**IV:** {iv:.2%} | **RV:** {rv:.2%}")
    else:
        st.info("No narratives available. Click refresh to fetch.")

# Column 3: Decision Moment
with col3:
    st.subheader("🏛️ Judgment in the Agora")
    
    user_view = st.selectbox(
        "Your Market View",
        options=['bullish', 'bearish', 'neutral', 'hedge'],
        index=2
    )
    
    user_thoughts = st.text_area(
        "Why? (optional)",
        height=100,
        placeholder="Enter your rationale..."
    )
    
    if st.button("🔍 Analyze Trade", use_container_width=True, type="primary"):
        if st.session_state.narratives:
            decision_moment = DecisionMoment()
            
            with st.spinner("Analyzing..."):
                decision = decision_moment.analyze_with_elfa(
                    strategy=strategy,
                    narratives=st.session_state.narratives,
                    market_combo=st.session_state.market_combo,
                    user_view=user_view,
                    thoughts=user_thoughts
                )
            
            # Display score
            score = decision['score']
            score_color = '🟢' if score > 0.7 else ('🟡' if score > 0.4 else '🔴')
            st.metric("Alignment Score", f"{score_color} {score:.2f}")
            
            # Display reasoning
            st.write("**Reasoning:**")
            st.write(decision['reasoning'])
            
            # Display alignment status
            if decision['alignment']:
                st.success("✅ Strategy aligns with current signals.")
            else:
                st.warning("⚠️ Strategy may be suboptimal vs signals.")
            
            # Display alternatives
            if decision.get('alternatives'):
                st.write("**Alternatives:**")
                for alt in decision['alternatives']:
                    st.write(f"• {alt}")
            
            # Display risk notes
            if decision.get('riskNotes'):
                st.write("**Risk:**")
                for risk in decision['riskNotes']:
                    st.write(f"⚠️ {risk}")
            
            # Display growth notes
            if decision.get('growthNotes'):
                st.write("**Growth:**")
                for growth in decision['growthNotes']:
                    st.write(f"📈 {growth}")
        else:
            st.warning("Please fetch narratives first.")

# Footer

                # Update score and streak
                delta = (score - 0.5) * 20
                st.session_state.score += int(delta)
                if score > 0.6:
                    st.session_state.streak += 1
                else:
                    st.session_state.streak = 0
                
                # Store trade
                st.session_state.trades.append({
                    'strategy': strategy,
                    'user_view': user_view,
                    'score': float(score),
                    'underlying': underlying,
                    'strike': strike,
                    'expiry_days': expiry,
                })
                
                # Show streak reward if applicable
                reward_msg = streak_reward(st.session_state.streak)
                if reward_msg:
                    st.success(reward_msg)
                
                # Philosophical commentary
                st.markdown("---")
                st.markdown("### 🏛️ Oracular Banter")
                iv_level = st.session_state.market_combo.get('iv', 0.6) if st.session_state.market_combo else 0.6
                st.markdown(absurd_comment(score, strategy, user_view, iv_level))

                            # Farcaster sharing
                st.markdown("---")
                st.markdown("### 💎 Share to Farcaster")
                
                if st.button("🌐 Cast to Warpcast", use_container_width=True, type="secondary"):
                    try:
                        fc_client = FarcasterClient()
                        
                        # Generate cast text preview
                        cast_preview = fc_client.generate_cast_text(
                            strategy=strategy,
                            user_view=user_view,
                            score=score,
                            philosopher_quote=absurd_comment(score, strategy, user_view, iv_level),
                            cult_rank_name=cult_rank(st.session_state.score),
                            favor_score=st.session_state.score,
                            streak=st.session_state.streak,
                            underlying=underlying,
                            strike=strike,
                            expiry_days=expiry,
                            volatility=volatility
                        )
                        
                        # Show preview
                        with st.expander("👁️ Preview Cast", expanded=True):
                            st.code(cast_preview, language="text")
                        
                        # Try to post
                        result = fc_client.share_trade_result(
                            strategy=strategy,
                            user_view=user_view,
                            score=score,
                            philosopher_quote=absurd_comment(score, strategy, user_view, iv_level),
                            favor_score=st.session_state.score,
                            streak=st.session_state.streak,
                            underlying=underlying,
                            strike=strike,
                            expiry_days=expiry,
                            volatility=volatility
                        )
                        
                        if result.get('success'):
                            cast_hash = result['cast'].get('hash', '')
                            warpcast_url = fc_client.get_warpcast_url(cast_hash) if cast_hash else ''
                            st.success(f"✅ Cast posted successfully!")
                            if warpcast_url:
                                st.markdown(f"[View on Warpcast]({warpcast_url})")
                        else:
                            error_msg = result.get('error', 'Unknown error')
                            if 'not configured' in error_msg:
                                st.info("🔑 Farcaster credentials not configured. Add NEYNAR_API_KEY and FARCASTER_SIGNER_UUID to secrets to enable casting.")
                            else:
                                st.error(f"❌ Failed to post: {error_msg}")
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
# Display cult rank
rank = cult_rank(st.session_state.score)
st.markdown(f"**Cult Rank:** {rank} ({st.session_state.score} favor) | **Orgasmic Streak:** {st.session_state.streak} rites")
st.markdown("")  # spacing

st.divider()
st.caption("Mythic financial orgy — educational demo, not financial advice. May the gods favor your trades.")
