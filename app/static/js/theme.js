// Theme toggle: syncs our CSS variables and Bootstrap's data-bs-theme
(function () {
  const root = document.documentElement;
  const bootstrapThemeAttr = 'data-bs-theme';
  const ourThemeAttr = 'data-theme';
  const toggleBtn = document.getElementById('themeToggle');
  const saved = localStorage.getItem('theme') || 'light';

  function applyTheme(theme) {
    root.setAttribute(bootstrapThemeAttr, theme);
    root.setAttribute(ourThemeAttr, theme);
    localStorage.setItem('theme', theme);
    if (toggleBtn) {
      toggleBtn.textContent = theme === 'dark' ? '切换到浅色' : '切换到深色';
    }
  }

  applyTheme(saved);

  toggleBtn?.addEventListener('click', () => {
    const current = root.getAttribute(ourThemeAttr) || 'light';
    applyTheme(current === 'dark' ? 'light' : 'dark');
  });
})();