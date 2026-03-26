import type { ReactNode } from "react";

interface PanelProps {
  title: string;
  kicker?: string;
  children: ReactNode;
}

export function Panel({ title, kicker, children }: PanelProps) {
  return (
    <section className="rounded-[28px] bg-white p-5 shadow-lg ring-1 ring-slate-200">
      <header className="mb-4">
        {kicker ? <p className="text-xs uppercase tracking-[0.24em] text-slate-400">{kicker}</p> : null}
        <h2 className="mt-2 font-display text-2xl font-bold text-slate-900">{title}</h2>
      </header>
      {children}
    </section>
  );
}

