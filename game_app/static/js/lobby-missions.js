(() => {
  const container = document.querySelector('.mission-selection');
  const difficultySelect = document.querySelector('#mission-difficulty');
  const phaseSelect = document.querySelector('#mission-phase');
  const startButton = document.querySelector('#mission-start-form button[type="submit"]');
  if (!container || !difficultySelect || !phaseSelect || !startButton) return;

  const states = JSON.parse(container.dataset.difficultyStates);
  const phases = [...phaseSelect.options];
  const updatePhases = () => {
    const state = states.find((item) => item.key === difficultySelect.value);
    const available = new Set(state?.available_phases || []);
    phases.forEach((option) => {
      option.disabled = !available.has(Number(option.value));
    });
    if (!available.has(Number(phaseSelect.value))) {
      phaseSelect.value = String(state?.available_phases?.[0] || '');
    }
    phaseSelect.disabled = available.size === 0;
    startButton.disabled = available.size === 0;
  };
  difficultySelect.addEventListener('change', updatePhases);
  updatePhases();
})();
