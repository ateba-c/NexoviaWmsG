import type { ReactNode } from "react";

interface HandheldShellProps {
  title: string;
  subtitle: string;
  footer: ReactNode;
  children: ReactNode;
}

export function HandheldShell({ title, subtitle, footer, children }: HandheldShellProps) {
  return (
    <main className="min-h-screen bg-[radial-gradient(circle_at_top,#154a80_0%,#0f172a_35%,#020617_100%)] p-4 text-white">
      <div className="mx-auto flex min-h-[calc(100vh-2rem)] max-w-sm flex-col rounded-[30px] border border-slate-800 bg-slate-950/90 shadow-2xl shadow-sky-950/50">
        <header className="border-b border-slate-800 px-4 py-4">
          <p className="text-xs uppercase tracking-[0.3em] text-sky-300">{subtitle}</p>
          <h1 className="mt-2 text-3xl font-bold">{title}</h1>
        </header>
        <section className="flex flex-1 flex-col px-4 py-5">{children}</section>
        <footer className="border-t border-slate-800 p-4">{footer}</footer>
      </div>
    </main>
  );
}

