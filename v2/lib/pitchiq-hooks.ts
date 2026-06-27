"use client";

import { useEffect, useRef } from "react";

export function useInterval(callback: () => void, delay: number | null) {
  const savedCallback = useRef(callback);

  useEffect(() => {
    savedCallback.current = callback;
  }, [callback]);

  useEffect(() => {
    if (delay === null) {
      return undefined;
    }

    const id = window.setInterval(() => savedCallback.current(), delay);
    return () => window.clearInterval(id);
  }, [delay]);
}

export function americanOdds(value: number) {
  return value > 0 ? `+${value}` : `${value}`;
}

export function driftAmericanOdds(value: number) {
  const step = 5 + Math.floor(Math.random() * 6);
  const direction = Math.random() > 0.5 ? 1 : -1;
  const next = value + step * direction;

  if (next > -100 && next < 100) {
    return next >= 0 ? 105 : -105;
  }

  return next;
}
