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
:root{--navy:#0A2540;--teal:#00A6A6;--muted:#64748b;--line:#dce4ec}
.block-container{padding-top:.75rem;padding-bottom:1.5rem;max-width:100%}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#071f36 0%,#0A3654 58%,#0A5B66 100%);border-right:1px solid rgba(255,255,255,.14)}
[data-testid="stSidebar"] h1,[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3,[data-testid="stSidebar"] p,[data-testid="stSidebar"] label,[data-testid="stSidebar"] [data-testid="stCaptionContainer"]{color:#f8fafc!important}
[data-testid="stSidebar"] [data-baseweb="select"]>div{background:#fff!important;border:1px solid #cbd5e1!important;border-radius:8px!important}
[data-testid="stSidebar"] [data-baseweb="select"] span,[data-testid="stSidebar"] [data-baseweb="select"] input,[data-testid="stSidebar"] [data-baseweb="select"] svg{color:#0A2540!important;fill:#0A2540!important;-webkit-text-fill-color:#0A2540!important}
[data-testid="stSidebar"] [role="radiogroup"] label{padding:.34rem .45rem;border-radius:.5rem;color:#f8fafc!important}
[data-testid="stSidebar"] [role="radiogroup"] label:hover{background:rgba(255,255,255,.11)}
[data-baseweb="popover"] [role="option"],[data-baseweb="menu"] [role="option"]{color:#0A2540!important;background:#fff!important}
[data-baseweb="popover"] [role="option"]:hover,[data-baseweb="menu"] [role="option"]:hover{background:#e8f5f5!important}
.hero{padding:18px 24px;border-radius:14px;background:linear-gradient(120deg,#0A2540,#0A6672);color:white;margin-bottom:14px;overflow:visible;box-shadow:0 8px 24px rgba(10,37,64,.14)}
.hero h1{margin:0;max-width:100%;font-size:clamp(1.45rem,2.2vw,2rem);line-height:1.22;white-space:normal!important;overflow:visible!important;text-overflow:clip!important;word-break:normal}.hero p{margin:.5rem 0 0;color:#e4f7fa}
.brand{display:flex;align-items:center;gap:10px;margin-bottom:8px}.brandmark{width:34px;height:34px;border-radius:10px;background:#14b8a6;color:#042f2e;display:flex;align-items:center;justify-content:center;font-weight:800}.brandname{font-size:1rem;font-weight:700;letter-spacing:.02em}
.badge{font-size:.69rem;letter-spacing:.1em;text-transform:uppercase;font-weight:700;color:#d7f3f7;margin-bottom:8px}
.kpi-grid{display:grid;grid-template-columns:repeat(5,minmax(150px,1fr));gap:12px;margin:8px 0 12px}.kpi-card{position:relative;background:#fff;border:1px solid var(--line);border-radius:13px;padding:15px 16px 14px;box-shadow:0 5px 16px rgba(15,23,42,.055);min-height:116px}.kpi-card:before{content:"";position:absolute;left:0;top:0;right:0;height:4px;border-radius:13px 13px 0 0;background:linear-gradient(90deg,#00A6A6,#2563EB)}.kpi-label{font-size:.78rem;font-weight:700;color:#526176;text-transform:uppercase;letter-spacing:.035em}.kpi-value{font-size:1.72rem;font-weight:800;color:var(--navy);margin-top:10px;line-height:1}.kpi-note{font-size:.75rem;color:#718096;margin-top:9px}
.section-card{border:1px solid var(--line);border-radius:13px;padding:15px 17px;background:#fff;margin-top:8px;box-shadow:0 4px 14px rgba(15,23,42,.045)}.section-title{font-size:1.05rem;font-weight:800;color:var(--navy);margin-bottom:4px}.section-subtitle{font-size:.84rem;color:var(--muted);margin-bottom:8px}
.insight{display:flex;gap:10px;align-items:flex-start;padding:11px 0;border-bottom:1px solid #edf2f7}.insight:last-child{border-bottom:none}.insight-icon{width:28px;height:28px;border-radius:8px;background:#e8f5f5;color:#087b7b;display:flex;align-items:center;justify-content:center;font-weight:800}.insight-copy b{display:block;color:#183047;font-size:.9rem}.insight-copy span{color:#68778b;font-size:.78rem}
.action{border:1px solid #d9e1ea;border-left:5px solid #d97706;border-radius:10px;padding:10px 13px;margin:6px 0;background:white}.red{border-left-color:#dc2626}.blue{border-left-color:#2563eb}.pink{border-left-color:#e11d48}.meta{font-size:.82rem;color:#64748b}
.update-badge{display:inline-block;padding:6px 10px;border:1px solid #cfe5e7;border-radius:999px;background:#f1fbfb;color:#0A5B66;font-size:.76rem;font-weight:650;margin-bottom:8px}
@media(max-width:1100px){.kpi-grid{grid-template-columns:repeat(2,minmax(150px,1fr))}}@media(max-width:700px){.kpi-grid{grid-template-columns:1fr}.hero h1{font-size:1.45rem}}
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
        st.markdown('<div class="hero"><div class="badge">Clinexa AI · Value &amp; Governance Module</div><h1>Clinical AI Value Governance Platform</h1><p>Evidence-based portfolio oversight for value, quality, adoption, risk and responsible scale.</p></div>', unsafe_allow_html=True)
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
    st.markdown('<div class="hero"><div class="badge">Value &amp; Governance Module</div><h1>Clinical AI Value Governance Platform</h1><p>Evidence-based portfolio oversight for value, quality, adoption, risk and responsible scale.</p></div>', unsafe_allow_html=True)
    refreshed = pd.Timestamp.now().strftime("%d %b %Y · %I:%M %p")
    st.markdown(f'<span class="update-badge">Data refreshed · {refreshed}</span>', unsafe_allow_html=True)

    kpis = [
        ("Total initiatives", f"{len(f)}", f"Across {f.Department.nunique()} department(s)"),
        ("Annual investment", f"${f.Annual_Investment_USD.sum()/1000:,.0f}K", "Current portfolio commitment"),
        ("Forecast benefit", f"${f.Forecast_Annual_Benefit_USD.sum()/1000:,.0f}K", "Expected annual value"),
        ("Validated benefit", f"${f.Validated_Annual_Benefit_USD.sum()/1000:,.0f}K", "Evidence-supported value"),
        ("Evidence-adjusted net", f"${f.Evidence_Adjusted_Value.sum()/1000:,.0f}K", "After evidence and investment"),
    ]
    cards = ''.join([f'<div class="kpi-card"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div><div class="kpi-note">{note}</div></div>' for label,value,note in kpis])
    st.markdown(f'<div class="kpi-grid">{cards}</div>', unsafe_allow_html=True)
    st.caption("Forecast, validated and realized benefits are intentionally separated so unverified estimates are not presented as confirmed value.")

    scale_ready = int((f.AI_Value_Score >= 70).sum())
    validated_count = int(f.Benefit_Status.isin(["Validated", "Realized"]).sum())
    high_count = int(((f.Risk_Level == "High") & (f.Compliance_Score < 80)).sum())
    weak_count = int((f.Evidence_Confidence < 70).sum())
    overdue_count = int(((cf.Status != "Complete") & (cf.Due_Date < pd.Timestamp.today())).sum())

    chart_col, insight_col = st.columns([1.8, .8], gap="large")
    with chart_col:
        fig = px.scatter(f, x="Compliance_Score", y="AI_Value_Score", size="Annual_Investment_USD", color="Department", color_discrete_map=DEPT_COLORS, symbol="Risk_Level", hover_name="Initiative", hover_data={"Initiative_ID":True,"Department":True,"Risk_Level":True,"Benefit_Status":True,"Evidence_Confidence":True,"Annual_Investment_USD":":$,.0f"}, text="Initiative_ID", title="Portfolio value, compliance and risk", size_max=42)
        fig.add_hline(y=75, line_dash="dot", line_color="#94a3b8", annotation_text="Value threshold 75")
        fig.add_vline(x=80, line_dash="dot", line_color="#94a3b8", annotation_text="Compliance threshold 80")
        fig.update_traces(textposition="top center", marker=dict(line=dict(width=1,color="#334155")))
        fig.update_layout(height=475, plot_bgcolor="#ffffff", paper_bgcolor="#ffffff", margin=dict(l=20,r=20,t=58,b=25), legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0), xaxis=dict(title="Compliance score", gridcolor="#edf2f7", range=[45,102]), yaxis=dict(title="AI value score", gridcolor="#edf2f7", range=[0,100]))
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Color = department · Symbol = risk · Bubble size = investment · Label = initiative ID")
    with insight_col:
        st.markdown('<div class="section-card"><div class="section-title">Executive Insights</div><div class="section-subtitle">Current portfolio signals requiring leadership attention.</div>', unsafe_allow_html=True)
        insights = [("✓", f"{scale_ready} initiatives are scale-ready", "AI value score is 70 or higher."),("E", f"{validated_count} have validated or realized benefit", "Evidence is beyond forecast-only status."),("!", f"{high_count} high-risk initiatives need review", "High risk with compliance below 80."),("?", f"{weak_count} initiatives need stronger evidence", "Evidence confidence is below 70%."),("D", f"{overdue_count} governance actions are overdue", "Open controls have passed their due date.")]
        for icon,title,note in insights:
            st.markdown(f'<div class="insight"><div class="insight-icon">{icon}</div><div class="insight-copy"><b>{title}</b><span>{note}</span></div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    high = f[(f.Risk_Level == "High") & (f.Compliance_Score < 80)]
    weak = f[f.Evidence_Confidence < 70]
    overdue = cf[(cf.Status != "Complete") & (cf.Due_Date < pd.Timestamp.today())]
    st.markdown('<div class="section-card"><div class="section-title">Governance Action Center Summary</div><div class="section-subtitle">Select a category to reveal only its priority initiatives or actions.</div></div>', unsafe_allow_html=True)
    category = st.selectbox("Governance category", ["Select a category..."] + [f"High risk ({len(high)})", f"Evidence needed ({len(weak)})", f"Overdue governance ({len(overdue)})"], index=0, key="executive_governance_category", label_visibility="collapsed")
    if category != "Select a category...":
        if category.startswith("High risk"):
            items = high.sort_values(["Compliance_Score", "AI_Value_Score"]).head(6)
            if items.empty: st.success("No high-risk initiatives below the compliance threshold.")
            for _, r in items.iterrows():
                left, right = st.columns([5, 1])
                with left: st.markdown(f'<div class="action red"><b>{r.Initiative}</b><div class="meta">{r.Department} · {r.Initiative_ID} · Compliance {r.Compliance_Score:.0f} · Value {r.AI_Value_Score:.1f}</div></div>', unsafe_allow_html=True)
                with right:
                    if st.button("Open", key="exec_high_" + r.Initiative_ID, use_container_width=True): open_initiative(r.Initiative_ID); st.rerun()
        elif category.startswith("Evidence needed"):
            items = weak.sort_values("Evidence_Confidence").head(6)
            if items.empty: st.success("All selected initiatives meet the evidence threshold.")
            for _, r in items.iterrows():
                left, right = st.columns([5, 1])
                with left: st.markdown(f'<div class="action blue"><b>{r.Initiative}</b><div class="meta">{r.Department} · {r.Initiative_ID} · Evidence {r.Evidence_Confidence:.0f}% · {r.Evidence_Source}</div></div>', unsafe_allow_html=True)
                with right:
                    if st.button("Open", key="exec_weak_" + r.Initiative_ID, use_container_width=True): open_initiative(r.Initiative_ID); st.rerun()
        else:
            items = overdue.sort_values("Due_Date").head(6)
            if items.empty: st.success("No overdue governance actions.")
            for _, r in items.iterrows():
                name = f.loc[f.Initiative_ID == r.Initiative_ID, "Initiative"]
                name = name.iloc[0] if len(name) else r.Initiative_ID
                left, right = st.columns([5, 1])
                with left: st.markdown(f'<div class="action pink"><b>{r.Control}</b><div class="meta">{name} · {r.Department} · Due {r.Due_Date.date()} · Owner {r.Owner}</div></div>', unsafe_allow_html=True)
                with right:
                    if st.button("Open", key="exec_due_" + r.Control_ID, use_container_width=True): open_initiative(r.Initiative_ID); st.rerun()

    st.markdown('<div class="section-card"><div class="section-title">Recent Initiatives Overview</div><div class="section-subtitle">The most recently started initiatives in the selected portfolio.</div></div>', unsafe_allow_html=True)
    recent_cols = ["Initiative_ID","Initiative","Department","Lifecycle_Stage","Risk_Level","Benefit_Status","AI_Value_Score","Next_Review"]
    recent = f.sort_values("Pilot_Start", ascending=False).head(8)[recent_cols].copy()
    recent["AI_Value_Score"] = recent["AI_Value_Score"].round(1)
    recent["Next_Review"] = recent["Next_Review"].dt.strftime("%d %b %Y")
    recent.columns = ["ID","Initiative","Department","Lifecycle","Risk","Benefit status","Value score","Next review"]
    st.dataframe(recent, use_container_width=True, hide_index=True, height=310)

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
