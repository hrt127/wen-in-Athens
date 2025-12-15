// ---------- Utilities ----------
function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
function toYears(days) { return Math.max(1, Number(days)) / 365; }
function normPDF(x) { return Math.exp(-0.5 * x * x) / Math.sqrt(2 * Math.PI); }
function normCDF(x) {
  const sign = x < 0 ? -1 : 1; x = Math.abs(x) / Math.sqrt(2);
  const t = 1 / (1 + 0.3275911 * x);
  const a1 = 0.254829592, a2 = -0.284496736, a3 = 1.421413741, a4 = -1.453152027, a5 = 1.061405429;
  const erf = 1 - (((((a5 * t + a4) * t + a3) * t + a2) * t + a1) * t) * Math.exp(-x * x);
  return 0.5 * (1 + sign * erf);
}
function format(n, d = 4) { if (!isFinite(n)) return '-'; return Number(n).toFixed(d); }

// ---------- Black-Scholes price + Greeks (both call & put) ----------
function d1(S, K, r, sigma, T) {
  const eps = 1e-12;
  return (Math.log(S / K) + (r + 0.5 * sigma * sigma) * T) / (Math.max(sigma * Math.sqrt(T), eps));
}
function d2(d1Val, sigma, T) { return d1Val - sigma * Math.sqrt(T); }

// Calculate option price for call or put
function calculateOptionPrice(params, side) {
  const { S, K, r, sigma, T } = params;
  const d1v = d1(S, K, r, sigma, T);
  const d2v = d2(d1v, sigma, T);
  if (side === 'call') {
    return S * normCDF(d1v) - K * Math.exp(-r * T) * normCDF(d2v);
  } else {
    return K * Math.exp(-r * T) * normCDF(-d2v) - S * normCDF(-d1v);
  }
}

// Returns Greeks (delta, gamma, vega, theta-per-day) for call or put
function calculateGreeks(params, side) {
  const { S, K, r, sigma, T } = params;
  const eps = 1e-12;
  const d1v = d1(S, K, r, sigma, T);
  const d2v = d2(d1v, sigma, T);
  const pdf = normPDF(d1v);
  const gamma = pdf / (Math.max(S * sigma * Math.sqrt(T), eps));
  const vega = S * pdf * Math.sqrt(T); // per 1.0 vol (100%); we'll show per 1% or raw depending on UI
  let delta, thetaYear;
  if (side === 'call') {
    delta = normCDF(d1v);
    thetaYear = -(S * pdf * sigma) / (2 * Math.sqrt(T)) - r * K * Math.exp(-r * T) * normCDF(d2v);
  } else {
    delta = normCDF(d1v) - 1;
    thetaYear = -(S * pdf * sigma) / (2 * Math.sqrt(T)) + r * K * Math.exp(-r * T) * normCDF(-d2v);
  }
  return {
    delta,
    gamma,
    vega,            // per 1.0 vol (100%)
    vegaPer1Pct: vega / 100, // per 1%
    thetaPerDay: thetaYear / 365
  };
}

// Apply position long/short sign to price & Greeks
function applyPositionSign({ price, delta, gamma, vega, thetaPerDay }, position) {
  const sign = position === 'short' ? -1 : 1;
  return {
    price: price * sign,
    delta: delta * sign,
    gamma: gamma * sign,
    vega: vega * sign,
    thetaPerDay: thetaPerDay * sign
  };
}

