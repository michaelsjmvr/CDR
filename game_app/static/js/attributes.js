(() => {
  const page = document.querySelector('.attribute-layout');
  if (!page) return;

  const socket = window.io ? window.io() : null;
  const csrfToken = page.dataset.csrfToken || '';
  let requestSequence = 0;

  function showNotice(message, category = 'success') {
    const slot = document.querySelector('.attribute-notice-slot');
    if (!slot || !message) return;
    slot.replaceChildren();
    const notice = document.createElement('div');
    notice.className = `notice ${category} talent-notice`;
    notice.setAttribute('role', category === 'error' ? 'alert' : 'status');
    notice.textContent = message;
    slot.append(notice);
    window.setTimeout(() => notice.remove(), 5000);
  }

  function updateEstimate(form) {
    const input = form.querySelector('input[name="amount"]');
    const submit = form.querySelector('button[type="submit"]');
    const estimate = form.querySelector('[data-estimated-value]');
    const warning = form.querySelector('[data-estimate-warning]');
    if (!input || !submit || !estimate || !warning) return;

    const current = Number(form.dataset.current) || 0;
    if (input.disabled) {
      estimate.textContent = current.toLocaleString('pt-BR');
      warning.hidden = true;
      submit.disabled = true;
      return;
    }
    const cap = Number(form.dataset.cap) || 0;
    const available = Number(form.dataset.available) || 0;
    const amount = Number(input.value);
    const valid = Number.isInteger(amount) && amount > 0;
    const exceedsPoints = valid && amount > available;
    const exceedsLimit = valid && current + amount > cap;
    estimate.textContent = (current + (valid ? amount : 0)).toLocaleString('pt-BR');
    warning.hidden = !(exceedsPoints || exceedsLimit);
    warning.textContent = exceedsPoints
      ? `Você tem apenas ${available.toLocaleString('pt-BR')} ponto(s) livre(s).`
      : exceedsLimit
        ? `O limite deste atributo é ${cap.toLocaleString('pt-BR')}.`
        : '';
    submit.disabled = form.dataset.busy === '1' || input.disabled || !valid || exceedsPoints || exceedsLimit;
  }

  document.querySelectorAll('.attribute-allocation-form').forEach((form) => {
    const input = form.querySelector('input[name="amount"]');
    input?.addEventListener('input', () => updateEstimate(form));
    updateEstimate(form);
  });

  function applyState(state, announce = false) {
    if (state.attributes) {
      Object.entries(state.attributes).forEach(([key, value]) => {
        const valueNode = document.querySelector(`[data-attribute-value="${key}"]`);
        if (valueNode) valueNode.textContent = Number(value).toLocaleString('pt-BR');
        const form = document.querySelector(`.attribute-allocation-form[data-attribute="${key}"]`);
        if (!form) return;
        form.dataset.current = String(value);
        form.dataset.available = String(state.attribute_points ?? 0);
        const input = form.querySelector('input[name="amount"]');
        const submit = form.querySelector('button[type="submit"]');
        const available = Number(state.attribute_points) || 0;
        const cap = Number(form.dataset.cap) || 0;
        if (input) {
          input.max = String(available);
          if (Number(input.value) > available && available > 0) input.value = String(available);
          input.disabled = available <= 0 || Number(value) >= cap;
        }
        if (submit && (available <= 0 || Number(value) >= cap)) submit.disabled = true;
        updateEstimate(form);
      });
    }

    if (state.attribute_points !== undefined) {
      const points = Math.max(0, Number(state.attribute_points) || 0);
      const pointsNode = document.querySelector('#attribute-points');
      if (pointsNode) pointsNode.textContent = points.toLocaleString('pt-BR');
      document.querySelectorAll('.attribute-allocation-form').forEach((form) => {
        form.dataset.available = String(points);
        updateEstimate(form);
      });
    }

    if (state.combat_summary) {
      Object.entries(state.combat_summary).forEach(([key, value]) => {
        const node = document.querySelector(`[data-combat-value="${key}"]`);
        if (!node) return;
        if (key.endsWith('_cooldown')) node.textContent = `${Number(value).toLocaleString('pt-BR', { minimumFractionDigits: 3, maximumFractionDigits: 3 })} s`;
        else if (key.endsWith('_damage_exact')) {
          node.textContent = Number(value).toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 });
          if (key === 'elemental_damage_exact' && node.dataset.elementalName) {
            node.textContent += ` · ${node.dataset.elementalName}`;
          }
        }
        else if (key === 'move_speed_bonus') node.textContent = `+${Number(value).toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 })}%`;
        else if (['critical_chance', 'critical_heal', 'dodge_chance', 'damage_reduction', 'ranged_reduction', 'life_steal', 'damage_reflection'].includes(key)) node.textContent = `${(Number(value) * 100).toLocaleString('pt-BR', { minimumFractionDigits: 1, maximumFractionDigits: 1 })}%`;
        else if (key === 'attack_range' || key === 'skill_range') node.textContent = `${Math.round(Number(value)).toLocaleString('pt-BR')} un.`;
        else node.textContent = Number(value).toLocaleString('pt-BR');
      });
    }

    const autoForm = document.querySelector('.attribute-auto-setting');
    if (autoForm && state.auto_allocate_attributes !== undefined) {
      const enabled = Boolean(state.auto_allocate_attributes);
      autoForm.dataset.autoEnabled = enabled ? '1' : '0';
      const enabledInput = autoForm.querySelector('input[name="enabled"]');
      const button = autoForm.querySelector('button[type="submit"]');
      if (enabledInput) enabledInput.value = enabled ? '0' : '1';
      if (button) button.textContent = enabled ? 'Desativar' : 'Ativar';
    }

    if (announce && state.message) showNotice(state.message, 'success');
  }

  function submitSocketAction(form, eventName, payload) {
    if (!socket?.connected) {
      showNotice('Conectando ao servidor. Aguarde alguns segundos e tente novamente.', 'error');
      return;
    }
    const requestId = ++requestSequence;
    form.dataset.busy = '1';
    form.querySelectorAll('button[type="submit"]').forEach((button) => { button.disabled = true; });
    const timeout = window.setTimeout(() => {
      if (form.dataset.busy !== '1') return;
      form.dataset.busy = '0';
      form.querySelectorAll('button[type="submit"]').forEach((button) => { button.disabled = false; });
      form.querySelectorAll('.attribute-allocation-form').forEach(updateEstimate);
      showNotice('O servidor não respondeu a tempo. Confira sua conexão e tente novamente.', 'error');
    }, 10000);
    form.dataset.requestId = String(requestId);
    socket.emit(eventName, { ...payload, csrf_token: csrfToken }, (result) => {
      window.clearTimeout(timeout);
      if (form.dataset.requestId !== String(requestId)) return;
      form.dataset.busy = '0';
      if (!result?.ok) {
        form.querySelectorAll('button[type="submit"]').forEach((button) => { button.disabled = false; });
        form.querySelectorAll('.attribute-allocation-form').forEach(updateEstimate);
        showNotice(result?.error || 'Não foi possível salvar a distribuição.', 'error');
        return;
      }
      form.querySelectorAll('button[type="submit"]').forEach((button) => { button.disabled = false; });
      applyState(result, true);
    });
  }

  document.querySelectorAll('.attribute-allocation-form').forEach((form) => {
    form.addEventListener('submit', (event) => {
      event.preventDefault();
      submitSocketAction(form, 'attributes:allocate', {
        attribute: form.dataset.attribute,
        amount: form.querySelector('input[name="amount"]')?.value,
      });
    });
  });

  const autoForm = document.querySelector('.attribute-auto-setting');
  autoForm?.addEventListener('submit', (event) => {
    event.preventDefault();
    const enabled = Number(autoForm.querySelector('input[name="enabled"]')?.value);
    submitSocketAction(autoForm, 'attributes:auto_toggle', { enabled });
  });

  socket?.on('attributes:updated', (state) => applyState(state, false));
  socket?.on('connect_error', () => showNotice('Conexão em tempo real indisponível. Reconectando…', 'error'));

  document.querySelectorAll('.talent-notice').forEach((notice) => {
    window.setTimeout(() => notice.remove(), 5000);
  });
})();
