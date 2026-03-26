import { useQuery } from "@tanstack/react-query";

import { apiClient } from "@/api/client";
import { countTasks, pickTasks, receivingQueue } from "@/api/mockData";

function extractList<T>(payload: unknown): T[] {
  if (Array.isArray(payload)) {
    return payload as T[];
  }
  if (payload && typeof payload === "object" && Array.isArray((payload as { results?: unknown[] }).results)) {
    return (payload as { results: T[] }).results;
  }
  return [];
}

function extractDetail<T>(payload: unknown): T | null {
  if (payload && typeof payload === "object" && !Array.isArray(payload)) {
    return payload as T;
  }
  return null;
}

export function useReceivingQueue() {
  return useQuery({
    queryKey: ["receiving-queue"],
    queryFn: async () => {
      try {
        const response = await apiClient.get("/inbound/orders/");
        const items = extractList<{
          id: string;
          order_number: string;
          supplier_name: string;
          status: string;
          line_count?: number;
        }>(response.data);
        return items.map((item) => ({
          id: item.order_number,
          supplier: item.supplier_name || "Unknown",
          status: item.status,
          lines: item.line_count ?? 0,
        }));
      } catch {
        return receivingQueue;
      }
    },
  });
}

export function useInboundLines() {
  return useQuery({
    queryKey: ["inbound-lines"],
    queryFn: async () => {
      try {
        const response = await apiClient.get("/inbound/lines/");
        const items = extractList<{
          id: string;
          inbound_order: string;
          item: string;
          item_sku: string;
          order_number?: string;
          supplier_name?: string;
          line_number: number;
          qty_expected: number;
          qty_received: number;
          qty_remaining?: number;
        }>(response.data);
        return items.map((item) => ({
          backendId: item.id,
          orderId: item.inbound_order,
          itemId: item.item,
          sku: item.item_sku,
          orderNumber: item.order_number ?? "",
          supplierName: item.supplier_name ?? "",
          lineNumber: item.line_number,
          qtyExpected: item.qty_expected,
          qtyReceived: item.qty_received,
          qtyRemaining: item.qty_remaining ?? Math.max(item.qty_expected - item.qty_received, 0),
        }));
      } catch {
        return [];
      }
    },
  });
}

export function useInboundLineDetail(inboundLineId: string) {
  return useQuery({
    queryKey: ["inbound-line-detail", inboundLineId],
    enabled: Boolean(inboundLineId),
    queryFn: async () => {
      const response = await apiClient.get(`/inbound/lines/${inboundLineId}/`);
      const item = extractDetail<{
        id: string;
        inbound_order: string;
        item: string;
        item_sku: string;
        order_number?: string;
        supplier_name?: string;
        line_number: number;
        qty_expected: number;
        qty_received: number;
        qty_remaining?: number;
        requires_lot: boolean;
        requires_expiry: boolean;
      }>(response.data);
      if (!item) {
        return null;
      }
      return {
        backendId: item.id,
        orderId: item.inbound_order,
        itemId: item.item,
        sku: item.item_sku,
        orderNumber: item.order_number ?? "",
        supplierName: item.supplier_name ?? "",
        lineNumber: item.line_number,
        qtyExpected: item.qty_expected,
        qtyReceived: item.qty_received,
        qtyRemaining: item.qty_remaining ?? Math.max(item.qty_expected - item.qty_received, 0),
        requiresLot: item.requires_lot,
        requiresExpiry: item.requires_expiry,
      };
    },
  });
}

export function useLocations() {
  return useQuery({
    queryKey: ["locations"],
    queryFn: async () => {
      try {
        const response = await apiClient.get("/warehouse/locations/");
        const items = extractList<{ id: string; code: string }>(response.data);
        return items.map((item) => ({ id: item.id, label: item.code }));
      } catch {
        return [
          { id: "00000000-0000-0000-0000-000000000401", label: "A-01-B-03" },
          { id: "00000000-0000-0000-0000-000000000402", label: "C-01-01-01" },
        ];
      }
    },
  });
}

export function useItems() {
  return useQuery({
    queryKey: ["items"],
    queryFn: async () => {
      try {
        const response = await apiClient.get("/items/");
        const items = extractList<{ id: string; sku: string; description_en: string }>(response.data);
        return items.map((item) => ({
          id: item.id,
          sku: item.sku,
          description: item.description_en,
        }));
      } catch {
        return [
          { id: "00000000-0000-0000-0000-000000000301", sku: "SKU-CNT-01", description: "Cycle Count SKU" },
          { id: "00000000-0000-0000-0000-000000000302", sku: "SKU-RET-01", description: "Reserve SKU" },
        ];
      }
    },
  });
}

export function usePickTasks() {
  return useQuery({
    queryKey: ["pick-tasks"],
    queryFn: async () => {
      try {
        const response = await apiClient.get("/outbound/pick-tasks/");
        const items = extractList<{
          id: string;
          task_number: string;
          status: string;
          location_code: string;
          item_sku: string;
          quantity_to_pick: number;
          quantity_picked?: number;
          quantity_remaining?: number;
          order_number: string;
        }>(response.data);
        return items.map((item) => ({
          backendId: item.id,
          id: item.task_number,
          status: item.status,
          location: item.location_code,
          sku: item.item_sku,
          quantity: item.quantity_to_pick,
          quantityPicked: item.quantity_picked ?? 0,
          quantityRemaining: item.quantity_remaining ?? item.quantity_to_pick,
          order: item.order_number,
        }));
      } catch {
        return pickTasks;
      }
    },
  });
}

export function usePickTaskDetail(pickTaskId: string) {
  return useQuery({
    queryKey: ["pick-task-detail", pickTaskId],
    enabled: Boolean(pickTaskId),
    queryFn: async () => {
      const response = await apiClient.get(`/outbound/pick-tasks/${pickTaskId}/`);
      const item = extractDetail<{
        id: string;
        task_number: string;
        status: string;
        location_code: string;
        item_sku: string;
        quantity_to_pick: number;
        quantity_picked?: number;
        quantity_remaining?: number;
        order_number: string;
      }>(response.data);
      if (!item) {
        return null;
      }
      return {
        backendId: item.id,
        id: item.task_number,
        status: item.status,
        location: item.location_code,
        sku: item.item_sku,
        quantity: item.quantity_to_pick,
        quantityPicked: item.quantity_picked ?? 0,
        quantityRemaining: item.quantity_remaining ?? item.quantity_to_pick,
        order: item.order_number,
      };
    },
  });
}

export function useCountTasks() {
  return useQuery({
    queryKey: ["count-tasks"],
    queryFn: async () => {
      try {
        const response = await apiClient.get("/counting/tasks/");
        const items = extractList<{
          id: string;
          reference: string;
          location_code: string;
          task_type: string;
          status: string;
          result_count?: number;
          latest_item_id?: string;
          latest_item_sku?: string;
        }>(response.data);
        return items.map((item) => ({
          backendId: item.id,
          id: item.reference,
          itemId: item.latest_item_id ?? "",
          itemSku: item.latest_item_sku ?? "",
          location: item.location_code,
          type: item.task_type,
          status: item.status,
          resultCount: item.result_count ?? 0,
        }));
      } catch {
        return countTasks;
      }
    },
  });
}

export function useCountTaskDetail(countTaskId: string) {
  return useQuery({
    queryKey: ["count-task-detail", countTaskId],
    enabled: Boolean(countTaskId),
    queryFn: async () => {
      const response = await apiClient.get(`/counting/tasks/${countTaskId}/`);
      const item = extractDetail<{
        id: string;
        reference: string;
        location_code: string;
        task_type: string;
        status: string;
        result_count?: number;
        latest_item_id?: string;
        latest_item_sku?: string;
      }>(response.data);
      if (!item) {
        return null;
      }
      return {
        backendId: item.id,
        id: item.reference,
        itemId: item.latest_item_id ?? "",
        itemSku: item.latest_item_sku ?? "",
        location: item.location_code,
        type: item.task_type,
        status: item.status,
        resultCount: item.result_count ?? 0,
      };
    },
  });
}
