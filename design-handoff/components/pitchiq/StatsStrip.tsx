"use client";

import { animate, useInView } from "framer-motion";
import { useEffect, useRef, useState } from "react";
import { stats, type StatItem } from "./data";

function StatNumber({ stat }: { stat: StatItem }) {
  const ref = useRef<HTMLDivElement>(null);
  const inView = useInView(ref, { once: true, amount: 0.4 });
  const [display, setDisplay] = useState("0");

  useEffect(() => {
    if (!inView) return;
    const controls = animate(0, stat.count, {
      duration: 1.4,
      ease: [0.25, 0, 0.1, 1],
      onUpdate(value) {
        const v = Math.round(value);
        setDisplay((v >= 1000 ? v.toLocaleString() : String(v)) + (stat.suffix || ""));
      },
    });
    return () => controls.stop();
  }, [inView, stat.count, stat.suffix]);

  return (
    <div className="stat-n" ref={ref}>
      {display}
    </div>
  );
}

export function StatsStrip() {
  return (
    <div className="stats-strip">
      <div className="stats-inner">
        {stats.map((s) => (
          <div className="stat-item" key={s.label}>
            <StatNumber stat={s} />
            <div className="stat-l">{s.label}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
