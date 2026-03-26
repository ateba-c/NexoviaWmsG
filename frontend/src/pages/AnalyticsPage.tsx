import { useTranslation } from "react-i18next";

import { MetricCard } from "@/components/ui/MetricCard";
import { Panel } from "@/components/ui/Panel";
import { useDashboardSummary } from "@/hooks/useDashboardSummary";

export function AnalyticsPage() {
  const { t } = useTranslation();
  const summary = useDashboardSummary();
  const data = summary.data;

  return (
    <main className="grid gap-6">
      <Panel title={t("analytics_title")} kicker={t("analytics_label")}>
        <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          <MetricCard label={t("orders_received")} value={data?.ordersReceived ?? 0} />
          <MetricCard label={t("orders_shipped")} value={data?.ordersShipped ?? 0} accent="bg-emerald-500" />
          <MetricCard label={t("returns_received")} value={data?.returnsReceived ?? 0} accent="bg-amber-500" />
          <MetricCard label={t("picks_completed")} value={data?.picksCompleted ?? 0} accent="bg-sky-600" />
          <MetricCard label={t("counts_completed")} value={data?.countTasksCompleted ?? 0} accent="bg-slate-700" />
        </div>
      </Panel>
    </main>
  );
}

