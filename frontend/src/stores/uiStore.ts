import { create } from "zustand";

type Language = "en-CA" | "fr-CA";

interface UIState {
  language: Language;
  setLanguage: (language: Language) => void;
}

export const useUIStore = create<UIState>((set) => ({
  language: "en-CA",
  setLanguage: (language) => set({ language }),
}));

