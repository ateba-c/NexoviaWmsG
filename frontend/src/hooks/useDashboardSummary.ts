import { useQuery } from "@tanstack/react-query";

import { apiClient } from "@/api/client";
import { dashboardSummary } from "@/api/mockData";

export function useDashboardSummary() {
  return useQuery({
    queryKey: ["dashboard-summary"],
    queryFn: async () => {
      try {
        const response = await apiClient.get("/analytics/metrics/summary/");
        return {
          ordersReceived: response.data.orders_received ?? 0,
          ordersShipped: response.data.orders_shipped ?? 0,
          returnsReceived: response.data.returns_received ?? 0,
          picksCompleted: response.data.picks_completed ?? 0,
          countTasksCompleted: response.data.count_tasks_completed ?? 0,
        } satisfies typeof dashboardSummary;
      } catch {
        return dashboardSummary;
      }
    },
  });
}
