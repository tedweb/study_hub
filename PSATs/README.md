# PSAT Study Guide & Progress Tracker

A personal study dashboard built from College Board PSAT practice-test results. Parses the answer key + rationales out of the raw test HTML, scores it, clusters the missed questions by topic, and generates targeted study guides and worksheets.

Live site: https://tedweb.github.io/psats/ (if GitHub Pages is enabled)

## What's here

| File | Purpose |
|---|---|
| [`index.html`](index.html) | Landing page — score cards, links to every report |
| [`PSAT1.html`](PSAT1.html) | Raw College Board practice test (source of truth) |
| [`PSAT1_summary.html`](PSAT1_summary.html) | Full results dashboard with every missed question + rationale |
| [`PSAT1_studyplan.html`](PSAT1_studyplan.html) | Personalized 4-week plan; links to guides & worksheets |
| `math_guide_*.html` | Topic-specific study guides (5 topics) with YouTube video references |
| `math_ws_*.html` | Practice worksheets — original misses plus fresh problems, with solutions |
| [`psat1_data.json`](psat1_data.json) | Structured answers, rationales, and score data extracted from the raw test |
| [`build_reports.py`](build_reports.py) | Regenerates `PSAT1_summary.html` from `psat1_data.json` |
| [`build_math_guides.py`](build_math_guides.py) | Regenerates all math guides and worksheets |

## Topic guides

Priority-ordered from the topics that cost the most points on Test #1:

1. **Quadratics** — discriminant, completing the square, Vieta's, vertex form
2. **Exponentials & Growth** — P(t)=P₀·r^t, doubling, geometric sequences
3. **Linear Equations** — no-solution systems, translations, intercepts
4. **Functions & Asymptotes** — evaluating, solving for a constant, rational graphs
5. **Percent & Exponents** — percent multipliers, fractional exponents

Each guide has a matching worksheet with step-by-step solutions.

## Regenerating

```bash
python3 build_reports.py       # rebuilds PSAT1_summary.html
python3 build_math_guides.py   # rebuilds all math guides + worksheets
```

Edit `psat1_data.json` first if you're correcting an answer or adding notes.

## Adding a new test

1. Save the College Board answer-and-rationale HTML as `PSAT2.html` (or similar).
2. Extract into `psat2_data.json` matching the schema in `psat1_data.json`.
3. Duplicate the build scripts and update the input/output filenames.
4. Add a new row of report tiles to `index.html`.
