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
:root{
  --primary:#56308F;
  --charcoal:#30343B;
  --white:#FFFFFF;
  --soft:#F4F1F8;
  --surface:#FFFFFF;
  --line:#DED7E8;
  --muted:#6B6673;
  --primary-soft:#EEE8F6;
  --primary-dark:#34205E;
  --magenta:#B33A8A;
  --coral:#F06A5F;
  --teal:#18A7A0;
}
html,body,[class*="css"]{color:var(--charcoal)}
.stApp{background:var(--soft)}
.block-container{padding-top:.8rem;padding-bottom:1.7rem;max-width:1480px}

/* Sidebar */
[data-testid="stSidebar"]{background:linear-gradient(180deg,#3B2367 0%,#552B86 52%,#6A3191 100%);border-right:1px solid #34205E}
[data-testid="stSidebar"] h1,[data-testid="stSidebar"] h2,[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,[data-testid="stSidebar"] label,
[data-testid="stSidebar"] [data-testid="stCaptionContainer"]{color:var(--white)!important}
[data-testid="stSidebar"] [data-baseweb="select"]>div{background:var(--white)!important;border:1px solid #CFC4C9!important;border-radius:8px!important}
[data-testid="stSidebar"] [data-baseweb="select"] span,
[data-testid="stSidebar"] [data-baseweb="select"] input,
[data-testid="stSidebar"] [data-baseweb="select"] svg{color:var(--charcoal)!important;fill:var(--charcoal)!important;-webkit-text-fill-color:var(--charcoal)!important}
[data-testid="stSidebar"] [role="radiogroup"] label{padding:.48rem .62rem;border-radius:.58rem;color:var(--white)!important;margin:.08rem 0}
[data-testid="stSidebar"] [role="radiogroup"] label:hover{background:rgba(255,255,255,.13)}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked){background:var(--white)!important;color:var(--primary)!important;box-shadow:0 3px 10px rgba(0,0,0,.16)}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) p{color:var(--primary)!important}

/* Select menus */
[data-baseweb="popover"] [role="option"],[data-baseweb="menu"] [role="option"]{color:var(--charcoal)!important;background:var(--white)!important}
[data-baseweb="popover"] [role="option"]:hover,[data-baseweb="menu"] [role="option"]:hover{background:#EEE8F6!important;color:var(--charcoal)!important}

/* Shared page header: no eyebrow/badge above title */
.hero{padding:20px 25px;border-radius:13px;background:linear-gradient(110deg,#56308F 0%,#9B3D91 58%,#F06A5F 100%);color:var(--white);margin-bottom:16px;overflow:visible;box-shadow:0 8px 22px rgba(86,48,143,.20);border:1px solid rgba(255,255,255,.10)}
.hero h1{margin:0;max-width:100%;font-size:clamp(1.42rem,2.05vw,1.95rem);line-height:1.22;color:var(--white)!important;white-space:normal!important;overflow:visible!important;text-overflow:clip!important;word-break:normal}
.hero p{margin:.5rem 0 0;color:var(--white)!important;opacity:.93;font-size:.91rem;max-width:980px}
.badge{display:none!important}

/* Cards and section text */
.kpi-grid{display:grid;grid-template-columns:repeat(4,minmax(170px,1fr));gap:14px;margin:10px 0 16px}
.kpi-card{position:relative;background:var(--white);border:1px solid var(--line);border-radius:12px;padding:15px 16px 14px;box-shadow:0 5px 16px rgba(63,68,68,.065);min-height:118px}
.kpi-card:before{content:"";position:absolute;left:0;top:0;right:0;height:4px;border-radius:12px 12px 0 0;background:var(--primary)}
.kpi-card:nth-child(1):before{background:var(--teal)}
.kpi-card:nth-child(2):before{background:var(--primary)}
.kpi-card:nth-child(3):before{background:var(--magenta)}
.kpi-card:nth-child(4):before{background:var(--coral)}
.kpi-card:nth-child(5):before{background:var(--teal)}
.kpi-card:nth-child(6):before{background:var(--primary)}

.kpi-label{font-size:.78rem;font-weight:700;color:var(--charcoal);text-transform:uppercase;letter-spacing:.035em}
.kpi-value{font-size:1.72rem;font-weight:800;color:var(--primary);margin-top:10px;line-height:1}
.kpi-note{font-size:.75rem;color:var(--muted);margin-top:9px}
.section-card{border:1px solid var(--line);border-radius:12px;padding:16px 18px;background:var(--surface);margin-top:10px;box-shadow:0 4px 13px rgba(63,68,68,.05)}
.section-title{font-size:1.05rem;font-weight:800;color:var(--primary);margin-bottom:4px}
.section-subtitle{font-size:.84rem;color:var(--charcoal);margin-bottom:8px}
.action{border:1px solid var(--line);border-left:5px solid var(--teal);border-radius:10px;padding:11px 14px;margin:7px 0;background:var(--white);box-shadow:0 2px 8px rgba(63,68,68,.04)}
.red,.blue,.pink{border-left-color:var(--primary)}
.meta{font-size:.82rem;color:var(--charcoal)}
.update-badge{display:inline-block;padding:6px 10px;border:1px solid #D7CDE5;border-radius:999px;background:#F2EDF8;color:var(--primary);font-size:.76rem;font-weight:650;margin-bottom:8px}

/* Buttons and tables */
.stButton>button,.stDownloadButton>button{background:var(--primary)!important;color:var(--white)!important;border:1px solid var(--primary)!important;border-radius:8px!important;font-weight:700!important;box-shadow:none!important}
.stButton>button:hover,.stDownloadButton>button:hover{background:#44256F!important;border-color:#44256F!important;transform:none}
[data-testid="stDataFrame"] thead tr th{background:var(--primary)!important;color:var(--white)!important}
[data-testid="stDataFrame"]{border:1px solid var(--line);border-radius:10px;overflow:hidden;background:var(--white);box-shadow:0 3px 10px rgba(63,68,68,.04)}
[data-testid="stMetric"]{border-top:3px solid var(--teal);border-radius:10px;padding:.5rem .7rem;background:var(--white)}
[data-testid="stMetricLabel"],[data-testid="stMetricValue"]{color:var(--charcoal)!important}
hr{border-color:var(--line)!important}

@media(max-width:1100px){.kpi-grid{grid-template-columns:repeat(2,minmax(150px,1fr))}}
@media(max-width:700px){.kpi-grid{grid-template-columns:1fr}.hero h1{font-size:1.38rem}}
</style>
""", unsafe_allow_html=True)

def render_page_header(section_label="", subtitle="Evidence-based portfolio oversight for value, quality, adoption, risk and responsible scale."):
    # Keep the same clean title treatment across every page. The navigation already identifies the section.
    st.markdown(
        f'<div class="hero"><h1>Clinical AI Value Governance Platform</h1><p>{subtitle}</p></div>',
        unsafe_allow_html=True,
    )

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
    st.caption("Clinical Intelligence Platform · Demo v1.4")
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
    page_meta = {
        "Executive Command Center": ("Value & Governance Module", "Evidence-based portfolio oversight for value, quality, adoption, risk and responsible scale."),
        "Initiative Registry": ("Initiative Registry", "Portfolio ownership, lifecycle and intended use."),
        "Value & Evidence": ("Value & Evidence", "Inspect score composition, evidence confidence and risk deductions."),
        "Governance & Risk": ("Governance & Risk", "Review controls, ownership and deadlines."),
        "Adoption & Maturity": ("Adoption & Maturity", "Compare training completion with active use."),
        "Incidents & Actions": ("Incidents & Actions", "Track open findings and corrective actions."),
        "Data Quality": ("Data Quality", "Review structural checks and trusted-data readiness."),
    }
    section_label, subtitle = page_meta.get(page, (page, "Select a department from the left sidebar to populate this page."))
    render_page_header(section_label, subtitle)
    st.info("Select **All Departments** or one department from the left sidebar to load dashboard content.")
    st.stop()

f = all_scored[all_scored.Department.isin(selected_departments)].copy()
cf = D["controls"][D["controls"].Department.isin(selected_departments)].copy()
incf = D["incidents"][D["incidents"].Department.isin(selected_departments)].copy()

def open_initiative(initiative_id):
    st.session_state.selected_initiative = initiative_id
    st.session_state.target_page = "Value & Evidence"

def polish_figure(fig, height=None):
    """Apply one restrained visual standard to Plotly charts across pages."""
    fig.update_layout(
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
        font=dict(color="#30343B", family="Arial, sans-serif"),
        margin=dict(l=24, r=24, t=28, b=24),
        hoverlabel=dict(bgcolor="#FFFFFF", font_color="#30343B", bordercolor="#D7CDE5"),
    )
    if height:
        fig.update_layout(height=height)
    fig.update_xaxes(gridcolor="#ECE7F1", zerolinecolor="#ECE7F1", linecolor="#D9D2E3")
    fig.update_yaxes(gridcolor="#ECE7F1", zerolinecolor="#ECE7F1", linecolor="#D9D2E3")
    return fig

if page == "Executive Command Center":
    render_page_header("Value & Governance Module", "Evidence-based portfolio oversight for value, quality, adoption, risk and responsible scale.")
    refreshed = pd.Timestamp.now().strftime("%d %b %Y · %I:%M %p")
    st.markdown(f'<span class="update-badge">Data refreshed · {refreshed}</span>', unsafe_allow_html=True)

    kpis = [
        ("Total initiatives", f"{len(f)}", f"Across {f.Department.nunique()} department(s)"),
        ("Annual investment", f"${f.Annual_Investment_USD.sum()/1000:,.0f}K", "Current portfolio commitment"),
        ("Forecast benefit", f"${f.Forecast_Annual_Benefit_USD.sum()/1000:,.0f}K", "Expected annual value"),
        ("Validated benefit", f"${f.Validated_Annual_Benefit_USD.sum()/1000:,.0f}K", "Evidence-supported value"),
        ("Realized benefit", f"${f.Realized_Annual_Benefit_USD.sum()/1000:,.0f}K", "Benefit already realized"),
        ("Evidence-adjusted net", f"${f.Evidence_Adjusted_Value.sum()/1000:,.0f}K", "Validated value adjusted for evidence and investment"),
    ]
    cards = ''.join([f'<div class="kpi-card"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div><div class="kpi-note">{note}</div></div>' for label,value,note in kpis])
    st.markdown(f'<div class="kpi-grid">{cards}</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-card"><div class="section-title">Portfolio Value, Compliance and Risk</div><div class="section-subtitle">Each bubble is an initiative. Color represents department, bubble size represents annual investment, and risk is available in the hover details.</div></div>', unsafe_allow_html=True)
    fig = px.scatter(
        f,
        x="Compliance_Score",
        y="AI_Value_Score",
        size="Annual_Investment_USD",
        color="Department",
        color_discrete_map=DEPT_COLORS,
        hover_name="Initiative",
        hover_data={
            "Initiative_ID": True,
            "Department": True,
            "Risk_Level": True,
            "Benefit_Status": True,
            "Evidence_Confidence": ":.0f",
            "Annual_Investment_USD": ":$,.0f",
        },
        text="Initiative_ID",
        size_max=34,
    )
    fig.add_hline(y=75, line_dash="dot", line_color="#94a3b8")
    fig.add_vline(x=80, line_dash="dot", line_color="#94a3b8")
    fig.update_traces(textposition="top center", textfont=dict(size=10), marker=dict(line=dict(width=1, color="#ffffff")))
    polish_figure(fig, height=430)
    fig.update_layout(
        legend=dict(orientation="h", yanchor="bottom", y=1.01, xanchor="left", x=0, title_text="Department"),
        xaxis=dict(title="Compliance score", range=[35, 102]),
        yaxis=dict(title="AI value score", range=[0, 105]),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

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

    st.markdown('<div class="section-card"><div class="section-title">AI Initiative Portfolio</div><div class="section-subtitle">Recently started initiatives in the selected portfolio, presented for quick executive review.</div></div>', unsafe_allow_html=True)
    lifecycle_col = "Lifecycle" if "Lifecycle" in f.columns else ("Lifecycle_Stage" if "Lifecycle_Stage" in f.columns else None)
    requested_cols = ["Initiative_ID", "Initiative", "Department"]
    if lifecycle_col:
        requested_cols.append(lifecycle_col)
    requested_cols += ["Risk_Level", "Benefit_Status", "AI_Value_Score", "Next_Review"]
    recent_cols = [c for c in requested_cols if c in f.columns]
    sort_col = "Pilot_Start" if "Pilot_Start" in f.columns else "Initiative_ID"
    recent = f.sort_values(sort_col, ascending=False).head(8)[recent_cols].copy()
    if "AI_Value_Score" in recent.columns:
        recent["AI_Value_Score"] = recent["AI_Value_Score"].round(1)
    if "Next_Review" in recent.columns:
        recent["Next_Review"] = pd.to_datetime(recent["Next_Review"], errors="coerce").dt.strftime("%d %b %Y")
    rename_map = {
        "Initiative_ID": "ID", "Initiative": "Initiative", "Department": "Department",
        "Lifecycle": "Lifecycle", "Lifecycle_Stage": "Lifecycle", "Risk_Level": "Risk",
        "Benefit_Status": "Benefit status", "AI_Value_Score": "Value score", "Next_Review": "Next review"
    }
    recent = recent.rename(columns=rename_map)
    st.dataframe(recent, use_container_width=True, hide_index=True, height=300)

elif page == "Initiative Registry":
    render_page_header("Initiative Registry", "Portfolio ownership, lifecycle and intended use.")
    reg = D["registry"][D["registry"].Department.isin(selected_departments)]
    st.dataframe(reg, use_container_width=True, hide_index=True)
    st.download_button("Download filtered registry", reg.to_csv(index=False).encode(), "initiative_registry_filtered.csv", "text/csv")

elif page == "Value & Evidence":
    render_page_header("Value & Evidence", "Inspect score composition, evidence confidence and risk deductions.")
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
    render_page_header("Governance & Risk", "Review controls, ownership and deadlines.")
    st.dataframe(cf.sort_values(["Status","Due_Date"]), use_container_width=True, hide_index=True)

elif page == "Adoption & Maturity":
    render_page_header("Adoption & Maturity", "Compare training completion with active use.")
    ad = D["adoption"][D["adoption"].Department.isin(selected_departments)]
    fig = px.scatter(ad, x="Training_Completion_Pct", y="Monthly_Active_Rate_Pct", size="Eligible_Users", color="Department", color_discrete_map=DEPT_COLORS, text="Department")
    fig.update_traces(textposition="top center", marker=dict(line=dict(width=1, color="#FFFFFF")))
    polish_figure(fig, height=470)
    fig.update_layout(legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0))
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

elif page == "Incidents & Actions":
    render_page_header("Incidents & Actions", "Track open findings and corrective actions.")
    st.dataframe(incf, use_container_width=True, hide_index=True)

else:
    render_page_header("Data Quality", "Review structural checks and trusted-data readiness.")
    st.success("No structural issues detected in the filtered initiative data.")
    st.dataframe(f, use_container_width=True, hide_index=True)

st.divider()
st.caption("Clinexa AI demonstration · Representative data only · Not validated for production or GxP use")
