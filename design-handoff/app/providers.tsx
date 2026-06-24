"use client";

import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useRef,
  useState,
  type ReactNode,
} from "react";

type Theme = "light" | "dark";

interface MatchState {
  min: number;
  home: number;
  away: number;
  live: boolean;
}

interface Odds {
  fra: number;
  draw: number;
  uru: number;
  ou: number;
}

interface Prob {
  h: number;
  d: number;
  a: number;
}

interface AppContextValue {
  theme: Theme;
  toggleTheme: () => void;
  toast: { msg: string; id: number; show: boolean };
  showToast: (msg: string) => void;
  match: MatchState;
  scoreFlashId: number;
  odds: Odds;
  prob: Prob;
  cricketOpen: boolean;
  setCricketOpen: (v: boolean) => void;
}

const AppContext = createContext<AppContextValue | null>(null);

export function useApp(): AppContextValue {
  const ctx = useContext(AppContext);
  if (!ctx) throw new Error("useApp must be used within AppProvider");
  return ctx;
}

export function AppProvider({ children }: { children: ReactNode }) {
  /* ── THEME ─────────────────────────────── */
  const [theme, setTheme] = useState<Theme>("light");

  useEffect(() => {
    const current = (document.documentElement.dataset.theme as Theme) || "light";
    setTheme(current);
  }, []);

  const toggleTheme = useCallback(() => {
    setTheme((prev) => {
      const next: Theme = prev === "dark" ? "light" : "dark";
      const root = document.documentElement;
      root.classList.add("theme-switching");
      root.dataset.theme = next;
      try {
        localStorage.setItem("pitchiq-theme", next);
      } catch {
        /* ignore */
      }
      window.setTimeout(() => root.classList.remove("theme-switching"), 400);
      return next;
    });
  }, []);

  /* ── TOAST ─────────────────────────────── */
  const [toast, setToast] = useState({ msg: "", id: 0, show: false });
  const toastTimer = useRef<number | undefined>(undefined);

  const showToast = useCallback((msg: string) => {
    setToast((t) => ({ msg, id: t.id + 1, show: true }));
    window.clearTimeout(toastTimer.current);
    toastTimer.current = window.setTimeout(
      () => setToast((t) => ({ ...t, show: false })),
      2800
    );
  }, []);

  /* ── LIVE MATCH SIMULATION ─────────────── */
  const [match, setMatch] = useState<MatchState>({
    min: 67,
    home: 1,
    away: 0,
    live: true,
  });
  const [scoreFlashId, setScoreFlashId] = useState(0);
  const [odds, setOdds] = useState<Odds>({ fra: -140, draw: 290, uru: 380, ou: -110 });
  const [prob, setProb] = useState<Prob>({ h: 65, d: 20, a: 15 });

  const simRef = useRef<MatchState>({ min: 67, home: 1, away: 0, live: true });
  const firedRef = useRef<Set<number>>(new Set());

  const driftOdds = useCallback(
    (fraD: number, drawD: number, uruD: number, ouD: number) => {
      setOdds((o) => ({
        fra: o.fra + fraD,
        draw: o.draw + drawD,
        uru: o.uru + uruD,
        ou: o.ou + ouD,
      }));
    },
    []
  );

  useEffect(() => {
    const id = window.setInterval(() => {
      const s = simRef.current;
      if (!s.live) return;
      s.min += 1;

      // GOAL — 73'
      if (s.min >= 73 && !firedRef.current.has(73)) {
        firedRef.current.add(73);
        s.home += 1;
        setProb({ h: 80, d: 13, a: 7 });
        setScoreFlashId((n) => n + 1);
        showToast("⚽ GOAL! Mbappé 73' — France 2–0 Uruguay");
        driftOdds(-20, 30, 60, 5);
      }
      // YELLOW — 84'
      if (s.min >= 84 && !firedRef.current.has(84)) {
        firedRef.current.add(84);
        showToast("🟨 Yellow Card — Giménez (Uruguay) 84'");
      }
      // INJURY TIME — 90'
      if (s.min >= 90 && !firedRef.current.has(90)) {
        firedRef.current.add(90);
        showToast("🕐 +4 min injury time added");
      }
      // FULL TIME — 94'
      if (s.min >= 94 && !firedRef.current.has(94)) {
        firedRef.current.add(94);
        s.live = false;
        showToast("🔔 Full Time — France 2–0 Uruguay");
      }

      setMatch({ min: s.min, home: s.home, away: s.away, live: s.live });
    }, 1500);

    return () => window.clearInterval(id);
  }, [driftOdds, showToast]);

  /* random small drift every 20s */
  useEffect(() => {
    const id = window.setInterval(() => {
      const rand = () => (Math.random() > 0.5 ? 5 : -5);
      driftOdds(rand(), rand() * 2, rand() * 2, rand());
    }, 20000);
    return () => window.clearInterval(id);
  }, [driftOdds]);

  /* ── CRICKET MODAL ─────────────────────── */
  const [cricketOpen, setCricketOpen] = useState(false);

  const value: AppContextValue = {
    theme,
    toggleTheme,
    toast,
    showToast,
    match,
    scoreFlashId,
    odds,
    prob,
    cricketOpen,
    setCricketOpen,
  };

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>;
}
