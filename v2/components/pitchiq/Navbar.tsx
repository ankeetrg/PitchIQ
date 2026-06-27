"use client";

import { Moon, Sun } from "lucide-react";
import { useTheme } from "./ThemeProvider";

const navItems = ["Predictions", "Fantasy", "Standings", "News"];

export function Navbar() {
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="sticky top-11 z-[190] border-b border-[rgba(255,255,255,0.08)] bg-navy text-white shadow-[0_8px_30px_rgba(0,0,0,0.18)]">
      <div className="max-shell flex h-16 items-center justify-between gap-5">
        <a href="#" className="flex items-center gap-3" aria-label="PitchIQ home">
          <span className="flex h-10 w-10 items-center justify-center rounded-md bg-gold text-lg font-black text-white">
            IQ
          </span>
          <span className="font-cond text-3xl font-black uppercase leading-none tracking-normal">
            Pitch<span className="text-gold">IQ</span>
          </span>
        </a>

        <nav className="hidden items-center gap-7 md:flex" aria-label="Primary navigation">
          {navItems.map((item) => (
            <a key={item} href={`#${item.toLowerCase()}`} className="text-sm font-bold text-white/72 transition hover:text-white">
              {item}
            </a>
          ))}
        </nav>

        <div className="flex items-center gap-3">
          <a
            href="#newsletter"
            className="hidden rounded-md bg-green px-4 py-2 text-sm font-black text-white transition hover:bg-green-hover sm:inline-flex"
          >
            Get Alerts
          </a>
          <button
            type="button"
            onClick={toggleTheme}
            className="flex h-10 w-10 items-center justify-center rounded-md border border-white/12 bg-white/5 text-white transition hover:bg-white/10"
            aria-label={`Switch to ${theme === "dark" ? "light" : "dark"} theme`}
          >
            {theme === "dark" ? <Sun size={18} /> : <Moon size={18} />}
          </button>
        </div>
      </div>
    </header>
  );
}
