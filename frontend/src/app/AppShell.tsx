import { Link, NavLink, Outlet } from "react-router-dom";
import { useTranslation } from "react-i18next";

import { LanguageToggle } from "@/components/ui/LanguageToggle";

export function AppShell() {
  const { t } = useTranslation();

  return (
    <div className="min-h-screen bg-[linear-gradient(180deg,#e2e8f0_0%,#f8fafc_40%,#f8fafc_100%)] text-slate-900">
      <header className="border-b border-slate-200 bg-white/80 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-6 px-6 py-4">
          <div>
            <Link to="/" className="font-display text-2xl font-bold text-slate-950">
              {t("app_name")}
            </Link>
            <p className="text-sm text-slate-500">{t("app_tagline")}</p>
          </div>
          <div className="flex items-center gap-3">
            <LanguageToggle />
          </div>
        </div>
      </header>
      <div className="mx-auto grid max-w-7xl gap-6 px-6 py-6 lg:grid-cols-[240px_1fr]">
        <aside className="rounded-[28px] bg-slate-950 p-4 text-white shadow-xl">
          <nav className="grid gap-2">
            {[
              ["/", t("dashboard")],
              ["/receiving", t("receiving_title")],
              ["/picking", t("picking_title")],
              ["/counting", t("counting_title")],
              ["/analytics", t("analytics_title")],
              ["/floor/receive", t("floor_receive_title")],
              ["/floor/pick", t("floor_pick_title")],
              ["/floor/count", t("floor_count_title")],
            ].map(([to, label]) => (
              <NavLink
                key={to}
                to={to}
                className={({ isActive }) =>
                  `rounded-2xl px-4 py-3 text-sm font-semibold transition ${
                    isActive ? "bg-white text-slate-950" : "text-slate-300 hover:bg-slate-900"
                  }`
                }
              >
                {label}
              </NavLink>
            ))}
          </nav>
        </aside>
        <Outlet />
      </div>
    </div>
  );
}

