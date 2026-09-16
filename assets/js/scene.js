/* ============================================================
   CoolIn hero scene
   three.js: drifting air currents (cool blue over warm orange)
   plus a fine particle field. Deliberately slow and quiet.

   three.js is ~600kb, so it is only fetched when it will actually be
   seen: a wide viewport, motion allowed, and a canvas on the page.
   Phones and reduced motion users get the CSS gradient hero instead,
   which keeps Largest Contentful Paint honest.
   ============================================================ */
(function () {
  var canvas = document.getElementById('scene');
  if (!canvas) return;

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var narrow = window.matchMedia('(max-width: 899px)').matches;
  var saveData = navigator.connection && navigator.connection.saveData;
  if (reduced || narrow || saveData) { canvas.remove(); return; }

  var s = document.createElement('script');
  s.src = 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js';
  s.async = true;
  s.onload = function () { buildScene(); };
  s.onerror = function () { canvas.remove(); };

  // wait until the browser is idle so the library never competes with first paint
  if ('requestIdleCallback' in window) {
    requestIdleCallback(function () { document.head.appendChild(s); }, { timeout: 2500 });
  } else {
    setTimeout(function () { document.head.appendChild(s); }, 600);
  }
})();

function buildScene() {
  var canvas = document.getElementById('scene');
  if (!canvas || typeof THREE === 'undefined') return;

  var reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  var COOL = new THREE.Color('#5CB8DC');
  var WARM = new THREE.Color('#E4632C');
  var DEEP = new THREE.Color('#0C2A39');

  var renderer = new THREE.WebGLRenderer({ canvas: canvas, alpha: true, antialias: true });
  renderer.setClearColor(0x000000, 0);
  renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 1.8));

  var scene = new THREE.Scene();
  scene.fog = new THREE.FogExp2(0x0c2a39, 0.0072);

  var camera = new THREE.PerspectiveCamera(52, 1, 1, 400);
  camera.position.set(0, 0, 62);

  var group = new THREE.Group();
  scene.add(group);

  /* ---------- flowing currents ---------- */
  var LINES = 30;
  var SEGS = 140;
  var SPAN = 150;
  var lines = [];

  for (var i = 0; i < LINES; i++) {
    var t = i / (LINES - 1);
    var positions = new Float32Array((SEGS + 1) * 3);
    var colors = new Float32Array((SEGS + 1) * 3);

    // cool at the top of the stack, warm at the bottom, like the logo waves
    var tone = COOL.clone().lerp(WARM, Math.pow(t, 1.6));

    for (var s = 0; s <= SEGS; s++) {
      var f = s / SEGS;
      // fade each end into the background so lines have no hard stop
      var edge = Math.min(1, Math.sin(f * Math.PI) * 2.9);
      var c = DEEP.clone().lerp(tone, edge);
      colors[s * 3] = c.r;
      colors[s * 3 + 1] = c.g;
      colors[s * 3 + 2] = c.b;
    }

    var geo = new THREE.BufferGeometry();
    geo.setAttribute('position', new THREE.BufferAttribute(positions, 3));
    geo.setAttribute('color', new THREE.BufferAttribute(colors, 3));

    var mat = new THREE.LineBasicMaterial({
      vertexColors: true,
      transparent: true,
      opacity: 0.3 + (1 - Math.abs(t - 0.5) * 2) * 0.45,
      depthWrite: false
    });

    var line = new THREE.Line(geo, mat);
    line.userData = {
      baseY: (t - 0.5) * 52,
      z: -22 + Math.random() * 40,
      amp: 2.8 + Math.random() * 3.8,
      len: 0.055 + Math.random() * 0.035,
      speed: 0.16 + Math.random() * 0.18,
      phase: Math.random() * Math.PI * 2,
      drift: 0.5 + Math.random() * 0.8
    };
    group.add(line);
    lines.push(line);
  }

  /* ---------- particle field ---------- */
  var COUNT = 900;
  var pPos = new Float32Array(COUNT * 3);
  var pSeed = new Float32Array(COUNT * 2);

  for (var p = 0; p < COUNT; p++) {
    pPos[p * 3] = (Math.random() - 0.5) * SPAN;
    pPos[p * 3 + 1] = (Math.random() - 0.5) * 70;
    pPos[p * 3 + 2] = -40 + Math.random() * 62;
    pSeed[p * 2] = Math.random() * Math.PI * 2;
    pSeed[p * 2 + 1] = 0.3 + Math.random() * 0.9;
  }

  var pGeo = new THREE.BufferGeometry();
  pGeo.setAttribute('position', new THREE.BufferAttribute(pPos, 3));

  var dots = new THREE.Points(pGeo, new THREE.PointsMaterial({
    color: 0xbfe4f3,
    size: 0.32,
    sizeAttenuation: true,
    transparent: true,
    opacity: 0.55,
    depthWrite: false
  }));
  group.add(dots);

  /* ---------- sizing ---------- */
  function resize() {
    var w = canvas.clientWidth || window.innerWidth;
    var h = canvas.clientHeight || window.innerHeight;
    renderer.setSize(w, h, false);
    camera.aspect = w / h;
    // pull the camera back on narrow screens so the currents still read
    camera.position.z = w < 800 ? 82 : 62;
    camera.updateProjectionMatrix();
  }
  window.addEventListener('resize', resize);
  resize();

  /* ---------- pointer parallax ---------- */
  var mx = 0, my = 0, cx = 0, cy = 0;
  window.addEventListener('pointermove', function (e) {
    mx = (e.clientX / window.innerWidth - 0.5) * 2;
    my = (e.clientY / window.innerHeight - 0.5) * 2;
  }, { passive: true });

  /* ---------- frame ---------- */
  function shape(time) {
    for (var i = 0; i < lines.length; i++) {
      var l = lines[i];
      var d = l.userData;
      var arr = l.geometry.attributes.position.array;
      for (var s = 0; s <= SEGS; s++) {
        var f = s / SEGS;
        var x = (f - 0.5) * SPAN;
        var wave =
          Math.sin(x * d.len + time * d.speed + d.phase) * d.amp +
          Math.sin(x * d.len * 0.43 - time * d.speed * 0.7) * d.amp * 0.45;
        arr[s * 3] = x;
        arr[s * 3 + 1] = d.baseY + wave;
        arr[s * 3 + 2] = d.z + Math.sin(x * 0.02 + time * 0.12 + d.phase) * 6;
      }
      l.geometry.attributes.position.needsUpdate = true;
      l.position.y = Math.sin(time * 0.1 * d.drift + d.phase) * 1.2;
    }

    var arr2 = dots.geometry.attributes.position.array;
    for (var p = 0; p < COUNT; p++) {
      var sp = pSeed[p * 2 + 1];
      arr2[p * 3] += sp * 0.035;
      if (arr2[p * 3] > SPAN / 2) arr2[p * 3] = -SPAN / 2;
      arr2[p * 3 + 1] += Math.sin(time * 0.35 * sp + pSeed[p * 2]) * 0.012;
    }
    dots.geometry.attributes.position.needsUpdate = true;
  }

  var visible = true;
  var hero = document.getElementById('hero');
  if ('IntersectionObserver' in window && hero) {
    new IntersectionObserver(function (entries) {
      visible = entries[0].isIntersecting;
    }, { threshold: 0.01 }).observe(hero);
  }

  var start = performance.now();
  function frame(now) {
    requestAnimationFrame(frame);
    if (!visible) return;
    var time = (now - start) / 1000;
    shape(time);
    cx += (mx - cx) * 0.035;
    cy += (my - cy) * 0.035;
    group.rotation.y = cx * 0.06;
    group.rotation.x = -cy * 0.04;
    camera.position.x = cx * 3.2;
    camera.position.y = -cy * 2.2;
    camera.lookAt(0, 0, 0);
    renderer.render(scene, camera);
  }

  if (reduced) {
    shape(3.4);
    renderer.render(scene, camera);
  } else {
    requestAnimationFrame(frame);
  }
}
