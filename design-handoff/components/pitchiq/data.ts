/* ═══════════════════════════════════════════
   PITCHIQ · Hardcoded demo data (World Cup 2026)
═══════════════════════════════════════════ */

export type Pos = "FWD" | "MID" | "DEF" | "GK";

export interface TickItem {
  status: "live" | "ft" | "ko";
  statusLabel: string;
  home: string;
  away: string;
  score?: string;
  trailing?: string; // e.g. live minute
  /** marks the France–Uruguay live match so the score can sync with the sim */
  liveMatch?: boolean;
}

export const tickerItems: TickItem[] = [
  { status: "live", statusLabel: "LIVE", home: "FRA", away: "URU", score: "1–0", trailing: "67'", liveMatch: true },
  { status: "ft", statusLabel: "FT", home: "MEX", away: "RSA", score: "2–0" },
  { status: "ft", statusLabel: "FT", home: "KOR", away: "CZE", score: "2–1" },
  { status: "ft", statusLabel: "FT", home: "CAN", away: "BIH", score: "1–1" },
  { status: "ft", statusLabel: "FT", home: "USA", away: "PAR", score: "4–1" },
  { status: "ko", statusLabel: "3PM ET", home: "QAT", away: "SUI" },
  { status: "ko", statusLabel: "6PM ET", home: "BRA", away: "MAR" },
  { status: "ko", statusLabel: "9PM ET", home: "HTI", away: "SCO" },
];

export const navLinks = [
  { label: "Scores", active: false },
  { label: "World Cup", active: true },
  { label: "Fantasy", active: false },
  { label: "Betting", active: false },
  { label: "Analysis", active: false },
  { label: "News", active: false, isNew: true },
];

export interface Fixture {
  status: "live" | "ft" | "ko";
  statusLabel: string;
  match: string;
  meta: string;
  score: string;
  scoreUpcoming?: boolean;
  liveMatch?: boolean;
}

export const fixtures: Fixture[] = [
  { status: "live", statusLabel: "LIVE", match: "France vs Uruguay", meta: "Group E · ", score: "1–0", liveMatch: true },
  { status: "ft", statusLabel: "FT", match: "Argentina vs Australia", meta: "Group A · Full Time", score: "2–1" },
  { status: "ft", statusLabel: "FT", match: "Germany vs Saudi Arabia", meta: "Group B · Full Time", score: "4–0" },
  { status: "ko", statusLabel: "6PM", match: "Spain vs Mexico", meta: "Group C · MetLife Stadium", score: "6:00 PM", scoreUpcoming: true },
  { status: "ko", statusLabel: "9PM", match: "Brazil vs Colombia", meta: "Group D · Allegiant Stadium", score: "9:00 PM", scoreUpcoming: true },
  { status: "ko", statusLabel: "9PM", match: "Portugal vs South Korea", meta: "Group F · AT&T Stadium", score: "9:00 PM", scoreUpcoming: true },
];

export interface BestBet {
  name: string;
  meta: string;
  tag: string;
  tagKind?: "value" | "hot" | "sharp";
  odds: string;
}

export const bestBets: BestBet[] = [
  { name: "France –1.5 Goals", meta: "FRA vs URU · Group E", tag: "VALUE", tagKind: "value", odds: "+118" },
  { name: "Spain Win & BTTS", meta: "ESP vs MEX · Group C", tag: "VALUE", tagKind: "value", odds: "+195" },
  { name: "Mbappé Anytime Scorer", meta: "FRA vs URU · Group E", tag: "HOT", tagKind: "hot", odds: "-130" },
  { name: "Brazil Over 2.5 Goals", meta: "BRA vs COL · Group D", tag: "SHARP", tagKind: "sharp", odds: "-120" },
];

export const sportsbooks = [
  { name: "DraftKings", offer: "Bet $5, Get $200" },
  { name: "FanDuel", offer: "$150 in Bonus Bets" },
  { name: "BetMGM", offer: "$1,500 First Bet" },
  { name: "Caesars", offer: "$1,000 First Bet" },
];

export interface StatItem {
  count: number;
  suffix?: string;
  label: string;
}

export const stats: StatItem[] = [
  { count: 64, label: "Matches Covered" },
  { count: 1800, label: "Players Ranked" },
  { count: 72, suffix: "%", label: "AI Pick Accuracy" },
  { count: 50000, label: "Daily Simulations" },
  { count: 1, suffix: "M+", label: "Active Users" },
  { count: 24, suffix: "/7", label: "Live Coverage" },
];

export interface StandingRow {
  flag: string;
  name: string;
  p: number;
  w: number;
  d: number;
  gd: string;
  pts: number;
}

export interface Group {
  letter: string;
  sub: string;
  rows: StandingRow[];
}

export const groups: Group[] = [
  {
    letter: "Group A",
    sub: "MD 1 of 3",
    rows: [
      { flag: "🇦🇷", name: "Argentina", p: 1, w: 1, d: 0, gd: "+1", pts: 3 },
      { flag: "🇵🇱", name: "Poland", p: 1, w: 1, d: 0, gd: "+1", pts: 3 },
      { flag: "🇦🇺", name: "Australia", p: 1, w: 0, d: 0, gd: "-1", pts: 0 },
      { flag: "🇸🇳", name: "Senegal", p: 1, w: 0, d: 0, gd: "-1", pts: 0 },
    ],
  },
  {
    letter: "Group B",
    sub: "MD 1 of 3",
    rows: [
      { flag: "🇩🇪", name: "Germany", p: 1, w: 1, d: 0, gd: "+4", pts: 3 },
      { flag: "🇯🇵", name: "Japan", p: 1, w: 1, d: 0, gd: "+1", pts: 3 },
      { flag: "🇨🇷", name: "Costa Rica", p: 1, w: 0, d: 0, gd: "-1", pts: 0 },
      { flag: "🇸🇦", name: "Saudi Arabia", p: 1, w: 0, d: 0, gd: "-4", pts: 0 },
    ],
  },
  {
    letter: "Group C",
    sub: "Kicks off 6PM",
    rows: [
      { flag: "🇪🇸", name: "Spain", p: 0, w: 0, d: 0, gd: "0", pts: 0 },
      { flag: "🇲🇽", name: "Mexico", p: 0, w: 0, d: 0, gd: "0", pts: 0 },
      { flag: "🇭🇷", name: "Croatia", p: 0, w: 0, d: 0, gd: "0", pts: 0 },
      { flag: "🇨🇦", name: "Canada", p: 0, w: 0, d: 0, gd: "0", pts: 0 },
    ],
  },
  {
    letter: "Group D",
    sub: "Kicks off 9PM",
    rows: [
      { flag: "🇧🇷", name: "Brazil", p: 0, w: 0, d: 0, gd: "0", pts: 0 },
      { flag: "🇨🇴", name: "Colombia", p: 0, w: 0, d: 0, gd: "0", pts: 0 },
      { flag: "🇨🇭", name: "Switzerland", p: 0, w: 0, d: 0, gd: "0", pts: 0 },
      { flag: "🇬🇭", name: "Ghana", p: 0, w: 0, d: 0, gd: "0", pts: 0 },
    ],
  },
];

export interface ScheduleRow {
  status: "live" | "ft" | "ko";
  statusLabel: string;
  match: string;
  score: string;
  liveMatch?: boolean;
}

export const schedule: ScheduleRow[] = [
  { status: "live", statusLabel: "LIVE", match: "France vs Uruguay", score: "1–0", liveMatch: true },
  { status: "ft", statusLabel: "FT", match: "Argentina vs Australia", score: "2–1" },
  { status: "ft", statusLabel: "FT", match: "Germany vs Saudi Arabia", score: "4–0" },
  { status: "ft", statusLabel: "FT", match: "England vs USA", score: "3–0" },
  { status: "ko", statusLabel: "6PM", match: "Spain vs Mexico", score: "6:00 PM" },
  { status: "ko", statusLabel: "9PM", match: "Brazil vs Colombia", score: "9:00 PM" },
  { status: "ko", statusLabel: "9PM", match: "Portugal vs South Korea", score: "9:00 PM" },
  { status: "ko", statusLabel: "JUN 13", match: "Netherlands vs Ecuador", score: "12:00 PM" },
];

export interface Player {
  rank: number;
  flag: string;
  name: string;
  nation: string;
  pos: Pos;
  matchTeam: string;
  opp: string;
  proj: string;
  own: string;
  trend: string;
  trendKind: "up" | "down" | "flat";
}

export const players: Player[] = [
  { rank: 1, flag: "🇫🇷", name: "Kylian Mbappé", nation: "France", pos: "FWD", matchTeam: "FRA", opp: "vs URU", proj: "9.2", own: "68.4%", trend: "↑ +1.8", trendKind: "up" },
  { rank: 2, flag: "🇧🇷", name: "Vinicius Jr.", nation: "Brazil", pos: "FWD", matchTeam: "BRA", opp: "vs COL", proj: "8.7", own: "54.2%", trend: "↑ +0.9", trendKind: "up" },
  { rank: 3, flag: "🇳🇴", name: "Erling Haaland", nation: "Norway", pos: "FWD", matchTeam: "NOR", opp: "vs GHA", proj: "8.4", own: "71.1%", trend: "→ 0.0", trendKind: "flat" },
  { rank: 4, flag: "🇵🇹", name: "Bruno Fernandes", nation: "Portugal", pos: "MID", matchTeam: "POR", opp: "vs KOR", proj: "7.8", own: "41.3%", trend: "↑ +2.1", trendKind: "up" },
  { rank: 5, flag: "🇪🇸", name: "Pedri", nation: "Spain", pos: "MID", matchTeam: "ESP", opp: "vs MEX", proj: "7.6", own: "38.9%", trend: "↓ −0.4", trendKind: "down" },
  { rank: 6, flag: "🇵🇹", name: "Rúben Dias", nation: "Portugal", pos: "DEF", matchTeam: "POR", opp: "vs KOR", proj: "6.8", own: "29.7%", trend: "↑ +0.8", trendKind: "up" },
  { rank: 7, flag: "🇧🇷", name: "Alisson", nation: "Brazil", pos: "GK", matchTeam: "BRA", opp: "vs COL", proj: "6.4", own: "22.1%", trend: "→ 0.0", trendKind: "flat" },
];

export interface ParlayLeg {
  name: string;
  match: string;
  odds: string;
  conf: number;
}

export const parlay = {
  odds: "+485",
  legs: [
    { name: "Brazil Win", match: "BRA vs COL · Group D", odds: "−138", conf: 71 },
    { name: "Germany Over 3.5 Goals", match: "GER vs KSA · Group B", odds: "+110", conf: 64 },
    { name: "Spain Win to Nil", match: "ESP vs MEX · Group C", odds: "−110", conf: 68 },
  ] as ParlayLeg[],
};

export interface LineMove {
  tag: string;
  tagKind: "sharp" | "hot" | "value" | "public";
  name: string;
  match: string;
  open: string;
  now: string;
  move: string;
  moveKind: "up" | "down";
}

export const lineMoves: LineMove[] = [
  { tag: "Sharp", tagKind: "sharp", name: "Uruguay Moneyline", match: "FRA vs URU · Group E", open: "+420", now: "+380", move: "▼ 40", moveKind: "down" },
  { tag: "Hot", tagKind: "hot", name: "Mbappé Anytime Scorer", match: "FRA vs URU · Group E", open: "−115", now: "−130", move: "▲ 15", moveKind: "up" },
  { tag: "Value", tagKind: "value", name: "Spain −1.5 Goals", match: "ESP vs MEX · Group C", open: "+135", now: "+118", move: "▼ 17", moveKind: "down" },
  { tag: "Public", tagKind: "public", name: "Brazil Over 2.5 Goals", match: "BRA vs COL · Group D", open: "−110", now: "−120", move: "▲ 10", moveKind: "up" },
];

export interface NewsCard {
  variant: "france" | "brazil" | "betting" | "fantasy";
  icon: string;
  cat: string;
  headline: string;
  by: string;
  date: string;
  read: string;
  featured?: boolean;
}

export const news: NewsCard[] = [
  {
    variant: "france",
    icon: "🏆",
    cat: "Featured Analysis",
    headline:
      "France's Striker Revolution: Why Deschamps' Bold System Change Makes Les Bleus the 2026 Favorites",
    by: "James Walker",
    date: "Jun 12, 2026",
    read: "9 min read",
    featured: true,
  },
  {
    variant: "brazil",
    icon: "⚽",
    cat: "Fantasy",
    headline: "Vinicius Jr. vs. Colombia's Leaky Defense: The Fantasy Differential of Matchday 1",
    by: "Sarah Kim",
    date: "Jun 12, 2026",
    read: "5 min read",
  },
  {
    variant: "betting",
    icon: "📊",
    cat: "Betting",
    headline: "Sharp Money Is Hammering Spain –1.5 Against Mexico: Here's Why the Model Agrees",
    by: "Carlos Rivera",
    date: "Jun 12, 2026",
    read: "4 min read",
  },
];

export interface Alert {
  kind: "goal" | "yellow" | "doubt" | "fit" | "news";
  icon: string;
  player: string;
  msg: string;
  time: string;
}

export const alerts: Alert[] = [
  { kind: "goal", icon: "⚽", player: "Folarin Balogun", msg: "Goal vs Uruguay — assist to fantasy owners (54% rostered)", time: "2 min ago" },
  { kind: "yellow", icon: "🟨", player: "Kylian Mbappé", msg: "Yellow card, 84' — one away from suspension", time: "6 min ago" },
  { kind: "doubt", icon: "❓", player: "Vinicius Jr.", msg: "Late fitness test — listed as a game-time decision vs Colombia", time: "22 min ago" },
  { kind: "fit", icon: "✅", player: "Erling Haaland", msg: "Passed fitness test — confirmed to start vs Ghana", time: "38 min ago" },
  { kind: "goal", icon: "⚽", player: "Heung-min Son", msg: "Goal in warmup fixture — in form ahead of Portugal clash", time: "51 min ago" },
  { kind: "news", icon: "📰", player: "Lionel Messi", msg: "Rested for Argentina opener — expected back for Matchday 2", time: "1 hr ago" },
];

export const footerCols = [
  {
    title: "World Cup 2026",
    links: ["Match Schedule", "Group Standings", "Player Stats", "AI Predictions", "Bracket Tracker"],
  },
  {
    title: "Fantasy",
    links: ["Player Rankings", "Daily Picks", "Ownership %", "Injury Report", "Draft Assistant"],
  },
  {
    title: "Betting",
    links: ["Today's Best Bets", "Odds Tracker", "Line Movement", "Sharp Reports", "Sportsbooks"],
  },
];

export const mobNav = [
  { icon: "🏠", label: "Home" },
  { icon: "⚽", label: "Scores" },
  { icon: "🌟", label: "Fantasy" },
  { icon: "📊", label: "Betting" },
  { icon: "👤", label: "Account" },
];
