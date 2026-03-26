import { useTranslation } from "react-i18next";

import { Panel } from "@/components/ui/Panel";
import { TaskList } from "@/components/ui/TaskList";
import { useReceivingQueue } from "@/hooks/useOperationsData";

export function ReceivingPage() {
  const { t } = useTranslation();
  const receiving = useReceivingQueue();

  return (
    <main className="grid gap-6">
      <Panel title={t("receiving_title")} kicker={t("inbound_label")}>
        <TaskList
          items={receiving.data ?? []}
          columns={[
            { key: "id", label: t("reference_label") },
            { key: "supplier", label: t("supplier_label") },
            { key: "status", label: t("status_label") },
            { key: "lines", label: t("lines_label") },
          ]}
        />
      </Panel>
    </main>
  );
}

