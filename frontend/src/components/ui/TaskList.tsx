interface TaskItem {
  id: string;
  [key: string]: string | number;
}

interface TaskListProps<T extends TaskItem> {
  items: T[];
  columns: Array<{ key: keyof T; label: string }>;
}

export function TaskList<T extends TaskItem>({ items, columns }: TaskListProps<T>) {
  return (
    <div className="grid gap-3">
      {items.map((item) => (
        <article
          key={item.id}
          className="grid gap-2 rounded-2xl border border-slate-200 bg-slate-50 px-4 py-4 text-sm text-slate-700"
        >
          {columns.map((column) => (
            <div key={String(column.key)} className="flex items-center justify-between gap-4">
              <span className="text-slate-400">{column.label}</span>
              <span className="font-semibold text-slate-900">{String(item[column.key])}</span>
            </div>
          ))}
        </article>
      ))}
    </div>
  );
}

