const assert = require('node:assert/strict');
const fs = require('node:fs');
const net = require('node:net');
const os = require('node:os');
const path = require('node:path');
const { spawn } = require('node:child_process');
const test = require('node:test');
const { chromium } = require('playwright');

const projectRoot = path.resolve(__dirname, '../..');
const serverScript = path.join(__dirname, 'mission-e2e-server.py');
const pythonExecutable = path.join(projectRoot, '.conda', 'python.exe');
let browser;

test.before(async () => {
  browser = await chromium.launch({ headless: true });
});

test.after(async () => {
  await browser?.close();
});

async function reservePort() {
  const server = net.createServer();
  await new Promise((resolve, reject) => {
    server.once('error', reject);
    server.listen(0, '127.0.0.1', resolve);
  });
  const { port } = server.address();
  await new Promise((resolve, reject) => {
    server.close((error) => (error ? reject(error) : resolve()));
  });
  return port;
}

async function startScenario(mode, difficulty) {
  assert.ok(fs.existsSync(pythonExecutable), 'workspace Python environment is required');
  const directory = fs.mkdtempSync(path.join(os.tmpdir(), 'cronicas-mission-e2e-'));
  const port = await reservePort();
  const database = path.join(directory, 'mission.sqlite3');
  const sessionCookiePath = path.join(directory, 'session.json');
  const args = [
    serverScript,
    '--mode', mode,
    '--port', String(port),
    '--database', database,
    '--session-cookie', sessionCookiePath,
  ];
  if (difficulty) args.push('--difficulty', difficulty);

  const child = spawn(pythonExecutable, args, {
    cwd: projectRoot,
    env: { ...process.env },
    stdio: ['ignore', 'pipe', 'pipe'],
  });
  let stdout = '';
  let stderr = '';
  child.stdout.setEncoding('utf8').on('data', (chunk) => { stdout += chunk; });
  child.stderr.setEncoding('utf8').on('data', (chunk) => { stderr += chunk; });

  const baseUrl = `http://127.0.0.1:${port}`;
  let sessionCookie;
  const deadline = Date.now() + 15000;
  try {
    while (Date.now() < deadline) {
      if (child.exitCode !== null) {
        throw new Error(`E2E server exited (${child.exitCode}): ${stderr || stdout}`);
      }
      if (fs.existsSync(sessionCookiePath)) {
        sessionCookie = JSON.parse(fs.readFileSync(sessionCookiePath, 'utf8'));
        try {
          const response = await fetch(`${baseUrl}/cadastro`);
          if (response.ok) break;
        } catch {
          await new Promise((resolve) => setTimeout(resolve, 100));
        }
      } else {
        await new Promise((resolve) => setTimeout(resolve, 100));
      }
    }
    assert.ok(sessionCookie, `E2E server did not start: ${stderr || stdout}`);
    return {
      baseUrl,
      sessionCookie,
      output: () => `${stdout}\n${stderr}`,
      async stop() {
        if (child.exitCode === null) child.kill();
        await Promise.race([
          new Promise((resolve) => child.once('exit', resolve)),
          new Promise((resolve) => setTimeout(resolve, 5000)),
        ]);
        fs.rmSync(directory, { recursive: true, force: true });
      },
    };
  } catch (error) {
    if (child.exitCode === null) child.kill();
    fs.rmSync(directory, { recursive: true, force: true });
    throw error;
  }
}

async function openAuthenticatedPage(scenario) {
  const context = await browser.newContext();
  await context.addCookies([{
    ...scenario.sessionCookie,
    domain: '127.0.0.1',
    path: '/',
    httpOnly: true,
    secure: false,
    sameSite: 'Lax',
  }]);
  return { context, page: await context.newPage() };
}

async function exposeGameSocket(page, events) {
  await page.exposeFunction('recordMissionE2EEvent', (eventName, payload) => {
    events.push({ eventName, payload });
  });
  await page.addInitScript(() => {
    let ioFactory;
    Object.defineProperty(window, 'io', {
      configurable: true,
      get: () => ioFactory,
      set: (factory) => {
        ioFactory = (...args) => {
          const socket = factory(...args);
          window.__missionE2ESocket = socket;
          socket.on('combat:enemy_updated', (payload) => {
            window.recordMissionE2EEvent('combat:enemy_updated', payload);
          });
          socket.on('combat:player_damaged', (payload) => {
            window.recordMissionE2EEvent('combat:player_damaged', payload);
          });
          return socket;
        };
        Object.assign(ioFactory, factory);
      },
    });
  });
}

test('phase one renders the Terminal de Vilar map in the real game canvas', async () => {
  const scenario = await startScenario('mission', 'risk_low');
  const { context, page } = await openAuthenticatedPage(scenario);
  const pageErrors = [];
  page.on('pageerror', (error) => pageErrors.push(error.message));

  try {
    await page.addInitScript(() => {
      const originalDrawImage = CanvasRenderingContext2D.prototype.drawImage;
      window.__terminalVilarArtworkDraws = 0;
      window.__terminalVilarArtworkDimensions = null;
      window.__terminalVilarArtworkDrawArguments = null;
      CanvasRenderingContext2D.prototype.drawImage = function (image, ...args) {
        if (image instanceof HTMLImageElement && image.src.includes('terminal_vilar_fase1.jpg')) {
          window.__terminalVilarArtworkDraws += 1;
          window.__terminalVilarArtworkDimensions = [image.naturalWidth, image.naturalHeight];
          window.__terminalVilarArtworkDrawArguments = args;
        }
        return originalDrawImage.call(this, image, ...args);
      };
    });
    await page.goto(`${scenario.baseUrl}/sala-de-espera`);
    await page.locator('#mission-phase').selectOption('1');
    await Promise.all([
      page.waitForURL(/\/jogo$/),
      page.locator('#mission-start-form button[type="submit"]').click(),
    ]);
    assert.equal(await page.locator('.scene-label').getAttribute('data-phase'), '1');
    await page.waitForFunction(
      () => window.__terminalVilarArtworkDraws > 0,
      null,
      { timeout: 8000 },
    );
    assert.deepEqual(
      await page.evaluate(() => window.__terminalVilarArtworkDimensions),
      [1200, 896],
    );
    const artworkDrawArguments = await page.evaluate(
      () => window.__terminalVilarArtworkDrawArguments,
    );
    assert.equal(artworkDrawArguments.length, 8);
    assert.ok(artworkDrawArguments[0] > 0);
    assert.ok(artworkDrawArguments[1] > 0);
    assert.equal(artworkDrawArguments[4], 0);
    assert.equal(artworkDrawArguments[5], 0);
    const colliders = JSON.parse(
      await page.locator('#terminal-vilar-collision-map').textContent(),
    );
    assert.ok(colliders.some((collider) => collider.id === 'canopy-bench-west'));
    await page.waitForFunction(
      () => document.querySelector('#phase-preparation')?.hidden === true,
      null,
      { timeout: 8000 },
    );
    const initialCoordinates = await page.locator('#coordinates').textContent();
    await page.keyboard.down('w');
    await page.waitForTimeout(1800);
    await page.keyboard.up('w');
    const movedCoordinates = await page.locator('#coordinates').textContent();
    assert.notEqual(movedCoordinates, initialCoordinates, 'the integrated map must preserve player movement');
    const y = Number(movedCoordinates.match(/Y (\d+)/)?.[1]);
    assert.ok(y >= 625 && y < 850, `player should stop at the center bench, received Y=${y}`);
    assert.deepEqual(pageErrors, []);
  } finally {
    await context.close();
    await scenario.stop();
  }
});

test('Terminal de Vilar preview route uses current artwork, geometry and debug controls', async () => {
  const scenario = await startScenario('inventory');
  const { context, page } = await openAuthenticatedPage(scenario);
  const pageErrors = [];
  page.on('pageerror', (error) => pageErrors.push(error.message));

  try {
    await page.addInitScript(() => {
      const originalDrawImage = CanvasRenderingContext2D.prototype.drawImage;
      window.__terminalVilarArtworkDraws = 0;
      window.__terminalVilarArtworkDimensions = null;
      CanvasRenderingContext2D.prototype.drawImage = function (image, ...args) {
        if (image instanceof HTMLImageElement && image.src.includes('terminal_vilar_fase1.jpg')) {
          window.__terminalVilarArtworkDraws += 1;
          window.__terminalVilarArtworkDimensions = [image.naturalWidth, image.naturalHeight];
        }
        return originalDrawImage.call(this, image, ...args);
      };
    });
    await page.goto(`${scenario.baseUrl}/mapas/terminal-vilar-fase1`);
    const canvas = page.locator('#gameCanvas');
    await page.waitForFunction(
      () => window.__terminalVilarArtworkDraws > 0,
    );
    assert.deepEqual(
      await page.evaluate(() => window.__terminalVilarArtworkDimensions),
      [1200, 896],
    );
    assert.equal(await canvas.getAttribute('width'), '2400');
    assert.equal(await canvas.getAttribute('height'), '1800');
    const mapConfig = JSON.parse(
      await page.locator('#terminal-vilar-map-config').textContent(),
    );
    assert.ok(mapConfig.colliders.length > 0);
    assert.ok(mapConfig.solid_polygons.length > 0);
    assert.ok(mapConfig.collision_walls.length > 0);
    await page.locator('#debugBtn').click();
    assert.match(await page.locator('#debugBtn').getAttribute('class'), /active/);
    assert.deepEqual(pageErrors, []);
  } finally {
    await context.close();
    await scenario.stop();
  }
});

async function attackForMissionFlow(page, enemy, csrfToken) {
  for (let attempt = 0; attempt < 5; attempt += 1) {
    const result = await page.evaluate(
      ({ target, token }) => new Promise((resolve) => {
        window.__missionE2ESocket.emit('combat:attack', {
          enemy_id: target.id,
          enemy_x: target.world_x,
          enemy_y: target.world_y,
          player_x: target.world_x,
          player_y: target.world_y,
          skill_id: 'basic',
          nearby_enemies: [],
          csrf_token: token,
        }, resolve);
      }),
      { target: enemy, token: csrfToken },
    );
    if (result?.ok) return result;
    if (result?.error === 'Ataque básico em recarga.') {
      await page.waitForTimeout(150);
      continue;
    }
    assert.fail(`mission attack failed: ${JSON.stringify(result)}`);
  }
  assert.fail('basic attack remained on cooldown after retries');
}

for (const difficulty of ['risk_moderate', 'risk_high', 'risk_extreme']) {
  test(`real mission page starts ${difficulty} and applies active movement/attack`, async () => {
    const scenario = await startScenario('mission', difficulty);
    const { context, page } = await openAuthenticatedPage(scenario);
    const pageErrors = [];
    page.on('pageerror', (error) => pageErrors.push(error.message));

    try {
      await page.goto(`${scenario.baseUrl}/sala-de-espera`);
      await page.locator('#mission-difficulty').selectOption(difficulty);
      await page.locator('#mission-phase').selectOption('1');
      await Promise.all([
        page.waitForURL(/\/jogo$/),
        page.locator('#mission-start-form button[type="submit"]').click(),
      ]);

      const scene = page.locator('.scene-label');
      assert.equal(await scene.getAttribute('data-difficulty'), difficulty);
      assert.equal(await page.locator('#phase-preparation').isHidden(), false);
      const enemies = JSON.parse(
        await page.locator('#card-xp-orbs').getAttribute('data-enemies'),
      );
      assert.ok(enemies.length >= 3, 'expected a live wave loaded by the Flask route');
      assert.ok(enemies.every((enemy) => enemy.hp > 0 && enemy.hp === enemy.max_hp));
      await page.waitForFunction(
        () => document.querySelector('#socket-status')?.title === 'Conexão em tempo real ativa',
        null,
        { timeout: 8000 },
      );

      await page.waitForFunction(
        () => document.querySelector('#phase-preparation')?.hidden === true,
        null,
        { timeout: 8000 },
      );
      const start = { x: 1200, y: 900 };
      const target = enemies
        .filter((enemy) => !enemy.is_boss && !enemy.is_miniboss)
        .sort((left, right) => (
          Math.hypot(left.world_x - start.x, left.world_y - start.y)
          - Math.hypot(right.world_x - start.x, right.world_y - start.y)
        ))[0];
      assert.ok(target, 'expected a common enemy in the first wave');

      const dx = target.world_x - start.x;
      const dy = target.world_y - start.y;
      const keys = [];
      if (dx > 12) keys.push('d');
      if (dx < -12) keys.push('a');
      if (dy > 12) keys.push('s');
      if (dy < -12) keys.push('w');
      const initialCoordinates = await page.locator('#coordinates').textContent();
      const initialHealth = (await page.locator('#health-value').textContent()).trim();
      for (const key of keys) await page.keyboard.down(key);
      await page.waitForTimeout(1300);
      for (const key of keys) await page.keyboard.up(key);
      const movedCoordinates = await page.locator('#coordinates').textContent();
      assert.notEqual(movedCoordinates, initialCoordinates, 'movement input should move the player');

      const targetPanel = page.locator('#target-monster-panel');
      await targetPanel.waitFor({ state: 'visible', timeout: 6000 });
      const health = page.locator('#target-monster-health');
      const beforeAttack = (await health.textContent()).trim();
      let attackLanded = false;
      for (let attempt = 0; attempt < 4 && !attackLanded; attempt += 1) {
        await page.keyboard.press('1');
        try {
          await page.waitForFunction(
            (previous) => {
              const current = document.querySelector('#target-monster-health');
              return current && current.textContent.trim() !== previous;
            },
            beforeAttack,
            { timeout: 1400 },
          );
          attackLanded = true;
        } catch {
          await page.waitForTimeout(250);
        }
      }
      assert.ok(attackLanded, `basic attack did not update target health from ${beforeAttack}`);
      await page.waitForFunction(
        (previous) => {
          const current = document.querySelector('#health-value');
          return current && current.textContent.trim() !== previous;
        },
        initialHealth,
        { timeout: 6000 },
      );
      assert.deepEqual(pageErrors, []);
    } finally {
      await context.close();
      await scenario.stop();
    }
  });
}

for (const difficulty of ['risk_moderate', 'risk_high', 'risk_extreme']) {
  test(`real Flask mission completes boss phase 10 in ${difficulty}`, { timeout: 180000 }, async () => {
    const scenario = await startScenario('full_mission', difficulty);
    const { context, page } = await openAuthenticatedPage(scenario);
    const pageErrors = [];
    const events = [];
    page.on('pageerror', (error) => pageErrors.push(error.message));

    try {
      await exposeGameSocket(page, events);
      await page.goto(`${scenario.baseUrl}/sala-de-espera`);
      await page.locator('#mission-difficulty').selectOption(difficulty);
      await page.locator('#mission-phase').selectOption('10');
      await Promise.all([
        page.waitForURL(/\/jogo$/),
        page.locator('#mission-start-form button[type="submit"]').click(),
      ]);
      await page.waitForFunction(
        () => window.__missionE2ESocket?.connected,
        null,
        { timeout: 8000 },
      );
      assert.equal(
        await page.locator('.scene-label').getAttribute('data-phase'),
        '10',
      );
      await page.waitForFunction(
        () => document.querySelector('#phase-preparation')?.hidden === true,
        null,
        { timeout: 8000 },
      );

      const enemyData = await page.locator('#card-xp-orbs').getAttribute('data-enemies');
      let enemies = JSON.parse(enemyData);
      const csrfToken = await page.locator('#card-xp-orbs').getAttribute('data-csrf-token');
      const completedWaves = [];
      let wave = 1;
      let attackCount = 0;
      let missionComplete = false;

      while (wave <= 10 && !missionComplete) {
        const target = enemies.find((enemy) => enemy.alive && enemy.hp > 0);
        assert.ok(target, `phase ${wave} must contain a live enemy`);
        let result;
        try {
          result = await attackForMissionFlow(page, target, csrfToken);
        } catch (error) {
          const completedByEvent = events.some(
            (event) => event.eventName === 'combat:enemy_updated'
              && event.payload.mission_complete,
          );
          if (!completedByEvent) throw error;
          completedWaves.push(wave);
          missionComplete = true;
          break;
        }
        attackCount += 1;
        target.hp = result.hp;
        if (result.defeated) target.alive = false;

        if (result.enemies_remaining === 0) {
          completedWaves.push(wave);
          if (result.mission_complete) {
            assert.equal(wave, 10);
            missionComplete = true;
            break;
          }
          assert.equal(result.wave, wave + 1);
          wave = result.wave;
          enemies = result.next_enemies;
          assert.ok(enemies.length > 0, `wave ${wave} must spawn enemies`);
        } else {
          await page.waitForTimeout(650);
        }
      }

      await page.waitForURL(/\/jogo\/pos-fase$/, { timeout: 10000 });
      assert.equal(missionComplete, true);
      assert.deepEqual(completedWaves, [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);
      assert.ok(attackCount >= 10, 'the phase should resolve through combat attacks');
      const completionEvent = events.find(
        (event) => event.eventName === 'combat:enemy_updated'
          && event.payload.mission_complete,
      );
      assert.ok(completionEvent, 'the boss defeat should complete the mission');
      assert.equal(completionEvent.payload.boss_defeated, true);
      assert.ok(
        events.some((event) => event.eventName === 'combat:player_damaged'),
        'enemy attacks should reach the player during the full phase',
      );
      assert.equal(await page.locator('#mission-completion-continue').count(), 1);
      assert.deepEqual(pageErrors, []);
    } finally {
      await context.close();
      await scenario.stop();
    }
  });
}

test('real post-mission page resolves a full inventory after selling an old item', async () => {
  const scenario = await startScenario('inventory');
  const { context, page } = await openAuthenticatedPage(scenario);
  const pageErrors = [];
  page.on('pageerror', (error) => pageErrors.push(error.message));

  try {
    await page.goto(`${scenario.baseUrl}/jogo/pos-fase`);
    assert.equal(
      await page.locator('#mission-completion-continue').count(),
      1,
      `post-mission page was not rendered at ${page.url()}: `
        + `${(await page.locator('body').innerText()).slice(0, 500)}\n${scenario.output()}`,
    );
    await page.locator('#mission-completion-continue').click();
    assert.equal(await page.locator('.inventory-capacity').first().textContent(), '30 / 30');
    assert.equal(await page.locator('#mission-loot-submit').isDisabled(), true);
    assert.match(
      await page.locator('#capacity-feedback').textContent(),
      /A seleção ocupa 31 espaços/,
    );
    assert.equal(await page.getByText('Sala de Espera bloqueada').count(), 1);

    const firstItem = page.locator('.inventory-resolution-panel .resolution-item').first();
    await firstItem.locator('button[name="action"][value="sell"]').click();
    await page.locator('#mission-completion-continue').click();
    assert.equal(await page.locator('.inventory-capacity').first().textContent(), '29 / 30');
    assert.equal(await page.locator('#mission-loot-submit').isDisabled(), false);
    assert.match(
      await page.locator('#capacity-feedback').textContent(),
      /Após confirmar: 30 \/ 30 espaços ocupados/,
    );

    await page.locator('#mission-loot-submit').click();
    await page.waitForURL(/\/sala-de-espera$/, { timeout: 5000 }).catch(async () => {
      assert.fail(
        `loot resolution stayed at ${page.url()}: `
          + `${(await page.locator('body').innerText()).slice(0, 500)}\n${scenario.output()}`,
      );
    });
    assert.match(await page.locator('.lobby-notice').textContent(), /1 item\(ns\) resgatado/);
    await page.goto(`${scenario.baseUrl}/inventario`);
    assert.match(
      await page.locator('.inventory-account-summary').textContent(),
      /Inventário: 30 \/ 30/,
    );
    assert.deepEqual(pageErrors, []);
  } finally {
    await context.close();
    await scenario.stop();
  }
});
