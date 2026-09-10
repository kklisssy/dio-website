(() => {
  const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  if (reducedMotion.matches || !('IntersectionObserver' in window)) return;

  const blocks = document.querySelectorAll(
    'main > section:not(.hero-section), main > .hero-features > li'
  );
  const reveal = (block) => {
    block.classList.remove('home-reveal-pending');
    observer.unobserve(block);
  };
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) reveal(entry.target);
    });
  }, { threshold: 0, rootMargin: '0px 0px -32px 0px' });

  blocks.forEach((block) => {
    if (block.getBoundingClientRect().top < window.innerHeight) return;
    block.classList.add('home-reveal', 'home-reveal-pending');
    observer.observe(block);
  });

  document.addEventListener('focusin', (event) => {
    const block = event.target.closest('.home-reveal-pending');
    if (block) reveal(block);
  });
  reducedMotion.addEventListener('change', () => {
    if (reducedMotion.matches) {
      blocks.forEach(reveal);
      observer.disconnect();
    }
  });
})();
