function toggleMenu() { document.getElementById('mobileMenu').classList.toggle('open'); }
  function closeMenu() { document.getElementById('mobileMenu').classList.remove('open'); }
  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry, i) => { if (entry.isIntersecting) setTimeout(() => entry.target.classList.add('visible'), i * 80); });
  }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });
  document.querySelectorAll('.fade-up').forEach(el => observer.observe(el));
  document.addEventListener('click', (e) => { if (!e.target.closest('nav') && !e.target.closest('#mobileMenu')) closeMenu(); });