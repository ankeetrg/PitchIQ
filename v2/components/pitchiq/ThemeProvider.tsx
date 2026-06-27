"use client";

import { createContext, useCallback, useContext, useEffect, useMemo, useState } from "react";
import type { Theme } from "@/lib/pitchiq-types";

interface ThemeContextValue {
  theme: Theme;
  toggleTheme: () => void;
  setPitchiqTheme: (theme: Theme) => void;
}

const ThemeContext = createContext<ThemeContextValue | null>(null);

function getStoredTheme(): Theme {
  if (typeof window === "undefined") {
    return "dark";
  }

  const stored = window.localStorage.getItem("pitchiq-theme");
  return stored === "light" || stored === "dark" ? stored : "dark";
}

export function ThemeProvider({ children }: { children: React.ReactNode }) {
  const [theme, setTheme] = useState<Theme>("dark");

  useEffect(() => {
    const stored = getStoredTheme();
    setTheme(stored);
    document.documentElement.setAttribute("data-theme", stored);
  }, []);

  const setPitchiqTheme = useCallback((nextTheme: Theme) => {
    const root = document.documentElement;
    root.classList.add("theme-switching");
    root.setAttribute("data-theme", nextTheme);
    window.localStorage.setItem("pitchiq-theme", nextTheme);
    setTheme(nextTheme);

    window.setTimeout(() => {
      root.classList.remove("theme-switching");
    }, 400);
  }, []);

  const toggleTheme = useCallback(() => {
    setPitchiqTheme(theme === "dark" ? "light" : "dark");
  }, [setPitchiqTheme, theme]);

  const value = useMemo(
    () => ({
      theme,
      toggleTheme,
      setPitchiqTheme,
    }),
    [setPitchiqTheme, theme, toggleTheme],
  );

  return <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>;
}

export function useTheme() {
  const context = useContext(ThemeContext);

  if (!context) {
    throw new Error("useTheme must be used inside ThemeProvider");
  }

  return context;
}
