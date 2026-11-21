(() => {
  const palettes = {
    guardian: { cloth: '#8c302e', metal: '#c5a56a', light: '#edc77c', weapon: '#d8d5c8' },
    mage: { cloth: '#493a72', metal: '#9d83d3', light: '#bca2ff', weapon: '#c3b9eb' },
    archer: { cloth: '#315742', metal: '#9c9b65', light: '#a4d58c', weapon: '#c8bb8b' },
    'rune-blade': { cloth: '#31516a', metal: '#83b8ca', light: '#9be2e5', weapon: '#d2eff0' },
  };
  const classPalettes = {
    ash_weaver: 'mage',
    wild_scout: 'archer',
    rune_blade: 'rune-blade',
  };

  function paintPortrait(canvas) {
    const context = canvas.getContext('2d');
    if (!context) return;
    const bounds = canvas.getBoundingClientRect();
    if (!bounds.width || !bounds.height) return;
    const ratio = Math.min(window.devicePixelRatio || 1, 2);
    canvas.width = Math.round(bounds.width * ratio);
    canvas.height = Math.round(bounds.height * ratio);
    context.setTransform(ratio, 0, 0, ratio, 0, 0);
    const w = bounds.width;
    const h = bounds.height;
    const paletteKey = classPalettes[canvas.dataset.classId] || canvas.dataset.classId;
    const palette = palettes[paletteKey] || palettes.guardian;
    const cx = w / 2;
    const cy = h * 0.54;

    const background = context.createLinearGradient(0, 0, w, h);
    background.addColorStop(0, '#1b2029');
    background.addColorStop(1, '#090c12');
    context.fillStyle = background;
    context.fillRect(0, 0, w, h);
    const glow = context.createRadialGradient(cx, h * .38, 2, cx, h * .42, h * .72);
    glow.addColorStop(0, `${palette.light}33`);
    glow.addColorStop(1, 'transparent');
    context.fillStyle = glow;
    context.fillRect(0, 0, w, h);

    context.strokeStyle = `${palette.metal}45`;
    context.lineWidth = 1;
    context.beginPath();
    context.ellipse(cx, h * .88, w * .36, h * .075, 0, 0, Math.PI * 2);
    context.stroke();
    context.fillStyle = `${palette.light}18`;
    context.beginPath();
    context.ellipse(cx, h * .88, w * .26, h * .035, 0, 0, Math.PI * 2);
    context.fill();

    // Retrato ilustrativo provisório; a arte final do personagem será integrada depois.
    context.fillStyle = '#07090d99';
    context.beginPath();
    context.ellipse(cx, cy + h * .25, w * .29, h * .31, 0, 0, Math.PI * 2);
    context.fill();
    context.fillStyle = palette.cloth;
    context.beginPath();
    context.moveTo(cx - w * .12, cy + h * .02);
    context.lineTo(cx - w * .29, h * .9);
    context.quadraticCurveTo(cx, h * .83, cx + w * .28, h * .9);
    context.lineTo(cx + w * .11, cy + h * .02);
    context.closePath();
    context.fill();
    context.fillStyle = palette.metal;
    context.fillRect(cx - w * .14, cy + h * .19, w * .28, h * .055);
    context.fillStyle = '#d0a77d';
    context.beginPath();
    context.ellipse(cx, cy - h * .12, w * .14, h * .17, 0, 0, Math.PI * 2);
    context.fill();
    context.fillStyle = '#241e1c';
    context.beginPath();
    context.arc(cx, cy - h * .2, w * .15, Math.PI, Math.PI * 2);
    context.lineTo(cx + w * .12, cy - h * .17);
    context.lineTo(cx - w * .13, cy - h * .17);
    context.fill();
    context.fillStyle = palette.metal;
    context.beginPath();
    context.moveTo(cx - w * .18, cy - h * .19);
    context.lineTo(cx, cy - h * .34);
    context.lineTo(cx + w * .18, cy - h * .19);
    context.lineTo(cx + w * .13, cy - h * .12);
    context.lineTo(cx - w * .13, cy - h * .12);
    context.closePath();
    context.fill();
    context.fillStyle = palette.light;
    context.fillRect(cx - w * .105, cy - h * .13, w * .21, h * .018);

    context.save();
    context.translate(cx + w * .21, cy + h * .08);
    context.rotate(-.28);
    context.fillStyle = palette.weapon;
    context.fillRect(-w * .018, -h * .36, w * .036, h * .42);
    context.fillStyle = palette.metal;
    context.fillRect(-w * .07, h * .035, w * .14, h * .04);
    context.restore();
    context.fillStyle = '#d9c28f';
    context.font = '9px sans-serif';
    context.textAlign = 'center';
    context.fillText('✦', cx, h * .15);
  }

  const portraits = [...document.querySelectorAll('.character-portrait-canvas, .lobby-avatar-canvas')];
  portraits.forEach(paintPortrait);
  if ('ResizeObserver' in window) {
    const observer = new ResizeObserver((entries) => entries.forEach(({ target }) => paintPortrait(target)));
    portraits.forEach((canvas) => observer.observe(canvas));
  } else {
    window.addEventListener('resize', () => portraits.forEach(paintPortrait));
  }
})();
