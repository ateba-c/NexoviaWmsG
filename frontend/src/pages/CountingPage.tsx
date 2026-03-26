import { useTranslation } from "react-i18next";

import { Panel } from "@/components/ui/Panel";
import { TaskList } from "@/components/ui/TaskList";
import { useCountTasks } from "@/hooks/useOperationsData";

export function CountingPage() {
  const { t } = useTranslation();
  const tasks = useCountTasks();

  return (
    <main className="grid gap-6">
      <Panel title={t("counting_title")} kicker={t("control_label")}>
        <TaskList
          items={tasks.data ?? []}
          columns={[
            { key: "id", label: t("reference_label") },
            { key: "location", label: t("location_label") },
            { key: "type", label: t("type_label") },
            { key: "status", label: t("status_label") },
          ]}
        />
      </Panel>
    </main>
  );
}

