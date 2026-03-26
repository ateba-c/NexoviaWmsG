import { createBrowserRouter } from "react-router-dom";

import { AppShell } from "@/app/AppShell";
import { AnalyticsPage } from "@/pages/AnalyticsPage";
import { CountingPage } from "@/pages/CountingPage";
import { DashboardPage } from "@/pages/DashboardPage";
import { FloorCountPage } from "@/pages/FloorCountPage";
import { FloorPickPage } from "@/pages/FloorPickPage";
import { FloorReceivePage } from "@/pages/FloorReceivePage";
import { PickingPage } from "@/pages/PickingPage";
import { ReceivingPage } from "@/pages/ReceivingPage";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <AppShell />,
    children: [
      { index: true, element: <DashboardPage /> },
      { path: "receiving", element: <ReceivingPage /> },
      { path: "picking", element: <PickingPage /> },
      { path: "counting", element: <CountingPage /> },
      { path: "analytics", element: <AnalyticsPage /> },
      { path: "floor/receive", element: <FloorReceivePage /> },
      { path: "floor/pick", element: <FloorPickPage /> },
      { path: "floor/count", element: <FloorCountPage /> },
    ],
  },
]);

