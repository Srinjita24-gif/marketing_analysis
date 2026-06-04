import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Marketing Intelligence Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&display=swap');

*, html, body, [class*="css"],
p, span, div, h1, h2, h3, h4, h5, h6, label,
.stMarkdown, .stText, [data-testid="stMarkdownContainer"] * {
    font-family: 'DM Sans', sans-serif !important;
    box-sizing: border-box;
}

[data-testid="stAppViewContainer"] p,
[data-testid="stAppViewContainer"] span,
[data-testid="stAppViewContainer"] div,
[data-testid="stAppViewContainer"] label,
[data-testid="stMarkdownContainer"] p { color: #0F172A; }

[data-testid="stAppViewContainer"],
[data-testid="stAppViewContainer"] > .main,
[data-testid="stMain"] { background: #F5F7FA !important; }
.block-container { padding: 1.5rem 2rem 3rem !important; max-width: 100% !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #0F172A !important;
    border-right: 1px solid #1E293B !important;
}
[data-testid="stSidebar"] * {
    color: #E2E8F0 !important;
    font-family: 'DM Sans', sans-serif !important;
}
[data-testid="stSidebar"] h1 {
    color: #FFFFFF !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 1px;
}
[data-testid="stSidebar"] hr { border-color: #334155 !important; margin: 12px 0 !important; }
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stRadio label {
    color: #CBD5E1 !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    text-transform: uppercase;
    letter-spacing: 0.8px;
}
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] .stMultiSelect > div > div {
    background: #1E293B !important;
    border: 1px solid #475569 !important;
    border-radius: 6px !important;
    color: #F1F5F9 !important;
}
[data-testid="stSidebar"] .stSelectbox > div > div > div,
[data-testid="stSidebar"] .stSelectbox span { color: #F1F5F9 !important; }
[data-testid="stSidebar"] .stRadio > div { gap: 4px; }
[data-testid="stSidebar"] .stRadio > div > label {
    font-size: 12px !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
    color: #CBD5E1 !important;
}
[data-testid="stSidebar"] .stCaption,
[data-testid="stSidebar"] .stCaption p { color: #64748B !important; font-size: 11px !important; }
[data-testid="stSidebar"] .stSlider [data-testid="stTickBarMin"],
[data-testid="stSidebar"] .stSlider [data-testid="stTickBarMax"] { color: #94A3B8 !important; }
[data-testid="stSidebar"] .stSlider > div > div > div { background: #334155 !important; }

/* ── Main content text ── */
.stTabs [data-testid="stMarkdownContainer"] * { color: #0F172A !important; }

/* ── Tabs ── */
div[data-testid="stTabs"] { border-bottom: 2px solid #E2E8F0; margin-bottom: 10px; }
div[data-testid="stTabs"] button {
    font-size: 13px !important;
    font-weight: 500 !important;
    color: #334155 !important;
    padding: 10px 20px !important;
    border-radius: 0 !important;
    background: transparent !important;
}
div[data-testid="stTabs"] button:hover { color: #0F172A !important; }
div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #0F172A !important;
    font-weight: 700 !important;
    border-bottom: 2.5px solid #0F172A !important;
    background: transparent !important;
}
div[data-testid="stTabs"] button p { color: inherit !important; font-size: inherit !important; }

/* ══════════════════════════════════════════════════════
   KPI CARDS — thin black border all around
   ══════════════════════════════════════════════════════ */
.kpi-row { display: flex; gap: 14px; margin-bottom: 24px; flex-wrap: nowrap; }
.kpi-card {
    flex: 1; background: #FFFFFF; min-width: 0;
    border-radius: 12px;
    padding: 22px 16px 18px 16px;
    /* CHANGED: unified thin black border + accent left */
    border: 1px solid #0F172A;
    border-left: 5px solid var(--ac);
    box-shadow: 0 1px 4px rgba(0,0,0,0.05);
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
}
.kpi-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.12); }

/* CHANGED: font-size 35px → 28px */
.kpi-value {
    font-size: 30px !important;
    font-weight: 500 !important;
    line-height: 1.0;
    margin: 0 0 8px 0;
    color: var(--ac) !important;
    letter-spacing: -1px;
    display: block;
    width: 100%;
    text-align: center;
}
.kpi-label {
    font-size: 11px !important;
    font-weight: 700 !important;
    color: #0F172A !important;
    text-transform: uppercase;
    letter-spacing: 0.9px;
    margin: 0 0 6px 0;
    display: block;
    width: 100%;
    text-align: center;
    line-height: 1.3;
}
.kpi-delta { font-size: 10px; font-weight: 600; margin: 0; display: block; text-align: center; width: 100%; }
.kpi-delta.pos { color: #059669; }
.kpi-delta.neg { color: #DC2626; }
.kpi-delta.neu { color: #64748B; }

/* ── Section header ── */
.sec-header { margin: 2px 0 16px; }
.sec-title { font-size: 17px; font-weight: 700; color: #0F172A !important; margin: 0 0 4px; }
.sec-sub { font-size: 12px; color: #475569 !important; margin: 0; }

/* ── Insight box ── */
.insight-box {
    background: #FAFAFA; border: 1px solid #E2E8F0;
    border-left: 4px solid #0F172A; border-radius: 8px;
    padding: 13px 18px; margin-top: 14px; font-size: 13px; color: #0F172A !important;
}
.insight-box b { color: #0F172A !important; font-weight: 700; }

/* ── Chart wrapper — thin black border + shadow ── */
[data-testid="stPlotlyChart"] {
    border: 1px solid #0F172A;
    border-radius: 10px;
    overflow: hidden;
    box-shadow: 0 2px 10px rgba(0,0,0,0.10);
    background: #FFFFFF;
}


/* ── Dataframe ── */
[data-testid="stDataFrame"] { border-radius: 8px !important; overflow: hidden; border: 1px solid #E2E8F0 !important; }
[data-testid="stDataFrame"] th { background: #F8FAFC !important; color: #0F172A !important; font-weight: 700 !important; font-size: 11px !important; text-transform: uppercase; letter-spacing: 0.6px; }
[data-testid="stDataFrame"] td { color: #0F172A !important; }

/* ── Download button — CHANGED: added thin black border ── */
[data-testid="stDownloadButton"] > button {
    background: #0F172A !important; color: #FFFFFF !important;
    border: 1px solid #0F172A !important;
    border-radius: 6px !important;
    font-size: 13px !important; font-weight: 600 !important; padding: 8px 20px !important;
    box-shadow: 0 1px 4px rgba(0,0,0,0.18) !important;
}
[data-testid="stDownloadButton"] > button:hover {
    border: 1px solid #334155 !important;
    box-shadow: 0 3px 10px rgba(0,0,0,0.22) !important;
}

/* ── Divider ── */
.hdr-divider { border: none; border-top: 1.5px solid #E2E8F0; margin: 8px 0 20px; }

/* Force plotly chart text black */
.js-plotly-plot .plotly .gtitle { fill: #0F172A !important; }
.js-plotly-plot .plotly .xtick text,
.js-plotly-plot .plotly .ytick text,
.js-plotly-plot .plotly .g-xtitle text,
.js-plotly-plot .plotly .g-ytitle text,
.js-plotly-plot .plotly .legendtext { fill: #0F172A !important; }
</style>
""", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# CHART DESIGN SYSTEM
# ══════════════════════════════════════════════════════
BG    = '#FFFFFF'
GRID  = '#F1F5F9'
BLACK = '#0F172A'

C_BLUE   = '#2563EB'
C_TEAL   = '#0D9488'
C_AMBER  = '#D97706'
C_RED    = '#DC2626'
C_GREEN  = '#059669'
C_PURPLE = '#7C3AED'
C_PINK   = '#BE185D'
C_ORANGE = '#EA580C'
C_SKY    = '#0284C7'

PALETTE    = [C_BLUE, C_TEAL, C_AMBER, C_PURPLE, C_RED, C_GREEN, C_PINK, C_ORANGE]
SEG_COLORS = {'Low value': C_RED, 'Mid value': C_AMBER, 'High value': C_GREEN}
EDU_PALETTE = ['#0D9488', '#059669', '#0891B2', '#0284C7', '#7C3AED', '#BE185D', '#D97706', '#EA580C']
HEATMAP_WARM  = [[0,'#FFF7ED'],[0.35,'#FDBA74'],[0.7,'#F97316'],[1,'#9A3412']]
HEATMAP_CORAL = [[0,'#FFF1F2'],[0.35,'#FDA4AF'],[0.7,'#F43F5E'],[1,'#881337']]

def hex_rgba(h, a=0.12):
    h = h.lstrip('#')
    r,g,b = int(h[0:2],16), int(h[2:4],16), int(h[4:6],16)
    return f'rgba({r},{g},{b},{a})'

XAX_BASE = dict(
    showline=True, linecolor=BLACK, linewidth=1.8,
    tickfont=dict(color=BLACK, size=11, family='DM Sans'),
    title_font=dict(color=BLACK, size=12, family='DM Sans', weight=600),
    gridcolor=GRID, gridwidth=1, zeroline=False,
    ticks='outside', tickcolor=BLACK, ticklen=4,
)
YAX_BASE = dict(
    showline=True, linecolor=BLACK, linewidth=1.8,
    tickfont=dict(color=BLACK, size=11, family='DM Sans'),
    title_font=dict(color=BLACK, size=12, family='DM Sans', weight=600),
    gridcolor=GRID, gridwidth=1, zeroline=False,
    ticks='outside', tickcolor=BLACK, ticklen=4,
)
HOVER = dict(bgcolor=BLACK, font_size=12, font_family='DM Sans',
             bordercolor=BLACK, font_color='#FFFFFF')

def _leg(orient='h', y=-0.22, x=0.5):
    return dict(
        font=dict(family='DM Sans', color=BLACK, size=11),
        bgcolor='rgba(0,0,0,0)', borderwidth=0,
        title_font=dict(color=BLACK),
        orientation=orient,
        yanchor='top' if orient=='h' else 'middle',
        y=y, xanchor='center' if orient=='h' else 'left',
        x=x
    )

def sf(fig, title='', h=True, v=False, height=340):
    upd = dict(
        paper_bgcolor=BG, plot_bgcolor=BG, height=height,
        font=dict(family='DM Sans', color=BLACK, size=12),
        title_text=title,
        title_font=dict(family='DM Sans', color=BLACK, size=13, weight=700),
        title_x=0.0, title_xanchor='left',
        title_pad=dict(t=4, b=12),
        margin=dict(t=48, b=80, l=60, r=24),
        hoverlabel=HOVER,
    )
    if h and not v:
        upd['legend'] = _leg('h', y=-0.28)
    elif v:
        upd['legend'] = _leg('v', y=0.5, x=1.02)
    else:
        upd['showlegend'] = False
    fig.update_layout(**upd)
    fig.update_xaxes(**XAX_BASE)
    fig.update_yaxes(**YAX_BASE)
    for tr in fig.data:
        if hasattr(tr, 'type') and tr.type == 'bar':
            tr.marker.line.color = 'rgba(0,0,0,0.25)'
            tr.marker.line.width = 0.8
    return fig

def donut(fig, title='', height=340):
    fig.update_layout(
        paper_bgcolor=BG, height=height,
        font=dict(family='DM Sans', color=BLACK, size=12),
        title_text=title,
        title_font=dict(family='DM Sans', color=BLACK, size=13, weight=700),
        title_x=0.0, title_xanchor='left',
        title_pad=dict(t=4, b=12),
        legend=dict(
            font=dict(family='DM Sans', color=BLACK, size=11),
            bgcolor='rgba(0,0,0,0)', borderwidth=0,
            orientation='h', yanchor='top', y=-0.12,
            xanchor='center', x=0.5
        ),
        margin=dict(t=48, b=60, l=16, r=16),
    )
    fig.update_traces(
        textinfo='percent+label',
        textfont=dict(family='DM Sans', size=11, color='#0F172A'),
        marker=dict(line=dict(color='#FFFFFF', width=2)),
        hovertemplate='<b>%{label}</b><br>Count: %{value}<br>%{percent}<extra></extra>',
    )
    return fig

def heatmap(fig, title='', height=320, lmargin=110):
    fig.update_layout(
        paper_bgcolor=BG, plot_bgcolor=BG, height=height,
        font=dict(family='DM Sans', color=BLACK, size=12),
        title_text=title,
        title_font=dict(family='DM Sans', color=BLACK, size=13, weight=700),
        title_x=0.0, title_xanchor='left',
        title_pad=dict(t=4, b=12),
        margin=dict(t=48, b=50, l=lmargin, r=20),
        coloraxis_colorbar=dict(
            tickfont=dict(color=BLACK, family='DM Sans', size=11),
            title_font=dict(color=BLACK, family='DM Sans'),
        ),
        hoverlabel=HOVER,
    )
    fig.update_xaxes(
        tickfont=dict(color=BLACK, size=11, family='DM Sans'),
        title_font=dict(color=BLACK, size=12, family='DM Sans'),
        showline=False, showgrid=False, zeroline=False, ticks='',
    )
    fig.update_yaxes(
        tickfont=dict(color=BLACK, size=11, family='DM Sans'),
        title_font=dict(color=BLACK, size=12, family='DM Sans'),
        showline=False, showgrid=False, zeroline=False, ticks='',
    )
    fig.update_traces(
        textfont=dict(color=BLACK, size=11, family='DM Sans'),
        xgap=2, ygap=2,
    )
    return fig




# ══════════════════════════════════════════════════════
# DATA
# ══════════════════════════════════════════════════════
@st.cache_data
def load_data():
    df = pd.read_excel('marketing_campaign.xlsx')
    df.dropna(subset=['Income'], inplace=True)
    df['Age'] = 2024 - df['Year_Birth']
    df = df[(df['Age'] >= 18) & (df['Age'] <= 90)]
    df['Dt_Customer'] = pd.to_datetime(df['Dt_Customer'], dayfirst=True, errors='coerce')
    df['Tenure_Days'] = (pd.Timestamp('2024-01-01') - df['Dt_Customer']).dt.days
    df['Tenure_Years'] = (df['Tenure_Days'] / 365).round(1)
    df['TotalSpend']    = (df['MntWines']+df['MntFruits']+df['MntMeatProducts']
                          +df['MntFishProducts']+df['MntSweetProducts']+df['MntGoldProds'])
    df['TotalPurchases']= (df['NumWebPurchases']+df['NumCatalogPurchases']+df['NumStorePurchases'])
    df['TotalAccepted'] = (df['AcceptedCmp1']+df['AcceptedCmp2']+df['AcceptedCmp3']
                          +df['AcceptedCmp4']+df['AcceptedCmp5']+df['Response'])
    df['HasChildren']   = ((df['Kidhome']+df['Teenhome'])>0).astype(int)
    df['ROI']           = (df['TotalAccepted']*df['Z_Revenue'])-(6*df['Z_CostContact'])
    df['DealDependency']= (df['NumDealsPurchases']/(df['TotalPurchases']+1)*100).round(1)
    df['Segment'] = pd.cut(df['TotalSpend'], bins=[-1,200,800,99999],
                           labels=['Low value','Mid value','High value'])
    df['AgeGroup'] = pd.cut(df['Age'], bins=[17,30,45,60,90],
                            labels=['18-30','31-45','46-60','60+'])
    df['IncomeBand'] = pd.cut(df['Income'], bins=[0,30000,60000,90000,9999999],
                              labels=['<$30K','$30-60K','$60-90K','$90K+'])
    return df

df = load_data()


# ══════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("<h1>Filters</h1>", unsafe_allow_html=True)
    st.markdown("---")
    edu_opts = ['All']+sorted(df['Education'].dropna().unique().tolist())
    sel_edu  = st.selectbox("Education", edu_opts)
    mar_opts = ['All']+sorted(df['Marital_Status'].dropna().unique().tolist())
    sel_mar  = st.selectbox("Marital Status", mar_opts)
    inc_min, inc_max = int(df['Income'].min()), int(df['Income'].max())
    income_rng = st.slider("Income Range ($)", inc_min, inc_max, (inc_min,inc_max), step=1000)
    seg_opts = st.multiselect("Segment", ['Low value','Mid value','High value'],
                              default=['Low value','Mid value','High value'])
    children   = st.radio("Has Children", ["All","Yes","No"])
    age_grp_opts = ['All','18-30','31-45','46-60','60+']
    sel_age_grp  = st.selectbox("Age Group", age_grp_opts)
    ten_min, ten_max = float(df['Tenure_Years'].min()), float(df['Tenure_Years'].max())
    tenure_rng = st.slider("Tenure (Years)", ten_min, ten_max, (ten_min,ten_max), step=0.5)
    st.markdown("---")
    st.caption(f"Total respondents: {len(df):,}")


# ══════════════════════════════════════════════════════
# FILTERS
# ══════════════════════════════════════════════════════
filt = df.copy()
if sel_edu  != 'All': filt = filt[filt['Education']      == sel_edu]
if sel_mar  != 'All': filt = filt[filt['Marital_Status'] == sel_mar]
filt = filt[(filt['Income']>=income_rng[0])&(filt['Income']<=income_rng[1])]
if seg_opts:          filt = filt[filt['Segment'].isin(seg_opts)]
else:
    st.warning("Select at least one customer segment.")
    st.stop()
if children == 'Yes': filt = filt[filt['HasChildren']==1]
elif children == 'No': filt = filt[filt['HasChildren']==0]
if sel_age_grp != 'All': filt = filt[filt['AgeGroup']==sel_age_grp]
filt = filt[(filt['Tenure_Years']>=tenure_rng[0])&(filt['Tenure_Years']<=tenure_rng[1])]
if filt.empty:
    st.error("No data matches the selected filters.")
    st.stop()


# ══════════════════════════════════════════════════════
# HEADER
# ══════════════════════════════════════════════════════
hc1, hc2 = st.columns([3,1])
with hc1:
    st.markdown(
        "<h2 style='margin:0;color:#0F172A;font-family:DM Sans,sans-serif;"
        "font-weight:700;font-size:22px;letter-spacing:-0.3px;'>"
        "Marketing Intelligence Dashboard</h2>",
        unsafe_allow_html=True)
with hc2:
    pct = len(filt)/len(df)*100
    st.markdown(
        f"<div style='text-align:right;padding-top:10px;'>"
        f"<span style='font-size:11px;color:#475569;'>Showing </span>"
        f"<span style='font-size:16px;font-weight:700;color:#0F172A;'>{len(filt):,}</span>"
        f"<span style='font-size:11px;color:#475569;'> of {len(df):,}&nbsp;&nbsp;{pct:.1f}%</span>"
        f"</div>", unsafe_allow_html=True)
st.markdown("<hr class='hdr-divider'>", unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# KPI CARDS
# ══════════════════════════════════════════════════════
avg_spend   = filt['TotalSpend'].mean()
accept_rate = filt['TotalAccepted'].gt(0).mean()*100
avg_roi     = filt['ROI'].mean()
avg_income  = filt['Income'].mean()
deal_dep    = filt['DealDependency'].mean()

d_spend  = avg_spend   - df['TotalSpend'].mean()
d_accept = accept_rate - df['TotalAccepted'].gt(0).mean()*100
d_roi    = avg_roi     - df['ROI'].mean()
d_income = avg_income  - df['Income'].mean()
d_deal   = deal_dep    - df['DealDependency'].mean()

def delta_html(val, prefix='', suffix='', pos_good=True):
    if abs(val) < 0.01:
        return "<span class='kpi-delta neu'>No change vs avg</span>"
    sym  = '+' if val > 0 else '-'
    good = (val>0)==pos_good
    cls  = 'pos' if good else 'neg'
    return f"<span class='kpi-delta {cls}'>{sym} {prefix}{abs(val):,.0f}{suffix} vs avg</span>"

roi_color = C_GREEN if avg_roi >= 0 else C_RED

kpi_cards = [
    (C_BLUE,   "Avg Spend / Customer",  f"${avg_spend:,.0f}",  delta_html(d_spend,'$','',True)),
    (C_TEAL,   "Campaign Acceptance",   f"{accept_rate:.1f}%", delta_html(d_accept,'','%',True)),
    (roi_color,"Avg ROI / Customer",    f"${avg_roi:,.1f}",    delta_html(d_roi,'$','',True)),
    (C_AMBER,  "Avg Annual Income",     f"${avg_income:,.0f}", delta_html(d_income,'$','',True)),
    (C_PURPLE, "Deal Dependency",       f"{deal_dep:.1f}%",    delta_html(d_deal,'','%',False)),
]

html = '<div class="kpi-row">'
for ac, lbl, val, delta in kpi_cards:
    html += f"""
    <div class="kpi-card" style="--ac:{ac};">
      <span class="kpi-value">{val}</span>
      <span class="kpi-label">{lbl}</span>
      {delta}
    </div>"""
html += '</div>'
st.markdown(html, unsafe_allow_html=True)


# ══════════════════════════════════════════════════════
# TABS
# ══════════════════════════════════════════════════════
tab1,tab2,tab3,tab4,tab5 = st.tabs([
    "Customer Profile","Spending Behavior","Campaigns","Channels","ROI & Segments"
])

CAMPS = {'Cmp 1':'AcceptedCmp1','Cmp 2':'AcceptedCmp2','Cmp 3':'AcceptedCmp3',
         'Cmp 4':'AcceptedCmp4','Cmp 5':'AcceptedCmp5','Last':'Response'}
SPEND_COLS = {'Wines':'MntWines','Fruits':'MntFruits','Meat':'MntMeatProducts',
              'Fish':'MntFishProducts','Sweets':'MntSweetProducts','Gold':'MntGoldProds'}
SPEND_COLORS = {'Wines':C_BLUE,'Fruits':C_TEAL,'Meat':C_AMBER,
                'Fish':C_SKY,'Sweets':C_PINK,'Gold':C_PURPLE}


# ══════════════════════════════════════════
# TAB 1 — CUSTOMER PROFILE
# ══════════════════════════════════════════
with tab1:
    st.markdown('<div class="sec-header"><p class="sec-title">Customer Demographics</p>'
                '<p class="sec-sub">Age distribution, education breakdown, income–spend relationship and lifestyle overview</p></div>',
                unsafe_allow_html=True)

    c1,c2 = st.columns(2, gap='large')
    with c1:
        fig = px.histogram(filt, x='Age', nbins=25, color_discrete_sequence=[C_TEAL])
        fig.update_traces(
            marker_line_color='rgba(0,0,0,0.25)', marker_line_width=0.8,
            hovertemplate='Age: %{x}<br>Count: %{y}<extra></extra>'
        )
        fig.update_layout(bargap=0.06, showlegend=False,
                          xaxis_title='Age (years)', yaxis_title='Customers')
        sf(fig, title='Age Distribution', h=False)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        edu_df = (filt['Education'].value_counts().reset_index()
                  .rename(columns={'Education':'Edu','count':'N'}).sort_values('N'))
        bar_colors = [EDU_PALETTE[i % len(EDU_PALETTE)] for i in range(len(edu_df))]
        fig = go.Figure()
        for _, row in edu_df.iterrows():
            fig.add_shape(type='line', x0=0, x1=row['N'], y0=row['Edu'], y1=row['Edu'],
                          line=dict(color='#E2E8F0', width=1.5))
        fig.add_trace(go.Scatter(
            x=edu_df['N'], y=edu_df['Edu'], mode='markers+text',
            marker=dict(size=16, color=bar_colors, line=dict(color='#FFFFFF', width=2)),
            text=edu_df['N'], textposition='middle right',
            textfont=dict(color=BLACK, size=11, family='DM Sans'),
            hovertemplate='%{y}: <b>%{x}</b><extra></extra>',
        ))
        fig.update_layout(xaxis_title='Customers', yaxis_title='', showlegend=False,
                          paper_bgcolor=BG, plot_bgcolor=BG)
        sf(fig, title='Education Level Breakdown', h=False)
        st.plotly_chart(fig, use_container_width=True)

    c3,c4 = st.columns(2, gap='large')
    with c3:
        fig = px.scatter(filt, x='Income', y='TotalSpend', color='Segment',
                         color_discrete_map=SEG_COLORS, opacity=0.45,
                         hover_data=['Age','Education'])
        fig.update_traces(marker=dict(size=5, line=dict(color='#FFFFFF', width=0.5)))
        fig.update_layout(xaxis_title='Annual Income ($)', yaxis_title='Total Spend ($)',
                          xaxis_tickprefix='$', yaxis_tickprefix='$')
        sf(fig, title='Income vs Total Spend by Segment', h=True)
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        mar_df = filt['Marital_Status'].value_counts().reset_index()
        mar_df.columns = ['Status','Count']
        mar_df['Pct'] = (mar_df['Count']/mar_df['Count'].sum()*100).round(1)
        fig = px.treemap(mar_df, path=['Status'], values='Count',
                         color='Count',
                         color_continuous_scale=[[0,'#DBEAFE'],[0.5,'#60A5FA'],[1,C_BLUE]],
                         custom_data=['Pct'])
        fig.update_traces(
            texttemplate='<b>%{label}</b><br>%{value:,}<br>%{customdata[0][0]:.1f}%',
            textfont=dict(size=12, family='DM Sans', color=BLACK),
            marker=dict(line=dict(width=2, color='#FFFFFF')),
        )
        fig.update_layout(paper_bgcolor=BG, height=340,
                          font=dict(family='DM Sans', color=BLACK),
                          title_text='Marital Status Distribution',
                          title_font=dict(family='DM Sans', color=BLACK, size=13, weight=700),
                          title_x=0.0, title_xanchor='left', title_pad=dict(t=4,b=12),
                          margin=dict(t=48,b=10,l=10,r=10),
                          coloraxis_showscale=False)
        st.plotly_chart(fig, use_container_width=True)

    c5,c6 = st.columns(2, gap='large')
    with c5:
        ch_df = (filt['HasChildren'].map({0:'No Children',1:'Has Children'})
                 .value_counts().reset_index())
        ch_df.columns = ['Status','Count']
        fig = px.pie(ch_df, names='Status', values='Count', hole=0.58,
                     color_discrete_sequence=[C_PURPLE,C_TEAL])
        donut(fig, title='Children at Home')
        st.plotly_chart(fig, use_container_width=True)

    with c6:
        fig = px.histogram(filt, x='Tenure_Years', nbins=20,
                           color_discrete_sequence=[C_AMBER])
        fig.update_traces(
            marker_line_color='rgba(0,0,0,0.25)', marker_line_width=0.8,
            hovertemplate='Tenure: %{x:.1f}yr<br>Count: %{y}<extra></extra>'
        )
        fig.update_layout(bargap=0.06, showlegend=False,
                          xaxis_title='Years as Customer', yaxis_title='Customers')
        sf(fig, title='Customer Tenure Distribution', h=False)
        st.plotly_chart(fig, use_container_width=True)

    edu_mode = filt['Education'].mode()
    edu_str  = edu_mode.iloc[0] if not edu_mode.empty else 'N/A'
    st.markdown(
        f'<div class="insight-box"><b>Key Insight:</b> Average age <b>{filt["Age"].mean():.0f} yrs</b>'
        f' &nbsp;·&nbsp; <b>{(filt["HasChildren"]==0).mean()*100:.0f}%</b> have no children'
        f' &nbsp;·&nbsp; Most common education: <b>{edu_str}</b>'
        f' &nbsp;·&nbsp; Avg tenure: <b>{filt["Tenure_Years"].mean():.1f} years</b></div>',
        unsafe_allow_html=True)


# ══════════════════════════════════════════
# TAB 2 — SPENDING BEHAVIOR
# ══════════════════════════════════════════
with tab2:
    st.markdown('<div class="sec-header"><p class="sec-title">Spending Patterns</p>'
                '<p class="sec-sub">Category spend breakdown, segment profiles, and income/age spending relationships</p></div>',
                unsafe_allow_html=True)

    c1,c2 = st.columns(2, gap='large')
    with c1:
        cat_tot = {k: filt[v].sum() for k,v in SPEND_COLS.items()}
        cat_df  = pd.DataFrame({'Cat':list(cat_tot.keys()),'Tot':list(cat_tot.values())}).sort_values('Tot')
        pcts    = [v/sum(cat_tot.values())*100 for v in cat_df['Tot']]
        colors  = [SPEND_COLORS[c] for c in cat_df['Cat']]
        fig = go.Figure(go.Bar(
            x=cat_df['Tot'], y=cat_df['Cat'], orientation='h',
            marker_color=colors,
            marker_line_color='rgba(0,0,0,0.25)', marker_line_width=0.8,
            text=[f'${v:,.0f}  ({p:.1f}%)' for v,p in zip(cat_df['Tot'],pcts)],
            textposition='outside',
            textfont=dict(color=BLACK, size=11, family='DM Sans'),
            hovertemplate='<b>%{y}</b><br>$%{x:,.0f}<extra></extra>',
        ))
        fig.update_layout(xaxis_title='Total Spend ($)', yaxis_title='', showlegend=False,
                          xaxis_range=[0, cat_df['Tot'].max()*1.38])
        sf(fig, title='Total Spend by Category', h=False)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        seg_cat = (filt.groupby('Segment', observed=True)[list(SPEND_COLS.values())]
                   .mean().reset_index())
        seg_cat.columns = ['Segment'] + list(SPEND_COLS.keys())
        seg_melt = seg_cat.melt(id_vars='Segment', var_name='Category', value_name='Avg Spend')
        fig = px.bar(seg_melt, x='Category', y='Avg Spend', color='Segment',
                     barmode='group', color_discrete_map=SEG_COLORS)
        fig.update_traces(marker_line_color='rgba(0,0,0,0.25)', marker_line_width=0.8)
        fig.update_layout(xaxis_title='Category', yaxis_title='Avg Spend ($)',
                          yaxis_tickprefix='$')
        sf(fig, title='Avg Spend per Category by Segment', h=True)
        st.plotly_chart(fig, use_container_width=True)

    c3,c4 = st.columns(2, gap='large')
    with c3:
        age_sp = (filt.groupby('AgeGroup', observed=True)['TotalSpend']
                  .agg(['median','mean']).reset_index())
        age_sp.columns = ['AgeGroup','Median','Mean']
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=age_sp['AgeGroup'], y=age_sp['Median'], mode='lines+markers', name='Median',
            line=dict(color=C_BLUE, width=2.5),
            marker=dict(size=9, color=C_BLUE, line=dict(color='#FFFFFF', width=1.5)),
            fill='tozeroy', fillcolor=hex_rgba(C_BLUE, 0.07),
            hovertemplate='<b>%{x}</b><br>Median: $%{y:,.0f}<extra></extra>',
        ))
        fig.add_trace(go.Scatter(
            x=age_sp['AgeGroup'], y=age_sp['Mean'], mode='lines+markers', name='Mean',
            line=dict(color=C_TEAL, width=2, dash='dot'),
            marker=dict(size=8, color=C_TEAL, line=dict(color='#FFFFFF', width=1.5)),
            hovertemplate='<b>%{x}</b><br>Mean: $%{y:,.0f}<extra></extra>',
        ))
        fig.update_layout(xaxis_title='Age Group', yaxis_title='Spend ($)', yaxis_tickprefix='$')
        sf(fig, title='Spend Trend by Age Group', h=True)
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        inc_seg = (filt.groupby(['IncomeBand','Segment'], observed=True)['TotalSpend']
                   .mean().reset_index())
        inc_seg.columns = ['Income Band','Segment','Avg Spend']
        fig = px.bar(inc_seg, x='Income Band', y='Avg Spend', color='Segment',
                     barmode='group', color_discrete_map=SEG_COLORS)
        fig.update_traces(marker_line_color='rgba(0,0,0,0.25)', marker_line_width=0.8)
        fig.update_layout(xaxis_title='Income Band', yaxis_title='Avg Spend ($)', yaxis_tickprefix='$')
        sf(fig, title='Avg Spend: Income Band by Segment', h=True)
        st.plotly_chart(fig, use_container_width=True)

    age_cat = filt.groupby('AgeGroup', observed=True)[list(SPEND_COLS.values())].mean()
    age_cat.columns = list(SPEND_COLS.keys())
    fig = px.imshow(age_cat,
                    color_continuous_scale=HEATMAP_WARM,
                    text_auto='.0f', aspect='auto')
    heatmap(fig, title='Avg Spend per Category by Age Group', height=260, lmargin=80)
    fig.update_layout(xaxis_title='Spend Category', yaxis_title='Age Group')
    st.plotly_chart(fig, use_container_width=True)

    top_cat = max(cat_tot, key=cat_tot.get)
    hi = filt[filt['Segment']=='High value']['TotalSpend']
    lo = filt[filt['Segment']=='Low value']['TotalSpend']
    lo_mean = lo.mean() if len(lo) > 0 else 1
    st.markdown(
        f'<div class="insight-box"><b>Key Insight:</b> <b>{top_cat}</b> is the dominant category'
        f' &nbsp;·&nbsp; High-value customers spend <b>${hi.mean():,.0f}</b> avg'
        f' vs <b>${lo_mean:,.0f}</b> for low-value — a <b>{hi.mean()/lo_mean:.1f}x</b> gap</div>',
        unsafe_allow_html=True)


# ══════════════════════════════════════════
# TAB 3 — CAMPAIGNS
# ══════════════════════════════════════════
with tab3:
    st.markdown('<div class="sec-header"><p class="sec-title">Campaign Performance</p>'
                '<p class="sec-sub">Acceptance rates by campaign, education, complaint status and customer tenure</p></div>',
                unsafe_allow_html=True)

    accept_rates = {k: filt[v].mean()*100 for k,v in CAMPS.items()}
    c1,c2 = st.columns(2, gap='large')

    with c1:
        cmp_df = (pd.DataFrame(list(accept_rates.items()),columns=['Campaign','Rate'])
                  .sort_values('Rate',ascending=False))
        max_r, min_r = cmp_df['Rate'].max(), cmp_df['Rate'].min()
        bc = [C_GREEN if r==max_r else (C_RED if r==min_r else C_TEAL) for r in cmp_df['Rate']]
        fig = go.Figure(go.Bar(
            x=cmp_df['Campaign'], y=cmp_df['Rate'],
            marker_color=bc,
            marker_line_color='rgba(0,0,0,0.25)', marker_line_width=0.8,
            text=[f'{r:.1f}%' for r in cmp_df['Rate']], textposition='outside',
            textfont=dict(color=BLACK, size=11, family='DM Sans'),
            hovertemplate='<b>%{x}</b><br>Acceptance: %{y:.1f}%<extra></extra>',
        ))
        fig.update_layout(yaxis_title='Acceptance Rate (%)', xaxis_title='',
                          showlegend=False, yaxis_range=[0, cmp_df['Rate'].max()*1.3])
        sf(fig, title='Acceptance Rate by Campaign', h=False)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        heat_df = filt.groupby('Education')[list(CAMPS.values())].mean()*100
        heat_df.columns = list(CAMPS.keys())
        fig = px.imshow(heat_df,
                        color_continuous_scale=HEATMAP_CORAL,
                        text_auto='.1f', aspect='auto')
        heatmap(fig, title='Acceptance Rate (%) — Education by Campaign')
        st.plotly_chart(fig, use_container_width=True)

    c3,c4 = st.columns(2, gap='large')
    with c3:
        f2 = filt.copy()
        f2['NumAcc'] = f2[list(CAMPS.values())].sum(axis=1)
        acc_seg = f2.groupby(['Segment','NumAcc'],observed=True).size().reset_index(name='Count')
        fig = px.bar(acc_seg, x='NumAcc', y='Count', color='Segment',
                     barmode='stack', color_discrete_map=SEG_COLORS,
                     labels={'NumAcc':'Campaigns Accepted','Count':'Customers'})
        fig.update_traces(marker_line_color='rgba(0,0,0,0.25)', marker_line_width=0.8)
        sf(fig, title='Campaigns Accepted by Segment', h=True)
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        f3 = filt.copy()
        f3['TenBin'] = pd.cut(f3['Tenure_Years'], bins=[0,1,2,3,4,5,20],
                              labels=['<1yr','1-2yr','2-3yr','3-4yr','4-5yr','5yr+'])
        ten_acc = (f3.groupby('TenBin', observed=True)[list(CAMPS.values())].mean()*100).reset_index()
        ten_acc = ten_acc.set_index('TenBin')
        ten_acc.columns = list(CAMPS.keys())
        fig = px.imshow(
            ten_acc,
            color_continuous_scale=HEATMAP_WARM,
            text_auto='.1f', aspect='auto',
            labels=dict(x='Campaign', y='Tenure', color='Accept %'),
        )
        heatmap(fig, title='Campaign Acceptance (%) by Tenure', height=340, lmargin=70)
        st.plotly_chart(fig, use_container_width=True)

    comp_df = filt.groupby('Complain')[list(CAMPS.values())].mean()*100
    comp_df.index = comp_df.index.map({0:'No Complaint',1:'Complained'})
    comp_df.columns = list(CAMPS.keys())
    comp_m = comp_df.reset_index().melt(id_vars='Complain', var_name='Campaign', value_name='Rate (%)')
    fig = px.bar(comp_m, x='Campaign', y='Rate (%)', color='Complain', barmode='group',
                 color_discrete_map={'No Complaint':C_TEAL,'Complained':C_RED})
    fig.update_traces(marker_line_color='rgba(0,0,0,0.25)', marker_line_width=0.8)
    sf(fig, title='Campaign Acceptance — Complaint vs No Complaint', h=True, height=300)
    st.plotly_chart(fig, use_container_width=True)

    best_c  = max(accept_rates, key=accept_rates.get)
    worst_c = min(accept_rates, key=accept_rates.get)
    st.markdown(
        f'<div class="insight-box"><b>Key Insight:</b> <b>{best_c}</b> achieved the highest acceptance'
        f' at <b>{accept_rates[best_c]:.1f}%</b> &nbsp;·&nbsp; <b>{worst_c}</b> was weakest at'
        f' <b>{accept_rates[worst_c]:.1f}%</b> — review targeting and messaging</div>',
        unsafe_allow_html=True)


# ══════════════════════════════════════════
# TAB 4 — CHANNELS
# ══════════════════════════════════════════
with tab4:
    st.markdown('<div class="sec-header"><p class="sec-title">Purchase Channels</p>'
                '<p class="sec-sub">Channel share, deal dependency, web conversion and tenure patterns</p></div>',
                unsafe_allow_html=True)

    ch_tot = {'Web':filt['NumWebPurchases'].sum(),'Store':filt['NumStorePurchases'].sum(),
              'Catalog':filt['NumCatalogPurchases'].sum(),'Deals':filt['NumDealsPurchases'].sum()}

    c1,c2 = st.columns(2, gap='large')
    with c1:
        fig = px.pie(values=list(ch_tot.values()), names=list(ch_tot.keys()), hole=0.55,
                     color_discrete_sequence=[C_BLUE,C_TEAL,C_AMBER,C_PURPLE])
        donut(fig, title='Purchase Channel Share')
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        ch_seg = filt.groupby('Segment',observed=True)[
            ['NumWebPurchases','NumStorePurchases','NumCatalogPurchases','NumDealsPurchases']
        ].mean().reset_index()
        ch_seg.columns = ['Segment','Web','Store','Catalog','Deals']
        ch_m = ch_seg.melt(id_vars='Segment', var_name='Channel', value_name='Avg')
        fig  = px.bar(ch_m, x='Avg', y='Channel', color='Segment', barmode='group',
                      orientation='h', color_discrete_map=SEG_COLORS)
        fig.update_traces(marker_line_color='rgba(0,0,0,0.25)', marker_line_width=0.8)
        sf(fig, title='Avg Purchases by Channel and Segment', h=True)
        st.plotly_chart(fig, use_container_width=True)

    c3,c4 = st.columns(2, gap='large')
    with c3:
        fig = go.Figure()
        for seg, color in SEG_COLORS.items():
            sub = filt[filt['Segment']==seg]['DealDependency'].dropna()
            if sub.empty: continue
            fig.add_trace(go.Box(
                y=sub, name=seg,
                boxpoints='outliers',
                marker_color=color,
                marker=dict(size=4, color=color, line=dict(color='#FFFFFF', width=1)),
                line=dict(color=color, width=2),
                fillcolor=hex_rgba(color, 0.35),
                boxmean=True,
                whiskerwidth=0.5,
                hovertemplate='<b>%{x}</b><br>Value: %{y:.1f}%<extra></extra>',
            ))
        fig.update_layout(yaxis_title='Deal Dependency (%)', showlegend=True,
                          xaxis_title='Customer Segment')
        sf(fig, title='Deal Dependency Distribution by Segment', h=True)
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        wv = filt.copy()
        wv['VisitBin'] = pd.cut(wv['NumWebVisitsMonth'], bins=[0,2,4,6,8,20],
                                labels=['0-2','3-4','5-6','7-8','9+'])
        wv_g = wv.groupby(['VisitBin','Segment'],observed=True)['NumWebPurchases'].mean().reset_index()
        fig = px.line(wv_g, x='VisitBin', y='NumWebPurchases', color='Segment',
                      markers=True, color_discrete_map=SEG_COLORS)
        fig.update_traces(
            marker=dict(size=8, line=dict(color='#FFFFFF', width=1.5)),
            line=dict(width=2.5),
        )
        fig.update_layout(xaxis_title='Web Visits / Month', yaxis_title='Avg Web Purchases')
        sf(fig, title='Web Purchases vs Visit Frequency', h=True)
        st.plotly_chart(fig, use_container_width=True)

    f_t = filt.copy()
    f_t['TenBin'] = pd.cut(f_t['Tenure_Years'], bins=[0,1,2,3,4,5,20],
                           labels=['<1yr','1-2yr','2-3yr','3-4yr','4-5yr','5yr+'])
    ten_ch = f_t.groupby('TenBin',observed=True)[
        ['NumWebPurchases','NumStorePurchases','NumCatalogPurchases']
    ].mean().reset_index()
    ten_ch.columns = ['Tenure','Web','Store','Catalog']
    ten_m = ten_ch.melt(id_vars='Tenure', var_name='Channel', value_name='Avg')

    fig = go.Figure()
    ch_color_map = {'Web': C_BLUE, 'Store': C_TEAL, 'Catalog': C_AMBER}
    for ch, color in ch_color_map.items():
        sub = ten_m[ten_m['Channel']==ch]
        fig.add_trace(go.Bar(
            x=sub['Tenure'], y=sub['Avg'], name=ch,
            marker_color=color,
            marker_line_color='rgba(0,0,0,0.25)', marker_line_width=0.8,
            hovertemplate=f'<b>{ch}</b><br>Tenure: %{{x}}<br>Avg: %{{y:.2f}}<extra></extra>',
        ))
    fig.update_layout(barmode='group', xaxis_title='Customer Tenure', yaxis_title='Avg Purchases')
    sf(fig, title='Channel Purchases by Customer Tenure', h=True, height=300)
    st.plotly_chart(fig, use_container_width=True)

    top_ch  = max(ch_tot, key=ch_tot.get)
    hi_deal = (filt['DealDependency']>50).mean()*100
    st.markdown(
        f'<div class="insight-box"><b>Key Insight:</b> <b>{top_ch}</b> is the dominant channel'
        f' &nbsp;·&nbsp; <b>{hi_deal:.0f}%</b> of customers source over 50% of purchases via deals —'
        f' high deal dependency can erode margins</div>', unsafe_allow_html=True)


# ══════════════════════════════════════════
# TAB 5 — ROI & SEGMENTS
# ══════════════════════════════════════════
with tab5:
    st.markdown('<div class="sec-header"><p class="sec-title">ROI and Segmentation</p>'
                '<p class="sec-sub">Marketing return by segment, income band, tenure — identify where to invest</p></div>',
                unsafe_allow_html=True)

    roi_seg = filt.groupby('Segment',observed=True)['ROI'].mean().reset_index()
    c1,c2   = st.columns(2, gap='large')

    with c1:
        roi_cols = [C_GREEN if v>=0 else C_RED for v in roi_seg['ROI']]
        fig = go.Figure(go.Bar(
            x=roi_seg['Segment'], y=roi_seg['ROI'],
            marker_color=roi_cols,
            marker_line_color='rgba(0,0,0,0.25)', marker_line_width=0.8,
            text=[f'${v:,.1f}' for v in roi_seg['ROI']], textposition='outside',
            textfont=dict(color=BLACK, size=11, family='DM Sans'),
            hovertemplate='<b>%{x}</b><br>Avg ROI: $%{y:,.1f}<extra></extra>',
        ))
        fig.add_hline(y=0, line_dash='dot', line_color='#475569', line_width=1.8,
                      annotation_text='Break-even',
                      annotation_font_color=BLACK, annotation_font_size=11)
        fig.update_layout(yaxis_title='Avg ROI ($)', xaxis_title='',
                          showlegend=False, yaxis_tickprefix='$')
        sf(fig, title='Avg ROI by Segment', h=False)
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        roi_inc = (filt.groupby('IncomeBand',observed=True)
                   .agg(Avg_ROI=('ROI','mean'), Count=('ROI','count'), Avg_Inc=('Income','mean'))
                   .reset_index())
        roi_inc.columns = ['Band','ROI','Count','Income']
        p_colors = [C_GREEN if v>=0 else C_RED for v in roi_inc['ROI']]
        fig = go.Figure(go.Scatter(
            x=roi_inc['Income'], y=roi_inc['ROI'], mode='markers+text',
            text=roi_inc['Band'], textposition='top center',
            textfont=dict(color=BLACK, size=11, family='DM Sans'),
            marker=dict(
                size=[max(c/roi_inc['Count'].max()*50+18, 18) for c in roi_inc['Count']],
                color=p_colors, line=dict(color='#FFFFFF', width=1.5), opacity=0.85,
            ),
        ))
        fig.add_hline(y=0, line_dash='dot', line_color='#475569', line_width=1.8,
                      annotation_text='Break-even',
                      annotation_font_color=BLACK, annotation_font_size=11)
        fig.update_layout(xaxis_title='Avg Annual Income ($)', yaxis_title='Avg ROI ($)',
                          showlegend=False, xaxis_tickprefix='$', yaxis_tickprefix='$')
        sf(fig, title='ROI vs Income Band (bubble = customer count)', h=False)
        st.plotly_chart(fig, use_container_width=True)

    c3,c4 = st.columns(2, gap='large')
    with c3:
        roi_bins = pd.cut(filt['ROI'], bins=[-9999, -20, -10, 0, 10, 20, 9999],
                          labels=['<-$20','-$20 to -$10','-$10 to $0','$0 to $10','$10 to $20','>$20'])
        roi_dist = filt.copy()
        roi_dist['ROI_Bin'] = roi_bins
        roi_grp = roi_dist.groupby(['ROI_Bin','Segment'],observed=True).size().reset_index(name='Count')
        fig = px.bar(roi_grp, x='ROI_Bin', y='Count', color='Segment',
                     barmode='group', color_discrete_map=SEG_COLORS,
                     labels={'ROI_Bin':'ROI Range ($)', 'Count':'Customers'})
        fig.update_traces(marker_line_color='rgba(0,0,0,0.25)', marker_line_width=0.8)
        fig.add_vline(x=2.5, line_dash='dash', line_color='#475569', line_width=1.8,
                      annotation_text='Break-even',
                      annotation_font_color=BLACK, annotation_font_size=11)
        sf(fig, title='ROI Distribution by Segment', h=True)
        st.plotly_chart(fig, use_container_width=True)

    with c4:
        f4 = filt.copy()
        f4['PosROI'] = (f4['ROI'] > 0).astype(int)
        f4['TenBin'] = pd.cut(f4['Tenure_Years'], bins=[0,1,2,3,4,5,20],
                              labels=['<1yr','1-2yr','2-3yr','3-4yr','4-5yr','5yr+'])
        ten_roi_pivot = (
            f4.groupby(['TenBin','Segment'], observed=True)['PosROI']
            .mean() * 100
        ).unstack('Segment').fillna(0)
        col_order = [c for c in ['Low value','Mid value','High value'] if c in ten_roi_pivot.columns]
        ten_roi_pivot = ten_roi_pivot[col_order]

        fig = go.Figure()
        for seg in col_order:
            color = SEG_COLORS[seg]
            fig.add_trace(go.Bar(
                name=seg,
                x=ten_roi_pivot.index.astype(str),
                y=ten_roi_pivot[seg],
                marker_color=color,
                marker_line_color='rgba(0,0,0,0.25)',
                marker_line_width=0.8,
                text=[f'{v:.0f}%' for v in ten_roi_pivot[seg]],
                textposition='inside',
                textfont=dict(color='#FFFFFF', size=10, family='DM Sans'),
                hovertemplate=f'<b>{seg}</b><br>Tenure: %{{x}}<br>Pos ROI: %{{y:.1f}}%<extra></extra>',
            ))
        fig.update_layout(
            barmode='group',
            xaxis_title='Customer Tenure',
            yaxis_title='% Customers with Positive ROI',
            yaxis_range=[0, 115],
        )
        sf(fig, title='Positive-ROI Customers by Tenure & Segment', h=True)
        st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="sec-header" style="margin-top:20px;"><p class="sec-title">Segment Summary</p>'
                '<p class="sec-sub">Key metrics across all customer segments</p></div>',
                unsafe_allow_html=True)

    seg_tbl = (filt.groupby('Segment',observed=True).agg(
        Customers   =('ID','count'),
        Avg_Income  =('Income','mean'),
        Avg_Spend   =('TotalSpend','mean'),
        Avg_ROI     =('ROI','mean'),
        Accept_Rate =('TotalAccepted', lambda x:(x>0).mean()*100),
        Pos_ROI_Pct =('ROI', lambda x:(x>0).mean()*100),
        Deal_Dep    =('DealDependency','mean'),
    ).reset_index()
    .round({'Avg_Income':0,'Avg_Spend':0,'Avg_ROI':1,'Accept_Rate':1,'Pos_ROI_Pct':1,'Deal_Dep':1}))
    seg_tbl.columns = ['Segment','Customers','Avg Income ($)','Avg Spend ($)',
                       'Avg ROI ($)','Accept Rate (%)','% Positive ROI','Deal Dep (%)']

    st.dataframe(seg_tbl, use_container_width=True, hide_index=True,
        column_config={
            'Segment'        : st.column_config.TextColumn('Segment', width='medium'),
            'Customers'      : st.column_config.NumberColumn('Customers', format='%d'),
            'Avg Income ($)' : st.column_config.NumberColumn('Avg Income', format='$%d'),
            'Avg Spend ($)'  : st.column_config.NumberColumn('Avg Spend', format='$%d'),
            'Avg ROI ($)'    : st.column_config.NumberColumn('Avg ROI', format='$%.1f'),
            'Accept Rate (%)': st.column_config.ProgressColumn('Accept Rate',format='%.1f%%',min_value=0,max_value=100),
            '% Positive ROI' : st.column_config.ProgressColumn('% Pos ROI', format='%.1f%%',min_value=0,max_value=100),
            'Deal Dep (%)'   : st.column_config.ProgressColumn('Deal Dep.',  format='%.1f%%',min_value=0,max_value=100),
        })

    st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)
    dl_col,_ = st.columns([1,4])
    with dl_col:
        st.download_button("Download Filtered Data", data=filt.to_csv(index=False),
                           file_name='filtered_customers.csv', mime='text/csv')

    best_s  = roi_seg.loc[roi_seg['ROI'].idxmax(),'Segment'] if not roi_seg.empty else 'N/A'
    best_v  = roi_seg['ROI'].max() if not roi_seg.empty else 0
    neg_pct = (filt['ROI']<0).mean()*100
    st.markdown(
        f'<div class="insight-box"><b>Key Insight:</b> <b>{best_s}</b> delivers best avg ROI'
        f' of <b>${best_v:,.1f}</b> &nbsp;·&nbsp; <b>{neg_pct:.0f}%</b> of customers have negative ROI —'
        f' prioritise high-value, low-deal-dependency customers for maximum return</div>',
        unsafe_allow_html=True)
