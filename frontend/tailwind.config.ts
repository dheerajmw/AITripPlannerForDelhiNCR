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
        background: "#0e1416",
        surface: "#0e1416",
        "surface-dim": "#0e1416",
        "surface-bright": "#343a3c",
        "surface-container-lowest": "#090f11",
        "surface-container-low": "#171d1e",
        "surface-container": "#1b2122",
        "surface-container-high": "#252b2d",
        "surface-container-highest": "#303638",
        "surface-variant": "#303638",
        "on-surface": "#dee3e6",
        "on-surface-variant": "#bcc9cd",
        "on-background": "#dee3e6",
        outline: "#869397",
        "outline-variant": "#3d494c",
        primary: "#4cd7f6",
        "on-primary": "#003640",
        "primary-container": "#06b6d4",
        "on-primary-container": "#00424f",
        "primary-fixed": "#acedff",
        secondary: "#4fdbc8",
        "on-secondary": "#003731",
        "secondary-container": "#04b4a2",
        "on-secondary-container": "#003f38",
        "secondary-fixed": "#71f8e4",
        tertiary: "#ffb95f",
        "on-tertiary": "#472a00",
        "tertiary-container": "#e79400",
        error: "#ffb4ab",
        "on-error": "#690005",
        "error-container": "#93000a",
        "on-error-container": "#ffdad6",
      },
      fontFamily: {
        sans: ["var(--font-inter)", "Inter", "system-ui", "sans-serif"],
        mono: ["var(--font-geist-mono)", "monospace"],
      },
      fontSize: {
        "display-lg": ["48px", { lineHeight: "56px", letterSpacing: "-0.02em", fontWeight: "700" }],
        "headline-lg": ["32px", { lineHeight: "40px", letterSpacing: "-0.01em", fontWeight: "600" }],
        "headline-md": ["24px", { lineHeight: "32px", fontWeight: "500" }],
        "headline-mobile": ["24px", { lineHeight: "32px", fontWeight: "600" }],
        "body-lg": ["18px", { lineHeight: "28px", fontWeight: "400" }],
        "body-md": ["16px", { lineHeight: "24px", fontWeight: "400" }],
        "body-sm": ["14px", { lineHeight: "1.5", fontWeight: "400" }],
        "label-md": ["14px", { lineHeight: "20px", letterSpacing: "0.05em", fontWeight: "600" }],
        "mono-xs": ["11px", { lineHeight: "1", letterSpacing: "0.1em", fontWeight: "500" }],
      },
      borderRadius: {
        xl: "0.75rem",
        "2xl": "1rem",
        "3xl": "1.5rem",
      },
      spacing: {
        "container-margin": "24px",
        "container-mobile": "20px",
        "container-desktop": "40px",
        gutter: "16px",
        "stack-sm": "8px",
        "stack-md": "16px",
        "stack-lg": "32px",
        "section-gap": "48px",
        "card-gap": "24px",
      },
      boxShadow: {
        glow: "0 0 20px rgba(6, 182, 212, 0.35)",
        "glow-lg": "0 0 35px rgba(6, 182, 212, 0.55)",
        "glow-btn": "0 8px 20px rgba(76, 215, 246, 0.25)",
        "sidebar-glow": "0 0 20px rgba(173, 198, 255, 0.1)",
      },
      backgroundImage: {
        "mesh-gradient":
          "radial-gradient(at 0% 0%, rgba(76, 215, 246, 0.12) 0px, transparent 50%), radial-gradient(at 100% 0%, rgba(79, 219, 200, 0.08) 0px, transparent 50%), radial-gradient(at 100% 100%, rgba(255, 185, 95, 0.05) 0px, transparent 50%)",
      },
      animation: {
        "pulse-ring": "pulse-ring 4s cubic-bezier(0.4, 0, 0.6, 1) infinite",
        float: "float 6s ease-in-out infinite",
        "orbit-spin": "spin 20s linear infinite",
      },
      keyframes: {
        "pulse-ring": {
          "0%": { transform: "scale(0.8)", opacity: "0" },
          "50%": { opacity: "0.5" },
          "100%": { transform: "scale(1.5)", opacity: "0" },
        },
        float: {
          "0%, 100%": { transform: "translateY(0)" },
          "50%": { transform: "translateY(-12px)" },
        },
      },
    },
  },
  plugins: [],
};

export default config;
