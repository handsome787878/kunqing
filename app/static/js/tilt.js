// Lightweight 3D tilt interaction for cards
(function () {
  const cards = document.querySelectorAll('.nav-card[data-tilt]');
  const maxRotate = 8; // degrees
  const maxTranslateZ = 16; // px

  function handleMove(e) {
    const card = e.currentTarget;
    const rect = card.getBoundingClientRect();
    const x = e.clientX - rect.left;
    const y = e.clientY - rect.top;
    const midX = rect.width / 2;
    const midY = rect.height / 2;
    const rotY = ((x - midX) / midX) * maxRotate;
    const rotX = -((y - midY) / midY) * maxRotate;
    card.style.transform = `rotateX(${rotX}deg) rotateY(${rotY}deg) translateZ(${maxTranslateZ}px)`;
  }

  function handleLeave(e) {
    e.currentTarget.style.transform = 'rotateX(0) rotateY(0) translateZ(0)';
  }

  cards.forEach((card) => {
    card.addEventListener('mousemove', handleMove);
    card.addEventListener('mouseleave', handleLeave);
  });
})();