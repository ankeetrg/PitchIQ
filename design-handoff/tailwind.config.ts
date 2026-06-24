import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: ['selector', '[data-theme="dark"]'],
  content: [
    "./app/**/*.{ts,tsx}",
    "./components/**/*.{ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        navy: { DEFAULT: "#091525", 2: "#0C1C2E" },
        gold: {
          DEFAULT: "#D97706",
          hover: "#B45309",
          dim: "rgba(217,119,6,0.10)",
          border: "rgba(217,119,6,0.24)",
        },
        green: {
          DEFAULT: "#00963F",
          hover: "#007B33",
          dim: "rgba(0,150,63,0.10)",
          border: "rgba(0,150,63,0.22)",
        },
        red: { DEFAULT: "#DC2626", dim: "rgba(220,38,38,0.10)" },
        blue: { DEFAULT: "#2563EB", dim: "rgba(37,99,235,0.10)" },
        // theme-aware surfaces (driven by CSS variables in globals.css)
        bg: "var(--bg)",
        bg2: "var(--bg2)",
        surf: "var(--surf)",
        b1: "var(--b1)",
        b2: "var(--b2)",
        t1: "var(--t1)",
        t2: "var(--t2)",
        t3: "var(--t3)",
        t4: "var(--t4)",
      },
      fontFamily: {
        cond: ['var(--font-cond)', '"Barlow Condensed"', "Arial Narrow", "sans-serif"],
        sans: ['var(--font-inter)', "Inter", "system-ui", "sans-serif"],
      },
      borderRadius: {
        DEFAULT: "6px",
        lg: "12px",
      },
      maxWidth: {
        site: "1360px",
      },
      boxShadow: {
        card: "0 1px 3px rgba(15,10,5,0.05), 0 4px 14px rgba(15,10,5,0.04)",
        "card-hover": "0 6px 20px rgba(15,10,5,0.11), 0 16px 40px rgba(15,10,5,0.07)",
      },
    },
  },
  plugins: [],
};

export default config;
