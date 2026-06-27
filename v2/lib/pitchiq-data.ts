import type {
  Alert,
  AIPickResult,
  FantasyPick,
  GroupStandings,
  LineMovement,
  Lineup,
  Match,
  NewsItem,
  Odds,
  Parlay,
  ScheduleMatch,
  SportsbookPromo,
  StatCard,
  TickerItem,
} from "./pitchiq-types";

export const LIVE_MATCH: Match = {
  id: "fra-uru-2026-gb",
  competition: "FIFA World Cup 2026",
  group: "Group B",
  status: "live",
  minute: 67,
  clock: "67'",
  startTime: "Live now",
  venue: "MetLife Stadium",
  home: {
    name: "France",
    shortName: "FRA",
    fifaCode: "FRA",
    flagCode: "fr",
    record: "2-0-0",
    form: ["W", "W", "D", "W", "W"],
  },
  away: {
    name: "Uruguay",
    shortName: "URU",
    fifaCode: "URU",
    flagCode: "uy",
    record: "1-1-0",
    form: ["W", "D", "W", "L", "W"],
  },
  score: {
    home: 1,
    away: 0,
  },
  odds: {
    home: -185,
    draw: 310,
    away: 520,
    total: "2.5",
    spread: "France -0.5",
    book: "Consensus",
  },
  probabilities: {
    home: 68,
    draw: 20,
    away: 12,
  },
  stats: {
    xgHome: 1.84,
    xgAway: 0.71,
    shotsHome: 13,
    shotsAway: 7,
    possessionHome: 58,
    possessionAway: 42,
    cornersHome: 6,
    cornersAway: 3,
  },
  keyStats: [
    { label: "xG", value: "1.84 - 0.71", detail: "France pressure rising" },
    { label: "Shots", value: "13 - 7", detail: "5 on target" },
    { label: "Possession", value: "58%", detail: "France control" },
    { label: "Corners", value: "6 - 3", detail: "Set pieces edge" },
  ],
};

export const SCOREBOARD: Match[] = [
  LIVE_MATCH,
  {
    ...LIVE_MATCH,
    id: "usa-par-2026-ga",
    group: "Group A",
    status: "pre",
    minute: 0,
    clock: "8:00 PM ET",
    startTime: "8:00 PM ET",
    venue: "SoFi Stadium",
    home: {
      name: "United States",
      shortName: "USA",
      fifaCode: "USA",
      flagCode: "us",
      record: "1-0-1",
      form: ["W", "D", "W", "L", "W"],
    },
    away: {
      name: "Paraguay",
      shortName: "PAR",
      fifaCode: "PAR",
      flagCode: "py",
      record: "1-1-0",
      form: ["D", "W", "L", "W", "D"],
    },
    score: { home: 0, away: 0 },
    odds: {
      home: 125,
      draw: 225,
      away: 240,
      total: "2.5",
      spread: "USA -0.25",
      book: "Consensus",
    },
    probabilities: { home: 43, draw: 28, away: 29 },
    stats: {
      xgHome: 0,
      xgAway: 0,
      shotsHome: 0,
      shotsAway: 0,
      possessionHome: 50,
      possessionAway: 50,
      cornersHome: 0,
      cornersAway: 0,
    },
    keyStats: [
      { label: "Model", value: "43%", detail: "USA win probability" },
      { label: "Market", value: "+125", detail: "Consensus home price" },
      { label: "Total", value: "2.5", detail: "Balanced goal profile" },
      { label: "Kickoff", value: "8 PM", detail: "Prime-time window" },
    ],
  },
];

export const TICKER_ITEMS: TickerItem[] = [
  { id: "ticker-1", label: "Live", value: "France 1 - 0 Uruguay", status: "67'", accent: "red" },
  { id: "ticker-2", label: "Sharp move", value: "Spain -1.5 to -1.75", status: "12m ago", accent: "gold" },
  { id: "ticker-3", label: "Fantasy", value: "Mbappe captained in 41% of builds", status: "Hot", accent: "green" },
  { id: "ticker-4", label: "Alert", value: "Brazil lineup expected 70 minutes pre-kick", status: "Watch", accent: "blue" },
  { id: "ticker-5", label: "Odds", value: "USA total drops from 2.75 to 2.5", status: "Live", accent: "gold" },
];

export const STANDINGS: GroupStandings = {
  "Group A": [
    { team: "United States", flagCode: "us", played: 2, won: 1, drawn: 1, lost: 0, goalDiff: 3, points: 4 },
    { team: "Paraguay", flagCode: "py", played: 2, won: 1, drawn: 1, lost: 0, goalDiff: 1, points: 4 },
    { team: "Australia", flagCode: "au", played: 2, won: 1, drawn: 0, lost: 1, goalDiff: -1, points: 3 },
    { team: "Turkey", flagCode: "tr", played: 2, won: 0, drawn: 0, lost: 2, goalDiff: -3, points: 0 },
  ],
  "Group B": [
    { team: "France", flagCode: "fr", played: 2, won: 2, drawn: 0, lost: 0, goalDiff: 5, points: 6 },
    { team: "Uruguay", flagCode: "uy", played: 2, won: 1, drawn: 1, lost: 0, goalDiff: 2, points: 4 },
    { team: "Saudi Arabia", flagCode: "sa", played: 2, won: 0, drawn: 1, lost: 1, goalDiff: -2, points: 1 },
    { team: "Cape Verde", flagCode: "cv", played: 2, won: 0, drawn: 0, lost: 2, goalDiff: -5, points: 0 },
  ],
};

export const SCHEDULE: ScheduleMatch[] = [
  {
    id: "schedule-1",
    time: "3:00 PM ET",
    home: "Brazil",
    away: "Morocco",
    group: "Group C",
    venue: "Mercedes-Benz Stadium",
    tag: "AI lean: Brazil ML",
  },
  {
    id: "schedule-2",
    time: "6:00 PM ET",
    home: "Spain",
    away: "Saudi Arabia",
    group: "Group B",
    venue: "AT&T Stadium",
    tag: "Sharp: Spain -1.5",
  },
  {
    id: "schedule-3",
    time: "8:00 PM ET",
    home: "United States",
    away: "Paraguay",
    group: "Group A",
    venue: "SoFi Stadium",
    tag: "Fantasy: Pulisic chalk",
  },
];

export const FANTASY_PICKS: FantasyPick[] = [
  {
    id: "fp-1",
    player: "Kylian Mbappe",
    team: "France",
    flagCode: "fr",
    position: "FWD",
    salary: "$11.8k",
    projection: 18.7,
    ownership: "41%",
    edge: "+4.2",
    note: "Penalty equity plus highest shot volume on the slate.",
  },
  {
    id: "fp-2",
    player: "Antoine Griezmann",
    team: "France",
    flagCode: "fr",
    position: "MID",
    salary: "$8.9k",
    projection: 13.6,
    ownership: "24%",
    edge: "+2.9",
    note: "Set-piece floor keeps him viable even if France slows the match.",
  },
  {
    id: "fp-3",
    player: "Federico Valverde",
    team: "Uruguay",
    flagCode: "uy",
    position: "MID",
    salary: "$7.8k",
    projection: 11.1,
    ownership: "17%",
    edge: "+1.8",
    note: "Ball recoveries and late shots create comeback correlation.",
  },
  {
    id: "fp-4",
    player: "Theo Hernandez",
    team: "France",
    flagCode: "fr",
    position: "DEF",
    salary: "$6.4k",
    projection: 9.8,
    ownership: "19%",
    edge: "+2.1",
    note: "Advanced fullback role with clean-sheet upside.",
  },
  {
    id: "fp-5",
    player: "Sergio Rochet",
    team: "Uruguay",
    flagCode: "uy",
    position: "GK",
    salary: "$4.7k",
    projection: 6.9,
    ownership: "8%",
    edge: "+1.2",
    note: "Save volume path if Uruguay absorbs pressure.",
  },
  {
    id: "fp-6",
    player: "Vinicius Junior",
    team: "Brazil",
    flagCode: "br",
    position: "FWD",
    salary: "$10.9k",
    projection: 17.4,
    ownership: "32%",
    edge: "+3.7",
    note: "Best open-play creator in the Brazil-Morocco window.",
  },
  {
    id: "fp-7",
    player: "Achraf Hakimi",
    team: "Morocco",
    flagCode: "ma",
    position: "DEF",
    salary: "$6.9k",
    projection: 10.4,
    ownership: "13%",
    edge: "+2.4",
    note: "Counter-attacking assist equity at modest ownership.",
  },
  {
    id: "fp-8",
    player: "Christian Pulisic",
    team: "United States",
    flagCode: "us",
    position: "MID",
    salary: "$9.4k",
    projection: 14.8,
    ownership: "38%",
    edge: "+2.6",
    note: "Corner share and penalty equity make the floor stable.",
  },
];

export const PARLAY: Parlay = {
  title: "AI Parlay of the Day",
  payout: "+612",
  confidence: 71,
  rationale:
    "The model prefers correlated favorites with shot-volume floors and avoids thin plus-money narratives. This is AI-generated analysis, not financial advice.",
  legs: [
    { id: "leg-1", label: "France moneyline", odds: "-185", confidence: 78 },
    { id: "leg-2", label: "Brazil over 1.5 team goals", odds: "+105", confidence: 69 },
    { id: "leg-3", label: "USA draw no bet", odds: "-115", confidence: 66 },
  ],
};

export const LINE_MOVEMENT: LineMovement[] = [
  {
    id: "lm-1",
    match: "Spain vs Saudi Arabia",
    market: "Spread",
    open: "Spain -1.5",
    current: "Spain -1.75",
    move: "25pt steam",
    signal: "Sharp favorite pressure",
    movement: "up",
  },
  {
    id: "lm-2",
    match: "USA vs Paraguay",
    market: "Total",
    open: "2.75",
    current: "2.5",
    move: "Under money",
    signal: "Tempo downgrade after lineup note",
    movement: "down",
  },
  {
    id: "lm-3",
    match: "Brazil vs Morocco",
    market: "Moneyline",
    open: "Brazil -140",
    current: "Brazil -155",
    move: "Favorite support",
    signal: "Public and model aligned",
    movement: "up",
  },
];

export const ALERTS: Alert[] = [
  {
    id: "alert-1",
    title: "France goal probability climbs",
    body: "Live xG and final-third entries now project a 74% France win state.",
    time: "1m",
    tone: "success",
  },
  {
    id: "alert-2",
    title: "Brazil XI watch",
    body: "Expected lineup drops roughly 70 minutes before kickoff. Hold late swaps.",
    time: "12m",
    tone: "info",
  },
  {
    id: "alert-3",
    title: "USA total moved down",
    body: "Market shifted from 2.75 to 2.5 after training-note circulation.",
    time: "19m",
    tone: "warning",
  },
];

export const NEWS_ITEMS: NewsItem[] = [
  {
    id: "news-1",
    category: "Tactics",
    title: "France striker rotation turns one-way pressure into fantasy value",
    summary: "Wide overloads are creating a steady stream of box touches and a cleaner Mbappe captain path.",
    readTime: "4 min",
  },
  {
    id: "news-2",
    category: "Fantasy",
    title: "Vinicius Junior leads Brazil stacks, but the best salary relief is behind him",
    summary: "Brazil builds remain expensive. The defender pool is where projections are opening leverage.",
    readTime: "5 min",
  },
  {
    id: "news-3",
    category: "Betting",
    title: "Sharp money pushed Spain from -1.5 toward a heavier spread",
    summary: "The line move is real, but the price now demands a clean multi-goal script.",
    readTime: "3 min",
  },
  {
    id: "news-4",
    category: "DFS",
    title: "Three underowned defenders with crossing floors for tonight",
    summary: "Projected ownership still trails set-piece and open-play involvement in late-slate builds.",
    readTime: "6 min",
  },
];

export const STATS: StatCard[] = [
  { id: "stat-1", label: "Matches tracked", value: 47, suffix: "+", detail: "Live model slate" },
  { id: "stat-2", label: "Model hit rate", value: 64, suffix: "%", detail: "Back-tested picks" },
  { id: "stat-3", label: "Fantasy edges", value: 128, suffix: "", detail: "Player signals" },
  { id: "stat-4", label: "Odds updates", value: 920, suffix: "+", detail: "Market checks" },
];

export const SPORTSBOOK_PROMOS: SportsbookPromo[] = [
  {
    id: "promo-1",
    name: "DraftKings",
    offer: "World Cup odds boost",
    detail: "Compare legal-market prices before kickoff.",
    cta: "View Lines",
  },
  {
    id: "promo-2",
    name: "FanDuel",
    offer: "Soccer same-game builder",
    detail: "Track props, totals, and moneylines side by side.",
    cta: "Compare",
  },
  {
    id: "promo-3",
    name: "BetMGM",
    offer: "Live betting dashboard",
    detail: "Monitor second-half movement with PitchIQ context.",
    cta: "Explore",
  },
];

export const BEST_BETS = [
  {
    id: "bet-1",
    label: "France ML",
    odds: "-185",
    book: "Consensus",
    edge: "+5.4%",
    confidence: 78,
  },
  {
    id: "bet-2",
    label: "Brazil team total over 1.5",
    odds: "+105",
    book: "FanDuel",
    edge: "+3.1%",
    confidence: 69,
  },
  {
    id: "bet-3",
    label: "USA draw no bet",
    odds: "-115",
    book: "DraftKings",
    edge: "+2.7%",
    confidence: 66,
  },
] as const;

export const HARDCODED_ODDS: Odds[] = [
  {
    id: "odds-1",
    matchId: "fra-uru-2026-gb",
    sportsbook: "DraftKings",
    market: "h2h",
    outcomes: [
      { name: "France", price: -185 },
      { name: "Draw", price: 310 },
      { name: "Uruguay", price: 520 },
    ],
    lastUpdate: new Date(0).toISOString(),
  },
  {
    id: "odds-2",
    matchId: "fra-uru-2026-gb",
    sportsbook: "FanDuel",
    market: "totals",
    outcomes: [
      { name: "Over", price: -105, point: 2.5 },
      { name: "Under", price: -115, point: 2.5 },
    ],
    lastUpdate: new Date(0).toISOString(),
  },
];

export const FALLBACK_AI_PICK: AIPickResult = {
  winProbability: 68,
  recommendation: "France moneyline remains the preferred side while the live shot profile favors sustained pressure.",
  confidence: 71,
  topFantasyPicks: ["Kylian Mbappe", "Antoine Griezmann", "Theo Hernandez"],
  riskNotes: ["Price is no longer cheap", "Late Uruguay counters remain the main drawdown risk"],
};

export const FALLBACK_LINEUPS: Lineup[] = [
  {
    team: "France",
    formation: "4-2-3-1",
    players: ["Maignan", "Kounde", "Saliba", "Upamecano", "T. Hernandez", "Tchouameni", "Rabiot", "Dembele", "Griezmann", "Mbappe", "Thuram"],
  },
  {
    team: "Uruguay",
    formation: "4-3-3",
    players: ["Rochet", "Varela", "Gimenez", "Araujo", "Olivera", "Valverde", "Ugarte", "Bentancur", "Pellistri", "Nunez", "Araujo"],
  },
];
