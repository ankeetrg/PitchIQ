export type Sport = "soccer" | "cricket";
export type Theme = "light" | "dark";
export type MatchStatus = "pre" | "live" | "halftime" | "fulltime";
export type Movement = "up" | "down" | "flat";
export type FantasyPosition = "FWD" | "MID" | "DEF" | "GK";

export interface Team {
  name: string;
  shortName: string;
  fifaCode: string;
  flagCode: string;
  record: string;
  form: Array<"W" | "D" | "L">;
}

export interface MatchStatLine {
  label: string;
  value: string;
  detail?: string;
}

export interface Match {
  id: string;
  competition: string;
  group: string;
  status: MatchStatus;
  minute: number;
  clock: string;
  startTime: string;
  venue: string;
  home: Team;
  away: Team;
  score: {
    home: number;
    away: number;
  };
  odds: {
    home: number;
    draw: number;
    away: number;
    total: string;
    spread: string;
    book: string;
  };
  probabilities: {
    home: number;
    draw: number;
    away: number;
  };
  stats: {
    xgHome: number;
    xgAway: number;
    shotsHome: number;
    shotsAway: number;
    possessionHome: number;
    possessionAway: number;
    cornersHome: number;
    cornersAway: number;
  };
  keyStats: MatchStatLine[];
}

export interface OddsOutcome {
  name: string;
  price: number;
  point?: number;
}

export interface Odds {
  id: string;
  matchId: string;
  sportsbook: string;
  market: "h2h" | "spreads" | "totals";
  outcomes: OddsOutcome[];
  lastUpdate: string;
}

export interface TickerItem {
  id: string;
  label: string;
  value: string;
  status: string;
  accent: "red" | "green" | "gold" | "blue";
}

export interface StandingRow {
  team: string;
  flagCode: string;
  played: number;
  won: number;
  drawn: number;
  lost: number;
  goalDiff: number;
  points: number;
}

export type GroupStandings = Record<string, StandingRow[]>;

export interface ScheduleMatch {
  id: string;
  time: string;
  home: string;
  away: string;
  group: string;
  venue: string;
  tag: string;
}

export interface FantasyPick {
  id: string;
  player: string;
  team: string;
  flagCode: string;
  position: FantasyPosition;
  salary: string;
  projection: number;
  ownership: string;
  edge: string;
  note: string;
}

export interface ParlayLeg {
  id: string;
  label: string;
  odds: string;
  confidence: number;
}

export interface Parlay {
  title: string;
  payout: string;
  confidence: number;
  legs: ParlayLeg[];
  rationale: string;
}

export interface LineMovement {
  id: string;
  match: string;
  market: string;
  open: string;
  current: string;
  move: string;
  signal: string;
  movement: Movement;
}

export interface Alert {
  id: string;
  title: string;
  body: string;
  time: string;
  tone: "info" | "warning" | "success";
}

export interface NewsItem {
  id: string;
  category: string;
  title: string;
  summary: string;
  readTime: string;
}

export interface StatCard {
  id: string;
  label: string;
  value: number;
  suffix: string;
  prefix?: string;
  detail: string;
}

export interface SportsbookPromo {
  id: string;
  name: string;
  offer: string;
  detail: string;
  cta: string;
}

export interface MatchStats {
  possessionHome: number;
  possessionAway: number;
  shotsHome: number;
  shotsAway: number;
  xgHome: number;
  xgAway: number;
  cornersHome: number;
  cornersAway: number;
}

export interface Lineup {
  team: string;
  formation: string;
  players: string[];
}

export interface AIPickInput {
  matchId: string;
  matchContext: string;
  form: string;
  h2h: string;
  injuries: string;
  odds: Odds[];
}

export interface AIPickResult {
  winProbability: number;
  recommendation: string;
  confidence: number;
  topFantasyPicks: string[];
  riskNotes: string[];
}
