import { HARDCODED_ODDS } from "./pitchiq-data";
import type { Odds } from "./pitchiq-types";

// LEGAL-REVIEW-REQUIRED: odds data is informational and must be reviewed before production wagering UI activation.
const ODDS_API_URL = "https://api.the-odds-api.com/v4/sports/soccer_fifa_world_cup/odds";

interface OddsApiOutcome {
  name?: string;
  price?: number;
  point?: number;
}

interface OddsApiMarket {
  key?: "h2h" | "spreads" | "totals";
  outcomes?: OddsApiOutcome[];
}

interface OddsApiBookmaker {
  key?: string;
  title?: string;
  last_update?: string;
  markets?: OddsApiMarket[];
}

interface OddsApiEvent {
  id?: string;
  home_team?: string;
  away_team?: string;
  bookmakers?: OddsApiBookmaker[];
}

function normalizeOdds(event: OddsApiEvent): Odds[] {
  const matchId = event.id ?? `${event.home_team ?? "home"}-${event.away_team ?? "away"}`;
  const odds: Odds[] = [];

  event.bookmakers?.forEach((bookmaker) => {
    bookmaker.markets?.forEach((market) => {
      if (!market.key) {
        return;
      }

      odds.push({
        id: `${matchId}-${bookmaker.key ?? bookmaker.title ?? "book"}-${market.key}`,
        matchId,
        sportsbook: bookmaker.title ?? bookmaker.key ?? "Unknown",
        market: market.key,
        outcomes: (market.outcomes ?? [])
          .filter((outcome): outcome is OddsApiOutcome & { name: string; price: number } => typeof outcome.name === "string" && typeof outcome.price === "number")
          .map((outcome) => ({
            name: outcome.name,
            price: outcome.price,
            point: outcome.point,
          })),
        lastUpdate: bookmaker.last_update ?? new Date().toISOString(),
      });
    });
  });

  return odds;
}

export async function getMatchOdds(matchId?: string): Promise<Odds[]> {
  const apiKey = process.env.ODDS_API_KEY;

  if (!apiKey) {
    return matchId ? HARDCODED_ODDS.filter((odds) => odds.matchId === matchId) : HARDCODED_ODDS;
  }

  try {
    const url = new URL(ODDS_API_URL);
    url.searchParams.set("apiKey", apiKey);
    url.searchParams.set("regions", "us");
    url.searchParams.set("markets", "h2h,spreads,totals");

    const response = await fetch(url, {
      next: { revalidate: 60 },
    });

    if (!response.ok) {
      return matchId ? HARDCODED_ODDS.filter((odds) => odds.matchId === matchId) : HARDCODED_ODDS;
    }

    const events = (await response.json()) as OddsApiEvent[];
    const normalized = events.flatMap(normalizeOdds);
    const filtered = matchId ? normalized.filter((odds) => odds.matchId === matchId) : normalized;
    return filtered.length > 0 ? filtered : HARDCODED_ODDS;
  } catch {
    return matchId ? HARDCODED_ODDS.filter((odds) => odds.matchId === matchId) : HARDCODED_ODDS;
  }
}
