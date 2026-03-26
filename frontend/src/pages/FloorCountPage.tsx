import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { getApiErrorMessage } from "@/api/errors";
import { HandheldShell } from "@/components/ui/HandheldShell";
import { SelectField } from "@/components/ui/SelectField";
import { useCountTaskDetail, useCountTasks, useItems } from "@/hooks/useOperationsData";
import { useExecuteCount } from "@/hooks/useWorkflowMutations";

export function FloorCountPage() {
  const { t } = useTranslation();
  const [quantity, setQuantity] = useState("0");
  const [selectedTaskId, setSelectedTaskId] = useState("");
  const [selectedItemId, setSelectedItemId] = useState("");
  const countTasks = useCountTasks();
  const items = useItems();
  const taskDetail = useCountTaskDetail(selectedTaskId);
  const executeCount = useExecuteCount();
  const task = taskDetail.data ?? countTasks.data?.find((entry) => entry.backendId === selectedTaskId);
  const item = items.data?.find((entry) => entry.id === selectedItemId);
  const quantityNumber = Number(quantity);
  const validationMessage =
    !selectedTaskId
      ? t("validation_select_count_task")
      : !selectedItemId
        ? t("validation_select_item")
        : !Number.isFinite(quantityNumber) || quantityNumber < 0
          ? t("validation_non_negative_quantity")
          : null;

  useEffect(() => {
    if (!selectedTaskId && countTasks.data?.length) {
      setSelectedTaskId(countTasks.data[0].backendId);
    }
  }, [countTasks.data, selectedTaskId]);

  useEffect(() => {
    if (!selectedItemId && task?.itemId) {
      setSelectedItemId(task.itemId);
    }
  }, [selectedItemId, task?.itemId]);

  const handleSubmit = async () => {
    if (!task?.backendId || validationMessage) {
      return;
    }
    await executeCount.mutateAsync({
      countTaskId: task.backendId,
      itemId: selectedItemId,
      countedQuantity: quantityNumber,
    });
  };

  return (
    <HandheldShell
      title={t("floor_count_title")}
      subtitle={t("counting_title")}
      footer={
        <button
          className="w-full rounded-2xl bg-amber-400 px-4 py-4 text-lg font-semibold text-slate-950"
          onClick={() => void handleSubmit()}
          type="button"
        >
          {t("submit_count")}
        </button>
      }
    >
      <div className="flex h-full flex-col justify-between gap-5">
        <div>
          <SelectField
            label={t("count_task_label")}
            onChange={setSelectedTaskId}
            options={
              countTasks.data?.map((entry) => ({
                value: entry.backendId,
                label: `${entry.id} - ${entry.location} - ${entry.type}`,
              })) ?? []
            }
            value={selectedTaskId}
          />
          <p className="text-sm text-slate-400">{t("location_label")}</p>
          <p className="mt-2 font-mono text-4xl font-bold">{task?.location ?? "C-01-01-01"}</p>
          <div className="mt-6 rounded-[28px] border border-slate-800 bg-slate-900 px-4 py-5">
            <SelectField
              label={t("sku_label")}
              onChange={setSelectedItemId}
              options={
                items.data?.map((entry) => ({
                  value: entry.id,
                  label: `${entry.sku} - ${entry.description}`,
                })) ?? []
              }
              value={selectedItemId}
            />
            <p className="text-xs uppercase tracking-[0.25em] text-sky-300">{t("sku_label")}</p>
            <p className="mt-2 text-2xl font-bold">{item?.sku ?? "SKU-CNT-01"}</p>
            {task ? (
              <div className="mt-3 rounded-2xl bg-slate-950 px-4 py-3 text-sm text-slate-300 ring-1 ring-slate-800">
                <p>{t("type_label")}: {task.type || "-"}</p>
                <p>{t("status_label")}: {task.status || "-"}</p>
                <p>{t("results_label")}: {task.resultCount}</p>
              </div>
            ) : null}
          </div>
        </div>
        <div className="rounded-3xl border-2 border-dashed border-amber-400 px-4 py-8 text-center">
          <p className="text-lg font-semibold">{t("enter_count_prompt")}</p>
          <input
            className="mt-4 w-full rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-center text-5xl font-bold text-white"
            onChange={(event) => setQuantity(event.target.value)}
            placeholder="0"
            value={quantity}
          />
          {validationMessage ? <p className="mt-3 text-sm text-amber-300">{validationMessage}</p> : null}
          {executeCount.isError ? (
            <p className="mt-3 text-sm text-rose-300">{getApiErrorMessage(executeCount.error, t("action_failed"))}</p>
          ) : null}
          {executeCount.isSuccess ? <p className="mt-3 text-sm text-emerald-400">{t("action_success")}</p> : null}
        </div>
      </div>
    </HandheldShell>
  );
}
