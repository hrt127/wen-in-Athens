# Wen in Athens — Options Greeks Playground

An interactive, client-only educational application for learning options Greeks (Delta, Gamma, Vega, Theta) with live Bitcoin market context.

## 🚀 Quick Start

### Option 1: Direct file opening
Simply open `index.html` in your web browser.

### Option 2: Local web server (recommended)
```bash
# Python 3
python3 -m http.server 8080

# Python 2
python -m SimpleHTTPServer 8080

# Node.js (with http-server)
npx http-server -p 8080
```

Then open `http://localhost:8080` in your browser.

## 📁 Project Structure

```
wen-in-Athens/
├── index.html              # v1: Main HTML file
├── manifest.json           # v1: PWA manifest
├── .gitignore             # Git ignore rules
├── css/                    # v1: Stylesheets
│   ├── main.css           # Main styles
│   └── onboarding.css     # Onboarding styles
├── js/                     # v1: JavaScript modules
│   ├── blackscholes.js    # Black-Scholes calculations
│   ├── strategies.js      # Strategy templates & evaluation
│   ├── chart.js           # Chart.js wrapper
│   ├── onboarding.js     # Onboarding system
│   └── app.js            # Main application logic
├── streamlit/              # v2: Streamlit application
│   ├── app.py            # Main Streamlit app
│   ├── blackscholes.py   # Python Black-Scholes implementation
│   ├── strategies.py     # Strategy system in Python
│   ├── charts.py         # Plotly visualization functions
│   ├── elfa_client.py    # ELFA API client
│   ├── narrative_radar.py # Narrative analysis
│   ├── decision_moment.py # Trade decision analysis
│   └── requirements.txt  # Python dependencies
├── .streamlit/            # Streamlit configuration
│   ├── config.toml       # Streamlit config
│   └── secrets.toml      # API keys template
├── assets/
│   └── images/           # Images (icons, etc.)
└── docs/
    ├── README.md         # Full documentation
    ├── TECHNICAL.md      # Technical documentation
    ├── CONTRIBUTING.md   # Contribution guidelines
    └── QUICK_REFERENCE.md # Quick reference guide
```

## 📚 Documentation

- **[Full Documentation](docs/README.md)** - Complete user and developer guide
- **[Technical Docs](docs/TECHNICAL.md)** - Technical implementation details
- **[Contributing](docs/CONTRIBUTING.md)** - How to contribute
- **[Quick Reference](docs/QUICK_REFERENCE.md)** - Quick reference card

## 🌐 Deployment

### v1 (HTML/JS) - GitHub Pages

1. Push to `main` branch
2. Go to: `https://github.com/hrt127/wen-in-Athens/settings/pages`
3. Set Source: "Deploy from a branch"
4. Branch: "main" → `/root`
5. Save

Your app will be live at: **`https://hrt127.github.io/wen-in-Athens/`** 🎉

### v2 (Streamlit) - Streamlit Cloud

1. **Install dependencies:**
   ```bash
   cd streamlit
   pip install -r requirements.txt
   ```

2. **Configure secrets:**
   - Copy `.streamlit/secrets.toml` and add your ELFA API key
   - For Streamlit Cloud: Add secrets via the dashboard

3. **Run locally:**
   ```bash
   # From project root
   streamlit run streamlit/app.py
   
   # Or from streamlit directory
   cd streamlit
   streamlit run app.py
   ```

4. **Deploy to Streamlit Cloud:**
   - Push your code to GitHub
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Connect your repository
   - Set main file path: `streamlit/app.py`
   - Add secrets in the dashboard (ELFA_API_KEY)
   - Deploy!

Your Streamlit app will be live at: **`https://your-app-name.streamlit.app`** 🚀

## ✨ Features

### v1 (HTML/JS)
- Interactive option pricing with Black-Scholes model
- Real-time Greeks calculations (Delta, Gamma, Vega, Theta)
- Multiple chart views (Greeks, Price, PnL)
- Strategy builder and evaluation
- Quiz mode with badge system
- Guided onboarding tour
- BTC market context integration

### v2 (Streamlit) - NEW!
- All v1 features plus:
- **Live ELFA Integration**: Real-time market narratives and sentiment
- **3-Column Layout**: Greeks visualization, ELFA narratives, Decision moment
- **Interactive Plotly Charts**: Enhanced visualizations with zoom and hover
- **Strategy Analysis**: AI-powered trade decision analysis with ELFA data
- **Rapid Iteration**: Easy parameter adjustment with live updates

## ⚠️ Disclaimer

**This is an educational tool, not financial advice.** Always do your own research and consult with financial professionals before making trading decisions.

## 📝 License

[Specify your license here]

---

**Built with ❤️ for learning options trading**
