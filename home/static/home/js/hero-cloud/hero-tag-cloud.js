const root = document.querySelector("[data-hero-cloud]");

if (root) {
  const canvas = root.querySelector("[data-cloud-canvas]");
  const labelsLayer = root.querySelector("[data-cloud-labels]");

  const tags = [...root.querySelectorAll('[data-cloud-source] a')].map((link) => ({
    label: link.textContent.trim(),
    href: link.getAttribute('href'),
    kind: link.dataset.cloudCategory || 'default',
  }));

  const reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const colors = {
    primary: 0xc91f2f,
    service: 0x2f6f9f,
    data: 0x25845f,
    default: 0xd9e4ef
  };

  try {
    const THREE = await import("./three.module.min.js");
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(36, 1, 0.1, 100);
    const renderer = new THREE.WebGLRenderer({
      canvas,
      antialias: true,
      alpha: true,
      powerPreference: "high-performance"
    });

    renderer.setClearColor(0x000000, 0);
    renderer.outputColorSpace = THREE.SRGBColorSpace;
    renderer.setPixelRatio(Math.min(window.devicePixelRatio || 1, 2));

    const group = new THREE.Group();
    scene.add(group);

    scene.add(new THREE.AmbientLight(0xffffff, 0.72));
    const redLight = new THREE.PointLight(0xff5967, 2.4, 12);
    redLight.position.set(-3, 2, 5);
    scene.add(redLight);
    const blueLight = new THREE.PointLight(0x6ea7dc, 1.7, 10);
    blueLight.position.set(4, -2, 4);
    scene.add(blueLight);

    const core = new THREE.Mesh(
      new THREE.SphereGeometry(0.62, 42, 42),
      new THREE.MeshStandardMaterial({
        color: 0xc91f2f,
        emissive: 0x4b0710,
        roughness: 0.36,
        metalness: 0.22,
        transparent: true,
        opacity: 0.86
      })
    );
    group.add(core);

    const halo = new THREE.Mesh(
      new THREE.SphereGeometry(0.92, 48, 48),
      new THREE.MeshBasicMaterial({
        color: 0xc91f2f,
        transparent: true,
        opacity: 0.1,
        depthWrite: false
      })
    );
    group.add(halo);

    const ringMaterial = new THREE.MeshBasicMaterial({
      color: 0xffffff,
      transparent: true,
      opacity: 0.14,
      depthWrite: false
    });

    [
      [1.78, 0.08, 0.62],
      [2.18, -0.55, 0.28],
      [2.52, 0.28, -0.42]
    ].forEach(([radius, x, z]) => {
      const ring = new THREE.Mesh(new THREE.TorusGeometry(radius, 0.006, 12, 160), ringMaterial);
      ring.rotation.set(x, 0.18, z);
      group.add(ring);
    });

    const nodeGeometry = new THREE.SphereGeometry(0.078, 22, 22);
    const linePositions = [];
    const nodes = tags.map((tag, index) => {
      const y = 1 - (index / Math.max(1, tags.length - 1)) * 2;
      const radiusAtY = Math.sqrt(1 - y * y);
      const theta = index * Math.PI * (3 - Math.sqrt(5));
      const radius = tag.kind === "primary" ? 2.48 : 2.74;
      const position = new THREE.Vector3(
        Math.cos(theta) * radiusAtY * radius,
        y * radius * 0.78,
        Math.sin(theta) * radiusAtY * radius
      );

      const material = new THREE.MeshStandardMaterial({
        color: colors[tag.kind] || colors.default,
        emissive: colors[tag.kind] || 0x273746,
        emissiveIntensity: tag.kind === "primary" ? 0.24 : 0.14,
        roughness: 0.44,
        metalness: 0.16
      });

      const mesh = new THREE.Mesh(nodeGeometry, material);
      mesh.position.copy(position);
      mesh.scale.setScalar(tag.kind === "primary" ? 1.35 : tag.kind === "default" ? 0.94 : 1.12);
      group.add(mesh);

      linePositions.push(0, 0, 0, position.x, position.y, position.z);

      const label = document.createElement("a");
      label.className = `cloud-tag${tag.kind === "primary" ? " is-primary" : ""}${tag.kind === "service" ? " is-service" : ""}${tag.kind === "data" ? " is-data" : ""}${tag.kind === "default" ? " is-detail" : ""}${tag.mobileDetail ? " is-mobile-detail" : ""}`;
      label.href = tag.href;
      label.textContent = tag.displayLabel || tag.label;
      label.title = tag.label;
      label.setAttribute("aria-label", tag.label);
      labelsLayer.appendChild(label);

      return { mesh, label, tag, width: 0, height: 0 };
    });

    const lineGeometry = new THREE.BufferGeometry();
    lineGeometry.setAttribute("position", new THREE.Float32BufferAttribute(linePositions, 3));
    const lines = new THREE.LineSegments(
      lineGeometry,
      new THREE.LineBasicMaterial({
        color: 0xffffff,
        transparent: true,
        opacity: 0.12,
        depthWrite: false
      })
    );
    group.add(lines);

    const pointer = { x: 0, y: 0 };
    const smoothPointer = { x: 0, y: 0 };
    const viewport = { width: 1, height: 1 };
    let pointerRect = root.getBoundingClientRect();
    const refreshPointerRect = () => {
      pointerRect = root.getBoundingClientRect();
    };
    root.addEventListener("pointerenter", refreshPointerRect);
    window.addEventListener("scroll", refreshPointerRect, { passive: true, capture: true });
    root.addEventListener("pointermove", (event) => {
      if (event.pointerType === "touch" || reduceMotion) return;
      pointer.x = THREE.MathUtils.clamp(((event.clientX - pointerRect.left) / Math.max(1, pointerRect.width) - 0.5) * 2, -1, 1);
      pointer.y = THREE.MathUtils.clamp(((event.clientY - pointerRect.top) / Math.max(1, pointerRect.height) - 0.5) * 2, -1, 1);
    });

    root.addEventListener("pointerleave", () => {
      pointer.x = 0;
      pointer.y = 0;
    });

    const world = new THREE.Vector3();
    const projected = new THREE.Vector3();

    function syncLabelText() {
      const compact = root.clientWidth < 520;

      nodes.forEach(({ label, tag }) => {
        label.textContent = compact && tag.shortLabel ? tag.shortLabel : tag.displayLabel || tag.label;
      });
    }

    function resize() {
      syncLabelText();
      const rect = root.getBoundingClientRect();
      const width = Math.max(1, Math.floor(rect.width));
      const height = Math.max(1, Math.floor(rect.height));
      pointerRect = rect;
      viewport.width = width;
      viewport.height = height;
      renderer.setSize(width, height, false);
      camera.aspect = width / height;
      camera.position.set(0, 0, width < 520 ? 7.2 : 6.2);
      camera.updateProjectionMatrix();
    }

    function updateLabels() {
      const { width, height } = viewport;
      const edgePadding = width < 520 ? 10 : 16;

      nodes.forEach(({ mesh, label, width: labelWidth, height: labelHeight }) => {
        mesh.getWorldPosition(world);
        projected.copy(world).project(camera);
        const x = (projected.x * 0.5 + 0.5) * width;
        const y = (-projected.y * 0.5 + 0.5) * height;
        const depth = THREE.MathUtils.clamp(1 - (projected.z + 1) / 2, 0, 1);
        const scale = THREE.MathUtils.lerp(0.86, 1.16, depth);
        const opacity = THREE.MathUtils.lerp(0.48, 1, depth);
        const halfWidth = (labelWidth * scale) / 2;
        const halfHeight = (labelHeight * scale) / 2;
        const clampedX = THREE.MathUtils.clamp(x, edgePadding + halfWidth, width - edgePadding - halfWidth);
        const clampedY = THREE.MathUtils.clamp(y, edgePadding + halfHeight, height - edgePadding - halfHeight);

        label.style.opacity = String(opacity);
        label.style.zIndex = String(Math.round(100 + depth * 100));
        label.style.transform = `translate(${clampedX}px, ${clampedY}px) translate(-50%, -50%) scale(${scale})`;
      });
    }

    let rafId = 0;
    let previousTime = null;
    let elapsed = 0;

    function render(time = performance.now()) {
      rafId = 0;
      if (document.hidden) return;
      const delta = previousTime === null ? 0 : Math.min((time - previousTime) / 1000, 0.05);
      previousTime = time;
      elapsed += delta;
      // Exponential smoothing gives the same response at different frame rates.
      const follow = 1 - Math.exp(-14 * delta);
      smoothPointer.x += (pointer.x - smoothPointer.x) * follow;
      smoothPointer.y += (pointer.y - smoothPointer.y) * follow;
      const spin = reduceMotion ? 0 : elapsed * 0.12;
      group.rotation.y = spin + smoothPointer.x * 0.32;
      group.rotation.x = -0.12 + smoothPointer.y * 0.18;
      core.rotation.y = elapsed * 0.18;
      halo.scale.setScalar(1 + Math.sin(elapsed * 1.3) * 0.025);

      renderer.render(scene, camera);
      updateLabels();

      if (!reduceMotion) {
        rafId = window.requestAnimationFrame(render);
      }
    }

    const observer = new ResizeObserver(() => {
      resize();
      renderer.render(scene, camera);
      updateLabels();
    });

    // Measure all labels together, outside the animation loop.
    const measureLabels = () => {
      nodes.forEach((node) => {
        node.width = node.label.offsetWidth;
        node.height = node.label.offsetHeight;
      });
      if (reduceMotion) updateLabels();
    };
    const labelObserver = new ResizeObserver(measureLabels);

    nodes.forEach(({ label }) => labelObserver.observe(label));
    observer.observe(root);
    resize();
    measureLabels();
    render();
    // Replace the static preview only after the first WebGL frame is drawn.
    window.requestAnimationFrame(() => {
      root.classList.remove('is-loading');
      root.classList.add('is-ready');
    });

    document.addEventListener("visibilitychange", () => {
      window.cancelAnimationFrame(rafId);
      rafId = 0;
      previousTime = null;
      if (!document.hidden) {
        refreshPointerRect();
        render();
      }
    });
  } catch (error) {
    root.classList.remove("is-loading", "is-ready");
    root.classList.add("is-fallback");
    console.warn("3D tag cloud fallback", error);
  }
}


