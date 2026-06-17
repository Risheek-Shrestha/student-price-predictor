import streamlit as st
import plotly.graph_objects as go
import requests
import os

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Student Performance Analytics",
    page_icon="🎓",
    layout="wide"
)

# ==========================================
# SESSION STATE
# ==========================================

if "predicted" not in st.session_state:
    st.session_state.predicted = False

if "prediction_data" not in st.session_state:
    st.session_state.prediction_data = {}

if "page" not in st.session_state:
    st.session_state.page = "Home"

# ==========================================
# CSS — PREMIUM ENTERPRISE OBSIDIAN THEME
# ==========================================

st.markdown("""
<style>

/* Seamlessly hide default Streamlit branding and spacing overhead */
header[data-testid="stHeader"], [data-testid="stHeader"] {
    display: none !important;
    visibility: hidden !important;
    height: 0 !important;
}
#MainMenu {display: none !important;}
footer {display: none !important;}

/* Global Canvas Styling — Dark Mode Aesthetic */
html, body, .stApp {
    background: #090d16 !important;
    color: #f8fafc !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    font-size: 16px !important;
}

/* SIDEBAR — Obsidian Pro Navigation Panel */
section[data-testid="stSidebar"] {
    display: block !important;
    width: 290px !important;
    visibility: visible !important;
    background: #05070c !important;
    border-right: 1px solid #1e293b !important;
}

section[data-testid="stSidebar"] > div {
    display: block !important;
    visibility: visible !important;
    width: 100% !important;
    background: #05070c !important;
}

section[data-testid="stSidebar"] * {
    color: #94a3b8 !important;
    visibility: visible !important;
}

section[data-testid="stSidebar"] strong { 
    color: #ffffff !important; 
}

section[data-testid="stSidebar"] a { 
    color: #6366f1 !important; 
    text-decoration: none; 
    transition: color 0.15s ease;
}

section[data-testid="stSidebar"] a:hover { 
    color: #818cf8 !important; 
}

/* Sidebar Tab Buttons — SaaS Application Layout */
section[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    color: #94a3b8 !important;
    border: 1px solid transparent !important;
    border-radius: 8px !important;
    padding: 12px 16px !important;
    font-size: 0.92rem !important;
    font-weight: 500 !important;
    text-align: left !important;
    width: 100% !important;
    transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
    margin-bottom: 6px !important;
}
            
section[data-testid="stSidebar"] .stButton > button:hover {
    background: #111726 !important;
    color: #ffffff !important;
    border-left: 3px solid #6366f1 !important;
    border-radius: 0px 8px 8px 0px !important;
    padding-left: 13px !important;
}

/* Main Layout Centering and Margins */
.block-container {
    padding: 2.5rem 3.5rem 4rem !important;
    max-width: 1250px !important;
    margin: 0 auto !important;
}

[data-testid="stAppViewBlockContainer"] {
    padding-top: 1.5rem !important;
}

/* Clean Dashboard Header Blocks */
.page-header {
    margin-bottom: 2.25rem;
    padding-bottom: 1.25rem;
    border-bottom: 1px solid #1e293b;
}

.page-header-left h2 {
    font-size: 1.85rem;
    font-weight: 700;
    color: #ffffff;
    letter-spacing: -0.02em;
    margin: 0 0 6px 0;
}

.page-header-left p {
    font-size: 1rem;
    color: #94a3b8;
    margin: 0;
}

/* Elite Glassmorphism KPI Display Grid */
.kpi-container {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 2.5rem;
}

.kpi-card {
    background: #111726;
    padding: 22px;
    border-radius: 12px;
    border: 1px solid #1e293b;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
    transition: border-color 0.2s ease;
}

.kpi-card:hover {
    border-color: #334155;
}

.kpi-label {
    font-size: 0.75rem;
    font-weight: 600;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 8px;
}

.kpi-value {
    font-size: 2.1rem;
    font-weight: 700;
    color: #ffffff;
    line-height: 1.1;
}

.kpi-sub {
    font-size: 0.85rem;
    color: #94a3b8;
    margin-top: 6px;
}

/* Feature & Architecture Grid Informational Cards */
.content-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 18px;
    margin-bottom: 2rem;
}

.content-card {
    background: #111726;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    transition: transform 0.2s ease, border-color 0.2s ease;
}

.content-card:hover {
    transform: translateY(-2px);
    border-color: #4f46e5;
}

.content-card-icon {
    width: 42px;
    height: 42px;
    border-radius: 10px;
    background: #1e1b4b;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
    margin-bottom: 16px;
}

.content-card-title {
    font-size: 1.15rem;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 8px;
}

.content-card-desc {
    font-size: 0.95rem;
    color: #94a3b8;
    line-height: 1.65;
}

/* Dynamic Section Labels */
.section-label {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #818cf8;
    margin: 2.5rem 0 1.25rem 0;
}

/* Premium Uniform Data Ledger (Model Table) */
.model-table {
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    background: #111726;
    border: 1px solid #1e293b;
    border-radius: 12px;
    overflow: hidden;
    margin-bottom: 2rem;
}

.model-table th {
    background: #0d1321;
    padding: 16px 20px;
    text-align: left;
    font-size: 0.78rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: #94a3b8;
    border-bottom: 1px solid #1e293b;
}

.model-table td {
    padding: 16px 20px;
    border-bottom: 1px solid #1e293b;
    color: #cbd5e1;
    font-size: 0.95rem;
}

.model-table tr:last-child td { border-bottom: none; }
.model-table tr.best-row td { background: #1a1e2e; font-weight: 600; color: #ffffff; }

.pill {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
}

.pill-green { background: #064e3b; border: 1px solid #047857; color: #34d399; }
.pill-amber { background: #78350f; border: 1px solid #b45309; color: #fbbf24; }
.pill-blue  { background: #1e1b4b; border: 1px solid #3730a3; color: #818cf8; }
.pill-red   { background: #7f1d1d; border: 1px solid #b91c1c; color: #f87171; }

/* Interactive Form Parameter Headers */
.form-group-label {
    font-size: 0.8rem !important;
    font-weight: 700 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.06em !important;
    color: #818cf8 !important;
    margin: 0 0 1.2rem 0 !important;
}

.form-divider {
    height: 1px;
    background: #1e293b;
    margin: 1.75rem 0;
}

/* =======================================================
   CRITICAL REQUIREMENT: PRESERVE AND ENHANCE DROPDOWN CARETS
   ======================================================= */
div[data-baseweb="select"] > div {
    background: #111726 !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
    color: #ffffff !important;
}

div[data-baseweb="select"] [data-testid="stSelectboxDiv"] span,
div[data-baseweb="select"] span {
    color: #ffffff !important;
}

/* Force carets/dropdown signs to remain fully visible and contrast-heavy */
div[data-baseweb="select"] svg {
    display: block !important;
    visibility: visible !important;
    opacity: 1 !important;
    fill: #818cf8 !important;
    width: 20px !important;
    height: 20px !important;
}

/* Dropdown Menu Overlay Overrides */
div[data-baseweb="popover"],
div[data-baseweb="popover"] > div,
ul[role="listbox"],
div[role="listbox"] {
    background: #111726 !important;
    background-color: #111726 !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
}

li[role="option"],
div[role="option"] {
    background: #111726 !important;
    color: #cbd5e1 !important;
}

li[role="option"]:hover,
div[role="option"]:hover {
    background: #4f46e5 !important;
    color: #ffffff !important;
}

li[aria-selected="true"],
div[aria-selected="true"] {
    background: #1e1b4b !important;
    color: #818cf8 !important;
    font-weight: 600 !important;
}

label { 
    color: #cbd5e1 !important; 
    font-size: 0.95rem !important; 
    font-weight: 500 !important; 
}

/* Streamlit Native Sliders Layout Adjustments for Dark Mode */
div[data-testid="stSlider"] * {
    color: #cbd5e1 !important;
}

/* Execution Performance Output Banner Card */
.result-hero {
    background: #111726;
    border: 1px solid #1e293b;
    border-radius: 16px;
    overflow: hidden;
    box-shadow: 0 10px 25px -5px rgba(0,0,0,0.3);
    margin-bottom: 2rem;
}

.result-hero-top {
    background: linear-gradient(135deg, #1e1b4b 0%, #0f172a 100%);
    padding: 36px;
    display: flex;
    align-items: center;
    gap: 32px;
    border-bottom: 1px solid #1e293b;
}

.result-grade-num {
    font-size: 5.5rem;
    font-weight: 800;
    color: #ffffff;
    line-height: 1;
    letter-spacing: -0.04em;
    text-shadow: 0 0 20px rgba(99, 102, 241, 0.3);
}

.result-hero-meta { flex: 1; }

.result-hero-title {
    font-size: 1.35rem;
    font-weight: 600;
    color: #ffffff;
    margin-bottom: 6px;
}

.result-hero-sub {
    font-size: 0.95rem;
    color: #94a3b8;
    margin-bottom: 16px;
}

.result-badges {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
}

.badge-light { 
    padding: 6px 14px; 
    border-radius: 20px; 
    font-size: 0.78rem; 
    font-weight: 600;
    background: rgba(255,255,255,0.06); 
    color: #f8fafc; 
    border: 1px solid rgba(255,255,255,0.12); 
}

.result-hero-bottom {
    padding: 22px 36px;
    background: #0d1321;
    font-size: 0.98rem;
    color: #cbd5e1;
    line-height: 1.65;
}

/* High-End Micro Progress Loaders */
.progress-wrap {
    background: #1e293b;
    border-radius: 10px;
    height: 8px;
    overflow: hidden;
}

.progress-fill {
    height: 100%;
    border-radius: 10px;
    background: linear-gradient(90deg, #6366f1, #818cf8);
    box-shadow: 0 0 8px rgba(99, 102, 241, 0.5);
}

/* Micro Grid Metrics Summary Dashboard */
.summary-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 14px;
    margin-bottom: 2rem;
}

.summary-item {
    background: #111726;
    border: 1px solid #1e293b;
    border-radius: 10px;
    padding: 16px 20px;
}

.summary-item-label {
    font-size: 0.75rem;
    color: #64748b;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 6px;
    font-weight: 600;
}

.summary-item-value { 
    font-size: 1.1rem; 
    font-weight: 600; 
    color: #ffffff; 
}

/* System Action Banner Blocks */
.verdict-banner {
    background: #111726;
    border: 1px solid #1e293b;
    border-left: 4px solid #6366f1;
    border-radius: 0 12px 12px 0;
    padding: 22px;
    font-size: 0.98rem;
    line-height: 1.7;
    color: #cbd5e1;
    margin-bottom: 2.5rem;
}

/* Core Interface Call-To-Action Primary Button */
.stButton > button {
    background: #4f46e5 !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 12px 24px !important;
    font-size: 0.92rem !important;
    font-weight: 600 !important;
    width: 100% !important;
    transition: all 0.15s ease !important;
    box-shadow: 0 4px 12px rgba(79, 70, 229, 0.2) !important;
}

.stButton > button:hover { 
    background: #4338ca !important; 
    box-shadow: 0 6px 16px rgba(79, 70, 229, 0.35) !important;
}

hr { border-color: #1e293b !important; margin: 2rem 0 !important; }

/* Responsive Media Controls */
@media (max-width: 992px) {
    .kpi-container { grid-template-columns: repeat(2, 1fr); }
    .content-grid { grid-template-columns: 1fr; }
    .summary-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 576px) {
    .kpi-container { grid-template-columns: 1fr; }
    .summary-grid { grid-template-columns: 1fr; }
    .block-container { padding: 1.5rem 1.5rem 3rem !important; }
    .result-hero-top { flex-direction: column; align-items: flex-start; gap: 20px; }
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR
# ==========================================

with st.sidebar:
    st.markdown("""
    <div style="padding: 26px 20px 20px;">
        <div style="font-size:1.15rem; font-weight:700; color:#ffffff; margin-bottom:4px; letter-spacing:-0.01em;">🎓 Grade Predictor</div>
        <div style="font-size:0.75rem; color:#475569; letter-spacing:0.3px;">UCI Student Performance Dataset</div>
    </div>
    <div style="height:1px; background:#1e293b; margin:0 20px 18px;"></div>
    <div style="font-size:0.7rem; font-weight:700; color:#475569; text-transform:uppercase; letter-spacing:0.08em; padding: 0 20px 10px;">Navigation</div>
    """, unsafe_allow_html=True)

    if st.button("🏠   Home Overview"):
        st.session_state.page = "Home"
        st.session_state.predicted = False
        st.rerun()

    if st.button("🔮   Predict Performance"):
        st.session_state.page = "Predict"
        st.session_state.predicted = False
        st.rerun()

    if st.button("📊   Model Performance Comparison"):
        st.session_state.page = "Model Comparison"
        st.rerun()

    st.markdown("""
    <div style="height:1px; background:#1e293b; margin:24px 20px 18px;"></div>
    <div style="padding: 0 20px;">
        <div style="font-size:0.7rem; font-weight:700; color:#475569; text-transform:uppercase; letter-spacing:0.08em; margin-bottom:14px;">Active Engine</div>
        <div style="background:#111726; border:1px solid #1e293b; border-radius:10px; padding:16px;">
            <div style="font-size:0.85rem; color:#ffffff; font-weight:600; margin-bottom:12px;">🌲 Random Forest</div>
            <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                <span style="font-size:0.78rem; color:#94a3b8;">R² Validation</span>
                <span style="font-size:0.78rem; color:#34d399; font-weight:600;">0.83</span>
            </div>
            <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
                <span style="font-size:0.78rem; color:#94a3b8;">MAE Margin</span>
                <span style="font-size:0.78rem; color:#ffffff; font-weight:600;">1.11</span>
            </div>
            <div style="display:flex; justify-content:space-between;">
                <span style="font-size:0.78rem; color:#94a3b8;">Train N</span>
                <span style="font-size:0.78rem; color:#ffffff; font-weight:600;">395 rows</span>
            </div>
        </div>
    </div>
    <div style="height:1px; background:#1e293b; margin:24px 20px 18px;"></div>
    <div style="padding: 0 20px 24px;">
        <div style="font-size:0.78rem; color:#475569;">
            Engineer: <strong style="color:#94a3b8;">Risheek Shrestha</strong><br>
            <a href="https://github.com/Risheek-Shrestha/student-price-predictor">Repository Index ↗</a>
        </div>
    </div>
    """, unsafe_allow_html=True)

page = st.session_state.page

# ==========================================
# PAGE: HOME
# ==========================================

if page == "Home":

    st.markdown("""
    <div class="page-header">
        <div class="page-header-left">
            <h2>Student Performance Analytics</h2>
            <p>Predict secondary education test outcomes via core tracking models engineered on environmental and historic metrics.</p>
        </div>
    </div>
    <div class="kpi-container">
        <div class="kpi-card">
            <div class="kpi-label">R² Score Metric</div>
            <div class="kpi-value">0.83</div>
            <div class="kpi-sub">Variance explanation</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Mean Abs. Error</div>
            <div class="kpi-value">1.11</div>
            <div class="kpi-sub">Error scale out of 20</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Training Profile</div>
            <div class="kpi-value">395</div>
            <div class="kpi-sub">Validated samples</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Tracked Vectors</div>
            <div class="kpi-value">6</div>
            <div class="kpi-sub">Academic & Social features</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">System Architecture & Pipeline Blueprint</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="content-grid">
        <div class="content-card">
            <div class="content-card-icon">🎯</div>
            <div class="content-card-title">Core Objective</div>
            <div class="content-card-desc">Calculates student final metrics (G3 out of 20 points) leveraging supervised forest models optimized for regional secondary education frameworks.</div>
        </div>
        <div class="content-card">
            <div class="content-card-icon">📥</div>
            <div class="content-card-title">Feature Engineering</div>
            <div class="content-card-desc">Ingests sequential historical records (G1/G2 tiers), cumulative periodic testing records, temporal study distributions, and localized social indicators.</div>
        </div>
        <div class="content-card">
            <div class="content-card-icon">⚙️</div>
            <div class="content-card-title">Asynchronous Integration</div>
            <div class="content-card-desc">The localized Streamlit layout safely coordinates calculations with an isolated Django REST API engine, returning structured payload matrices instantly.</div>
        </div>
        <div class="content-card">
            <div class="content-card-icon">📊</div>
            <div class="content-card-title">Model Diagnostics</div>
            <div class="content-card-desc">Our baseline Random Forest implementation limits noise amplification, outperforming heavily regularized alternatives on small enterprise rows.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">Exploratory Sample Distributions</div>', unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns(3)

    # Cohesive dark adjustments for Plotly layouts
    with col_a:
        fig_dist = go.Figure()
        fig_dist.add_trace(go.Histogram(
            x=[8,9,10,10,11,11,11,12,12,12,13,13,13,13,14,14,14,15,15,16,16,17,18],
            nbinsx=12,
            marker_color="#4f46e5",
        ))
        fig_dist.update_layout(
            title=dict(text="G3 Density Frequency", font=dict(size=12, color="#94a3b8", weight="bold"), x=0),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            height=200, margin=dict(t=40, b=20, l=10, r=10),
            font=dict(color="#94a3b8", size=11, family="Inter"),
            xaxis=dict(showgrid=False, tickfont=dict(color="#64748b")),
            yaxis=dict(gridcolor="#1e293b", tickfont=dict(color="#64748b"))
        )
        st.plotly_chart(fig_dist, use_container_width=True)

    with col_b:
        fig_sf = go.Figure()
        fig_sf.add_trace(go.Bar(
            x=["< 2 hrs", "2–5 hrs", "5–10 hrs", "> 10 hrs"],
            y=[102, 162, 95, 36],
            marker_color=["#1e1b4b","#312e81","#4338ca","#4f46e5"],
        ))
        fig_sf.update_layout(
            title=dict(text="Study Volume Matrix", font=dict(size=12, color="#94a3b8", weight="bold"), x=0),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            height=200, margin=dict(t=40, b=20, l=10, r=10),
            font=dict(color="#94a3b8", size=11, family="Inter"),
            xaxis=dict(showgrid=False, tickfont=dict(color="#64748b")),
            yaxis=dict(gridcolor="#1e293b", tickfont=dict(color="#64748b"))
        )
        st.plotly_chart(fig_sf, use_container_width=True)

    with col_c:
        fig_fail = go.Figure()
        fig_fail.add_trace(go.Bar(
            x=["0", "1", "2", "3+"],
            y=[265, 84, 26, 20],
            marker_color=["#4f46e5","#4338ca","#1e1b4b","#7f1d1d"],
        ))
        fig_fail.update_layout(
            title=dict(text="Historical Attrition Log", font=dict(size=12, color="#94a3b8", weight="bold"), x=0),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            height=200, margin=dict(t=40, b=20, l=10, r=10),
            font=dict(color="#94a3b8", size=11, family="Inter"),
            xaxis=dict(showgrid=False, tickfont=dict(color="#64748b")),
            yaxis=dict(gridcolor="#1e293b", tickfont=dict(color="#64748b"))
        )
        st.plotly_chart(fig_fail, use_container_width=True)

# ==========================================
# PAGE: PREDICT
# ==========================================

elif page == "Predict":

    if not st.session_state.predicted:

        st.markdown("""
        <div class="page-header">
            <div class="page-header-left">
                <h2>Grade Optimization Interface</h2>
                <p>Input candidate structural parameters below to check variance projections against the active validation setup.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_left, col_right = st.columns([3, 2], gap="large")

        with col_left:
            st.markdown('<p class="form-group-label">📚 Examination Baselines</p>', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                g1 = st.slider("G1 — Initial Assessment Grade", 0, 20, 10)
            with col2:
                g2 = st.slider("G2 — Midterm Assessment Grade", 0, 20, 10)

            st.markdown('<div class="form-divider"></div>', unsafe_allow_html=True)

            st.markdown('<p class="form-group-label">📖 Execution Vectors</p>', unsafe_allow_html=True)
            col3, col4 = st.columns(2)
            with col3:
                studytime = st.selectbox(
                    "Weekly Study Allotment",
                    options=[1, 2, 3, 4],
                    format_func=lambda x: {
                        1: "Tier 1 — Under 2 Hours/wk",
                        2: "Tier 2 — Between 2 and 5 Hours/wk",
                        3: "Tier 3 — Between 5 and 10 Hours/wk",
                        4: "Tier 4 — Exceeding 10 Hours/wk"
                    }[x]
                )
            with col4:
                failures = st.selectbox(
                    "Prior Block Failures",
                    options=[0, 1, 2, 3, 4],
                    format_func=lambda x: {
                        0: "Zero Historical Failures",
                        1: "Single Failure Record",
                        2: "Two Failure Records",
                        3: "Three Failure Records",
                        4: "Four or More Attritions"
                    }[x]
                )

            st.markdown('<div class="form-divider"></div>', unsafe_allow_html=True)

            st.markdown('<p class="form-group-label">👨‍👩‍👧 Familial Socio-Demographics</p>', unsafe_allow_html=True)
            edu_labels = {
                0: "No Institutional Background",
                1: "Primary Education Block (4th Grade)",
                2: "Basic Academic Secondary (5th–9th Grade)",
                3: "Secondary Certification Achieved",
                4: "Higher Educational Degree Attained"
            }
            col5, col6 = st.columns(2)
            with col5:
                medu = st.selectbox("Maternal Educational Level", options=[0,1,2,3,4], format_func=lambda x: edu_labels[x])
            with col6:
                fedu = st.selectbox("Paternal Educational Level", options=[0,1,2,3,4], format_func=lambda x: edu_labels[x])

            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("🔮  Compute Structural Prediction"):
                st.session_state.predicted = True
                st.session_state.prediction_data = {
                    "g1": g1, "g2": g2, "studytime": studytime,
                    "failures": failures, "medu": medu, "fedu": fedu
                }
                st.rerun()

        with col_right:
            st.markdown("""
            <div style="background:#111726; border:1px solid #1e293b; border-radius:12px; padding:24px; box-shadow: 0 4px 12px rgba(0,0,0,0.2); margin-bottom:16px;">
                <div style="font-size:0.75rem; font-weight:700; text-transform:uppercase; letter-spacing:0.05em; color:#818cf8; margin-bottom:16px; padding-bottom:12px; border-bottom:1px solid #1e293b;">Score Tier Matrix</div>
                <table style="width:100%; font-size:0.9rem; border-collapse:collapse;">
                    <tr style="border-bottom:1px solid #1e293b;">
                        <td style="padding:10px 0; color:#ffffff; font-weight:600;">16 – 20</td>
                        <td style="padding:10px 0; text-align:right;"><span class="pill pill-green">Class A — Excellent</span></td>
                    </tr>
                    <tr style="border-bottom:1px solid #1e293b;">
                        <td style="padding:10px 0; color:#ffffff; font-weight:600;">14 – 15</td>
                        <td style="padding:10px 0; text-align:right;"><span class="pill pill-blue">Class B — Meritorious</span></td>
                    </tr>
                    <tr style="border-bottom:1px solid #1e293b;">
                        <td style="padding:10px 0; color:#ffffff; font-weight:600;">10 – 13</td>
                        <td style="padding:10px 0; text-align:right;"><span class="pill pill-amber">Class C — Competent</span></td>
                    </tr>
                    <tr>
                        <td style="padding:10px 0; color:#ffffff; font-weight:600;">0 – 9</td>
                        <td style="padding:10px 0; text-align:right;"><span class="pill pill-red">Class D — Critical Risk</span></td>
                    </tr>
                </table>
            </div>
            <div style="background:#1e1b4b; border:1px solid #312e81; border-radius:12px; padding:20px;">
                <div style="font-size:0.75rem; font-weight:700; text-transform:uppercase; letter-spacing:0.05em; color:#818cf8; margin-bottom:8px;">Pipeline Weight Notice</div>
                <div style="font-size:0.9rem; color:#cbd5e1; line-height:1.6;">Sequential historical vectors (G1/G2) encapsulate maximum feature weight. Behavioral variations introduce an additional 12% shift boundary.</div>
            </div>
            """, unsafe_allow_html=True)

    else:

        d = st.session_state.prediction_data
        g1 = d["g1"]; g2 = d["g2"]
        studytime = d["studytime"]; failures = d["failures"]
        medu = d["medu"]; fedu = d["fedu"]

        # Read the live backend URL from Render's environment, or default to local if not set
        backend_base_url = os.environ.get("BACKEND_API_URL", "http://127.0.0.1:8000")

        try:
            response = requests.post(
                f"{backend_base_url.rstrip('/')}/api/predict/",
                json={"g1": g1, "g2": g2, "failures": failures,
                    "studytime": studytime, "medu": medu, "fedu": fedu}
                )
            prediction = response.json()["predicted_grade"]
        except Exception as e:
            st.error(f"Could not reach the API at {backend_base_url}: {e}")
            st.stop()

        percentage = min(int((prediction / 20) * 100), 100)

        if prediction >= 16:
            grade_letter, risk_label, feedback_msg = "A", "Optimal Status", "🎉 Performance model identifies an exceptional academic track. Maintain target habits heading into evaluation."
            show_balloons = True
        elif prediction >= 14:
            grade_letter, risk_label, feedback_msg = "B", "Minimal Risk", "✅ High performance capacity indicated. Minor calibration updates should push vectors towards top-tier bands."
            show_balloons = False
        elif prediction >= 10:
            grade_letter, risk_label, feedback_msg = "C", "Moderate Risk", "⚠️ Moderate target trajectory identified. Incremental study volume scales are recommended to build performance safety nets."
            show_balloons = False
        else:
            grade_letter, risk_label, feedback_msg = "D", "Elevated Hazard", "🚨 High system divergence spotted. Structured academic intervention protocols are strongly advised."
            show_balloons = False

        st.markdown("""
        <div class="page-header">
            <div class="page-header-left">
                <h2>Analysis Execution Output</h2>
                <p>Derived model outputs based on evaluation metrics.</p>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="result-hero">
            <div class="result-hero-top">
                <div class="result-grade-num">{prediction}</div>
                <div class="result-hero-meta">
                    <div class="result-hero-title">Predicted End Evaluation Score (G3)</div>
                    <div class="result-hero-sub">{percentage}% of maximum evaluation threshold</div>
                    <div class="result-badges">
                        <span class="badge-light">Band {grade_letter} Classification</span>
                        <span class="badge-light">{risk_label}</span>
                        <span class="badge-light">{percentage}% Confidence Weight</span>
                    </div>
                    <div class="progress-wrap" style="margin-top:16px;">
                        <div class="progress-fill" style="width:{percentage}%;"></div>
                    </div>
                </div>
            </div>
            <div class="result-hero-bottom">{feedback_msg}</div>
        </div>
        """, unsafe_allow_html=True)

        if show_balloons:
            st.balloons()

        st.markdown('<div class="section-label">Dimensional Diagnostics</div>', unsafe_allow_html=True)

        chart_left, chart_right = st.columns(2)

        with chart_left:
            gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=prediction,
                title={"text": "Absolute Score Vector", "font": {"color": "#94a3b8", "size": 13, "family": "Inter"}},
                number={"font": {"color": "#ffffff", "size": 40, "family": "Inter", "weight": "bold"}},
                gauge={
                    "axis": {"range": [0, 20], "tickcolor": "#475569", "tickfont": {"color": "#64748b", "size": 11}},
                    "bar": {"color": "#6366f1", "thickness": 0.22},
                    "bgcolor": "#111726",
                    "borderwidth": 1,
                    "bordercolor": "#1e293b",
                    "steps": [
                        {"range": [0, 9],   "color": "#451a03"},
                        {"range": [9, 13],  "color": "#78350f"},
                        {"range": [13, 16], "color": "#1e1b4b"},
                        {"range": [16, 20], "color": "#064e3b"}
                    ],
                }
            ))
            gauge.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                height=220, margin=dict(t=20, b=10, l=20, r=20)
            )
            st.plotly_chart(gauge, use_container_width=True)

        with chart_right:
            radar = go.Figure()
            radar.add_trace(go.Scatterpolar(
                r=[g1, g2, studytime * 5, max((4 - failures) * 5, 0), medu * 5, fedu * 5],
                theta=["G1", "G2", "Study Volume", "Mitigation Index", "Maternal Tier", "Paternal Tier"],
                fill="toself",
                fillcolor="rgba(99,102,241,0.12)",
                line=dict(color="#6366f1", width=2),
            ))
            radar.update_layout(
                polar=dict(
                    bgcolor="#111726",
                    radialaxis=dict(visible=True, range=[0, 20], tickcolor="#1e293b", gridcolor="#1e293b", tickfont={"size": 10, "color": "#64748b"}),
                    angularaxis=dict(tickcolor="#1e293b", gridcolor="#1e293b", tickfont={"size": 11, "color": "#94a3b8"})
                ),
                paper_bgcolor="rgba(0,0,0,0)",
                showlegend=False, height=220, margin=dict(t=20, b=20, l=40, r=40)
            )
            st.plotly_chart(radar, use_container_width=True)

        st.markdown('<div class="section-label">Vector Parameter Logs</div>', unsafe_allow_html=True)

        study_map = {1: "< 2 Hours/wk", 2: "2–5 Hours/wk", 3: "5–10 Hours/wk", 4: "> 10 Hours/wk"}
        edu_map = {0: "None", 1: "Primary", 2: "Middle School", 3: "Secondary Achieved", 4: "Higher Institution"}

        st.markdown(f"""
        <div class="summary-grid">
            <div class="summary-item"><div class="summary-item-label">Initial Assessment (G1)</div><div class="summary-item-value">{g1} / 20</div></div>
            <div class="summary-item"><div class="summary-item-label">Midterm Matrix (G2)</div><div class="summary-item-value">{g2} / 20</div></div>
            <div class="summary-item"><div class="summary-item-label">Study Allocation</div><div class="summary-item-value">{study_map[studytime]}</div></div>
            <div class="summary-item"><div class="summary-item-label">Attrition Record Count</div><div class="summary-item-value">{failures}</div></div>
            <div class="summary-item"><div class="summary-item-label">Maternal Academic Block</div><div class="summary-item-value">{edu_map[medu]}</div></div>
            <div class="summary-item"><div class="summary-item-label">Paternal Academic Block</div><div class="summary-item-value">{edu_map[fedu]}</div></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        col_back, _ = st.columns([1, 4])
        with col_back:
            if st.button("← Initialize New Log"):
                st.session_state.predicted = False
                st.session_state.prediction_data = {}
                st.rerun()

# ==========================================
# PAGE: MODEL COMPARISON
# ==========================================

elif page == "Model Comparison":

    st.markdown("""
    <div class="page-header">
        <div class="page-header-left">
            <h2>Model Diagnostic Matrix</h2>
            <p>Comparative model validation tracking charts against secondary student records.</p>
        </div>
    </div>
    <div class="kpi-container">
        <div class="kpi-card">
            <div class="kpi-label">Top Engine</div>
            <div class="kpi-value" style="font-size:1.35rem; font-weight:700; padding-top:4px; color:#ffffff;">Random Forest</div>
            <div class="kpi-sub">Baseline configuration</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Peak R² Bounds</div>
            <div class="kpi-value">0.83</div>
            <div class="kpi-sub">Optimal validation score</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Minimal MAE Bounds</div>
            <div class="kpi-value">1.11</div>
            <div class="kpi-sub">Lower threshold boundary</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-label">Evaluated Frameworks</div>
            <div class="kpi-value">3</div>
            <div class="kpi-sub">RF, RF-Tuned, XGBoost</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">Validation Framework Ledger</div>', unsafe_allow_html=True)

    st.markdown("""
    <table class="model-table">
        <thead>
            <tr>
                <th>Target Architecture</th>
                <th>Hyperparameters</th>
                <th>R² Metric Bounds</th>
                <th>MAE Metric Bounds</th>
                <th>Status Classification</th>
            </tr>
        </thead>
        <tbody>
            <tr class="best-row">
                <td>🌲 Random Forest</td>
                <td>Standard Base</td>
                <td><strong>0.83</strong></td>
                <td><strong>1.11</strong></td>
                <td><span class="pill pill-green">Active Deploy</span></td>
            </tr>
            <tr>
                <td>🌲 Random Forest (Tuned)</td>
                <td>GridSearchCV Extensive</td>
                <td>0.77</td>
                <td>1.37</td>
                <td><span class="pill pill-amber">−7.2% Shift</span></td>
            </tr>
            <tr>
                <td>🚀 XGBoost Engine</td>
                <td>Standard Base</td>
                <td>0.76</td>
                <td>1.35</td>
                <td><span class="pill pill-red">−8.4% Shift</span></td>
            </tr>
        </tbody>
    </table>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label">Graphical Metric Variance Checks</div>', unsafe_allow_html=True)

    models_list = ["Random Forest", "RF (Tuned)", "XGBoost Engine"]
    mae_scores = [1.11, 1.37, 1.35]
    r2_scores = [0.83, 0.77, 0.76]
    colors = ["#4f46e5", "#312e81", "#1e1b4b"]

    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=models_list, y=r2_scores, marker_color=colors,
            text=[str(v) for v in r2_scores], textposition="outside",
            textfont={"color": "#94a3b8", "size": 11, "family": "Inter"}
        ))
        fig.update_layout(
            yaxis=dict(range=[0, 1], gridcolor="#1e293b", tickfont={"size": 11, "color": "#64748b"}, title=dict(text="R² Metric Weight", font=dict(size=11, color="#94a3b8"))),
            xaxis=dict(tickfont=dict(color="#94a3b8")),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            height=250, margin=dict(t=20, b=20, l=10, r=10),
            showlegend=False, font={"family": "Inter", "size": 12, "color": "#94a3b8"}
        )
        fig.update_xaxes(showgrid=False)
        st.plotly_chart(fig, use_container_width=True)

    with col_chart2:
        fig2 = go.Figure()
        fig2.add_trace(go.Bar(
            x=models_list, y=mae_scores, marker_color=colors,
            text=[str(v) for v in mae_scores], textposition="outside",
            textfont={"color": "#94a3b8", "size": 11, "family": "Inter"}
        ))
        fig2.update_layout(
            yaxis=dict(range=[0, 2], gridcolor="#1e293b", tickfont={"size": 11, "color": "#64748b"}, title=dict(text="Absolute Error Volatility", font=dict(size=11, color="#94a3b8"))),
            xaxis=dict(tickfont=dict(color="#94a3b8")),
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            height=250, margin=dict(t=20, b=20, l=10, r=10),
            showlegend=False, font={"family": "Inter", "size": 12, "color": "#94a3b8"}
        )
        fig2.update_xaxes(showgrid=False)
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="section-label">Analytical Evaluation</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="verdict-banner">
        <strong>Random Forest architectures using localized defaults maximize generalizability</strong> on small data distributions (R² = 0.83, MAE = 1.11). Exhaustive optimization sweeps (GridSearchCV) overfit background noise instead of true performance signal indicators.
    </div>
    """, unsafe_allow_html=True)