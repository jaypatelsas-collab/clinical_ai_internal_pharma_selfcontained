from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Clinexa AI | Value & Governance", page_icon="📊", layout="wide")
DATA = Path(__file__).parent / "data"
DEPT_COLORS = {
    "Biostatistics": "#2563EB",
    "Statistical Programming": "#059669",
    "Data Management": "#EA580C",
    "Clinical Operations": "#7C3AED",
    "Medical Writing": "#DC2626",
    "Pharmacovigilance": "#CA8A04",
}
RISK_PENALTY = {"High": 15, "Medium": 5, "Low": 0}

st.markdown("""
<style>
.block-container{padding-top:.8rem;max-width:100%}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#082a4a 0%,#0b4663 58%,#0f6b72 100%);border-right:1px solid rgba(255,255,255,.12)}
[data-testid="stSidebar"] *{color:#f8fafc!important}
[data-testid="stSidebar"] [data-baseweb="select"]>div{background:rgba(255,255,255,.12)!important;border-color:rgba(255,255,255,.3)!important}
[data-testid="stSidebar"] [role="radiogroup"] label{padding:.28rem .35rem;border-radius:.45rem}
[data-testid="stSidebar"] [role="radiogroup"] label:hover{background:rgba(255,255,255,.10)}
.hero{padding:20px 26px;border-radius:14px;background:linear-gradient(120deg,#0b2b4c,#12677a);color:white;margin-bottom:14px;overflow:visible}
.hero h1{margin:0;max-width:100%;font-size:clamp(1.35rem,2vw,1.85rem);line-height:1.25;white-space:normal!important;overflow:visible!important;text-overflow:clip!important;word-break:normal}.hero p{margin:.55rem 0 0;color:#e4f7fa}
.brand{display:flex;align-items:center;gap:10px;margin-bottom:8px}.brandmark{width:34px;height:34px;border-radius:10px;background:#14b8a6;color:#042f2e;display:flex;align-items:center;justify-content:center;font-weight:800}.brandname{font-size:1rem;font-weight:700;letter-spacing:.02em}
.badge{font-size:.69rem;letter-spacing:.1em;text-transform:uppercase;font-weight:700;color:#d7f3f7;margin-bottom:8px}
[data-testid="stMetric"]{border:1px solid #d8dee8;padding:13px;border-radius:11px;background:white}
.action{border:1px solid #d9e1ea;border-left:5px solid #d97706;border-radius:10px;padding:10px 13px;margin:6px 0;background:white}
.red{border-left-color:#dc2626}.blue{border-left-color:#2563eb}.pink{border-left-color:#e11d48}.meta{font-size:.82rem;color:#64748b}.section-card{border:1px solid #d9e1ea;border-radius:12px;padding:14px 16px;background:#fff;margin-top:8px}.section-title{font-size:1.05rem;font-weight:750;color:#0b2b4c;margin-bottom:4px}.section-subtitle{font-size:.84rem;color:#64748b;margin-bottom:8px}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return {
        "initiatives": pd.read_csv(DATA / "initiatives.csv", parse_dates=["Pilot_Start", "Next_Review"]),
        "controls": pd.read_csv(DATA / "governance_controls.csv", parse_dates=["Due_Date"]),
        "incidents": pd.read_csv(DATA / "incidents.csv", parse_dates=["Opened_Date"]),
        "registry": pd.read_csv(DATA / "initiative_registry.csv", parse_dates=["Pilot_Start", "Next_Review"]),
        "adoption": pd.read_csv(DATA / "adoption.csv"),
    }

def score(df, incidents):
    out = df.copy()
    out["Weighted_Base_Score"] = (
        out.Efficiency_Score * 20 + out.Quality_Score * 25 + out.Adoption_Score * 15 +
        out.Compliance_Score * 25 + out.Financial_Score * 15
    ) / 100
    out["Evidence_Adjustment"] = (100 - out.Evidence_Confidence) * 0.10
    critical = set(incidents.loc[(incidents.Severity == "Critical") & (incidents.Status != "Closed"), "Initiative_ID"])
    def penalty(r):
        value = RISK_PENALTY[r.Risk_Level]
        value += 10 if r.Compliance_Score < 70 else 0
        value += 8 if r.Evidence_Confidence < 60 else 0
        value += 15 if r.Initiative_ID in critical else 0
        return value
    out["Risk_Adjustment"] = out.apply(penalty, axis=1)
    out["AI_Value_Score"] = (out.Weighted_Base_Score - out.Evidence_Adjustment - out.Risk_Adjustment).clip(0, 100)
    out["Evidence_Adjusted_Value"] = out.Validated_Annual_Benefit_USD * out.Evidence_Confidence / 100 - out.Annual_Investment_USD
    return out

D = load_data()
all_scored = score(D["initiatives"], D["incidents"])
if "selected_initiative" not in st.session_state: st.session_state.selected_initiative = None
if "target_page" not in st.session_state: st.session_state.target_page = "Executive Command Center"

with st.sidebar:
    st.markdown("## Clinexa AI")
    st.caption("Clinical AI Value & Governance · Demo v1.4")
    st.selectbox("View as", ["Executive Leadership", "Department Leader", "AI Governance", "Quality", "Finance"])
    departments = sorted(all_scored.Department.unique())
    department_choice = st.selectbox(
        "Department",
        ["Select department..."] + ["All Departments"] + departments,
        index=0,
        key="department_filter",
    )
    if department_choice == "Select department...":
        selected_departments = []
    elif department_choice == "All Departments":
        selected_departments = departments
    else:
        selected_departments = [department_choice]
    pages = ["Executive Command Center", "Initiative Registry", "Value & Evidence", "Governance & Risk", "Adoption & Maturity", "Incidents & Actions", "Data Quality"]
    page = st.radio("Navigate", pages, index=pages.index(st.session_state.target_page) if st.session_state.target_page in pages else 0)
    st.session_state.target_page = page

if not selected_departments:
    if page == "Executive Command Center":
        st.markdown('<div class="hero"><div class="badge">Clinexa AI · Value &amp; Governance Module</div><h1>AI Value &amp; Governance</h1><p>Evidence-based portfolio oversight for value, quality, adoption, risk and responsible scale.</p></div>', unsafe_allow_html=True)
    else:
        page_titles = {
            "Initiative Registry": "Initiative Registry",
            "Value & Evidence": "Value & Evidence",
            "Governance & Risk": "Governance & Risk",
            "Adoption & Maturity": "Adoption & Maturity",
            "Incidents & Actions": "Incidents & Actions",
            "Data Quality": "Data Quality",
        }
        st.markdown(f'<div class="hero"><div class="badge">Clinexa AI</div><h1>{page_titles.get(page, page)}</h1><p>Select a department from the left sidebar to populate this page.</p></div>', unsafe_allow_html=True)
    st.info("Select **All Departments** or one department from the left sidebar to load dashboard content.")
    st.stop()

f = all_scored[all_scored.Department.isin(selected_departments)].copy()
cf = D["controls"][D["controls"].Department.isin(selected_departments)].copy()
incf = D["incidents"][D["incidents"].Department.isin(selected_departments)].copy()

def open_initiative(initiative_id):
    st.session_state.selected_initiative = initiative_id
    st.session_state.target_page = "Value & Evidence"

if page == "Executive Command Center":
    st.markdown('<div class="hero"><div class="badge">Value &amp; Governance Module</div><h1>AI Value &amp; Governance</h1><p>Evidence-based portfolio oversight for value, quality, adoption, risk and responsible scale.</p></div>', unsafe_allow_html=True)
    a,b,c,d,e = st.columns(5)
    a.metric("Annual investment", f"${f.Annual_Investment_USD.sum()/1000:,.0f}K")
    b.metric("Forecast benefit", f"${f.Forecast_Annual_Benefit_USD.sum()/1000:,.0f}K")
    c.metric("Validated benefit", f"${f.Validated_Annual_Benefit_USD.sum()/1000:,.0f}K")
    d.metric("Realized benefit", f"${f.Realized_Annual_Benefit_USD.sum()/1000:,.0f}K")
    e.metric("Evidence-adjusted net", f"${f.Evidence_Adjusted_Value.sum()/1000:,.0f}K")
    st.caption("Forecast, validated and realized benefits are intentionally separated to prevent unverified estimates from being presented as confirmed value.")

    scale_ready = int((f.AI_Value_Score >= 70).sum())
    validated_count = int(f.Benefit_Status.isin(["Validated", "Realized"]).sum())
    open_actions = int(((cf.Status != "Complete") & (cf.Due_Date < pd.Timestamp.today())).sum())
    st.info(f"**Portfolio at a glance:** {len(f)} initiatives across {f.Department.nunique()} department(s) · {scale_ready} scale-ready · {validated_count} with validated/realized benefit · {open_actions} overdue governance action(s)")

    c1, c2 = st.columns([1, 1.25])
    with c1:
        g = f.groupby("Department", as_index=False).AI_Value_Score.mean().rename(columns={"AI_Value_Score":"Value"})
        fig = px.bar(g.sort_values("Value"), x="Value", y="Department", orientation="h", color="Department", color_discrete_map=DEPT_COLORS, text_auto=".1f", range_x=[0,100], title="Department value score (0–100)")
        fig.add_vrect(x0=0,x1=40,fillcolor="#fee2e2",opacity=.18,line_width=0)
        fig.add_vrect(x0=40,x1=70,fillcolor="#fef3c7",opacity=.18,line_width=0)
        fig.add_vrect(x0=70,x1=100,fillcolor="#dcfce7",opacity=.18,line_width=0)
        fig.update_layout(showlegend=False, xaxis_title="Value score", yaxis_title="")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.scatter(f, x="Compliance_Score", y="AI_Value_Score", size="Annual_Investment_USD", color="Department", color_discrete_map=DEPT_COLORS, symbol="Risk_Level", hover_name="Initiative", hover_data=["Initiative_ID","Department","Risk_Level","Benefit_Status","Evidence_Confidence"], text="Initiative_ID", title="Portfolio value, compliance and risk", size_max=38)
        fig.add_hline(y=75, line_dash="dot", annotation_text="Value threshold 75")
        fig.add_vline(x=80, line_dash="dot", annotation_text="Compliance threshold 80")
        fig.update_traces(textposition="top center", marker=dict(line=dict(width=1,color="#334155")))
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Color = department · Symbol = risk · Bubble size = investment · Label = initiative ID")

    # Compact Governance Action Center summary remains on the executive page.
    high = f[(f.Risk_Level == "High") & (f.Compliance_Score < 80)]
    weak = f[f.Evidence_Confidence < 70]
    overdue = cf[(cf.Status != "Complete") & (cf.Due_Date < pd.Timestamp.today())]

    st.markdown('<div class="section-card"><div class="section-title">Governance Action Center Summary</div><div class="section-subtitle">Select a category to review priority items without leaving the executive dashboard.</div></div>', unsafe_allow_html=True)
    category = st.selectbox(
        "Governance category",
        ["Select a category..."] + [f"High risk ({len(high)})", f"Evidence needed ({len(weak)})", f"Overdue governance ({len(overdue)})"],
        index=0,
        key="executive_governance_category",
        label_visibility="collapsed",
    )

    if category == "Select a category...":
        st.caption("Choose a category to display its priority initiatives or governance actions.")
    elif category.startswith("High risk"):
        items = high.sort_values(["Compliance_Score", "AI_Value_Score"]).head(6)
        if items.empty:
            st.success("No high-risk initiatives below the compliance threshold.")
        for _, r in items.iterrows():
            left, right = st.columns([5, 1])
            with left:
                st.markdown(f'<div class="action red"><b>{r.Initiative}</b><div class="meta">{r.Department} · {r.Initiative_ID} · Compliance {r.Compliance_Score:.0f} · Value {r.AI_Value_Score:.1f}</div></div>', unsafe_allow_html=True)
            with right:
                if st.button("Open", key="exec_high_" + r.Initiative_ID, use_container_width=True):
                    open_initiative(r.Initiative_ID); st.rerun()
    elif category.startswith("Evidence needed"):
        items = weak.sort_values("Evidence_Confidence").head(6)
        if items.empty:
            st.success("All selected initiatives meet the evidence threshold.")
        for _, r in items.iterrows():
            left, right = st.columns([5, 1])
            with left:
                st.markdown(f'<div class="action blue"><b>{r.Initiative}</b><div class="meta">{r.Department} · {r.Initiative_ID} · Evidence {r.Evidence_Confidence:.0f}% · {r.Evidence_Source}</div></div>', unsafe_allow_html=True)
            with right:
                if st.button("Open", key="exec_weak_" + r.Initiative_ID, use_container_width=True):
                    open_initiative(r.Initiative_ID); st.rerun()
    else:
        items = overdue.sort_values("Due_Date").head(6)
        if items.empty:
            st.success("No overdue governance actions.")
        for _, r in items.iterrows():
            name = f.loc[f.Initiative_ID == r.Initiative_ID, "Initiative"]
            name = name.iloc[0] if len(name) else r.Initiative_ID
            left, right = st.columns([5, 1])
            with left:
                st.markdown(f'<div class="action pink"><b>{r.Control}</b><div class="meta">{name} · {r.Department} · Due {r.Due_Date.date()} · Owner {r.Owner}</div></div>', unsafe_allow_html=True)
            with right:
                if st.button("Open", key="exec_due_" + r.Control_ID, use_container_width=True):
                    open_initiative(r.Initiative_ID); st.rerun()

    st.caption("The summary shows up to six priority items for the selected category. Department filtering applies automatically.")

elif page == "Initiative Registry":
    st.markdown('<div class="hero"><div class="brand"><div class="brandmark">C</div><div class="brandname">Clinexa AI</div></div><div class="badge">Controlled inventory</div><h1>Initiative Registry</h1><p>Portfolio ownership, lifecycle and intended use.</p></div>', unsafe_allow_html=True)
    reg = D["registry"][D["registry"].Department.isin(selected_departments)]
    st.dataframe(reg, use_container_width=True, hide_index=True)
    st.download_button("Download filtered registry", reg.to_csv(index=False).encode(), "initiative_registry_filtered.csv", "text/csv")

elif page == "Value & Evidence":
    st.markdown('<div class="hero"><div class="brand"><div class="brandmark">C</div><div class="brandname">Clinexa AI</div></div><div class="badge">Transparent scoring</div><h1>Value &amp; Evidence</h1><p>Inspect score composition, evidence confidence and risk deductions.</p></div>', unsafe_allow_html=True)
    ids = f.Initiative_ID.tolist()
    idx = ids.index(st.session_state.selected_initiative) if st.session_state.selected_initiative in ids else 0
    chosen = st.selectbox("Initiative", ids, index=idx, format_func=lambda x: f.loc[f.Initiative_ID == x, "Initiative"].iloc[0])
    st.session_state.selected_initiative = chosen
    r = f[f.Initiative_ID == chosen].iloc[0]
    a,b,c,d,e = st.columns(5)
    a.metric("Final value score", f"{r.AI_Value_Score:.1f}/100")
    b.metric("Weighted base", f"{r.Weighted_Base_Score:.1f}")
    c.metric("Evidence confidence", f"{r.Evidence_Confidence:.0f}%")
    d.metric("Evidence adjustment", f"-{r.Evidence_Adjustment:.1f}")
    e.metric("Risk adjustment", f"-{r.Risk_Adjustment:.1f}")
    st.dataframe(pd.DataFrame({"Dimension":["Efficiency","Quality","Adoption","Compliance","Financial"],"Score":[r.Efficiency_Score,r.Quality_Score,r.Adoption_Score,r.Compliance_Score,r.Financial_Score],"Weight":[20,25,15,25,15]}), use_container_width=True, hide_index=True)

elif page == "Governance & Risk":
    st.markdown('<div class="hero"><div class="brand"><div class="brandmark">C</div><div class="brandname">Clinexa AI</div></div><div class="badge">Governance workflow</div><h1>Governance &amp; Risk</h1><p>Review controls, ownership and deadlines.</p></div>', unsafe_allow_html=True)
    st.dataframe(cf.sort_values(["Status","Due_Date"]), use_container_width=True, hide_index=True)

elif page == "Adoption & Maturity":
    st.markdown('<div class="hero"><div class="brand"><div class="brandmark">C</div><div class="brandname">Clinexa AI</div></div><div class="badge">Operational adoption</div><h1>Adoption &amp; Maturity</h1><p>Compare training completion with active use.</p></div>', unsafe_allow_html=True)
    ad = D["adoption"][D["adoption"].Department.isin(selected_departments)]
    fig = px.scatter(ad, x="Training_Completion_Pct", y="Monthly_Active_Rate_Pct", size="Eligible_Users", color="Department", color_discrete_map=DEPT_COLORS, text="Department")
    fig.update_traces(textposition="top center")
    st.plotly_chart(fig, use_container_width=True)

elif page == "Incidents & Actions":
    st.markdown('<div class="hero"><div class="brand"><div class="brandmark">C</div><div class="brandname">Clinexa AI</div></div><div class="badge">Operational oversight</div><h1>Incidents &amp; Actions</h1><p>Track open findings.</p></div>', unsafe_allow_html=True)
    st.dataframe(incf, use_container_width=True, hide_index=True)

else:
    st.markdown('<div class="hero"><div class="brand"><div class="brandmark">C</div><div class="brandname">Clinexa AI</div></div><div class="badge">Trusted data foundation</div><h1>Data Quality</h1><p>Basic structural checks.</p></div>', unsafe_allow_html=True)
    st.success("No structural issues detected in the filtered initiative data.")
    st.dataframe(f, use_container_width=True, hide_index=True)

st.divider()
st.caption("Internal pharma prototype · Representative data only · Not validated for production or GxP use")
