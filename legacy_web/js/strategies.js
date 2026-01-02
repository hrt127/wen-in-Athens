// ---------- Strategy templates & simulation ----------
const STRATEGY_TEMPLATES = {
  covered_call: (inputs) => ({
    legs: [
      { type: 'stock', qty: +1, price: inputs.S },
      { type: 'call', qty: -1, K: inputs.K, T: toYears(inputs.days), sigma: inputs.sigma, r: inputs.r }
    ]
  }),
  protective_put: (inputs) => ({
    legs: [
      { type: 'stock', qty: +1, price: inputs.S },
      { type: 'put', qty: +1, K: inputs.K, T: toYears(inputs.days), sigma: inputs.sigma, r: inputs.r }
    ]
  }),
  short_straddle: (inputs) => ({
    legs: [
      { type: 'call', qty: -1, K: inputs.K, T: toYears(inputs.days), sigma: inputs.sigma, r: inputs.r },
      { type: 'put', qty: -1, K: inputs.K, T: toYears(inputs.days), sigma: inputs.sigma, r: inputs.r }
    ]
  }),
  iron_condor: (inputs) => ({
    legs: [
      { type: 'call', qty: -1, K: inputs.K + 500, T: toYears(inputs.days), sigma: inputs.sigma, r: inputs.r },
      { type: 'call', qty: +1, K: inputs.K + 1200, T: toYears(inputs.days), sigma: inputs.sigma, r: inputs.r },
      { type: 'put', qty: -1, K: inputs.K - 500, T: toYears(inputs.days), sigma: inputs.sigma, r: inputs.r },
      { type: 'put', qty: +1, K: inputs.K - 1200, T: toYears(inputs.days), sigma: inputs.sigma, r: inputs.r }
    ]
  }),
  long_straddle: (inputs) => ({
    legs: [
      { type: 'call', qty: +1, K: inputs.K, T: toYears(inputs.days), sigma: inputs.sigma, r: inputs.r },
      { type: 'put', qty: +1, K: inputs.K, T: toYears(inputs.days), sigma: inputs.sigma, r: inputs.r }
    ]
  })
};

function simulateStrategyPnL(template) {
  const { S, K, r, sigma, days } = state.inputs;
  const T = toYears(days);
  const span = 0.5; const steps = 61;
  const labels = []; const pnl = [];
  // baseline
  let baseVal = 0;
  for (const leg of template.legs) {
    if (leg.type === 'stock') baseVal += leg.qty * S;
    else {
      const price = calculateOptionPrice({ S, K: leg.K, r, sigma, T }, leg.type);
      baseVal += leg.qty * price;
    }
  }
  for (let i = 0; i < steps; i++) {
    const Si = S * (1 - span + (2 * span) * i / (steps - 1));
    labels.push(Math.round(Si));
    let val = 0;
    for (const leg of template.legs) {
      if (leg.type === 'stock') val += leg.qty * Si;
      else {
        const price = calculateOptionPrice({ S: Si, K: leg.K || K, r, sigma, T }, leg.type);
        val += leg.qty * price;
      }
    }
    pnl.push(val - baseVal);
  }
  return { labels, datasets: [{ label: 'Strategy PnL', data: pnl, borderColor: '#22c1c3', tension: 0.2 }] };
}

function evaluateStrategy() {
  const choice = els.strategyChoice.value;
  const view = els.userView.value;
  const thoughts = els.userRationale.value || '';
  const c = state.marketCombo || { deltaLike: 0, vegaLike: 0, gammaLike: 0, thetaLike: 0, pcr: 1.5 };

  const verdict = { correct: false, reason: '', alt: [], riskNotes: [], growthNotes: [] };

  // Simple rule-set evaluation
  if (Math.abs(c.deltaLike) < 0.2 && c.vegaLike > 0.5 && c.pcr > 2.5) {
    // neutral + rich IV + skew -> consider short premium
    if (choice === 'short_straddle' || choice === 'iron_condor') verdict.correct = true;
    verdict.reason = 'IV rich with skew; selling premium structures can monetize theta and vega.';
    verdict.alt = ['Iron butterfly', 'Short strangle (wings)'];
    verdict.riskNotes = ['Tail risk on large directional moves; use size management and wings.'];
    verdict.growthNotes = ['Income-oriented; compound small wins if risk managed.'];
  } else if (c.deltaLike < -0.25 && c.pcr > 2.5) {
    // bearish + put demand -> hedging or protective
    if (choice === 'protective_put') verdict.correct = true;
    verdict.reason = 'Risk-off / put-heavy: hedging with protective puts is sensible to protect downside.';
    verdict.alt = ['Put spread (cheaper)', 'Collar'];
    verdict.riskNotes = ['Premium cost; consider strike level and time to expiry.'];
    verdict.growthNotes = ['Protects drawdowns; can preserve long-term growth.'];
  } else if (Math.abs(c.deltaLike) < 0.2 && c.vegaLike < 0.4) {
    // low vega -> consider long volatility if expecting a move
    if (choice === 'long_straddle') verdict.correct = true;
    verdict.reason = 'Implied low: buying convexity can pay off if a large move or vol expansion occurs.';
    verdict.alt = ['Calendar spread around event'];
    verdict.riskNotes = ['Theta decay is an enemy; time the entry near catalysts.'];
    verdict.growthNotes = ['Asymmetric upside; increases portfolio convexity.'];
  } else {
    // fallback
    if (choice === 'covered_call') verdict.correct = true;
    verdict.reason = 'Mixed signals; covered call harvests income while keeping directional exposure.';
    verdict.alt = ['Bull call spread', 'Collar'];
    verdict.riskNotes = ['Caps upside; assignment risk if the underlying rallies strongly.'];
    verdict.growthNotes = ['Generates consistent income; good for conservative growth.'];
  }

  // Render guidance
  renderGuidance(verdict, { choice, view, thoughts });
  // Prepare template for simulation & exposure
  state.strategyTemplate = STRATEGY_TEMPLATES[choice](state.inputs);
  renderExposureTable(state.strategyTemplate);
}

function renderGuidance(verdict, user) {
  const box = els.guidanceBox;
  box.innerHTML = `
    <div class="${verdict.correct ? 'ok' : 'warn'}">${verdict.correct ? 'Strategy aligns with current signals.' : 'Strategy may be suboptimal vs signals.'}</div>
    <div style="margin-top:6px">${verdict.reason}</div>
    <div style="margin-top:6px"><strong>Alternatives:</strong> ${verdict.alt.join(', ')}</div>
    <div style="margin-top:6px"><strong>Risk:</strong> ${verdict.riskNotes.join(' | ')}</div>
    <div style="margin-top:6px"><strong>Growth:</strong> ${verdict.growthNotes.join(' | ')}</div>
    <div style="margin-top:6px;color:var(--muted)">Your view: ${user.view} ${user.thoughts ? ('• ' + user.thoughts) : ''}</div>
  `;
}

function applyStrategyToChart() {
  if (!state.strategyTemplate) {
    alert('No strategy selected/applied yet.');
    return;
  }
  const chart = state.chart.instance;
  const sim = simulateStrategyPnL(state.strategyTemplate);
  state.chart.view = 'pnl';
  chart.data.labels = sim.labels;
  chart.data.datasets = sim.datasets;
  chart.update();
  renderExposureTable(state.strategyTemplate);
}

// ---------- Exposure table rendering ----------
function calculateLegGreeks(leg, S, r, sigma, T) {
  if (leg.type === 'stock') return { delta: leg.qty, gamma: 0, vega: 0, theta: 0 };
  const g = calculateGreeks({ S, K: leg.K, r, sigma, T }, leg.type);
  // Use vega per 1% in display (g.vegaPer1Pct)
  return { delta: g.delta * leg.qty, gamma: g.gamma * leg.qty, vega: g.vegaPer1Pct * leg.qty, theta: g.thetaPerDay * leg.qty };
}

function renderExposureTable(template) {
  const { S, r, sigma, days } = state.inputs;
  const T = toYears(days);
  let net = { delta: 0, gamma: 0, vega: 0, theta: 0 };
  let rows = '';
  for (const leg of template.legs) {
    const g = calculateLegGreeks(leg, S, r, sigma, T);
    net.delta += g.delta; net.gamma += g.gamma; net.vega += g.vega; net.theta += g.theta;
    rows += `<tr><td>${leg.type}${leg.K ? (' K=' + leg.K) : ''}</td><td>${leg.qty}</td><td>${g.delta.toFixed(3)}</td><td>${g.gamma.toExponential(3)}</td><td>${g.vega.toFixed(3)}</td><td>${g.theta.toFixed(4)}</td></tr>`;
  }
  const table = `
    <table>
      <thead><tr><th>Leg</th><th>Qty</th><th>Δ</th><th>Γ</th><th>Vega (1%)</th><th>Θ/day</th></tr></thead>
      <tbody>${rows}</tbody>
      <tfoot><tr><td>Net</td><td></td><td>${net.delta.toFixed(3)}</td><td>${net.gamma.toExponential(3)}</td><td>${net.vega.toFixed(3)}</td><td>${net.theta.toFixed(4)}</td></tr></tfoot>
    </table>
  `;
  els.exposureTable.innerHTML = table;
}

function promptStrategy() {
  const c = state.marketCombo || { deltaLike: 0, vegaLike: 0, gammaLike: 0, thetaLike: 0, pcr: 1.5 };
  let bias = 'neutral';
  if (c.deltaLike < -0.25) bias = 'bearish';
  if (c.deltaLike > 0.25) bias = 'bullish';
  els.strategyPrompt.textContent = `Market view: ${bias}. IV-RV ${(c.iv - c.rv || 0).toFixed?.(2) ?? '–'}. PCR ${c.pcr?.toFixed?.(2) || '–'}. Choose a strategy and evaluate.`;
}

