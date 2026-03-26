import { useMutation, useQueryClient } from "@tanstack/react-query";

import { apiClient } from "@/api/client";

export function useReceiveLine() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (payload: {
      inboundLineId: string;
      quantity: number;
      locationId: string;
      lotNumber?: string;
      expiryDate?: string;
    }) => {
      const response = await apiClient.post(`/inbound/lines/${payload.inboundLineId}/receive/`, {
        quantity: payload.quantity,
        location: payload.locationId,
        lot_number: payload.lotNumber ?? "",
        expiry_date: payload.expiryDate || null,
      });
      return response.data;
    },
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["receiving-queue"] });
      await queryClient.invalidateQueries({ queryKey: ["inbound-lines"] });
    },
  });
}

export function useStartPickTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (pickTaskId: string) => {
      const response = await apiClient.post(`/outbound/pick-tasks/${pickTaskId}/start/`);
      return response.data;
    },
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["pick-tasks"] });
    },
  });
}

export function useConfirmPickTask() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (payload: { pickTaskId: string; quantity: number }) => {
      const response = await apiClient.post(`/outbound/pick-tasks/${payload.pickTaskId}/confirm/`, {
        quantity: payload.quantity,
      });
      return response.data;
    },
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["pick-tasks"] });
      await queryClient.invalidateQueries({ queryKey: ["dashboard-summary"] });
    },
  });
}

export function useExecuteCount() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: async (payload: { countTaskId: string; itemId: string; countedQuantity: number }) => {
      const response = await apiClient.post(`/counting/tasks/${payload.countTaskId}/execute/`, {
        item: payload.itemId,
        counted_quantity: payload.countedQuantity,
      });
      return response.data;
    },
    onSuccess: async () => {
      await queryClient.invalidateQueries({ queryKey: ["count-tasks"] });
      await queryClient.invalidateQueries({ queryKey: ["dashboard-summary"] });
    },
  });
}
