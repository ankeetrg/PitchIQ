import Image from "next/image";
import { STANDINGS } from "@/lib/pitchiq-data";

function Flag({ flagCode, team }: { flagCode: string; team: string }) {
  return (
    <Image
      src={`https://flagcdn.com/w40/${flagCode}.png`}
      alt={`${team} flag`}
      width={24}
      height={18}
      sizes="24px"
      className="h-[18px] w-6 rounded-sm object-cover"
    />
  );
}

export function GroupStandings() {
  return (
    <div className="rounded-lg border border-[var(--b1)] bg-[var(--surf)] p-5 shadow-[var(--shadow-soft)]">
      <div className="flex items-center justify-between gap-3">
        <div>
          <p className="text-xs font-black uppercase tracking-[0.14em] text-gold">Live table</p>
          <h2 className="mt-1 font-cond text-3xl font-black uppercase leading-none">Group Standings</h2>
        </div>
        <span className="rounded-sm bg-green-dim px-2 py-1 text-xs font-black uppercase text-green">Auto</span>
      </div>

      <div className="mt-5 grid gap-5 xl:grid-cols-2">
        {Object.entries(STANDINGS).map(([group, rows]) => (
          <div key={group} className="overflow-hidden rounded-md border border-[var(--b1)]">
            <div className="bg-[var(--bg2)] px-3 py-2 text-xs font-black uppercase tracking-[0.14em] text-[var(--t3)]">{group}</div>
            <table className="w-full text-sm">
              <thead className="text-[11px] uppercase tracking-[0.12em] text-[var(--t4)]">
                <tr>
                  <th className="px-3 py-2 text-left">Team</th>
                  <th className="px-2 py-2 text-right">P</th>
                  <th className="px-2 py-2 text-right">GD</th>
                  <th className="px-3 py-2 text-right">Pts</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((row) => (
                  <tr key={row.team} className="border-t border-[var(--b1)]">
                    <td className="px-3 py-2">
                      <div className="flex items-center gap-2 font-bold">
                        <Flag flagCode={row.flagCode} team={row.team} />
                        {row.team}
                      </div>
                    </td>
                    <td className="px-2 py-2 text-right text-[var(--t2)]">{row.played}</td>
                    <td className="px-2 py-2 text-right text-[var(--t2)]">{row.goalDiff > 0 ? `+${row.goalDiff}` : row.goalDiff}</td>
                    <td className="px-3 py-2 text-right font-black">{row.points}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ))}
      </div>
    </div>
  );
}
