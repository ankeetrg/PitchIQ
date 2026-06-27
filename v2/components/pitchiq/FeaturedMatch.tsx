"use client";

import Image from "next/image";
import { motion } from "framer-motion";
import { ExternalLink } from "lucide-react";
import { americanOdds } from "@/lib/pitchiq-hooks";
import type { Match, Team } from "@/lib/pitchiq-types";
import { useToast } from "./Toast";

interface FeaturedMatchProps {
  match: Match;
  oddsFlashKey: number;
  scoreFlashKey: number;
}

function Flag({ team }: { team: Team }) {
  return (
    <Image
      src={`https://flagcdn.com/w40/${team.flagCode}.png`}
      alt={`${team.name} flag`}
      width={54}
      height={40}
      sizes="54px"
      className="h-[40px] w-[54px] rounded-sm object-cover shadow-sm"
    />
  );
}

function FormDots({ form }: { form: Team["form"] }) {
  return (
    <div className="mt-3 flex justify-center gap-1.5">
      {form.map((item, index) => (
        <span
          key={`${item}-${index}`}
          className={`flex h-5 w-5 items-center justify-center rounded-sm text-[10px] font-black text-white ${
            item === "W" ? "bg-green" : item === "D" ? "bg-gold" : "bg-red"
          }`}
        >
          {item}
        </span>
      ))}
    </div>
  );
}

function TeamBlock({ team, align }: { team: Team; align: "left" | "right" }) {
  return (
    <div className={`flex flex-col items-center ${align === "left" ? "md:items-end" : "md:items-start"}`}>
      <Flag team={team} />
      <h3 className="mt-3 font-cond text-[22px] font-black uppercase leading-none text-white">{team.name}</h3>
      <p className="mt-1 text-xs font-bold uppercase tracking-[0.12em] text-white/55">{team.record}</p>
      <FormDots form={team.form} />
    </div>
  );
}

export function FeaturedMatch({ match, oddsFlashKey, scoreFlashKey }: FeaturedMatchProps) {
  const { showToast } = useToast();
  const odds = [
    { label: match.home.shortName, value: americanOdds(match.odds.home), book: match.odds.book, move: "up" },
    { label: "Draw", value: americanOdds(match.odds.draw), book: "Best price", move: "flat" },
    { label: match.away.shortName, value: americanOdds(match.odds.away), book: "Consensus", move: "down" },
    { label: "Total", value: `O/U ${match.odds.total}`, book: match.odds.spread, move: "flat" },
  ];
  const probability = [
    { label: match.home.shortName, value: match.probabilities.home, className: "bg-green" },
    { label: "Draw", value: match.probabilities.draw, className: "bg-gold" },
    { label: match.away.shortName, value: match.probabilities.away, className: "bg-red" },
  ];

  return (
    <article className="overflow-hidden rounded-lg border border-[rgba(255,255,255,0.08)] bg-navy text-white shadow-[var(--shadow)]">
      <div className="bg-[linear-gradient(135deg,#091424_0%,#0D2248_50%,#102E60_100%)] p-5 sm:p-6">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div className="flex items-center gap-2">
            <span className="rounded-sm border border-white/14 bg-white/8 px-3 py-1 text-xs font-black uppercase tracking-[0.12em] text-white/75">
              {match.group}
            </span>
            <span className="flex items-center gap-2 rounded-sm bg-red px-3 py-1 text-xs font-black uppercase tracking-[0.12em]">
              <span className="live-dot h-2 w-2 rounded-full bg-white" />
              {match.status === "fulltime" ? "Final" : "Live"}
            </span>
          </div>
          <div className="text-right text-xs font-bold uppercase tracking-[0.12em] text-white/60">
            <div>{match.clock}</div>
            <div>{match.venue}</div>
          </div>
        </div>

        <div className="mt-8 grid items-center gap-6 md:grid-cols-[1fr_140px_1fr]">
          <TeamBlock team={match.home} align="left" />
          <div className="flex flex-col items-center">
            <div key={scoreFlashKey} className="score-flash font-cond text-[60px] font-black leading-none tracking-normal">
              {match.score.home}-{match.score.away}
            </div>
            <div className="mt-2 rounded-sm bg-white/10 px-3 py-1 text-xs font-black uppercase tracking-[0.14em] text-white/65">
              {match.competition}
            </div>
          </div>
          <TeamBlock team={match.away} align="right" />
        </div>

        <div key={oddsFlashKey} className="odds-flash mt-8 grid gap-2 rounded-lg border border-white/10 bg-white/[0.04] p-2 sm:grid-cols-4">
          {odds.map((item) => (
            <div key={item.label} className="rounded-md bg-white/[0.04] p-3">
              <div className="flex items-center justify-between gap-2 text-[11px] font-black uppercase tracking-[0.14em] text-white/50">
                <span>{item.label}</span>
                <span>{item.move === "up" ? "↗" : item.move === "down" ? "↘" : "→"}</span>
              </div>
              <div className="mt-2 font-cond text-3xl font-black leading-none">{item.value}</div>
              <div className="mt-1 text-xs font-semibold text-white/45">{item.book}</div>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-[var(--surf)] p-5 text-[var(--t1)] sm:p-6">
        <div className="rounded-lg border border-[var(--b1)] bg-[var(--bg)] p-4">
          <div className="mb-3 flex items-center justify-between gap-3">
            <h4 className="text-sm font-black uppercase tracking-[0.14em] text-[var(--t3)]">Win Probability</h4>
            <span className="text-sm font-bold text-green">{match.probabilities.home}% France</span>
          </div>
          <div className="flex h-3 overflow-hidden rounded-full bg-[var(--b1)]">
            {probability.map((item) => (
              <motion.div
                key={item.label}
                initial={{ width: 0 }}
                animate={{ width: `${item.value}%` }}
                transition={{ duration: 0.55, ease: [0.25, 0, 0.1, 1] }}
                className={item.className}
              />
            ))}
          </div>
          <div className="mt-2 grid grid-cols-3 gap-2 text-xs font-bold text-[var(--t3)]">
            {probability.map((item) => (
              <span key={item.label}>
                {item.label} {item.value}%
              </span>
            ))}
          </div>
        </div>

        <div className="mt-4 grid gap-3 sm:grid-cols-4">
          {match.keyStats.map((stat) => (
            <div key={stat.label} className="rounded-md border border-[var(--b1)] bg-[var(--surf)] p-3">
              <div className="text-[11px] font-black uppercase tracking-[0.14em] text-[var(--t4)]">{stat.label}</div>
              <div className="mt-1 font-cond text-2xl font-black leading-none">{stat.value}</div>
              <div className="mt-1 text-xs text-[var(--t3)]">{stat.detail}</div>
            </div>
          ))}
        </div>

        <div className="mt-5 flex flex-col gap-3 sm:flex-row sm:items-center">
          <button
            type="button"
            onClick={() => showToast("France moneyline added to your watchlist", "success")}
            className="inline-flex min-h-11 items-center justify-center rounded-md bg-gold px-5 text-sm font-black text-white transition hover:bg-gold-hover"
          >
            Bet France {americanOdds(match.odds.home)}
          </button>
          <a
            href="#predictions"
            className="inline-flex min-h-11 items-center justify-center gap-2 rounded-md border border-[var(--b1)] px-5 text-sm font-black text-[var(--t1)] transition hover:border-gold-border hover:text-gold"
          >
            Full Preview <ExternalLink size={16} />
          </a>
          <p className="text-xs font-semibold text-[var(--t3)]">LEGAL-REVIEW-REQUIRED: verify legal availability and line movement before wagering.</p>
        </div>
      </div>
    </article>
  );
}
