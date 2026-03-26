import i18n from "i18next";
import { initReactI18next } from "react-i18next";

import enCommon from "@/locales/en-CA/common.json";
import frCommon from "@/locales/fr-CA/common.json";

void i18n.use(initReactI18next).init({
  lng: "en-CA",
  fallbackLng: "en-CA",
  resources: {
    "en-CA": { common: enCommon },
    "fr-CA": { common: frCommon },
  },
  defaultNS: "common",
  ns: ["common"],
  interpolation: { escapeValue: false },
});

export { i18n };

