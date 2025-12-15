"""
Strategy templates, simulation, and evaluation logic.
Port of JavaScript implementation to Python.
"""
from blackscholes import calculate_option_price, calculate_greeks, to_years


def get_strategy_template(strategy_name, inputs):
    """
    Get strategy template based on strategy name.
    
    Parameters:
    -----------
    strategy_name : str
        Strategy name: 'call', 'put', 'covered_call', 'protective_put', 
                      'short_straddle', 'iron_condor', 'long_straddle', 'strangle'
    inputs : dict
        Dictionary with keys: S, K, days, sigma, r
    
    Returns:
    --------
    dict
        Strategy template with 'legs' list
    """
    S = inputs['S']
    K = inputs['K']
    days = inputs['days']
    sigma = inputs.get('sigma', 0.6)
    r = inputs.get('r', 0.0)
    T = to_years(days)
    
    templates = {
        'call': {
            'legs': [
                {'type': 'call', 'qty': 1, 'K': K, 'T': T, 'sigma': sigma, 'r': r}
            ]
        },
        'put': {
            'legs': [
                {'type': 'put', 'qty': 1, 'K': K, 'T': T, 'sigma': sigma, 'r': r}
            ]
        },
        'covered_call': {
            'legs': [
                {'type': 'stock', 'qty': 1, 'price': S},
                {'type': 'call', 'qty': -1, 'K': K, 'T': T, 'sigma': sigma, 'r': r}
            ]
        },
        'protective_put': {
            'legs': [
                {'type': 'stock', 'qty': 1, 'price': S},
                {'type': 'put', 'qty': 1, 'K': K, 'T': T, 'sigma': sigma, 'r': r}
            ]
        },
        'short_straddle': {
            'legs': [
                {'type': 'call', 'qty': -1, 'K': K, 'T': T, 'sigma': sigma, 'r': r},
                {'type': 'put', 'qty': -1, 'K': K, 'T': T, 'sigma': sigma, 'r': r}
            ]
        },
        'iron_condor': {
            'legs': [
                {'type': 'call', 'qty': -1, 'K': K + 500, 'T': T, 'sigma': sigma, 'r': r},
                {'type': 'call', 'qty': 1, 'K': K + 1200, 'T': T, 'sigma': sigma, 'r': r},
                {'type': 'put', 'qty': -1, 'K': K - 500, 'T': T, 'sigma': sigma, 'r': r},
                {'type': 'put', 'qty': 1, 'K': K - 1200, 'T': T, 'sigma': sigma, 'r': r}
            ]
        },
        'long_straddle': {
            'legs': [
                {'type': 'call', 'qty': 1, 'K': K, 'T': T, 'sigma': sigma, 'r': r},
                {'type': 'put', 'qty': 1, 'K': K, 'T': T, 'sigma': sigma, 'r': r}
            ]
        },
        'strangle': {
            'legs': [
                {'type': 'call', 'qty': 1, 'K': K + 500, 'T': T, 'sigma': sigma, 'r': r},
                {'type': 'put', 'qty': 1, 'K': K - 500, 'T': T, 'sigma': sigma, 'r': r}
            ]
        }
    }
    
    return templates.get(strategy_name, templates['call'])


def simulate_strategy_pnl(template, inputs):
    """
    Simulate strategy PnL across a range of underlying prices.
    
    Parameters:
    -----------
    template : dict
        Strategy template with 'legs' list
    inputs : dict
        Dictionary with keys: S, K, r, sigma, days
    
    Returns:
    --------
    tuple
        (labels, pnl_data) where labels are underlying prices and pnl_data is PnL values
    """
    import numpy as np
    
    S = inputs['S']
    K = inputs['K']
    r = inputs.get('r', 0.0)
    sigma = inputs.get('sigma', 0.6)
    days = inputs['days']
    T = to_years(days)
    
    span = 0.5
    steps = 61
    
    # Calculate baseline value
    base_val = 0
    for leg in template['legs']:
        if leg['type'] == 'stock':
            base_val += leg['qty'] * S
        else:
            price = calculate_option_price(S, leg['K'], r, sigma, T, leg['type'])
            base_val += leg['qty'] * price
    
    # Calculate PnL across price range
    labels = []
    pnl = []
    
    for i in range(steps):
        Si = S * (1 - span + (2 * span) * i / (steps - 1))
        labels.append(round(Si))
        
        val = 0
        for leg in template['legs']:
            if leg['type'] == 'stock':
                val += leg['qty'] * Si
            else:
                price = calculate_option_price(Si, leg['K'], r, sigma, T, leg['type'])
                val += leg['qty'] * price
        
        pnl.append(val - base_val)
    
    return labels, pnl


def evaluate_strategy(choice, market_combo, user_view='neutral', thoughts=''):
    """
    Evaluate strategy against market conditions.
    
    Parameters:
    -----------
    choice : str
        Strategy name
    market_combo : dict
        Market data with keys: deltaLike, vegaLike, gammaLike, thetaLike, pcr, iv, rv
    user_view : str
        User's market view: 'bullish', 'bearish', 'neutral', 'hedge'
    thoughts : str
        User's rationale (optional)
    
    Returns:
    --------
    dict
        Verdict with keys: correct, reason, alt, riskNotes, growthNotes
    """
    c = market_combo or {'deltaLike': 0, 'vegaLike': 0, 'gammaLike': 0, 'thetaLike': 0, 'pcr': 1.5}
    
    verdict = {
        'correct': False,
        'reason': '',
        'alt': [],
        'riskNotes': [],
        'growthNotes': []
    }
    
    # Simple rule-set evaluation
    if abs(c.get('deltaLike', 0)) < 0.2 and c.get('vegaLike', 0) > 0.5 and c.get('pcr', 1.5) > 2.5:
        # neutral + rich IV + skew -> consider short premium
        if choice in ['short_straddle', 'iron_condor']:
            verdict['correct'] = True
        verdict['reason'] = 'IV rich with skew; selling premium structures can monetize theta and vega.'
        verdict['alt'] = ['Iron butterfly', 'Short strangle (wings)']
        verdict['riskNotes'] = ['Tail risk on large directional moves; use size management and wings.']
        verdict['growthNotes'] = ['Income-oriented; compound small wins if risk managed.']
    elif c.get('deltaLike', 0) < -0.25 and c.get('pcr', 1.5) > 2.5:
        # bearish + put demand -> hedging or protective
        if choice == 'protective_put':
            verdict['correct'] = True
        verdict['reason'] = 'Risk-off / put-heavy: hedging with protective puts is sensible to protect downside.'
        verdict['alt'] = ['Put spread (cheaper)', 'Collar']
        verdict['riskNotes'] = ['Premium cost; consider strike level and time to expiry.']
        verdict['growthNotes'] = ['Protects drawdowns; can preserve long-term growth.']
    elif abs(c.get('deltaLike', 0)) < 0.2 and c.get('vegaLike', 0) < 0.4:
        # low vega -> consider long volatility if expecting a move
        if choice == 'long_straddle':
            verdict['correct'] = True
        verdict['reason'] = 'Implied low: buying convexity can pay off if a large move or vol expansion occurs.'
        verdict['alt'] = ['Calendar spread around event']
        verdict['riskNotes'] = ['Theta decay is an enemy; time the entry near catalysts.']
        verdict['growthNotes'] = ['Asymmetric upside; increases portfolio convexity.']
    else:
        # fallback
        if choice == 'covered_call':
            verdict['correct'] = True
        verdict['reason'] = 'Mixed signals; covered call harvests income while keeping directional exposure.'
        verdict['alt'] = ['Bull call spread', 'Collar']
        verdict['riskNotes'] = ['Caps upside; assignment risk if the underlying rallies strongly.']
        verdict['growthNotes'] = ['Generates consistent income; good for conservative growth.']
    
    return verdict


def calculate_leg_greeks(leg, S, r, sigma, T):
    """
    Calculate Greeks for a single leg.
    
    Parameters:
    -----------
    leg : dict
        Leg dictionary with type, qty, K, etc.
    S : float
        Underlying price
    r : float
        Risk-free rate
    sigma : float
        Volatility
    T : float
        Time to expiry in years
    
    Returns:
    --------
    dict
        Greeks: delta, gamma, vega, theta
    """
    if leg['type'] == 'stock':
        return {'delta': leg['qty'], 'gamma': 0, 'vega': 0, 'theta': 0}
    
    g = calculate_greeks(S, leg['K'], r, sigma, T, leg['type'])
    return {
        'delta': g['delta'] * leg['qty'],
        'gamma': g['gamma'] * leg['qty'],
        'vega': g['vegaPer1Pct'] * leg['qty'],
        'theta': g['thetaPerDay'] * leg['qty']
    }


def calculate_exposure_table(template, inputs):
    """
    Calculate exposure table for multi-leg strategy.
    
    Parameters:
    -----------
    template : dict
        Strategy template with 'legs' list
    inputs : dict
        Dictionary with keys: S, r, sigma, days
    
    Returns:
    --------
    dict
        Dictionary with 'legs' list (each with greeks) and 'net' greeks
    """
    S = inputs['S']
    r = inputs.get('r', 0.0)
    sigma = inputs.get('sigma', 0.6)
    days = inputs['days']
    T = to_years(days)
    
    net = {'delta': 0, 'gamma': 0, 'vega': 0, 'theta': 0}
    legs_data = []
    
    for leg in template['legs']:
        g = calculate_leg_greeks(leg, S, r, sigma, T)
        net['delta'] += g['delta']
        net['gamma'] += g['gamma']
        net['vega'] += g['vega']
        net['theta'] += g['theta']
        
        leg_label = leg['type']
        if 'K' in leg:
            leg_label += f" K={leg['K']}"
        
        legs_data.append({
            'leg': leg_label,
            'qty': leg['qty'],
            **g
        })
    
    return {
        'legs': legs_data,
        'net': net
    }

