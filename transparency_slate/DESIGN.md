# Design System Specification: The Architectural Lens

## 1. Overview & Creative North Star
The creative North Star for this design system is **"The Architectural Lens."** 

In the context of "PropiedadTransparente," we are not merely building a dashboard; we are constructing a high-fidelity digital environment that mirrors the clarity and structure of modern architecture. This system moves away from the "boxy" nature of standard SaaS templates by embracing **Tonal Layering** and **Editorial Spacing**. 

By utilizing intentional asymmetry—such as placing high-density data tables against expansive, airy header sections—we create a rhythmic flow that guides the eye toward critical financial and property metrics. The goal is "Professionalism through Restraint": every pixel must serve a purpose, and every surface must feel like a physical layer of frosted glass or polished stone.

---

## 2. Colors & Surface Philosophy
This system relies on a sophisticated palette of deep blues and neutrals to establish trust. We reject the "flat" look of 2010s SaaS in favor of depth and atmospheric light.

### The "No-Line" Rule
**Explicit Instruction:** Designers are prohibited from using 1px solid borders to section off the UI. Containers must be defined solely through background color shifts or tonal transitions.
- **Example:** A `surface-container-low` sidebar sitting against a `surface` main content area provides a clean, borderless boundary that feels more integrated and high-end.

### Surface Hierarchy & Nesting
Treat the UI as a series of nested physical layers. Use the following tiers to define importance:
- **Surface (Base):** The foundation of the application.
- **Surface-Container-Low:** For large structural elements like sidebars or secondary navigation.
- **Surface-Container-Lowest:** For the primary content cards or data tables, providing the highest "lift."
- **Surface-Container-Highest:** For persistent utility panels or drawers that need to feel "closer" to the user.

### The "Glass & Gradient" Rule
To elevate the experience, floating elements (like dropdowns, modals, or top-bars) should utilize **Glassmorphism**:
- Use semi-transparent `surface` colors (e.g., `surface/80`) with a `backdrop-blur-md` effect.
- **Signature Textures:** For primary Action Buttons or high-level Metric Cards, use a subtle linear gradient: `primary` (#000000) to `primary_container` (#00174b). This creates a sense of "visual soul" and depth that static hex codes cannot provide.

---

## 3. Typography: The Editorial Scale
We pair the structural precision of **Manrope** for displays with the functional clarity of **Inter** for data.

- **Display & Headlines (Manrope):** Large, bold, and authoritative. These are used for page titles and high-level summaries. They should feel like an architectural blueprint—strong and intentional.
- **Body & Labels (Inter):** Highly legible and optimized for information density. Use `label-sm` for metadata and `body-md` for the bulk of administrative data.

The contrast between the wider, more geometric Manrope and the compact Inter creates a sophisticated "Editorial" look that distinguishes the brand from generic "out-of-the-box" dashboards.

---

## 4. Elevation & Depth: Tonal Layering
Traditional drop shadows are often messy. This system uses **Ambient Light** and **Soft Tones** to convey hierarchy.

- **The Layering Principle:** Depth is achieved by stacking. A `surface-container-lowest` card placed on a `surface-container-low` section creates a natural lift without a single line of CSS shadow.
- **Ambient Shadows:** When a float is required (e.g., a Modal), use an extra-diffused shadow: `shadow-[0_20px_50px_rgba(25,28,30,0.06)]`. The shadow is a low-opacity tint of the `on-surface` color, mimicking natural light.
- **The "Ghost Border" Fallback:** If accessibility requires a border, use the `outline_variant` token at **10-20% opacity**. Never use a 100% opaque, high-contrast border.

---

## 5. Components

### Buttons
- **Primary:** High-contrast `primary` background. Use a slight `xl` rounding. No border.
- **Secondary:** Use `secondary_container` background with `on_secondary_container` text. This avoids the "outlined" look and feels more integrated.
- **Tertiary:** No background. Bold `on_surface` text. Used for low-priority actions to maintain information hierarchy.

### Cards & Data Tables
- **Rule:** Forbid the use of divider lines between rows. 
- **Separation:** Use `8px` of vertical white space (spacing-2) or a subtle shift to `surface_container_high` on hover to indicate row selection.
- **Rounding:** All cards must use `rounded-lg` (1rem) to soften the professional tone.

### Metric Chips
- **Status Accents:** Use `error` (#ba1a1a) and `on_error_container` for alerts, but always against a `error_container` background to soften the visual "sting." This ensures the dashboard remains professional even when displaying warnings.

### Input Fields
- Avoid the "boxed-in" feel. Use `surface_container_highest` as the background with a `ghost border` that only activates (becomes slightly more opaque) on focus. This keeps the form-heavy administrative pages feeling light and airy.

---

## 6. Do's and Don'ts

### Do:
- **Do** use `surface_container_lowest` for the "white paper" feel of the main data area.
- **Do** lean into `Manrope` for large numerical values (KPIs) to make them feel like "hero" elements.
- **Do** use `Lucide React` icons with a `stroke-width` of 1.5px to maintain the refined, thin-line aesthetic.

### Don't:
- **Don't** use `#000000` for text unless it's a primary heading. Use `on_surface_variant` for body text to reduce eye strain.
- **Don't** use standard 1px borders to separate the sidebar from the content. Use a `16px` gap or a background color transition.
- **Don't** use "pure grey" for shadows. Always tint shadows with the `on_surface` color to maintain tonal harmony.

### Accessibility Note:
While we utilize tonal layering, ensure that the contrast ratio between nested surfaces meets WCAG AA standards. When in doubt, the `on_surface` text should always provide the primary contrast, rather than the container edge itself.