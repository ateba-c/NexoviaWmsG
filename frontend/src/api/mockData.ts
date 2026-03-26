export const dashboardSummary = {
  ordersReceived: 28,
  ordersShipped: 19,
  returnsReceived: 4,
  picksCompleted: 132,
  countTasksCompleted: 7,
};

export const receivingQueue = [
  { id: "po-1001", supplier: "Northline Retail", status: "Dock Ready", lines: 12 },
  { id: "po-1002", supplier: "Medilogic", status: "QC Pending", lines: 4 },
];

export const pickTasks = [
  {
    backendId: "00000000-0000-0000-0000-000000000101",
    id: "PT-1",
    status: "OPEN",
    location: "A-01-B-03",
    sku: "SKU-BLK-01",
    quantity: 4,
    quantityPicked: 0,
    quantityRemaining: 4,
    order: "SO-1001",
  },
  {
    backendId: "00000000-0000-0000-0000-000000000102",
    id: "PT-2",
    status: "OPEN",
    location: "B-14-A-02",
    sku: "SKU-WHT-07",
    quantity: 2,
    quantityPicked: 0,
    quantityRemaining: 2,
    order: "SO-1008",
  },
];

export const countTasks = [
  {
    backendId: "00000000-0000-0000-0000-000000000201",
    itemId: "00000000-0000-0000-0000-000000000301",
    id: "COUNT-1",
    location: "C-01-01-01",
    type: "Cycle",
    status: "Open",
    itemSku: "SKU-CNT-01",
    resultCount: 1,
  },
  {
    backendId: "00000000-0000-0000-0000-000000000202",
    itemId: "00000000-0000-0000-0000-000000000302",
    id: "COUNT-2",
    location: "D-02-04-03",
    type: "Variance",
    status: "Open",
    itemSku: "SKU-RET-01",
    resultCount: 0,
  },
];
