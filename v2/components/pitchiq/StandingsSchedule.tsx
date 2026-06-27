import { GroupStandings } from "./GroupStandings";
import { Reveal } from "./Reveal";
import { TodaySchedule } from "./TodaySchedule";

export function StandingsSchedule() {
  return (
    <section id="standings" className="bg-[var(--bg)] py-10">
      <div className="max-shell grid gap-5 lg:grid-cols-[minmax(0,1.15fr)_minmax(340px,0.85fr)]">
        <Reveal>
          <GroupStandings />
        </Reveal>
        <Reveal delay={0.08}>
          <TodaySchedule />
        </Reveal>
      </div>
    </section>
  );
}
