"""
Plotly chart creation functions for Greeks visualization.
"""
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from blackscholes import calculate_option_price, calculate_greeks, to_years


def create_greeks_chart(S, K, r, sigma, days, side='call'):
    """
    Create Plotly chart showing Greeks vs underlying price.
    
    Parameters:
    -----------
    S : float
        Current underlying price
    K : float
        Strike price
    r : float
        Risk-free rate
    sigma : float
        Volatility
    days : int
        Days to expiry
    side : str
        'call' or 'put'
    
    Returns:
    --------
    plotly.graph_objects.Figure
        Plotly figure
    """
    T = to_years(days)
    span = 0.5
    steps = 41
    
    # Generate price range
    price_range = S * (1 - span + np.linspace(0, 2 * span, steps))
    price_range = np.round(price_range).astype(int)
    
    # Calculate Greeks for each price
    deltas = []
    gammas = []
    vegas = []
    thetas = []
    
    for Si in price_range:
        greeks = calculate_greeks(Si, K, r, sigma, T, side)
        deltas.append(greeks['delta'])
        gammas.append(greeks['gamma'])
        vegas.append(greeks['vegaPer1Pct'])
        thetas.append(greeks['thetaPerDay'])
    
    # Create figure
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=price_range,
        y=deltas,
        mode='lines',
        name='Delta (Δ)',
        line=dict(color='#8be3ff', width=2),
        hovertemplate='Price: $%{x}<br>Delta: %{y:.4f}<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=price_range,
        y=gammas,
        mode='lines',
        name='Gamma (Γ)',
        line=dict(color='#ffd4a3', width=2),
        hovertemplate='Price: $%{x}<br>Gamma: %{y:.6f}<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=price_range,
        y=vegas,
        mode='lines',
        name='Vega (per 1%)',
        line=dict(color='#ffd1ff', width=2),
        hovertemplate='Price: $%{x}<br>Vega: %{y:.4f}<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=price_range,
        y=thetas,
        mode='lines',
        name='Theta (per day)',
        line=dict(color='#b9ffb3', width=2),
        hovertemplate='Price: $%{x}<br>Theta: %{y:.6f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Greeks vs Underlying Price',
        xaxis_title='Underlying Price ($)',
        yaxis_title='Greek Value',
        hovermode='x unified',
        template='plotly_dark',
        height=400,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    return fig


def create_price_chart(S, K, r, sigma, days, side='call'):
    """
    Create Plotly chart showing option price vs underlying price.
    
    Parameters:
    -----------
    S : float
        Current underlying price
    K : float
        Strike price
    r : float
        Risk-free rate
    sigma : float
        Volatility
    days : int
        Days to expiry
    side : str
        'call' or 'put'
    
    Returns:
    --------
    plotly.graph_objects.Figure
        Plotly figure
    """
    T = to_years(days)
    span = 0.5
    steps = 41
    
    # Generate price range
    price_range = S * (1 - span + np.linspace(0, 2 * span, steps))
    price_range = np.round(price_range).astype(int)
    
    # Calculate option prices
    prices = []
    for Si in price_range:
        price = calculate_option_price(Si, K, r, sigma, T, side)
        prices.append(price)
    
    # Create figure
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=price_range,
        y=prices,
        mode='lines',
        name=f'{side.capitalize()} Price',
        line=dict(color='#a78bfa', width=2),
        fill='tozeroy',
        hovertemplate='Price: $%{x}<br>Option Value: $%{y:.2f}<extra></extra>'
    ))
    
    # Add strike line
    fig.add_vline(
        x=K,
        line_dash="dash",
        line_color="gray",
        annotation_text=f"Strike: ${K:,}",
        annotation_position="top"
    )
    
    fig.update_layout(
        title=f'{side.capitalize()} Option Price vs Underlying Price',
        xaxis_title='Underlying Price ($)',
        yaxis_title='Option Price ($)',
        template='plotly_dark',
        height=400
    )
    
    return fig


def create_pnl_chart(template, inputs):
    """
    Create Plotly chart showing strategy PnL vs underlying price.
    
    Parameters:
    -----------
    template : dict
        Strategy template with 'legs' list
    inputs : dict
        Dictionary with keys: S, K, r, sigma, days
    
    Returns:
    --------
    plotly.graph_objects.Figure
        Plotly figure
    """
    from strategies import simulate_strategy_pnl
    
    labels, pnl = simulate_strategy_pnl(template, inputs)
    
    # Create figure
    fig = go.Figure()
    
    # Add zero line
    fig.add_hline(
        y=0,
        line_dash="dash",
        line_color="gray",
        opacity=0.5
    )
    
    fig.add_trace(go.Scatter(
        x=labels,
        y=pnl,
        mode='lines',
        name='Strategy PnL',
        line=dict(color='#22c1c3', width=2),
        fill='tozeroy',
        hovertemplate='Price: $%{x}<br>PnL: $%{y:,.2f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Strategy PnL vs Underlying Price',
        xaxis_title='Underlying Price ($)',
        yaxis_title='Profit/Loss ($)',
        template='plotly_dark',
        height=400
    )
    
    return fig

