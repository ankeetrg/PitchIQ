"use client";

import { createContext, useContext, useEffect, useMemo, useState } from "react";
import { LIVE_MATCH, SCOREBOARD } from "@/lib/pitchiq-data";
import { driftAmericanOdds } from "@/lib/pitchiq-hooks";
import type { Match } from "@/lib/pitchiq-types";

const POLL_INTERVAL_MS = 30_000;

interface LiveMatchContextValue {
  match: Match;
  matches: Match[];
  oddsFlashKey: number;
  scoreFlashKey: number;
}

const LiveMatchContext = createContext<LiveMatchContextValue | null>(null);

function pickFeaturedMatch(matches: Match[]): Match {
  return (
    matches.find((m) => m.status === "live" || m.status === "halftime") ??
    matches.find((m) => m.status === "pre") ??
    matches[0] ??
    LIVE_MATCH
  );
}

export function LiveMatchProvider({ children }: { children: React.ReactNode }) {
  const [matches, setMatches] = useState<Match[]>(SCOREBOARD);
  const [match, setMatch] = useState<Match>(pickFeaturedMatch(SCOREBOARD));
  const [oddsFlashKey, setOddsFlashKey] = useState(0);
  const [scoreFlashKey, setScoreFlashKey] = useState(0);

  async function fetchScores() {
    try {
      const res = await fetch("/api/live-scores");
      if (!res.ok) return;
      const data = (await res.json()) as Match[];
      if (!Array.isArray(data) || data.length === 0) return;

      setMatches((prev) => {
        const prevFeatured = pickFeaturedMatch(prev);
        const nextFeatured = pickFeaturedMatch(data);

        if (
          nextFeatured.score.home !== prevFeatured.score.home ||
          nextFeatured.score.away !== prevFeatured.score.away
        ) {
          setScoreFlashKey((k) => k + 1);
        }

        setMatch(nextFeatured);
        return data;
      });
    } catch {
      // network error — keep showing last known state
    }
  }

  // initial fetch on mount
  useEffect(() => {
    fetchScores();
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  // poll every 30 seconds
  useEffect(() => {
    const id = window.setInterval(fetchScores, POLL_INTERVAL_MS);
    return () => window.clearInterval(id);
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  // odds drift: cosmetic micro-movement every 20s so the UI feels alive
  useEffect(() => {
    const id = window.setInterval(() => {
      setMatch((current) => ({
        ...current,
        odds: {
          ...current.odds,
          home: driftAmericanOdds(current.odds.home),
          draw: driftAmericanOdds(current.odds.draw),
          away: driftAmericanOdds(current.odds.away),
        },
      }));
      setOddsFlashKey((k) => k + 1);
    }, 20_000);
    return () => window.clearInterval(id);
  }, []);

  const value = useMemo(
    () => ({ match, matches, oddsFlashKey, scoreFlashKey }),
    [match, matches, oddsFlashKey, scoreFlashKey],
  );

  return <LiveMatchContext.Provider value={value}>{children}</LiveMatchContext.Provider>;
}

export function useLiveMatch() {
  const context = useContext(LiveMatchContext);
  if (!context) throw new Error("useLiveMatch must be used inside LiveMatchProvider");
  return context;
}
