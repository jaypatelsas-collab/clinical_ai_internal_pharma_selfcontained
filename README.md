# Clinical AI Value & Governance Platform — Internal Pharma Prototype

This Streamlit prototype is designed for internal pharmaceutical-company evaluation of AI initiatives. It uses representative dummy data and separates forecast, validated and realized benefits.

## Included modules
- Executive Command Center
- Controlled AI Initiative Registry
- Value and Evidence scorecard
- Governance and Risk controls
- Adoption and Maturity
- Incidents and Corrective Actions
- Data Quality and Integration catalog
- Admin Data Manager with downloadable templates

## Repository structure
```
app.py
requirements.txt
data/
  initiatives.csv
  initiative_registry.csv
  governance_controls.csv
  monthly_trends.csv
  adoption.csv
  incidents.csv
  data_source_catalog.csv
```

## Run locally
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python -m streamlit run app.py
```

## Private deployment
For internal testing, deploy inside a company-approved environment using SSO, role-based access, secrets management, audit logging, an approved database and separate development/test/production environments.

Do not load patient-identifiable or confidential production data into this prototype. It is not a validated GxP system.
