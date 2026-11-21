(() => {
  const canvas = document.querySelector('#game');
  const ctx = canvas.getContext('2d');
  const coordinates = document.querySelector('#coordinates');
  const orbData = document.querySelector('#card-xp-orbs');
  const dialogueHooks = JSON.parse(
    document.querySelector('#mission-dialogue-hooks')?.textContent
      || '{"status":"pending","mission_start":null,"boss_encounter":null}'
  );
  const dispatchDialogueHook = (kind, context) => {
    window.dispatchEvent(new CustomEvent('game:dialogue-hook', {
      detail: {
        kind,
        status: dialogueHooks.status,
        dialogue: dialogueHooks[kind],
        context,
      },
    }));
  };
  const sceneLabel = document.querySelector('.scene-label');
  const mapIndex = Math.max(0, Math.min(8, Number(sceneLabel?.dataset.mapIndex || 0)));
  const scenePhase = Number(sceneLabel?.dataset.phase || 1);
  const isTerminalVilarPhase = scenePhase === 1 && mapIndex === 0;
  const mapConfigElement = document.querySelector('#terminal-vilar-map-config');
  const terminalVilarMapConfig = isTerminalVilarPhase
    ? JSON.parse(mapConfigElement?.textContent || 'null')
    : null;
  const collisionMapElement = document.querySelector('#terminal-vilar-collision-map');
  const terminalVilarColliders = isTerminalVilarPhase
    ? JSON.parse(collisionMapElement?.textContent || '[]')
    : [];
  const terminalVilarSolidPolygons = isTerminalVilarPhase
    ? terminalVilarMapConfig.solid_polygons
    : [];
  const terminalVilarCollisionWalls = isTerminalVilarPhase
    ? terminalVilarMapConfig.collision_walls
    : [];
  const withTerminalVilarCollider = (id, visual) => {
    const collider = terminalVilarColliders.find((entry) => entry.id === id);
    return collider ? { ...collider, ...visual } : null;
  };
  const terminalVilarArtwork = isTerminalVilarPhase ? new Image() : null;
  let terminalVilarArtworkLoaded = false;
  if (terminalVilarArtwork) {
    terminalVilarArtwork.addEventListener('load', () => {
      terminalVilarArtworkLoaded = true;
    });
    terminalVilarArtwork.addEventListener('error', () => {
      console.error('Não foi possível carregar a arte do mapa Terminal de Vilar.');
    });
    const artworkUrl = new URL(
      '../images/maps/terminal_vilar_fase1.jpg',
      document.currentScript.src,
    );
    artworkUrl.searchParams.set('v', '0.139');
    terminalVilarArtwork.src = artworkUrl.href;
  }
  const terminalVilarEffects = isTerminalVilarPhase
    ? window.createTerminalVilarEffects(terminalVilarArtwork)
    : null;
  const mapThemes = [
    { floor: ['#202327', '#24272a', '#1d2226', '#292a2a'], grout: '#b7a982', edge: '#b7a982', accent: '#c4a561' },
    { floor: ['#202725', '#252b29', '#1c2526', '#292e2b'], grout: '#8fa9a2', edge: '#78988f', accent: '#7fc4c2' },
    { floor: ['#242322', '#2a2825', '#201f20', '#302a27'], grout: '#b18b67', edge: '#a9795b', accent: '#d38b60' },
    { floor: ['#1d2429', '#202a30', '#1c222b', '#252d32'], grout: '#88a6bd', edge: '#7792a5', accent: '#78bfd1' },
    { floor: ['#252128', '#2b2530', '#211e28', '#302a32'], grout: '#ab91b9', edge: '#9679a7', accent: '#c49ed8' },
    { floor: ['#202823', '#252e27', '#1c241f', '#2a3028'], grout: '#95a887', edge: '#7d9974', accent: '#aecb80' },
    { floor: ['#292321', '#302725', '#252120', '#352925'], grout: '#bb8d71', edge: '#a7735f', accent: '#dc8e62' },
    { floor: ['#1c252c', '#202d33', '#1b232b', '#293137'], grout: '#89b1c2', edge: '#6996a8', accent: '#73d0dd' },
    { floor: ['#282722', '#302f28', '#242722', '#34332a'], grout: '#b6a879', edge: '#aa9866', accent: '#d7bd75' },
  ];
  const cardXpOrbs = JSON.parse(orbData?.dataset.orbs || '[]');
  let isPremium = orbData?.dataset.premium === '1';
  const baseAttackRange = Math.max(70, Number(orbData?.dataset.baseAttackRange || 120));
  const skillAttackRange = Math.max(baseAttackRange, Number(orbData?.dataset.baseSkillRange || baseAttackRange * 1.35));
  const collectingOrbs = new Set();
  const appliedOrbCollections = new Set();
  const socket = window.io ? window.io() : null;
  const keys = new Set();
  const heldMouseButtons = new Set();
  const mouse = { x: window.innerWidth / 2, y: window.innerHeight / 2 - 100 };
  const world = isTerminalVilarPhase
    ? { ...terminalVilarMapConfig.world }
    : { width: 2400, height: 1800 };
  const mapPlayerBounds = isTerminalVilarPhase
    ? terminalVilarMapConfig.player_bounds
    : null;
  const clampWorldX = (x) => Math.max(
    mapPlayerBounds ? mapPlayerBounds.min_x : 130,
    Math.min(mapPlayerBounds ? mapPlayerBounds.max_x : world.width - 130, x),
  );
  const clampWorldY = (y) => Math.max(
    mapPlayerBounds ? mapPlayerBounds.min_y : 130,
    Math.min(mapPlayerBounds ? mapPlayerBounds.max_y : world.height - 130, y),
  );
  const TERMINAL_VILAR_MAP = {
    geometry: {
      tileSize: 96,
      tileFill: 94,
      borderOffset: 110,
      platform: { x: 640, y: 700, width: 1120, height: 520 },
      canopy: { x: 740, y: 455, width: 940, depth: 162 },
    },
    palette: {
      asphalt: '#191c20',
      tiles: ['#202327', '#24272a', '#1d2226', '#292a2a'],
      concrete: '#373b42',
      concreteDark: '#25282e',
      neon: '#c026d3',
      neonBright: '#e879f9',
    },
    pillars: [
      withTerminalVilarCollider('canopy-post-west', { visualHeight: 155, posters: ['#eab308', '#ef4444'] }),
      withTerminalVilarCollider('canopy-post-west-center', { visualHeight: 155, posters: ['#38bdf8', '#f8fafc'] }),
      withTerminalVilarCollider('canopy-post-east-center', { visualHeight: 155, posters: ['#f97316', '#e2e8f0'] }),
      withTerminalVilarCollider('canopy-post-east', { visualHeight: 155, posters: ['#a855f7', '#fde047'] }),
      withTerminalVilarCollider('plaza-pillar-west', { visualHeight: 230, posters: ['#f43f5e', '#cbd5e1'] }),
      withTerminalVilarCollider('plaza-pillar-west-center', { visualHeight: 230, posters: ['#22c55e', '#f1f5f9'] }),
      withTerminalVilarCollider('plaza-pillar-east-center', { visualHeight: 230, posters: ['#38bdf8', '#f8fafc'] }),
      withTerminalVilarCollider('plaza-pillar-east', { visualHeight: 230, posters: ['#eab308', '#ef4444'] }),
    ].filter(Boolean),
    buses: [
      withTerminalVilarCollider('bus-northwest', { silhouettes: 3 }),
      withTerminalVilarCollider('bus-west', { vertical: true, silhouettes: 4 }),
      withTerminalVilarCollider('bus-east', { vertical: true, silhouettes: 4 }),
      withTerminalVilarCollider('bus-southwest', { silhouettes: 3 }),
      withTerminalVilarCollider('bus-south-center', { silhouettes: 4 }),
      withTerminalVilarCollider('bus-southeast', { silhouettes: 3 }),
    ].filter(Boolean),
    puddles: [
      { x: 520, y: 1280, rx: 140, ry: 65, neon: true },
      { x: 960, y: 1390, rx: 130, ry: 55, neon: true },
      { x: 1480, y: 1360, rx: 110, ry: 50, neon: true },
      { x: 1950, y: 1270, rx: 120, ry: 60, neon: true },
      { x: 890, y: 1050, rx: 95, ry: 48, neon: true },
      { x: 1580, y: 510, rx: 85, ry: 42, neon: false },
    ],
    streetlights: [
      { x: 610, y: 350, flicker: 0.85 },
      { x: 1810, y: 350, flicker: 0.92 },
      { x: 710, y: 1450, flicker: 0.78 },
      { x: 1760, y: 1450, flicker: 0.88 },
    ],
    rifts: [
      { x: 980, y: 58, rx: 220, ry: 48 },
      { x: 1560, y: 78, rx: 150, ry: 36 },
    ],
  };
  // 58° downward pitch from the horizon; cosine gives the floor's projected Y scale.
  // Tune pitch, zoom limits, and wheel speed here without changing world coordinates.
  const CAMERA_PITCH_DEGREES = 58;
  const CAMERA_CONFIG = Object.freeze({
    minZoom: 0.72,
    maxZoom: 1.6,
    initialZoom: 1,
    zoomSmoothing: 8,
    pitchDegrees: CAMERA_PITCH_DEGREES,
    tiltY: Math.cos(CAMERA_PITCH_DEGREES * Math.PI / 180),
    wheelStep: 0.12,
  });
  const cameraTiltY = isTerminalVilarPhase ? 1 : CAMERA_CONFIG.tiltY;
  let cameraZoom = CAMERA_CONFIG.initialZoom;
  let targetCameraZoom = CAMERA_CONFIG.initialZoom;
  let currentCamera = { x: 0, y: 0, viewWidth: 0, viewHeight: 0, zoom: CAMERA_CONFIG.initialZoom, tiltY: cameraTiltY };
  let controlScheme = orbData?.dataset.controlScheme || 'mouse_keyboard';
  let skillSlots = JSON.parse(orbData?.dataset.skillSlots || '["basic","","",""]');
  let mouseLeftSlot = Number(orbData?.dataset.mouseLeftSlot || 2);
  let mouseRightSlot = Number(orbData?.dataset.mouseRightSlot || 2);
  const player = { x: world.width / 2, y: world.height / 2, radius: 13, speed: 245 };
  const dash = { remaining: 0, duration: 0.2, speed: 720, direction: -Math.PI / 2 };
  const enemies = JSON.parse(orbData?.dataset.enemies || '[]').map(prepareEnemy);
  dispatchDialogueHook('mission_start', {
    phase: Number(sceneLabel?.dataset.phase || 1),
    difficulty: sceneLabel?.dataset.difficulty || 'risk_low',
  });
  const enemyAttacks = [];
  const playerProjectiles = [];
  const skillEffects = [];
  const skillCooldowns = new Map();
  const localAttackCooldowns = new Map();
  const fallbackNoticeTimes = new Map();
  let width = 0;
  let height = 0;
  let pixelRatio = 1;
  let previousTime = 0;
  const potionToggleRequests = new Set();
  let aimAngle = -Math.PI / 2;
  let attackInFlight = false;
  let playerProjectileInFlight = false;
  let dashRequestInFlight = false;
  let phasePreparationUntil = Number(orbData?.dataset.phasePreparationUntil || 0);
  let pendingCardChoices = Number(orbData?.dataset.pendingCardChoices || 0);
  let latestCardOfferRevision = Number(orbData?.dataset.cardOfferRevision || 0);
  let latestCardOfferResolved = orbData?.dataset.cardOfferResolved === '1';
  let cardChoiceInFlight = false;
  let cardAutoPickInterval = null;
  let cardAutoPickOfferId = 0;
  let cardAutoPickSubmittedId = 0;
  let targetedEnemy = null;
  let targetPortraitEnemyId = null;
  let activeCardsFull = Number(orbData?.dataset.activeCardCount || 0)
    >= Number(orbData?.dataset.cardLimit || 6);
  let activeCardData = JSON.parse(orbData?.dataset.activeCards || '[]');
  let orbCollectionInFlight = null;
  let orbCollectionRetryAt = 0;
  const agility = Math.max(0, Number(orbData?.dataset.agility || 0));
  let cooldownScale = Math.max(.5, 1 - agility * .005) * Number(orbData?.dataset.cooldownMultiplier || 1);
  let moveSpeedMultiplier = Number(orbData?.dataset.moveSpeedMultiplier || 1);
  let attackRangeMultiplier = Number(orbData?.dataset.attackRangeMultiplier || 1);

  window.addEventListener('pointermove', (event) => {
    const bounds = canvas.getBoundingClientRect();
    mouse.x = event.clientX - bounds.left;
    mouse.y = event.clientY - bounds.top;
  });
  canvas.addEventListener('mousedown', (event) => {
    if (event.button !== 0 && event.button !== 2) return;
    if (controlScheme === 'keyboard_only') return;
    event.preventDefault();
    heldMouseButtons.add(event.button);
    const assignedSlot = event.button === 0 ? mouseLeftSlot : mouseRightSlot;
    const action = assignedSlot >= 2 ? skillSlots[assignedSlot - 1] : '';
    if (!action) showNotice(`A magia do espaço ${assignedSlot - 1} ainda não está equipada.`, 'info');
    else attackWith(action);
  });
  canvas.addEventListener('contextmenu', (event) => event.preventDefault());
  canvas.addEventListener('dragstart', (event) => event.preventDefault());
  document.querySelector('.game-shell').addEventListener('selectstart', (event) => event.preventDefault());
  window.addEventListener('mouseup', (event) => heldMouseButtons.delete(event.button));

  const gameShell = document.querySelector('.game-shell');
  gameShell.addEventListener('wheel', (event) => {
    if (event.target.closest('dialog, .card-draft-backdrop')) return;
    event.preventDefault();
    const bounds = cameraZoomBounds();
    targetCameraZoom = clamp(targetCameraZoom + (event.deltaY < 0 ? CAMERA_CONFIG.wheelStep : -CAMERA_CONFIG.wheelStep), bounds.min, bounds.max);
  }, { passive: false });

  function resize() {
    pixelRatio = Math.min(window.devicePixelRatio || 1, 2);
    width = window.innerWidth;
    height = window.innerHeight;
    canvas.width = Math.round(width * pixelRatio);
    canvas.height = Math.round(height * pixelRatio);
    ctx.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);
    const bounds = cameraZoomBounds();
    targetCameraZoom = clamp(targetCameraZoom, bounds.min, bounds.max);
    cameraZoom = clamp(cameraZoom, bounds.min, bounds.max);
  }
  function clamp(value, minimum, maximum) { return Math.max(minimum, Math.min(maximum, value)); }

  function terminalVilarCollides(x, y, radius) {
    if (!isTerminalVilarPhase) return false;
    const hitsRectangle = terminalVilarColliders.some((collider) => {
      const cosine = Math.cos(collider.angle);
      const sine = Math.sin(collider.angle);
      const offsetX = x - collider.x;
      const offsetY = y - collider.y;
      const localX = offsetX * cosine + offsetY * sine;
      const localY = -offsetX * sine + offsetY * cosine;
      const nearestX = clamp(localX, -collider.width / 2, collider.width / 2);
      const nearestY = clamp(localY, -collider.height / 2, collider.height / 2);
      return (localX - nearestX) ** 2 + (localY - nearestY) ** 2 <= radius ** 2;
    });
    if (hitsRectangle) return true;

    const distanceToSegmentSquared = (ax, ay, bx, by) => {
      const dx = bx - ax;
      const dy = by - ay;
      const lengthSquared = dx * dx + dy * dy;
      const amount = lengthSquared
        ? clamp(((x - ax) * dx + (y - ay) * dy) / lengthSquared, 0, 1)
        : 0;
      return (x - (ax + amount * dx)) ** 2 + (y - (ay + amount * dy)) ** 2;
    };
    const hitsPolygon = (points) => {
      let inside = false;
      for (let index = 0, previousIndex = points.length - 1;
        index < points.length; previousIndex = index, index += 1) {
        const point = points[index];
        const previous = points[previousIndex];
        if (((point[1] > y) !== (previous[1] > y))
          && x < (previous[0] - point[0]) * (y - point[1])
            / (previous[1] - point[1]) + point[0]) {
          inside = !inside;
        }
      }
      if (inside) return true;
      return points.some((point, index) => {
        const next = points[(index + 1) % points.length];
        return distanceToSegmentSquared(point[0], point[1], next[0], next[1]) <= radius ** 2;
      });
    };
    if (terminalVilarSolidPolygons.some(({ points }) => hitsPolygon(points))) return true;

    const wallRadius = radius + terminalVilarMapConfig.wall_thickness;
    const wallRadiusSquared = wallRadius ** 2;
    return terminalVilarCollisionWalls.some(({ points }) => points.slice(1).some((point, index) => (
      distanceToSegmentSquared(
        points[index][0], points[index][1], point[0], point[1],
      ) <= wallRadiusSquared
    )));
  }

  function cameraZoomBounds() {
    // Never zoom out far enough to expose empty space beyond any map edge.
    const fitZoom = Math.max(width / world.width, height / (world.height * cameraTiltY));
    return { min: Math.max(CAMERA_CONFIG.minZoom, fitZoom), max: Math.max(CAMERA_CONFIG.maxZoom, fitZoom) };
  }

  function updateCamera(delta) {
    const bounds = cameraZoomBounds();
    targetCameraZoom = clamp(targetCameraZoom, bounds.min, bounds.max);
    const easing = 1 - Math.exp(-CAMERA_CONFIG.zoomSmoothing * delta);
    cameraZoom += (targetCameraZoom - cameraZoom) * easing;
    const viewWidth = width / cameraZoom;
    const viewHeight = height / (cameraZoom * cameraTiltY);
    return {
      x: clamp(player.x - viewWidth / 2, 0, Math.max(0, world.width - viewWidth)),
      y: clamp(player.y - viewHeight / 2, 0, Math.max(0, world.height - viewHeight)),
      viewWidth,
      viewHeight,
      zoom: cameraZoom,
      tiltY: cameraTiltY,
    };
  }

  function screenToWorld(screenX, screenY, camera = currentCamera) {
    return { x: screenX / camera.zoom + camera.x, y: screenY / (camera.zoom * camera.tiltY) + camera.y };
  }

  function worldToScreen(worldX, worldY, camera = currentCamera) {
    return { x: (worldX - camera.x) * camera.zoom, y: (worldY - camera.y) * camera.zoom * camera.tiltY };
  }

  const optionsDialog = document.querySelector('#game-options-dialog');
  const optionsFeedback = document.querySelector('#game-options-feedback');
  function setOptionsFeedback(message, isError = false) {
    if (!optionsFeedback) return;
    optionsFeedback.textContent = message;
    optionsFeedback.hidden = !message;
    optionsFeedback.classList.toggle('is-error', isError);
  }
  function applyControlOptions(options) {
    keys.clear();
    heldMouseButtons.clear();
    controlScheme = options.scheme;
    skillSlots = ['basic', ...options.skill_slots.slice(1)];
    mouseLeftSlot = Number(options.mouse_left_slot);
    mouseRightSlot = Number(options.mouse_right_slot);
    orbData.dataset.controlScheme = controlScheme;
    orbData.dataset.skillSlots = JSON.stringify(skillSlots);
    orbData.dataset.mouseLeftSlot = String(mouseLeftSlot);
    orbData.dataset.mouseRightSlot = String(mouseRightSlot);
    const schemeInput = document.querySelector('#control-scheme-setting');
    if (schemeInput) schemeInput.value = controlScheme;
    document.querySelectorAll('[data-skill-slot-setting]').forEach((select) => {
      if (!select.disabled) select.value = skillSlots[Number(select.dataset.skillSlotSetting) - 1] || '';
    });
    document.querySelector('[data-mouse-slot-setting="left"]').value = String(mouseLeftSlot);
    document.querySelector('[data-mouse-slot-setting="right"]').value = String(mouseRightSlot);
    const hint = document.querySelector('.controls-hint');
    if (hint) hint.textContent = controlScheme === 'keyboard_only' ? 'Alvo na direção do movimento' : 'Mouse aponta a direção';
    updateHotkeyLabels();
  }

  function updateHotkeyLabels() {
    document.querySelectorAll('.skill-slot[data-skill]').forEach((button) => {
      const action = button.dataset.skill;
      if (action === 'dash') return;
      const numbers = action === 'basic' ? ['1'] : skillSlots
        .map((slot, index) => slot === action && index > 0 ? String(index + 1) : '')
        .filter(Boolean);
      const mouseLabels = [];
      if (controlScheme === 'mouse_keyboard') {
        if (mouseLeftSlot >= 2 && skillSlots[mouseLeftSlot - 1] === action) mouseLabels.push('ESQ.');
        if (mouseRightSlot >= 2 && skillSlots[mouseRightSlot - 1] === action) mouseLabels.push('DIR.');
      }
      const keyNode = button.querySelector('kbd');
      if (keyNode) keyNode.textContent = [...numbers, ...mouseLabels].join(' · ') || 'SEM ATALHO';
    });
  }

  document.querySelector('#open-game-options')?.addEventListener('click', () => {
    keys.clear();
    heldMouseButtons.clear();
    setOptionsFeedback('');
    optionsDialog?.showModal();
  });
  document.querySelector('#close-game-options')?.addEventListener('click', () => optionsDialog?.close());
  optionsDialog?.addEventListener('click', (event) => {
    if (event.target === optionsDialog) optionsDialog.close();
  });
  document.querySelector('#save-game-options')?.addEventListener('click', (event) => {
    const button = event.currentTarget;
    if (!socket?.connected) { setOptionsFeedback('Conecte-se ao jogo para salvar as opções.', true); return; }
    const settings = {
      scheme: document.querySelector('#control-scheme-setting').value,
      skill_slots: [...document.querySelectorAll('[data-skill-slot-setting]')]
        .map((select) => select.value),
      mouse_left_slot: Number(document.querySelector('[data-mouse-slot-setting="left"]').value),
      mouse_right_slot: Number(document.querySelector('[data-mouse-slot-setting="right"]').value),
      csrf_token: orbData.dataset.csrfToken,
    };
    button.disabled = true;
    socket.emit('options:update_controls', settings, (result) => {
      button.disabled = false;
      if (!result?.ok) { setOptionsFeedback(result?.error || 'Não foi possível salvar as opções.', true); return; }
      applyControlOptions(result);
      setOptionsFeedback('');
      optionsDialog.close();
      showNotice('Opções salvas na sua conta.');
    });
  });
  socket?.on('options:controls_updated', applyControlOptions);
  applyControlOptions({
    scheme: controlScheme,
    skill_slots: skillSlots,
    mouse_left_slot: mouseLeftSlot,
    mouse_right_slot: mouseRightSlot,
  });

  function roundedRect(x, y, w, h, r) {
    ctx.beginPath();
    ctx.roundRect(x, y, w, h, r);
  }

  function drawFloor(cameraX, cameraY, viewWidth, viewHeight) {
    if (isTerminalVilarPhase) {
      if (terminalVilarArtworkLoaded) {
        const sourceX = cameraX / world.width * terminalVilarArtwork.naturalWidth;
        const sourceY = cameraY / world.height * terminalVilarArtwork.naturalHeight;
        const sourceWidth = viewWidth / world.width * terminalVilarArtwork.naturalWidth;
        const sourceHeight = viewHeight / world.height * terminalVilarArtwork.naturalHeight;
        ctx.drawImage(
          terminalVilarArtwork,
          sourceX,
          sourceY,
          sourceWidth,
          sourceHeight,
          0,
          0,
          viewWidth,
          viewHeight,
        );
        return;
      }
      drawTerminalVilarFloor(cameraX, cameraY, viewWidth, viewHeight);
      return;
    }

    const tile = 96;
    const theme = mapThemes[mapIndex];
    const startX = Math.floor(cameraX / tile) * tile;
    const startY = Math.floor(cameraY / tile) * tile;
    for (let y = startY; y < cameraY + viewHeight + tile; y += tile) {
      for (let x = startX; x < cameraX + viewWidth + tile; x += tile) {
        const sx = x - cameraX;
        const sy = y - cameraY;
        const variation = (Math.floor(x / tile) * 17 + Math.floor(y / tile) * 31) % 4;
        ctx.fillStyle = theme.floor[variation];
        ctx.fillRect(sx, sy, tile - 2, tile - 2);
        ctx.strokeStyle = theme.grout + '22';
        ctx.lineWidth = 1;
        ctx.strokeRect(sx + .5, sy + .5, tile - 2, tile - 2);
        if ((Math.floor(x / tile) * 7 + Math.floor(y / tile) * 13) % 9 === 0) {
          ctx.fillStyle = 'rgba(189, 168, 124, .12)';
          ctx.fillRect(sx + 20 + variation * 7, sy + 27, 2, 2);
          ctx.fillRect(sx + 58, sy + 69 - variation * 5, 1, 1);
        }
      }
    }
  }

  function terminalVilarNoise(seed) {
    const value = Math.sin(seed * 9999.91) * 10000;
    return value - Math.floor(value);
  }

  function terminalVilarPoint(x, y, cameraX, cameraY) {
    return { x: x - cameraX, y: y - cameraY };
  }

  function drawTerminalVilarFloor(cameraX, cameraY, viewWidth, viewHeight) {
    const { tileSize, tileFill, borderOffset } = TERMINAL_VILAR_MAP.geometry;
    ctx.fillStyle = TERMINAL_VILAR_MAP.palette.asphalt;
    ctx.fillRect(-cameraX, -cameraY, world.width, world.height);

    const startX = Math.floor(cameraX / tileSize) * tileSize;
    const startY = Math.floor(cameraY / tileSize) * tileSize;
    for (let y = startY; y < cameraY + viewHeight + tileSize; y += tileSize) {
      for (let x = startX; x < cameraX + viewWidth + tileSize; x += tileSize) {
        const row = Math.floor(y / tileSize);
        const column = Math.floor(x / tileSize);
        const shade = Math.floor(terminalVilarNoise(row * 131 + column * 17) * 4);
        ctx.fillStyle = TERMINAL_VILAR_MAP.palette.tiles[shade];
        ctx.fillRect(x - cameraX + 1, y - cameraY + 1, tileFill, tileFill);
      }
    }

    ctx.save();
    ctx.strokeStyle = 'rgba(183, 169, 130, .25)';
    ctx.lineWidth = 4;
    ctx.setLineDash([28, 22]);
    [440, 1960].forEach((x) => {
      ctx.beginPath();
      ctx.moveTo(x - cameraX, 180 - cameraY);
      ctx.lineTo(x - cameraX, 1620 - cameraY);
      ctx.stroke();
    });
    ctx.setLineDash([24, 18]);
    ctx.strokeStyle = 'rgba(183, 169, 130, .32)';
    ctx.lineWidth = 6;
    ctx.strokeRect(
      borderOffset - cameraX,
      borderOffset - cameraY,
      world.width - borderOffset * 2,
      world.height - borderOffset * 2,
    );
    ctx.restore();

    ctx.save();
    ctx.strokeStyle = '#0e1013';
    ctx.lineWidth = 2.5;
    for (let index = 0; index < 42; index += 1) {
      let x = terminalVilarNoise(index * 19) * 2200 + 100;
      let y = terminalVilarNoise(index * 43) * 1600 + 100;
      if (Math.hypot(x - 1200, y - 900) < 240) continue;
      ctx.beginPath();
      ctx.moveTo(x - cameraX, y - cameraY);
      for (let segment = 0; segment < 5; segment += 1) {
        x += (terminalVilarNoise(index * 10 + segment) - 0.5) * 75;
        y += (terminalVilarNoise(index * 20 + segment) - 0.5) * 75;
        ctx.lineTo(x - cameraX, y - cameraY);
      }
      ctx.stroke();
    }

    for (let index = 0; index < 85; index += 1) {
      const x = terminalVilarNoise(index * 71) * 2300 + 50;
      const y = terminalVilarNoise(index * 89) * 1700 + 50;
      if (Math.hypot(x - 1200, y - 900) < 320) continue;
      ctx.fillStyle = ['#4b5563', '#9ca3af', '#78350f'][index % 3];
      ctx.fillRect(x - cameraX, y - cameraY, 10 + (index % 12), 6 + (index % 8));
    }
    ctx.restore();

    TERMINAL_VILAR_MAP.puddles.forEach((puddle) => {
      const point = terminalVilarPoint(puddle.x, puddle.y, cameraX, cameraY);
      ctx.save();
      ctx.fillStyle = '#111318';
      ctx.beginPath();
      ctx.ellipse(point.x, point.y, puddle.rx + 4, puddle.ry + 4, 0, 0, Math.PI * 2);
      ctx.fill();

      const gradient = ctx.createRadialGradient(point.x, point.y, 5, point.x, point.y, puddle.rx);
      if (puddle.neon) {
        gradient.addColorStop(0, 'rgba(192, 38, 211, .55)');
        gradient.addColorStop(.55, 'rgba(88, 28, 135, .45)');
        gradient.addColorStop(1, '#181524');
      } else {
        gradient.addColorStop(0, '#2b303a');
        gradient.addColorStop(1, '#171920');
      }
      ctx.fillStyle = gradient;
      ctx.beginPath();
      ctx.ellipse(point.x, point.y, puddle.rx, puddle.ry, 0, 0, Math.PI * 2);
      ctx.fill();
      if (puddle.neon) {
        ctx.strokeStyle = 'rgba(232, 121, 249, .4)';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.ellipse(point.x - puddle.rx * .2, point.y, puddle.rx * .45, puddle.ry * .35, 0, .2, 2.4);
        ctx.stroke();
      }
      ctx.restore();
    });
  }

  function drawCentralPlatform(cameraX, cameraY) {
    const platform = TERMINAL_VILAR_MAP.geometry.platform;
    const x = platform.x - cameraX;
    const y = platform.y - cameraY;
    ctx.save();
    ctx.fillStyle = '#14161b';
    ctx.fillRect(x - 6, y + 8, platform.width + 12, platform.height + 10);
    ctx.fillStyle = '#2b2f37';
    ctx.fillRect(x, y, platform.width, platform.height);

    ctx.strokeStyle = '#383d47';
    ctx.lineWidth = 2;
    for (let gridX = platform.x + 65; gridX < platform.x + platform.width; gridX += 65) {
      ctx.beginPath();
      ctx.moveTo(gridX - cameraX, y);
      ctx.lineTo(gridX - cameraX, platform.y + platform.height - cameraY);
      ctx.stroke();
    }
    for (let gridY = platform.y + 65; gridY < platform.y + platform.height; gridY += 65) {
      ctx.beginPath();
      ctx.moveTo(x, gridY - cameraY);
      ctx.lineTo(platform.x + platform.width - cameraX, gridY - cameraY);
      ctx.stroke();
    }
    ctx.strokeStyle = '#525866';
    ctx.lineWidth = 5;
    ctx.strokeRect(x, y, platform.width, platform.height);

    const glow = ctx.createRadialGradient(1200 - cameraX, 720 - cameraY, 20, 1200 - cameraX, 720 - cameraY, 460);
    glow.addColorStop(0, 'rgba(192, 38, 211, .22)');
    glow.addColorStop(1, 'rgba(192, 38, 211, 0)');
    ctx.fillStyle = glow;
    ctx.fillRect(x, y, platform.width, platform.height);
    ctx.restore();
  }

  function drawTerminalVilarLabel(text, x, y, cameraX, cameraY, font, color) {
    ctx.save();
    ctx.translate(x - cameraX, y - cameraY);
    ctx.scale(1, 1 / cameraTiltY);
    ctx.font = font;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillStyle = color;
    ctx.fillText(text, 0, 0);
    ctx.restore();
  }

  function drawTerminalVilarLandmarks(cameraX, cameraY) {
    const palette = TERMINAL_VILAR_MAP.palette;
    const canopy = TERMINAL_VILAR_MAP.geometry.canopy;
    const canopyX = canopy.x - cameraX;
    const canopyY = canopy.y - cameraY;
    const canopyHeight = 115;

    ctx.save();
    ctx.fillStyle = '#12131a';
    [
      [0, 20, 260, 100], [270, 45, 220, 80], [500, 60, 190, 65],
      [1720, 45, 210, 80], [1940, 25, 240, 100], [2190, 10, 210, 115],
    ].forEach(([x, y, width, height]) => {
      ctx.fillRect(x - cameraX, y - cameraY, width, height);
    });

    ctx.strokeStyle = '#2e323b';
    ctx.lineWidth = 3;
    ctx.beginPath();
    ctx.moveTo(-cameraX, 128 - cameraY);
    ctx.lineTo(world.width - cameraX, 128 - cameraY);
    ctx.stroke();
    TERMINAL_VILAR_MAP.rifts.forEach((rift, index) => {
      const x = rift.x - cameraX;
      const y = rift.y - cameraY;
      ctx.save();
      ctx.shadowColor = palette.neon;
      ctx.shadowBlur = 28;
      ctx.fillStyle = 'rgba(46, 8, 68, .68)';
      ctx.strokeStyle = palette.neonBright;
      ctx.lineWidth = 3;
      ctx.beginPath();
      for (let point = 0; point <= 18; point += 1) {
        const angle = point / 18 * Math.PI * 2;
        const jitter = .75 + terminalVilarNoise(index * 100 + point) * .45;
        const px = x + Math.cos(angle) * rift.rx * jitter;
        const py = y + Math.sin(angle) * rift.ry * jitter;
        if (point === 0) ctx.moveTo(px, py);
        else ctx.lineTo(px, py);
      }
      ctx.closePath();
      ctx.fill();
      ctx.stroke();
      ctx.restore();
    });
    ctx.restore();

    ctx.save();
    ctx.fillStyle = '#1c1e24';
    ctx.fillRect(canopyX + 20, canopyY - canopyHeight + 20, canopy.width - 40, canopyHeight + canopy.depth - 20);
    ctx.fillStyle = '#374151';
    [canopy.x + 230, canopy.x + 470, canopy.x + 720].forEach((x) => {
      ctx.fillRect(x - cameraX, canopy.y + 145 - cameraY - 22, 110, 18);
    });
    ctx.fillStyle = '#2d313a';
    ctx.strokeStyle = '#111317';
    ctx.lineWidth = 3;
    ctx.fillRect(canopyX, canopyY - canopyHeight, canopy.width, canopy.depth);
    ctx.strokeRect(canopyX, canopyY - canopyHeight, canopy.width, canopy.depth);
    ctx.fillStyle = '#1a0b24';
    ctx.fillRect(canopyX + 18, canopyY - canopyHeight + canopy.depth - 24, canopy.width - 36, 44);
    ctx.shadowColor = palette.neon;
    ctx.shadowBlur = 22;
    ctx.strokeStyle = palette.neonBright;
    ctx.lineWidth = 2.5;
    ctx.strokeRect(canopyX + 18, canopyY - canopyHeight + canopy.depth - 24, canopy.width - 36, 44);
    ctx.restore();
    drawTerminalVilarLabel(
      'TERMINAL DE VILAR - SETOR 01',
      canopy.x + canopy.width / 2,
      canopy.y - canopyHeight + canopy.depth - 2,
      cameraX,
      cameraY,
      'bold 22px Segoe UI, sans-serif',
      '#f5d0fe',
    );

    TERMINAL_VILAR_MAP.pillars.forEach((pillar) => {
      const x = pillar.x - cameraX;
      const y = pillar.y - cameraY;
      const width = pillar.width;
      const depth = pillar.height;
      ctx.save();
      ctx.fillStyle = 'rgba(0, 0, 0, .45)';
      ctx.beginPath();
      ctx.ellipse(x + 12, y + 8, width * .75, depth * .65, .2, 0, Math.PI * 2);
      ctx.fill();
      ctx.fillStyle = palette.concrete;
      ctx.strokeStyle = '#181a20';
      ctx.lineWidth = 2.5;
      ctx.fillRect(x - width / 2, y - depth / 2 - pillar.visualHeight, width, depth + pillar.visualHeight);
      ctx.strokeRect(x - width / 2, y - depth / 2 - pillar.visualHeight, width, depth + pillar.visualHeight);
      ctx.fillStyle = '#4b515c';
      ctx.fillRect(x - width / 2, y - depth / 2 - pillar.visualHeight, width, depth);
      pillar.posters.forEach((color, index) => {
        ctx.fillStyle = color;
        ctx.globalAlpha = .85;
        ctx.fillRect(x - width / 2 + 8 + index * 16, y - depth / 2 + 18 + index * 24, 16, 22);
      });
      ctx.restore();
    });

    TERMINAL_VILAR_MAP.buses.forEach((bus) => {
      const x = bus.x - cameraX;
      const y = bus.y - cameraY;
      const bodyHeight = bus.height + 68;
      ctx.save();
      ctx.translate(x, y);
      ctx.rotate(bus.angle);
      ctx.fillStyle = 'rgba(0, 0, 0, .65)';
      ctx.fillRect(-bus.width / 2 + 10, -bodyHeight / 2 + 12, bus.width, bodyHeight);
      ctx.fillStyle = '#3f3d38';
      ctx.strokeStyle = '#141519';
      ctx.lineWidth = 3;
      ctx.fillRect(-bus.width / 2, -bus.height / 2 - 68, bus.width, bodyHeight);
      ctx.strokeRect(-bus.width / 2, -bus.height / 2 - 68, bus.width, bodyHeight);
      ctx.fillStyle = '#57534e';
      ctx.fillRect(-bus.width / 2 + 4, -bus.height / 2 - 64, bus.width - 8, bodyHeight - 76);

      const isLong = bus.width > bus.height;
      const count = 5;
      if (isLong) {
        ctx.fillStyle = '#292524';
        ctx.fillRect(-bus.width / 2, bus.height / 2 - 68, bus.width, 68);
        ctx.fillStyle = '#854d0e';
        ctx.fillRect(-bus.width / 2 + 6, bus.height / 2 - 30, bus.width - 12, 10);
      }
      for (let index = 0; index < count; index += 1) {
        const distance = isLong
          ? -bus.width / 2 + 30 + index * ((bus.width - 60) / count)
          : -bus.height / 2 + 20 + index * ((bus.height - 40) / count);
        const windowX = isLong ? distance : -bus.width / 2 + 18;
        const windowY = isLong ? bus.height / 2 - 60 : distance - 68;
        const windowWidth = isLong ? 42 : Math.max(28, bus.width - 36);
        const windowHeight = isLong ? 24 : 34;
        ctx.fillStyle = '#0f172a';
        ctx.fillRect(windowX, windowY, windowWidth, windowHeight);
        if (index < bus.silhouettes) {
          ctx.fillStyle = '#050507';
          ctx.beginPath();
          ctx.arc(windowX + windowWidth / 2, windowY + 12, 7, 0, Math.PI * 2);
          ctx.fill();
          ctx.fillRect(windowX + windowWidth * .3, windowY + 16, windowWidth * .4, 8);
          ctx.fillStyle = palette.neonBright;
          ctx.fillRect(windowX + windowWidth * .43, windowY + 10, 2.5, 2.5);
          ctx.fillRect(windowX + windowWidth * .53, windowY + 10, 2.5, 2.5);
        }
      }
      ctx.restore();
      if (isLong) {
        drawTerminalVilarLabel(
          'VIAÇÃO RODA-PRESA',
          bus.x,
          bus.y + bus.height / 2 - 5,
          cameraX,
          cameraY,
          'bold 9px Segoe UI, sans-serif',
          '#d6d3d1',
        );
      }
    });

    TERMINAL_VILAR_MAP.streetlights.forEach((light) => {
      const x = light.x - cameraX;
      const y = light.y - cameraY;
      const glowX = x + 25;
      const glowY = y + 40;
      ctx.save();
      const gradient = ctx.createRadialGradient(glowX, glowY, 10, glowX, glowY, 210);
      gradient.addColorStop(0, `rgba(251, 191, 36, ${.24 * light.flicker})`);
      gradient.addColorStop(1, 'rgba(251, 191, 36, 0)');
      ctx.fillStyle = gradient;
      ctx.beginPath();
      ctx.ellipse(glowX, glowY, 210, 180, 0, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = '#4b5563';
      ctx.lineWidth = 6;
      ctx.beginPath();
      ctx.moveTo(x, y);
      ctx.lineTo(x, y - 135);
      ctx.lineTo(x + 28, y - 143);
      ctx.stroke();
      ctx.fillStyle = '#fef08a';
      ctx.shadowColor = '#f59e0b';
      ctx.shadowBlur = 15;
      ctx.beginPath();
      ctx.arc(x + 30, y - 141, 6, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    });
  }

  function drawMapLandmarks(cameraX, cameraY) {
    if (isTerminalVilarPhase) {
      if (!terminalVilarArtworkLoaded) {
        drawTerminalVilarLandmarks(cameraX, cameraY);
      }
      return;
    }

    const theme = mapThemes[mapIndex];
    ctx.save();
    ctx.strokeStyle = theme.accent + '28';
    ctx.fillStyle = theme.accent + '12';
    ctx.lineWidth = 5;
    if (mapIndex === 0) {
      for (let x = 340; x < world.width - 300; x += 310) {
        ctx.strokeRect(x - cameraX, 300 - cameraY, 170, 95);
        ctx.fillRect(x - cameraX + 16, 316 - cameraY, 138, 12);
      }
    } else if (mapIndex === 1) {
      [690, 745, 1300, 1355].forEach((y) => {
        ctx.beginPath();
        ctx.moveTo(130 - cameraX, y - cameraY);
        ctx.lineTo(world.width - 130 - cameraX, y - cameraY);
        ctx.stroke();
      });
    } else if (mapIndex === 2 || mapIndex === 4) {
      for (let x = 420; x < world.width - 400; x += 260) {
        ctx.strokeRect(x - cameraX, 390 - cameraY, 160, 115);
        ctx.strokeRect(x - cameraX, 1295 - cameraY, 160, 115);
      }
    } else if (mapIndex === 3) {
      ctx.lineWidth = 34;
      ctx.beginPath();
      ctx.moveTo(120 - cameraX, 1350 - cameraY);
      ctx.bezierCurveTo(700 - cameraX, 1130 - cameraY, 1490 - cameraX, 1650 - cameraY, 2280 - cameraX, 1230 - cameraY);
      ctx.stroke();
    } else if (mapIndex === 5) {
      for (let row = 0; row < 5; row += 1) {
        for (let column = 0; column < 8; column += 1) {
          const x = 430 + column * 210 - cameraX;
          const y = 410 + row * 230 - cameraY;
          ctx.fillRect(x, y, 42, 30);
          ctx.strokeRect(x, y, 42, 30);
        }
      }
    } else if (mapIndex === 6) {
      [430, 1380].forEach((x) => {
        ctx.beginPath();
        ctx.arc(x - cameraX, 900 - cameraY, 145, 0, Math.PI * 2);
        ctx.stroke();
        ctx.beginPath();
        ctx.arc(x - cameraX, 900 - cameraY, 115, 0, Math.PI * 2);
        ctx.stroke();
      });
      ctx.strokeRect(730 - cameraX, 480 - cameraY, 950, 18);
      ctx.strokeRect(730 - cameraX, 1300 - cameraY, 950, 18);
    } else if (mapIndex === 7) {
      for (let x = 360; x <= 2040; x += 420) {
        ctx.beginPath();
        ctx.moveTo(x - cameraX, 260 - cameraY);
        ctx.lineTo(x - cameraX, 1540 - cameraY);
        ctx.stroke();
        ctx.beginPath();
        ctx.arc(x - cameraX, 900 - cameraY, 34, 0, Math.PI * 2);
        ctx.fill();
      }
    } else {
      for (let row = 0; row < 6; row += 1) {
        const y = 330 + row * 220 - cameraY;
        ctx.beginPath();
        ctx.moveTo(270 - cameraX, y);
        ctx.lineTo(world.width - 270 - cameraX, y);
        ctx.stroke();
      }
    }
    ctx.restore();
  }

  function drawRuins(cameraX, cameraY) {
    if (isTerminalVilarPhase) return;

    const theme = mapThemes[mapIndex];
    const pillars = [
      [world.width / 2 - 370, world.height / 2 - 220], [world.width / 2 + 390, world.height / 2 - 280],
      [world.width / 2 - 420, world.height / 2 + 280], [world.width / 2 + 450, world.height / 2 + 240],
      [world.width / 2 - 90, world.height / 2 - 430], [world.width / 2 + 160, world.height / 2 + 420]
    ];
    for (const [x, y] of pillars) {
      const sx = x - cameraX;
      const sy = y - cameraY;
      ctx.fillStyle = 'rgba(0, 0, 0, .32)';
      roundedRect(sx - 18, sy - 10, 52, 45, 6); ctx.fill();
      ctx.fillStyle = theme.floor[1];
      roundedRect(sx - 24, sy - 20, 48, 42, 5); ctx.fill();
      ctx.strokeStyle = theme.edge + '55'; ctx.lineWidth = 1; ctx.stroke();
      ctx.fillStyle = theme.accent + '33';
      ctx.fillRect(sx - 18, sy - 15, 36, 2);
    }

    // Ruined perimeter walls define a readable test room without external art.
    const margin = 110;
    ctx.strokeStyle = theme.edge + '88';
    ctx.lineWidth = 12;
    ctx.setLineDash([68, 18]);
    ctx.strokeRect(margin - cameraX, margin - cameraY, world.width - margin * 2, world.height - margin * 2);
    ctx.setLineDash([]);
    ctx.strokeStyle = theme.edge + '30';
    ctx.lineWidth = 1;
    ctx.strokeRect(margin - cameraX + 9, margin - cameraY + 9, world.width - margin * 2 - 18, world.height - margin * 2 - 18);
  }

  function drawBaseRange(cameraX, cameraY, time) {
    const screenX = player.x - cameraX;
    const screenY = player.y - cameraY;
    const pulse = 0.5 + Math.sin(time * 0.0014) * 0.5;
    ctx.save();
    ctx.beginPath();
    ctx.arc(screenX, screenY, baseAttackRange * attackRangeMultiplier, 0, Math.PI * 2);
    ctx.fillStyle = `rgba(213, 177, 106, ${0.009 + pulse * 0.008})`;
    ctx.fill();
    ctx.shadowColor = 'rgba(226, 192, 125, .24)';
    ctx.shadowBlur = 7 + pulse * 4;
    ctx.strokeStyle = `rgba(226, 192, 125, ${0.15 + pulse * 0.06})`;
    ctx.lineWidth = 1.2;
    ctx.stroke();
    ctx.beginPath();
    ctx.arc(screenX, screenY, skillAttackRange * attackRangeMultiplier, 0, Math.PI * 2);
    ctx.shadowColor = 'rgba(113, 181, 232, .25)';
    ctx.shadowBlur = 7 + pulse * 4;
    ctx.strokeStyle = `rgba(113, 181, 232, ${0.12 + pulse * 0.06})`;
    ctx.setLineDash([5, 7]);
    ctx.stroke();
    ctx.setLineDash([]);
    ctx.restore();
  }

  function isGamePaused() {
    // Só as decisões de morte/fim de fase pausam o mundo; escolher cartas não pausa.
    const phaseOverlay = document.querySelector('#phase-choice-overlay');
    const deathOverlay = document.querySelector('#death-overlay');
    const campaignOverlay = document.querySelector('#campaign-complete-overlay');
    return Boolean((phaseOverlay && !phaseOverlay.hidden) || (deathOverlay && !deathOverlay.hidden)
      || (campaignOverlay && !campaignOverlay.hidden) || optionsDialog?.open);
  }

  function enterPhaseIntermission() {
    keys.clear();
    heldMouseButtons.clear();
    stopCardAutoPick();
    pendingCardChoices = 0;
    clearCardDialog();
    syncCardDraftToggle();
    document.querySelector('#phase-choice-overlay').hidden = false;
    const activeCards = document.querySelector('.active-card-list');
    if (activeCards) activeCards.replaceChildren();
    const emptyCards = document.querySelector('.no-active-cards');
    if (emptyCards) emptyCards.textContent = 'A nova coleção será escolhida ao iniciar a próxima fase.';
  }

  function drawPlayer(screenX, screenY, time) {
    const pulse = 0.5 + Math.sin(time * 0.003) * 0.08;
    const glow = ctx.createRadialGradient(screenX, screenY + 3, 3, screenX, screenY + 3, 46);
    glow.addColorStop(0, 'rgba(213, 177, 106, .24)');
    glow.addColorStop(1, 'rgba(213, 177, 106, 0)');
    ctx.fillStyle = glow; ctx.beginPath(); ctx.arc(screenX, screenY, 46, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = 'rgba(0, 0, 0, .52)';
    ctx.beginPath(); ctx.ellipse(screenX, screenY + 11, 16, 8, 0, 0, Math.PI * 2); ctx.fill();

    ctx.save();
    ctx.translate(screenX, screenY);
    // O piso é comprimido pela câmera, mas o personagem permanece em pé e legível.
    ctx.scale(1, 1 / cameraTiltY);
    const visualAimAngle = Math.atan2(
      Math.sin(aimAngle) * cameraTiltY,
      Math.cos(aimAngle),
    );
    // O desenho base olha para cima; a rotação acompanha a direção projetada.
    ctx.rotate(visualAimAngle + Math.PI / 2);
    ctx.fillStyle = '#393a3a';
    ctx.beginPath(); ctx.ellipse(0, 3, 11, 13, 0, 0, Math.PI * 2); ctx.fill();
    ctx.strokeStyle = `rgba(224, 190, 120, ${pulse})`; ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.ellipse(0, 3, 11, 13, 0, 0, Math.PI * 2); ctx.stroke();
    ctx.fillStyle = '#d8c49b';
    ctx.beginPath(); ctx.arc(0, -8, 6, 0, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#272a2d';
    ctx.beginPath(); ctx.arc(0, -10, 6, Math.PI, Math.PI * 2); ctx.fill();
    ctx.fillStyle = '#f0d895';
    ctx.beginPath(); ctx.arc(2, -8, 1.3, 0, Math.PI * 2); ctx.fill();
    ctx.restore();
  }

  function drawEnemy(cameraX, cameraY) {
    if (isPhasePreparing()) return;
    for (const enemy of enemies) {
      if (!enemy.alive) continue;
      const x = enemy.world_x - cameraX, y = enemy.world_y - cameraY;
      const barWidth = enemy.is_boss ? 64 : enemy.is_miniboss ? 56 : 40;
      const barY = -enemy.radius - 10;
      const bossLike = enemy.is_boss || enemy.is_miniboss;
      if (enemy === targetedEnemy) {
        ctx.strokeStyle = 'rgba(239, 211, 151, .9)'; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.arc(x, y, enemy.radius + 7, 0, Math.PI * 2); ctx.stroke();
      }
      if (enemy.immobilizedUntil > performance.now()) {
        ctx.strokeStyle = 'rgba(180, 160, 240, .95)';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.arc(x, y, enemy.radius + 11, 0, Math.PI * 2);
        ctx.stroke();
      }
      ctx.save();
      ctx.translate(x, y);
      ctx.scale(1, 1 / cameraTiltY);
      ctx.font = '10px DM Sans, sans-serif'; ctx.textAlign = 'center'; ctx.fillStyle = '#e6d9c3';
      ctx.fillText(enemy.name || 'Monstro da Cripta', 0, barY - 5);
      ctx.fillStyle = bossLike ? '#583d24' : enemy.attack_style === 'ranged' ? '#344b55' : '#6f302d';
      ctx.beginPath();
      if (enemy.attack_style === 'ranged' && !bossLike) {
        ctx.moveTo(0, -enemy.radius); ctx.lineTo(enemy.radius, 0); ctx.lineTo(0, enemy.radius); ctx.lineTo(-enemy.radius, 0); ctx.closePath();
      } else ctx.arc(0, 0, enemy.radius, 0, Math.PI * 2);
      ctx.fill();
      ctx.strokeStyle = enemy.is_boss ? '#e2bd71' : enemy.is_miniboss ? '#bc8461' : enemy.attack_style === 'ranged' ? '#83b6c2' : '#c16c53';
      ctx.lineWidth = bossLike ? 3 : 2; ctx.stroke();
      ctx.fillStyle = '#241b1b'; ctx.fillRect(-barWidth / 2, barY, barWidth, 5);
      ctx.fillStyle = enemy.is_boss ? '#d59c45' : enemy.is_miniboss ? '#bc7655' : '#a94d43'; ctx.fillRect(-barWidth / 2, barY, barWidth * enemy.hp / enemy.max_hp, 5);
      ctx.restore();
    }
  }

  function prepareEnemy(enemy) {
    const bossLike = enemy.is_boss || enemy.is_miniboss;
    const attackStyle = enemy.attack_style || (enemy.is_boss ? 'boss' : enemy.is_miniboss ? 'miniboss' : (enemy.enemy_index || 0) % 2 ? 'ranged' : 'melee');
    return {
      ...enemy,
      radius: enemy.is_boss ? 28 : enemy.is_miniboss ? 24 : 17,
      attack_style: attackStyle,
      attackRange: enemy.is_boss || enemy.is_miniboss ? 430 : attackStyle === 'ranged' ? 390 : 150,
      preferredRange: attackStyle === 'ranged' ? 250 : 0,
      chaseSpeed: enemy.is_boss ? 43 : enemy.is_miniboss ? 52 : attackStyle === 'ranged' ? 54 : 62 + ((enemy.enemy_index || 0) % 3) * 8,
      orbitDirection: Number(enemy.enemy_index || 0) % 2 ? 1 : -1,
      nextOrbitChangeAt: Date.now() + 2800 + (Number(enemy.enemy_index || 0) % 3) * 700,
      // attackWith only selects enemies whose attackReady flag is true.
      attackReady: true,
      attackRequestInFlight: false,
      nextAttackAt: Date.now() + 850 + ((enemy.enemy_index || 0) % 3) * 360
    };
  }

  function findTargetedEnemy(camera) {
    if (isGamePaused() || isPhasePreparing()) return null;
    if (controlScheme === 'mouse_keyboard') {
      const hovered = enemies
        .filter((enemy) => enemy.alive)
        .map((enemy) => {
          const projected = worldToScreen(enemy.world_x, enemy.world_y, camera);
          return { enemy, distance: Math.hypot(projected.x - mouse.x, projected.y - mouse.y) };
        })
        .filter((item) => item.distance <= item.enemy.radius * camera.zoom + 26)
        .sort((a, b) => a.distance - b.distance)[0]?.enemy;
      return hovered || null;
    }
    const maxTargetRange = baseAttackRange * attackRangeMultiplier;
    return enemies
      .filter((enemy) => enemy.alive)
      .map((enemy) => {
        const dx = enemy.world_x - player.x;
        const dy = enemy.world_y - player.y;
        let difference = Math.atan2(dy, dx) - aimAngle;
        difference = Math.atan2(Math.sin(difference), Math.cos(difference));
        return { enemy, distance: Math.hypot(dx, dy), difference: Math.abs(difference) };
      })
      .filter((item) => item.distance <= maxTargetRange + item.enemy.radius
        && item.difference <= (controlScheme === 'keyboard_only' ? Math.PI / 3 : .23))
      .sort((a, b) => a.distance - b.distance)[0]?.enemy || null;
  }

  function drawMonsterPortrait(enemy) {
    const portrait = document.querySelector('#target-monster-portrait');
    const portraitCtx = portrait?.getContext('2d');
    if (!portrait || !portraitCtx) return;
    const accent = enemy.affinity?.color || (enemy.is_boss ? '#d5a64e' : enemy.is_miniboss ? '#bc7655' : enemy.attack_style === 'ranged' ? '#83b6c2' : '#c16c53');
    portraitCtx.clearRect(0, 0, portrait.width, portrait.height);
    const glow = portraitCtx.createRadialGradient(48, 44, 6, 48, 48, 48);
    glow.addColorStop(0, `${accent}55`); glow.addColorStop(1, '#0b0e14');
    portraitCtx.fillStyle = glow; portraitCtx.fillRect(0, 0, 96, 96);
    portraitCtx.fillStyle = 'rgba(0,0,0,.45)';
    portraitCtx.beginPath(); portraitCtx.ellipse(48, 75, 30, 9, 0, 0, Math.PI * 2); portraitCtx.fill();
    portraitCtx.fillStyle = enemy.is_boss ? '#34302d' : enemy.attack_style === 'ranged' ? '#26363a' : '#3b2927';
    portraitCtx.beginPath();
    if (enemy.attack_style === 'ranged' && !enemy.is_boss && !enemy.is_miniboss) {
      portraitCtx.moveTo(48, 20); portraitCtx.lineTo(76, 49); portraitCtx.lineTo(48, 77); portraitCtx.lineTo(20, 49); portraitCtx.closePath();
    } else portraitCtx.ellipse(48, 51, enemy.is_boss ? 28 : 23, enemy.is_boss ? 31 : 26, 0, 0, Math.PI * 2);
    portraitCtx.fill();
    if (enemy.is_boss || enemy.is_miniboss) {
      portraitCtx.fillStyle = accent;
      portraitCtx.beginPath(); portraitCtx.moveTo(29, 34); portraitCtx.lineTo(20, 14); portraitCtx.lineTo(39, 28); portraitCtx.fill();
      portraitCtx.beginPath(); portraitCtx.moveTo(67, 34); portraitCtx.lineTo(76, 14); portraitCtx.lineTo(57, 28); portraitCtx.fill();
    }
    portraitCtx.strokeStyle = accent; portraitCtx.lineWidth = 2;
    portraitCtx.beginPath(); portraitCtx.ellipse(48, 51, enemy.is_boss ? 28 : 23, enemy.is_boss ? 31 : 26, 0, 0, Math.PI * 2); portraitCtx.stroke();
    portraitCtx.fillStyle = '#f0d895';
    portraitCtx.beginPath(); portraitCtx.ellipse(40, 47, 3, 2, 0, 0, Math.PI * 2); portraitCtx.ellipse(56, 47, 3, 2, 0, 0, Math.PI * 2); portraitCtx.fill();
  }

  function updateTargetPanel(enemy) {
    const panel = document.querySelector('#target-monster-panel');
    if (!panel) return;
    targetedEnemy = enemy;
    panel.hidden = !enemy;
    if (!enemy) return;
    const kind = enemy.is_boss ? 'CHEFE' : enemy.is_miniboss ? 'SEMICHEFE' : enemy.attack_style === 'ranged' ? 'ATAQUE À DISTÂNCIA' : 'CORPO A CORPO';
    const affinity = enemy.affinity;
    const element = affinity?.name || 'Neutro';
    const resistance = affinity
      ? `${Math.round((Number(affinity.resistance) || 0) * 100)}% a ${affinity.name}`
      : 'Nenhuma conhecida';
    const values = {
      '#target-monster-kind': kind,
      '#target-monster-name': enemy.name || 'Monstro da Cripta',
      '#target-monster-level': `Nv. ${enemy.level || 1}`,
      '#target-monster-health': `${Math.max(0, Math.round(enemy.hp || 0))} / ${Math.max(1, Math.round(enemy.max_hp || 1))}`,
      '#target-monster-element': element,
      '#target-monster-resistance': resistance,
      '#target-monster-weakness': 'Ainda não identificado'
    };
    for (const [selector, value] of Object.entries(values)) {
      const node = panel.querySelector(selector);
      if (node && node.textContent !== value) node.textContent = value;
    }
    const ratio = Math.max(0, Math.min(1, (enemy.hp || 0) / Math.max(1, enemy.max_hp || 1)));
    const fill = panel.querySelector('#target-monster-health-fill');
    const track = fill?.parentElement;
    if (fill) fill.style.width = `${ratio * 100}%`;
    if (track) track.setAttribute('aria-valuenow', String(Math.round(ratio * 100)));
    const elementNode = panel.querySelector('#target-monster-element');
    if (elementNode) elementNode.style.color = affinity?.color || '';
    if (targetPortraitEnemyId !== enemy.id) {
      drawMonsterPortrait(enemy);
      targetPortraitEnemyId = enemy.id;
    }
  }

  function registerEnemyAttack(attack) {
    if (!attack?.attack_id || enemyAttacks.some((item) => item.attack_id === attack.attack_id)) return;
    enemyAttacks.push(attack);
  }

  function releaseEnemyAttackRequest(enemy, requestId) {
    if (enemy.attackRequestId !== requestId) return false;
    window.clearTimeout(enemy.attackRequestTimeout);
    enemy.attackRequestId = null;
    enemy.attackRequestTimeout = null;
    enemy.attackRequestInFlight = false;
    return true;
  }

  function resetEnemyAttackRequests() {
    for (const enemy of enemies) {
      if (enemy.attackRequestTimeout) window.clearTimeout(enemy.attackRequestTimeout);
      enemy.attackRequestId = null;
      enemy.attackRequestTimeout = null;
      enemy.attackRequestInFlight = false;
      enemy.nextAttackAt = Date.now() + 250;
    }
    enemyAttacks.length = 0;
  }

  function requestEnemyAttack(enemy) {
    if (!socket?.connected || enemy.attackRequestInFlight || Date.now() < enemy.nextAttackAt) return;
    const requestId = Symbol();
    enemy.attackRequestId = requestId;
    enemy.attackRequestInFlight = true;
    enemy.nextAttackAt = Date.now() + 900;
    enemy.attackRequestTimeout = window.setTimeout(() => {
      if (!releaseEnemyAttackRequest(enemy, requestId)) return;
      enemy.nextAttackAt = Date.now() + 250;
    }, 5000);
    socket.emit('combat:request_enemy_attack', {
      enemy_id: enemy.id,
      enemy_x: enemy.world_x,
      enemy_y: enemy.world_y,
      target_x: player.x,
      target_y: player.y,
      csrf_token: orbData.dataset.csrfToken
    }, (response) => {
      if (!releaseEnemyAttackRequest(enemy, requestId)) return;
      if (response?.ok) {
        enemy.nextAttackAt = Date.now() + (response.cooldown_ms || 4000);
        registerEnemyAttack(response);
      } else if (response?.cooldown) {
        enemy.nextAttackAt = Date.now() + (response.retry_after_ms || 1000);
      } else if (response?.pending) {
        enemy.nextAttackAt = Date.now() + 1000;
      } else {
        enemy.nextAttackAt = Date.now() + 1300;
      }
    });
  }

  function drawEnemyTelegraphs(cameraX, cameraY, time) {
    const now = Date.now();
    for (const attack of enemyAttacks) {
      const remaining = Math.max(0, attack.impact_at - now);
      const fullDuration = Math.max(1, attack.impact_at - attack.created_at);
      const progress = Math.max(0, Math.min(1, 1 - remaining / fullDuration));
      const pulse = .5 + .5 * Math.sin(time * .018);
      for (let index = 0; index < attack.areas.length; index += 1) {
        const area = attack.areas[index];
        const x = area.x - cameraX, y = area.y - cameraY;
        ctx.save();
        ctx.fillStyle = `rgba(204, 72, 59, ${.10 + pulse * .07})`;
        ctx.strokeStyle = `rgba(240, 128, 94, ${.58 + pulse * .3})`;
        ctx.lineWidth = 2;
        ctx.beginPath(); ctx.arc(x, y, area.radius, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
        ctx.strokeStyle = 'rgba(247, 215, 178, .74)'; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.arc(x, y, area.radius * (.22 + progress * .78), -Math.PI / 2, -Math.PI / 2 + Math.PI * 2 * progress); ctx.stroke();
        ctx.strokeStyle = 'rgba(255, 223, 188, .55)'; ctx.lineWidth = 1;
        ctx.beginPath(); ctx.moveTo(x - 6, y); ctx.lineTo(x + 6, y); ctx.moveTo(x, y - 6); ctx.lineTo(x, y + 6); ctx.stroke();
        if (index === 0) {
          ctx.font = 'bold 10px DM Sans, sans-serif'; ctx.textAlign = 'center';
          ctx.fillStyle = '#ffe0bd'; ctx.shadowColor = '#250b0b'; ctx.shadowBlur = 5;
          ctx.fillText(`${attack.name} · ${(remaining / 1000).toFixed(1)}s`, x, y - area.radius - 12);
        }
        ctx.restore();
      }
    }
  }

  function drawEnemyProjectiles(cameraX, cameraY, time) {
    const now = Date.now();
    for (const attack of enemyAttacks) {
      for (const projectile of attack.projectiles || []) {
        const flight = Math.max(1, projectile.flight_ms);
        const startAt = attack.impact_at - flight;
        const progress = Math.max(0, Math.min(1, (now - startAt) / flight));
        if (progress <= 0 || progress >= 1) continue;
        const worldX = projectile.origin_x + (projectile.target_x - projectile.origin_x) * progress;
        const worldY = projectile.origin_y + (projectile.target_y - projectile.origin_y) * progress;
        const height = Math.sin(progress * Math.PI) * 92;
        const x = worldX - cameraX, y = worldY - cameraY;
        const targetX = projectile.target_x - cameraX, targetY = projectile.target_y - cameraY;
        const shadowSize = 8 + progress * 13;
        ctx.save();
        ctx.fillStyle = `rgba(3, 5, 9, ${.28 + progress * .36})`;
        ctx.beginPath(); ctx.ellipse(x, y + height * .18, shadowSize * 1.35, shadowSize * .55, 0, 0, Math.PI * 2); ctx.fill();
        ctx.globalCompositeOperation = 'lighter';
        const glow = ctx.createRadialGradient(x, y - height, 1, x, y - height, 22);
        glow.addColorStop(0, 'rgba(255, 226, 173, .95)');
        glow.addColorStop(.35, 'rgba(231, 120, 83, .74)');
        glow.addColorStop(1, 'rgba(176, 57, 53, 0)');
        ctx.fillStyle = glow; ctx.beginPath(); ctx.arc(x, y - height, 22, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#f3c17d'; ctx.beginPath(); ctx.arc(x, y - height, 5 + progress * 2, 0, Math.PI * 2); ctx.fill();
        const landingPulse = .55 + .25 * Math.sin(time * .02);
        ctx.globalCompositeOperation = 'source-over';
        ctx.fillStyle = `rgba(4, 6, 9, ${landingPulse})`;
        ctx.beginPath(); ctx.ellipse(targetX, targetY, 10 + progress * 7, 5 + progress * 4, 0, 0, Math.PI * 2); ctx.fill();
        ctx.restore();
      }
    }
  }

  function registerPlayerProjectile(attack, resolveOnImpact) {
    playerProjectiles.push({
      ...attack,
      resolveOnImpact,
      resolving: false,
    });
  }

  function resolvePlayerProjectile(projectile) {
    if (!socket?.connected || projectile.resolving) return;
    projectile.resolving = true;
    socket.emit('combat:resolve_player_projectile', {
      attack_id: projectile.attack_id,
      csrf_token: orbData.dataset.csrfToken
    }, (result) => {
      if (result?.early || result?.busy) {
        projectile.resolving = false;
        window.setTimeout(() => resolvePlayerProjectile(projectile), 100);
        return;
      }
      playerProjectileInFlight = false;
      const index = playerProjectiles.indexOf(projectile);
      if (index >= 0) playerProjectiles.splice(index, 1);
      if (!result?.ok) showNotice(result?.error || 'O projétil não atingiu o alvo.', 'error');
    });
  }

  function drawPlayerProjectiles(cameraX, cameraY, time) {
    const now = Date.now();
    for (let index = playerProjectiles.length - 1; index >= 0; index -= 1) {
      const attack = playerProjectiles[index];
      const projectile = attack.projectile;
      const progress = Math.max(0, Math.min(1, (now - attack.created_at) / projectile.flight_ms));
      const target = enemies.find((enemy) => enemy.id === attack.enemy_id && enemy.alive);
      const targetX = target?.world_x ?? projectile.target_x;
      const targetY = target?.world_y ?? projectile.target_y;
      const worldX = projectile.origin_x + (targetX - projectile.origin_x) * progress;
      const worldY = projectile.origin_y + (targetY - projectile.origin_y) * progress;
      const height = Math.sin(progress * Math.PI) * 55;
      const x = worldX - cameraX, y = worldY - cameraY;
      const colors = {
        fire: ['#ffbd77', '#ed684d'],
        ice: ['#dcfaff', '#69c5df'],
        lightning: ['#fff0a5', '#e4c444'],
        umbral: ['#e1caff', '#9873d1'],
      };
      const [core, glow] = colors[projectile.element] || ['#e5e7eb', '#8eb8e8'];
      ctx.save();
      ctx.globalCompositeOperation = 'lighter';
      const gradient = ctx.createRadialGradient(x, y - height, 1, x, y - height, 20);
      gradient.addColorStop(0, `${core}f2`);
      gradient.addColorStop(.38, `${glow}b8`);
      gradient.addColorStop(1, `${glow}00`);
      ctx.fillStyle = gradient;
      ctx.beginPath(); ctx.arc(x, y - height, 20, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = core;
      ctx.beginPath(); ctx.arc(x, y - height, 5, 0, Math.PI * 2); ctx.fill();
      ctx.restore();
      if (progress >= 1) {
        if (attack.resolveOnImpact) resolvePlayerProjectile(attack);
        else playerProjectiles.splice(index, 1);
      }
    }
  }

  function drawSkillEffects(cameraX, cameraY, time) {
    for (let index = skillEffects.length - 1; index >= 0; index -= 1) {
      const effect = skillEffects[index];
      const progress = (time - effect.startedAt) / 850;
      if (progress >= 1) {
        skillEffects.splice(index, 1);
        continue;
      }
      const colors = {
        repulse: '#f0bd63',
        gravity_well: '#a58ce0',
        area_burst: '#f08c62',
        chain: '#fff0a5',
        combo: '#dc7566',
        echo_strikes: '#b7a0e8',
        shadow_raise: '#a58ce0',
        guard: '#91bde6',
        sanctuary: '#8fd7e6',
        evasion: '#c4e6f4',
        execution: '#e8b870',
        precision: '#fff0a5',
        drain: '#c594df',
        rune_combo: '#e5c27a',
      };
      const color = colors[effect.kind] || '#e2c07d';
      const centerX = effect.x - cameraX;
      const centerY = effect.y - cameraY;
      const baseRadius = Math.max(34, Number(effect.radius) || 70);
      const radius = effect.kind === 'gravity_well'
        ? baseRadius * (1 - progress * .72)
        : baseRadius * (.25 + progress * .75);
      ctx.save();
      ctx.globalCompositeOperation = 'lighter';
      ctx.globalAlpha = (1 - progress) * .75;
      ctx.strokeStyle = color;
      ctx.lineWidth = Math.max(1, 4 * (1 - progress));
      ctx.beginPath();
      ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
      ctx.stroke();
      if (effect.kind === 'chain' || effect.count > 1) {
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.arc(centerX, centerY, radius * .62, 0, Math.PI * 2);
        ctx.stroke();
      }
      ctx.restore();
    }
  }

  function advanceEnemyAttacks() {
    const now = Date.now();
    for (let index = enemyAttacks.length - 1; index >= 0; index -= 1) {
      const attack = enemyAttacks[index];
      if (now < attack.impact_at) continue;
      enemyAttacks.splice(index, 1);
      if (!socket?.connected || isGamePaused()) continue;
      resolveEnemyAttack(attack, 0);
    }
  }

  function resolveEnemyAttack(attack, attempt) {
    if (!socket?.connected || attempt > 3) return;
    socket.emit('combat:resolve_enemy_attack', {
      attack_id: attack.attack_id,
      player_x: player.x,
      player_y: player.y,
      csrf_token: orbData.dataset.csrfToken
    }, (response) => {
      if (response?.busy && attempt < 3) {
        window.setTimeout(() => resolveEnemyAttack(attack, attempt + 1), 100 * (attempt + 1));
      }
    });
  }

  function drawCardXpOrbs(cameraX, cameraY, time) {
    for (const orb of cardXpOrbs) {
      if (orb.collected || orb.collecting) continue;
      const x = orb.world_x - cameraX;
      const y = orb.world_y - cameraY;
      if (x < -35 || y < -35 || x > width + 35 || y > height + 35) continue;
      const pulse = .5 + .5 * Math.sin(time * .002 + orb.id * .71);
      const glowRadius = 48 + pulse * 12;
      ctx.save();
      ctx.globalCompositeOperation = 'lighter';
      const diffuseGlow = ctx.createRadialGradient(x, y - 2, 0, x, y - 2, glowRadius);
      diffuseGlow.addColorStop(0, `rgba(255, 246, 205, ${.52 + pulse * .12})`);
      diffuseGlow.addColorStop(.18, `rgba(255, 221, 139, ${.34 + pulse * .1})`);
      diffuseGlow.addColorStop(.52, `rgba(255, 177, 62, ${.16 + pulse * .08})`);
      diffuseGlow.addColorStop(1, 'rgba(255, 161, 42, 0)');
      ctx.fillStyle = diffuseGlow;
      ctx.beginPath(); ctx.arc(x, y - 2, glowRadius, 0, Math.PI * 2); ctx.fill();

      const innerGlow = ctx.createRadialGradient(x, y - 3, 1, x, y - 3, 19 + pulse * 3);
      innerGlow.addColorStop(0, 'rgba(255, 255, 239, .98)');
      innerGlow.addColorStop(.28, 'rgba(255, 242, 190, .94)');
      innerGlow.addColorStop(.62, 'rgba(255, 203, 99, .52)');
      innerGlow.addColorStop(1, 'rgba(255, 174, 55, 0)');
      ctx.fillStyle = innerGlow;
      ctx.beginPath(); ctx.arc(x, y - 3, 22 + pulse * 3, 0, Math.PI * 2); ctx.fill();

      for (let spark = 0; spark < 6; spark += 1) {
        const angle = time * .00038 + spark * Math.PI / 3 + orb.id;
        const radius = 15 + pulse * 5 + (spark % 2) * 4;
        const sparkAlpha = .3 + pulse * .3;
        ctx.fillStyle = `rgba(255, 249, 220, ${sparkAlpha})`;
        ctx.beginPath(); ctx.arc(x + Math.cos(angle) * radius, y - 3 + Math.sin(angle) * radius * .55, 1.1, 0, Math.PI * 2); ctx.fill();
      }
      ctx.restore();

      ctx.strokeStyle = `rgba(255, 231, 167, ${.7 + pulse * .22})`;
      ctx.lineWidth = 1.5;
      ctx.beginPath(); ctx.ellipse(x, y + 4, 14 + pulse * 2, 5.5 + pulse, 0, 0, Math.PI * 2); ctx.stroke();
      ctx.fillStyle = 'rgba(255, 202, 91, .32)';
      ctx.beginPath(); ctx.ellipse(x, y + 4, 9 + pulse, 3 + pulse * .35, 0, 0, Math.PI * 2); ctx.fill();

      // Bright, sharply defined nucleus sits above the fuzzy aura.
      ctx.fillStyle = '#fff1b8';
      ctx.beginPath(); ctx.arc(x, y - 5, 7.5, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = '#fffdf0';
      ctx.beginPath(); ctx.arc(x - 1, y - 6, 4.4, 0, Math.PI * 2); ctx.fill();
      ctx.fillStyle = '#ffffff';
      ctx.beginPath(); ctx.arc(x - 1.5, y - 7, 2.2, 0, Math.PI * 2); ctx.fill();
    }
  }

  function collectNearbyOrb() {
    if (!orbData || !socket?.connected || orbCollectionInFlight !== null || Date.now() < orbCollectionRetryAt) return;
    const orb = cardXpOrbs.find((candidate) => !candidate.collected && !collectingOrbs.has(candidate.id)
      && Math.hypot(candidate.world_x - player.x, candidate.world_y - player.y) < player.radius + 11);
    if (!orb) return;
    orbCollectionInFlight = orb.id;
    collectingOrbs.add(orb.id);
    orb.collecting = true;
    socket.emit('card_orb:collect', {
      orb_id: orb.id,
      csrf_token: orbData.dataset.csrfToken
    }, (result) => {
      if (result?.ok) {
        applyOrbCollection(result);
        return;
      }
      if (orbCollectionInFlight === orb.id) orbCollectionInFlight = null;
      orb.collecting = false;
      collectingOrbs.delete(orb.id);
      if (result?.busy) orbCollectionRetryAt = Date.now() + 180;
      else if (result?.error) showNotice(result.error, 'error');
    });
  }

  function applyOrbCollection(state) {
    const orbId = Number(state?.orb_id);
    if (!orbId) return;
    const orb = cardXpOrbs.find((candidate) => Number(candidate.id) === orbId);
    if (orb) { orb.collected = true; orb.collecting = false; }
    collectingOrbs.delete(orbId);
    if (orbCollectionInFlight === orbId) orbCollectionInFlight = null;
    if (state.already_collected || appliedOrbCollections.has(orbId)) return;
    appliedOrbCollections.add(orbId);
    updateCardXpProgress(state);
    activeCardsFull = state.active_cards.length >= state.card_limit;
    showNotice(`Orbe coletado: +${state.xp_gained} de experiência para cartas.`);
  }

  function moveOrbsTowardPlayer(delta) {
    for (const orb of cardXpOrbs) {
      if (orb.collected || orb.collecting) continue;
      const dx = player.x - orb.world_x;
      const dy = player.y - orb.world_y;
      const distance = Math.hypot(dx, dy);
      if (distance > 155 || distance < 1) continue;
      const pullSpeed = 90 + (155 - distance) * 4.2;
      const movement = Math.min(distance, pullSpeed * delta);
      orb.world_x += (dx / distance) * movement;
      orb.world_y += (dy / distance) * movement;
    }
  }

  function showNotice(message, category = 'success') {
    let notices = document.querySelector('.game-notices');
    if (!notices) {
      notices = document.createElement('div');
      notices.className = 'game-notices';
      document.querySelector('.game-shell').append(notices);
    }
    notices.replaceChildren();
    const notice = document.createElement('div');
    notice.className = `notice ${category}`;
    notice.textContent = message;
    notices.append(notice);
    window.setTimeout(() => notice.remove(), 2800);
  }

  function updateCardPanel(state) {
    const panel = document.querySelector('.active-card-panel');
    if (!panel || !state) return;
    if (Array.isArray(state.active_cards)) activeCardData = state.active_cards;
    pendingCardChoices = Math.max(0, Number(state.pending_card_choices) || 0);
    syncCardDraftToggle();
    updateCardXpProgress(state);
    const ready = panel.querySelector('.card-xp-ready');
    if (state.pending_card_choices > 0 && !ready) {
      const notice = document.createElement('b'); notice.className = 'card-xp-ready';
      notice.textContent = 'Escolha de carta disponível';
      panel.querySelector('.card-xp-progress')?.append(notice);
    } else if (state.pending_card_choices <= 0) {
      ready?.remove();
    }
    const heading = panel.querySelector('.active-card-heading span');
    if (heading) heading.textContent = `${state.active_cards.length} / ${state.card_limit}`;
    if (state.max_health && state.health !== undefined) updateResourceValue('health', state.health, state.max_health);
    if (state.max_mana && state.mana !== undefined) updateResourceValue('mana', state.mana, state.max_mana);
    if (state.move_speed_multiplier) moveSpeedMultiplier = Number(state.move_speed_multiplier);
    if (state.attack_range_multiplier) attackRangeMultiplier = Number(state.attack_range_multiplier);
    if (state.cooldown_multiplier) cooldownScale = Math.max(.5, 1 - agility * .005) * Number(state.cooldown_multiplier);
    const previousList = panel.querySelector('.active-card-list, .no-active-cards');
    if (previousList) previousList.remove();
    if (state.active_cards.length) {
      const list = document.createElement('div');
      list.className = 'active-card-list';
      for (const card of state.active_cards) {
        const chip = document.createElement('div');
        chip.className = 'active-card-chip';
        chip.tabIndex = 0;
        chip.style.setProperty('--rarity-color', card.color);
        chip.title = card.description;
        chip.setAttribute('aria-label', `${card.name} · ${card.rarity} · ${card.description}`);
        const name = document.createElement('span'); name.textContent = card.name;
        const rarity = document.createElement('small'); rarity.textContent = card.rarity;
        const tooltip = document.createElement('span'); tooltip.className = 'active-card-tooltip';
        tooltip.setAttribute('role', 'tooltip'); tooltip.textContent = card.description;
        chip.append(name, rarity, tooltip); list.append(chip);
      }
      panel.append(list);
    } else {
      const empty = document.createElement('p');
      empty.className = 'no-active-cards'; empty.textContent = 'Escolha uma carta antes de iniciar a onda.';
      panel.append(empty);
    }
  }

  function updateCardXpProgress(state) {
    const panel = document.querySelector('.active-card-panel');
    if (!panel || !state) return;
    const xp = panel.querySelector('.card-xp-copy strong');
    const xpFill = panel.querySelector('.card-xp-track span');
    const xpTrack = panel.querySelector('.card-xp-track');
    if (xp && xpFill && xpTrack) {
      const current = state.card_experience || 0;
      const needed = state.card_experience_needed || 100;
      xp.textContent = `${current} / ${needed}`;
      xpFill.style.width = `${Math.min(100, current / needed * 100)}%`;
      xpTrack.setAttribute('aria-valuenow', String(current));
    }
  }

  function stopCardAutoPick() {
    if (cardAutoPickInterval !== null) window.clearInterval(cardAutoPickInterval);
    cardAutoPickInterval = null;
    cardAutoPickOfferId = 0;
  }

  function tickCardAutoPick(offerId, recommendedId, deadline) {
    if (cardAutoPickOfferId !== Number(offerId)) return;
    const remaining = Math.max(0, Math.ceil(Number(deadline) - Date.now() / 1000));
    const countdown = document.querySelector('#card-auto-countdown');
    if (countdown) countdown.textContent = remaining > 0 ? `${remaining}s` : (isPremium ? '0s' : 'Escolha manual');
    if (remaining <= 0 && !isPremium) {
      if (cardAutoPickInterval !== null) window.clearInterval(cardAutoPickInterval);
      cardAutoPickInterval = null;
      return;
    }
    if (remaining > 0 || !socket?.connected || cardChoiceInFlight
        || cardAutoPickSubmittedId === Number(offerId)) return;
    cardChoiceInFlight = true;
    cardAutoPickSubmittedId = Number(offerId);
    document.querySelectorAll('.offered-card').forEach((option) => {
      option.disabled = true;
      option.setAttribute('aria-busy', 'true');
    });
    socket.emit('card:auto_choose', {
      offer_id: offerId,
      csrf_token: orbData.dataset.csrfToken
    }, (result) => {
      cardChoiceInFlight = false;
      if (result?.ok) {
        cardAutoPickSubmittedId = 0;
        // A resposta pode chegar depois do evento card:state da próxima oferta.
        // Aplicar o estado retornado mantém o novo prazo de 10 s por escolha.
        applyCardState(result);
        return;
      }
      cardAutoPickSubmittedId = 0;
      document.querySelectorAll('.offered-card').forEach((option) => {
        option.disabled = false;
        option.removeAttribute('aria-busy');
      });
      if (result?.stale) applyCardState(result);
      else if (!result?.busy && !result?.not_due) showNotice(result?.error || 'Não foi possível escolher a carta recomendada.', 'error');
      if (result?.not_due && result.remaining_seconds) {
        const nextDeadline = Date.now() / 1000 + Number(result.remaining_seconds);
        startCardAutoPick({ id: offerId, recommended_card_id: recommendedId, auto_pick_at: nextDeadline });
      }
    });
  }

  function startCardAutoPick(offer) {
    stopCardAutoPick();
    if (!isPremium) return;
    const offerId = Number(offer?.id || 0);
    const recommendedId = offer?.recommended_card_id ?? '';
    const deadline = Number(offer?.auto_pick_at || 0);
    if (!offerId || !recommendedId || !deadline) return;
    cardAutoPickOfferId = offerId;
    cardAutoPickSubmittedId = 0;
    tickCardAutoPick(offerId, recommendedId, deadline);
    cardAutoPickInterval = window.setInterval(
      () => tickCardAutoPick(offerId, recommendedId, deadline), 250
    );
  }

  function clearCardDialog() {
    stopCardAutoPick();
    document.querySelector('.card-draft-backdrop')?.remove();
    syncCardDraftToggle();
  }

  function isCardDraftOpen() {
    const backdrop = document.querySelector('.card-draft-backdrop');
    return Boolean(backdrop && !backdrop.hidden);
  }

  function syncCardDraftToggle() {
    const toggle = document.querySelector('#card-draft-toggle');
    if (!toggle) return;
    const label = toggle.querySelector('[data-card-toggle-label]');
    const notification = toggle.querySelector('[data-card-new-indicator]');
    const count = toggle.querySelector('[data-card-choice-count]');
    const open = isCardDraftOpen();
    toggle.hidden = pendingCardChoices <= 0;
    toggle.dataset.pendingChoices = String(pendingCardChoices);
    toggle.classList.toggle('has-new-card', pendingCardChoices > 0 && !open);
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', pendingCardChoices > 0
      ? `${pendingCardChoices} nova(s) escolha(s) de carta. ${open ? 'Pressione Tab para ocultar.' : 'Pressione Tab para abrir.'}`
      : 'Nenhuma escolha de carta pendente.');
    if (label) label.textContent = open ? 'Ocultar cartas' : 'Ver cartas';
    if (notification) notification.hidden = open || pendingCardChoices <= 0;
    if (count) count.textContent = `${pendingCardChoices} ${pendingCardChoices === 1 ? 'escolha' : 'escolhas'}`;
  }

  function setCardDraftOpen(open) {
    const backdrop = document.querySelector('.card-draft-backdrop');
    if (!backdrop) return;
    backdrop.hidden = !open;
    syncCardDraftToggle();
    if (open) backdrop.querySelector('.offered-card, .replacement-card-choice input, .replace-card-form button:not(:disabled)')?.focus();
    else document.querySelector('#card-draft-toggle')?.focus();
  }

  function toggleCardDraft() {
    if (pendingCardChoices <= 0) return;
    setCardDraftOpen(!isCardDraftOpen());
  }

  function emitCardChoice(payload, onFailure = null, onSuccess = null) {
    if (!socket?.connected) {
      showNotice('Reconectando ao servidor. Tente novamente em instantes.', 'error');
      onFailure?.({ offline: true });
      return;
    }
    socket.emit('card:choose', { ...payload, csrf_token: orbData.dataset.csrfToken }, (result) => {
      if (!result?.ok) {
        if (result?.stale) applyCardState(result);
        showNotice(result?.error || 'Não foi possível salvar a escolha.', result?.stale ? 'info' : 'error');
        onFailure?.(result);
        return;
      }
      onSuccess?.(result);
    });
  }

  function applyCardState(state) {
    if (!state) return;
    if (isGamePaused() && (state.offer || state.replacement_required)) return;
    const hasOfferPayload = Object.prototype.hasOwnProperty.call(state, 'offer')
      || Object.prototype.hasOwnProperty.call(state, 'offer_id')
      || state.replacement_required;
    const offerId = Number(state.offer?.id ?? state.offer_id ?? 0);
    const offerRevision = Number(state.offer_revision ?? latestCardOfferRevision);
    const hasOffer = Boolean(state.replacement_required || state.offer);
    if (hasOfferPayload && offerRevision < latestCardOfferRevision) return;
    if (hasOfferPayload && hasOffer && offerRevision === latestCardOfferRevision && latestCardOfferResolved) return;
    if (offerRevision > latestCardOfferRevision) latestCardOfferRevision = offerRevision;
    if (hasOffer) latestCardOfferResolved = false;
    else if (state.offer_resolved || Number(state.pending_card_choices || 0) === 0) {
      latestCardOfferResolved = true;
    }
    const previouslySelectedActiveId = document.querySelector(
      '.replace-card-form [name="replacement_card_id"]:checked'
    )?.value;
    updateCardPanel(state);
    if (state.replacement_required) {
      renderReplacement(state.selected_card, state.active_cards, offerId, {
        selectedActiveId: previouslySelectedActiveId,
        saving: cardChoiceInFlight,
      });
      setCardDraftOpen(true);
    }
    else if (state.offer) {
      if (state.offer.selected_card) {
        renderReplacement(state.offer.selected_card, state.active_cards || [], offerId, {
          selectedActiveId: previouslySelectedActiveId,
          saving: cardChoiceInFlight,
        });
        setCardDraftOpen(true);
      }
      else renderOffer(state.offer);
    }
    else clearCardDialog();
    if (state.message) showNotice(state.message);
  }

  function createCardBackdrop(kicker, title, description) {
    clearCardDialog();
    const backdrop = document.createElement('div'); backdrop.id = 'card-draft-backdrop'; backdrop.className = 'card-draft-backdrop';
    const dialog = document.createElement('section'); dialog.className = 'card-draft-dialog';
    dialog.setAttribute('role', 'dialog'); dialog.setAttribute('aria-modal', 'false');
    const eyebrow = document.createElement('span'); eyebrow.className = 'scene-kicker'; eyebrow.textContent = kicker;
    const heading = document.createElement('h2'); heading.textContent = title;
    const copy = document.createElement('p'); copy.textContent = description;
    dialog.append(eyebrow, heading, copy); backdrop.append(dialog);
    document.querySelector('.game-shell').append(backdrop);
    backdrop.hidden = true;
    syncCardDraftToggle();
    return dialog;
  }

  function renderOffer(offer) {
    const phase = document.querySelector('#phase-number')?.textContent;
    const wave = document.querySelector('#wave-number')?.textContent;
    const phaseWave = phase && wave ? `FASE ${phase} / ONDA ${wave}` : 'COLEÇÃO';
    const dialog = createCardBackdrop(phaseWave, 'Escolha uma carta', 'A recomendação considera sua classe, os efeitos e a raridade. Você pode escolher qualquer uma das três.');
    if (isPremium) {
      const timer = document.createElement('p'); timer.className = 'card-auto-countdown';
      timer.append('A recomendada será ativada em ');
      const timerValue = document.createElement('strong'); timerValue.id = 'card-auto-countdown'; timerValue.textContent = '10s';
      timer.append(timerValue, ' se você não escolher. Cada oferta tem seu próprio prazo.');
      dialog.append(timer);
    } else {
      const manual = document.createElement('p'); manual.className = 'card-manual-choice';
      manual.textContent = 'Escolha no seu tempo. A carta recomendada está destacada.';
      dialog.append(manual);
    }
    const grid = document.createElement('div'); grid.className = 'card-offer-grid';
    for (const card of offer.cards || []) {
      const recommended = card.id === offer.recommended_card_id;
      const button = document.createElement('button'); button.type = 'button'; button.className = `offered-card${recommended ? ' is-recommended' : ''}`;
      button.dataset.cardId = card.id;
      button.dataset.offerId = offer.id;
      button.dataset.cardDetails = JSON.stringify(card);
      button.style.setProperty('--rarity-color', card.color);
      if (recommended) {
        const badge = document.createElement('span'); badge.className = 'offered-card-recommendation'; badge.textContent = 'RECOMENDADA';
        button.append(badge);
      }
      const rarity = document.createElement('span'); rarity.className = 'offered-card-rarity'; rarity.textContent = card.rarity;
      const name = document.createElement('strong'); name.textContent = card.name;
      const category = document.createElement('span'); category.className = 'offered-card-category'; category.textContent = card.category;
      const description = document.createElement('span'); description.className = 'offered-card-description'; description.textContent = card.description;
      const action = document.createElement('span'); action.className = 'offered-card-select'; action.textContent = 'Escolher carta';
      button.append(rarity, name, category, description, action);
      grid.append(button);
    }
    dialog.append(grid);
    if (activeCardsFull) {
      const keepForm = document.createElement('form');
      keepForm.method = 'post'; keepForm.action = '/jogo/cartas/escolher';
      keepForm.className = 'keep-offer-form';
      const csrf = document.createElement('input'); csrf.type = 'hidden'; csrf.name = 'csrf_token'; csrf.value = orbData.dataset.csrfToken;
      const keep = document.createElement('button');
      keep.type = 'submit'; keep.name = 'skip_replacement'; keep.value = '1'; keep.className = 'keep-offer-button';
      keep.dataset.cardKeepOffer = String(offer.id);
      keep.textContent = 'Manter cartas ativas · descartar estas 3 opções';
      keepForm.append(csrf, keep); dialog.append(keepForm);
    }
    startCardAutoPick(offer);
  }

  function renderReplacement(card, activeCards, offerId, options = {}) {
    stopCardAutoPick();
    const dialog = createCardBackdrop('COLEÇÃO CHEIA', 'Escolha a carta que sairá', `Nova carta: ${card.name} · ${card.rarity}. Marque uma carta ativa e confirme a substituição.`);
    dialog.classList.add('replacement-dialog');
    const form = document.createElement('form'); form.className = 'replace-card-form';
    form.method = 'post'; form.action = '/jogo/cartas/escolher';
    form.dataset.offerId = String(offerId || 0);
    const csrf = document.createElement('input'); csrf.type = 'hidden'; csrf.name = 'csrf_token'; csrf.value = orbData.dataset.csrfToken;
    const selected = document.createElement('input'); selected.type = 'hidden'; selected.name = 'selected_card_id'; selected.value = card.id;
    const label = document.createElement('strong'); label.className = 'replacement-selection-prompt'; label.textContent = 'Clique na carta ativa que deseja remover';
    const choices = document.createElement('div'); choices.className = 'replacement-card-options';
    for (const active of activeCards) {
      const choice = document.createElement('label'); choice.className = 'replacement-card-choice';
      choice.style.setProperty('--rarity-color', active.color || '#8f8f8f');
      const radio = document.createElement('input'); radio.type = 'radio'; radio.name = 'replacement_card_id'; radio.value = active.id; radio.required = true;
      radio.checked = String(active.id) === String(options.selectedActiveId || '');
      const rarity = document.createElement('small'); rarity.textContent = active.rarity || 'Comum';
      const name = document.createElement('strong'); name.textContent = active.name;
      const effect = document.createElement('span'); effect.className = 'replacement-card-effect';
      effect.textContent = `Efeito atual: ${active.description || 'Efeito não informado.'}`;
      choice.append(radio, rarity, name, effect); choices.append(choice);
    }
    const replace = document.createElement('button'); replace.type = 'submit'; replace.className = 'primary-button'; replace.textContent = 'Substituir e ativar';
    const keep = document.createElement('button'); keep.type = 'submit'; keep.className = 'keep-cards-button'; keep.name = 'skip_replacement'; keep.value = '1'; keep.formNoValidate = true; keep.textContent = 'Manter cartas ativas · descartar opções';
    if (options.saving) {
      const saving = document.createElement('small'); saving.className = 'replacement-save-status';
      saving.textContent = 'Abrindo substituição…';
      form.append(csrf, selected, label, saving, choices, replace, keep);
      replace.disabled = true;
      keep.disabled = true;
      dialog.append(form);
      return;
    }
    form.append(csrf, selected, label, choices, replace, keep); dialog.append(form);
  }

  function updateWaveState(state) {
    if (state.card_state) applyCardState(state.card_state);
    if (state.phase_changed) {
      cardXpOrbs.splice(0, cardXpOrbs.length);
      collectingOrbs.clear();
      appliedOrbCollections.clear();
    }
    updateStageNumbers(state.phase, state.wave);
    const healthFill = document.querySelector('#health-fill');
    const healthValue = document.querySelector('#health-value');
    const manaFill = document.querySelector('#mana-fill');
    const manaValue = document.querySelector('#mana-value');
    if (healthFill && state.max_health) healthFill.style.width = `${state.health / state.max_health * 100}%`;
    if (healthValue && state.max_health) healthValue.textContent = `${state.health} / ${state.max_health}`;
    if (manaFill && state.max_mana) manaFill.style.width = `${state.mana / state.max_mana * 100}%`;
    if (manaValue && state.max_mana) manaValue.textContent = `${state.mana} / ${state.max_mana}`;
    if (state.monsters_remaining !== undefined) updateMonsterCount(state.monsters_remaining);
    if (state.phase_preparation_until !== undefined) setPhasePreparation(state.phase_preparation_until);
    const level = document.querySelector('#character-level');
    if (level) level.innerHTML = `${state.level}<small> / ${state.max_level}</small>`;
    const track = document.querySelector('#character-experience-track');
    const fill = document.querySelector('#character-experience-fill');
    if (track && fill) {
      track.setAttribute('aria-valuemax', String(state.next_level_xp));
      track.setAttribute('aria-valuenow', String(state.experience));
      fill.style.width = `${state.next_level_xp ? state.experience / state.next_level_xp * 100 : 100}%`;
    }
    updateExperienceCopy(state.experience, state.next_level_xp, state.level, state.max_level);
    const waveForm = document.querySelector('.wave-prototype-action');
    if (waveForm) {
      const caption = waveForm.querySelector('span');
      const button = waveForm.querySelector('button');
      caption.textContent = `Conclusão simulada · recompensa de ${state.next_wave_reward} de experiência`;
      button.textContent = state.campaign_complete
        ? 'Temporada concluída'
        : state.next_is_boss ? 'Concluir chefe' : 'Concluir onda';
      button.disabled = Boolean(state.campaign_complete);
    }
    if (state.orb && !cardXpOrbs.some((orb) => orb.id === state.orb.id)) cardXpOrbs.push(state.orb);
    if (state.awaiting_phase_choice) {
      enterPhaseIntermission();
    }
    if (state.campaign_complete) {
      const campaignOverlay = document.querySelector('#campaign-complete-overlay');
      if (campaignOverlay) campaignOverlay.hidden = false;
      showNotice('Temporada 1 concluída. Sua progressão foi preservada.', 'success');
      return;
    }
    let message = state.is_boss_wave
      ? `Chefe derrotado no protótipo. Fase ${state.phase} iniciada.`
      : `Onda concluída. Próxima: fase ${state.phase}, onda ${state.wave}.`;
    if (state.phase_changed) showChapterIntro(state.phase);
    else announceStage(state.phase, state.wave, {
      isBossWave: state.next_is_boss,
      isMiniBossWave: state.next_is_miniboss,
    });
    if (state.levels_gained) message += ` Você subiu ${state.levels_gained} nível(is)!`;
    showNotice(message);
  }

  function isPhasePreparing() {
    return phasePreparationUntil > Date.now() / 1000;
  }

  function setPhasePreparation(until) {
    phasePreparationUntil = Number(until) || 0;
    updatePhasePreparation();
  }

  function updatePhasePreparation() {
    const panel = document.querySelector('#phase-preparation');
    const countdown = document.querySelector('#phase-preparation-seconds');
    const now = Date.now() / 1000;
    const remaining = Math.max(0, Math.ceil(phasePreparationUntil - now));
    const goVisible = phasePreparationUntil > 0 && now < phasePreparationUntil + 0.65;
    if (!panel) return;
    panel.hidden = remaining <= 0 && !goVisible;
    if (countdown && remaining > 0) countdown.textContent = String(remaining);
    else if (countdown && goVisible) countdown.textContent = 'VAI!';
    if (remaining > 0) {
      keys.clear();
      heldMouseButtons.clear();
    }
  }

  function updateMonsterCount(count) {
    const counter = document.querySelector('#monster-count');
    if (counter) counter.textContent = String(Math.max(0, Number(count) || 0));
  }

  function updateStageNumbers(phase, wave) {
    const phaseNumber = document.querySelector('#phase-number');
    const waveNumber = document.querySelector('#wave-number');
    if (phaseNumber && phase !== undefined) phaseNumber.textContent = String(phase);
    if (waveNumber && wave !== undefined) waveNumber.textContent = String(wave);
  }

  function updateExperienceCopy(experience, nextLevelXp, level, maxLevel) {
    const copy = document.querySelector('#character-experience-copy');
    if (!copy) return;
    if (Number(maxLevel) > 0 && Number(level) >= Number(maxLevel)) {
      copy.textContent = 'Nível máximo atingido';
      return;
    }
    const current = Number(experience) || 0;
    const required = Number(nextLevelXp) || 0;
    copy.textContent = `Experiência ${current} / ${required} · faltam ${Math.max(0, required - current)} para o próximo nível`;
  }

  function handleSocketForm(event) {
    const replacementForm = event.target.closest('.replace-card-form');
    const waveForm = event.target.closest('.wave-prototype-action');
    if (!replacementForm && !waveForm) return;
    event.preventDefault();
    if (replacementForm && cardChoiceInFlight) return;
    if (!socket?.connected) { showNotice('Conexão em tempo real indisponível. Aguarde a reconexão.', 'error'); return; }
    if (replacementForm) {
      const keeping = event.submitter?.name === 'skip_replacement';
      const replacement = replacementForm.querySelector('[name="replacement_card_id"]:checked');
      if (!keeping && !replacement) {
        showNotice('Clique na carta ativa que deseja substituir.', 'info');
        return;
      }
      cardChoiceInFlight = true;
      const controls = replacementForm.querySelectorAll('button, input[type="radio"]');
      controls.forEach((control) => { control.disabled = true; });
      emitCardChoice(keeping
        ? { offer_id: replacementForm.dataset.offerId, action: 'keep' }
        : { offer_id: replacementForm.dataset.offerId, replacement_card_id: replacement.value },
      () => {
        cardChoiceInFlight = false;
        controls.forEach((control) => { control.disabled = false; });
      },
      () => {
        cardChoiceInFlight = false;
        controls.forEach((control) => { control.disabled = false; });
      });
    } else {
      socket.emit('game:complete_wave', { csrf_token: orbData.dataset.csrfToken }, (result) => {
        if (!result?.ok) { showNotice(result?.error || 'Não foi possível concluir a onda.', 'error'); return; }
      });
    }
  }

  function bindRealtimeEvents() {
    if (!socket) { showNotice('Não foi possível iniciar a conexão em tempo real.', 'error'); return; }
    const statusDot = document.querySelector('#socket-status');
    socket.on('connect', () => {
      statusDot?.classList.remove('is-connecting', 'is-disconnected');
      if (statusDot) { statusDot.title = 'Conexão em tempo real ativa'; statusDot.setAttribute('aria-label', statusDot.title); }
    });
    socket.on('disconnect', () => {
      resetEnemyAttackRequests();
      attackInFlight = false;
      playerProjectileInFlight = false;
      playerProjectiles.length = 0;
      orbCollectionInFlight = null;
      cardChoiceInFlight = false;
      cardAutoPickSubmittedId = 0;
      document.querySelector('#save-game-options').disabled = false;
      if (optionsDialog?.open) setOptionsFeedback('Conexão perdida. As opções ainda não foram salvas.', true);
      document.querySelectorAll('.offered-card').forEach((option) => {
        option.disabled = false;
        option.removeAttribute('aria-busy');
      });
      collectingOrbs.clear();
      cardXpOrbs.forEach((orb) => { orb.collecting = false; });
      statusDot?.classList.add('is-disconnected');
      if (statusDot) { statusDot.title = 'Conexão em tempo real perdida'; statusDot.setAttribute('aria-label', statusDot.title); }
    });
    socket.on('card_xp:updated', (state) => {
      applyOrbCollection(state);
    });
    socket.on('card:state', applyCardState);
    socket.on('combat:auto_potion_state', (state) => setAutoPotionButton(state.resource, state.enabled));
    socket.on('combat:potion_used', (state) => {
      updateResourceValue(state.resource, state.value, state.maximum);
      showNotice(`Auto-poção de ${state.resource === 'health' ? 'Vida' : 'Mana'} utilizada.`);
    });
    socket.on('combat:player_projectile', (attack) => registerPlayerProjectile(attack, false));
    socket.on('combat:player_mana_updated', (state) => {
      updateResourceValue('mana', state.mana, state.max_mana);
    });
    socket.on('combat:enemy_reflected', (state) => {
      const enemy = enemies.find((item) => item.id === state.enemy_id);
      if (!enemy) return;
      enemy.hp = state.hp;
      showDamageNumber(state.damage, enemy);
    });
    socket.on('combat:enemy_telegraph', registerEnemyAttack);
    socket.on('combat:enemy_updated', (state) => {
      if (state.mission_complete) {
        window.location.assign('/jogo/pos-fase');
        return;
      }
      const enemy = enemies.find((item) => item.id === state.enemy_id);
      if (state.effect_kind && state.effect_center) {
        skillEffects.push({
          kind: state.effect_kind,
          x: state.effect_center.x,
          y: state.effect_center.y,
          radius: state.effect_radius,
          count: state.hit_count,
          startedAt: performance.now(),
        });
      }
      const affectedEnemies = state.affected_enemies || [];
      affectedEnemies.forEach((affected) => {
        const affectedEnemy = enemies.find((item) => item.id === affected.id);
        if (!affectedEnemy) return;
        affectedEnemy.hp = affected.hp;
        affectedEnemy.alive = affected.alive;
        if (affected.position_changed) {
          affectedEnemy.world_x = affected.world_x;
          affectedEnemy.world_y = affected.world_y;
        }
        if (affected.root_duration_ms) {
          affectedEnemy.immobilizedUntil =
            performance.now() + affected.root_duration_ms;
        }
        if (affected.id !== state.enemy_id && affected.damage) {
          showDamageNumber(affected.damage, affectedEnemy);
        }
        if (!affected.alive) {
          for (let index = enemyAttacks.length - 1; index >= 0; index -= 1) {
            if (enemyAttacks[index].enemy_id === affected.id) enemyAttacks.splice(index, 1);
          }
        }
      });
      if (enemy && !affectedEnemies.some((affected) => affected.id === state.enemy_id)) {
        enemy.hp = state.hp;
        enemy.alive = !state.defeated;
        if (state.drop_position) {
          enemy.world_x = state.drop_position.world_x;
          enemy.world_y = state.drop_position.world_y;
        }
      }
      if (state.defeated) {
        for (let index = enemyAttacks.length - 1; index >= 0; index -= 1) {
          if (enemyAttacks[index].enemy_id === state.enemy_id) enemyAttacks.splice(index, 1);
        }
      }
      if (state.phase_changed) {
        cardXpOrbs.splice(0, cardXpOrbs.length);
        collectingOrbs.clear();
        appliedOrbCollections.clear();
      }
      (state.orbs || (state.orb ? [state.orb] : [])).forEach((orb) => {
        if (!cardXpOrbs.some((item) => item.id === orb.id)) cardXpOrbs.push(orb);
      });
      if (state.card_state) applyCardState(state.card_state);
      if (state.enemies_remaining === 0) {
        if (state.is_boss_wave && !state.mission_complete) {
          dispatchDialogueHook('boss_encounter', {
            phase: state.phase,
            difficulty: sceneLabel?.dataset.difficulty || 'risk_low',
          });
        }
        enemyAttacks.length = 0;
        enemies.splice(0, enemies.length, ...state.next_enemies.map(prepareEnemy));
        updateMonsterCount(state.next_enemies.length);
        if (state.phase_preparation_until !== undefined) setPhasePreparation(state.phase_preparation_until);
        updateStageNumbers(state.phase, state.wave);
        if (state.phase_changed && !state.mission_complete) showChapterIntro(state.phase);
        if (state.awaiting_phase_choice && !state.mission_complete) {
          enterPhaseIntermission();
        }
        else if (!state.campaign_complete && !state.mission_complete) announceStage(state.phase, state.wave, {
          bossDefeated: state.boss_defeated,
          isBossWave: state.is_boss_wave,
          isMiniBossWave: state.is_miniboss_wave
        });
      } else updateMonsterCount(state.enemies_remaining);
      const level = document.querySelector('#character-level');
      if (level) level.innerHTML = `${state.level}<small> / ${state.max_level}</small>`;
      const xpTrack = document.querySelector('#character-experience-track');
      const xpFill = document.querySelector('#character-experience-fill');
      if (xpTrack && xpFill) {
        xpTrack.setAttribute('aria-valuemax', String(state.next_level_xp));
        xpTrack.setAttribute('aria-valuenow', String(state.experience));
        xpFill.style.width = `${state.next_level_xp ? state.experience / state.next_level_xp * 100 : 100}%`;
      }
      updateExperienceCopy(state.experience, state.next_level_xp, state.level, state.max_level);
      if (state.campaign_complete) {
        const campaignOverlay = document.querySelector('#campaign-complete-overlay');
        if (campaignOverlay) campaignOverlay.hidden = false;
      }
      if (state.defeated) {
        let message = state.campaign_complete
          ? 'Temporada 1 concluída. Sua progressão foi preservada.'
          : state.phase_changed
            ? 'Fase concluída. A coleção temporária foi encerrada; prepare a próxima fase na Sala de Espera.'
            : state.enemies_remaining === 0
              ? `Onda concluída! Próxima: fase ${state.phase}, onda ${state.wave}. +${state.experience_gained} de experiência e um orbe caiu.`
              : `Monstro derrotado: +${state.experience_gained} de experiência. Um orbe de cartas caiu.`;
        if (state.levels_gained) message += ` Você subiu ${state.levels_gained} nível(is)!`;
        if (state.legacy_points_gained) {
          const points = Number(state.legacy_points_gained);
          message += ` Você recebeu ${points} ${points === 1 ? 'Ponto' : 'Pontos'} de Legado.`;
        }
        if (state.legacy_milestones_gained) message += ' Marco de 50 níveis alcançado!';
        showNotice(message);
      }
      if (state.life_stolen) showNotice(`Você recuperou ${state.life_stolen} de Vida pelo dano causado.`);
      if (state.active_effect?.damage_reduction) {
        showNotice('Proteção ativada: você receberá menos dano por alguns instantes.', 'success');
      } else if (state.active_effect?.dodge_chance) {
        showNotice('Esquiva ampliada por alguns instantes.', 'success');
      } else if (state.hit_count > 1 && state.skill_name) {
        showNotice(`${state.skill_name}: ${state.hit_count} impactos.`, 'success');
      }
      if (state.shadow_summoned) {
        const count = Number(state.shadow_soldier_count || 0);
        const soldierLabel = count === 1
          ? 'soldado das sombras ajuda'
          : 'soldados das sombras ajudam';
        showNotice(`Erga-se! ${count} ${soldierLabel} nos próximos ataques.`, 'success');
      }
      if (state.shadow_support_damage) {
        showNotice(`Soldados das sombras causaram ${state.shadow_support_damage} de dano.`, 'success');
      }
      if (state.effect_kind === 'gravity_well' && state.affected_enemies?.length) {
        showNotice('O núcleo gravitacional prendeu os inimigos por alguns instantes.', 'success');
      }
      const manaFill = document.querySelector('#mana-fill');
      const manaValue = document.querySelector('#mana-value');
      const healthFill = document.querySelector('#health-fill');
      const healthValue = document.querySelector('#health-value');
      if (healthFill) healthFill.style.width = `${state.health / state.max_health * 100}%`;
      if (healthValue) healthValue.textContent = `${state.health} / ${state.max_health}`;
      if (manaFill) manaFill.style.width = `${state.mana / state.max_mana * 100}%`;
      if (manaValue) manaValue.textContent = `${state.mana} / ${state.max_mana}`;
      if (state.damage && enemy) showDamageNumber(state.damage, enemy, state.critical);
    });
    socket.on('combat:player_damaged', (state) => {
      const fill = document.querySelector('#health-fill');
      const value = document.querySelector('#health-value');
      if (fill) fill.style.width = `${state.health / state.max_health * 100}%`;
      if (value) value.textContent = `${state.health} / ${state.max_health}`;
      const manaFill = document.querySelector('#mana-fill');
      const manaValue = document.querySelector('#mana-value');
      if (manaFill) manaFill.style.width = `${state.mana / state.max_mana * 100}%`;
      if (manaValue) manaValue.textContent = `${state.mana} / ${state.max_mana}`;
      if (state.damage) showPlayerDamage(state.damage);
      if (state.dodged) showNotice('Esquiva!', 'success');
      if (state.card_state) {
        cardXpOrbs.splice(0, cardXpOrbs.length);
        collectingOrbs.clear();
        appliedOrbCollections.clear();
        clearCardDialog();
        applyCardState(state.card_state);
      }
      if (state.death) {
        enemyAttacks.length = 0;
        heldMouseButtons.clear();
        keys.clear();
        document.querySelector('#death-overlay').hidden = false;
        enemies.splice(0, enemies.length, ...state.next_enemies.map(prepareEnemy));
        updateMonsterCount(state.next_enemies.length);
        updateStageNumbers(state.phase, 1);
      }
    });
    socket.on('game:wave_updated', updateWaveState);
    socket.on('auth:logout', () => window.location.assign('/'));
    socket.on('connect_error', () => {
      statusDot?.classList.add('is-connecting');
      showNotice('Reconectando ao servidor em tempo real…', 'error');
    });
    document.addEventListener('submit', handleSocketForm);
  }

  function updateResourceValue(resource, value, maximum) {
    const fill = document.querySelector(`#${resource === 'health' ? 'health' : 'mana'}-fill`);
    const label = document.querySelector(`#${resource === 'health' ? 'health' : 'mana'}-value`);
    if (fill) fill.style.width = `${value / maximum * 100}%`;
    if (label) label.textContent = `${value} / ${maximum}`;
  }

  function setAutoPotionButton(resource, enabled) {
    const button = document.querySelector(`[data-potion="${resource}"]`);
    if (!button) return;
    button.dataset.enabled = enabled ? '1' : '0';
    button.classList.toggle('is-enabled', enabled);
    button.setAttribute('aria-pressed', enabled ? 'true' : 'false');
    const label = button.querySelector('small');
    if (label) label.textContent = enabled ? 'Ativa' : 'Desativada';
  }

  function toggleAutoPotion(button) {
    const resource = button.dataset.potion;
    if (button.dataset.premium !== '1') {
      showNotice('As poções automáticas exigem o benefício especial.', 'error');
      return;
    }
    if (!socket?.connected || potionToggleRequests.has(resource)) return;
    const enabled = button.dataset.enabled !== '1';
    potionToggleRequests.add(resource);
    socket.emit('combat:auto_potion:toggle', {
      resource, enabled, csrf_token: orbData.dataset.csrfToken
    }, (result) => {
      potionToggleRequests.delete(resource);
      if (!result?.ok) {
        showNotice(result?.error || 'Não foi possível alterar a auto-poção.', 'error');
        return;
      }
      setAutoPotionButton(resource, result.enabled);
    });
  }

  document.querySelectorAll('[data-potion]').forEach((button) => {
    button.addEventListener('click', () => toggleAutoPotion(button));
  });
  document.querySelector('#premium-test-toggle')?.addEventListener('click', (event) => {
    const button = event.currentTarget;
    if (!socket?.connected) {
      showNotice('Conexão em tempo real indisponível. Aguarde a reconexão.', 'error');
      return;
    }
    button.disabled = true;
    socket.emit('account:toggle_test_premium', {
      csrf_token: orbData.dataset.csrfToken
    }, (result) => {
      if (!result?.ok) {
        button.disabled = false;
        showNotice(result?.error || 'Não foi possível alterar o benefício especial.', 'error');
        return;
      }
      window.location.reload();
    });
  });
  document.querySelector('#card-draft-toggle')?.addEventListener('click', toggleCardDraft);
  document.addEventListener('click', (event) => {
    const keepOffer = event.target.closest('[data-card-keep-offer]');
    if (keepOffer && !cardChoiceInFlight) {
      event.preventDefault();
      cardChoiceInFlight = true;
      keepOffer.disabled = true;
      emitCardChoice({ offer_id: keepOffer.dataset.cardKeepOffer, action: 'keep' }, () => {
        cardChoiceInFlight = false;
        keepOffer.disabled = false;
      }, () => {
        cardChoiceInFlight = false;
        keepOffer.disabled = false;
      });
      return;
    }
    const button = event.target.closest('.offered-card[data-card-id]');
    if (!button || button.disabled || cardChoiceInFlight) return;
    event.preventDefault();
    const offerId = Number(button.dataset.offerId);
    let selectedCard = null;
    try { selectedCard = JSON.parse(button.dataset.cardDetails || '{}'); } catch (_error) { /* fallback to the server response */ }
    const offerSnapshot = activeCardsFull ? {
      id: offerId,
      cards: [...document.querySelectorAll('.offered-card[data-card-details]')].map((option) => {
        try { return JSON.parse(option.dataset.cardDetails); } catch (_error) { return null; }
      }).filter(Boolean),
      recommended_card_id: document.querySelector('.offered-card.is-recommended')?.dataset.cardId,
      auto_pick_at: Number(orbData.dataset.cardAutoPickAt || 0),
    } : null;
    if (offerSnapshot && selectedCard?.id) {
      renderReplacement(selectedCard, activeCardData, offerId, { saving: true });
      setCardDraftOpen(true);
    }
    cardChoiceInFlight = true;
    document.querySelectorAll('.offered-card').forEach((option) => {
      option.disabled = true;
      option.setAttribute('aria-busy', 'true');
    });
    const chosenCardId = button.dataset.cardId;
    emitCardChoice({ card_id: chosenCardId, offer_id: offerId }, (result) => {
      cardChoiceInFlight = false;
      if (result?.stale) return;
      if (offerSnapshot) {
        renderOffer(offerSnapshot);
        setCardDraftOpen(true);
        return;
      }
      document.querySelectorAll('.offered-card').forEach((option) => {
        option.disabled = false;
        option.removeAttribute('aria-busy');
      });
    }, (result) => {
      cardChoiceInFlight = false;
      if (result?.stale) return;
      applyCardState(result);
    });
  });
  document.addEventListener('keydown', (event) => {
    if (optionsDialog?.open) return;
    if (event.key === 'Tab' && pendingCardChoices > 0) {
      event.preventDefault();
      event.stopPropagation();
      if (!event.repeat) toggleCardDraft();
      return;
    }
    if (event.repeat || event.target instanceof HTMLInputElement || event.target instanceof HTMLTextAreaElement) return;
    if (event.key.toLowerCase() === 'q') document.querySelector('[data-potion="health"]')?.click();
    if (event.key.toLowerCase() === 'e') document.querySelector('[data-potion="mana"]')?.click();
  });

  function attackWith(skillId) {
    if (isGamePaused() || isPhasePreparing() || isCardDraftOpen() || playerProjectileInFlight) return;
    if (!skillId) return;
    const requestedSkillId = skillId;
    const requestedSlot = document.querySelector(`[data-skill="${skillId}"]`);
    const requestOnCooldown = skillId !== 'basic'
      && (performance.now() < (localAttackCooldowns.get(skillId) || 0)
        || requestedSlot?.classList.contains('is-cooling'));
    const manaValue = Number(document.querySelector('#mana-value')?.textContent.match(/^\s*(\d+)/)?.[1] || 0);
    const requestWithoutMana = skillId !== 'basic'
      && manaValue < Number(requestedSlot?.dataset.manaCost || 0);
    const localFallbackReason = requestOnCooldown ? 'cooldown' : requestWithoutMana ? 'mana' : null;
    if (localFallbackReason) skillId = 'basic';
    const range = (skillId === 'basic' ? baseAttackRange : skillAttackRange) * attackRangeMultiplier;
    const aimTolerance = skillId === 'basic' ? Math.PI / 3 : Math.PI / 4;
    const candidates = enemies
      .filter((enemy) => enemy.alive && enemy.attackReady)
      .map((enemy) => {
        const dx = enemy.world_x - player.x;
        const dy = enemy.world_y - player.y;
        const distance = Math.hypot(dx, dy);
        let angleDifference = Math.atan2(dy, dx) - aimAngle;
        angleDifference = Math.atan2(Math.sin(angleDifference), Math.cos(angleDifference));
        return { enemy, distance, angleDifference: Math.abs(angleDifference) };
      })
      .filter((candidate) => candidate.distance <= range + candidate.enemy.radius
        && candidate.angleDifference <= aimTolerance)
      .sort((a, b) => a.distance - b.distance);
    const target = (controlScheme === 'mouse_keyboard'
      ? candidates.find((candidate) => candidate.enemy === targetedEnemy)
      : null)?.enemy || candidates[0]?.enemy;
    if (!target || !target.attackReady || !socket?.connected || attackInFlight) return;
    target.attackReady = false;
    const cooldown = (skillId === 'basic' ? 1000 : 6000) * cooldownScale;
    const cooldownUntil = localAttackCooldowns.get(skillId) || 0;
    if (performance.now() < cooldownUntil) { target.attackReady = true; return; }
    attackInFlight = true;
    socket.emit('combat:attack', {
      enemy_id: target.id,
      enemy_x: target.world_x,
      enemy_y: target.world_y,
      player_x: player.x,
      player_y: player.y,
      skill_id: skillId,
      nearby_enemies: enemies.filter((item) => item.alive).map((item) => ({
        id: item.id, x: item.world_x, y: item.world_y,
      })),
      csrf_token: orbData.dataset.csrfToken
    }, (result) => {
      attackInFlight = false;
      if (!result?.ok) {
        if (target.alive) target.attackReady = true;
        const message = result?.error || 'Ataque indisponível.';
        const failedSkillId = result?.fallback ? 'basic' : skillId;
        localAttackCooldowns.set(failedSkillId, performance.now() + (result?.busy ? 1000 : message.includes('recarga') ? cooldown : 0));
        if (!result?.fallback) showNotice(message, 'error');
        return;
      }
      const actualCooldown = Number(result.cooldown_ms) || cooldown;
      const actualSkillId = result.skill_id || skillId;
      localAttackCooldowns.set(actualSkillId, performance.now() + actualCooldown + 75);
      startCooldown(actualSkillId, actualCooldown);
      if (result.mana !== undefined) updateResourceValue('mana', result.mana, result.max_mana);
      if (result.projectile_pending) {
        playerProjectileInFlight = true;
        registerPlayerProjectile(result, true);
      }
      if ((result.fallback || localFallbackReason) && requestedSkillId !== actualSkillId) {
        const fallbackReason = result.fallback_reason || localFallbackReason;
        const noticeKey = `${requestedSkillId}:${fallbackReason}`;
        const now = performance.now();
        if (now - (fallbackNoticeTimes.get(noticeKey) || 0) > 5000) {
          fallbackNoticeTimes.set(noticeKey, now);
          showNotice(fallbackReason === 'mana'
            ? 'Mana insuficiente: Ataque básico executado.'
            : 'Habilidade em recarga: Ataque básico executado.', 'info');
        }
      }
      window.setTimeout(() => {
        if (target.alive) target.attackReady = true;
      }, result.projectile_pending
        ? Number(result.projectile.flight_ms) + 100
        : skillId === 'basic' ? 450 : 250);
    });
  }

  function startDash() {
    if (isGamePaused() || dashRequestInFlight || !socket?.connected) return;
    const slot = document.querySelector('[data-skill="dash"]');
    if (slot?.classList.contains('is-cooling')) return;
    dashRequestInFlight = true;
    socket.emit('combat:dash', { csrf_token: orbData.dataset.csrfToken }, (result) => {
      dashRequestInFlight = false;
      if (!result?.ok) { showNotice(result?.error || 'Avanço indisponível.', 'error'); return; }
      dash.direction = aimAngle;
      dash.remaining = dash.duration;
      startCooldown('dash', result.cooldown * 1000);
    });
  }

  function startCooldown(skillId, duration) {
    const slot = document.querySelector(`[data-skill="${skillId}"]`);
    if (!slot) return;
    slot.classList.add('is-cooling');
    const fill = slot.querySelector('i'); fill.style.transform = 'scaleX(1)';
    const start = performance.now();
    const timer = window.setInterval(() => {
      const remaining = Math.max(0, 1 - (performance.now() - start) / duration);
      fill.style.transform = `scaleX(${remaining})`;
      if (!remaining) { clearInterval(timer); slot.classList.remove('is-cooling'); }
    }, 50);
    skillCooldowns.set(skillId, timer);
  }

  function showDamageNumber(amount, enemy, critical = false) {
    if (!enemy) return;
    const x = enemy.world_x, y = enemy.world_y - 25;
    const label = document.createElement('span');
    label.className = `damage-float${critical ? ' is-critical' : ''}`;
    label.textContent = `-${amount}${critical ? ' CRÍTICO' : ''}`;
    label.dataset.worldX = String(x);
    label.dataset.worldY = String(y);
    const screen = worldToScreen(x, y);
    label.style.left = `${screen.x}px`; label.style.top = `${screen.y}px`;
    document.querySelector('.game-shell').append(label);
    window.setTimeout(() => label.remove(), 850);
  }

  function showPlayerDamage(amount) {
    const label = document.createElement('span'); label.className = 'damage-float damage-received';
    label.textContent = `-${amount}`; label.style.left = `${width / 2}px`; label.style.top = `${height / 2 - 35}px`;
    document.querySelector('.game-shell').append(label); window.setTimeout(() => label.remove(), 850);
  }

  function showCenterBanner(message) {
    const banner = document.createElement('div'); banner.className = 'combat-center-banner'; banner.textContent = message;
    document.querySelector('.game-shell').append(banner); window.setTimeout(() => banner.remove(), 3000);
  }

  function showChapterIntro(phase) {
    if (!sceneLabel || !phase) return false;
    const chapter = Math.floor((phase - 1) / 10);
    const seenKey = `cronicas:character:${sceneLabel.dataset.characterId}:chapter:${chapter}`;
    if (localStorage.getItem(seenKey)) return false;
    localStorage.setItem(seenKey, '1');
    sceneLabel.querySelector('.scene-kicker').textContent = chapter === 0 ? 'CAPÍTULO ZERO' : `CAPÍTULO ${chapter}`;
    if (chapter > 0) {
      sceneLabel.querySelector('h2').textContent = 'Um novo capítulo';
      sceneLabel.querySelector('p').textContent = `A fase ${phase} marca uma nova etapa da jornada.`;
    }
    sceneLabel.classList.remove('is-hidden');
    window.setTimeout(() => sceneLabel.classList.add('is-hidden'), 4800);
    return true;
  }

  function initializeChapterIntro(phase) {
    if (!sceneLabel || !phase) return;
    const chapter = Math.floor((phase - 1) / 10);
    const seenKey = `cronicas:character:${sceneLabel.dataset.characterId}:chapter:${chapter}`;
    if (localStorage.getItem(seenKey)) {
      sceneLabel.classList.add('is-hidden');
      return;
    }
    showChapterIntro(phase);
  }

  function announceStage(phase, wave, { bossDefeated = false, isBossWave = false, isMiniBossWave = false } = {}) {
    const message = bossDefeated
      ? `CHEFE DERROTADO · FASE ${phase} · ONDA ${wave}`
      : isBossWave ? `CHEFE DA FASE · FASE ${phase} · ONDA ${wave}`
        : isMiniBossWave ? `SEMICHEFE · FASE ${phase} · ONDA ${wave}`
        : `FASE ${phase} · ONDA ${wave}`;
    if (showChapterIntro(phase)) {
      window.setTimeout(() => showCenterBanner(message), 5000);
      return;
    }
    showCenterBanner(message);
  }

  function drawVignette() {
    ctx.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);
    const gradient = ctx.createRadialGradient(width / 2, height / 2, Math.min(width, height) * .16, width / 2, height / 2, Math.max(width, height) * .75);
    gradient.addColorStop(0, 'rgba(4, 6, 10, 0)');
    gradient.addColorStop(1, 'rgba(4, 6, 10, .64)');
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, width, height);
  }

  function moveEnemies(delta) {
    if (isPhasePreparing()) return;
    for (const enemy of enemies) {
      if (!enemy.alive) continue;
      if (enemy.immobilizedUntil > performance.now()) continue;
      const dx = player.x - enemy.world_x;
      const dy = player.y - enemy.world_y;
      const distance = Math.hypot(dx, dy);
      const contactDistance = player.radius + enemy.radius + 2;
      const bossStyle = enemy.attack_style === 'miniboss' || enemy.attack_style === 'boss';
      const preferredBossRange = enemy.attack_style === 'boss' ? 265 : 205;
      if (distance <= enemy.attackRange) requestEnemyAttack(enemy);
      if (enemy.attack_style === 'ranged' && distance <= enemy.attackRange) {
        if (distance >= enemy.preferredRange - 25 && distance <= enemy.preferredRange + 45) continue;
      }
      if (enemy.attack_style === 'melee' && distance <= contactDistance + 1) {
        continue;
      }
      if (distance < 1) continue;
      const rangedRetreating = enemy.attack_style === 'ranged' && distance < enemy.preferredRange - 25;
      const bossOrbiting = bossStyle && Math.abs(distance - preferredBossRange) <= 65;
      if (bossStyle && Date.now() >= enemy.nextOrbitChangeAt) {
        enemy.orbitDirection *= -1;
        enemy.nextOrbitChangeAt = Date.now() + 2800 + (Number(enemy.enemy_index || 0) % 3) * 700;
      }
      const retreating = rangedRetreating || (bossStyle && distance < preferredBossRange - 65);
      const travel = bossStyle
        ? bossOrbiting ? Math.min(enemy.chaseSpeed * delta, 18)
          : Math.min(Math.abs(distance - preferredBossRange), enemy.chaseSpeed * delta)
        : rangedRetreating
          ? Math.min(enemy.preferredRange - distance, enemy.chaseSpeed * delta)
          : Math.min(Math.max(0, distance - contactDistance), enemy.chaseSpeed * delta);
      const radialAngle = Math.atan2(retreating ? -dy : dy, retreating ? -dx : dx);
      const targetAngle = bossOrbiting
        ? Math.atan2(dy, dx) + enemy.orbitDirection * Math.PI / 2
        : radialAngle;
      const turns = [0, -Math.PI / 6, Math.PI / 6, -Math.PI / 3, Math.PI / 3,
        -Math.PI / 2, Math.PI / 2, -Math.PI * 2 / 3, Math.PI * 2 / 3, Math.PI];
      let destination = null;
      let bestScore = Infinity;
      for (const turn of turns) {
        const angle = targetAngle + turn;
        const nextX = clampWorldX(enemy.world_x + Math.cos(angle) * travel);
        const nextY = clampWorldY(enemy.world_y + Math.sin(angle) * travel);
        const overlapsAlly = enemies.some((other) => other !== enemy && other.alive
          && Math.hypot(other.world_x - nextX, other.world_y - nextY) < enemy.radius + other.radius - 1);
        if (overlapsAlly || terminalVilarCollides(nextX, nextY, enemy.radius)) continue;
        const remaining = Math.hypot(player.x - nextX, player.y - nextY);
        if (remaining < contactDistance - 1) continue;
        const score = bossStyle
          ? Math.abs(remaining - preferredBossRange) + Math.abs(turn) * 14
            + (bossOrbiting && turn * enemy.orbitDirection < 0 ? 7 : 0)
          : retreating ? -remaining + Math.abs(turn) * 8 : remaining + Math.abs(turn) * 8;
        if (score < bestScore) { bestScore = score; destination = { x: nextX, y: nextY }; }
      }
      if (destination) {
        enemy.world_x = destination.x;
        enemy.world_y = destination.y;
      } else if (distance <= contactDistance + enemy.radius * 2) {
        // If the direct lane is packed, sidestep around the ally to find a free approach.
        const side = Number(enemy.enemy_index || enemy.id) % 2 ? 1 : -1;
        const angle = targetAngle + side * Math.PI / 2;
        const nextX = clampWorldX(enemy.world_x + Math.cos(angle) * enemy.chaseSpeed * delta);
        const nextY = clampWorldY(enemy.world_y + Math.sin(angle) * enemy.chaseSpeed * delta);
        if (!terminalVilarCollides(nextX, nextY, enemy.radius)
          && !enemies.some((other) => other !== enemy && other.alive
            && Math.hypot(other.world_x - nextX, other.world_y - nextY) < enemy.radius + other.radius - 1)) {
          enemy.world_x = nextX;
          enemy.world_y = nextY;
        }
      }
    }
  }

  function update(delta) {
    moveEnemies(delta);
    advanceEnemyAttacks();
    if (keys.has(' ') && dash.remaining <= 0) startDash();
    let dx = Number(keys.has('d') || keys.has('arrowright')) - Number(keys.has('a') || keys.has('arrowleft'));
    let dy = Number(keys.has('s') || keys.has('arrowdown')) - Number(keys.has('w') || keys.has('arrowup'));
    const isDashing = dash.remaining > 0;
    let movementSpeed = player.speed * moveSpeedMultiplier;
    if (isDashing) {
      dx = Math.cos(dash.direction);
      dy = Math.sin(dash.direction);
      movementSpeed = dash.speed;
      dash.remaining = Math.max(0, dash.remaining - delta);
    } else if (dx && dy) { dx *= Math.SQRT1_2; dy *= Math.SQRT1_2; }
    if (controlScheme === 'keyboard_only' && !isDashing && (dx || dy)) {
      aimAngle = Math.atan2(dy, dx);
    }
    const nextX = clampWorldX(player.x + dx * movementSpeed * delta);
    const nextY = clampWorldY(player.y + dy * movementSpeed * delta);
    const canMoveTo = (x, y) => !terminalVilarCollides(x, y, player.radius)
      && (isDashing || isPhasePreparing() || !enemies.some((enemy) => enemy.alive
        && Math.hypot(enemy.world_x - x, enemy.world_y - y) < player.radius + enemy.radius));
    if (isTerminalVilarPhase) {
      const distance = Math.hypot(nextX - player.x, nextY - player.y);
      const stepCount = Math.max(1, Math.ceil(distance / Math.max(2, player.radius * .35)));
      const stepX = (nextX - player.x) / stepCount;
      const stepY = (nextY - player.y) / stepCount;
      for (let step = 0; step < stepCount; step += 1) {
        const candidateX = clampWorldX(player.x + stepX);
        const candidateY = clampWorldY(player.y + stepY);
        if (canMoveTo(candidateX, candidateY)) {
          player.x = candidateX;
          player.y = candidateY;
        } else {
          if (canMoveTo(candidateX, player.y)) player.x = candidateX;
          if (canMoveTo(player.x, candidateY)) player.y = candidateY;
        }
      }
    } else if (canMoveTo(nextX, nextY)) {
      player.x = nextX;
      player.y = nextY;
    } else {
      if (canMoveTo(nextX, player.y)) player.x = nextX;
      if (canMoveTo(player.x, nextY)) player.y = nextY;
    }
  }

  function frame(time) {
    const delta = Math.min((time - (previousTime || time)) / 1000, 0.04);
    previousTime = time;
    if (!isGamePaused() && !isPhasePreparing()) {
      update(delta);
      if (controlScheme === 'mouse_keyboard' && heldMouseButtons.has(0)) attackWith(skillSlots[mouseLeftSlot - 1]);
      if (controlScheme === 'mouse_keyboard' && heldMouseButtons.has(2)) attackWith(skillSlots[mouseRightSlot - 1]);
    }
    updatePhasePreparation();
    if (!isGamePaused() && !isPhasePreparing()) {
      moveOrbsTowardPlayer(delta);
      collectNearbyOrb();
    }

    currentCamera = updateCamera(delta);
    if (controlScheme === 'mouse_keyboard') {
      const pointerWorld = screenToWorld(mouse.x, mouse.y, currentCamera);
      aimAngle = Math.atan2(pointerWorld.y - player.y, pointerWorld.x - player.x);
    }
    updateTargetPanel(findTargetedEnemy(currentCamera));
    ctx.setTransform(pixelRatio, 0, 0, pixelRatio, 0, 0);
    ctx.clearRect(0, 0, width, height);
    ctx.setTransform(pixelRatio * cameraZoom, 0, 0, pixelRatio * cameraZoom * cameraTiltY, 0, 0);
    ctx.save();
    ctx.beginPath();
    ctx.rect(-currentCamera.x, -currentCamera.y, world.width, world.height);
    ctx.clip();
    drawFloor(currentCamera.x, currentCamera.y, currentCamera.viewWidth, currentCamera.viewHeight);
    terminalVilarEffects?.drawGround(ctx, currentCamera, time / 1000);
    if (isTerminalVilarPhase && !terminalVilarArtworkLoaded) {
      drawCentralPlatform(currentCamera.x, currentCamera.y);
    }
    drawMapLandmarks(currentCamera.x, currentCamera.y);
    drawRuins(currentCamera.x, currentCamera.y);
    drawBaseRange(currentCamera.x, currentCamera.y, time);
    drawEnemyTelegraphs(currentCamera.x, currentCamera.y, time);
    drawCardXpOrbs(currentCamera.x, currentCamera.y, time);
    drawEnemy(currentCamera.x, currentCamera.y);
    drawEnemyProjectiles(currentCamera.x, currentCamera.y, time);
    drawPlayerProjectiles(currentCamera.x, currentCamera.y, time);
    drawSkillEffects(currentCamera.x, currentCamera.y, time);
    drawPlayer(player.x - currentCamera.x, player.y - currentCamera.y, time);
    terminalVilarEffects?.drawAtmosphere(ctx, currentCamera, player.y, time / 1000);
    ctx.restore();
    if (!terminalVilarArtworkLoaded) drawVignette();
    document.querySelectorAll('.damage-float[data-world-x]').forEach((label) => {
      const screen = worldToScreen(Number(label.dataset.worldX), Number(label.dataset.worldY));
      label.style.left = `${screen.x}px`;
      label.style.top = `${screen.y}px`;
    });
    coordinates.innerHTML = `X ${String(Math.round(player.x)).padStart(4, '0')} <span>·</span> Y ${String(Math.round(player.y)).padStart(4, '0')}`;
    requestAnimationFrame(frame);
  }

  window.addEventListener('keydown', (event) => {
    const key = event.key.toLowerCase();
    if (optionsDialog?.open) return;
    if (isGamePaused()) { event.preventDefault(); return; }
    if (isPhasePreparing()) { event.preventDefault(); return; }
    if (isCardDraftOpen()) {
      if (['w', 'a', 's', 'd', 'arrowup', 'arrowdown', 'arrowleft', 'arrowright'].includes(key)) {
        event.preventDefault();
        keys.add(key);
        return;
      }
      if (key === ' ') {
        event.preventDefault();
        keys.add(key);
        if (!event.repeat) startDash();
        return;
      }
      return;
    }
    const slotMatch = event.code.match(/^(?:Digit|Numpad)([1-4])$/);
    if (slotMatch) {
      event.preventDefault();
      if (event.repeat) return;
      const slotNumber = Number(slotMatch[1]);
      if (slotNumber === 1) {
        attackWith('basic');
        return;
      }
      const action = skillSlots[slotNumber - 1];
      if (action) attackWith(action);
      else showNotice(`A magia do espaço ${slotNumber - 1} ainda não está equipada.`, 'info');
      return;
    }
    if (key === ' ') {
      event.preventDefault();
      keys.add(key);
      if (!event.repeat) startDash();
      return;
    }
    if (['w', 'a', 's', 'd', 'arrowup', 'arrowdown', 'arrowleft', 'arrowright'].includes(key)) event.preventDefault();
    keys.add(key);
  });
  window.addEventListener('keyup', (event) => keys.delete(event.key.toLowerCase()));
  window.addEventListener('blur', () => { keys.clear(); heldMouseButtons.clear(); });
  window.addEventListener('resize', resize);
  document.querySelector('#fullscreen').addEventListener('click', async () => {
    if (!document.fullscreenElement) await document.documentElement.requestFullscreen?.();
    else await document.exitFullscreen?.();
  });

  resize();
  initializeChapterIntro(Number(sceneLabel?.dataset.phase));
  syncCardDraftToggle();
  if (orbData?.dataset.cardReplacementPending === '1') setCardDraftOpen(true);
  bindRealtimeEvents();
  if (Number(orbData?.dataset.cardOfferId || 0) > 0) {
    startCardAutoPick({
      id: orbData?.dataset.cardOfferId,
      recommended_card_id: orbData?.dataset.cardRecommendedId,
      auto_pick_at: orbData?.dataset.cardAutoPickAt
    });
  }
  requestAnimationFrame(frame);
})();
