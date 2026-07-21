from pathlib import Path
import io
import base64
import zipfile
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title='Clinical AI Value & Governance Platform', page_icon='🛡️', layout='wide')
APP_DIR=Path(__file__).resolve().parent
DATA_DIR=APP_DIR/'data'
FILES={
 'initiatives':'initiatives.csv','registry':'initiative_registry.csv','controls':'governance_controls.csv',
 'trends':'monthly_trends.csv','adoption':'adoption.csv','sources':'data_source_catalog.csv','incidents':'incidents.csv'}

st.markdown('''<style>
.block-container{padding-top:1.1rem;padding-bottom:2rem}.hero{padding:22px;border-radius:16px;background:linear-gradient(120deg,#10243e,#165a72);color:white;margin-bottom:14px}.hero h1{margin:0;font-size:2rem}.hero p{margin:.45rem 0 0;color:#dbeafe}.internal{font-size:.78rem;letter-spacing:.08em;text-transform:uppercase;font-weight:700;color:#bfdbfe}[data-testid="stMetric"]{background:var(--secondary-background-color);border:1px solid rgba(128,128,128,.22);padding:14px;border-radius:12px}[data-testid="stSidebar"]{background:rgba(128,128,128,.06)}.note{font-size:.82rem;color:#64748b}</style>''',unsafe_allow_html=True)

EMBEDDED_DATA_ZIP = "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"

@st.cache_data
def load_data():
    missing=[f for f in FILES.values() if not (DATA_DIR/f).exists()]

    def read_source(key, **kwargs):
        filename=FILES[key]
        file_path=DATA_DIR/filename
        if file_path.exists():
            return pd.read_csv(file_path, **kwargs)
        raw=base64.b64decode(EMBEDDED_DATA_ZIP)
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            with z.open(filename) as source:
                return pd.read_csv(source, **kwargs)

    if missing:
        st.warning(
            "The external data folder was not found. The app is running with "
            "embedded dummy data. Upload the data folder later to replace it."
        )

    return {
      'initiatives':read_source('initiatives',parse_dates=['Pilot_Start','Next_Review']),
      'registry':read_source('registry',parse_dates=['Pilot_Start','Next_Review']),
      'controls':read_source('controls',parse_dates=['Due_Date']),
      'trends':read_source('trends',parse_dates=['Month']),
      'adoption':read_source('adoption'),
      'sources':read_source('sources'),
      'incidents':read_source('incidents',parse_dates=['Detected_Date'])}

def money(v):
    return f'${v/1_000_000:.2f}M' if abs(v)>=1_000_000 else f'${v/1_000:.0f}K'

def pct_series(s):
    return pd.to_numeric(s.astype(str).str.rstrip('%'),errors='coerce')

def workbook(d):
    b=io.BytesIO()
    with pd.ExcelWriter(b,engine='xlsxwriter') as w:
        for k,v in d.items():
            v.to_excel(w,sheet_name=k[:31],index=False)
    return b.getvalue()

SCORING_REQUIRED=[
    'Initiative_ID','Initiative','Department','Annual_Investment_USD',
    'Forecast_Annual_Benefit_USD','Validated_Annual_Benefit_USD',
    'Realized_Annual_Benefit_USD','Efficiency_Score','Quality_Score',
    'Adoption_Score','Compliance_Score','Evidence_Confidence',
    'Evidence_Source','Evidence_Strength','Benefit_Status','Risk_Level',
    'Pilot_Start','Next_Review'
]
NUMERIC_COLUMNS=[
    'Annual_Investment_USD','Forecast_Annual_Benefit_USD',
    'Validated_Annual_Benefit_USD','Realized_Annual_Benefit_USD',
    'Efficiency_Score','Quality_Score','Adoption_Score',
    'Compliance_Score','Evidence_Confidence'
]

def validate(df,required=None,date_pairs=None):
    issues=[]
    required=required or SCORING_REQUIRED
    if not isinstance(df,pd.DataFrame):
        return [('Critical','Uploaded content could not be interpreted as a table.')]
    miss=sorted(set(required)-set(df.columns))
    if miss:
        issues.append(('Critical',f'Missing columns: {", ".join(miss)}'))
        return issues
    if df.empty:
        issues.append(('Critical','Dataset has no records.'))
    if df.duplicated().sum():
        issues.append(('Warning',f'{df.duplicated().sum()} duplicate row(s).'))
    if df['Initiative_ID'].astype(str).duplicated().sum():
        issues.append(('Critical','Initiative_ID must be unique.'))
    for col in [c for c in NUMERIC_COLUMNS if c in df.columns]:
        converted=pd.to_numeric(df[col],errors='coerce')
        if converted.isna().any():
            issues.append(('Critical',f'{col} contains non-numeric or missing values.'))
    for col in ['Efficiency_Score','Quality_Score','Adoption_Score','Compliance_Score','Evidence_Confidence']:
        if col in df.columns:
            vals=pd.to_numeric(df[col],errors='coerce')
            if ((vals<0)|(vals>100)).any():
                issues.append(('Critical',f'{col} must be between 0 and 100.'))
    allowed_risk={'Low','Medium','High'}
    if 'Risk_Level' in df.columns:
        unknown=sorted(set(df['Risk_Level'].dropna().astype(str))-allowed_risk)
        if unknown:
            issues.append(('Critical',f'Risk_Level contains unsupported value(s): {", ".join(unknown)}. Use Low, Medium or High.'))
    allowed_strength={'Low','Medium','High'}
    if 'Evidence_Strength' in df.columns:
        unknown=sorted(set(df['Evidence_Strength'].dropna().astype(str))-allowed_strength)
        if unknown:
            issues.append(('Critical',f'Evidence_Strength contains unsupported value(s): {", ".join(unknown)}. Use Low, Medium or High.'))
    allowed_benefit={'Forecast','Reported','Under Review','Validated','Realized'}
    if 'Benefit_Status' in df.columns:
        unknown=sorted(set(df['Benefit_Status'].dropna().astype(str))-allowed_benefit)
        if unknown:
            issues.append(('Critical',f'Benefit_Status contains unsupported value(s): {", ".join(unknown)}. Use Forecast, Reported, Under Review, Validated or Realized.'))
    for s,e in date_pairs or [('Pilot_Start','Next_Review')]:
        if s in df and e in df:
            sd=pd.to_datetime(df[s],errors='coerce'); ed=pd.to_datetime(df[e],errors='coerce')
            if sd.isna().sum()+ed.isna().sum():
                issues.append(('Critical',f'Invalid or missing dates detected in {s}/{e}.'))
            if (sd>ed).sum():
                issues.append(('Critical',f'{(sd>ed).sum()} record(s) have {s} after {e}.'))
    return issues or [('Pass','No structural or scoring-schema issues detected.')]

def read_uploaded_table(upload):
    try:
        if upload.name.lower().endswith('.csv'):
            return pd.read_csv(upload)
        return pd.read_excel(upload)
    except UnicodeDecodeError:
        raise ValueError('The CSV encoding is not supported. Save it as UTF-8 and try again.')
    except Exception as exc:
        raise ValueError(f'Unable to read the file: {exc}') from exc

def financial_score(series_benefit,series_investment):
    return np.clip(series_benefit.div(series_investment.replace(0,np.nan)).mul(50).fillna(0),0,100)

def evidence_confidence(source,existing,mapping):
    """Resolve confidence without silently forcing an ambiguous keyword match."""
    source_text=str(source).strip()
    if source_text in mapping:
        return float(mapping[source_text]), 'Exact', source_text
    lower=source_text.lower()
    aliases=[
        (('system log','telemetry','audit log','repository log','review log'), 'Automated system log'),
        (('database','warehouse','data mart'), 'Enterprise database'),
        (('validated upload','validated file','eqms export','ctms metrics'), 'Validated upload'),
        (('spreadsheet','tracker','time study','review record'), 'Manual spreadsheet'),
        (('survey','questionnaire'), 'Survey'),
        (('estimate','assumption','expert assessment'), 'User estimate'),
    ]
    matches=[]
    for keywords,key in aliases:
        if key in mapping and any(k in lower for k in keywords):
            matches.append(key)
    matches=list(dict.fromkeys(matches))
    if len(matches)==1:
        key=matches[0]
        return float(mapping[key]), 'Alias', key
    try:
        fallback=float(existing)
    except (TypeError,ValueError):
        fallback=0.0
    status='Ambiguous fallback' if len(matches)>1 else 'Unmapped fallback'
    return fallback, status, ''

def calculate_scores(df,weights,evidence_map,penalties,incidents,model_version):
    scored=df.copy()
    for col in NUMERIC_COLUMNS:
        scored[col]=pd.to_numeric(scored[col],errors='coerce')
    scored['Financial_Score']=financial_score(scored['Validated_Annual_Benefit_USD'],scored['Annual_Investment_USD']).round(1)
    total=max(sum(weights.values()),1)
    scored['Weighted_Base_Score']=(
        scored.Efficiency_Score*weights['Efficiency']+
        scored.Quality_Score*weights['Quality']+
        scored.Adoption_Score*weights['Adoption']+
        scored.Compliance_Score*weights['Compliance']+
        scored.Financial_Score*weights['Financial']
    ).div(total).round(1)
    scored['Input_Evidence_Confidence']=scored['Evidence_Confidence']
    evidence_resolution=[
        evidence_confidence(src,existing,evidence_map)
        for src,existing in zip(scored['Evidence_Source'],scored['Input_Evidence_Confidence'])
    ]
    scored['Evidence_Confidence']=[x[0] for x in evidence_resolution]
    scored['Evidence_Mapping_Status']=[x[1] for x in evidence_resolution]
    scored['Evidence_Mapped_Category']=[x[2] for x in evidence_resolution]
    scored['Evidence_Adjustment']=((100-scored.Evidence_Confidence)*0.10).round(1)
    scored['Risk_Adjustment']=0.0
    scored.loc[scored.Risk_Level.eq('High'),'Risk_Adjustment']+=penalties['High risk']
    scored.loc[scored.Risk_Level.eq('Medium'),'Risk_Adjustment']+=penalties['Medium risk']
    scored.loc[scored.Compliance_Score.lt(70),'Risk_Adjustment']+=penalties['Compliance below 70']
    scored.loc[scored.Evidence_Confidence.lt(60),'Risk_Adjustment']+=penalties['Evidence below 60']
    critical_ids=set()
    if {'Severity','Status','Initiative_ID'}.issubset(incidents.columns):
        critical_ids=set(incidents.loc[(incidents.Severity.eq('Critical')) & (~incidents.Status.eq('Closed')),'Initiative_ID'].astype(str))
    scored.loc[scored.Initiative_ID.astype(str).isin(critical_ids),'Risk_Adjustment']+=penalties['Open critical incident']
    scored['AI_Value_Score']=np.clip(scored['Weighted_Base_Score']-scored['Evidence_Adjustment']-scored['Risk_Adjustment'],0,100).round(1)
    scored['Validated_Net_Value']=scored.Validated_Annual_Benefit_USD-scored.Annual_Investment_USD
    scored['Evidence_Adjusted_Value']=scored.Validated_Annual_Benefit_USD*scored.Evidence_Confidence/100-scored.Annual_Investment_USD
    scored['Scoring_Model_Version']=model_version
    return scored

D=load_data()
DEFAULT_WEIGHTS={'Efficiency':20,'Quality':25,'Adoption':15,'Compliance':25,'Financial':15}
DEFAULT_EVIDENCE={'Automated system log':100,'Enterprise database':90,'Validated upload':80,'Manual spreadsheet':60,'Survey':50,'User estimate':30}
DEFAULT_PENALTIES={'High risk':15,'Medium risk':5,'Compliance below 70':10,'Evidence below 60':8,'Open critical incident':15}
if 'score_weights' not in st.session_state: st.session_state.score_weights=DEFAULT_WEIGHTS.copy()
if 'evidence_map' not in st.session_state: st.session_state.evidence_map=DEFAULT_EVIDENCE.copy()
if 'risk_penalties' not in st.session_state: st.session_state.risk_penalties=DEFAULT_PENALTIES.copy()
if 'model_version' not in st.session_state: st.session_state.model_version='CAVF 1.1'
if 'initiative_data' not in st.session_state: st.session_state.initiative_data=D['initiatives'].copy()

with st.sidebar:
    st.title('Clinical AI Platform')
    st.caption('Internal pharma prototype')
    role=st.selectbox('View as',['Executive Leadership','Department Leader','AI Governance','Quality / Validation','Finance','Initiative Owner','System Administrator'])
    pages=['Executive Command Center','Initiative Registry','Value & Evidence','Governance & Risk','Adoption & Maturity','Incidents & Actions','Scoring Configuration','Data Quality & Integrations','Admin Data Manager']
    page=st.radio('Navigate',pages)
    st.divider()
    st.caption(f"Scoring model: {st.session_state.model_version}")
    st.caption('Persona preview only — not production access control.')
    st.caption('Configure and publish changes from Scoring Configuration.')

weights=st.session_state.score_weights
schema_issues=validate(st.session_state.initiative_data)
blocking=[msg for sev,msg in schema_issues if sev=='Critical']
if blocking:
    st.error('The active initiative dataset cannot be scored: ' + ' | '.join(blocking))
    st.stop()
init=calculate_scores(
    st.session_state.initiative_data,
    weights,
    st.session_state.evidence_map,
    st.session_state.risk_penalties,
    D['incidents'],
    st.session_state.model_version,
)
controls=D['controls']; adoption=D['adoption']

all_depts=sorted(init.Department.unique()); selected=st.multiselect('Department scope',all_depts,default=all_depts)
f=init[init.Department.isin(selected)].copy(); cf=controls[controls.Department.isin(selected)].copy()

if page=='Executive Command Center':
    st.markdown('<div class="hero"><div class="internal">Internal decision support</div><h1>Clinical AI Value & Governance Platform</h1><p>Evidence-based portfolio oversight for value, quality, adoption, risk and responsible scale.</p></div>',unsafe_allow_html=True)
    vals=[f.Annual_Investment_USD.sum(),f.Forecast_Annual_Benefit_USD.sum(),f.Validated_Annual_Benefit_USD.sum(),f.Realized_Annual_Benefit_USD.sum()]
    c=st.columns(5); c[0].metric('Annual investment',money(vals[0])); c[1].metric('Forecast benefit',money(vals[1])); c[2].metric('Validated benefit',money(vals[2])); c[3].metric('Realized benefit',money(vals[3])); c[4].metric('Evidence-adjusted net',money(f.Evidence_Adjusted_Value.sum()))
    st.caption('Forecast, validated and realized benefits are intentionally separated to prevent unverified estimates from being presented as confirmed value.')
    c1,c2=st.columns([1.15,1])
    dept=f.groupby('Department',as_index=False).agg(Value=('AI_Value_Score','mean'),Investment=('Annual_Investment_USD','sum'),Validated=('Validated_Annual_Benefit_USD','sum'),Realized=('Realized_Annual_Benefit_USD','sum'))
    with c1:
        fig=px.bar(dept.sort_values('Value'),x='Value',y='Department',orientation='h',text_auto='.1f',range_x=[0,100],title='Department value score'); st.plotly_chart(fig,use_container_width=True)
    with c2:
        fig=px.scatter(f,x='Compliance_Score',y='AI_Value_Score',size='Annual_Investment_USD',color='Risk_Level',hover_name='Initiative',symbol='Benefit_Status',title='Portfolio value, compliance and risk'); fig.add_hline(y=75,line_dash='dot'); fig.add_vline(x=80,line_dash='dot'); st.plotly_chart(fig,use_container_width=True)
    high=f[(f.Risk_Level=='High')&(f.Compliance_Score<80)]; weak=f[f.Evidence_Confidence<70]; overdue=cf[(cf.Status!='Complete')&(cf.Due_Date<pd.Timestamp.today())]
    a, b, c = st.columns(3)
    a.warning(f'{len(high)} high-risk initiative(s) below compliance threshold')
    b.info(f'{len(weak)} initiative(s) need stronger evidence')
    if len(overdue):
        c.error(f'{len(overdue)} overdue governance action(s)')
    else:
        c.success('No overdue governance actions')

elif page=='Initiative Registry':
    st.markdown('<div class="hero"><div class="internal">Controlled inventory</div><h1>AI Initiative Registry</h1><p>Maintain ownership, intended use, classification, lifecycle and periodic review.</p></div>',unsafe_allow_html=True)
    reg=D['registry']; reg=reg[reg.Department.isin(selected)]
    st.dataframe(reg,use_container_width=True,hide_index=True,column_config={'Pilot_Start':st.column_config.DateColumn(),'Next_Review':st.column_config.DateColumn()})
    st.download_button('Download registry CSV',reg.to_csv(index=False).encode(),'initiative_registry.csv','text/csv')

elif page=='Value & Evidence':
    st.markdown('<div class="hero"><div class="internal">Evidence-based ROI</div><h1>Value & Evidence</h1><p>Review score composition, benefit maturity, source evidence and confidence.</p></div>',unsafe_allow_html=True)
    st.caption('Risk and evidence strength act as adjustments to the weighted base score, not additive weights. This prevents a high-risk or weakly evidenced initiative from appearing stronger by definition.')
    chosen=st.selectbox('Initiative',f.Initiative.tolist()); r=f[f.Initiative==chosen].iloc[0]
    a,b,c,d,e=st.columns(5); a.metric('Final AI score',f'{r.AI_Value_Score:.1f}/100'); b.metric('Weighted base',f'{r.Weighted_Base_Score:.1f}'); c.metric('Evidence confidence',f'{r.Evidence_Confidence:.0f}%'); d.metric('Risk penalty',f'-{r.Risk_Adjustment:.1f}'); e.metric('Model version',r.Scoring_Model_Version)
    c1,c2=st.columns(2)
    with c1:
        cats=['Efficiency','Quality','Adoption','Compliance','Financial']; vals=[r.Efficiency_Score,r.Quality_Score,r.Adoption_Score,r.Compliance_Score,r.Financial_Score]
        fig=go.Figure(go.Scatterpolar(r=vals+[vals[0]],theta=cats+[cats[0]],fill='toself')); fig.update_layout(polar=dict(radialaxis=dict(range=[0,100],visible=True)),showlegend=False,title='Balanced value profile'); st.plotly_chart(fig,use_container_width=True)
    with c2:
        stages=pd.DataFrame({'Benefit type':['Forecast','Validated','Realized'],'USD':[r.Forecast_Annual_Benefit_USD,r.Validated_Annual_Benefit_USD,r.Realized_Annual_Benefit_USD]}); st.plotly_chart(px.bar(stages,x='Benefit type',y='USD',text_auto='.2s',title='Benefit maturity'),use_container_width=True)
        st.info(f'**Evidence source:** {r.Evidence_Source}\n\n**Evidence strength:** {r.Evidence_Strength}\n\n**Evidence adjustment:** -{r.Evidence_Adjustment:.1f} points\n\n**Risk adjustment:** -{r.Risk_Adjustment:.1f} points\n\n**Next review:** {r.Next_Review.date()}')
    breakdown=pd.DataFrame({'Category':['Efficiency','Quality','Adoption','Compliance','Financial'],'Raw score':[r.Efficiency_Score,r.Quality_Score,r.Adoption_Score,r.Compliance_Score,r.Financial_Score],'Weight':[weights['Efficiency'],weights['Quality'],weights['Adoption'],weights['Compliance'],weights['Financial']]}); breakdown['Weighted contribution']=(breakdown['Raw score']*breakdown['Weight']/max(sum(weights.values()),1)).round(2); st.subheader('Transparent score calculation'); st.dataframe(breakdown,use_container_width=True,hide_index=True); st.caption(f"Final score = {r.Weighted_Base_Score:.1f} weighted base − {r.Evidence_Adjustment:.1f} evidence adjustment − {r.Risk_Adjustment:.1f} risk adjustment = {r.AI_Value_Score:.1f}")

elif page=='Governance & Risk':
    st.markdown('<div class="hero"><div class="internal">Responsible scale</div><h1>Governance & Risk</h1><p>Track controls, evidence, ownership, due dates and unresolved gaps.</p></div>',unsafe_allow_html=True)
    cf['Evidence_Confidence_Num']=pct_series(cf.Evidence_Confidence)
    pivot=pd.crosstab(cf.Department,cf.Status); st.plotly_chart(px.bar(pivot.reset_index(),x='Department',y=[x for x in ['Complete','In Progress','Gap'] if x in pivot],barmode='stack',title='Control status by department'),use_container_width=True)
    open_actions=cf[cf.Status!='Complete'].sort_values(['Due_Date','Department']); st.dataframe(open_actions,use_container_width=True,hide_index=True,column_config={'Due_Date':st.column_config.DateColumn(),'Evidence_Confidence_Num':st.column_config.ProgressColumn(min_value=0,max_value=100)})

elif page=='Adoption & Maturity':
    st.markdown('<div class="hero"><div class="internal">Sustainable use</div><h1>Adoption & Maturity</h1><p>Measure active usage, training, overrides, satisfaction and long-term readiness.</p></div>',unsafe_allow_html=True)
    af=adoption[adoption.Department.isin(selected)]
    c1,c2=st.columns(2)
    with c1: st.plotly_chart(px.bar(af,x='Department',y='Monthly_Active_Rate_Pct',color='Role_Group',barmode='group',title='Monthly active use by role'),use_container_width=True)
    with c2: st.plotly_chart(px.scatter(af,x='Training_Completion_Pct',y='Monthly_Active_Rate_Pct',size='Eligible_Users',color='Role_Group',hover_name='Department',title='Training versus active use'),use_container_width=True)
    tf=D['trends'][D['trends'].Department.isin(selected)]; st.plotly_chart(px.line(tf,x='Month',y='AI_Value_Score',color='Department',markers=True,title='Value trend over time'),use_container_width=True)

elif page=='Incidents & Actions':
    st.markdown('<div class="hero"><div class="internal">Operational oversight</div><h1>Incidents & Corrective Actions</h1><p>Surface quality, performance and integration issues requiring ownership.</p></div>',unsafe_allow_html=True)
    inc=D['incidents']; inc=inc[inc.Department.isin(selected)]
    st.dataframe(inc,use_container_width=True,hide_index=True,column_config={'Detected_Date':st.column_config.DateColumn()})
    st.warning('Prototype workflow only. A production implementation should link to the approved eQMS or service-management process rather than replace it.')


elif page=='Scoring Configuration':
    st.markdown('<div class="hero"><div class="internal">Controlled rules engine</div><h1>Scoring Configuration</h1><p>Configure category weights, evidence confidence and risk penalties with transparent versioning.</p></div>',unsafe_allow_html=True)
    st.warning('Prototype behavior: changes are stored only for the current browser session. Production use should require authentication, review, approval, effective dates and an audit trail.')
    tab1,tab2,tab3,tab4=st.tabs(['Category weights','Evidence confidence','Risk adjustments','Model governance'])
    with tab1:
        st.write('Weights determine the contribution of each category to the weighted base score. They are normalized automatically, so they do not need to total 100 while editing.')
        cols=st.columns(5); draft={}
        for c,(name,val) in zip(cols,st.session_state.score_weights.items()):
            draft[name]=c.number_input(name,min_value=0,max_value=100,value=int(val),step=1,key=f'w_{name}')
        total=sum(draft.values()); st.metric('Current weight total',f'{total}%')
        if total:
            norm=pd.DataFrame({'Category':list(draft),'Entered weight':list(draft.values()),'Normalized contribution (%)':[round(v/total*100,1) for v in draft.values()]})
            st.dataframe(norm,use_container_width=True,hide_index=True)
        if st.button('Apply category weights',type='primary'):
            if total==0: st.error('At least one category weight must be greater than zero.')
            else: st.session_state.score_weights=draft; st.success('Category weights applied to this session. Scores have been recalculated.'); st.rerun()
    with tab2:
        st.write('Evidence confidence indicates how reliable the supporting source is. Mappings are applied immediately to each initiative through Evidence_Source. Exact labels are used first, followed by transparent keyword-based fallback; the original row value is retained only when no mapping applies.')
        ev=pd.DataFrame({'Evidence source':list(st.session_state.evidence_map),'Confidence (%)':list(st.session_state.evidence_map.values())})
        edited=st.data_editor(ev,use_container_width=True,hide_index=True,num_rows='dynamic',column_config={'Confidence (%)':st.column_config.NumberColumn(min_value=0,max_value=100,step=5)})
        if st.button('Apply evidence mapping'):
            st.session_state.evidence_map={str(r['Evidence source']):int(r['Confidence (%)']) for _,r in edited.dropna().iterrows()}; st.success('Evidence mapping applied.')
    with tab3:
        st.write('Penalties reduce the final score when material governance or risk conditions are present.')
        rp=pd.DataFrame({'Condition':list(st.session_state.risk_penalties),'Penalty points':list(st.session_state.risk_penalties.values())})
        redited=st.data_editor(rp,use_container_width=True,hide_index=True,column_config={'Penalty points':st.column_config.NumberColumn(min_value=0,max_value=50,step=1)})
        if st.button('Apply risk penalties'):
            st.session_state.risk_penalties={str(r['Condition']):int(r['Penalty points']) for _,r in redited.iterrows()}; st.success('Risk penalties applied.'); st.rerun()
    with tab4:
        version=st.text_input('Draft model version',value=st.session_state.model_version)
        status=st.selectbox('Configuration status',['Draft','Under Review','Approved','Published'])
        effective=st.date_input('Effective date')
        rationale=st.text_area('Change rationale',placeholder='Explain what changed and why.')
        c1,c2=st.columns(2)
        if c1.button('Publish model version',type='primary'):
            if status!='Published': st.error('Set configuration status to Published before publishing.')
            elif not rationale.strip(): st.error('A change rationale is required.')
            else: st.session_state.model_version=version.strip() or st.session_state.model_version; st.success(f'{st.session_state.model_version} published for this session.'); st.rerun()
        if c2.button('Restore defaults'):
            st.session_state.score_weights=DEFAULT_WEIGHTS.copy(); st.session_state.evidence_map=DEFAULT_EVIDENCE.copy(); st.session_state.risk_penalties=DEFAULT_PENALTIES.copy(); st.session_state.model_version='CAVF 1.0'; st.rerun()
        st.subheader('Prototype audit record')
        st.dataframe(pd.DataFrame([{'Version':st.session_state.model_version,'Status':status,'Effective date':effective,'Rationale':rationale or 'No unpublished change recorded','User role':role}]),use_container_width=True,hide_index=True)

elif page=='Data Quality & Integrations':
    st.markdown('<div class="hero"><div class="internal">Trusted data foundation</div><h1>Data Quality & Integrations</h1><p>Validate data contracts and plan governed connections to internal systems.</p></div>',unsafe_allow_html=True)
    issues=validate(st.session_state.initiative_data)
    for sev,msg in issues:
        {'Pass':st.success,'Warning':st.warning,'Critical':st.error}[sev](msg)
    mapping_review=init.loc[init['Evidence_Mapping_Status'].isin(['Ambiguous fallback','Unmapped fallback']),['Initiative_ID','Initiative','Evidence_Source','Evidence_Mapping_Status','Evidence_Confidence']]
    if not mapping_review.empty:
        st.warning(f'{len(mapping_review)} evidence source(s) use the uploaded row confidence because no unique configured mapping was found. Review these sources before relying on the score.')
        st.dataframe(mapping_review,use_container_width=True,hide_index=True)
    else:
        st.success('All evidence sources resolved through an exact or unique configured mapping.')
    st.subheader('Integration catalog'); st.dataframe(D['sources'],use_container_width=True,hide_index=True)
    st.info('Use aggregated operational metadata for the prototype. Do not ingest patient-identifiable information without an approved privacy, security and validation architecture.')

elif page=='Admin Data Manager':
    st.markdown('<div class="hero"><div class="internal">Administrator workspace</div><h1>Admin Data Manager</h1><p>Download controlled templates and test uploaded portfolio files within the current session.</p></div>',unsafe_allow_html=True)
    st.info('A validated upload can replace the initiative dataset for the current browser session. It does not overwrite files in GitHub or any enterprise system.')
    upload=st.file_uploader('Upload initiative CSV or Excel',type=['csv','xlsx'])
    test=st.session_state.initiative_data.copy()
    upload_ok=False
    if upload:
        try:
            test=read_uploaded_table(upload)
            issues=validate(test)
            for sev,msg in issues:
                {'Pass':st.success,'Warning':st.warning,'Critical':st.error}[sev](msg)
            upload_ok=not any(sev=='Critical' for sev,_ in issues)
        except ValueError as exc:
            st.error(str(exc))
    else:
        for sev,msg in validate(test):
            {'Pass':st.success,'Warning':st.warning,'Critical':st.error}[sev](msg)
    st.dataframe(test.head(30),use_container_width=True,hide_index=True)
    c1,c2=st.columns(2)
    if c1.button('Use uploaded data in dashboard',type='primary',disabled=not upload_ok):
        for col in ['Pilot_Start','Next_Review']:
            test[col]=pd.to_datetime(test[col],errors='coerce')
        st.session_state.initiative_data=test.copy()
        st.success('Uploaded initiative data is now active for this session.')
        st.rerun()
    if c2.button('Restore packaged dummy data'):
        st.session_state.initiative_data=D['initiatives'].copy()
        st.rerun()
    st.download_button('Download complete internal dummy-data workbook',workbook({**D,'initiatives':st.session_state.initiative_data}),'clinical_ai_internal_dummy_inputs.xlsx','application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

st.divider(); st.caption(f'Internal pharma prototype • Active view: {role} • Representative data only • Not validated for production or GxP use')
