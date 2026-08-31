# Clara's Study Hub

A collection of study materials, practice test reviews, and personalized study plans.

## Getting Started

Open [index.html](index.html) in a browser to access the study hub landing page, which links to all study areas.

## Contents

### [PSATs/](PSATs/)
PSAT practice test analysis and study materials.

- **[PSATs/index.html](PSATs/index.html)** — Score dashboard and entry point
- **PSAT1.html** — Full source of PSAT Practice Test 1
- **PSAT1_summary.html** — Results overview: section/module scores, missed questions with rationale
- **PSAT1_studyplan.html** — 4-week personalized study plan built from the misses
- **math_guide_*.html** — Topic study guides (linear, quadratics, exponentials, functions, percent/exponents)
- **math_ws_*.html** — Practice worksheets for each math topic
- **build_math_guides.py / build_reports.py** — Python generators for the guides and reports
- **psat1_data.json** — Raw test data

### [AP Precalculus Test Review 1/](AP%20Precalculus%20Test%20Review%201/)
Interactive review for AP Precalculus sections 1.1–1.6.

- **[AP Precalculus Test Review 1/index.html](AP%20Precalculus%20Test%20Review%201/index.html)** — Interactive quiz with score tracking; select A–D and submit to unlock the explanation for each question

## Structure

```
Clara/
├── index.html                          # Landing page linking to all study areas
├── README.md
├── PSATs/
│   ├── index.html
│   ├── PSAT1.html
│   ├── PSAT1_summary.html
│   ├── PSAT1_studyplan.html
│   ├── math_guide_*.html
│   ├── math_ws_*.html
│   └── build_*.py
└── AP Precalculus Test Review 1/
    └── index.html
```
