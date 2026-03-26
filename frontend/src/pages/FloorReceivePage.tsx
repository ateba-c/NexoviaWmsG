import { useEffect, useState } from "react";
import { useTranslation } from "react-i18next";

import { getApiErrorMessage } from "@/api/errors";
import { HandheldShell } from "@/components/ui/HandheldShell";
import { SelectField } from "@/components/ui/SelectField";
import { useInboundLineDetail, useInboundLines, useLocations } from "@/hooks/useOperationsData";
import { useReceiveLine } from "@/hooks/useWorkflowMutations";

export function FloorReceivePage() {
  const { t } = useTranslation();
  const [quantity, setQuantity] = useState("1");
  const [selectedLineId, setSelectedLineId] = useState("");
  const [locationId, setLocationId] = useState("");
  const inboundLines = useInboundLines();
  const locations = useLocations();
  const lineDetail = useInboundLineDetail(selectedLineId);
  const receiveLine = useReceiveLine();
  const line = lineDetail.data ?? inboundLines.data?.find((entry) => entry.backendId === selectedLineId);
  const quantityNumber = Number(quantity);
  const validationMessage =
    !selectedLineId
      ? t("validation_select_line")
      : !locationId
        ? t("validation_select_location")
        : !Number.isFinite(quantityNumber) || quantityNumber <= 0
          ? t("validation_positive_quantity")
          : null;

  useEffect(() => {
    if (!selectedLineId && inboundLines.data?.length) {
      setSelectedLineId(inboundLines.data[0].backendId);
    }
  }, [inboundLines.data, selectedLineId]);

  useEffect(() => {
    if (!locationId && locations.data?.length) {
      setLocationId(locations.data[0].id);
    }
  }, [locationId, locations.data]);

  useEffect(() => {
    if (line?.qtyRemaining) {
      setQuantity(String(line.qtyRemaining));
    }
  }, [line?.backendId, line?.qtyRemaining]);

  const handleSubmit = async () => {
    if (!line || validationMessage) {
      return;
    }
    await receiveLine.mutateAsync({
      inboundLineId: line.backendId,
      quantity: quantityNumber,
      locationId,
    });
  };

  return (
    <HandheldShell
      title={t("floor_receive_title")}
      subtitle={t("receiving_title")}
      footer={
        <button
          className="w-full rounded-2xl bg-emerald-500 px-4 py-4 text-lg font-semibold text-slate-950"
          onClick={() => void handleSubmit()}
          type="button"
        >
          {t("confirm")}
        </button>
      }
    >
      <div className="flex h-full flex-col justify-between gap-5">
        <div>
          <p className="text-sm text-slate-400">{t("scan_prompt")}</p>
          <div className="mt-4 rounded-[28px] border-2 border-dashed border-sky-500 px-4 py-10 text-center">
            <p className="text-3xl font-bold">{line?.sku ?? "PO-1001"}</p>
            <p className="mt-2 text-sm text-slate-400">{t("dock_receive_hint")}</p>
          </div>
          <div className="mt-5 grid gap-3">
            <SelectField
              label={t("receive_line_label")}
              onChange={setSelectedLineId}
              options={
                inboundLines.data?.map((entry) => ({
                  value: entry.backendId,
                  label: `${entry.sku} - ${entry.qtyReceived}/${entry.qtyExpected}`,
                })) ?? []
              }
              value={selectedLineId}
            />
            <SelectField
              label={t("location_label")}
              onChange={setLocationId}
              options={locations.data?.map((entry) => ({ value: entry.id, label: entry.label })) ?? []}
              value={locationId}
            />
            <input
              className="rounded-2xl border border-slate-700 bg-slate-900 px-4 py-3 text-white"
              onChange={(event) => setQuantity(event.target.value)}
              placeholder={t("quantity_placeholder")}
              value={quantity}
            />
            {line ? (
              <div className="rounded-2xl bg-slate-900/80 px-4 py-3 text-sm text-slate-300 ring-1 ring-slate-800">
                <p>{t("order_label")}: {line.orderNumber || "-"}</p>
                <p>{t("supplier_label")}: {line.supplierName || "-"}</p>
                <p>{t("remaining_label")}: {line.qtyRemaining}</p>
              </div>
            ) : null}
          </div>
        </div>
        <div className="rounded-3xl bg-slate-900 p-4 ring-1 ring-slate-800">
          <p className="text-xs uppercase tracking-[0.25em] text-sky-300">{t("next_step_label")}</p>
          <p className="mt-2 text-lg font-semibold">{t("receive_item_loop")}</p>
          {validationMessage ? <p className="mt-2 text-sm text-amber-300">{validationMessage}</p> : null}
          {receiveLine.isError ? (
            <p className="mt-2 text-sm text-rose-300">
              {getApiErrorMessage(receiveLine.error, t("action_failed"))}
            </p>
          ) : null}
          {receiveLine.isSuccess ? <p className="mt-2 text-sm text-emerald-400">{t("action_success")}</p> : null}
        </div>
      </div>
    </HandheldShell>
  );
}
