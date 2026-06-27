import { CalendarDays } from "lucide-react";
import { SCHEDULE } from "@/lib/pitchiq-data";

export function TodaySchedule() {
  return (
    <div className="rounded-lg border border-[var(--b1)] bg-[var(--surf)] p-5 shadow-[var(--shadow-soft)]">
      <div className="flex items-center justify-between gap-3">
        <div>
          <p className="text-xs font-black uppercase tracking-[0.14em] text-green">Upcoming</p>
          <h2 className="mt-1 font-cond text-3xl font-black uppercase leading-none">Today&apos;s Schedule</h2>
        </div>
        <CalendarDays className="text-[var(--t3)]" size={20} />
      </div>

      <div className="mt-5 space-y-3">
        {SCHEDULE.map((match) => (
          <div key={match.id} className="rounded-md border border-[var(--b1)] bg-[var(--bg)] p-4">
            <div className="flex items-center justify-between gap-3 text-xs font-bold text-[var(--t3)]">
              <span>{match.time}</span>
              <span>{match.group}</span>
            </div>
            <div className="mt-2 font-cond text-2xl font-black uppercase leading-none">
              {match.home} <span className="text-gold">vs</span> {match.away}
            </div>
            <div className="mt-2 flex flex-wrap items-center justify-between gap-2 text-xs">
              <span className="text-[var(--t3)]">{match.venue}</span>
              <span className="rounded-sm bg-gold-dim px-2 py-1 font-black text-gold">{match.tag}</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
