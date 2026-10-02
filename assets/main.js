(() => {
  const navigation = document.querySelector('.site-header nav');
  const toggle = document.querySelector('.menu-toggle');
  toggle?.addEventListener('click', () => {
    const open = navigation.classList.toggle('is-open');
    toggle.setAttribute('aria-expanded', String(open));
    toggle.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
  });
  navigation?.querySelectorAll('a').forEach(link => link.addEventListener('click', () => {
    navigation.classList.remove('is-open');
    toggle?.setAttribute('aria-expanded', 'false');
  }));

  const slides = [...document.querySelectorAll('.player-screen .slide')];
  if (slides.length > 1 && !window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
    let current = 0;
    window.setInterval(() => {
      slides[current].classList.remove('is-active');
      current = (current + 1) % slides.length;
      slides[current].classList.add('is-active');
    }, 5200);
  }

  const boxes = [...document.querySelectorAll('[data-step]')];
  const count = document.getElementById('progress-count');
  const bar = document.getElementById('progress-bar');
  try {
    const stored = JSON.parse(window.localStorage.getItem('hack-my-y1-steps') || '[]');
    boxes.forEach(box => { box.checked = stored.includes(box.dataset.step); });
  } catch (_) { /* The checklist still works without browser storage. */ }
  function updateProgress() {
    const done = boxes.filter(box => box.checked);
    count.textContent = `${done.length} / ${boxes.length}`;
    bar.style.width = `${(done.length / boxes.length) * 100}%`;
    try { window.localStorage.setItem('hack-my-y1-steps', JSON.stringify(done.map(box => box.dataset.step))); } catch (_) { /* optional */ }
  }
  boxes.forEach(box => box.addEventListener('change', updateProgress));
  updateProgress();

  const platformCommands = {
    mac: 'cd theme\npython3 -m venv .venv\nsource .venv/bin/activate\npython -m pip install -r requirements.txt\npython tools/build_gallery.py --covers my-covers',
    win: 'cd theme\npy -m venv .venv\n.venv\\Scripts\\activate\npython -m pip install -r requirements.txt\npython tools\\build_gallery.py --covers my-covers'
  };
  const code = document.querySelector('#platform-code code');
  document.querySelectorAll('.code-tab').forEach(tab => tab.addEventListener('click', () => {
    document.querySelectorAll('.code-tab').forEach(other => {
      const active = other === tab;
      other.classList.toggle('is-active', active);
      other.setAttribute('aria-pressed', String(active));
    });
    code.textContent = platformCommands[tab.dataset.platform];
  }));
  document.querySelector('.copy-button')?.addEventListener('click', async event => {
    try {
      await navigator.clipboard.writeText(code.textContent);
      event.currentTarget.textContent = 'Copied!';
      window.setTimeout(() => { event.currentTarget.textContent = 'Copy'; }, 1800);
    } catch (_) {
      event.currentTarget.textContent = 'Select text';
      window.setTimeout(() => { event.currentTarget.textContent = 'Copy'; }, 1800);
    }
  });
})();
