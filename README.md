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
├── index.html              # Main HTML file
├── manifest.json           # PWA manifest
├── .gitignore             # Git ignore rules
├── css/
│   ├── main.css           # Main styles
│   └── onboarding.css     # Onboarding styles
├── js/
│   ├── blackscholes.js    # Black-Scholes calculations
│   ├── strategies.js      # Strategy templates & evaluation
│   ├── chart.js           # Chart.js wrapper
│   ├── onboarding.js     # Onboarding system
│   └── app.js            # Main application logic
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

## 🌐 GitHub Pages Deployment

This project is configured for GitHub Pages deployment:

1. Push to `main` branch
2. Go to: `https://github.com/hrt127/wen-in-Athens/settings/pages`
3. Set Source: "Deploy from a branch"
4. Branch: "main" → `/root`
5. Save

Your app will be live at: **`https://hrt127.github.io/wen-in-Athens/`** 🎉

## ✨ Features

- Interactive option pricing with Black-Scholes model
- Real-time Greeks calculations (Delta, Gamma, Vega, Theta)
- Multiple chart views (Greeks, Price, PnL)
- Strategy builder and evaluation
- Quiz mode with badge system
- Guided onboarding tour
- BTC market context integration

## ⚠️ Disclaimer

**This is an educational tool, not financial advice.** Always do your own research and consult with financial professionals before making trading decisions.

## 📝 License

[Specify your license here]

---

**Built with ❤️ for learning options trading**
