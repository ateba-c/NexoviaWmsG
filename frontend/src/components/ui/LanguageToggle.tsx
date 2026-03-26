import { useTranslation } from "react-i18next";

import { useUIStore } from "@/stores/uiStore";
import { i18n } from "@/app/i18n";

export function LanguageToggle() {
  const { t } = useTranslation();
  const language = useUIStore((state) => state.language);
  const setLanguage = useUIStore((state) => state.setLanguage);

  const changeLanguage = async (nextLanguage: "en-CA" | "fr-CA") => {
    setLanguage(nextLanguage);
    await i18n.changeLanguage(nextLanguage);
  };

  return (
    <div className="inline-flex rounded-full border border-slate-300 bg-white p-1 shadow-sm">
      {(["en-CA", "fr-CA"] as const).map((code) => (
        <button
          key={code}
          className={`rounded-full px-3 py-1 text-xs font-semibold ${
            language === code ? "bg-slate-900 text-white" : "text-slate-600"
          }`}
          onClick={() => void changeLanguage(code)}
          type="button"
        >
          {code === "en-CA" ? t("language_en") : t("language_fr")}
        </button>
      ))}
    </div>
  );
}

