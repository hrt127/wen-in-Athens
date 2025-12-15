# Wen in Athens — Options Greeks Playground

An interactive, client-only educational application for learning options Greeks (Delta, Gamma, Vega, Theta) with live Bitcoin market context. Built as a single-file HTML application with vanilla JavaScript and Chart.js.

## 🎯 Overview

**Wen in Athens** is designed to help users understand options trading concepts through hands-on experimentation. The app provides real-time calculations, interactive visualizations, and guided learning experiences to make complex financial concepts accessible.

### Key Concepts Covered
- **Delta (Δ)**: Price sensitivity — how much the option price changes when the underlying asset moves $1
- **Gamma (Γ)**: Rate of change of Delta — how quickly Delta changes as the underlying moves
- **Vega**: Volatility sensitivity — how much the option price changes when implied volatility increases by 1%
- **Theta (Θ)**: Time decay — how much value the option loses per day as time passes

## ✨ Features

### Core Functionality
- **Interactive Controls**: Sliders and inputs for adjusting option parameters (strike, expiry, volatility, underlying price)
- **Real-time Calculations**: Instant Black-Scholes option pricing and Greeks calculations
- **Multiple Chart Views**: 
  - Greeks vs. underlying price
  - Option price vs. underlying price
  - Strategy PnL vs. underlying price
- **Strategy Builder**: Evaluate and simulate common options strategies:
  - Covered Call
  - Protective Put
  - Short Straddle
  - Iron Condor
  - Long Straddle

### Educational Features
- **Guided Onboarding**: Step-by-step tutorial for new users
- **Quiz Mode**: Interactive questions with scoring and streak tracking
- **Badge System**: Earn badges for mastering different Greeks concepts
- **Strategy Guidance**: AI-like evaluation of strategy choices based on market conditions
- **Exposure Tables**: Multi-leg strategy analysis showing net Greeks exposure

### Market Integration
- **BTC Market Context**: Live Bitcoin price and market sentiment analysis
- **Market Signal Parsing**: Delta-like, Gamma-like, Vega-like indicators from market data
- **Strategy Recommendations**: Context-aware suggestions based on current market conditions

## 🚀 Getting Started

### Prerequisites
- A modern web browser (Chrome, Firefox, Safari, Edge)
- Python 3 (optional, for local server)

### Installation

1. **Clone or download the repository**
   ```bash
   git clone <repository-url>
   cd wen-in-Athens
   ```

2. **Run the application**

   **Option 1: Direct file opening**
   - Simply open `index.html` in your web browser
   - Note: Some features may be limited due to CORS restrictions

   **Option 2: Local web server (recommended)**
   ```bash
   # Python 3
   python3 -m http.server 8080
   
   # Python 2
   python -m SimpleHTTPServer 8080
   
   # Node.js (with http-server)
   npx http-server -p 8080
   ```

3. **Access the application**
   - Open your browser and navigate to `http://localhost:8080`

## 📖 Usage Guide

### First Time Users

1. **Onboarding Tour**: When you first open the app, you'll see a guided tour:
   - Step 1: Welcome and overview
   - Step 2: Choose a strategy to explore
   - Step 3: Learn about adjusting parameters and understanding Greeks
   - Step 4: Wrap-up and tips
   - You can skip the tour or restart it anytime using the "🔄 Restart Tour" button

2. **Basic Workflow**:
   - Adjust sliders in the left panel to change option parameters
   - Click "Apply" to update calculations
   - Switch chart views to see different perspectives
   - Try the quiz mode to test your understanding

### Using the Controls

**Input Parameters:**
- **S (Underlying Price)**: Current price of the underlying asset (default: $90,000)
- **K (Strike Price)**: Strike price of the option (default: $90,000)
- **Days to Expiry**: Time remaining until expiration (1-365 days)
- **Volatility σ**: Implied volatility as a decimal (0.01-2.00, default: 0.6)
- **Side**: Choose Call or Put option
- **Position**: Long or Short position

**Chart Views:**
- **Greeks vs S**: Shows how Delta, Gamma, Vega, and Theta change with underlying price
- **Option Price vs S**: Shows option price across different underlying prices
- **Strategy PnL vs S**: Shows profit/loss for multi-leg strategies

### Quiz Mode

1. Click "Next Q" to start a new question
2. Select your answer from the multiple-choice options
3. Click "Submit" to check your answer
4. Earn badges by answering questions correctly (3 correct answers per Greek)
5. Track your score and streak

### Strategy Evaluation

1. Select a strategy from the dropdown (Covered Call, Protective Put, etc.)
2. Choose your market view (Bullish, Bearish, Neutral, Hedging)
3. Optionally add your rationale
4. Click "Evaluate" to get strategy guidance
5. Click "Apply to sim" to visualize the strategy's PnL on the chart

### Badge System

Earn badges by correctly answering quiz questions:
- **Delta Master**: 3 correct Delta-related questions
- **Gamma Guru**: 3 correct Gamma-related questions
- **Vega Explorer**: 3 correct Vega-related questions
- **Theta Ticker**: 3 correct Theta-related questions

Badges are saved in browser localStorage and persist across sessions.

## 🏗️ Architecture

### Technology Stack
- **Frontend**: Vanilla JavaScript (ES6+)
- **Visualization**: Chart.js 4.4.0
- **Styling**: CSS3 with CSS Variables
- **Storage**: Browser localStorage for badges and preferences

### Project Structure
```
wen-in-Athens/
├── index.html          # Single-file application (HTML, CSS, JavaScript)
├── README.md          # This file
└── assets/            # (Empty, reserved for future assets)
```

### Key Components

1. **Black-Scholes Calculator**: Core pricing and Greeks calculations
2. **Chart Manager**: Chart.js wrapper for interactive visualizations
3. **Quiz Engine**: Question generation and scoring system
4. **Badge System**: Progress tracking and achievement system
5. **Strategy Simulator**: Multi-leg strategy PnL calculation
6. **Market Data Parser**: BTC market signal extraction and analysis
7. **Onboarding System**: Guided tour and tutorial

## 🔧 Technical Details

### Black-Scholes Implementation

The app implements the Black-Scholes-Merton model for European options:

- **Option Pricing**: Standard B-S formula for calls and puts
- **Greeks Calculations**:
  - Delta: First derivative with respect to underlying price
  - Gamma: Second derivative with respect to underlying price
  - Vega: First derivative with respect to volatility
  - Theta: First derivative with respect to time (per day)

### Market Data Integration

The app attempts to fetch BTC market data from `https://app.elfa.ai/api/btc/summary`. If unavailable, it falls back to synthetic data and text parsing for demonstration purposes.

### Browser Compatibility

- Modern browsers with ES6+ support
- localStorage support required for badges
- Canvas API for Chart.js

## 📚 Learning Resources

### Understanding Options Greeks

- **Delta**: Think of it as a "steering wheel" — how the option price moves when the underlying moves
- **Gamma**: The "sensitivity of the steering" — how quickly Delta changes
- **Vega**: A "volatility compass" — sensitivity to implied volatility changes
- **Theta**: A "time decay clock" — how the option loses value over time

### Common Strategies

- **Covered Call**: Own stock + sell call option (income generation)
- **Protective Put**: Own stock + buy put option (downside protection)
- **Straddle**: Buy/sell call and put at same strike (volatility play)
- **Iron Condor**: Four-leg strategy with limited risk and profit (neutral market)

## ⚠️ Important Disclaimers

**This is an educational tool, not financial advice.**

- All calculations are for educational purposes only
- Real options trading involves additional factors not modeled here
- Market conditions, liquidity, and transaction costs are not accounted for
- Always do your own research and consult with financial professionals before making trading decisions

## 🛠️ Development

### Extending the Application

The code is modular and well-organized. Key areas for extension:

1. **Add New Strategies**: Extend `STRATEGY_TEMPLATES` object
2. **Add Quiz Questions**: Extend `QUIZ_TEMPLATES` array
3. **Custom Market Data**: Modify `fetchBTCData()` and parsing functions
4. **Additional Greeks**: Extend `calculateGreeks()` function (e.g., Rho)

### Code Organization

- **Utilities**: Mathematical functions (normPDF, normCDF, Black-Scholes helpers)
- **State Management**: Centralized `state` object
- **DOM Management**: Centralized `els` object for element references
- **Event Wiring**: `wire()` function for event listeners

## 📝 License

[Specify your license here]

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional strategies
- More quiz questions
- Enhanced market data integration
- Mobile responsiveness improvements
- Accessibility enhancements

## 📧 Contact

[Add contact information or issue tracker link]

---

**Built with ❤️ for learning options trading**
