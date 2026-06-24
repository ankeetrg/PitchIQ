export const STATIC_WORLD_CUP_ROUTES = [
  "/world-cup-2026",
  "/world-cup-2026/scores",
  "/world-cup-2026/schedule",
  "/world-cup-2026/how-to-watch",
  "/world-cup-2026/fantasy",
  "/world-cup-2026/fantasy/best-players",
  "/world-cup-2026/betting/odds-explained",
  "/world-cup-2026/betting/world-cup-picks-today",
] as const;

export const FIRST_BATCH_ROUTES = [
  "/world-cup-2026/how-to-watch",
  "/world-cup-2026/schedule",
  "/world-cup-2026/teams/usa-guide",
  "/world-cup-2026/teams/brazil-guide",
  "/world-cup-2026/teams/france-guide",
  "/world-cup-2026/fantasy/best-players",
  "/world-cup-2026/betting/odds-explained",
  "/world-cup-2026/betting/world-cup-picks-today",
  "/world-cup-2026/matches/brazil-morocco/preview",
  "/world-cup-2026/matches/brazil-morocco/odds-picks",
] as const;

export const INTENT_MATCH_SLUGS = ["brazil-morocco"] as const;

export const SKIPPED_PROGRAMMATIC_SUBPAGES =
  "Preview, odds-picks, and how-to-watch subpages were not generated for all 72 matches. Only first-batch, high-intent routes are live until search demand is proven.";
