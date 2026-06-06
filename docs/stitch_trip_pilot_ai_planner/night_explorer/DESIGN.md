---
name: Night Explorer
colors:
  surface: '#0e1416'
  surface-dim: '#0e1416'
  surface-bright: '#343a3c'
  surface-container-lowest: '#090f11'
  surface-container-low: '#171d1e'
  surface-container: '#1b2122'
  surface-container-high: '#252b2d'
  surface-container-highest: '#303638'
  on-surface: '#dee3e6'
  on-surface-variant: '#bcc9cd'
  inverse-surface: '#dee3e6'
  inverse-on-surface: '#2b3133'
  outline: '#869397'
  outline-variant: '#3d494c'
  surface-tint: '#4cd7f6'
  primary: '#4cd7f6'
  on-primary: '#003640'
  primary-container: '#06b6d4'
  on-primary-container: '#00424f'
  inverse-primary: '#00687a'
  secondary: '#4fdbc8'
  on-secondary: '#003731'
  secondary-container: '#04b4a2'
  on-secondary-container: '#003f38'
  tertiary: '#ffb95f'
  on-tertiary: '#472a00'
  tertiary-container: '#e79400'
  on-tertiary-container: '#563400'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#acedff'
  primary-fixed-dim: '#4cd7f6'
  on-primary-fixed: '#001f26'
  on-primary-fixed-variant: '#004e5c'
  secondary-fixed: '#71f8e4'
  secondary-fixed-dim: '#4fdbc8'
  on-secondary-fixed: '#00201c'
  on-secondary-fixed-variant: '#005048'
  tertiary-fixed: '#ffddb8'
  tertiary-fixed-dim: '#ffb95f'
  on-tertiary-fixed: '#2a1700'
  on-tertiary-fixed-variant: '#653e00'
  background: '#0e1416'
  on-background: '#dee3e6'
  surface-variant: '#303638'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '500'
    lineHeight: 32px
  body-lg:
    fontFamily: Inter
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 28px
  body-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.05em
  caption:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 8px
  container-margin: 24px
  gutter: 16px
  section-gap: 48px
  stack-sm: 8px
  stack-md: 16px
  stack-lg: 32px
---

## Brand & Style
The design system is engineered for "Night Explorer," a premium AI travel experience. The brand personality is cinematic, sophisticated, and forward-leaning, evoking the feeling of a luxury flight deck or a high-end AI operating system. 

The aesthetic leverages **Glassmorphism** and **Atmospheric Lighting** to create depth within a deep-space canvas. It prioritizes a dark, immersive environment that reduces cognitive load during late-night trip planning while using vibrant accents to highlight intelligent AI insights. The emotional response should be one of "effortless discovery"—where technology feels like a quiet, high-end concierge rather than a complex tool.

## Colors
The palette is built on a "Midnight Base" to provide maximum contrast for neon-inspired accents. 

- **Primary (Travel Cyan):** Used for main actions, active states, and AI-driven pathfinding.
- **Secondary (Teal):** Used for success states and secondary supportive branding.
- **Highlight (Warm Amber):** Reserved for "Golden Hour" moments—premium upgrades, saved favorites, and critical alerts.
- **Atmospheric Gradients:** Backgrounds should utilize subtle radial gradients of Cyan and Teal (at 5-10% opacity) to create a sense of horizon and depth, preventing the dark interface from feeling "flat."

## Typography
This design system utilizes **Inter** exclusively to maintain a clean, systematic, and utilitarian feel. 

- **Weight Strategy:** Use Bold/Semi-Bold for headlines to anchor the layout against the dark background. 
- **Legibility:** Body text uses the Secondary Text color (#94A3B8) to maintain hierarchy, while Primary Text (#F8FAFC) is reserved for headers and high-priority information.
- **Letter Spacing:** Labels use a slight tracking increase to enhance the "OS-feel" of the interface.

## Layout & Spacing
The layout follows a **Fluid Grid** model with a 12-column structure for desktop and a 4-column structure for mobile. 

- **Safe Zones:** High-margin layouts (24px+) are preferred to create a premium, uncrowded feel.
- **Rhythm:** Spacing is strictly based on an 8px linear scale. 
- **AI Focus:** Centralize the most complex AI interactions in "Wide" cards that span 8-10 columns on desktop to provide focus.

## Elevation & Depth
Depth is created through **Glassmorphism** rather than traditional drop shadows.

1.  **The Base Layer:** The solid #07111F background.
2.  **The Surface Layer:** Semi-transparent panels (`rgba(15, 23, 42, 0.78)`) with a `backdrop-filter: blur(12px)`.
3.  **The Stroke Layer:** A 1px border using the Border variable (`rgba(148, 163, 184, 0.12)`) provides definition.
4.  **The Glow Layer:** Interactive elements emit a soft 15px outer glow of their respective accent color (Cyan or Teal) when hovered or active.

## Shapes
The design system uses a generous **Rounded (16px)** corner radius to soften the technical nature of the UI, making it feel more approachable and "human."

- **Base Radius:** 16px (1rem) for cards, modals, and main containers.
- **Small Radius:** 8px (0.5rem) for input fields and small chips.
- **Pill Radius:** Used exclusively for buttons and status indicators to differentiate them from static containers.

## Components

- **Buttons:** Primary buttons use a solid Cyan gradient background with white text. Secondary buttons are "Ghost" style with a 1px border and blur background.
- **Cards:** Always use the glassmorphic surface. Cards should have a subtle top-down linear gradient (transparent to slightly opaque) to catch the "light" from the top of the screen.
- **Inputs:** Darker than the surface, with a 1px Cyan border appearing only on focus. Use a subtle inner shadow to create a "recessed" feel.
- **Chips:** Small, pill-shaped elements with 10% opacity fills of the accent colors.
- **AI Orbit:** A unique component—a rotating, soft-glow ring that surrounds user avatars or specific location icons when the AI is "calculating" or providing a live recommendation.
- **Navigation:** A docked, bottom-fixed glass bar with blurred background and icon-only indicators.