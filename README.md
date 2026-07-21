# Clinical AI Value & Governance Platform

Internal pharma prototype for evaluating AI initiatives across value, quality, adoption, governance, evidence strength, financial benefit and operational risk.

## New configurable scoring engine

The Scoring Configuration page supports:

- Configurable category weights
- Evidence-source confidence mappings
- Configurable risk penalties
- Transparent initiative-level score calculations
- Draft/review/publish simulation
- Scoring model version display
- Session-level restore to defaults

The prototype formula is:

Final AI Score = Weighted Base Score - Evidence Adjustment - Risk Adjustment

Configuration changes are session-based in this prototype. A production implementation should store approved versions in a controlled database with authentication, approval workflow, audit trails and effective dates.

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

The application uses external CSV files when the `data` directory is present and embedded representative data as a fallback.

> Prototype only. Not validated for production or GxP use. Do not load patient-identifiable or confidential production data without an approved architecture.
