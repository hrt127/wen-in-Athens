# Streamlit v2 - Greeks Orgy 🔥

Streamlit version of the Options Greeks Playground with ELFA integration.

## Quick Start

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure secrets:**
   - Copy `.streamlit/secrets.toml` from parent directory
   - Add your ELFA API key (or leave empty for synthetic data)

3. **Run the app:**
   ```bash
   streamlit run app.py
   ```

## Features

- **3-Column Layout**: Greeks visualization, ELFA narratives, Decision moment
- **Live ELFA Integration**: Real-time market narratives and sentiment
- **Interactive Plotly Charts**: Enhanced visualizations
- **Strategy Analysis**: AI-powered trade decision analysis

## Modules

- `app.py` - Main Streamlit application
- `blackscholes.py` - Black-Scholes calculations
- `strategies.py` - Strategy templates and evaluation
- `charts.py` - Plotly visualization functions
- `elfa_client.py` - ELFA API client
- `narrative_radar.py` - Narrative analysis
- `decision_moment.py` - Trade decision analysis

## Deployment

See main README.md for Streamlit Cloud deployment instructions.

