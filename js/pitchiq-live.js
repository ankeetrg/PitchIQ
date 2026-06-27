/**
 * PitchIQ Live Updater
 *
 * Reads /data/live.json (written by generate_live_data.py) and updates
 * the DOM on every page without a full reload.
 *
 * How it works:
 *  1. On page load, fetch /data/live.json.
 *  2. Detect which page we're on via <meta name="pitchiq:page"> and
 *     <meta name="pitchiq:slug"> tags (added by generate_pages.py).
 *  3. Update the relevant DOM elements.
 *  4. Poll again every PITCHIQ_CONFIG.pollInterval ms.
 *
 * Elements are updated in two ways:
 *  a) [data-live="path.to.key"] attributes — generic, dot-path into live.json.
 *  b) Class-based detection on match pages — no attributes needed on the 87
 *     individual HTML files; the updater reads .odd-label text to determine
 *     which odds value to replace.
 *
 * To add a new data field:
 *  - Add it to live.json schema in generate_live_data.py.
 *  - Add a data-live="..." attribute to the HTML element, OR
 *  - Add a handler in the relevant update* function below.
 */

(function () {
  'use strict';

  const CFG      = window.PITCHIQ_CONFIG || {};
  const DATA_URL = CFG.liveDataUrl  || '/data/live.json';
  const POLL_MS  = CFG.pollInterval ?? 5 * 60 * 1000;
  const FEAT     = CFG.features     || {};

  // ── Page context ─────────────────────────────────────────────────────────

  function getPageContext() {
    const metaPage = document.querySelector('meta[name="pitchiq:page"]');
    const metaSlug = document.querySelector('meta[name="pitchiq:slug"]');
    const metaHome = document.querySelector('meta[name="pitchiq:home"]');
    const metaAway = document.querySelector('meta[name="pitchiq:away"]');

    const page = metaPage ? metaPage.content : _inferPageFromUrl();
    const slug = metaSlug ? metaSlug.content : _inferSlugFromUrl();

    return {
      page,
      slug,
      home: metaHome ? metaHome.content : null,
      away: metaAway ? metaAway.content : null,
    };
  }

  function _inferPageFromUrl() {
    const p = location.pathname.replace(/\//g, '').replace('.html', '');
    if (!p || p === 'index')   return 'home';
    if (p === 'standings')     return 'standings';
    if (p === 'fantasy')       return 'fantasy';
    if (p === 'predictions')   return 'predictions';
    return 'match';
  }

  function _inferSlugFromUrl() {
    return location.pathname.replace(/\//g, '').replace('.html', '') || null;
  }

  // ── Data fetch ────────────────────────────────────────────────────────────

  let _lastEtag = null;

  async function fetchLiveData() {
    try {
      const headers = {};
      if (_lastEtag) headers['If-None-Match'] = _lastEtag;

      const r = await fetch(DATA_URL + '?_=' + Date.now(), { headers });
      if (r.status === 304) return null;   // not modified
      if (!r.ok) return null;

      _lastEtag = r.headers.get('etag');
      return await r.json();
    } catch {
      return null;
    }
  }

  // ── Generic [data-live] updater ───────────────────────────────────────────
  // Any element with data-live="some.nested.key" gets its textContent updated
  // from the corresponding value in live.json.

  function updateDataLiveAttrs(data) {
    document.querySelectorAll('[data-live]').forEach(el => {
      const val = _resolve(data, el.dataset.live);
      if (val != null) el.textContent = val;
    });
  }

  function _resolve(obj, path) {
    return path.split('.').reduce((o, k) => (o != null ? o[k] : undefined), obj);
  }

  // ── Match page: odds strip ────────────────────────────────────────────────

  function updateMatchOdds(slug, home, away, data) {
    if (FEAT.matchOdds === false) return;
    const match = data.matches?.[slug];
    if (!match) return;

    // Resolve home/away names from meta or from live.json
    const homeName = home || match.home || '';
    const awayName = away || match.away || '';

    // Update each odd-card: find the label, then update the adjacent value div
    document.querySelectorAll('.odd-label').forEach(label => {
      const text   = label.textContent.trim();
      const valEl  = label.nextElementSibling;
      if (!valEl || !valEl.classList.contains('odd-val')) return;

      let newVal = null;
      if (text === homeName + ' Win')  newVal = match.home_ml;
      else if (text === awayName + ' Win') newVal = match.away_ml;
      else if (text === 'Draw')           newVal = match.draw_ml;
      else if (/^Over [\d.]+ Goals$/.test(text))  newVal = match.ou_over;
      else if (/^Under [\d.]+ Goals$/.test(text)) newVal = match.ou_under;

      if (newVal == null) return;
      _setOddsVal(valEl, newVal);
    });

    // Sidebar: favourite moneyline shown in all sb-book-odds cells
    const homeN = parseInt(match.home_ml || '0');
    const awayN = parseInt(match.away_ml || '0');
    const favMl = homeN < awayN ? match.home_ml : match.away_ml;
    document.querySelectorAll('.sb-book-odds').forEach(el => {
      el.textContent = favMl;
    });

    // Sidebar "Best Odds:" header label
    const favName = homeN < awayN ? homeName : awayName;
    document.querySelectorAll('.sc-head').forEach(el => {
      if (el.textContent.startsWith('Best Odds:')) {
        el.textContent = `Best Odds: ${favName} Win`;
      }
    });

    // Probability bars
    if (FEAT.probBars !== false) {
      _updateProbBars(match.home_prob, match.draw_prob, match.away_prob);
    }
  }

  function _setOddsVal(el, val) {
    if (!val) return;
    el.textContent = val;
    const n = parseInt(val, 10);
    el.classList.toggle('fav', !isNaN(n) && n < 0);
    el.classList.toggle('dog', !isNaN(n) && n >= 0);
  }

  function _updateProbBars(homeP, drawP, awayP) {
    if (homeP == null) return;
    const home = document.querySelector('.prob-seg.home');
    const draw = document.querySelector('.prob-seg.draw');
    const away = document.querySelector('.prob-seg.away');
    if (home) home.style.width = homeP + '%';
    if (draw) draw.style.width = drawP + '%';
    if (away) away.style.width = awayP + '%';
  }

  // ── Homepage: live ticker ─────────────────────────────────────────────────

  function updateTicker(data) {
    if (FEAT.ticker === false || !data.ticker?.length) return;

    // Locate the scrolling track inside .ticker
    const track = document.querySelector('#tickerTrack, .ticker-track, .ticker-scroll .tick-inner, .ticker-inner');
    if (!track) return;

    const items = data.ticker.map(m => {
      let scoreStr;
      if (m.status === 'live') {
        const clock = m.clock ? ` ${m.clock}` : '';
        scoreStr = `${m.score_home ?? 0}–${m.score_away ?? 0}${clock}`;
      } else if (m.status === 'ft') {
        scoreStr = `FT ${m.score_home}–${m.score_away}`;
      } else {
        // Upcoming — show kickoff time
        scoreStr = m.time_str || m.date_short || '';
      }

      const liveClass = m.status === 'live' ? ' class="tick-live"' : '';
      return (
        `<span class="tick-item">` +
        `<span class="tick-teams">${m.home_emoji || ''} ${m.home} <span class="tick-vs">vs</span> ${m.away} ${m.away_emoji || ''}</span>` +
        `<span class="tick-score"${liveClass}>${scoreStr}</span>` +
        `</span>`
      );
    }).join('<span class="tick-sep"> · </span>');

    // Duplicate for seamless marquee loop
    track.innerHTML = items + '<span class="tick-sep" aria-hidden="true"> · </span>' + items;
  }

  // ── Homepage: best bets widget ────────────────────────────────────────────
  // Best bets uses [data-live] attributes on .bet-odds-pill elements.
  // Those are added in index.html. No extra logic needed here — handled by
  // updateDataLiveAttrs().

  // ── Standings page ────────────────────────────────────────────────────────
  // Standings rows use [data-live] attributes generated into standings.html.

  // ── Main update cycle ─────────────────────────────────────────────────────

  async function runUpdate() {
    const data = await fetchLiveData();
    if (!data) return;

    const ctx = getPageContext();

    // Generic data-live attrs work on every page
    updateDataLiveAttrs(data);

    if (ctx.page === 'home') {
      updateTicker(data);
    }

    if (ctx.page === 'match' && ctx.slug) {
      updateMatchOdds(ctx.slug, ctx.home, ctx.away, data);
    }
  }

  // Kick off immediately, then on interval
  runUpdate();
  if (POLL_MS > 0) {
    setInterval(runUpdate, POLL_MS);
  }

})();
