# Quick Reference Guide — Wen in Athens

A quick reference card for common tasks and concepts in the Options Greeks Playground.

## Keyboard Shortcuts

Currently, the app is primarily mouse/touch-driven. Keyboard shortcuts may be added in future versions.

## Common Tasks

### Adjust Option Parameters
1. Use sliders in left panel
2. Or type values in number inputs
3. Click "Apply" to update

### Switch Chart Views
- Click "Greeks vs S" — See all Greeks
- Click "Option Price vs S" — See option pricing
- Click "Strategy PnL vs S" — See strategy profit/loss

### Start Quiz
1. Click "Next Q" in Quiz Mode section
2. Select an answer
3. Click "Submit"
4. Track your score and earn badges!

### Evaluate a Strategy
1. Select strategy from dropdown
2. Choose your market view
3. Add rationale (optional)
4. Click "Evaluate" for guidance
5. Click "Apply to sim" to visualize

### Restart Onboarding
- Click "🔄 Restart Tour" button in header

## Greeks Quick Reference

| Greek | Symbol | Meaning | Typical Range |
|-------|--------|---------|---------------|
| **Delta** | Δ | Price sensitivity | Call: 0 to 1<br>Put: -1 to 0 |
| **Gamma** | Γ | Rate of Delta change | Always positive |
| **Vega** | V | Volatility sensitivity | Always positive |
| **Theta** | Θ | Time decay | Always negative |

## Strategy Quick Guide

| Strategy | Best For | Risk Level |
|----------|----------|------------|
| **Covered Call** | Income generation | Low-Medium |
| **Protective Put** | Downside protection | Low |
| **Short Straddle** | Neutral, high IV | High |
| **Iron Condor** | Neutral, range-bound | Medium |
| **Long Straddle** | Volatility expansion | Medium-High |

## Default Values

- **Underlying Price (S)**: $90,000
- **Strike (K)**: $90,000
- **Days to Expiry**: 30
- **Volatility (σ)**: 0.6 (60%)
- **Side**: Call
- **Position**: Long

## Tips & Tricks

### Understanding Charts
- **Greeks vs S**: Shows how Greeks change as underlying price moves
- **Option Price vs S**: Shows intrinsic + time value
- **Strategy PnL**: Shows profit/loss across price range

### Quiz Strategy
- Answer 3 questions correctly per Greek to earn badges
- Streak tracking helps you see improvement
- Questions are randomized for variety

### Strategy Evaluation
- Market signals are parsed from BTC data
- Guidance considers current market conditions
- Always review risk notes before trading

### Badge System
- Badges persist in browser localStorage
- Progress is tracked per Greek category
- Earn badges by answering quiz questions correctly

## Troubleshooting

### Chart Not Updating
- Click "Apply" after changing inputs
- Check that inputs are valid numbers
- Try refreshing the page

### Quiz Not Working
- Make sure you've selected an answer
- Click "Submit" after selecting
- Try "Next Q" to get a new question

### Badges Not Saving
- Check browser localStorage is enabled
- Clear cache and try again
- Badges are saved automatically

### Market Data Not Loading
- App uses fallback data if API unavailable
- Check browser console for errors
- Internet connection required for live data

## Formula Reference

### Black-Scholes (Call)
```
C = S × N(d1) - K × e^(-rT) × N(d2)
```

### Black-Scholes (Put)
```
P = K × e^(-rT) × N(-d2) - S × N(-d1)
```

Where:
- `d1 = (ln(S/K) + (r + σ²/2) × T) / (σ × √T)`
- `d2 = d1 - σ × √T`
- `N(x)` = Cumulative normal distribution

## Common Scenarios

### Learning Delta
1. Set strike = underlying price (at-the-money)
2. Adjust underlying price slider
3. Watch Delta change in metrics
4. View "Greeks vs S" chart

### Understanding Time Decay
1. Set days to expiry to 365
2. Note Theta value
3. Reduce days to 30
4. See Theta increase (more negative)

### Exploring Volatility
1. Set volatility to 0.2 (low)
2. Note option price
3. Increase to 1.0 (high)
4. See price increase significantly

### Strategy Comparison
1. Select a strategy
2. Click "Evaluate"
3. Note guidance and risk notes
4. Try different market views
5. Compare strategies

---

**Remember**: This is an educational tool. Always do your own research before making trading decisions.

