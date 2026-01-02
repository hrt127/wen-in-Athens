// ---------- DOM elements ----------
const els = {
  inpS: document.getElementById('inpS'), inpSNum: document.getElementById('inpSNum'),
  inpK: document.getElementById('inpK'), inpKNum: document.getElementById('inpKNum'),
  inpDays: document.getElementById('inpDays'), inpDaysNum: document.getElementById('inpDaysNum'),
  inpSigma: document.getElementById('inpSigma'), inpSigmaNum: document.getElementById('inpSigmaNum'),
  inpSide: document.getElementById('inpSide'), inpPosition: document.getElementById('inpPosition'),
  btnApplyInputs: document.getElementById('btnApplyInputs'), btnReset: document.getElementById('btnReset'),
  priceCall: document.getElementById('priceCall'), deltaCall: document.getElementById('deltaCall'), gammaCall: document.getElementById('gammaCall'),
  vegaCall: document.getElementById('vegaCall'), thetaCall: document.getElementById('thetaCall'),
  pricePut: document.getElementById('pricePut'), deltaPut: document.getElementById('deltaPut'), gammaPut: document.getElementById('gammaPut'),
  vegaPut: document.getElementById('vegaPut'), thetaPut: document.getElementById('thetaPut'),
  mainChart: document.getElementById('mainChart'),
  viewGreeks: document.getElementById('viewGreeks'), viewPrice: document.getElementById('viewPrice'), viewPnL: document.getElementById('viewPnL'),
  btnAnimate: document.getElementById('btnAnimate'),
  btcSummary: document.getElementById('btcSummary'), mDelta: document.getElementById('mDelta'), mGamma: document.getElementById('mGamma'),
  mVega: document.getElementById('mVega'), marketCombo: document.getElementById('marketCombo'),
  strategyPrompt: document.getElementById('strategyPrompt'), strategyChoice: document.getElementById('strategyChoice'),
  userView: document.getElementById('userView'), userRationale: document.getElementById('userRationale'),
  btnEvaluate: document.getElementById('btnEvaluate'), guidanceBox: document.getElementById('guidanceBox'),
  btnApplyToSim: document.getElementById('btnApplyToSim'), exposureTable: document.getElementById('exposureTable'),
  badgeList: document.getElementById('badgeList'),
  quizQuestion: document.getElementById('quizQuestion'), quizChoices: document.getElementById('quizChoices'),
  btnNextQ: document.getElementById('btnNextQ'), btnSubmitAnswer: document.getElementById('btnSubmitAnswer'),
  quizFeedback: document.getElementById('quizFeedback'), quizScore: document.getElementById('quizScore'), quizStreak: document.getElementById('quizStreak')
};

// ---------- App state ----------
const state = {
  inputs: { S: 90000, K: 90000, days: 30, sigma: 0.6, r: 0.0, side: 'call', position: 'long' },
  outputs: {}, putOutputs: {},
  chart: { instance: null, view: 'greeks', anim: true },
  quiz: { score: 0, streak: 0, current: null },
  badges: loadBadges(),
  marketCombo: null,
  strategyTemplate: null
};

// ---------- Persisted badges ----------
function loadBadges() {
  try { return JSON.parse(localStorage.getItem('greeks_badges_v2')) || { earned: [], progress: {} }; } catch (e) { return { earned: [], progress: {} }; }
}
function saveBadges() {
  localStorage.setItem('greeks_badges_v2', JSON.stringify(state.badges));
  renderBadges();
}
function awardBadge(tag) {
  if (!state.badges.progress[tag]) state.badges.progress[tag] = 0;
  state.badges.progress[tag] += 1;
  const goal = 3;
  if (state.badges.progress[tag] >= goal && !state.badges.earned.includes(tag)) {
    state.badges.earned.push(tag);
    state.quizFeedback && (els.quizFeedback.innerHTML = `<span class="ok">Badge earned: ${badgeTitle(tag)} 🏅</span>`);
  }
  saveBadges();
}
function badgeTitle(tag) {
  return { delta: 'Delta Master', gamma: 'Gamma Guru', vega: 'Vega Explorer', theta: 'Theta Ticker' }[tag] || tag;
}
function renderBadges() {
  els.badgeList.innerHTML = '';
  if (!state.badges.earned.length) {
    els.badgeList.innerHTML = '<div class="badge">No badges yet</div>';
    return;
  }
  state.badges.earned.forEach(b => {
    const d = document.createElement('div'); d.className = 'badge'; d.textContent = `${badgeTitle(b)} 🏅`; els.badgeList.appendChild(d);
  });
}

// ---------- UI wiring & helpers ----------
function syncRangeNumber(rangeEl, numEl) {
  rangeEl.addEventListener('input', () => { numEl.value = rangeEl.value; });
  numEl.addEventListener('change', () => { rangeEl.value = numEl.value; });
}
function setInputsToDOM() {
  els.inpS.value = state.inputs.S; els.inpSNum.value = state.inputs.S;
  els.inpK.value = state.inputs.K; els.inpKNum.value = state.inputs.K;
  els.inpDays.value = state.inputs.days; els.inpDaysNum.value = state.inputs.days;
  els.inpSigma.value = state.inputs.sigma; els.inpSigmaNum.value = state.inputs.sigma;
  els.inpSide.value = state.inputs.side; els.inpPosition.value = state.inputs.position;
}

// ---------- Update calculations & UI ----------
function updateAllFromInputs() {
  // read DOM inputs into state.inputs
  state.inputs.S = Number(els.inpS.value);
  state.inputs.K = Number(els.inpK.value);
  state.inputs.days = Number(els.inpDays.value);
  state.inputs.sigma = Number(els.inpSigma.value);
  state.inputs.side = els.inpSide.value;
  state.inputs.position = els.inpPosition.value;
  state.inputs.r = Number(els.inpR?.value || 0);

  const params = { S: state.inputs.S, K: state.inputs.K, r: state.inputs.r, sigma: state.inputs.sigma, T: toYears(state.inputs.days) };

  // Call and put values
  const callPrice = calculateOptionPrice(params, 'call');
  const putPrice = calculateOptionPrice(params, 'put');
  const callG = calculateGreeks(params, 'call');
  const putG = calculateGreeks(params, 'put');

  // Apply position sign to show net exposures if user selected short
  const callSigned = applyPositionSign({ price: callPrice, delta: callG.delta, gamma: callG.gamma, vega: callG.vegaPer1Pct, thetaPerDay: callG.thetaPerDay }, 'long');
  const putSigned = applyPositionSign({ price: putPrice, delta: putG.delta, gamma: putG.gamma, vega: putG.vegaPer1Pct, thetaPerDay: putG.thetaPerDay }, 'long');

  // UI: show raw (long) values; position sign is used when building multi-leg strategies
  els.priceCall.textContent = format(callPrice, 2);
  els.deltaCall.textContent = format(callG.delta, 4);
  els.gammaCall.textContent = format(callG.gamma, 6);
  els.vegaCall.textContent = format(callG.vegaPer1Pct, 4);
  els.thetaCall.textContent = format(callG.thetaPerDay, 6);

  els.pricePut.textContent = format(putPrice, 2);
  els.deltaPut.textContent = format(putG.delta, 4);
  els.gammaPut.textContent = format(putG.gamma, 6);
  els.vegaPut.textContent = format(putG.vegaPer1Pct, 4);
  els.thetaPut.textContent = format(putG.thetaPerDay, 6);

  // update chart
  if (state.chart.instance) updateChart();
}

// ---------- Quiz: templates, generate, check ----------
const QUIZ_TEMPLATES = [
  { q: 'What happens to Vega when implied volatility increases (all else equal)?', options: ['Decreases', 'Increases', 'Stays same'], correct: 1, tag: 'vega' },
  { q: 'For a long call, when underlying price rises, Delta...', options: ['Decreases', 'Increases', 'Stays same'], correct: 1, tag: 'delta' },
  { q: 'As time to expiry approaches, Theta typically becomes...', options: ['More positive', 'More negative', 'Unchanged'], correct: 1, tag: 'theta' },
  { q: 'Gamma for near-the-money options near expiry tends to...', options: ['Decrease', 'Increase', 'Stay same'], correct: 1, tag: 'gamma' }
];

function nextQuizQuestion() {
  const idx = Math.floor(Math.random() * QUIZ_TEMPLATES.length);
  state.quiz.current = JSON.parse(JSON.stringify(QUIZ_TEMPLATES[idx]));
  renderQuiz();
}

function renderQuiz() {
  const cur = state.quiz.current;
  els.quizQuestion.textContent = cur.q;
  els.quizChoices.innerHTML = '';
  cur.options.forEach((opt, i) => {
    const btn = document.createElement('button');
    btn.className = 'btn';
    btn.textContent = `${String.fromCharCode(65 + i)}: ${opt}`;
    btn.onclick = () => { selectQuizChoice(i); };
    els.quizChoices.appendChild(btn);
  });
  els.btnSubmitAnswer.disabled = true;
  els.quizFeedback.textContent = '';
}

let selectedQuizChoice = null;
function selectQuizChoice(i) {
  selectedQuizChoice = i;
  [...els.quizChoices.children].forEach((b, idx) => b.style.outline = idx === i ? '2px solid #86f0e7' : '');
  els.btnSubmitAnswer.disabled = false;
}

function submitQuizAnswer() {
  if (selectedQuizChoice === null) return;
  const cur = state.quiz.current;
  const correct = selectedQuizChoice === cur.correct;
  if (correct) {
    state.quiz.score++; state.quiz.streak++; awardBadge(cur.tag);
    els.quizFeedback.innerHTML = `<span class="ok">Correct.</span> Good job — ${badgeTitle(cur.tag)} progress tracked.`;
  } else {
    state.quiz.streak = 0;
    els.quizFeedback.innerHTML = `<span class="warn">Incorrect.</span> Correct: ${cur.options[cur.correct]}`;
  }
  els.quizScore.textContent = state.quiz.score;
  els.quizStreak.textContent = state.quiz.streak;
  // disable submit until next
  els.btnSubmitAnswer.disabled = true;
  selectedQuizChoice = null;
}

// ---------- BTC Market play area: fetch + parse + mapping ----------
// fetchBTCData -> parseMarketGreeks -> renderMarketCombo
async function fetchBTCData() {
  // NOTE: placeholder endpoint. Replace with your real API endpoint if available.
  const url = 'https://app.elfa.ai/api/btc/summary'; // placeholder
  try {
    const resp = await fetch(url, { cache: 'no-store' });
    if (!resp.ok) throw new Error('no data');
    const data = await resp.json();
    const combo = parseMarketGreeks(data);
    renderMarketCombo(combo);
    state.marketCombo = combo;
  } catch (err) {
    // fallback: create synthetic data & parse a sample text report
    const sampleReport = "Markets: BTC $89,565; VIX 18.2; put/call ratio 3.2; implied > realized; risk-off tone.";
    const parsed = parseTextReport(sampleReport);
    const combo = mapParsedToCombo(parsed);
    renderMarketCombo(combo);
    state.marketCombo = combo;
  }
}

// Parse JSON response (if available). This maps fields to friendly combo.
function parseMarketGreeks(json) {
  // expecting keys like price, vol.implied, vol.realized, momentum, pcr, sentiment...
  const price = json.price || json.last || 90000;
  const iv = json.vol?.implied ?? 0.6;
  const rv = json.vol?.realized ?? 0.45;
  const pcr = json.putCallRatio ?? json.pcr ?? 1.8;
  const sentiment = json.sentiment ?? (pcr > 2.5 ? 'risk-off' : 'neutral');
  const deltaLike = clamp((json.trend?.slope ?? 0) * 0.7, -1, 1);
  const gammaLike = clamp(iv > 0.5 ? 0.7 : 0.3, 0, 1);
  const vegaLike = clamp(iv - rv + 0.4, 0, 1);
  const thetaLike = clamp(iv - rv > 0.05 ? 0.3 : 0.15, 0, 1);
  return { price, deltaLike, gammaLike, vegaLike, thetaLike, iv, rv, pcr, sentiment };
}

// Quick text report parser (very simple heuristics)
function parseTextReport(text) {
  const num = (s) => { const m = s && s.match(/\$?([0-9,]{3,})/); return m ? Number(m[1].replace(/,/g, '')) : null }
  const btc = num(text) || 90000;
  const vMatch = text.match(/VIX\s*([\d.]+)/i);
  const vix = vMatch ? Number(vMatch[1]) : 18;
  const pcrMatch = text.match(/put\/call ratio\s*([0-9.]+)/i);
  const pcr = pcrMatch ? Number(pcrMatch[1]) : 2.0;
  const impliedRich = /implied.*higher|heavy put|skew/i.test(text);
  return { btc, vix, pcr, impliedRich };
}

// Map parsed report to combo greeks-like values
function mapParsedToCombo(parsed) {
  const deltaLike = parsed.impliedRich ? -0.25 : 0.05;
  const gammaLike = parsed.vix > 16 ? 0.6 : 0.3;
  const vegaLike = parsed.pcr > 2.5 ? 0.7 : 0.35;
  const thetaLike = parsed.impliedRich ? 0.25 : 0.12;
  return { price: parsed.btc || 90000, deltaLike, gammaLike, vegaLike, thetaLike, pcr: parsed.pcr || 2.0 };
}

function renderMarketCombo(combo) {
  if (!combo) return;
  els.btcSummary.textContent = `BTC ~$${Math.round(combo.price)} • Sentiment: ${combo.sentiment || 'mixed'} • PCR: ${combo.pcr?.toFixed(2) || '–'}`;
  const pct = v => `${clamp(Math.round(v * 100), 0, 100)}%`;
  els.mDelta.style.width = pct((combo.deltaLike + 1) / 2);
  els.mGamma.style.width = pct(combo.gammaLike);
  els.mVega.style.width = pct(combo.vegaLike);
  els.marketCombo.textContent = `Δ:${combo.deltaLike.toFixed(2)} • Γ:${combo.gammaLike.toFixed(2)} • Vega:${combo.vegaLike.toFixed(2)} • Θ:${combo.thetaLike.toFixed(2)}`;
  // prompt strategy text
  promptStrategy();
}

// ---------- Event wiring ----------
function wire() {
  // sync ranges + numbers
  syncRangeNumber(els.inpS, els.inpSNum);
  syncRangeNumber(els.inpK, els.inpKNum);
  syncRangeNumber(els.inpDays, els.inpDaysNum);
  syncRangeNumber(els.inpSigma, els.inpSigmaNum);

  // apply / reset
  els.btnApplyInputs.addEventListener('click', () => { updateAllFromInputs(); });
  els.btnReset.addEventListener('click', () => {
    state.inputs = { S: 90000, K: 90000, days: 30, sigma: 0.6, r: 0, side: 'call', position: 'long' };
    setInputsToDOM(); updateAllFromInputs();
  });

  // chart view toggles
  els.viewGreeks.addEventListener('click', () => { state.chart.view = 'greeks'; updateChart(); });
  els.viewPrice.addEventListener('click', () => { state.chart.view = 'price'; updateChart(); });
  els.viewPnL.addEventListener('click', () => { state.chart.view = 'pnl'; updateChart(); });
  els.btnAnimate.addEventListener('click', () => { state.chart.anim = !state.chart.anim; updateChart(); });

  // quiz
  els.btnNextQ.addEventListener('click', nextQuizQuestion);
  els.btnSubmitAnswer.addEventListener('click', submitQuizAnswer);

  // strategy
  els.btnEvaluate.addEventListener('click', evaluateStrategy);
  els.btnApplyToSim.addEventListener('click', applyStrategyToChart);
}

// ---------- bootstrap ----------
function bootstrap() {
  // Check onboarding status first
  const showOnboarding = checkOnboardingStatus();
  if (!showOnboarding) {
    document.getElementById('onboarding-overlay').classList.add('hidden');
  }

  // seed inputs & DOM
  setInputsToDOM();
  initChart();
  updateAllFromInputs();
  wire();
  renderBadges();
  // seed quiz
  nextQuizQuestion();
  // fetch BTC & market combo
  fetchBTCData();
}

// Run bootstrap on DOM ready
window.addEventListener('DOMContentLoaded', bootstrap);

// Expose a few functions to console for convenience
window.app = {
  calculateOptionPrice, calculateGreeks, applyPositionSign,
  fetchBTCData, parseMarketGreeks, parseTextReport, mapParsedToCombo,
  simulateStrategyPnL, applyStrategyToChart,
  restartOnboarding, nextOnboardingStep, finishOnboarding
};

