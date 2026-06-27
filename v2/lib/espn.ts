import { SCOREBOARD, STANDINGS } from "./pitchiq-data";
import type { GroupStandings, Match, Team } from "./pitchiq-types";

const ESPN_SCOREBOARD_URL = "https://site.api.espn.com/apis/site/v2/sports/soccer/fifa.world/scoreboard";

interface ESPNTeam {
  displayName?: string;
  shortDisplayName?: string;
  abbreviation?: string;
  countryFlag?: string;
}

interface ESPNCompetitor {
  homeAway?: "home" | "away";
  score?: string;
  team?: ESPNTeam;
  records?: Array<{ summary?: string }>;
}

interface ESPNCompetition {
  id?: string;
  competitors?: ESPNCompetitor[];
  venue?: { fullName?: string };
  status?: {
    type?: {
      name?: string;
      state?: string;
      completed?: boolean;
      detail?: string;
      shortDetail?: string;
    };
  };
}

interface ESPNEvent {
  id?: string;
  name?: string;
  competitions?: ESPNCompetition[];
  date?: string;
  league?: { name?: string };
}

interface ESPNScoreboardResponse {
  events?: ESPNEvent[];
  leagues?: Array<{ name?: string }>;
}

function teamFromCompetitor(competitor: ESPNCompetitor | undefined, fallback: Team): Team {
  const team = competitor?.team;
  const flagCode = team?.countryFlag?.split("/").pop()?.replace(".png", "").slice(0, 2).toLowerCase() ?? fallback.flagCode;

  return {
    name: team?.displayName ?? fallback.name,
    shortName: team?.abbreviation ?? team?.shortDisplayName ?? fallback.shortName,
    fifaCode: team?.abbreviation ?? fallback.fifaCode,
    flagCode,
    record: competitor?.records?.[0]?.summary ?? fallback.record,
    form: fallback.form,
  };
}

function normalizeStatus(competition: ESPNCompetition | undefined): Match["status"] {
  if (competition?.status?.type?.completed) {
    return "fulltime";
  }

  const state = competition?.status?.type?.state;
  if (state === "in") {
    return "live";
  }

  return "pre";
}

function normalizeMatch(event: ESPNEvent, index: number): Match {
  const fallback = SCOREBOARD[index] ?? SCOREBOARD[0];
  const competition = event.competitions?.[0];
  const home = competition?.competitors?.find((competitor) => competitor.homeAway === "home");
  const away = competition?.competitors?.find((competitor) => competitor.homeAway === "away");
  const statusText = competition?.status?.type?.shortDetail ?? competition?.status?.type?.detail ?? fallback.clock;
  const minute = Number.parseInt(statusText.replace(/[^0-9]/g, ""), 10);

  return {
    ...fallback,
    id: event.id ?? fallback.id,
    competition: event.league?.name ?? fallback.competition,
    status: normalizeStatus(competition),
    minute: Number.isFinite(minute) ? minute : fallback.minute,
    clock: statusText,
    startTime: event.date ?? fallback.startTime,
    venue: competition?.venue?.fullName ?? fallback.venue,
    home: teamFromCompetitor(home, fallback.home),
    away: teamFromCompetitor(away, fallback.away),
    score: {
      home: Number.parseInt(home?.score ?? `${fallback.score.home}`, 10),
      away: Number.parseInt(away?.score ?? `${fallback.score.away}`, 10),
    },
  };
}

export async function getLiveScores(): Promise<Match[]> {
  try {
    const response = await fetch(ESPN_SCOREBOARD_URL, {
      next: { revalidate: 30 },
    });

    if (!response.ok) {
      return SCOREBOARD;
    }

    const data = (await response.json()) as ESPNScoreboardResponse;
    const events = data.events ?? [];

    if (events.length === 0) {
      return SCOREBOARD;
    }

    return events.map(normalizeMatch);
  } catch {
    return SCOREBOARD;
  }
}

export async function getStandings(): Promise<GroupStandings> {
  return STANDINGS;
}
