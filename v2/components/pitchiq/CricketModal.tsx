"use client";

import { AnimatePresence, motion } from "framer-motion";
import { X } from "lucide-react";
import { useEffect, useState } from "react";

interface CricketModalProps {
  open: boolean;
  onClose: () => void;
}

export function CricketModal({ open, onClose }: CricketModalProps) {
  const [email, setEmail] = useState("");
  const [joined, setJoined] = useState(false);

  useEffect(() => {
    if (!open) {
      return undefined;
    }

    const original = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.body.style.overflow = original;
    };
  }, [open]);

  return (
    <AnimatePresence>
      {open ? (
        <motion.div
          className="fixed inset-0 z-[450] flex items-end justify-center bg-black/45 modal-backdrop"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          role="dialog"
          aria-modal="true"
          aria-label="Cricket waitlist"
        >
          <button type="button" className="absolute inset-0 cursor-default" aria-label="Close modal" onClick={onClose} />
          <motion.div
            initial={{ y: "100%" }}
            animate={{ y: 0 }}
            exit={{ y: "100%" }}
            transition={{ duration: 0.32, ease: [0.25, 0, 0.1, 1] }}
            className="relative w-full max-w-2xl rounded-t-[12px] border border-[var(--b1)] bg-[var(--surf)] p-6 shadow-[var(--shadow)]"
          >
            <div className="flex items-start justify-between gap-4">
              <div>
                <p className="text-xs font-black uppercase tracking-[0.16em] text-gold">Coming soon</p>
                <h2 className="mt-2 font-cond text-4xl font-black uppercase leading-none">Cricket IQ</h2>
              </div>
              <button
                type="button"
                onClick={onClose}
                className="flex h-10 w-10 items-center justify-center rounded-md border border-[var(--b1)] text-[var(--t2)] transition hover:bg-[var(--bg2)]"
                aria-label="Close cricket modal"
              >
                <X size={18} />
              </button>
            </div>
            <p className="mt-4 max-w-xl text-sm leading-6 text-[var(--t2)]">
              Cricket coverage is on the roadmap after the World Cup soccer launch. Join the waitlist for match alerts, fantasy edges, and market context when it opens.
            </p>
            <form
              className="mt-5 flex flex-col gap-3 sm:flex-row"
              onSubmit={(event) => {
                event.preventDefault();
                setJoined(true);
                window.setTimeout(() => {
                  setJoined(false);
                  setEmail("");
                }, 3500);
              }}
            >
              <input
                type="email"
                required
                value={email}
                onChange={(event) => setEmail(event.target.value)}
                placeholder="you@example.com"
                className="min-h-12 flex-1 rounded-md border border-[var(--b1)] bg-[var(--bg)] px-4 text-sm font-semibold text-[var(--t1)] outline-none transition focus:border-gold"
              />
              <button type="submit" className="min-h-12 rounded-md bg-gold px-6 text-sm font-black text-white transition hover:bg-gold-hover">
                {joined ? "Joined" : "Notify Me"}
              </button>
            </form>
          </motion.div>
        </motion.div>
      ) : null}
    </AnimatePresence>
  );
}
