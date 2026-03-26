import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        brand: {
          800: "var(--color-brand-800)",
          500: "var(--color-brand-500)"
        },
        accent: {
          500: "var(--color-accent-500)"
        }
      },
      fontFamily: {
        display: ["DM Sans", "system-ui", "sans-serif"],
        body: ["IBM Plex Sans", "system-ui", "sans-serif"],
        mono: ["IBM Plex Mono", "monospace"]
      }
    }
  },
  plugins: []
};

export default config;

