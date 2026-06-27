/**
 * PitchIQ client-side data config.
 *
 * TO MIGRATE TO A NEW API:
 * 1. Update config.py on the Python side (DATA_SOURCE, provider block).
 * 2. generate_live_data.py will write data/live.json in the same schema.
 * 3. No changes needed here — pitchiq-live.js reads live.json, not the API directly.
 *
 * The only reason to edit this file is to change polling behaviour or
 * feature flags for client-side refreshes.
 */

window.PITCHIQ_CONFIG = {

  // URL of the generated live-data file (relative to site root).
  // This is written by generate_live_data.py on every GitHub Actions run.
  liveDataUrl: '/data/live.json',

  // How often the client re-fetches live.json while the page is open (ms).
  // Set to 0 to rely entirely on GitHub Actions pushes (no client polling).
  // Default: 5 minutes (matches the Actions schedule).
  pollInterval: 5 * 60 * 1000,

  // Feature flags — disable any section to skip its DOM updates.
  features: {
    ticker:      true,   // scrolling live scores bar on homepage
    matchOdds:   true,   // odds strip on match preview pages
    probBars:    true,   // home/draw/away probability bars
    standings:   true,   // group standings tables
    bestBets:    true,   // best bets widget on homepage
  },

};
