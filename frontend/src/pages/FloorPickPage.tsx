import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { getApiErrorMessage } from "@/api/errors";
import { HandheldShell } from "@/components/ui/HandheldShell";
import { SelectField } from "@/components/ui/SelectField";
import { usePickTaskDetail, usePickTasks } from "@/hooks/useOperationsData";
import { useConfirmPickTask, useStartPickTask } from "@/hooks/useWorkflowMutations";

export function FloorPickPage() {
  const { t } = useTranslation();
  const [quantity, setQuantity] = useState("1");
  const [selectedTaskId, setSelectedTaskId] = useState("");
  const pickTasks = usePickTasks();
  const taskDetail = usePickTaskDetail(selectedTaskId);
  const task = taskDetail.data ?? pickTasks.data?.find((entry) => entry.backendId === selectedTaskId);
  const startTask = useStartPickTask();
  const confirmTask = useConfirmPickTask();
  const quantityNumber = Number(quantity);
  const validationMessage =
    !selectedTaskId
      ? t("validation_select_pick_task")
      : !Number.isFinite(quantityNumber) || quantityNumber <= 0
        ? t("validation_positive_quantity")
        : null;

  useEffect(() => {
    if (!selectedTaskId && pickTasks.data?.length) {
      setSelectedTaskId(pickTasks.data[0].backendId);
    }
  }, [pickTasks.data, selectedTaskId]);

  useEffect(() => {
    if (task?.quantityRemaining) {
      setQuantity(String(task.quantityRemaining));
    }
  }, [task?.backendId, task?.quantityRemaining]);

  const handleStart = async () => {
    if (!task?.backendId) {
      return;
    }
    await startTask.mutateAsync(task.backendId);
  };

  const handleConfirm = async () => {
    if (!task?.backendId || validationMessage) {
      return;
    }
    await confirmTask.mutateAsync({ pickTaskId: task.backendId, quantity: quantityNumber });
  };

  return (
    <HandheldShell
      title={t("floor_pick_title")}
      subtitle={t("picking_title")}
      footer={
        <button
          className="w-full rounded-2xl bg-emerald-500 px-4 py-4 text-lg font-semibold text-slate-950"
          onClick={() => void handleConfirm()}
          type="button"
        >
          {t("confirm")}
        </button>
      }
    >
      <div className="flex h-full flex-col justify-between gap-5">
        <div>
          <SelectField
            label={t("pick_task_label")}
            onChange={setSelectedTaskId}
            options={
              pickTasks.data?.map((entry) => ({
                value: entry.backendId,
                label: `${entry.id} - ${entry.location} - ${entry.sku}`,
              })) ?? []
            }
            value={selectedTaskId}
          />
          <p className="text-sm text-slate-400">{t("current_task_label")}</p>
          <p className="mt-2 font-mono text-4xl font-bold">{task?.location ?? "A-01-B-03"}</p>
          <div className="mt-6 rounded-[28px] border border-slate-800 bg-slate-900 px-4 py-5">
            <p className="text-xs uppercase tracking-[0.25em] text-sky-300">{t("sku_label")}</p>
            <p className="mt-2 text-2xl font-bold">{task?.sku ?? "SKU-BLK-01"}</p>
            <p className="mt-2 text-lg text-slate-300">{t("quantity_to_pick", { count: task?.quantity ?? 4 })}</p>
            {task ? (
              <div className="mt-3 rounded-2xl bg-slate-950 px-4 py-3 text-sm text-slate-300 ring-1 ring-slate-800">
                <p>{t("order_label")}: {task.order || "-"}</p>
                <p>{t("status_label")}: {task.status || "-"}</p>
                <p>{t("remaining_label")}: {task.quantityRemaining}</p>
              </div>
            ) : null}
            <input
              className="mt-4 w-full rounded-2xl border border-slate-700 bg-slate-950 px-4 py-3 text-white"
              onChange={(event) => setQuantity(event.target.value)}
              placeholder={t("quantity_placeholder")}
              value={quantity}
            />
          </div>
        </div>
        <div className="grid gap-3">
          <button
            className="rounded-3xl border-2 border-dashed border-sky-500 px-4 py-6 text-center text-lg font-semibold"
            onClick={() => void handleStart()}
            type="button"
          >
            {t("start_task")}
          </button>
          {validationMessage ? <p className="text-center text-sm text-amber-300">{validationMessage}</p> : null}
          {startTask.isError ? (
            <p className="text-center text-sm text-rose-300">{getApiErrorMessage(startTask.error, t("action_failed"))}</p>
          ) : null}
          {confirmTask.isError ? (
            <p className="text-center text-sm text-rose-300">
              {getApiErrorMessage(confirmTask.error, t("action_failed"))}
            </p>
          ) : null}
          {confirmTask.isSuccess ? <p className="text-center text-sm text-emerald-400">{t("action_success")}</p> : null}
        </div>
      </div>
    </HandheldShell>
  );
}
