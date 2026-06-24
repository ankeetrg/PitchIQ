/* ═══════════════════════════════════════════
   PITCHIQ APP
   Live simulation · Theme · Interactions
═══════════════════════════════════════════ */

/* ── THEME ───────────────────────────────── */
(function () {
  const saved = localStorage.getItem('pitchiq-theme') || 'light';
  applyTheme(saved, false);

  function applyTheme(theme, animate) {
    if (animate) document.documentElement.classList.add('theme-switching');
    document.documentElement.dataset.theme = theme;
    localStorage.setItem('pitchiq-theme', theme);
    // icon visibility handled by CSS [data-theme] selectors
    if (animate) setTimeout(() => document.documentElement.classList.remove('theme-switching'), 400);
  }

  document.getElementById('themeToggle')?.addEventListener('click', () => {
    const cur = document.documentElement.dataset.theme;
    applyTheme(cur === 'dark' ? 'light' : 'dark', true);
  });
})();

/* ── LIVE MATCH SIMULATION ───────────────── */
(function () {
  let min = 67, homeGoals = 1, awayGoals = 0, live = true;
  const firedAt = new Set();

  const matchEvents = [
    { at: 73, type: 'goal', team: 'home' },
    { at: 84, type: 'yellow' },
    { at: 90, type: 'injury', msg: '+4 min injury time added' },
    { at: 94, type: 'fulltime' },
  ];

  const els = {
    heroScore:   () => document.getElementById('heroScore'),
    heroMin:     () => document.getElementById('heroMin'),
    liveBadge:   () => document.getElementById('matchStatusBadge'),
    livePill:    () => document.querySelector('.mh-live-pill'),
    sideScore:   () => document.getElementById('side-score'),
    sideMin:     () => document.getElementById('side-minute'),
    fixLive:     () => document.querySelector('.fix-status.live'),
  };

  function scoreStr() { return `${homeGoals}–${awayGoals}`; }

  function render() {
    const sc = scoreStr();
    const minLabel = live ? `${min}'` : 'FT';
    if (els.heroScore()) els.heroScore().textContent = sc;
    if (els.heroMin())   els.heroMin().textContent   = live ? `● ${min}'` : '● FT';
    if (els.liveBadge()) els.liveBadge().textContent = minLabel;
    if (els.sideScore()) els.sideScore().textContent = sc;
    if (els.sideMin())   els.sideMin().textContent   = live ? `${min}'` : 'FT';
  }

  function flashScore() {
    const el = els.heroScore();
    if (!el) return;
    el.classList.remove('flash');
    void el.offsetWidth; // reflow
    el.classList.add('flash');
    setTimeout(() => el.classList.remove('flash'), 800);
  }

  function setProb(h, d, a) {
    const set = (id, w) => { const e = document.getElementById(id); if (e) e.style.width = w + '%'; };
    const setText = (id, v) => { const e = document.getElementById(id); if (e) e.textContent = v + '%'; };
    set('probHome', h); set('probDraw', d); set('probAway', a);
    setText('probHomePct', h); setText('probDrawPct', d); setText('probAwayPct', a);
  }

  function handleGoal() {
    homeGoals++;
    render();
    flashScore();
    setProb(80, 13, 7);
    showToast('⚽ GOAL! Mbappé 73\' — France 2–0 Uruguay');
    // Update ticker first duplicate too
    document.querySelectorAll('#tickerTrack .tick-item').forEach(item => {
      if (item.textContent.includes('FRA') && item.textContent.includes('URU')) {
        const sc = item.querySelector('.score');
        if (sc) sc.textContent = scoreStr();
      }
    });
    // Odds react
    driftOdds(-20, 30, 60, 5);
  }

  function handleFulltime() {
    live = false;
    render();
    const pill = els.livePill();
    if (pill) {
      pill.style.background = 'rgba(255,255,255,0.15)';
      const dot = pill.querySelector('.dot');
      if (dot) dot.style.animation = 'none';
    }
    const fixStatus = els.fixLive();
    if (fixStatus) { fixStatus.textContent = 'FT'; fixStatus.className = 'fix-status ft'; }
    showToast('🔔 Full Time — France 2–0 Uruguay');
  }

  // Tick every 1.5 s = 1 game minute
  const ticker = setInterval(() => {
    if (!live) { clearInterval(ticker); return; }
    min++;
    render();

    matchEvents.forEach(ev => {
      if (ev.at <= min && !firedAt.has(ev.at)) {
        firedAt.add(ev.at);
        if (ev.type === 'goal')     handleGoal();
        if (ev.type === 'fulltime') handleFulltime();
        if (ev.msg)                 showToast('🕐 ' + ev.msg);
      }
    });
  }, 1500);

  // Animate probability bar on load
  setTimeout(() => setProb(65, 20, 15), 700);
})();

/* ── ODDS DRIFT ──────────────────────────── */
const oddsState = { fra: -140, draw: 290, uru: 380, ou: -110 };

function driftOdds(fraD, drawD, uruD, ouD) {
  const apply = (id, delta) => {
    const key = { 'odd-fra': 'fra', 'odd-draw': 'draw', 'odd-uru': 'uru', 'odd-ou': 'ou' }[id];
    if (!key) return;
    oddsState[key] += delta;
    const el = document.getElementById(id);
    if (!el) return;
    const fmt = v => v > 0 ? `+${v}` : `${v}`;
    const next = fmt(oddsState[key]);
    if (el.textContent !== next) {
      el.textContent = next;
      el.classList.remove('flash-odds');
      void el.offsetWidth;
      el.classList.add('flash-odds');
      setTimeout(() => el.classList.remove('flash-odds'), 600);
    }
  };
  apply('odd-fra', fraD); apply('odd-draw', drawD);
  apply('odd-uru', uruD); apply('odd-ou', ouD);
}

// Random small drift every 20 s
setInterval(() => {
  const rand = () => (Math.random() > 0.5 ? 5 : -5);
  driftOdds(rand(), rand() * 2, rand() * 2, rand());
}, 20000);

/* ── SCROLL REVEAL + COUNTUP ─────────────── */
(function () {
  function countUp(el) {
    const target = +el.dataset.count;
    const suffix = el.dataset.suffix || '';
    const dur = 1400;
    const start = performance.now();
    const ease = t => 1 - Math.pow(1 - t, 3);
    (function frame(now) {
      const p = Math.min((now - start) / dur, 1);
      const val = Math.round(ease(p) * target);
      el.textContent = (val >= 1000 ? val.toLocaleString() : val) + suffix;
      if (p < 1) requestAnimationFrame(frame);
    })(start);
  }

  function reveal(el) {
    if (el.classList.contains('vis')) return;
    el.classList.add('vis');
    el.querySelectorAll('[data-count]').forEach(n => countUp(n));
  }

  const revObs = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      reveal(entry.target);
      revObs.unobserve(entry.target);
    });
  }, { threshold: 0.08 });

  document.querySelectorAll('.rv, .stat-item').forEach(el => revObs.observe(el));

  // Fallback: force-reveal anything still hidden after 300ms
  // (handles iframe / pre-render contexts where IntersectionObserver may not fire)
  setTimeout(() => {
    document.querySelectorAll('.rv:not(.vis), .stat-item:not(.vis)').forEach(el => reveal(el));
  }, 300);
})();

/* ── OWNERSHIP BAR ANIMATION ─────────────── */
(function () {
  const obs = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.querySelectorAll('.fp-own-fill').forEach(bar => {
        const w = bar.style.width;
        bar.style.width = '0';
        requestAnimationFrame(() => { bar.style.width = w; });
      });
      obs.unobserve(entry.target);
    });
  }, { threshold: 0.1 });
  document.querySelectorAll('.fp-card').forEach(el => obs.observe(el));
})();

/* ── FANTASY POSITION FILTER ─────────────── */
document.querySelectorAll('.fp-filter').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.fp-filter').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    const pos = btn.dataset.pos;
    document.querySelectorAll('.fp-table tbody tr').forEach(row => {
      if (!pos) { row.style.display = ''; return; }
      const pill = row.querySelector('.pos-pill');
      row.style.display = (pill && pill.textContent.trim() === pos) ? '' : 'none';
    });
  });
});

/* ── PICK SYSTEM ─────────────────────────── */
document.querySelectorAll('.btn-pick').forEach(btn => {
  btn.addEventListener('click', function () {
    const row = this.closest('tr');
    const player = this.dataset.player;
    const picked = this.classList.toggle('picked');
    this.textContent = picked ? '✓ Picked' : '+ Pick';
    row.classList.toggle('picked', picked);
    if (picked) {
      this.style.transform = 'scale(1.12)';
      setTimeout(() => { this.style.transform = ''; }, 180);
    }
    showToast(picked ? `✓ ${player} added to lineup!` : `${player} removed`);
  });
});

/* ── SEC TABS ────────────────────────────── */
document.querySelectorAll('.sec-tab').forEach(tab => {
  tab.addEventListener('click', () => {
    tab.closest('.sec-tabs').querySelectorAll('.sec-tab').forEach(t => t.classList.remove('active'));
    tab.classList.add('active');
  });
});

/* ── MOBILE NAV ──────────────────────────── */
document.querySelectorAll('.mob-nav-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.mob-nav-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
  });
});

/* ── CRICKET MODAL ───────────────────────── */
const cricketModal = document.getElementById('cricketModal');
document.getElementById('cricketTab')?.addEventListener('click', () => cricketModal?.classList.add('open'));
document.getElementById('modalClose')?.addEventListener('click', () => cricketModal?.classList.remove('open'));
cricketModal?.addEventListener('click', e => { if (e.target === cricketModal) cricketModal.classList.remove('open'); });

/* ── NEWSLETTER ──────────────────────────── */
document.getElementById('nlSubmit')?.addEventListener('click', function () {
  const form = this.closest('.nl-form');
  const input = form?.querySelector('.nl-input');
  if (input?.value?.includes('@')) {
    this.textContent = '✓ You\'re in!';
    this.style.background = 'var(--grn)';
    input.value = '';
    showToast('✓ Welcome to PitchIQ Daily — picks incoming!');
    setTimeout(() => { this.textContent = 'Subscribe'; this.style.background = ''; }, 3500);
  } else {
    if (input) { input.style.borderColor = 'var(--red)'; input.focus(); }
    setTimeout(() => { if (input) input.style.borderColor = ''; }, 1600);
  }
});

/* ── TOAST ───────────────────────────────── */
let _toastTimer;
function showToast(msg) {
  const toast = document.getElementById('toast');
  const msgEl = document.getElementById('toastMsg');
  if (!toast || !msgEl) return;
  msgEl.textContent = msg;
  toast.classList.add('show');
  clearTimeout(_toastTimer);
  _toastTimer = setTimeout(() => toast.classList.remove('show'), 2800);
}
window.showToast = showToast;
