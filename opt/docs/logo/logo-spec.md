# DebVisor -- Designer Spec

Overview

- Concept: Minimal server "brick" with a visor band across the top third and a stack of 2-3 VM blocks in the lower area.

- Primary lockup: mark (left) + wordmark "DebVisor" (right).

- Compact lockup: mark above, wordmark centered below.

- Tiny icon: just the rounded rectangle with visor band.
Colors (hex)

- Dark charcoal (primary background / outline): #1E1E21

- Visor (accent): #D70A53

- VM light: #E5E5E8

- VM accent (optional): #4FC3F7

- White (for monochrome inverted): #FFFFFF
Wordmark

- Typeface: Geometric rounded sans (Rubik or Montserrat recommended)

- Treatment: "DebVisor" with capital D and V, rest lowercase.

- Subtle custom tweak: extend the arms of the "V" slightly outward (2-4% of type height) to visually echo the visor band. For precise control, convert wordmark to outlines and nudge V arms.

- Suggested weights: Semi-Bold (600) for web; Bold or converted outlines for print.
Spacing & padding

- Mark clearspace: at minimum, equal to the height of the VM block in the mark (base unit). Keep all clear space around the mark equal to that unit.

- Lockup spacing (mark to wordmark horizontally): 1.5? mark width's base unit (visually balanced).

- For compact vertical lockup, vertical gap mark-to-wordmark: 0.75? base unit.
Geometry

- Mark shape: rounded rectangle, slightly wider than tall.

- Visor height: ~24-33% of mark height (top third).

- VM area: lower ~60% of mark height; use 2-3 equally sized rounded squares/bars. Align them horizontally with even spacing; optionally stagger for depth.
Export sizes

- Vector (source): SVG / PDF / EPS (preferred).

- Raster exports: 16?16 (tiny icon), 24?24, 32?32, 48?48, 64?64, 128?128, 256?256, 512?512, 1024?1024.

- For favicons: generate multi-resolution favicon.ico or separate PNGs (16, 32, 48 px).
Monochrome / one-color

- Provide two monochrome versions:

- White-on-dark (for dark backgrounds).

- Dark-on-white (for light backgrounds).

- Ensure high contrast and remove small VM details for the smallest sizes (<=24px) -- use only server + visor.
Tiny icon guidance

- For 16?16 and 32?32, simplify to server shape + visor band only (no VM blocks).

- Use solid shapes; avoid strokes.
Accessibility

- Ensure contrast ratio >4.5:1 for small text and UI uses.

- Provide alt text: "DebVisor logo" and role attributes in SVGs as needed.
Deliverables checklist

- SVG master (mark + wordmark)

- SVG mark-only

- SVG monochrome variants

- 16/32/64/128/256/512 PNGs (transparent background)

- Favicon set (multi-res .ico + pngs)

- Wordmark converted to outlines (PDF or SVG paths)
License / usage

- Default: include a statement clarifying allowed uses (e.g., repository/project icon and branding). If needed I can add an explicit license file.
Notes

- For pixel-perfect reproduction on the web, convert the wordmark to outlines and embed it in the final SVG; otherwise specify webfont (Rubik/Montserrat) in the page CSS.

- If you want the V-arm tweak exactly, I can produce an outlined wordmark SVG where the V arms are extended and kerned precisely.
