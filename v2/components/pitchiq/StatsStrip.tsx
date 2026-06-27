"use client";

import { useInView } from "framer-motion";
import { useEffect, useRef, useState } from "react";
import { STATS } from "@/lib/pitchiq-data";
import { Reveal } from "./Reveal";

function cubicBezier(t: number) {
  const cx = 3 * 0.25;
  const bx = 3 * (0.1 - 0.25) - cx;
  const ax = 1 - cx - bx;
  const cy = 0;
  const by = 3 * (1 - 0) - cy;
  const ay = 1 - cy - by;

  function sampleCurveX(x: number) {
    return ((ax * x + bx) * x + cx) * x;
  }

  function sampleCurveY(y: number) {
    return ((ay * y + by) * y + cy) * y;
  }

  function sampleCurveDerivativeX(x: number) {
    return (3 * ax * x + 2 * bx) * x + cx;
  }

  let x = t;
  for (let i = 0; i < 5; i += 1) {
    const derivative = sampleCurveDerivativeX(x);
    if (Math.abs(derivative) < 0.00001) {
      break;
    }
    x -= (sampleCurveX(x) - t) / derivative;
  }

  return sampleCurveY(Math.min(1, Math.max(0, x)));
}

function CountUp({ value, suffix, prefix = "" }: { value: number; suffix: string; prefix?: string }) {
  const ref = useRef<HTMLSpanElement | null>(null);
  const inView = useInView(ref, { once: true, amount: 0.08 });
  const [display, setDisplay] = useState(0);

  useEffect(() => {
    if (!inView) {
      return undefined;
    }

    let frame = 0;
    const start = performance.now();
    const duration = 1400;

    const animate = (time: number) => {
      const progress = Math.min(1, (time - start) / duration);
      setDisplay(Math.round(value * cubicBezier(progress)));
      if (progress < 1) {
        frame = requestAnimationFrame(animate);
      }
    };

    frame = requestAnimationFrame(animate);
    return () => cancelAnimationFrame(frame);
  }, [inView, value]);

  return (
    <span ref={ref}>
      {prefix}
      {display}
      {suffix}
    </span>
  );
}

export function StatsStrip() {
  return (
    <section className="bg-[var(--bg2)] py-8">
      <div className="max-shell">
        <div className="grid gap-3 md:grid-cols-4">
          {STATS.map((stat, index) => (
            <Reveal key={stat.id} delay={index * 0.04}>
              <div className="rounded-lg border border-[var(--b1)] bg-[var(--surf)] p-5 shadow-[var(--shadow-soft)]">
                <div className="font-cond text-5xl font-black leading-none text-gold">
                  <CountUp value={stat.value} prefix={stat.prefix} suffix={stat.suffix} />
                </div>
                <div className="mt-2 text-sm font-black uppercase tracking-[0.12em] text-[var(--t1)]">{stat.label}</div>
                <div className="mt-1 text-sm text-[var(--t3)]">{stat.detail}</div>
              </div>
            </Reveal>
          ))}
        </div>
      </div>
    </section>
  );
}
