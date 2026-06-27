"use client";

import { Mail } from "lucide-react";
import { useState } from "react";
import { Reveal } from "./Reveal";
import { useToast } from "./Toast";

function isValidEmail(value: string) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

export function NewsletterStrip() {
  const { showToast } = useToast();
  const [email, setEmail] = useState("");
  const [state, setState] = useState<"idle" | "error" | "success">("idle");

  return (
    <section id="newsletter" className="bg-navy py-10 text-white">
      <div className="max-shell">
        <Reveal>
          <div className="grid gap-5 rounded-lg border border-white/10 bg-white/[0.04] p-6 lg:grid-cols-[1fr_460px] lg:items-center">
            <div className="flex gap-4">
              <span className="flex h-12 w-12 shrink-0 items-center justify-center rounded-md bg-gold text-white">
                <Mail size={22} />
              </span>
              <div>
                <p className="text-xs font-black uppercase tracking-[0.16em] text-white/55">Inbox edge</p>
                <h2 className="font-cond text-4xl font-black uppercase leading-none">Get the Edge Before Kickoff</h2>
                <p className="mt-2 max-w-2xl text-sm leading-6 text-white/68">
                  Receive lineup alerts, fantasy pivots, and AI-labeled match notes before the slate locks.
                </p>
              </div>
            </div>

            <form
              className="grid gap-3 sm:grid-cols-[1fr_150px]"
              onSubmit={(event) => {
                event.preventDefault();
                if (!isValidEmail(email)) {
                  setState("error");
                  showToast("Enter a valid email address", "warning");
                  return;
                }

                setState("success");
                showToast("Newsletter signup confirmed", "success");
                window.setTimeout(() => {
                  setState("idle");
                  setEmail("");
                }, 3500);
              }}
            >
              <input
                type="email"
                value={email}
                onChange={(event) => {
                  setEmail(event.target.value);
                  setState("idle");
                }}
                placeholder="you@example.com"
                aria-label="Email address"
                className={`min-h-12 rounded-md border bg-white px-4 text-sm font-semibold text-navy outline-none transition ${
                  state === "error" ? "border-red" : state === "success" ? "border-green" : "border-transparent"
                }`}
              />
              <button
                type="submit"
                className={`min-h-12 rounded-md px-5 text-sm font-black text-white transition ${
                  state === "success" ? "bg-green" : "bg-gold hover:bg-gold-hover"
                }`}
              >
                {state === "success" ? "Subscribed" : "Subscribe"}
              </button>
              <p className="text-xs text-white/45 sm:col-span-2">No spam. Alerts and analysis only. Unsubscribe anytime.</p>
            </form>
          </div>
        </Reveal>
      </div>
    </section>
  );
}
