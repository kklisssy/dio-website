const clouds = document.querySelectorAll("[data-hero-cloud]");

const updateCloud = (cloud) => {
  const center = cloud.querySelector("[data-cloud-center]");
  const items = [...cloud.querySelectorAll("[data-cloud-item]")];
  const lines = [...cloud.querySelectorAll("[data-cloud-line]")];

  if (!center || !items.length) return;

  const cloudRect = cloud.getBoundingClientRect();
  const centerRect = center.getBoundingClientRect();
  const centerX = centerRect.left - cloudRect.left + centerRect.width / 2;
  const centerY = centerRect.top - cloudRect.top + centerRect.height / 2;
  const radiusX = cloudRect.width * 0.36;
  const radiusY = cloudRect.height * 0.36;

  items.forEach((item, index) => {
    const angle = -Math.PI / 2 + (Math.PI * 2 * index) / items.length;
    const x = centerX + Math.cos(angle) * radiusX;
    const y = centerY + Math.sin(angle) * radiusY;
    item.style.setProperty("--cloud-x", `${x}px`);
    item.style.setProperty("--cloud-y", `${y}px`);

    const line = lines[index];
    if (line) {
      line.setAttribute("x1", centerX);
      line.setAttribute("y1", centerY);
      line.setAttribute("x2", x);
      line.setAttribute("y2", y);
    }
  });
};

clouds.forEach((cloud) => {
  const lines = [...cloud.querySelectorAll("[data-cloud-line]")];
  const nodes = [...cloud.querySelectorAll("[data-cloud-node]")];

  nodes.forEach((node, index) => {
    const setActive = (active) => lines[index]?.classList.toggle("is-active", active);
    node.addEventListener("pointerenter", () => setActive(true));
    node.addEventListener("pointerleave", () => setActive(false));
    node.addEventListener("focus", () => setActive(true));
    node.addEventListener("blur", () => setActive(false));
  });

  const observer = new ResizeObserver(() => updateCloud(cloud));
  observer.observe(cloud);
  updateCloud(cloud);
});
