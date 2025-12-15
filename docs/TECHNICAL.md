# Technical Documentation — Wen in Athens

This document provides detailed technical information for developers working with or extending the Wen in Athens application.

## Table of Contents

1. [Architecture Overview](#architecture-overview)
2. [Core Algorithms](#core-algorithms)
3. [Data Structures](#data-structures)
4. [API Reference](#api-reference)
5. [State Management](#state-management)
6. [Extension Points](#extension-points)

## Architecture Overview

### Single-File Application

The entire application is contained in a single HTML file (`index.html`) with three main sections:
- **HTML**: Structure and DOM elements
- **CSS**: Styling with CSS variables for theming
- **JavaScript**: All application logic (ES6+)

### Design Patterns

1. **Modular Functions**: Related functionality grouped into logical sections
2. **Centralized State**: Single `state` object for application state
3. **DOM Abstraction**: Centralized `els` object for element references
4. **Event-Driven**: Event listeners wired in `wire()` function

## Core Algorithms

### Black-Scholes Implementation

#### Option Pricing

```javascript
function calculateOptionPrice(params, side) {
  const {S, K, r, sigma, T} = params;
  const d1v = d1(S, K, r, sigma, T);
  const d2v = d2(d1v, sigma, T);
  
  if (side === 'call') {
    return S * normCDF(d1v) - K * Math.exp(-r * T) * normCDF(d2v);
  } else {
    return K * Math.exp(-r * T) * normCDF(-d2v) - S * normCDF(-d1v);
  }
}
```

**Parameters:**
- `S`: Current underlying price
- `K`: Strike price
- `r`: Risk-free rate (default: 0)
- `sigma`: Volatility (annualized)
- `T`: Time to expiry (in years)
- `side`: 'call' or 'put'

#### Greeks Calculations

**Delta (Δ)**
- Call: `normCDF(d1)`
- Put: `normCDF(d1) - 1`

**Gamma (Γ)**
- Both: `normPDF(d1) / (S * sigma * sqrt(T))`

**Vega**
- Both: `S * normPDF(d1) * sqrt(T)` (per 1.0 vol = 100%)
- Display: `vega / 100` (per 1%)

**Theta (Θ)**
- Call: `-(S * pdf * sigma) / (2 * sqrt(T)) - r * K * exp(-r*T) * normCDF(d2)`
- Put: `-(S * pdf * sigma) / (2 * sqrt(T)) + r * K * exp(-r*T) * normCDF(-d2)`
- Display: `thetaYear / 365` (per day)

### Normal Distribution Functions

**Cumulative Distribution Function (CDF)**
- Uses Abramowitz and Stegun approximation
- Error function implementation with high precision

**Probability Density Function (PDF)**
- Standard normal PDF: `exp(-0.5 * x²) / sqrt(2π)`

### Strategy Simulation

Multi-leg strategies are simulated by:
1. Calculating baseline portfolio value at current price
2. Iterating through price range (±50% by default)
3. Recalculating each leg's value at each price point
4. Computing PnL as difference from baseline

## Data Structures

### State Object

```javascript
state = {
  inputs: {
    S: 90000,        // Underlying price
    K: 90000,        // Strike price
    days: 30,        // Days to expiry
    sigma: 0.6,      // Volatility (decimal)
    r: 0.0,          // Risk-free rate
    side: 'call',    // 'call' or 'put'
    position: 'long' // 'long' or 'short'
  },
  outputs: {},       // Call option results
  putOutputs: {},    // Put option results
  chart: {
    instance: null,   // Chart.js instance
    view: 'greeks',  // Current view mode
    anim: true       // Animation enabled
  },
  quiz: {
    score: 0,        // Total correct answers
    streak: 0,       // Current streak
    current: null    // Current question object
  },
  badges: {
    earned: [],      // Array of badge tags
    progress: {}     // Progress tracking per badge
  },
  marketCombo: null, // Market signal data
  strategyTemplate: null // Current strategy configuration
}
```

### Strategy Template Structure

```javascript
{
  legs: [
    {
      type: 'call' | 'put' | 'stock',
      qty: number,      // Positive for long, negative for short
      K: number,        // Strike (for options)
      T: number,        // Time to expiry in years
      sigma: number,    // Volatility
      r: number         // Risk-free rate
    }
  ]
}
```

### Quiz Question Structure

```javascript
{
  q: string,           // Question text
  options: string[],   // Array of answer choices
  correct: number,     // Index of correct answer (0-based)
  tag: string         // Badge tag ('delta', 'gamma', 'vega', 'theta')
}
```

### Market Combo Structure

```javascript
{
  price: number,       // BTC price
  deltaLike: number,   // -1 to 1 (market direction signal)
  gammaLike: number,   // 0 to 1 (volatility signal)
  vegaLike: number,    // 0 to 1 (volatility premium signal)
  thetaLike: number,   // 0 to 1 (time decay signal)
  iv: number,          // Implied volatility
  rv: number,          // Realized volatility
  pcr: number,         // Put/call ratio
  sentiment: string    // Market sentiment
}
```

## API Reference

### Global Functions

#### `calculateOptionPrice(params, side)`
Calculates option price using Black-Scholes model.

**Parameters:**
- `params`: Object with `{S, K, r, sigma, T}`
- `side`: 'call' or 'put'

**Returns:** Number (option price)

#### `calculateGreeks(params, side)`
Calculates all Greeks for an option.

**Parameters:**
- `params`: Object with `{S, K, r, sigma, T}`
- `side`: 'call' or 'put'

**Returns:** Object with `{delta, gamma, vega, vegaPer1Pct, thetaPerDay}`

#### `applyPositionSign(greeks, position)`
Applies position sign (long/short) to Greeks.

**Parameters:**
- `greeks`: Object with `{price, delta, gamma, vega, thetaPerDay}`
- `position`: 'long' or 'short'

**Returns:** Signed Greeks object

### Chart Functions

#### `initChart()`
Initializes Chart.js instance with default configuration.

#### `updateChart()`
Updates chart with current data based on selected view mode.

#### `generateSeries(view)`
Generates data series for chart visualization.

**Parameters:**
- `view`: 'greeks', 'price', or 'pnl'

**Returns:** Chart.js data object with `{labels, datasets}`

### Strategy Functions

#### `evaluateStrategy()`
Evaluates selected strategy against current market conditions.

**Returns:** Verdict object with guidance

#### `simulateStrategyPnL(template)`
Simulates profit/loss for a strategy across price range.

**Parameters:**
- `template`: Strategy template object

**Returns:** Chart.js data object

#### `renderExposureTable(template)`
Renders multi-leg strategy exposure table.

**Parameters:**
- `template`: Strategy template object

### Quiz Functions

#### `nextQuizQuestion()`
Loads a random quiz question.

#### `submitQuizAnswer()`
Checks answer and updates score/badges.

### Badge Functions

#### `awardBadge(tag)`
Awards progress toward a badge.

**Parameters:**
- `tag`: Badge identifier ('delta', 'gamma', 'vega', 'theta')

#### `renderBadges()`
Updates badge display in UI.

### Market Data Functions

#### `fetchBTCData()`
Fetches BTC market data from API (with fallback).

**Returns:** Promise (resolves when data is loaded)

#### `parseMarketGreeks(json)`
Parses JSON market data into market combo structure.

**Parameters:**
- `json`: Market data JSON object

**Returns:** Market combo object

#### `parseTextReport(text)`
Parses text-based market report.

**Parameters:**
- `text`: Market report string

**Returns:** Parsed data object

### Onboarding Functions

#### `nextOnboardingStep(step)`
Advances onboarding to specified step.

**Parameters:**
- `step`: Step number (1-4)

#### `finishOnboarding(skipped)`
Completes onboarding and hides overlay.

**Parameters:**
- `skipped`: Boolean (true if skipped)

#### `restartOnboarding()`
Resets and restarts onboarding tour.

## State Management

### Input Synchronization

Input controls use dual binding:
- Range sliders ↔ Number inputs
- Changes in either update the other
- "Apply" button commits changes to state

### Persistence

- **Badges**: Stored in `localStorage` as `'greeks_badges_v2'`
- **Onboarding**: Completion status in `localStorage` as `'onboarding_completed'`

### State Updates

State updates trigger:
1. Recalculation of option prices and Greeks
2. Chart update (if instance exists)
3. UI refresh for all dependent elements

## Extension Points

### Adding New Strategies

Extend `STRATEGY_TEMPLATES` object:

```javascript
STRATEGY_TEMPLATES.new_strategy = (inputs) => ({
  legs: [
    {type: 'call', qty: 1, K: inputs.K, T: toYears(inputs.days), ...},
    // ... more legs
  ]
});
```

Add option to strategy dropdown in HTML.

### Adding Quiz Questions

Extend `QUIZ_TEMPLATES` array:

```javascript
QUIZ_TEMPLATES.push({
  q: 'Your question?',
  options: ['Option A', 'Option B', 'Option C'],
  correct: 1, // Index of correct answer
  tag: 'delta' // Badge category
});
```

### Custom Market Data Source

Modify `fetchBTCData()`:

```javascript
async function fetchBTCData() {
  const url = 'YOUR_API_ENDPOINT';
  try {
    const resp = await fetch(url);
    const data = await resp.json();
    const combo = parseMarketGreeks(data);
    renderMarketCombo(combo);
  } catch(err) {
    // Fallback handling
  }
}
```

### Adding New Greeks

Extend `calculateGreeks()`:

```javascript
function calculateGreeks(params, side) {
  // ... existing calculations ...
  const rho = /* calculate rho */;
  return {
    // ... existing Greeks ...
    rho: rho
  };
}
```

### Custom Chart Views

Add new view mode:

1. Add button in HTML chart toolbar
2. Add event listener in `wire()` function
3. Extend `generateSeries()` to handle new view
4. Update chart view state

## Performance Considerations

### Optimization Strategies

1. **Chart Animation**: Can be disabled for better performance
2. **Calculation Caching**: Consider caching for repeated calculations
3. **Debouncing**: Input changes could be debounced for smoother UX
4. **Lazy Loading**: Market data fetched asynchronously

### Browser Compatibility

- **ES6+ Features**: Arrow functions, const/let, template literals
- **Modern APIs**: fetch, localStorage, Canvas API
- **Chart.js**: Requires Canvas support

## Testing Considerations

### Unit Testing

Key functions to test:
- `calculateOptionPrice()` — verify against known values
- `calculateGreeks()` — verify derivatives
- `normCDF()` / `normPDF()` — verify statistical accuracy
- Strategy simulation — verify PnL calculations

### Integration Testing

- State management flow
- UI updates on state changes
- Chart rendering with different data
- Badge system persistence

## Security Considerations

### Client-Side Only

- No server-side code
- No sensitive data storage
- API calls are read-only (if implemented)

### LocalStorage

- Only stores user progress (badges, onboarding status)
- No sensitive financial data
- Can be cleared by user

## Future Enhancements

### Potential Additions

1. **Additional Greeks**: Rho (interest rate sensitivity)
2. **More Strategies**: Butterfly spreads, calendar spreads, etc.
3. **Historical Data**: Backtesting capabilities
4. **Export Functionality**: Export charts/data
5. **Mobile App**: React Native or PWA version
6. **Real-time Updates**: WebSocket integration for live data
7. **Advanced Analytics**: Risk metrics, probability distributions

---

**Last Updated**: [Current Date]
**Version**: 1.0.0

