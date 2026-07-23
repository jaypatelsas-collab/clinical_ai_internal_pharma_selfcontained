# Clinical AI Value & Governance Platform — Demo v1.4

## Portfolio expansion

This package contains **23 representative initiatives across 6 departments**:

- Biostatistics: 4
- Statistical Programming: 5
- Data Management: 4
- Clinical Operations: 4
- Medical Writing: 3
- Pharmacovigilance: 3

The initiatives span Experiment, Business Case, Pilot, Validation, Controlled Pilot, Scale Candidate and Production stages. Financial value, evidence strength, risk, compliance, adoption, incidents and governance actions are intentionally varied to create a realistic leadership demo.

## Existing v1.3 enhancements retained

- Department colors and initiative labels in the portfolio chart
- 0–100 department value scoring with maturity bands
- Clickable Governance Action Center
- Direct navigation from an alert to the selected initiative

## New in v1.4

- 23 realistic initiatives
- Expanded governance controls and incidents
- Updated department adoption metrics
- Portfolio-at-a-glance executive summary

## Run

```bash
pip install -r requirements.txt
streamlit run app.py
```

Representative synthetic data only. Not validated for production or GxP use.


## v1.4 interface refinement
- Added Clinexa AI branding across the module.
- Fixed title wrapping so the dashboard name remains fully visible.
- Replaced the auto-populated department multiselect with a single dropdown: All Departments or one selected department.
- Moved initiative-level governance alerts to a dedicated Governance Action Center page with a category dropdown.
- Used the reclaimed Executive Command Center space for lifecycle and evidence-maturity graphs.


## Executive dashboard refinement

- Header typography was reduced slightly and forced to wrap normally so the full **Clinical AI Value & Governance Platform** title remains visible at narrower browser widths.
- The lifecycle and evidence maturity charts were removed from the first page to reduce visual density.
- The Governance Action Center is now summarized directly on the Executive Command Center with one category dropdown and direct initiative navigation.
- The separate Governance Action Center navigation page was removed to keep the workflow simpler.


## Latest interface refinements
- Executive title shortened to **AI Value & Governance** to prevent truncation at narrower browser widths.
- Clinexa AI branding is retained in the colored left sidebar rather than repeated in the main title.
- The sidebar now uses a navy-to-teal Clinexa color treatment.
- Department filtering starts blank. Dashboard data appears only after selecting **All Departments** or one department.
- Governance Action Center Summary starts blank. Category results appear only after selecting High risk, Evidence needed, or Overdue governance.
