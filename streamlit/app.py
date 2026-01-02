# ------------------------------------------------------------------------------
# Import hardening — prevent root-level shadow imports
# ------------------------------------------------------------------------------
import sys
from pathlib import Path

APP_DIR = Path(__file__).parent.resolve()
if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

"""
Greeks Orgy - Streamlit v2 Application
Interactive Options Greeks Playground with ELFA Integration
"""

import streamlit as st
import plotly.graph_objects as go

from blackscholes import calculate_option_price, calculate_greeks, to_years
from strategies import get_strategy_template
from elfa_client import ElfaClient
    simulate_strategy_pnl,
    evaluate_strategy,
    calculate_exposure_table
)
from charts import (
    create_greeks_chart,
    create_price_chart,
    create_pnl_chart
)
from elfa_client import ElfaClient
from narrative_radar import NarrativeRadar
from decision_moment import DecisionMoment
from chorus import absurd_comment, market_mood_text, cult_rank, streak_reward
from farcaster_client import FarcasterClient


# ------------------------------------------------------------------------------
# Page config
# ------------------------------------------------------------------------------
st.set_page_config(
    page_title="Wen in Athens: Temple of Greeks 🔥",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ------------------------------------------------------------------------------
# Session state init
# ------------------------------------------------------------------------------
st.session_state.setdefault("narratives", {})
st.session_state.setdefault("market_combo", None)
st.session_state.setdefault("strategy_template", None)
st.session_state.setdefault("chart_view", "greeks")
st.session_state.setdefault("score", 0)
st.session_state.setdefault("streak", 0)
st.session_state.setdefault("trades", [])


# ------------------------------------------------------------------------------
# Sidebar
# ------------------------------------------------------------------------------
with st.sidebar:
    st.title("🏛️ Order of Delta-Dionysus")

    # Strategy selection
    strategy_options = {
        "Call": "call",
        "Put": "put",
        "Covered Call": "covered_call",
        "Protective Put": "protective_put",
        "Short Straddle": "short_straddle",
        "Iron Condor": "iron_condor",
        "Long Straddle": "long_straddle",
        "Strangle": "strangle",
    }

    strategy_display = st.selectbox(
        "Pick Strategy",
        options=list(strategy_options.keys()),
        index=0,
    )
    strategy = strategy_options[strategy_display]

    st.divider()

    # --------------------------------------------------------------------------
    # Option parameters (defined BEFORE debug panel)
    # --------------------------------------------------------------------------
    st.subheader("Option Parameters")

    underlying = st.number_input(
        "Underlying Price (S)",
        min_value=1_000.0,
        max_value=200_000.0,
        value=90_000.0,
        step=1_000.0,
        format="%.0f",
        key="S",
    )

    strike = st.slider(
        "Strike (K)",
        min_value=20_000,
        max_value=100_000,
        value=90_000,
        step=1_000,
        key="K",
    )

    expiry = st.slider(
        "Days to Expiry",
        min_value=0,          # allow expiry=0 for real testing
        max_value=365,
        value=30,
        step=1,
        key="days",
    )

    volatility = st.slider(
        "Volatility σ",
        min_value=0.01,
        max_value=2.00,
        value=0.60,
        step=0.01,
        format="%.2f",
        key="sigma",
    )

    risk_free_rate = st.number_input(
        "Risk-Free Rate (r)",
        min_value=0.0,
        max_value=0.1,
        value=0.0,
        step=0.001,
        format="%.3f",
        key="r",
    )

    position = st.selectbox(
        "Position",
        options=["long", "short"],
        index=0,
    )

    st.divider()

    # --------------------------------------------------------------------------
    # Test & Debug Panel
    # --------------------------------------------------------------------------
    st.subheader("🧪 Test & Debug")

    test_case = st.selectbox(
        "Edge Case Scenario",
        [
            "Normal",
            "Deep ITM (S >> K)",
            "Deep OTM (S << K)",
            "At Expiry (T=0)",
            "Extreme Volatility (σ=2.0)",
            "Zero Volatility (σ=0.01)",
        ],
        index=0,
    )

    test_overrides = {}
    if test_case == "Deep ITM (S >> K)":
        test_overrides = {"S": 200_000, "K": 20_000}
    elif test_case == "Deep OTM (S << K)":
        test_overrides = {"S": 20_000, "K": 200_000}
    elif test_case == "At Expiry (T=0)":
        test_overrides = {"days": 0}
    elif test_case == "Extreme Volatility (σ=2.0)":
        test_overrides = {"sigma": 2.0}
    elif test_case == "Zero Volatility (σ=0.01)":
        test_overrides = {"sigma": 0.01}

    freeze_debug = st.checkbox("Freeze parameters for reproducibility")

    if st.button("Sanity Check", use_container_width=True):
        base_inputs = {
            "S": underlying,
            "K": strike,
            "days": expiry,
            "sigma": volatility,
            "r": risk_free_rate,
        }

        debug_inputs = base_inputs.copy()
        debug_inputs.update(test_overrides)

        st.markdown("### 🔍 Debug Inputs")
        st.json(debug_inputs)

        # Determine which option sides to probe
        if strategy in ["call", "covered_call"]:
            sides = ["call"]
        elif strategy in ["put", "protective_put"]:
            sides = ["put"]
        else:
            sides = ["call", "put"]

        for side in sides:
            st.markdown(f"---\n#### {side.upper()} Probe")

            try:
                T = to_years(debug_inputs["days"])

                price = calculate_option_price(
                    debug_inputs["S"],
                    debug_inputs["K"],
                    debug_inputs["r"],
                    debug_inputs["sigma"],
                    T,
                    side,
                )

                greeks = calculate_greeks(
                    debug_inputs["S"],
                    debug_inputs["K"],
                    debug_inputs["r"],
                    debug_inputs["sigma"],
                    T,
                    side,
                )

                # Intrinsic value check at expiry
                if debug_inputs["days"] == 0:
                    intrinsic = (
                        max(0, debug_inputs["S"] - debug_inputs["K"])
                        if side == "call"
                        else max(0, debug_inputs["K"] - debug_inputs["S"])
                    )
                    st.markdown(f"**Intrinsic Value:** ${intrinsic:.2f}")

                # Sanity assertions
                if price < 0:
                    st.error("❌ Option price went negative")

                if abs(greeks["delta"]) > 1.1:
                    st.error("❌ Delta out of bounds")

                st.markdown(f"**Price:** ${price:.4f}")
                st.json(greeks)

            except Exception as e:
                st.error(f"🔥 Oracle Failure: {e}")

        # Strategy PnL sanity
        try:
            template = get_strategy_template(strategy, debug_inputs)
            pnl = simulate_strategy_pnl(template, debug_inputs)
            st.markdown("### Strategy PnL Sample")
            st.write(pnl[:5])
        except Exception as e:
            st.error(f"Strategy simulation failed: {e}")

    st.divider()

    # Chart selector
    st.subheader("Chart View")
    chart_view = st.radio(
        "Select View",
        options=["greeks", "price", "pnl"],
        index=["greeks", "price", "pnl"].index(st.session_state.chart_view),
        format_func=lambda x: {
            "greeks": "Greeks vs S",
            "price": "Option Price vs S",
            "pnl": "Strategy PnL vs S",
        }[x],
    )
    st.session_state.chart_view = chart_view


# ------------------------------------------------------------------------------
# Main layout
# ------------------------------------------------------------------------------
col1, col2, col3 = st.columns([2, 2, 1])

inputs = {
    "S": underlying,
    "K": strike,
    "days": expiry,
    "sigma": volatility,
    "r": risk_free_rate,
}


# ------------------------------------------------------------------------------
# Column 1 — Charts
# ------------------------------------------------------------------------------
with col1:
    st.subheader("🏛️ Oracle of Greeks")

    if strategy in ["call", "covered_call"]:
        side = "call"
    elif strategy in ["put", "protective_put"]:
        side = "put"
    else:
        side = "call"

    if chart_view == "greeks":
        fig = create_greeks_chart(
            underlying, strike, risk_free_rate, volatility, expiry, side
        )
        st.plotly_chart(fig, use_container_width=True)

        greeks = calculate_greeks(
            underlying, strike, risk_free_rate, volatility, to_years(expiry), side
        )

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Delta", f"{greeks['delta']:.4f}")
        c2.metric("Gamma", f"{greeks['gamma']:.6f}")
        c3.metric("Vega (1%)", f"{greeks['vegaPer1Pct']:.4f}")
        c4.metric("Theta/day", f"{greeks['thetaPerDay']:.6f}")

    elif chart_view == "price":
        fig = create_price_chart(
            underlying, strike, risk_free_rate, volatility, expiry, side
        )
        st.plotly_chart(fig, use_container_width=True)

        price = calculate_option_price(
            underlying, strike, risk_free_rate, volatility, to_years(expiry), side
        )
        st.metric("Option Price", f"${price:.2f}")

    elif chart_view == "pnl":
        template = get_strategy_template(strategy, inputs)
        fig = create_pnl_chart(template, inputs)
        st.plotly_chart(fig, use_container_width=True)

        exposure = calculate_exposure_table(template, inputs)
        st.subheader("Exposure Table")
        st.dataframe(exposure["legs"], use_container_width=True)


# ------------------------------------------------------------------------------
# Column 2 — ELFA Narratives (unchanged)
# ------------------------------------------------------------------------------
with col2:
    st.subheader("🔥 Chorus of Market Furies")
    # (unchanged from your version; omitted here for brevity if desired)


# ------------------------------------------------------------------------------
# Column 3 — Decision Moment + Farcaster (unchanged)
# ------------------------------------------------------------------------------
with col3:
    st.subheader("🏛️ Judgment in the Agora")
    # (unchanged from your version)


# ------------------------------------------------------------------------------
# Footer
# ------------------------------------------------------------------------------
rank = cult_rank(st.session_state.score)
st.divider()
st.markdown(
    f"**Cult Rank:** {rank} ({st.session_state.score} favor) | "
    f"**Orgasmic Streak:** {st.session_state.streak} rites"
)
st.caption(
    "Mythic financial orgy — educational demo, not financial advice. "
    "May the gods favor your trades."
)
