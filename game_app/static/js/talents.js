(() => {
  const map = document.querySelector('.talent-graph-map');
  if (!map) return;

  const nodes = [...map.querySelectorAll('.talent-map-node')];
  const selectedSpecialization = map.dataset.selectedSpecialization || '';
  const inspector = {
    category: document.querySelector('#selected-node-category'),
    name: document.querySelector('#selected-node-name'),
    effect: document.querySelector('#selected-node-effect'),
    cost: document.querySelector('#selected-node-cost'),
    talentId: document.querySelector('#selected-talent-id'),
    form: document.querySelector('#talent-node-purchase'),
    status: document.querySelector('#selected-node-status'),
  };
  const labels = {
    small: 'TALENTO',
    notable: 'TALENTO ESPECIAL',
    keystone: 'HABILIDADE ESPECIAL',
    socket: 'ESPAÇO DE MELHORIA',
    starting: 'INÍCIO DA CLASSE',
    ultimate: 'HABILIDADE SUPREMA',
    spell_upgrade: 'MAESTRIA DE MAGIA',
  };

  function chooseNode(node) {
    nodes.forEach((item) => {
      const selected = item === node;
      item.classList.toggle('is-selected', selected);
      item.setAttribute('aria-pressed', String(selected));
    });
    const data = node.dataset;
    const isRoot = data.currentRoot === '1';
    const purchased = data.purchased === '1';
    const canUnlock = data.canUnlock === '1';
    const allocatable = data.allocatable === '1';
    const canPurchase = data.canPurchase === '1';

    if (inspector.category) inspector.category.textContent = labels[data.category] || 'NÓ';
    if (inspector.name) inspector.name.textContent = data.name || 'Nó da árvore';
    if (inspector.effect) inspector.effect.textContent = data.effect || '';
    const cost = Number(data.cost || 0);
    const pointLabel = cost === 1 ? 'Ponto de Legado' : 'Pontos de Legado';
    if (inspector.cost) inspector.cost.textContent = isRoot ? 'Início da classe' : `${cost} ${pointLabel}`;
    if (inspector.talentId) inspector.talentId.value = node.dataset.nodeId || '';
    if (inspector.form) inspector.form.hidden = !canPurchase;

    let status = '';
    if (isRoot) status = 'Raiz comum das três evoluções';
    else if (purchased) status = 'Já adquirido';
    else if (!selectedSpecialization) status = 'Esse é um dos três caminhos. Escolha somente um ao alcançar o nível 100.';
    else if (data.specializationId !== selectedSpecialization) status = 'Este é um dos outros dois caminhos e permanece bloqueado.';
    else if (!allocatable) status = 'Este espaço ainda não está disponível.';
    else if (!canUnlock) status = 'Desbloqueie o talento anterior deste caminho primeiro.';
    else if (!canPurchase) status = 'Você ainda não tem Pontos de Legado suficientes.';
    else status = 'Conectado ao seu caminho e disponível para investimento.';
    if (inspector.status) inspector.status.textContent = status;
  }

  nodes.forEach((node) => {
    node.addEventListener('click', () => chooseNode(node));
    node.addEventListener('pointerenter', () => chooseNode(node));
    node.addEventListener('focus', () => chooseNode(node));
    node.addEventListener('keydown', (event) => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault();
        chooseNode(node);
      }
    });
  });

  const initial = nodes.find((node) => node.classList.contains('is-current-root'))
    || nodes.find((node) => node.classList.contains('is-available'))
    || nodes[0];
  if (initial) chooseNode(initial);

  const specializationDialog = document.querySelector('.specialization-dialog');
  document.querySelector('[data-open-specializations]')?.addEventListener('click', () => {
    if (specializationDialog?.showModal) specializationDialog.showModal();
  });
  document.querySelector('[data-close-specializations]')?.addEventListener('click', () => {
    specializationDialog?.close();
  });
  specializationDialog?.addEventListener('click', (event) => {
    if (event.target === specializationDialog) specializationDialog.close();
  });

  const specializationPreview = {
    name: document.querySelector('#specialization-preview-name'),
    description: document.querySelector('#specialization-preview-description'),
    passiveName: document.querySelector('#specialization-preview-passive-name'),
    passive: document.querySelector('#specialization-preview-passive'),
    attributes: document.querySelector('#specialization-preview-attributes'),
    branch: document.querySelector('#specialization-preview-branch'),
    skill: document.querySelector('#specialization-preview-skill'),
    skillDescription: document.querySelector('#specialization-preview-skill-description'),
    ultimates: document.querySelector('#specialization-preview-ultimates'),
    ultimatesDescription: document.querySelector('#specialization-preview-ultimates-description'),
  };
  const specializationOptions = [...document.querySelectorAll('.specialization-option')];
  function previewSpecialization(option) {
    const data = option.dataset;
    if (specializationPreview.name) specializationPreview.name.textContent = data.name;
    if (specializationPreview.description) specializationPreview.description.textContent = data.description;
    if (specializationPreview.passiveName) specializationPreview.passiveName.textContent = data.passiveName;
    if (specializationPreview.passive) specializationPreview.passive.textContent = data.passiveDescription;
    if (specializationPreview.attributes) specializationPreview.attributes.textContent = data.attributes;
    if (specializationPreview.branch) {
      specializationPreview.branch.textContent =
        `Caminho completo: ${data.branchCost} Pontos de Legado (${data.attributeCost} em atributos + ${data.otherCombatCost} em vantagens + ${data.spellUpgradeCost} em maestrias + ${data.epicUnlockCost} em habilidades supremas + ${data.keystoneCost} na habilidade especial).`;
    }
    if (specializationPreview.skill) {
      specializationPreview.skill.textContent = `${data.baseSkill} → ${data.skillName}`;
    }
    if (specializationPreview.skillDescription) {
      specializationPreview.skillDescription.textContent =
        `${data.skillDescription} Custa ${data.skillMana} Mana e tem recarga de ${data.skillCooldown}s.`;
    }
    const epicSkills = JSON.parse(data.epicSkills || '[]');
    if (specializationPreview.ultimates) {
      specializationPreview.ultimates.textContent =
        epicSkills.map((skill) => skill.name).join(' · ');
    }
    if (specializationPreview.ultimatesDescription) {
      specializationPreview.ultimatesDescription.textContent = epicSkills
        .map((skill) => `${skill.description} (${skill.mana} Mana; recarga de ${skill.cooldown}s)`)
        .join(' ');
    }
  }
  specializationOptions.forEach((option) => {
    option.addEventListener('pointerenter', () => previewSpecialization(option));
    option.addEventListener('focusin', () => previewSpecialization(option));
    option.addEventListener('click', () => previewSpecialization(option));
  });
})();
