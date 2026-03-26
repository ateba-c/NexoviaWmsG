import { useTranslation } from "react-i18next";

import { Panel } from "@/components/ui/Panel";
import { TaskList } from "@/components/ui/TaskList";
import { usePickTasks } from "@/hooks/useOperationsData";

export function PickingPage() {
  const { t } = useTranslation();
  const tasks = usePickTasks();

  return (
    <main className="grid gap-6">
      <Panel title={t("picking_title")} kicker={t("floor_label")}>
        <TaskList
          items={tasks.data ?? []}
          columns={[
            { key: "id", label: t("reference_label") },
            { key: "order", label: t("order_label") },
            { key: "location", label: t("location_label") },
            { key: "sku", label: t("sku_label") },
            { key: "quantity", label: t("quantity_label") },
          ]}
        />
      </Panel>
    </main>
  );
}

