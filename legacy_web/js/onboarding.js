// ---------- Onboarding System ----------
let currentOnboardingStep = 1;
const totalOnboardingSteps = 4;

function checkOnboardingStatus() {
  try {
    const completed = localStorage.getItem('onboarding_completed');
    if (completed === 'true') {
      document.getElementById('onboarding-overlay').classList.add('hidden');
      return false;
    }
    return true;
  } catch (e) {
    return true;
  }
}

function nextOnboardingStep(step) {
  // Hide current step
  const currentCard = document.getElementById(`onboarding-step-${currentOnboardingStep}`);
  if (currentCard) currentCard.style.display = 'none';

  // Show new step
  currentOnboardingStep = step;
  const newCard = document.getElementById(`onboarding-step-${currentOnboardingStep}`);
  if (newCard) {
    newCard.style.display = 'block';

    // Add visual highlights for step 3
    if (step === 3) {
      setTimeout(() => {
        highlightOnboardingElements();
      }, 300);
    } else {
      removeHighlights();
    }
  }
}

function loadStrategyFromOnboarding(strategyType) {
  // Close onboarding temporarily to show the app
  const overlay = document.getElementById('onboarding-overlay');
  overlay.style.opacity = '0.3';
  overlay.style.pointerEvents = 'none';

  // Load the strategy
  if (strategyType === 'call') {
    els.inpSide.value = 'call';
    els.inpPosition.value = 'long';
    updateAllFromInputs();
    state.chart.view = 'price';
    updateChart();
  } else if (strategyType === 'put') {
    els.inpSide.value = 'put';
    els.inpPosition.value = 'long';
    updateAllFromInputs();
    state.chart.view = 'price';
    updateChart();
  } else if (strategyType === 'iron_condor') {
    els.strategyChoice.value = 'iron_condor';
    evaluateStrategy();
    applyStrategyToChart();
  }

  // Show a brief message
  setTimeout(() => {
    alert(`Strategy loaded! Check the chart and metrics. When ready, continue the tour.`);
    overlay.style.opacity = '1';
    overlay.style.pointerEvents = 'auto';
  }, 500);
}

function highlightOnboardingElements() {
  // Highlight the controls section
  const controlsSection = document.querySelector('aside h2');
  if (controlsSection) {
    controlsSection.closest('aside').classList.add('onboarding-highlight');
  }

  // Highlight the chart
  const chartSection = document.querySelector('#mainChart');
  if (chartSection) {
    chartSection.closest('section').classList.add('onboarding-highlight');
  }
}

function removeHighlights() {
  document.querySelectorAll('.onboarding-highlight').forEach(el => {
    el.classList.remove('onboarding-highlight');
  });
}

function skipOnboarding() {
  if (confirm('Skip the guided tour? You can always restart it later.')) {
    finishOnboarding(true);
  }
}

function finishOnboarding(skipped = false) {
  try {
    localStorage.setItem('onboarding_completed', 'true');
  } catch (e) { }

  const overlay = document.getElementById('onboarding-overlay');
  overlay.style.opacity = '0';
  overlay.style.transition = 'opacity 0.3s';

  setTimeout(() => {
    overlay.classList.add('hidden');
    removeHighlights();
  }, 300);

  if (!skipped) {
    // Show a welcome message
    setTimeout(() => {
      alert('Welcome! Explore the app freely. Use the strategy selector and sliders to experiment.');
    }, 400);
  }
}

function restartOnboarding() {
  try {
    localStorage.removeItem('onboarding_completed');
    currentOnboardingStep = 1;
    const overlay = document.getElementById('onboarding-overlay');
    overlay.classList.remove('hidden');
    overlay.style.opacity = '1';
    overlay.style.transition = '';

    // Show step 1
    for (let i = 1; i <= totalOnboardingSteps; i++) {
      const step = document.getElementById(`onboarding-step-${i}`);
      if (step) step.style.display = i === 1 ? 'block' : 'none';
    }
  } catch (e) { }
}

// Expose onboarding functions globally for onclick handlers
window.nextOnboardingStep = nextOnboardingStep;
window.loadStrategyFromOnboarding = loadStrategyFromOnboarding;
window.skipOnboarding = skipOnboarding;
window.finishOnboarding = finishOnboarding;
window.restartOnboarding = restartOnboarding;

