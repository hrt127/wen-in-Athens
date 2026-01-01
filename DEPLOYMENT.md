# 🏛️ Deployment Guide: Temple of Greeks (Wen in Athens)

Welcome, initiate! Follow this sacred scroll to summon the Temple of Greeks into existence.

## 🔥 Quick Start: Deploy to Streamlit Cloud

The fastest path to orgiastic enlightenment.

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))
- Optional: ELFA API key for live market narratives (get at [elfa.ai](https://elfa.ai))

### Deployment Steps

1. **Fork or clone this repository**
   ```bash
   git clone https://github.com/hrt127/wen-in-Athens.git
   cd wen-in-Athens
   ```

2. **Visit [share.streamlit.io](https://share.streamlit.io) and sign in**

3. **Click "New app"**

4. **Configure your app:**
   - Repository: `your-username/wen-in-Athens`
   - Branch: `main`
   - Main file path: `streamlit/app.py`
   - App URL: Choose your temple name (e.g., `temple-of-greeks`)

5. **Add secrets (optional but recommended):**
   - Click "Advanced settings"
   - Add to secrets:
   ```toml
   ELFA_API_KEY = "your-elfa-api-key-here"
   ```
   - Without ELFA key, the app uses synthetic demo data

6. **Deploy!**
   - Click "Deploy"
   - Wait ~2-3 minutes for the gods to align
   - Your temple will be live at: `https://[your-app-name].streamlit.app`

## 🎮 Local Development

For those who wish to experiment in their own chambers.

### Setup

```bash
# Clone the repository
git clone https://github.com/hrt127/wen-in-Athens.git
cd wen-in-Athens

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd streamlit
pip install -r requirements.txt

# Create secrets file (optional)
mkdir -p .streamlit
echo 'ELFA_API_KEY = "your-key"' > .streamlit/secrets.toml

# Run the temple
streamlit run app.py
```

The temple will open at `http://localhost:8501`

## 🌟 Features Explained

### Ancient Greek Theme
- **Order of Delta-Dionysus**: The sidebar where strategies are crafted
- **Oracle of Greeks**: Visualizations of the sacred Greeks (Delta, Gamma, Vega, Theta)
- **Chorus of Market Furies**: Live ELFA narratives whispering market truths
- **Judgment in the Agora**: Where your trades are judged by philosopher-oracles

### Scoring & Progression
- **Cult Rank**: Earn favor through wise trades
  - Exiled Bean Farmer (<0)
  - Initiate of Implied Vol (0-20)
  - Keeper of Gamma Goblets (20-50)
  - Priest of Perpetual Theta (50-100)
  - Archon of the Straddle (100-200)
  - Vega Whisperer (200-350)
  - Supreme Hedger of the Orgy (350+)

- **Orgasmic Streak**: Consecutive successful rites
  - 3 streak: Seat at the symposium
  - 5 streak: Diluted wine offering
  - 10 streak: Oracle invites you to inner temple
  - 20 streak: Your name carved in marble!

### Philosopher Commentary
After each trade analysis, a random philosopher offers absurd wisdom:
- Diogenes critiques your hedges
- Socrates drinks and philosophizes
- Heraclitus hoards volatility
- Plato judges from his cave

## 🛠️ Customization

### Adding More Philosophers
Edit `streamlit/chorus.py`:
```python
PHILOSOPHERS = [
    "Your philosopher, doing something absurd",
    ...
]
```

### Adjusting Cult Ranks
Edit the `cult_rank()` function in `chorus.py` to change thresholds.

### Modifying Strategies
The strategy templates are in the `strategies.py` module.

## 📦 Project Structure

```
wen-in-Athens/
├── streamlit/
│   ├── app.py              # Main application
│   ├── chorus.py           # Philosopher commentary engine
│   ├── blackscholes.py     # Options pricing
│   ├── strategies.py       # Strategy templates
│   ├── charts.py           # Plotly visualizations
│   ├── elfa_client.py      # ELFA API integration
│   ├── narrative_radar.py  # Market narrative processing
│   ├── decision_moment.py  # Trade analysis
│   └── requirements.txt    # Python dependencies
├── index.html              # V1 standalone version
├── README.md
└── DEPLOYMENT.md           # This file
```

## 🐛 Troubleshooting

**"Module not found" errors:**
- Ensure you're in the `streamlit/` directory when installing requirements
- Try: `pip install -r streamlit/requirements.txt` from root

**ELFA narratives not showing:**
- Check that `ELFA_API_KEY` is set in secrets
- App will work without it using synthetic data

**App won't start:**
- Verify Python 3.8+ is installed
- Check all dependencies are installed
- Look for errors in the Streamlit Cloud logs

**Philosophical commentary too mild:**
- This is a feature, not a bug
- The absurdity is intentionally restrained
- Edit `chorus.py` to add more chaos

## 🎯 Next Steps

Once deployed:
1. **Test a trade**: Pick a strategy, set parameters, click "Analyze Trade"
2. **Watch your rank**: Make wise trades to ascend the cult hierarchy
3. **Chase streaks**: Can you reach 20 consecutive rites?
4. **Customize**: Fork and add your own absurdist touches
5. **Share**: Send your temple URL to fellow degens

## 📜 License & Disclaimer

**Educational demo — not financial advice.**

This is a learning tool for understanding options Greeks and strategies. Real markets are more chaotic than any philosopher could predict. The gods favor those who do their own research.

May Dionysus bless your volatility.

---

*"To hedge is to admit mortality. The immortals laugh at your spreads."* — Chorus of Market Furies
