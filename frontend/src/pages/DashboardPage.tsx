import { useTranslation } from "react-i18next";

import { MetricCard } from "@/components/ui/MetricCard";
import { Panel } from "@/components/ui/Panel";
import { TaskList } from "@/components/ui/TaskList";
import { useDashboardSummary } from "@/hooks/useDashboardSummary";
import { useCountTasks, usePickTasks, useReceivingQueue } from "@/hooks/useOperationsData";

export function DashboardPage() {
  const { t } = useTranslation();
  const summary = useDashboardSummary();
  const receiving = useReceivingQueue();
  const picking = usePickTasks();
  const counting = useCountTasks();

  const data = summary.data;

  return (
    <main className="grid gap-6">
      <section className="rounded-[32px] bg-[linear-gradient(135deg,#0f172a_0%,#1d4ed8_55%,#38bdf8_100%)] p-8 text-white shadow-2xl">
        <p className="text-xs uppercase tracking-[0.35em] text-sky-200">{t("dashboard")}</p>
        <h1 className="mt-3 font-display text-5xl font-bold">{t("dashboard_heading")}</h1>
        <p className="mt-3 max-w-3xl text-base text-sky-50/85">{t("dashboard_description")}</p>
      </section>
      <section className="grid gap-4 xl:grid-cols-5">
        <MetricCard label={t("orders_received")} value={data?.ordersReceived ?? 0} detail={t("today_metric")} />
        <MetricCard label={t("orders_shipped")} value={data?.ordersShipped ?? 0} accent="bg-emerald-500" />
        <MetricCard label={t("returns_received")} value={data?.returnsReceived ?? 0} accent="bg-amber-500" />
        <MetricCard label={t("picks_completed")} value={data?.picksCompleted ?? 0} accent="bg-sky-600" />
        <MetricCard label={t("counts_completed")} value={data?.countTasksCompleted ?? 0} accent="bg-slate-700" />
      </section>
      <section className="grid gap-6 xl:grid-cols-3">
        <Panel title={t("receiving_title")} kicker={t("inbound_label")}>
          <TaskList
            items={receiving.data ?? []}
            columns={[
              { key: "id", label: t("reference_label") },
              { key: "supplier", label: t("supplier_label") },
              { key: "status", label: t("status_label") },
            ]}
          />
        </Panel>
        <Panel title={t("picking_title")} kicker={t("floor_label")}>
          <TaskList
            items={picking.data ?? []}
            columns={[
              { key: "order", label: t("order_label") },
              { key: "location", label: t("location_label") },
              { key: "quantity", label: t("quantity_label") },
            ]}
          />
        </Panel>
        <Panel title={t("counting_title")} kicker={t("control_label")}>
          <TaskList
            items={counting.data ?? []}
            columns={[
              { key: "id", label: t("reference_label") },
              { key: "location", label: t("location_label") },
              { key: "status", label: t("status_label") },
            ]}
          />
        </Panel>
      </section>
    </main>
  );
}

