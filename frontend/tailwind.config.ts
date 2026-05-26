import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: [
    "./pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./components/**/*.{js,ts,jsx,tsx,mdx}",
    "./app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        background: "#151024",
        surface: "#151024",
        "surface-dim": "#151024",
        "surface-bright": "#3b364c",
        "surface-container-lowest": "#100b1f",
        "surface-container-low": "#1d182d",
        "surface-container": "#211d31",
        "surface-container-high": "#2c273c",
        "surface-container-highest": "#373247",
        "on-surface": "#e7defb",
        "on-surface-variant": "#d1c2d2",
        outline: "#9a8c9b",
        "outline-variant": "#4e4350",
        primary: "#edb1ff",
        "on-primary": "#520070",
        "primary-container": "#9d50bb",
        "on-primary-container": "#fff3fd",
        secondary: "#5dd9d0",
        "on-secondary": "#003734",
        "secondary-container": "#00a29a",
        "on-secondary-container": "#00302d",
        tertiary: "#d6baff",
        "on-tertiary": "#40147a",
        error: "#ffb4ab",
        "on-error": "#690005",
        "error-container": "#93000a",
        "on-error-container": "#ffdad6",
      },
      fontFamily: {
        sans: ["var(--font-geist-sans)", "system-ui", "sans-serif"],
        mono: ["var(--font-geist-mono)", "monospace"],
      },
      fontSize: {
        "display-lg": ["48px", { lineHeight: "56px", letterSpacing: "-0.02em", fontWeight: "800" }],
        "headline-lg": ["32px", { lineHeight: "40px", fontWeight: "700" }],
        "headline-md": ["24px", { lineHeight: "1.3", letterSpacing: "-0.02em", fontWeight: "700" }],
        "headline-mobile": ["24px", { lineHeight: "32px", fontWeight: "700" }],
        "body-md": ["16px", { lineHeight: "24px", fontWeight: "400" }],
        "body-sm": ["14px", { lineHeight: "1.5", fontWeight: "400" }],
        "label-mono": ["14px", { lineHeight: "20px", letterSpacing: "0.05em", fontWeight: "500" }],
        "mono-xs": ["11px", { lineHeight: "1", letterSpacing: "0.1em", fontWeight: "500" }],
      },
      borderRadius: {
        xl: "0.75rem",
        "2xl": "1rem",
        "3xl": "1.5rem",
      },
      spacing: {
        "container-mobile": "20px",
        "container-desktop": "40px",
        "card-gap": "24px",
      },
      boxShadow: {
        glow: "0 0 20px rgba(157, 80, 187, 0.3)",
        "glow-lg": "0 0 30px rgba(157, 80, 187, 0.5)",
        "glow-btn": "0 8px 20px rgba(157, 80, 187, 0.2)",
      },
      backgroundImage: {
        "mesh-gradient":
          "radial-gradient(at 0% 0%, rgba(157, 80, 187, 0.15) 0px, transparent 50%), radial-gradient(at 100% 0%, rgba(93, 217, 208, 0.1) 0px, transparent 50%), radial-gradient(at 100% 100%, rgba(237, 177, 255, 0.05) 0px, transparent 50%), radial-gradient(at 0% 100%, rgba(0, 162, 154, 0.1) 0px, transparent 50%)",
      },
    },
  },
  plugins: [],
};

export default config;
