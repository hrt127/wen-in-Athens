---
name: Streamlit v2 Conversion
overview: Convert the HTML/JS Options Greeks Playground to a Streamlit application with ELFA integration, creating a modular Python codebase with a 3-column "Greeks Orgy" layout for live data and rapid iteration.
todos:
  - id: setup_structure
    content: Create streamlit/ directory and .streamlit/ config directory with requirements.txt and secrets template
    status: completed
  - id: convert_blackscholes
    content: Port Black-Scholes calculations from js/blackscholes.js to streamlit/blackscholes.py using Python/numpy/scipy
    status: completed
    dependencies:
      - setup_structure
  - id: port_strategies
    content: Convert strategy templates and evaluation logic from js/strategies.js to streamlit/strategies.py
    status: completed
    dependencies:
      - convert_blackscholes
  - id: create_elfa_modules
    content: Create elfa_client.py, narrative_radar.py, and decision_moment.py modules (stubs if not provided, matching expected interface)
    status: completed
    dependencies:
      - setup_structure
  - id: build_streamlit_app
    content: "Create streamlit/app.py with 3-column layout: Greeks chart, ELFA narratives, Decision moment"
    status: completed
    dependencies:
      - convert_blackscholes
      - port_strategies
      - create_elfa_modules
  - id: create_plotly_charts
    content: Implement Plotly visualization functions for Greeks, Price, and PnL charts
    status: completed
    dependencies:
      - convert_blackscholes
      - port_strategies
  - id: update_docs
    content: Update README.md with v2 Streamlit information and deployment instructions, update .gitignore
    status: completed
    dependencies:
      - build_streamlit_app
  - id: todo-1765790516953-nhxekce2v
    content: ""
    status: pending
---

# Streamlit v2 Conversion Plan

## Overview

Convert the current HTML/JavaScript application to a Streamlit-based Python application (v2) while keeping v1 in the root directory. The new version will integrate ELFA client tools and provide a multi-column layout for enhanced visualization and live data integration.

## Project Structure

```
wen-in-Athens/
├── index.html              # v1 (keep existing)
├── js/                     # v1 JavaScript modules
├── css/                    # v1 styles
├── streamlit/              # v2 Streamlit application
│   ├── app.py             # Main Streamlit app
│   ├── blackscholes.py    # Python Black-Scholes implementation
│   ├── strategies.py      # Strategy templates and evaluation
│   ├── elfa_client.py     # ELFA API client (to be provided/created)
│   ├── narrative_radar.py # Narrative analysis (to be provided/created)
│   ├── decision_moment.py  # Trade decision analysis (to be provided/created)
│   └── requirements.txt   # Python dependencies
├── .streamlit/            # Streamlit config (for secrets)
│   └── secrets.toml       # API keys (template)
└── README.md              # Updated with v1/v2 info
```

## Implementation Steps

### 1. Create Streamlit Directory Structure

- Create `streamlit/` directory
- Set up `requirements.txt` with: streamlit, plotly, numpy, scipy (for normCDF/normPDF)
- Create `.streamlit/secrets.toml` template for ELFA_API_KEY

### 2. Convert Black-Scholes to Python

- Port functions from `js/blackscholes.js` to `streamlit/blackscholes.py`:
  - `normPDF()`, `normCDF()` (use scipy.stats or custom implementation)
  - `d1()`, `d2()` helper functions
  - `calculate_option_price()` for call/put
  - `calculate_greeks()` returning delta, gamma, vega, theta
  - `apply_position_sign()` for long/short
- Maintain same mathematical accuracy as JS version

### 3. Port Strategy System

- Convert `js/strategies.py` logic to `streamlit/strategies.py`:
  - Strategy templates (covered_call, protective_put, short_straddle, iron_condor, long_straddle)
  - `simulate_strategy_pnl()` function
  - `evaluate_strategy()` with market condition logic
  - Exposure table calculation

### 4. Create ELFA Integration Modules

- **elfa_client.py**: 
  - `ElfaClient` class with `__init__(api_key)`
  - `get_narratives()` method returning dict of asset -> {momentum, sentiment, themes}
  - Handle API calls to ELFA endpoints
  - Error handling and fallback to synthetic data
- **narrative_radar.py**:
  - `NarrativeRadar` class for analyzing market narratives
  - Methods to extract themes and momentum from ELFA data
- **decision_moment.py**:
  - `DecisionMoment` class for trade analysis
  - `analyze_with_elfa(strategy, narratives)` returning {score, reasoning}
  - Integrate strategy evaluation with ELFA narrative data

### 5. Build Main Streamlit App (app.py)

- **Page Config**: Wide layout, title "Greeks Orgy 🔥"
- **Sidebar**:
  - Strategy selector (Call, Put, Iron Condor, Strangle, etc.)
  - Strike slider (20000-60000, default 40000)
  - Days to expiry slider (1-90, default 30)
  - Underlying price input
  - Volatility input
  - Position (Long/Short) selector
- **Main Layout - 3 Columns**:
  - **Column 1 (2x width)**: Greeks Visualization
    - Plotly chart showing Greeks vs underlying price
    - Toggle between Greeks view, Price view, PnL view
    - Interactive Plotly figure
  - **Column 2 (2x width)**: Live ELFA Narratives
    - Initialize ElfaClient with secrets
    - Display narratives in expandable sections
    - Show momentum, sentiment, themes per asset
    - Auto-refresh or manual refresh button
  - **Column 3 (1x width)**: Decision Moment
    - "Analyze Trade" button
    - Display decision score and reasoning
    - Show strategy alignment with narratives
    - Risk notes and alternatives

### 6. Create Plotly Visualization Functions

- `create_greeks_chart(strike, expiry, underlying, vol, ...)`:
  - Generate price range data
  - Calculate Greeks across range
  - Create Plotly figure with subplots or multiple traces
  - Color-coded lines for Delta, Gamma, Vega, Theta
  - Interactive tooltips and zoom
- `create_price_chart()`: Option price vs underlying
- `create_pnl_chart()`: Strategy PnL visualization

### 7. Streamlit Cloud Deployment Setup

- Create `.streamlit/config.toml` for app configuration
- Add `packages.txt` if needed for system dependencies
- Update README with Streamlit Cloud deployment instructions
- Document secrets setup in Streamlit Cloud dashboard

### 8. Testing & Validation

- Verify Black-Scholes calculations match JS version
- Test ELFA integration with real API (when available)
- Test fallback behavior when API unavailable
- Validate strategy PnL calculations
- Test responsive layout on different screen sizes

## Key Files to Create/Modify

### New Files

- `streamlit/app.py` - Main Streamlit application
- `streamlit/blackscholes.py` - Python Black-Scholes implementation
- `streamlit/strategies.py` - Strategy system in Python
- `streamlit/elfa_client.py` - ELFA API client (stub if not provided)
- `streamlit/narrative_radar.py` - Narrative analysis (stub if not provided)
- `streamlit/decision_moment.py` - Decision analysis (stub if not provided)
- `streamlit/requirements.txt` - Python dependencies
- `.streamlit/secrets.toml` - Secrets template
- `.streamlit/config.toml` - Streamlit configuration

### Modified Files

- `README.md` - Add v2 Streamlit section and deployment instructions
- `.gitignore` - Add Python/Streamlit ignores (.streamlit/secrets.toml, **pycache**, *.pyc, etc.)

## Dependencies

- streamlit >= 1.28.0
- plotly >= 5.17.0
- numpy >= 1.24.0
- scipy >= 1.11.0 (for statistical functions)

## Notes

- ELFA modules (elfa_client, narrative_radar, decision_moment) will be provided by user or created as stubs matching expected interface
- Maintain mathematical consistency with JS version
- Use Streamlit's session state for maintaining app state
- Implement caching with @st.cache_data for expensive calculations
- Handle API errors gracefully with fallback data