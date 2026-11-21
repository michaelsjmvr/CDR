(() => {
  const WORLD = { width: 2400, height: 1800 };
  const ENERGY_ZONE = [
    [773, -12], [742, 64], [751, 115], [788, 151], [914, 227], [1116, 291],
    [1462, 306], [1580, 303], [1712, 245], [1769, 118], [1778, -12],
    [1790, -63], [761, -63],
  ];
  const FOG_ZONES = [
    { poly: [[-16, 100], [-16, 79], [8, 61], [98, 70], [113, 88], [137, 167], [161, 185], [212, 182], [297, 136], [372, 121], [417, 160], [477, 248], [480, 272], [447, 278], [375, 263], [167, 260], [20, 233], [-19, 164], [-19, 103]] },
    { poly: [[212, 472], [411, 493], [474, 548], [589, 557], [604, 572], [604, 593], [556, 602], [402, 593], [309, 638], [182, 641], [164, 672], [185, 608], [191, 617], [200, 599]] },
    { poly: [[2393, 85], [2372, 85], [2257, 133], [2040, 245], [1971, 260], [1932, 278], [1899, 309], [1899, 327], [1926, 339], [2170, 354], [2179, 381], [2158, 418], [2070, 475], [1896, 542], [1860, 596], [2007, 605], [2170, 641], [2224, 663], [2224, 294], [2405, 257]] },
    { poly: [[2, 1265], [116, 1274], [110, 1349], [131, 1370], [179, 1382], [212, 1407], [219, 1485], [234, 1525], [188, 1537], [20, 1540], [-1, 1561]] },
    { poly: [[2393, 1252], [2354, 1243], [2326, 1265], [2323, 1298], [2338, 1325], [2329, 1352], [2188, 1385], [2134, 1416], [2092, 1425], [2079, 1440], [2137, 1452], [2314, 1552], [2396, 1576], [2405, 1564], [2408, 1446], [2396, 1255]] },
  ];
  const CRATERS_MAP = [
    { x: 540, y: 48, rx: 125, ry: 32, rate: 15 },
    { x: 778, y: 70, rx: 70, ry: 25, rate: 10 },
  ];
  const PUDDLES = [
    { x: 525, y: 914, rx: 112, ry: 48, phase: .2 },
    { x: 872, y: 888, rx: 132, ry: 58, phase: 1.1 },
    { x: 1504, y: 795, rx: 112, ry: 45, phase: 2 },
    { x: 875, y: 1260, rx: 148, ry: 64, phase: .7 },
    { x: 1495, y: 1290, rx: 140, ry: 62, phase: 1.8 },
    { x: 1935, y: 1355, rx: 118, ry: 58, phase: 2.6 },
    { x: 478, y: 1400, rx: 128, ry: 58, phase: 1.4 },
  ];
  const LAMPS = [
    { x: 570, y: 390 }, { x: 1840, y: 390 },
    { x: 710, y: 1430 }, { x: 1760, y: 1430 },
  ];
  const FOREGROUND = [
    { poly: [[0, 130], [470, 140], [485, 490], [0, 470]], foot: 500 },
    { poly: [[110, 710], [430, 730], [455, 1190], [390, 1290], [190, 1280], [150, 1180]], foot: 1300 },
    { poly: [[1900, 690], [2250, 690], [2290, 1220], [2190, 1290], [1990, 1250], [1900, 1160]], foot: 1300 },
    { poly: [[1210, 1370], [1810, 1370], [1830, 1640], [1250, 1650]], foot: 1660 },
    { poly: [[800, 1540], [1430, 1540], [1450, 1800], [820, 1800]], foot: 1800 },
    { poly: [[1860, 1400], [2400, 1400], [2400, 1800], [1900, 1800]], foot: 1800 },
    { poly: [[730, 345], [1690, 345], [1690, 510], [730, 510]], foot: 540 },
    { poly: [[760, 500], [850, 500], [850, 740], [760, 740]], foot: 750 },
    { poly: [[1030, 500], [1120, 500], [1120, 740], [1030, 740]], foot: 750 },
    { poly: [[1350, 500], [1440, 500], [1440, 740], [1350, 740]], foot: 750 },
    { poly: [[1620, 500], [1710, 500], [1710, 740], [1620, 740]], foot: 750 },
    { poly: [[750, 820], [850, 820], [850, 1110], [750, 1110]], foot: 1120 },
    { poly: [[1000, 820], [1100, 820], [1100, 1110], [1000, 1110]], foot: 1120 },
    { poly: [[1320, 820], [1420, 820], [1420, 1110], [1320, 1110]], foot: 1120 },
    { poly: [[1630, 820], [1730, 820], [1730, 1110], [1630, 1110]], foot: 1120 },
  ];

  function createTerminalVilarEffects(mapImage) {
    let ctx;
    const FOG = { scale: .25, ready: false };
    const EN = { ready: false, strikes: [], nextStrike: .9, sparks: [], smoke: [], lastT: 0 };

    function makeCanvas(width, height) {
      const canvas = document.createElement('canvas');
      canvas.width = Math.max(1, Math.round(width));
      canvas.height = Math.max(1, Math.round(height));
      return canvas;
    }

    function hash2(x, y, seed) {
      let hash = Math.imul(x, 374761393) ^ Math.imul(y, 668265263) ^ Math.imul(seed, 1442695041);
      hash = Math.imul(hash ^ (hash >>> 13), 1274126177);
      return ((hash ^ (hash >>> 16)) >>> 0) / 4294967296;
    }

    function periodicNoise(x, y, period, seed) {
      const xi = Math.floor(x);
      const yi = Math.floor(y);
      const xf = x - xi;
      const yf = y - yi;
      const u = xf * xf * (3 - 2 * xf);
      const v = yf * yf * (3 - 2 * yf);
      const xa = ((xi % period) + period) % period;
      const xb = (xa + 1) % period;
      const ya = ((yi % period) + period) % period;
      const yb = (ya + 1) % period;
      const a = hash2(xa, ya, seed);
      const b = hash2(xb, ya, seed);
      const c = hash2(xa, yb, seed);
      const d = hash2(xb, yb, seed);
      return a + (b - a) * u + (c - a) * v + (a - b - c + d) * u * v;
    }

    function pointInPoly(x, y, points) {
      let inside = false;
      for (let i = 0, j = points.length - 1; i < points.length; j = i, i += 1) {
        const a = points[i];
        const b = points[j];
        if (((a[1] > y) !== (b[1] > y))
          && x < (b[0] - a[0]) * (y - a[1]) / (b[1] - a[1]) + a[0]) {
          inside = !inside;
        }
      }
      return inside;
    }

    function featherCanvas(canvas, radius, passes) {
      const context = canvas.getContext('2d');
      const image = context.getImageData(0, 0, canvas.width, canvas.height);
      const data = image.data;
      const count = canvas.width * canvas.height;
      let alpha = new Float32Array(count);
      let temporary = new Float32Array(count);
      for (let i = 0; i < count; i += 1) alpha[i] = data[i * 4 + 3];
      const windowSize = radius * 2 + 1;
      for (let pass = 0; pass < passes; pass += 1) {
        for (let y = 0; y < canvas.height; y += 1) {
          const row = y * canvas.width;
          let sum = 0;
          for (let k = -radius; k <= radius; k += 1) {
            sum += alpha[row + Math.min(canvas.width - 1, Math.max(0, k))];
          }
          for (let x = 0; x < canvas.width; x += 1) {
            temporary[row + x] = sum / windowSize;
            sum += alpha[row + Math.min(canvas.width - 1, x + radius + 1)]
              - alpha[row + Math.max(0, x - radius)];
          }
        }
        for (let x = 0; x < canvas.width; x += 1) {
          let sum = 0;
          for (let k = -radius; k <= radius; k += 1) {
            sum += temporary[Math.min(canvas.height - 1, Math.max(0, k)) * canvas.width + x];
          }
          for (let y = 0; y < canvas.height; y += 1) {
            alpha[y * canvas.width + x] = sum / windowSize;
            sum += temporary[Math.min(canvas.height - 1, y + radius + 1) * canvas.width + x]
              - temporary[Math.max(0, y - radius) * canvas.width + x];
          }
        }
      }
      for (let i = 0; i < count; i += 1) {
        data[i * 4] = 255;
        data[i * 4 + 1] = 255;
        data[i * 4 + 2] = 255;
        data[i * 4 + 3] = alpha[i];
      }
      context.putImageData(image, 0, 0);
    }

    function softCanvas(source, levels) {
      let canvas = source;
      for (let i = 0; i < levels; i += 1) {
        const next = makeCanvas(Math.max(2, canvas.width >> 1), Math.max(2, canvas.height >> 1));
        const nextContext = next.getContext('2d');
        nextContext.imageSmoothingEnabled = true;
        nextContext.drawImage(canvas, 0, 0, next.width, next.height);
        canvas = next;
      }
      for (let i = levels - 1; i >= 0; i -= 1) {
        const width = i === 0 ? source.width : Math.round(source.width / (1 << i));
        const height = i === 0 ? source.height : Math.round(source.height / (1 << i));
        const next = makeCanvas(width, height);
        const nextContext = next.getContext('2d');
        nextContext.imageSmoothingEnabled = true;
        nextContext.drawImage(canvas, 0, 0, width, height);
        canvas = next;
      }
      return canvas;
    }

    function buildFog() {
      FOG.w = Math.round(WORLD.width * FOG.scale);
      FOG.h = Math.round(WORLD.height * FOG.scale);
      const mask = makeCanvas(FOG.w, FOG.h);
      const maskContext = mask.getContext('2d');
      maskContext.fillStyle = '#fff';
      for (const zone of FOG_ZONES) {
        maskContext.beginPath();
        zone.poly.forEach(([x, y], index) => {
          if (index) maskContext.lineTo(x * FOG.scale, y * FOG.scale);
          else maskContext.moveTo(x * FOG.scale, y * FOG.scale);
        });
        maskContext.closePath();
        maskContext.fill();
      }
      featherCanvas(mask, 7, 3);
      FOG.mask = mask;

      const size = 256;
      const tile = makeCanvas(size, size);
      const tileContext = tile.getContext('2d');
      const image = tileContext.createImageData(size, size);
      const data = image.data;
      for (let y = 0; y < size; y += 1) {
        for (let x = 0; x < size; x += 1) {
          let noise = 0;
          let amplitude = .5;
          let total = 0;
          for (let octave = 0; octave < 4; octave += 1) {
            const cells = 4 << octave;
            noise += amplitude * periodicNoise(x / size * cells, y / size * cells, cells, 11 + octave * 7);
            total += amplitude;
            amplitude *= .5;
          }
          noise /= total;
          let alpha = Math.max(0, Math.min(1, (noise - .36) / .46));
          alpha = alpha * alpha * (3 - 2 * alpha);
          const index = (y * size + x) * 4;
          data[index] = 176;
          data[index + 1] = 172;
          data[index + 2] = 206;
          data[index + 3] = alpha * 255;
        }
      }
      tileContext.putImageData(image, 0, 0);
      FOG.layer = makeCanvas(FOG.w, FOG.h);
      FOG.layerContext = FOG.layer.getContext('2d');
      FOG.pattern = FOG.layerContext.createPattern(tile, 'repeat');
      FOG.ready = true;
    }

    function drawFog(time) {
      if (!FOG.ready) return;
      const layerContext = FOG.layerContext;
      layerContext.setTransform(1, 0, 0, 1, 0, 0);
      layerContext.globalCompositeOperation = 'source-over';
      layerContext.globalAlpha = 1;
      layerContext.clearRect(0, 0, FOG.w, FOG.h);
      const layers = [
        { scale: 1.75, vx: 4, vy: .9, rotation: 0, alpha: .62, phase: 0 },
        { scale: 1.05, vx: -3.2, vy: 1.6, rotation: .35, alpha: .50, phase: 1.7 },
        { scale: .62, vx: 6, vy: -.8, rotation: -.22, alpha: .32, phase: 3.1 },
      ];
      for (const layer of layers) {
        const cosine = Math.cos(layer.rotation) * layer.scale;
        const sine = Math.sin(layer.rotation) * layer.scale;
        layerContext.setTransform(
          cosine, sine, -sine, cosine,
          time * layer.vx, time * layer.vy + Math.sin(time * .17 + layer.phase) * 7,
        );
        layerContext.globalAlpha = layer.alpha * (.9 + .1 * Math.sin(time * .29 + layer.phase * 2));
        layerContext.fillStyle = FOG.pattern;
        layerContext.fillRect(-4000, -4000, 8000, 8000);
      }
      layerContext.setTransform(1, 0, 0, 1, 0, 0);
      layerContext.globalAlpha = 1;
      layerContext.globalCompositeOperation = 'destination-in';
      layerContext.drawImage(FOG.mask, 0, 0);
      ctx.save();
      ctx.globalCompositeOperation = 'screen';
      ctx.globalAlpha = .5;
      ctx.imageSmoothingEnabled = true;
      ctx.imageSmoothingQuality = 'high';
      ctx.drawImage(FOG.layer, 0, 0, WORLD.width, WORLD.height);
      ctx.restore();
    }

    function buildEnergy() {
      const mapWidth = mapImage.naturalWidth;
      const mapHeight = mapImage.naturalHeight;
      const scaleX = WORLD.width / mapWidth;
      const scaleY = WORLD.height / mapHeight;
      const xCoordinates = ENERGY_ZONE.map(([x]) => x / scaleX);
      const yCoordinates = ENERGY_ZONE.map(([, y]) => y / scaleY);
      const x0 = Math.max(0, Math.floor(Math.min(...xCoordinates)) - 8);
      const x1 = Math.min(mapWidth, Math.ceil(Math.max(...xCoordinates)) + 8);
      const y0 = 0;
      const y1 = Math.min(mapHeight, Math.ceil(Math.max(...yCoordinates)) + 8);
      const width = x1 - x0;
      const height = y1 - y0;
      Object.assign(EN, {
        x0, y0, w: width, h: height, sx: scaleX, sy: scaleY,
        zone: ENERGY_ZONE.map(([x, y]) => [x / scaleX - x0, y / scaleY - y0]),
      });
      EN.craters = CRATERS_MAP.map((crater, index) => ({
        ...crater, i: index, x: crater.x - x0, y: crater.y - y0, points: [],
      }));
      EN.emit = EN.craters.map(() => 0);
      EN.smokeEmit = EN.craters.map(() => 0);
      const zoneMask = makeCanvas(width, height);
      const zoneContext = zoneMask.getContext('2d');
      zoneContext.fillStyle = '#fff';
      zoneContext.beginPath();
      EN.zone.forEach(([x, y], index) => {
        if (index) zoneContext.lineTo(x, y);
        else zoneContext.moveTo(x, y);
      });
      zoneContext.closePath();
      zoneContext.fill();
      featherCanvas(zoneMask, 4, 3);
      EN.zoneMask = zoneMask;

      const source = makeCanvas(width, height);
      const sourceContext = source.getContext('2d');
      sourceContext.drawImage(mapImage, x0, y0, width, height, 0, 0, width, height);
      const pixels = sourceContext.getImageData(0, 0, width, height).data;
      const bolt = sourceContext.createImageData(width, height);
      const core = sourceContext.createImageData(width, height);
      const boltData = bolt.data;
      const coreData = core.data;
      const points = [];
      for (let y = 0; y < height; y += 1) {
        for (let x = 0; x < width; x += 1) {
          if (!pointInPoly(x, y, EN.zone)) continue;
          const index = (y * width + x) * 4;
          const red = pixels[index];
          const green = pixels[index + 1];
          const blue = pixels[index + 2];
          if (blue > 140 && red > 105 && blue > green * 1.35 && red > green * 1.15 && red + blue > 300) {
            boltData[index] = Math.min(255, red * 1.05);
            boltData[index + 1] = green * .85;
            boltData[index + 2] = Math.min(255, blue * 1.12);
            boltData[index + 3] = Math.min(255, (red + blue - 290) * 2.4);
          }
          if (blue > 200 && red > 170 && green > 110) {
            coreData[index] = 255;
            coreData[index + 1] = Math.min(255, green + 70);
            coreData[index + 2] = 255;
            coreData[index + 3] = Math.min(255, (green - 100) * 4.5);
            if ((x * 7 + y * 13) % 5 === 0) points.push({ x, y });
          }
        }
      }
      EN.bolt = makeCanvas(width, height);
      EN.bolt.getContext('2d').putImageData(bolt, 0, 0);
      EN.core = makeCanvas(width, height);
      EN.core.getContext('2d').putImageData(core, 0, 0);
      EN.glowTight = softCanvas(EN.bolt, 2);
      EN.glowWide = softCanvas(EN.bolt, 4);
      EN.points = points;
      for (const crater of EN.craters) {
        crater.points = points.filter((point) => (
          ((point.x - crater.x) / (crater.rx * 1.3)) ** 2
          + ((point.y - crater.y) / (crater.ry * 2.4)) ** 2 < 1
        ));
      }
      EN.layer = makeCanvas(width, height);
      EN.layerContext = EN.layer.getContext('2d');
      EN.ready = true;
    }

    function seededRandom(seed) {
      return function nextRandom() {
        seed |= 0;
        seed = seed + 0x6D2B79F5 | 0;
        let value = Math.imul(seed ^ seed >>> 15, 1 | seed);
        value = value + Math.imul(value ^ value >>> 7, 61 | value) ^ value;
        return ((value ^ value >>> 14) >>> 0) / 4294967296;
      };
    }

    function boltPath(random, x0, y0, x1, y1, displacement) {
      let points = [[x0, y0], [x1, y1]];
      let offset = displacement;
      for (let pass = 0; pass < 4; pass += 1) {
        const nextPoints = [points[0]];
        for (let index = 1; index < points.length; index += 1) {
          const a = points[index - 1];
          const b = points[index];
          const dx = b[0] - a[0];
          const dy = b[1] - a[1];
          const length = Math.hypot(dx, dy) || 1;
          const amount = (random() - .5) * 2 * offset;
          nextPoints.push([
            (a[0] + b[0]) / 2 - dy / length * amount,
            (a[1] + b[1]) / 2 + dx / length * amount,
          ], b);
        }
        points = nextPoints;
        offset *= .55;
      }
      return points;
    }

    function strokeBolt(context, points, alpha) {
      if (alpha <= .01) return;
      context.lineCap = 'round';
      context.lineJoin = 'round';
      const passes = [[8, .10, '#9b3bff'], [4, .28, '#c56bff'], [1.9, .72, '#f0c8ff'], [.9, 1, '#fff']];
      for (const [lineWidth, opacity, color] of passes) {
        context.globalAlpha = Math.min(1, opacity * alpha * 1.2);
        context.strokeStyle = color;
        context.lineWidth = lineWidth;
        context.beginPath();
        points.forEach(([x, y], index) => index ? context.lineTo(x, y) : context.moveTo(x, y));
        context.stroke();
      }
    }

    function spawnStrike(time) {
      const crater = EN.craters[Math.random() < .62 ? 0 : 1];
      const origin = crater.points.length
        ? crater.points[Math.floor(Math.random() * crater.points.length)]
        : { x: crater.x, y: crater.y };
      const bolts = [];
      const count = 2 + Math.floor(Math.random() * 2);
      for (let index = 0; index < count; index += 1) {
        const angle = Math.random() < .6
          ? -Math.PI / 2 + (Math.random() - .5) * 1.5
          : Math.atan2(origin.y - crater.y, origin.x - crater.x) + (Math.random() - .5) * 1.1;
        let length = 55 + Math.random() * 115;
        let targetX = origin.x + Math.cos(angle) * length;
        let targetY = origin.y + Math.sin(angle) * length;
        let tries = 0;
        while (tries++ < 6 && !pointInPoly(targetX, targetY, EN.zone)) {
          length *= .72;
          targetX = origin.x + Math.cos(angle) * length;
          targetY = origin.y + Math.sin(angle) * length;
        }
        bolts.push({ x0: origin.x, y0: origin.y, x1: targetX, y1: targetY, weight: index === 0 ? 1 : .65 });
      }
      EN.strikes.push({ t0: time, duration: .3 + Math.random() * .3, seed: Math.random() * 100, id: (Math.random() * 1e9) | 0, bolts });
    }

    function updateStrikes(time) {
      if (time >= EN.nextStrike) {
        spawnStrike(time);
        EN.nextStrike = time + 1 + Math.random() * 2.4;
      }
      let flash = 0;
      for (let index = EN.strikes.length - 1; index >= 0; index -= 1) {
        const strike = EN.strikes[index];
        const age = time - strike.t0;
        if (age > strike.duration || age < 0) {
          EN.strikes.splice(index, 1);
          continue;
        }
        flash = Math.max(flash, Math.pow(1 - age / strike.duration, .7) * (.55 + .45 * Math.sin(age * 70 + strike.seed)));
      }
      return Math.max(0, flash);
    }

    function drawStrikes(context, time) {
      for (const strike of EN.strikes) {
        const age = time - strike.t0;
        const envelope = Math.pow(1 - age / strike.duration, .6) * (.6 + .4 * Math.sin(age * 70 + strike.seed));
        if (envelope <= 0) continue;
        const step = Math.floor(age * 22);
        strike.bolts.forEach((bolt, boltIndex) => {
          const random = seededRandom(strike.id + step * 131 + boltIndex * 17);
          const length = Math.hypot(bolt.x1 - bolt.x0, bolt.y1 - bolt.y0);
          const points = boltPath(random, bolt.x0, bolt.y0, bolt.x1, bolt.y1, length * .22);
          strokeBolt(context, points, envelope * bolt.weight);
          for (let branch = 0; branch < 2; branch += 1) {
            const point = points[2 + Math.floor(random() * Math.max(1, points.length - 4))];
            const angle = Math.atan2(bolt.y1 - bolt.y0, bolt.x1 - bolt.x0) + (random() - .5) * 1.8;
            const branchLength = 18 + random() * 40;
            strokeBolt(context, boltPath(
              random, point[0], point[1],
              point[0] + Math.cos(angle) * branchLength,
              point[1] + Math.sin(angle) * branchLength,
              branchLength * .25,
            ), envelope * bolt.weight * .6);
          }
        });
      }
    }

    function drawMicroArcs(context, time, intensity) {
      if (!EN.points.length) return;
      const random = seededRandom(Math.floor(time * 14) * 7919 + 13);
      for (let index = 0; index < 6; index += 1) {
        const keep = random() < .55;
        const point = EN.points[Math.floor(random() * EN.points.length)];
        const angle = random() * Math.PI * 2;
        const length = 10 + random() * 22;
        if (keep) {
          strokeBolt(context, boltPath(
            random, point.x, point.y,
            point.x + Math.cos(angle) * length,
            point.y + Math.sin(angle) * length,
            length * .35,
          ), .55 * Math.min(1, intensity));
        }
      }
    }

    function updateParticles(delta, intensity) {
      EN.craters.forEach((crater) => {
        EN.emit[crater.i] += delta * crater.rate * (.6 + intensity);
        while (EN.emit[crater.i] >= 1) {
          EN.emit[crater.i] -= 1;
          if (crater.points.length && EN.sparks.length < 180) {
            const point = crater.points[Math.floor(Math.random() * crater.points.length)];
            EN.sparks.push({
              x: point.x + (Math.random() - .5) * 5,
              y: point.y,
              vx: (Math.random() - .5) * 18,
              vy: -(14 + Math.random() * 36),
              age: 0,
              max: .8 + Math.random() * 1.4,
              size: .8 + Math.random() * 1.3,
            });
          }
        }
        EN.smokeEmit[crater.i] += delta * 2.2;
        while (EN.smokeEmit[crater.i] >= 1) {
          EN.smokeEmit[crater.i] -= 1;
          if (EN.smoke.length < 40) {
            EN.smoke.push({
              x: crater.x + (Math.random() - .5) * crater.rx * 1.3,
              y: crater.y + (Math.random() - .5) * crater.ry * .9,
              vx: (Math.random() - .5) * 5,
              vy: -(5 + Math.random() * 9),
              age: 0,
              max: 2.6 + Math.random() * 2.2,
              radius: 11 + Math.random() * 13,
            });
          }
        }
      });
      for (const particles of [EN.sparks, EN.smoke]) {
        for (let index = particles.length - 1; index >= 0; index -= 1) {
          const particle = particles[index];
          particle.age += delta;
          if (particle.age > particle.max) {
            particles.splice(index, 1);
            continue;
          }
          particle.x += particle.vx * delta;
          particle.y += particle.vy * delta;
          particle.vx += (Math.random() - .5) * 30 * delta;
        }
      }
    }

    function drawParticles(context) {
      for (const particle of EN.smoke) {
        const progress = particle.age / particle.max;
        const alpha = Math.sin(Math.PI * progress) * .085;
        const radius = particle.radius * (1 + progress * .9);
        const gradient = context.createRadialGradient(particle.x, particle.y, 0, particle.x, particle.y, radius);
        gradient.addColorStop(0, `rgba(165,85,240,${alpha})`);
        gradient.addColorStop(1, 'rgba(110,40,190,0)');
        context.globalAlpha = 1;
        context.fillStyle = gradient;
        context.fillRect(particle.x - radius, particle.y - radius, radius * 2, radius * 2);
      }
      for (const particle of EN.sparks) {
        const progress = particle.age / particle.max;
        const alpha = (1 - progress) * (.6 + .4 * Math.sin(particle.age * 40 + particle.x));
        context.globalAlpha = Math.max(0, alpha);
        context.fillStyle = '#f6d6ff';
        context.fillRect(particle.x - particle.size / 2, particle.y - particle.size / 2, particle.size, particle.size);
        context.globalAlpha = Math.max(0, alpha * .35);
        context.fillStyle = '#c070ff';
        context.fillRect(particle.x - particle.size, particle.y - particle.size, particle.size * 2, particle.size * 2);
      }
    }

    function drawEnergy(time) {
      if (!EN.ready) return;
      const delta = Math.max(0, Math.min(.05, time - EN.lastT));
      EN.lastT = time;
      const layerContext = EN.layerContext;
      layerContext.setTransform(1, 0, 0, 1, 0, 0);
      layerContext.globalAlpha = 1;
      layerContext.globalCompositeOperation = 'source-over';
      layerContext.clearRect(0, 0, EN.w, EN.h);
      layerContext.globalCompositeOperation = 'lighter';
      const breath = .5 + .5 * Math.sin(time * 1.9);
      const flicker = .5 + .5 * Math.sin(time * 7.3 + Math.sin(time * 2.1) * 2);
      const flash = updateStrikes(time);
      const intensity = .62 + .18 * breath + .10 * flicker + .55 * flash;
      for (const crater of EN.craters) {
        const radius = crater.rx * 1.3;
        layerContext.save();
        layerContext.translate(crater.x, crater.y);
        layerContext.scale(1, .55);
        const gradient = layerContext.createRadialGradient(0, 0, 2, 0, 0, radius);
        gradient.addColorStop(0, `rgba(175,75,255,${.09 * intensity})`);
        gradient.addColorStop(.5, `rgba(130,45,215,${.19 * intensity})`);
        gradient.addColorStop(1, 'rgba(90,30,170,0)');
        layerContext.fillStyle = gradient;
        layerContext.fillRect(-radius, -radius, radius * 2, radius * 2);
        layerContext.restore();
      }
      layerContext.globalAlpha = Math.min(1, .55 * intensity);
      layerContext.drawImage(EN.glowWide, 0, 0);
      layerContext.globalAlpha = Math.min(1, .65 * intensity);
      layerContext.drawImage(EN.glowTight, 0, 0);
      layerContext.globalAlpha = Math.min(1, .5 + .35 * Math.min(1, intensity));
      layerContext.drawImage(EN.bolt, 0, 0);
      EN.craters.forEach((crater, craterIndex) => {
        for (let index = 0; index < 2; index += 1) {
          const phase = (time * .42 + craterIndex * .37 + index * .5) % 1;
          const radius = .12 + phase * 1.55;
          const innerRadius = Math.max(0, radius - .3);
          layerContext.save();
          layerContext.beginPath();
          layerContext.ellipse(crater.x, crater.y, crater.rx * radius, crater.rx * radius * .9, 0, 0, Math.PI * 2);
          layerContext.moveTo(crater.x + crater.rx * innerRadius, crater.y);
          layerContext.ellipse(crater.x, crater.y, crater.rx * innerRadius, crater.rx * innerRadius * .9, 0, 0, Math.PI * 2);
          layerContext.clip('evenodd');
          layerContext.globalAlpha = Math.sin(Math.PI * phase) * .9;
          layerContext.drawImage(EN.core, 0, 0);
          layerContext.globalAlpha = Math.sin(Math.PI * phase) * .55;
          layerContext.drawImage(EN.bolt, 0, 0);
          layerContext.restore();
        }
      });
      layerContext.globalAlpha = Math.min(1, .25 + .45 * flicker * Math.min(1, intensity) + .3 * flash);
      layerContext.drawImage(EN.core, 0, 0);
      drawStrikes(layerContext, time);
      drawMicroArcs(layerContext, time, intensity);
      updateParticles(delta, intensity);
      drawParticles(layerContext);
      layerContext.setTransform(1, 0, 0, 1, 0, 0);
      layerContext.globalAlpha = 1;
      layerContext.globalCompositeOperation = 'destination-in';
      layerContext.drawImage(EN.zoneMask, 0, 0);
      ctx.save();
      ctx.globalCompositeOperation = 'screen';
      ctx.imageSmoothingEnabled = true;
      ctx.imageSmoothingQuality = 'high';
      ctx.drawImage(EN.layer, EN.x0 * EN.sx, EN.y0 * EN.sy, EN.w * EN.sx, EN.h * EN.sy);
      ctx.restore();
    }

    function drawWater(time) {
      for (const puddle of PUDDLES) {
        ctx.save();
        ctx.translate(puddle.x, puddle.y);
        ctx.rotate(Math.sin(time * .35 + puddle.phase) * .035);
        ctx.globalCompositeOperation = 'screen';
        const shimmer = .72 + .28 * Math.sin(time * 2.1 + puddle.phase);
        const glow = ctx.createRadialGradient(-puddle.rx * .12, -puddle.ry * .2, 3, 0, 0, puddle.rx * 1.05);
        glow.addColorStop(0, `rgba(220,155,255,${.28 * shimmer})`);
        glow.addColorStop(.38, `rgba(147,67,211,${.19 * shimmer})`);
        glow.addColorStop(.78, 'rgba(80,47,126,.10)');
        glow.addColorStop(1, 'rgba(80,47,126,0)');
        ctx.fillStyle = glow;
        ctx.beginPath();
        ctx.ellipse(0, 0, puddle.rx, puddle.ry, 0, 0, Math.PI * 2);
        ctx.fill();
        for (let index = 0; index < 5; index += 1) {
          const x = Math.sin(time * .75 + index * 2.4 + puddle.phase) * puddle.rx * .48;
          const y = Math.cos(time * .6 + index * 1.7 + puddle.phase) * puddle.ry * .38;
          ctx.strokeStyle = `rgba(${index % 2 ? 185 : 235},${index % 2 ? 132 : 205},255,${.12 + .10 * shimmer})`;
          ctx.lineWidth = 2 + (index % 2);
          ctx.beginPath();
          ctx.moveTo(x - puddle.rx * .16, y);
          ctx.quadraticCurveTo(x, y - 4, x + puddle.rx * .17, y + Math.sin(time * 2 + index) * 3);
          ctx.stroke();
        }
        for (let index = 0; index < 3; index += 1) {
          const phase = (time * .42 + index / 3 + puddle.phase * .13) % 1;
          const x = Math.sin(index * 8.3 + puddle.phase) * puddle.rx * .42;
          const y = Math.cos(index * 4.1 + puddle.phase) * puddle.ry * .36;
          ctx.strokeStyle = `rgba(226,195,255,${.34 * (1 - phase)})`;
          ctx.lineWidth = 1.8;
          ctx.beginPath();
          ctx.ellipse(x, y, 4 + phase * puddle.rx * .31, 2 + phase * puddle.ry * .34, 0, 0, Math.PI * 2);
          ctx.stroke();
        }
        ctx.restore();
      }
    }

    function drawLights(time) {
      ctx.save();
      ctx.globalCompositeOperation = 'screen';
      LAMPS.forEach((lamp, index) => {
        const flicker = .78 + .16 * Math.sin(time * 3.4 + index * 2) + .06 * Math.sin(time * 11 + index);
        const radius = 230 * flicker;
        const gradient = ctx.createRadialGradient(lamp.x, lamp.y, 4, lamp.x, lamp.y, radius);
        gradient.addColorStop(0, `rgba(255,220,145,${.23 * flicker})`);
        gradient.addColorStop(.35, `rgba(255,190,100,${.09 * flicker})`);
        gradient.addColorStop(1, 'rgba(255,190,100,0)');
        ctx.fillStyle = gradient;
        ctx.beginPath();
        ctx.ellipse(lamp.x, lamp.y, radius, radius * .72, 0, 0, Math.PI * 2);
        ctx.fill();
      });
      const neon = ctx.createRadialGradient(1200, 470, 20, 1200, 470, 650);
      neon.addColorStop(0, 'rgba(204,70,255,.13)');
      neon.addColorStop(1, 'rgba(204,70,255,0)');
      ctx.fillStyle = neon;
      ctx.fillRect(450, 250, 1500, 900);
      ctx.restore();
    }

    function drawRain(time) {
      ctx.save();
      ctx.globalCompositeOperation = 'screen';
      ctx.lineCap = 'round';
      for (let index = 0; index < 190; index += 1) {
        const depth = (index % 7) / 6;
        const speed = 520 + depth * 420;
        const x = (index * 173.7 + time * (95 + depth * 42)) % (WORLD.width + 180) - 90;
        const y = (index * 97.3 + time * speed) % (WORLD.height + 120) - 60;
        const alpha = .10 + depth * .14;
        ctx.strokeStyle = `rgba(205,218,255,${alpha})`;
        ctx.lineWidth = .75 + depth * .45;
        ctx.beginPath();
        ctx.moveTo(x, y);
        ctx.lineTo(x - 8 - depth * 5, y + 22 + depth * 12);
        ctx.stroke();
      }
      ctx.restore();
    }

    function drawOcclusion(playerY) {
      if (!mapImage.complete || !mapImage.naturalWidth) return;
      for (const structure of FOREGROUND) {
        if (playerY < structure.foot && playerY > structure.foot - 420) {
          ctx.save();
          ctx.beginPath();
          structure.poly.forEach(([x, y], index) => index ? ctx.lineTo(x, y) : ctx.moveTo(x, y));
          ctx.closePath();
          ctx.clip();
          ctx.globalAlpha = .43;
          ctx.drawImage(mapImage, 0, 0, WORLD.width, WORLD.height);
          ctx.restore();
        }
      }
    }

    function drawGround(targetContext, camera, time) {
      ctx = targetContext;
      ctx.save();
      ctx.translate(-camera.x, -camera.y);
      drawWater(time);
      drawEnergy(time);
      drawLights(time);
      ctx.restore();
    }

    function drawAtmosphere(targetContext, camera, playerY, time) {
      ctx = targetContext;
      ctx.save();
      ctx.translate(-camera.x, -camera.y);
      drawFog(time);
      drawOcclusion(playerY);
      drawRain(time);
      ctx.restore();
    }

    buildFog();
    if (mapImage.complete && mapImage.naturalWidth) buildEnergy();
    else mapImage.addEventListener('load', buildEnergy, { once: true });

    return { drawGround, drawAtmosphere };
  }

  window.createTerminalVilarEffects = createTerminalVilarEffects;
})();
