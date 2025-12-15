"""
Black-Scholes option pricing and Greeks calculations.
Port of JavaScript implementation to Python.
"""
import numpy as np
from scipy.stats import norm


def clamp(v, a, b):
    """Clamp value between a and b."""
    return max(a, min(b, v))


def to_years(days):
    """Convert days to years."""
    return max(1, float(days)) / 365.0


def norm_pdf(x):
    """Standard normal probability density function."""
    return np.exp(-0.5 * x * x) / np.sqrt(2 * np.pi)


def norm_cdf(x):
    """
    Standard normal cumulative distribution function.
    Uses Abramowitz and Stegun approximation for consistency with JS version.
    """
    x = np.asarray(x)
    sign = np.where(x < 0, -1, 1)
    x_abs = np.abs(x) / np.sqrt(2)
    t = 1.0 / (1.0 + 0.3275911 * x_abs)
    a1 = 0.254829592
    a2 = -0.284496736
    a3 = 1.421413741
    a4 = -1.453152027
    a5 = 1.061405429
    erf = 1 - (((((a5 * t + a4) * t + a3) * t + a2) * t + a1) * t) * np.exp(-x_abs * x_abs)
    return 0.5 * (1 + sign * erf)


def format_number(n, d=4):
    """Format number with d decimal places."""
    if not np.isfinite(n):
        return '-'
    return f"{float(n):.{d}f}"


def d1(S, K, r, sigma, T):
    """Calculate d1 parameter for Black-Scholes."""
    eps = 1e-12
    return (np.log(S / K) + (r + 0.5 * sigma * sigma) * T) / np.maximum(sigma * np.sqrt(T), eps)


def d2(d1_val, sigma, T):
    """Calculate d2 parameter for Black-Scholes."""
    return d1_val - sigma * np.sqrt(T)


def calculate_option_price(S, K, r, sigma, T, side='call'):
    """
    Calculate option price using Black-Scholes model.
    
    Parameters:
    -----------
    S : float or array
        Current underlying price
    K : float
        Strike price
    r : float
        Risk-free rate
    sigma : float
        Volatility (annualized)
    T : float
        Time to expiry (in years)
    side : str
        'call' or 'put'
    
    Returns:
    --------
    float or array
        Option price
    """
    d1v = d1(S, K, r, sigma, T)
    d2v = d2(d1v, sigma, T)
    
    if side == 'call':
        return S * norm_cdf(d1v) - K * np.exp(-r * T) * norm_cdf(d2v)
    else:
        return K * np.exp(-r * T) * norm_cdf(-d2v) - S * norm_cdf(-d1v)


def calculate_greeks(S, K, r, sigma, T, side='call'):
    """
    Calculate Greeks (delta, gamma, vega, theta) for an option.
    
    Parameters:
    -----------
    S : float or array
        Current underlying price
    K : float
        Strike price
    r : float
        Risk-free rate
    sigma : float
        Volatility (annualized)
    T : float
        Time to expiry (in years)
    side : str
        'call' or 'put'
    
    Returns:
    --------
    dict
        Dictionary with keys: delta, gamma, vega, vegaPer1Pct, thetaPerDay
    """
    eps = 1e-12
    d1v = d1(S, K, r, sigma, T)
    d2v = d2(d1v, sigma, T)
    pdf = norm_pdf(d1v)
    gamma = pdf / np.maximum(S * sigma * np.sqrt(T), eps)
    vega = S * pdf * np.sqrt(T)  # per 1.0 vol (100%)
    
    if side == 'call':
        delta = norm_cdf(d1v)
        theta_year = -(S * pdf * sigma) / (2 * np.sqrt(T)) - r * K * np.exp(-r * T) * norm_cdf(d2v)
    else:
        delta = norm_cdf(d1v) - 1
        theta_year = -(S * pdf * sigma) / (2 * np.sqrt(T)) + r * K * np.exp(-r * T) * norm_cdf(-d2v)
    
    return {
        'delta': delta,
        'gamma': gamma,
        'vega': vega,  # per 1.0 vol (100%)
        'vegaPer1Pct': vega / 100.0,  # per 1%
        'thetaPerDay': theta_year / 365.0
    }


def apply_position_sign(greeks_dict, position='long'):
    """
    Apply position sign (long/short) to price and Greeks.
    
    Parameters:
    -----------
    greeks_dict : dict
        Dictionary with keys: price, delta, gamma, vega, thetaPerDay
    position : str
        'long' or 'short'
    
    Returns:
    --------
    dict
        Signed Greeks dictionary
    """
    sign = -1 if position == 'short' else 1
    return {
        'price': greeks_dict['price'] * sign,
        'delta': greeks_dict['delta'] * sign,
        'gamma': greeks_dict['gamma'] * sign,
        'vega': greeks_dict['vega'] * sign,
        'thetaPerDay': greeks_dict['thetaPerDay'] * sign
    }

