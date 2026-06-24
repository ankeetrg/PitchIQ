"use client";

import { useState } from "react";
import { useApp } from "@/app/providers";
import { navLinks } from "./data";

function SunIcon() {
  return (
    <svg
      className="icon-sun"
      xmlns="http://www.w3.org/2000/svg"
      width="18"
      height="18"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <circle cx="12" cy="12" r="5" />
      <line x1="12" y1="1" x2="12" y2="3" />
      <line x1="12" y1="21" x2="12" y2="23" />
      <line x1="4.22" y1="4.22" x2="5.64" y2="5.64" />
      <line x1="18.36" y1="18.36" x2="19.78" y2="19.78" />
      <line x1="1" y1="12" x2="3" y2="12" />
      <line x1="21" y1="12" x2="23" y2="12" />
      <line x1="4.22" y1="19.78" x2="5.64" y2="18.36" />
      <line x1="18.36" y1="5.64" x2="19.78" y2="4.22" />
    </svg>
  );
}

function MoonIcon() {
  return (
    <svg
      className="icon-moon"
      xmlns="http://www.w3.org/2000/svg"
      width="17"
      height="17"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z" />
    </svg>
  );
}

export function Navbar() {
  const { toggleTheme } = useApp();
  const [open, setOpen] = useState(false);

  return (
    <nav className="nav" aria-label="Primary">
      <div className="nav-inner w">
        <a className="nav-logo" href="#">
          Pitch<span>IQ</span>
        </a>
        <div className="nav-links" style={open ? { display: "flex" } : undefined}>
          {navLinks.map((l) => (
            <a key={l.label} href="#" className={l.active ? "active" : undefined}>
              {l.label}
              {l.isNew ? <span className="nav-new">NEW</span> : null}
            </a>
          ))}
        </div>
        <div className="nav-right">
          <button
            className="theme-toggle"
            aria-label="Toggle dark mode"
            onClick={toggleTheme}
          >
            <SunIcon />
            <MoonIcon />
          </button>
        </div>
        <button
          className="nav-burger"
          aria-label="Menu"
          aria-expanded={open}
          onClick={() => setOpen((o) => !o)}
        >
          ☰
        </button>
      </div>
    </nav>
  );
}
