# Architecture Overview

The simulator is intentionally lightweight: a single Flask application renders
a pair of Jinja templates and delegates all scheduling logic to plain Python
functions. This document highlights the moving parts so that new contributors can
navigate the repository quickly.

```
Browser ⟷ Flask routes ⟷ Scheduling helpers ⟷ Rendered templates
```

## Components

### 1. Flask app (`app.py`)

- Defines the `Process` data container and helper functions that implement the
  scheduling algorithms.
- Exposes two routes:
  - `GET /` renders the configuration form.
  - `POST /simulate` runs the selected algorithms, computes aggregate metrics,
    and returns the results dashboard.
- Uses Python's standard library only (plus Flask) so that behaviour is easy to
  debug with prints or breakpoints.

### 2. Templates (`templates/index.html`, `templates/results.html`)

- Rely on Bootstrap 4 for layout and styling. No build tooling is required.
- `index.html` provides the configuration controls and live preview panel.
- `results.html` displays one card per algorithm, each containing an animated
  Gantt chart, collapsible tables, and a Chart.js dashboard comparing averages.
- Inline JavaScript handles the simple UI interactions (animations and
  localStorage persistence for saved scenarios).

### 3. Static assets (CDNs)

- Bootstrap CSS/JS and Chart.js are loaded via CDN links to reduce repository
  size.
- jQuery is bundled purely to simplify DOM manipulation in the templates.

### 4. Documentation (`docs/`)

- `algorithms.md` – explains the scheduling strategies and implementation
  choices.
- `user-guide.md` – offers a walkthrough of the UI for newcomers.
- `architecture.md` – this document.
- `assets/` – diagrams and screenshots referenced by the Markdown files.

## Data Flow

1. **Process generation** – `generate_processes` creates the baseline workload
   according to the user-configured ranges.
2. **Transient events** – `apply_transient_event_choice` optionally injects extra
   processes mid-simulation (e.g., a high-priority job at time=10).
3. **Simulation loop** – For each selected algorithm the app copies the workload
   to avoid cross-contamination, runs the scheduling function, and stores the
   resulting metrics.
4. **Rendering** – A summary dictionary plus per-algorithm details are passed to
   the results template, which handles visualisation.

All state lives in memory for the lifetime of the request; there is no database
or background worker.

## Deployment

The provided `Dockerfile` installs dependencies from `requirements.txt` and runs
Gunicorn bound to port `5000`. For production use consider setting
`FLASK_ENV=production` and fronting the container with a reverse proxy such as
NGINX for TLS termination.

