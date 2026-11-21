(() => {
  const bridge = window.terminalVilarMapEditorBridge;
  const editor = document.querySelector('#map-editor');
  const canvas = document.querySelector('#gameCanvas');
  const list = document.querySelector('#collider-list');
  const status = document.querySelector('#editor-status');
  const editButton = document.querySelector('#btnEditor');
  const colliderFields = [...document.querySelectorAll('[data-collider-field]')];
  const boundFields = [...document.querySelectorAll('[data-bound]')];
  const mapConfig = bridge.mapConfig;
  const previewGeometry = bridge.previewConfig.geometry;
  let selectedId = null;
  let dirty = false;
  let dragging = null;

  const setStatus = (message, kind = '') => {
    status.textContent = message;
    status.dataset.kind = kind;
  };

  const selectedCollider = () => bridge.colliders.find(({ id }) => id === selectedId);

  function refreshList() {
    list.replaceChildren();
    for (const collider of bridge.colliders) {
      const option = document.createElement('option');
      option.value = collider.id;
      option.textContent = collider.id;
      option.selected = collider.id === selectedId;
      list.append(option);
    }
    document.querySelector('#delete-collider').disabled = !selectedCollider();
    document.querySelector('#collider-fields').disabled = !selectedCollider();
  }

  function showSelectedFields() {
    const collider = selectedCollider();
    document.querySelector('#collider-id').value = collider?.id || '';
    document.querySelector('#collider-angle').value = collider
      ? String(Number((collider.angle * 180 / Math.PI).toFixed(1)))
      : '';
    for (const input of colliderFields) {
      const key = input.dataset.colliderField;
      input.value = collider ? String(collider[key]) : '';
      input.disabled = !collider;
    }
    document.querySelector('#collider-id').disabled = !collider;
    document.querySelector('#collider-angle').disabled = !collider;
    refreshList();
  }

  function syncBoundsToPreview() {
    const player = mapConfig.player_bounds;
    const spawn = mapConfig.spawn_bounds;
    previewGeometry.playerBounds = {
      minX: player.min_x,
      maxX: player.max_x,
      minY: player.min_y,
      maxY: player.max_y,
    };
    previewGeometry.spawnCandidateBounds = {
      minX: spawn.min_x,
      maxX: spawn.max_x,
      minY: spawn.min_y,
      maxY: spawn.max_y,
    };
  }

  function showBoundsFields() {
    for (const input of boundFields) {
      input.value = String(mapConfig[input.dataset.bound][input.dataset.axis]);
    }
  }

  function validateBounds() {
    const { width, height } = mapConfig.world;
    const player = mapConfig.player_bounds;
    const spawn = mapConfig.spawn_bounds;
    for (const [name, bounds] of [['movimento', player], ['spawn', spawn]]) {
      if (
        bounds.min_x < 0 || bounds.min_y < 0
        || bounds.max_x > width || bounds.max_y > height
        || bounds.min_x >= bounds.max_x || bounds.min_y >= bounds.max_y
      ) {
        return `Revise os limites de ${name}: devem formar um retângulo dentro do mundo.`;
      }
    }
    if (
      spawn.min_x < player.min_x || spawn.max_x > player.max_x
      || spawn.min_y < player.min_y || spawn.max_y > player.max_y
    ) {
      return 'A área de spawn precisa ficar dentro do limite de movimento.';
    }
    if (
      Math.ceil(spawn.min_x) > Math.floor(spawn.max_x)
      || Math.ceil(spawn.min_y) > Math.floor(spawn.max_y)
    ) {
      return 'A área de spawn precisa conter coordenadas inteiras em X e Y.';
    }
    if (
      player.min_x > 1200 || player.max_x < 1200
      || player.min_y > 900 || player.max_y < 900
    ) {
      return 'O limite de movimento precisa incluir o ponto inicial (1.200, 900).';
    }
    return '';
  }

  function validateCollider(collider) {
    if (!/^[a-z0-9][a-z0-9_-]{0,63}$/.test(collider.id)) {
      return 'O ID deve usar letras minúsculas, números, hífen ou sublinhado.';
    }
    if (bridge.colliders.some((other) => other !== collider && other.id === collider.id)) {
      return 'Já existe um colisor com esse ID.';
    }
    if (
      ![collider.x, collider.y, collider.width, collider.height, collider.angle].every(Number.isFinite)
      || collider.width <= 0 || collider.height <= 0
      || collider.width > mapConfig.world.width * 2
      || collider.height > mapConfig.world.height * 2
      || collider.angle < -Math.PI || collider.angle > Math.PI
    ) {
      return 'As coordenadas, dimensões ou rotação do colisor são inválidas.';
    }
    return '';
  }

  function markDirty(message = 'Alterações ainda não salvas.') {
    dirty = true;
    setStatus(message);
  }

  function refreshEditor() {
    showSelectedFields();
    syncBoundsToPreview();
    bridge.render();
  }

  function getWorldPoint(event) {
    const rect = canvas.getBoundingClientRect();
    return {
      x: (event.clientX - rect.left) / rect.width * mapConfig.world.width,
      y: (event.clientY - rect.top) / rect.height * mapConfig.world.height,
    };
  }

  function localPoint(point, collider) {
    const dx = point.x - collider.x;
    const dy = point.y - collider.y;
    const cosine = Math.cos(collider.angle);
    const sine = Math.sin(collider.angle);
    return {
      x: dx * cosine + dy * sine,
      y: -dx * sine + dy * cosine,
    };
  }

  function containsPoint(point, collider) {
    const local = localPoint(point, collider);
    return Math.abs(local.x) <= collider.width / 2
      && Math.abs(local.y) <= collider.height / 2;
  }

  function cornerAt(point, collider) {
    const local = localPoint(point, collider);
    const threshold = 18 * mapConfig.world.width / canvas.getBoundingClientRect().width;
    for (const signX of [-1, 1]) {
      for (const signY of [-1, 1]) {
        const dx = local.x - signX * collider.width / 2;
        const dy = local.y - signY * collider.height / 2;
        if (Math.hypot(dx, dy) <= threshold) return { signX, signY };
      }
    }
    return null;
  }

  function addCollider() {
    if (bridge.colliders.length >= 100) {
      setStatus('O editor aceita até 100 colisores.', 'error');
      return;
    }
    let number = bridge.colliders.length + 1;
    let id = `collider-${number}`;
    while (bridge.colliders.some((collider) => collider.id === id)) {
      id = `collider-${++number}`;
    }
    const collider = {
      id,
      x: mapConfig.world.width / 2,
      y: mapConfig.world.height / 2,
      width: 120,
      height: 80,
      angle: 0,
    };
    bridge.colliders.push(collider);
    selectedId = id;
    markDirty();
    refreshEditor();
  }

  function removeCollider() {
    const index = bridge.colliders.findIndex(({ id }) => id === selectedId);
    if (index < 0) return;
    bridge.colliders.splice(index, 1);
    selectedId = bridge.colliders[index]?.id || bridge.colliders[index - 1]?.id || null;
    markDirty();
    refreshEditor();
  }

  function setEditorOpen(open) {
    editor.hidden = !open;
    document.body.classList.toggle('editor-open', open);
    editButton.classList.toggle('active', open);
    editButton.setAttribute('aria-expanded', String(open));
    for (const id of ['resetBtn', 'debugBtn']) {
      const control = document.getElementById(id);
      if (control) control.disabled = open;
    }
    bridge.setEditorMode(open);
    if (open) {
      showBoundsFields();
      refreshEditor();
      setStatus(dirty ? 'Alterações ainda não salvas.' : 'Arraste os colisores na planta ou edite os campos.');
    }
  }

  async function saveMap() {
    if (saveMap.busy) return;
    const boundsError = validateBounds();
    if (boundsError) {
      setStatus(boundsError, 'error');
      return;
    }
    for (const collider of bridge.colliders) {
      const colliderError = validateCollider(collider);
      if (colliderError) {
        setStatus(`${collider.id}: ${colliderError}`, 'error');
        return;
      }
    }
    saveMap.busy = true;
    const saveButton = document.querySelector('#save-map');
    saveButton.disabled = true;
    setStatus('Salvando a configuração do mapa…');
    try {
      const response = await fetch('/mapas/terminal-vilar-fase1/salvar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...JSON.parse(JSON.stringify(mapConfig)),
          csrf_token: editor.dataset.csrfToken,
        }),
      });
      const responseText = await response.text();
      let result;
      try {
        result = JSON.parse(responseText);
      } catch {
        throw new Error(`O servidor respondeu de forma inesperada (${response.status}).`);
      }
      if (!response.ok || !result.ok) {
        throw new Error(result.error || `Não foi possível salvar (${response.status}).`);
      }
      Object.assign(mapConfig, result.map_config);
      bridge.colliders.splice(0, bridge.colliders.length, ...result.map_config.colliders);
      mapConfig.colliders = bridge.colliders;
      selectedId = bridge.colliders.some(({ id }) => id === selectedId)
        ? selectedId
        : bridge.colliders[0]?.id || null;
      syncBoundsToPreview();
      showBoundsFields();
      refreshEditor();
      dirty = false;
      setStatus('Mapa salvo no projeto. Recarregue páginas de jogo já abertas para aplicar os novos colisores e limites.', 'success');
    } catch (error) {
      setStatus(error.message || 'Falha ao salvar o mapa.', 'error');
    } finally {
      saveMap.busy = false;
      saveButton.disabled = false;
    }
  }

  function drawSelectionOverlay(context) {
    const collider = selectedCollider();
    if (!collider) return;
    context.save();
    context.translate(collider.x, collider.y);
    context.rotate(collider.angle);
    context.strokeStyle = '#22d3ee';
    context.lineWidth = 5;
    context.setLineDash([]);
    context.strokeRect(
      -collider.width / 2,
      -collider.height / 2,
      collider.width,
      collider.height,
    );
    context.fillStyle = '#f8fafc';
    context.strokeStyle = '#0f172a';
    context.lineWidth = 2;
    for (const signX of [-1, 1]) {
      for (const signY of [-1, 1]) {
        context.beginPath();
        context.rect(signX * collider.width / 2 - 7, signY * collider.height / 2 - 7, 14, 14);
        context.fill();
        context.stroke();
      }
    }
    context.restore();
  }

  editButton.addEventListener('click', () => setEditorOpen(editor.hidden));
  document.querySelector('#close-editor').addEventListener('click', () => setEditorOpen(false));
  document.querySelector('#add-collider').addEventListener('click', addCollider);
  document.querySelector('#delete-collider').addEventListener('click', removeCollider);
  document.querySelector('#save-map').addEventListener('click', saveMap);
  document.querySelector('#discard-map').addEventListener('click', () => {
    if (dirty && !window.confirm('Descartar as alterações não salvas e recarregar o mapa?')) return;
    window.location.reload();
  });

  list.addEventListener('change', () => {
    selectedId = list.value || null;
    showSelectedFields();
    bridge.render();
  });

  for (const input of colliderFields) {
    input.addEventListener('input', () => {
      const collider = selectedCollider();
      if (!collider) return;
      const value = input.valueAsNumber;
      if (!Number.isFinite(value)) return;
      collider[input.dataset.colliderField] = value;
      markDirty();
      const error = validateCollider(collider);
      if (error) {
        setStatus(error, 'error');
        return;
      }
      refreshList();
      bridge.render();
    });
  }

  document.querySelector('#collider-angle').addEventListener('input', (event) => {
    const collider = selectedCollider();
    const degrees = event.currentTarget.valueAsNumber;
    if (!collider || !Number.isFinite(degrees)) return;
    collider.angle = degrees * Math.PI / 180;
    markDirty();
    const error = validateCollider(collider);
    if (error) {
      setStatus(error, 'error');
      return;
    }
    refreshList();
    bridge.render();
  });

  document.querySelector('#collider-id').addEventListener('change', (event) => {
    const collider = selectedCollider();
    if (!collider) return;
    const oldId = collider.id;
    const candidateId = event.currentTarget.value.trim();
    collider.id = candidateId;
    const error = validateCollider(collider);
    if (error) {
      collider.id = oldId;
      event.currentTarget.value = oldId;
      setStatus(error, 'error');
      return;
    }
    selectedId = candidateId;
    markDirty();
    refreshEditor();
  });

  for (const input of boundFields) {
    input.addEventListener('input', () => {
      const value = input.valueAsNumber;
      if (!Number.isFinite(value)) return;
      mapConfig[input.dataset.bound][input.dataset.axis] = value;
      syncBoundsToPreview();
      markDirty();
      const error = validateBounds();
      if (error) {
        setStatus(error, 'error');
        return;
      }
      bridge.render();
    });
  }

  canvas.addEventListener('pointerdown', (event) => {
    if (editor.hidden || event.button !== 0) return;
    const point = getWorldPoint(event);
    const selected = selectedCollider();
    const corner = selected ? cornerAt(point, selected) : null;
    if (corner) {
      dragging = { mode: 'resize', collider: selected, ...corner };
    } else {
      const hit = [...bridge.colliders].reverse().find((collider) => containsPoint(point, collider));
      if (!hit) return;
      selectedId = hit.id;
      dragging = {
        mode: 'move',
        collider: hit,
        offsetX: point.x - hit.x,
        offsetY: point.y - hit.y,
      };
    }
    canvas.setPointerCapture(event.pointerId);
    refreshEditor();
  });

  canvas.addEventListener('pointermove', (event) => {
    if (!dragging) return;
    const point = getWorldPoint(event);
    if (dragging.mode === 'move') {
      dragging.collider.x = point.x - dragging.offsetX;
      dragging.collider.y = point.y - dragging.offsetY;
    } else {
      const local = localPoint(point, dragging.collider);
      dragging.collider.width = Math.max(1, Math.abs(local.x) * 2);
      dragging.collider.height = Math.max(1, Math.abs(local.y) * 2);
    }
    markDirty();
    refreshEditor();
  });

  for (const eventName of ['pointerup', 'pointercancel', 'lostpointercapture']) {
    canvas.addEventListener(eventName, () => { dragging = null; });
  }

  window.addEventListener('beforeunload', (event) => {
    if (!dirty) return;
    event.preventDefault();
    event.returnValue = '';
  });

  bridge.drawSelectionOverlay = drawSelectionOverlay;
  showSelectedFields();
  showBoundsFields();
  refreshList();
})();
