import { FALLBACK_LINEUPS, FANTASY_PICKS, LIVE_MATCH } from "./pitchiq-data";
import type { FantasyPick, Lineup, MatchStats } from "./pitchiq-types";

const STATS_API_BASE = "https://api.thestatsapi.com/api";
const COMPETITION_ID = "comp_6107";
const SEASON_ID = "sn_118868";

interface PlayerStatsResponse {
  data?: Array<{
    id?: string;
    player_name?: string;
    team_name?: string;
    position?: FantasyPick["position"];
    projection?: number;
  }>;
}

async function statsFetch<T>(path: string, revalidate: number): Promise<T | null> {
  const token = process.env.THESTATSAPI_KEY;

  if (!token) {
    return null;
  }

  try {
    const response = await fetch(`${STATS_API_BASE}${path}`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
      next: { revalidate },
    });

    if (!response.ok) {
      return null;
    }

    return (await response.json()) as T;
  } catch {
    return null;
  }
}

export async function getPlayerStats(): Promise<FantasyPick[]> {
  const data = await statsFetch<PlayerStatsResponse>(
    `/player-stats?competition_id=${COMPETITION_ID}&season_id=${SEASON_ID}`,
    300,
  );

  if (!data?.data?.length) {
    return FANTASY_PICKS;
  }

  return data.data.slice(0, 16).map((player, index) => ({
    id: player.id ?? `api-player-${index}`,
    player: player.player_name ?? FANTASY_PICKS[index % FANTASY_PICKS.length].player,
    team: player.team_name ?? FANTASY_PICKS[index % FANTASY_PICKS.length].team,
    flagCode: FANTASY_PICKS[index % FANTASY_PICKS.length].flagCode,
    position: player.position ?? FANTASY_PICKS[index % FANTASY_PICKS.length].position,
    salary: FANTASY_PICKS[index % FANTASY_PICKS.length].salary,
    projection: player.projection ?? FANTASY_PICKS[index % FANTASY_PICKS.length].projection,
    ownership: FANTASY_PICKS[index % FANTASY_PICKS.length].ownership,
    edge: FANTASY_PICKS[index % FANTASY_PICKS.length].edge,
    note: FANTASY_PICKS[index % FANTASY_PICKS.length].note,
  }));
}

export async function getLiveMatchStats(matchId: string): Promise<MatchStats> {
  const data = await statsFetch<Partial<MatchStats>>(`/matches/${matchId}/stats`, 30);

  return {
    possessionHome: data?.possessionHome ?? LIVE_MATCH.stats.possessionHome,
    possessionAway: data?.possessionAway ?? LIVE_MATCH.stats.possessionAway,
    shotsHome: data?.shotsHome ?? LIVE_MATCH.stats.shotsHome,
    shotsAway: data?.shotsAway ?? LIVE_MATCH.stats.shotsAway,
    xgHome: data?.xgHome ?? LIVE_MATCH.stats.xgHome,
    xgAway: data?.xgAway ?? LIVE_MATCH.stats.xgAway,
    cornersHome: data?.cornersHome ?? LIVE_MATCH.stats.cornersHome,
    cornersAway: data?.cornersAway ?? LIVE_MATCH.stats.cornersAway,
  };
}

export async function getLineups(matchId: string): Promise<Lineup[]> {
  const data = await statsFetch<{ data?: Lineup[] }>(`/matches/${matchId}/lineups`, 30);

  return data?.data?.length ? data.data : FALLBACK_LINEUPS;
}
