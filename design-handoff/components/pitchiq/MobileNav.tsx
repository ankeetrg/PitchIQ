"use client";

import { useState } from "react";
import { mobNav } from "./data";

export function MobileNav() {
  const [active, setActive] = useState(0);
  return (
    <nav className="mob-nav" aria-label="Mobile">
      <div className="mob-nav-inner">
        {mobNav.map((b, i) => (
          <button
            key={b.label}
            className={`mob-nav-btn${active === i ? " active" : ""}`}
            onClick={() => setActive(i)}
          >
            <span className="icon">{b.icon}</span>
            {b.label}
          </button>
        ))}
      </div>
    </nav>
  );
}
