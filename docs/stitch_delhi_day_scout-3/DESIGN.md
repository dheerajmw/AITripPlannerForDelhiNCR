---
name: TripPilot AI
colors:
  surface: '#151024'
  surface-dim: '#151024'
  surface-bright: '#3b364c'
  surface-container-lowest: '#100b1f'
  surface-container-low: '#1d182d'
  surface-container: '#211d31'
  surface-container-high: '#2c273c'
  surface-container-highest: '#373247'
  on-surface: '#e7defb'
  on-surface-variant: '#d1c2d2'
  inverse-surface: '#e7defb'
  inverse-on-surface: '#322d43'
  outline: '#9a8c9b'
  outline-variant: '#4e4350'
  surface-tint: '#edb1ff'
  primary: '#edb1ff'
  on-primary: '#520070'
  primary-container: '#9d50bb'
  on-primary-container: '#fff3fd'
  inverse-primary: '#883ca6'
  secondary: '#5dd9d0'
  on-secondary: '#003734'
  secondary-container: '#00a29a'
  on-secondary-container: '#00302d'
  tertiary: '#d6baff'
  on-tertiary: '#40147a'
  tertiary-container: '#835dc0'
  on-tertiary-container: '#fcf4ff'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#f9d8ff'
  primary-fixed-dim: '#edb1ff'
  on-primary-fixed: '#320046'
  on-primary-fixed-variant: '#6e208c'
  secondary-fixed: '#7cf6ec'
  secondary-fixed-dim: '#5dd9d0'
  on-secondary-fixed: '#00201e'
  on-secondary-fixed-variant: '#00504c'
  tertiary-fixed: '#ecdcff'
  tertiary-fixed-dim: '#d6baff'
  on-tertiary-fixed: '#270057'
  on-tertiary-fixed-variant: '#573092'
  background: '#151024'
  on-background: '#e7defb'
  surface-variant: '#373247'
typography:
  display-lg:
    fontFamily: Geist
    fontSize: 48px
    fontWeight: '800'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Geist
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
  headline-lg-mobile:
    fontFamily: Geist
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
  body-md:
    fontFamily: Geist
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-mono:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '500'
    lineHeight: 20px
    letterSpacing: 0.05em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 8px
  xs: 4px
  sm: 12px
  md: 24px
  lg: 40px
  xl: 64px
  gutter: 16px
  margin-mobile: 20px
  margin-desktop: 120px
---

## Brand & Style
The design system is engineered for a futuristic, AI-driven exploration of Delhi. It targets tech-savvy travelers who seek a blend of ancient heritage and cutting-edge navigation. The emotional response is one of nocturnal mystery and high-tech efficiency—evoking the feeling of a high-end cockpit navigating a vibrant metropolis at night.

The visual style is **Glassmorphism-lite** integrated with **Modern Minimalism**. It relies on deep, atmospheric gradients to provide infinite depth, while UI surfaces use frosted-glass textures to maintain a sense of lightness despite the dark palette. Interactive elements feature subtle "inner glows" to simulate neon lighting, ensuring the AI-driven features feel active and intelligent.

## Colors
The palette is rooted in the "Delhi Dusk" concept. The base environment uses a vertical linear gradient from **Deep Indigo (#0D0B1F)** to a slightly warmer **Dark Purple (#1A0B2E)**.

- **Primary Accent (Electric Purple):** Used for primary actions, active states, and AI-driven insights. It should often be applied as a gradient with Neon Violet to create a "glowing" effect.
- **Secondary Accent (Cool Teal):** Reserved specifically for transit lines, map paths, and "on-time" status indicators to provide a high-contrast break from the purple hues.
- **Surfaces:** All containers use a semi-transparent purple tint (15-40% opacity) with a background blur (12px - 20px) and a subtle 1px inner border to catch highlights.

## Typography
The system utilizes **Geist** for its systematic, technical, yet highly legible personality. Headlines are set with tight tracking and heavy weights to command attention against the dark backgrounds. 

For data-heavy information such as departure times, ticket costs, and GPS coordinates, **JetBrains Mono** is introduced. This monospaced font reinforces the "AI/Technical" narrative and ensures that numerical data remains perfectly aligned and scannable in dense layouts.

## Layout & Spacing
The system follows a **8pt soft grid**. Layouts are primarily fluid but constrained by generous safe-area margins to ensure the "glass" cards don't feel cramped against the screen edges.

- **Mobile:** A single-column vertical stack with a 20px side margin. Cards should utilize the full width of the container.
- **Desktop/Tablet:** A 12-column grid. AI chat panels and map overlays should appear as floating modules rather than fixed sidebars, maintaining the "layered glass" philosophy. 
- **Rhythm:** Use "md" (24px) for spacing between distinct content sections and "sm" (12px) for elements within a single card or module.

## Elevation & Depth
Depth is not communicated through traditional black shadows, but through **light and blur**.

1.  **Level 1 (Base):** The deep indigo gradient background.
2.  **Level 2 (Cards):** Frosted glass surfaces (#23153D at 40% opacity) with a 20px backdrop blur. They feature a 1px top-down stroke (White at 10% opacity) to simulate a light source from above.
3.  **Level 3 (Popovers/Modals):** Increased opacity (60%) and a subtle outer glow using the Primary Accent color (#9D50BB) with a very large blur (40px+) and low opacity (15%) to make the element appear as if it is emitting light.

## Shapes
The shape language is consistently "Soft-Organic." All primary containers, buttons, and input fields use a **1rem (16px) radius** to offset the technical coldness of the dark theme. High-level feature cards or image carousels should use **1.5rem (24px)** for a more pronounced, friendly appearance. Smaller utility elements like tags or chips use a full-pill radius.

## Components
- **Buttons:** Primary buttons use a linear gradient (Electric Purple to Neon Violet). They have no border but feature a soft outer glow in the same hue. Text is uppercase Bold.
- **Inputs:** Fields are dark purple-tinted glass. On focus, the 1px border transitions from soft lavender to Cool Teal with a subtle inner shadow.
- **Chips:** Small, pill-shaped tags used for "Heritage," "Food," or "Quickest." They use a ghost-style (outline only) unless selected, where they fill with a semi-transparent Cool Teal.
- **Cards:** The hallmark component. Includes a 1px border-image gradient (White to Transparent) to create a "glass edge" effect. Images within cards should have a subtle dark overlay to ensure text remains legible.
- **AI Voyager HUD:** A unique component—a floating bottom bar that houses the AI search and voice activation, styled with a more intense blur and a pulsating Electric Purple "active" state.