import type { ReactNode } from "react";

interface MetricCardProps {
  label: string;
  value: number | string;
  accent?: string;
  detail?: string;
  icon?: ReactNode;
}

export function MetricCard({ label, value, accent = "bg-sky-500", detail, icon }: MetricCardProps) {
  return (
    <article className="rounded-[28px] bg-white p-5 shadow-lg ring-1 ring-slate-200">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-xs uppercase tracking-[0.28em] text-slate-400">{label}</p>
          <p className="mt-3 text-4xl font-bold text-slate-900">{value}</p>
          {detail ? <p className="mt-2 text-sm text-slate-500">{detail}</p> : null}
        </div>
        <div className={`rounded-2xl ${accent} p-3 text-white shadow-md`}>{icon ?? <span>+</span>}</div>
      </div>
    </article>
  );
}

