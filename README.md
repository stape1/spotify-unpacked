# Spotify Unwrapped Unpacked

## 2026 MDAP research collaboration

## Project Structure

```
spotify-unpacked/
├── e2e/                          # End-to-end tests (Playwright)
│   └── vue.spec.ts               # Browser-based integration tests
├── explorations/                  # Python data exploration scripts
│   ├── code/
│   │   ├── ExplorePlaylists.py               # Playlist usage analysis and visualisations
│   │   └── InitialExplorationofSpotifyJSONfiles.py  # Initial Spotify export exploration
│   └── images/                    # Output charts from exploration scripts
├── public/                        # Static assets served as-is
├── src/
│   ├── __tests__/                 # Unit tests (Vitest)
│   │   └── App.spec.ts
│   ├── assets/
│   │   └── main.css               # Global styles and Tailwind imports
│   ├── components/
│   │   ├── AppHeader.vue          # Top bar with title, theme toggle, and about popover
│   │   ├── ControlsPanel.vue     # Right sidebar — chart type selector and donate link
│   │   ├── DataPanel.vue         # Left sidebar — data upload zone and dataset stats
│   │   ├── VisualisationPanel.vue # Central panel wrapping the active chart
│   │   └── ui/                    # shadcn-vue primitives (button, card, dialog, etc.)
│   ├── lib/
│   │   └── utils.ts               # Tailwind class-merge helper (`cn()`)
│   ├── router/
│   │   └── index.ts               # Vue Router config (/ → Dashboard, /donate → Donate)
│   ├── stores/
│   │   ├── counter.ts             # Example Pinia store (unused placeholder)
│   │   └── visualisation.ts       # Tracks the currently selected chart type
│   ├── views/
│   │   ├── DashboardView.vue     # Main layout — three resizable panels
│   │   └── DonateView.vue        # Data donation page (placeholder)
│   ├── visualisations/
│   │   ├── ChartDisplay.vue      # Renders charts (8 types) with dark mode support
│   │   └── chart-setup.ts        # Registers Chart.js plugins and controllers
│   ├── App.vue                    # Root component — renders the router view
│   └── main.ts                    # App entry point — mounts Vue, Pinia, Router, Chart.js
├── components.json                # shadcn-vue configuration
├── eslint.config.ts               # ESLint + Oxlint + Playwright/Vitest rules
├── index.html                     # HTML shell — Vite entry point
├── package.json                   # Dependencies, scripts, and Node version requirements
├── playwright.config.ts           # E2E test config (Chromium, Firefox, WebKit)
├── vite.config.ts                 # Vite build config with Vue, DevTools, and Tailwind plugins
├── vitest.config.ts               # Unit test config
└── tsconfig*.json                 # TypeScript configs (app, node, vitest)
```

### Key areas

#### `src/views/` — Pages

- **DashboardView** — The main page. Lays out three horizontally resizable panels (data, visualisation, controls) using shadcn-vue's `ResizablePanel` components.
- **DonateView** — Placeholder for a future data donation workflow.

#### `src/components/` — UI building blocks

- **AppHeader** — Site title, a sun/moon/system theme toggle, and an about popover.
- **DataPanel** — Drop zone for uploading Spotify data exports and a summary card for loaded dataset statistics (upload not yet wired up).
- **VisualisationPanel** — Wrapper that renders the currently active chart inside a card.
- **ControlsPanel** — Dropdown to pick one of eight chart types and a card linking to the donate page.
- **ui/** — Auto-generated shadcn-vue primitive components (button, card, dialog, dropdown-menu, popover, resizable, scroll-area, select). These are scaffolded by the `shadcn` CLI and generally shouldn't be edited by hand.

#### `src/visualisations/` — Chart rendering

- **chart-setup.ts** — Registers every Chart.js controller, scale, and plugin the app uses so they're available globally.
- **ChartDisplay.vue** — Reads the selected chart type from the Pinia store and renders the matching Chart.js chart. Currently uses hardcoded sample data. Adapts colours for dark/light mode via `@vueuse/core`'s `useDark()`.

#### `src/stores/` — State management (Pinia)

- **visualisation.ts** — Holds the `selectedChart` ref that the controls panel writes and the chart display reads.
- **counter.ts** — Boilerplate example store, not currently used.

#### `explorations/` — Python analysis notebooks

Standalone Python scripts used for early-stage data exploration of Spotify JSON exports. They load playlist and streaming history files, build pandas DataFrames, and produce charts (saved to `explorations/images/`). These aren't part of the web app — they're reference material for understanding the data.
