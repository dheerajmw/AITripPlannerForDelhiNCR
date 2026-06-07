---
name: Purple Aurora
colors:
  surface: '#0f131d'
  surface-dim: '#0f131d'
  surface-bright: '#353944'
  surface-container-lowest: '#0a0e17'
  surface-container-low: '#171c25'
  surface-container: '#1b2029'
  surface-container-high: '#262a34'
  surface-container-highest: '#31353f'
  on-surface: '#dfe2f0'
  on-surface-variant: '#cbc3d7'
  inverse-surface: '#dfe2f0'
  inverse-on-surface: '#2c303b'
  outline: '#958ea0'
  outline-variant: '#494454'
  surface-tint: '#d0bcff'
  primary: '#d0bcff'
  on-primary: '#3c0091'
  primary-container: '#a078ff'
  on-primary-container: '#340080'
  inverse-primary: '#6d3bd7'
  secondary: '#ddb7ff'
  on-secondary: '#490080'
  secondary-container: '#6f00be'
  on-secondary-container: '#d6a9ff'
  tertiary: '#ffb0cd'
  on-tertiary: '#640039'
  tertiary-container: '#f751a1'
  on-tertiary-container: '#570032'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#e9ddff'
  primary-fixed-dim: '#d0bcff'
  on-primary-fixed: '#23005c'
  on-primary-fixed-variant: '#5516be'
  secondary-fixed: '#f0dbff'
  secondary-fixed-dim: '#ddb7ff'
  on-secondary-fixed: '#2c0051'
  on-secondary-fixed-variant: '#6900b3'
  tertiary-fixed: '#ffd9e4'
  tertiary-fixed-dim: '#ffb0cd'
  on-tertiary-fixed: '#3e0022'
  on-tertiary-fixed-variant: '#8c0053'
  background: '#0f131d'
  on-background: '#dfe2f0'
  surface-variant: '#31353f'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '800'
    lineHeight: 56px
    letterSpacing: -0.02em
  display-lg-mobile:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '800'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
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
  base: 4px
  xs: 8px
  sm: 16px
  md: 24px
  lg: 40px
  xl: 64px
  container-max: 1280px
  gutter: 24px
---

## Brand & Style
The design system is engineered for a high-end, AI-native travel experience that feels both cinematic and deeply intelligent. It targets luxury travelers who value seamless, futuristic automation. 

The aesthetic is **Glassmorphic Minimalism** set against a deep cosmic backdrop. It leverages high-contrast vibrant accents against dark, layered surfaces to create a sense of infinite depth. Every interaction should feel like navigating a high-tech flight deck, using "Purple Aurora" gradients to signify AI activity and premium status. The emotional response is one of calm confidence, technological sophistication, and the excitement of modern exploration.

## Colors
The palette is rooted in a "Deep Space" foundation to allow the purple and pink accents to vibrate. 

- **Primary & Secondary Accents:** Used for interactive states, progress indicators, and AI-driven insights.
- **Glow & Highlight:** Reserved for active focus states, "magic" moments (AI suggestions), and high-priority call-to-actions.
- **Surfaces:** Use the secondary background for sectioning. The card background must always implement a `backdrop-filter: blur(12px)` to maintain the glassmorphic luxury feel.
- **Aurora Gradients:** Apply linear gradients moving from `#8B5CF6` to `#EC4899` at 45-degree angles for primary buttons and brand-heavy ornaments.

## Typography
This design system utilizes **Inter** exclusively to maintain a systematic, technical, and highly legible appearance. 

Headings should be set with tight letter-spacing to feel "impactful" and "contained." Display sizes are reserved for destination names and primary AI prompts. Labels use uppercase styling with increased tracking to evoke a "instrument panel" aesthetic found in high-end cockpits. Ensure a high contrast ratio by using `text_primary` for all critical information and `text_secondary` for metadata and descriptions.

## Layout & Spacing
The system follows a **12-column fluid grid** for desktop and a **4-column grid** for mobile. 

- **Generous Padding:** To maintain the luxury feel, utilize the `lg` (40px) spacing for internal card padding and section vertical spacing.
- **AI Focus:** Centrally aligned layouts are preferred for "AI Chat" or "Search" modes to focus the user's attention.
- **Safe Zones:** Ensure a minimum 24px margin on mobile devices to prevent content from touching the screen edges.
- **Rhythm:** All spacing must be a multiple of the 4px base unit to ensure mathematical harmony across the UI.

## Elevation & Depth
Depth is created through transparency and "light-leaks" rather than traditional heavy shadows.

- **Stacking Logic:** 
  - **Level 0 (Background):** Deep `#070B14` with occasional aurora blurs (fixed background).
  - **Level 1 (Cards):** Glassmorphic surfaces with `backdrop-filter: blur(16px)` and a 1px border of `border_subtle`.
  - **Level 2 (Modals/Popovers):** Higher opacity secondary background with a "Neon Glow" outer shadow using `#C084FC` at 15% opacity.
- **Glow Effects:** Critical components (like the "Plan My Trip" button) should utilize a soft back-glow (drop-shadow) using the primary accent color to simulate light emission.

## Shapes
The shape language is consistently **Rounded**, striking a balance between organic travel and technical precision.

- **Standard Elements:** Buttons and input fields use the `0.5rem` (8px) radius.
- **Container Elements:** Large itinerary cards and modals use the `rounded-xl` (1.5rem / 24px) radius to soften the futuristic aesthetic and make it feel more approachable.
- **Interactive States:** On hover, shapes may slightly expand (1-2%) to provide tactile feedback.

## Components

### Buttons
- **Primary:** Gradient fill (`#8B5CF6` to `#A855F7`), white text, and a 10px outer glow on hover.
- **Secondary:** Transparent background, 1px border of `primary_accent`, and blurred backdrop.
- **Ghost:** No border, `text_secondary`, turning `text_primary` on hover with a subtle purple underline.

### Cards & Itinerary Items
Cards are the heart of the system. They must feature a 1px top-down linear gradient border (white at 10% to white at 0%) to simulate a "specular highlight" on the top edge. Use `background_card` for the fill.

### Input Fields
Inputs should be dark and recessed. Use `background_secondary` with a bottom-only border that glows purple when the field is focused. Placeholder text should use `text_secondary`.

### Chips & Tags
Used for "Tags" (e.g., "Non-stop", "Luxury", "Beach"). Use a semi-transparent purple fill with `label-md` typography.

### Progress & AI Indicators
AI "thinking" states should be represented by a pulsing aurora gradient line or a rotating soft-glow ring. Use smooth, ease-in-out transitions for all state changes (300ms duration).

### Navigation
A floating bottom-bar or glassmorphic sidebar. Icons should be thin-stroke (1.5px) and glow when active.