// ---------- Chart (Chart.js) ----------
function initChart() {
  const ctx = els.mainChart.getContext('2d');
  state.chart.instance = new Chart(ctx, {
    type: 'line',
    data: { labels: [], datasets: [] },
    options: {
      responsive: true,
      animation: { duration: state.chart.anim ? 600 : 0 },
      plugins: { legend: { labels: { color: '#cfe8ff' } } },
      scales: {
        x: { ticks: { color: '#9fb0cc' }, grid: { color: 'rgba(255,255,255,0.03)' } },
        y: { ticks: { color: '#9fb0cc' }, grid: { color: 'rgba(255,255,255,0.03)' } }
      }
    }
  });
  updateChart();
}

function generateSeries(view) {
  const { S, K, r, sigma, days } = state.inputs;
  const T = toYears(days);
  const span = 0.5; const steps = 41;
  const labels = [], deltaSeries = [], gammaSeries = [], vegaSeries = [], thetaSeries = [], priceSeries = [], pnlSeries = [];
  const basePrice = calculateOptionPrice({ S, K, r, sigma, T }, 'call');

  for (let i = 0; i < steps; i++) {
    const Si = S * (1 - span + (2 * span) * i / (steps - 1));
    labels.push(Math.round(Si));
    const gCall = calculateGreeks({ S: Si, K, r, sigma, T }, 'call');
    const callP = calculateOptionPrice({ S: Si, K, r, sigma, T }, 'call');
    deltaSeries.push(gCall.delta);
    gammaSeries.push(gCall.gamma);
    vegaSeries.push(gCall.vegaPer1Pct);
    thetaSeries.push(gCall.thetaPerDay);
    priceSeries.push(callP);
    pnlSeries.push(callP - basePrice);
  }

  if (view === 'greeks') {
    return {
      labels,
      datasets: [
        { label: 'Delta', data: deltaSeries, borderColor: '#8be3ff', tension: 0.25 },
        { label: 'Gamma', data: gammaSeries, borderColor: '#ffd4a3', tension: 0.25 },
        { label: 'Vega (per 1%)', data: vegaSeries, borderColor: '#ffd1ff', tension: 0.25 },
        { label: 'Theta (per day)', data: thetaSeries, borderColor: '#b9ffb3', tension: 0.25 },
      ]
    };
  } else if (view === 'price') {
    return { labels, datasets: [{ label: 'Call price', data: priceSeries, borderColor: '#a78bfa', tension: 0.25 }] };
  } else {
    return { labels, datasets: [{ label: 'Relative PnL', data: pnlSeries, borderColor: '#6b7280', tension: 0.25 }] };
  }
}

function updateChart() {
  const chart = state.chart.instance;
  const payload = generateSeries(state.chart.view || 'greeks');
  chart.data.labels = payload.labels;
  chart.data.datasets = payload.datasets;
  chart.options.animation.duration = state.chart.anim ? 600 : 0;
  chart.update();
}

