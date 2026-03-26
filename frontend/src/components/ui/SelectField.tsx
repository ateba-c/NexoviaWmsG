interface SelectFieldOption {
  value: string;
  label: string;
}

interface SelectFieldProps {
  label: string;
  value: string;
  options: SelectFieldOption[];
  onChange: (value: string) => void;
}

export function SelectField({ label, value, options, onChange }: SelectFieldProps) {
  return (
    <label className="grid gap-2 text-left">
      <span className="text-xs uppercase tracking-[0.25em] text-slate-400">{label}</span>
      <select
        className="rounded-2xl border border-slate-700 bg-slate-900 px-4 py-3 text-white"
        onChange={(event) => onChange(event.target.value)}
        value={value}
      >
        <option value="">Select</option>
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </label>
  );
}
