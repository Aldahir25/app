document.addEventListener('DOMContentLoaded', function () {
  const cards = document.querySelectorAll('[data-count]');
  cards.forEach((el) => {
    const target = Number(el.dataset.count || 0);
    let current = 0;
    const step = Math.max(1, Math.ceil(target / 25));
    const tick = setInterval(() => {
      current += step;
      if (current >= target) {
        current = target;
        clearInterval(tick);
      }
      el.textContent = current;
    }, 25);
  });
});
