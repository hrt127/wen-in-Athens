# Contributing to Wen in Athens

Thank you for your interest in contributing to Wen in Athens! This document provides guidelines and information for contributors.

## Getting Started

1. **Fork the repository** (if applicable)
2. **Clone your fork** or the main repository
3. **Create a branch** for your feature or fix
4. **Make your changes**
5. **Test thoroughly**
6. **Submit a pull request** or patch

## Development Setup

### Prerequisites
- Modern web browser
- Text editor or IDE
- Basic knowledge of JavaScript, HTML, and CSS
- Understanding of options trading concepts (helpful but not required)

### Local Development

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd wen-in-Athens
   ```

2. Open `index.html` in your browser or use a local server:
   ```bash
   python3 -m http.server 8080
   ```

3. Make changes and test in browser

## Code Style Guidelines

### JavaScript

- Use ES6+ features (arrow functions, const/let, template literals)
- Follow existing code structure and naming conventions
- Keep functions focused and modular
- Add comments for complex logic
- Use meaningful variable names

**Example:**
```javascript
// Good
function calculateOptionPrice(params, side) {
  const {S, K, r, sigma, T} = params;
  // ... implementation
}

// Avoid
function calc(p, s) {
  // ... unclear parameters
}
```

### HTML

- Maintain semantic HTML structure
- Use descriptive IDs and classes
- Keep accessibility in mind
- Comment complex sections

### CSS

- Use CSS variables for theming (see `:root` in styles)
- Follow existing naming conventions
- Keep styles organized by section
- Use responsive design principles

## Areas for Contribution

### High Priority

1. **Additional Strategies**
   - Add new strategy templates
   - Implement strategy evaluation logic
   - Add to strategy dropdown

2. **Quiz Questions**
   - Add more quiz questions
   - Cover additional concepts
   - Improve question variety

3. **Market Data Integration**
   - Improve BTC data fetching
   - Add more data sources
   - Enhance market signal parsing

4. **Mobile Responsiveness**
   - Improve mobile layout
   - Touch-friendly controls
   - Responsive chart sizing

### Medium Priority

1. **Accessibility**
   - ARIA labels
   - Keyboard navigation
   - Screen reader support

2. **Performance**
   - Optimize calculations
   - Debounce input handlers
   - Lazy load components

3. **Documentation**
   - Code comments
   - User guides
   - Video tutorials

4. **Testing**
   - Unit tests for calculations
   - Integration tests
   - E2E tests

### Nice to Have

1. **Additional Features**
   - Export charts as images
   - Save/load configurations
   - Historical data backtesting
   - More Greeks (Rho, etc.)

2. **UI/UX Improvements**
   - Dark/light theme toggle
   - Customizable color schemes
   - Animation improvements
   - Better error messages

## Adding a New Strategy

1. **Define the strategy template** in `STRATEGY_TEMPLATES`:
   ```javascript
   STRATEGY_TEMPLATES.your_strategy = (inputs) => ({
     legs: [
       {type: 'call', qty: 1, K: inputs.K, T: toYears(inputs.days), ...},
       // ... more legs
     ]
   });
   ```

2. **Add to HTML dropdown**:
   ```html
   <option value="your_strategy">Your Strategy Name</option>
   ```

3. **Update evaluation logic** in `evaluateStrategy()` if needed

4. **Test thoroughly** with different market conditions

## Adding Quiz Questions

1. **Add to `QUIZ_TEMPLATES` array**:
   ```javascript
   {
     q: 'Your question text?',
     options: ['Option A', 'Option B', 'Option C'],
     correct: 1, // Index of correct answer (0-based)
     tag: 'delta' // Badge category: 'delta', 'gamma', 'vega', or 'theta'
   }
   ```

2. **Ensure questions are:**
   - Clear and unambiguous
   - Educational and relevant
   - Not too easy or too hard
   - Cover important concepts

## Testing Your Changes

### Manual Testing Checklist

- [ ] All input controls work correctly
- [ ] Calculations update in real-time
- [ ] Charts render properly
- [ ] Quiz mode functions correctly
- [ ] Badge system works
- [ ] Strategy evaluation provides meaningful guidance
- [ ] Onboarding tour works
- [ ] Mobile/responsive layout works
- [ ] No console errors
- [ ] localStorage persistence works

### Testing Calculations

Verify against known values:
- Use online Black-Scholes calculators
- Compare with financial textbooks
- Test edge cases (very high/low volatility, near expiry, etc.)

## Submitting Changes

### Before Submitting

1. **Test thoroughly** in multiple browsers
2. **Check for console errors**
3. **Verify responsive design**
4. **Update documentation** if needed
5. **Follow code style guidelines**

### Pull Request Process

1. **Create a clear title** describing your changes
2. **Provide a detailed description**:
   - What changed and why
   - How to test
   - Screenshots if UI changes
3. **Reference any related issues**
4. **Keep changes focused** (one feature/fix per PR)

### Commit Messages

Use clear, descriptive commit messages:

```
Good:
- "Add iron butterfly strategy template"
- "Fix Delta calculation for deep ITM options"
- "Improve mobile responsiveness for chart controls"

Avoid:
- "fix stuff"
- "updates"
- "changes"
```

## Code Review Process

1. **All submissions will be reviewed**
2. **Feedback will be provided** for improvements
3. **Be open to suggestions** and iterate
4. **Respond to review comments** promptly

## Questions?

- Open an issue for questions or discussions
- Check existing documentation first
- Be respectful and constructive in communications

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

---

**Thank you for contributing to Wen in Athens!** 🎉

