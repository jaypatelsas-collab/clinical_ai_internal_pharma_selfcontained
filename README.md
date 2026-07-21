# Clinical AI Value & Governance Platform

Internal pharmaceutical prototype for evaluating AI initiatives through a transparent, configurable scoring framework.

## Scoring design

The weighted base score contains five additive dimensions:

- Efficiency
- Quality
- Adoption
- Compliance
- Financial value

Risk and evidence strength are **not additive categories**. They are downward adjustments applied after the weighted base score. This prevents a high-risk or weakly evidenced initiative from appearing stronger simply because risk was included as a positive weighted dimension.

## Fixes in version 1.1

- Evidence-source confidence configuration now flows into score calculations through `Evidence_Source`.
- Exact evidence-source matches are supported, followed by documented keyword-based fallback and then the existing row value.
- Full scoring-schema validation covers score inputs, risk level, evidence fields, financial fields, IDs and dates.
- Uploaded CSV/XLSX initiative data can replace the active portfolio for the current Streamlit session after validation.
- Invalid or malformed files produce friendly errors instead of unhandled exceptions.
- Financial scoring is centralized in one function and reused by calculations and charts.
- The role selector is explicitly labeled as a persona preview, not access control.
- Representative CSV files remain visible in `data/`; the embedded dataset is only a deployment fallback.

## Deploy

Upload the following to the repository root:

- `app.py`
- `requirements.txt`
- `README.md`
- the complete `data/` folder

Then reboot the Streamlit application.

## Important

Representative data only. The prototype is not validated for production or GxP use and does not replace enterprise identity, eQMS, finance, validation or service-management systems.

## Version 1.2 demo-readiness fixes

- `Evidence_Strength` and `Benefit_Status` are now required by upload validation.
- Controlled values are validated before uploaded data can become active.
- Evidence-source resolution records Exact, Alias, Ambiguous fallback, or Unmapped fallback status.
- Ambiguous and unmapped sources retain the uploaded row-level confidence rather than being silently assigned to a possibly incorrect category.
- The Data Quality page lists evidence sources requiring administrator review.
