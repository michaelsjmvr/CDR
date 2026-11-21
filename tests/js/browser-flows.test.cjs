const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const { spawnSync } = require('node:child_process');
const test = require('node:test');
const { chromium } = require('playwright');

const projectRoot = path.resolve(__dirname, '../..');
const scriptsDirectory = path.join(projectRoot, 'game_app', 'static', 'js');
let browser;

function firstPartyJavaScriptFiles(directory) {
  return fs.readdirSync(directory, { withFileTypes: true }).flatMap((entry) => {
    const entryPath = path.join(directory, entry.name);
    if (entry.isDirectory()) {
      return entry.name === 'vendor' ? [] : firstPartyJavaScriptFiles(entryPath);
    }
    return entry.isFile() && entry.name.endsWith('.js') ? [entryPath] : [];
  });
}

function scriptPath(filename) {
  return path.join(scriptsDirectory, filename);
}

test.before(async () => {
  browser = await chromium.launch({ headless: true });
});

test.after(async () => {
  await browser?.close();
});

test('all first-party browser scripts pass the Node syntax check', () => {
  const scripts = firstPartyJavaScriptFiles(scriptsDirectory);
  assert.ok(scripts.length > 0, 'expected first-party JavaScript files');

  for (const file of scripts) {
    const result = spawnSync(process.execPath, ['--check', file], {
      encoding: 'utf8',
    });
    assert.equal(
      result.status,
      0,
      `${path.relative(projectRoot, file)} failed syntax check:\n${result.stderr}`,
    );
  }
});

test('lobby phase selector follows each difficulty available-phase state', async () => {
  const page = await browser.newPage();
  const pageErrors = [];
  page.on('pageerror', (error) => pageErrors.push(error.message));

  try {
    await page.setContent(`
      <section class="mission-selection">
        <select id="mission-difficulty">
          <option value="risk_low" selected>Baixo</option>
          <option value="risk_moderate">Moderado</option>
          <option value="risk_extreme">Extremo</option>
        </select>
        <select id="mission-phase">
          <option value="1">Fase 1</option>
          <option value="2">Fase 2</option>
          <option value="3" selected>Fase 3</option>
        </select>
        <form id="mission-start-form">
          <button type="submit">Começar</button>
        </form>
      </section>
    `);
    await page.locator('.mission-selection').evaluate((element) => {
      element.dataset.difficultyStates = JSON.stringify([
        { key: 'risk_low', available_phases: [1, 2] },
        { key: 'risk_moderate', available_phases: [1, 2, 3] },
        { key: 'risk_extreme', available_phases: [] },
      ]);
    });
    await page.addScriptTag({ path: scriptPath('lobby-missions.js') });

    assert.equal(await page.locator('#mission-phase').inputValue(), '1');
    assert.equal(await page.locator('#mission-phase option[value="3"]').isDisabled(), true);
    assert.equal(await page.locator('#mission-phase').isDisabled(), false);
    assert.equal(await page.locator('#mission-start-form button').isDisabled(), false);

    await page.locator('#mission-difficulty').selectOption('risk_moderate');
    assert.equal(await page.locator('#mission-phase option[value="3"]').isDisabled(), false);

    await page.locator('#mission-difficulty').selectOption('risk_extreme');
    assert.equal(await page.locator('#mission-phase').inputValue(), '');
    assert.equal(await page.locator('#mission-phase').isDisabled(), true);
    assert.equal(await page.locator('#mission-start-form button').isDisabled(), true);
    assert.deepEqual(pageErrors, []);
  } finally {
    await page.close();
  }
});

test('loot resolution enforces capacity and closes the completion dialog', async () => {
  const page = await browser.newPage();
  const pageErrors = [];
  page.on('pageerror', (error) => pageErrors.push(error.message));

  try {
    await page.setContent(`
      <dialog id="mission-completion-dialog">
        <button id="mission-completion-continue" type="button">Continuar</button>
      </dialog>
      <main>
        <form id="mission-loot-form" data-inventory-count="2" data-inventory-capacity="3">
          <input type="checkbox" name="keep_item_ids" checked>
          <input type="checkbox" name="keep_item_ids">
          <p id="capacity-feedback" role="status"></p>
          <button id="mission-loot-submit" type="submit">Confirmar</button>
        </form>
      </main>
    `);
    await page.addScriptTag({ path: scriptPath('mission-resolution.js') });

    const dialog = page.locator('#mission-completion-dialog');
    const submit = page.locator('#mission-loot-submit');
    const feedback = page.locator('#capacity-feedback');
    const checkboxes = page.locator('input[name="keep_item_ids"]');

    assert.equal(await dialog.evaluate((element) => element.open), true);
    await page.locator('#mission-completion-continue').click();
    assert.equal(await dialog.evaluate((element) => element.open), false);
    assert.equal(await submit.isDisabled(), false);
    assert.equal(await feedback.textContent(), 'Após confirmar: 3 / 3 espaços ocupados.');

    await checkboxes.nth(1).check();
    assert.equal(await submit.isDisabled(), true);
    assert.equal(
      await feedback.textContent(),
      'A seleção ocupa 4 espaços. Libere 1 espaço(s) ou desmarque espólios.',
    );

    await checkboxes.nth(0).uncheck();
    assert.equal(await submit.isDisabled(), false);
    assert.equal(await feedback.textContent(), 'Após confirmar: 3 / 3 espaços ocupados.');
    assert.deepEqual(pageErrors, []);
  } finally {
    await page.close();
  }
});
