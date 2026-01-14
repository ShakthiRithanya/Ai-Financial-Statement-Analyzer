import streamlit as st
import pandas as pd
import io
import plotly.express as px
import plotly.graph_objects as go
from pdf_extractor import extract_tables_from_pdf
from data_processing import process_multiple_tables
from ratio_analysis import calculate_ratios
from llm_analysis import get_llm_analysis, format_data_for_llm, list_available_models
from utils import validate_financial_data, get_demo_data, custom_metric_card, format_currency

# PAGE CONFIG
st.set_page_config(
    page_title="AI Financial Analyzer | Premium",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# PROFESSIONAL FINANCE THEME CSS
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700;800;900&display=swap');
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700;800;900&display=swap');
    
    * {
        margin: 0;
        padding: 0;
        box-sizing: border-box;
    }
    
    html, body {
        background-color: #0a1628 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    
    /* Main Container - Professional Finance Background */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0a1628 0%, #1a2942 25%, #0f2744 50%, #1a2942 75%, #0a1628 100%) !important;
        background-attachment: fixed !important;
        background-size: 400% 400% !important;
        animation: gradientShift 15s ease infinite;
        position: relative;
    }
    
    /* Elegant grid overlay pattern */
    [data-testid="stAppViewContainer"]::before {
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background-image: 
            linear-gradient(rgba(212, 175, 55, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(212, 175, 55, 0.03) 1px, transparent 1px);
        background-size: 50px 50px;
        pointer-events: none;
        z-index: 0;
    }
    
    /* Subtle radial glow effect */
    [data-testid="stAppViewContainer"]::after {
        content: "";
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        width: 80%;
        height: 80%;
        background: radial-gradient(circle, rgba(212, 175, 55, 0.08) 0%, transparent 70%);
        pointer-events: none;
        z-index: 0;
    }
    
    [data-testid="stMain"] {
        background: transparent !important;
    }
    
    .stApp {
        background: transparent !important;
    }
    
    /* ===== ANIMATIONS ===== */
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    @keyframes slideUp {
        from { opacity: 0; transform: translateY(40px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-12px); }
    }
    
    @keyframes glow {
        0%, 100% { box-shadow: 0 0 20px rgba(212, 175, 55, 0.3); }
        50% { box-shadow: 0 0 40px rgba(212, 175, 55, 0.5); }
    }
    
    @keyframes shimmer {
        0% { background-position: -1000px 0; }
        100% { background-position: 1000px 0; }
    }
    
    /* ===== HIDE DEFAULT ELEMENTS ===== */
    [data-testid="stSidebar"] { display: none; }
    [data-testid="stSidebarNav"] { display: none; }
    #MainMenu { visibility: hidden; }
    footer { visibility: hidden; }
    header { visibility: hidden; }
    
    /* ===== TABS STYLING ===== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background-color: transparent;
        padding: 12px 0;
        border-bottom: 2px solid rgba(212, 175, 55, 0.2);
        flex-wrap: wrap;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: rgba(26, 41, 66, 0.6);
        border: 1px solid rgba(212, 175, 55, 0.2);
        color: #b8c5d6;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        border-radius: 8px;
        padding: 8px 24px !important;
        letter-spacing: 0.5px;
        font-family: 'Montserrat', sans-serif;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(212, 175, 55, 0.15);
        border-color: rgba(212, 175, 55, 0.4);
        color: #d4af37;
    }
    
    .stTabs [aria-selected="true"] {
        color: #ffffff !important;
        background: linear-gradient(135deg, rgba(212, 175, 55, 0.25) 0%, rgba(26, 41, 66, 0.8) 100%) !important;
        border-color: #d4af37 !important;
        border-bottom: 2px solid #d4af37 !important;
        box-shadow: 0 8px 24px rgba(212, 175, 55, 0.2) !important;
    }
    
    /* ===== BUTTON STYLING ===== */
    .stButton>button {
        border-radius: 8px;
        background: linear-gradient(135deg, #d4af37 0%, #c5a028 100%);
        color: #0a1628;
        border: none;
        padding: 12px 28px;
        font-weight: 700;
        font-size: 0.95rem;
        letter-spacing: 0.5px;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        box-shadow: 0 8px 24px rgba(212, 175, 55, 0.3);
        text-transform: uppercase;
        font-family: 'Montserrat', sans-serif;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 12px 32px rgba(212, 175, 55, 0.45);
        background: linear-gradient(135deg, #e5c048 0%, #d4af37 100%);
    }
    
    .stButton>button:active {
        transform: translateY(-1px) scale(0.98);
        box-shadow: 0 4px 16px rgba(212, 175, 55, 0.25);
    }
    
    /* ===== TITLE GRADIENT ===== */
    .title-gradient {
        background: linear-gradient(135deg, #d4af37, #f0d878, #4a90e2, #d4af37);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 4rem;
        font-weight: 900;
        letter-spacing: -2px;
        animation: gradientShift 8s ease infinite;
        background-size: 300% 300%;
        font-family: 'Playfair Display', serif;
    }
    
    /* ===== GLASSMORPHISM CARDS ===== */
    .config-box {
        background: rgba(26, 41, 66, 0.7);
        backdrop-filter: blur(30px);
        -webkit-backdrop-filter: blur(30px);
        border: 1px solid rgba(212, 175, 55, 0.2);
        border-radius: 16px;
        padding: 40px;
        margin-bottom: 50px;
        box-shadow: 0 20px 50px rgba(10, 22, 40, 0.4),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.3s ease;
    }
    
    .config-box:hover {
        background: rgba(26, 41, 66, 0.85);
        border-color: rgba(212, 175, 55, 0.35);
        box-shadow: 0 25px 60px rgba(10, 22, 40, 0.5),
                    inset 0 1px 0 rgba(255, 255, 255, 0.15);
    }
    
    /* ===== INPUT STYLING ===== */
    .stTextInput input, .stSelectbox select, .stNumberInput input {
        background-color: rgba(26, 41, 66, 0.6) !important;
        border: 1px solid rgba(212, 175, 55, 0.2) !important;
        border-radius: 8px !important;
        color: #e8eef5 !important;
        padding: 12px 16px !important;
        transition: all 0.3s ease !important;
        font-size: 0.95rem !important;
        font-family: 'Inter', sans-serif;
    }
    
    .stTextInput input:focus, .stSelectbox select:focus, .stNumberInput input:focus {
        background-color: rgba(26, 41, 66, 0.8) !important;
        border-color: #d4af37 !important;
        box-shadow: 0 0 20px rgba(212, 175, 55, 0.3) !important;
    }
    
    /* ===== DATAFRAME STYLING ===== */
    .stDataFrame {
        background-color: rgba(26, 41, 66, 0.6) !important;
        border-radius: 12px !important;
        overflow: hidden !important;
        box-shadow: 0 12px 32px rgba(10, 22, 40, 0.3) !important;
        border: 1px solid rgba(212, 175, 55, 0.1);
    }
    
    .stDataFrame div {
        color: #e8eef5 !important;
    }
    
    /* ===== TEXT STYLING ===== */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff !important;
        letter-spacing: -0.5px;
        font-family: 'Playfair Display', serif;
    }
    
    p, span, label {
        color: #b8c5d6 !important;
        font-family: 'Inter', sans-serif;
    }
    
    /* ===== METRIC CARDS ===== */
    .metric-card {
        background: linear-gradient(135deg, rgba(26, 41, 66, 0.8) 0%, rgba(15, 39, 68, 0.6) 100%);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid rgba(212, 175, 55, 0.2);
        border-radius: 16px;
        padding: 28px;
        box-shadow: 0 12px 32px rgba(10, 22, 40, 0.3),
                    inset 0 1px 0 rgba(255, 255, 255, 0.1);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .metric-card:hover {
        transform: translateY(-6px);
        background: linear-gradient(135deg, rgba(26, 41, 66, 0.9) 0%, rgba(15, 39, 68, 0.7) 100%);
        border-color: #d4af37;
        box-shadow: 0 16px 48px rgba(212, 175, 55, 0.2),
                    inset 0 1px 0 rgba(255, 255, 255, 0.15);
    }
    
    /* ===== SUCCESS/ERROR/INFO BOXES ===== */
    .stSuccess, .stInfo, .stWarning, .stError {
        background: rgba(26, 41, 66, 0.7) !important;
        border: 1px solid rgba(212, 175, 55, 0.3) !important;
        border-radius: 12px !important;
        backdrop-filter: blur(20px) !important;
        -webkit-backdrop-filter: blur(20px) !important;
        box-shadow: 0 8px 24px rgba(10, 22, 40, 0.2) !important;
    }
    
    .stError {
        background: rgba(220, 38, 38, 0.1) !important;
        border-color: rgba(220, 38, 38, 0.3) !important;
    }
    
    .stWarning {
        background: rgba(245, 158, 11, 0.1) !important;
        border-color: rgba(245, 158, 11, 0.3) !important;
    }
    
    /* ===== SPINNER ===== */
    .stSpinner {
        color: #d4af37;
    }
    
    /* ===== SCROLLBAR ===== */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(26, 41, 66, 0.3);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #d4af37, #c5a028);
        border-radius: 10px;
        transition: all 0.3s ease;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #e5c048, #d4af37);
    }
    
    /* ===== RESPONSIVE ===== */
    @media (max-width: 768px) {
        .title-gradient {
            font-size: 2.5rem;
        }
        
        .config-box {
            padding: 24px;
            margin-bottom: 30px;
        }
    }
    </style>
    """, unsafe_allow_html=True)

if 'page' not in st.session_state:
    st.session_state.page = 'landing'
if 'active_mode' not in st.session_state:
    st.session_state.active_mode = 'Extraction'

def landing_page():
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Header section
    header_html = """
    <div style="text-align: center; padding: 80px 40px 60px; position: relative; z-index: 2;">
        <div style="display: inline-block; padding: 10px 24px; background: linear-gradient(135deg, rgba(212, 175, 55, 0.15), rgba(74, 144, 226, 0.1)); border: 1px solid rgba(212, 175, 55, 0.3); border-radius: 50px; color: #d4af37; font-size: 0.85rem; font-weight: 700; margin-bottom: 28px; text-transform: uppercase; letter-spacing: 1.5px; backdrop-filter: blur(20px); font-family: 'Montserrat', sans-serif;">
            💎 AI-Powered Financial Intelligence
        </div>
        <h1 style="font-size: 5rem; font-weight: 900; margin-bottom: 20px; line-height: 1.1; letter-spacing: -2px; font-family: 'Playfair Display', serif;">
            <span class="title-gradient">Master Your Financial Narrative</span>
        </h1>
        <p style="font-size: 1.3rem; color: #b8c5d6; max-width: 900px; margin: 0 auto 50px; line-height: 1.7; font-weight: 400; font-family: 'Inter', sans-serif;">
            Transform complex financial reports into actionable insights in seconds. 
            <br><strong style="color: #e8eef5;">AI-powered analysis. Zero spreadsheet chaos.</strong>
        </p>
        <div style="display: inline-block; padding: 20px 40px; background: linear-gradient(135deg, rgba(212, 175, 55, 0.12), rgba(26, 41, 66, 0.6)); border: 1px solid rgba(212, 175, 55, 0.25); border-radius: 12px; color: #d4af37; font-size: 0.85rem; backdrop-filter: blur(20px); font-family: 'Montserrat', sans-serif; font-weight: 600;">
            📊 3-Stage Analysis Pipeline: Extract → Analyze → Predict
        </div>
    </div>
    """
    st.markdown(header_html, unsafe_allow_html=True)

    # Terminal selection section
    terminal_header = """
    <div style="margin: 60px 0; position: relative; z-index: 2;">
        <div style="text-align: center; margin-bottom: 50px;">
            <h2 style="font-size: 2.2rem; font-weight: 800; color: #ffffff; margin: 0; letter-spacing: -0.5px; font-family: 'Playfair Display', serif;">
                Choose Your Analysis Terminal
            </h2>
        </div>
    </div>
    """
    st.markdown(terminal_header, unsafe_allow_html=True)
    
    f_col1, f_col2, f_col3 = st.columns(3, gap="medium")
    
    with f_col1:
        st.markdown("""
            <div class="metric-card" style="text-align: center; cursor: pointer; transition: all 0.3s ease;">
                <div style="font-size: 3.5rem; margin-bottom: 12px;">📄</div>
                <h3 style="font-size: 1.4rem; color: #ffffff; margin-bottom: 8px; font-weight: 800; font-family: 'Playfair Display', serif;">
                    Extraction Lab
                </h3>
                <p style="color: #b8c5d6; margin: 0; line-height: 1.6; font-size: 0.95rem; font-family: 'Inter', sans-serif;">
                    Auto-extract and cleanse raw financial data from PDFs, Excel, and CSV with AI-powered normalization.
                </p>
                <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid rgba(212, 175, 55, 0.2);">
                    <p style="font-size: 0.85rem; color: #d4af37; font-weight: 700; margin: 0; font-family: 'Montserrat', sans-serif;">PHASE 1 — Foundation</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("🚀 Launch Lab", use_container_width=True, key="btn_extract"):
            st.session_state.active_mode = 'Extraction'
            st.session_state.page = 'analyzer'
            st.rerun()
    
    with f_col2:
        st.markdown("""
            <div class="metric-card" style="text-align: center; cursor: pointer; transition: all 0.3s ease;">
                <div style="font-size: 3.5rem; margin-bottom: 12px;">📊</div>
                <h3 style="font-size: 1.4rem; color: #ffffff; margin-bottom: 8px; font-weight: 800; font-family: 'Playfair Display', serif;">
                    Analysis Desk
                </h3>
                <p style="color: #b8c5d6; margin: 0; line-height: 1.6; font-size: 0.95rem; font-family: 'Inter', sans-serif;">
                    Visualize 15+ financial metrics, growth trajectories, and solvency matrices with interactive charts.
                </p>
                <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid rgba(212, 175, 55, 0.2);">
                    <p style="font-size: 0.85rem; color: #4a90e2; font-weight: 700; margin: 0; font-family: 'Montserrat', sans-serif;">PHASE 2 — Analysis</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("📊 Launch Desk", use_container_width=True, key="btn_analysis"):
            st.session_state.active_mode = 'Computation'
            st.session_state.page = 'analyzer'
            st.rerun()
        
    with f_col3:
        st.markdown("""
            <div class="metric-card" style="text-align: center; cursor: pointer; transition: all 0.3s ease;">
                <div style="font-size: 3.5rem; margin-bottom: 12px;">🧠</div>
                <h3 style="font-size: 1.4rem; color: #ffffff; margin-bottom: 8px; font-weight: 800; font-family: 'Playfair Display', serif;">
                    AI War Room
                </h3>
                <p style="color: #b8c5d6; margin: 0; line-height: 1.6; font-size: 0.95rem; font-family: 'Inter', sans-serif;">
                    Run deep forensic LLM analysis to identify hidden risks, strengths, and investment theses.
                </p>
                <div style="margin-top: 20px; padding-top: 20px; border-top: 1px solid rgba(212, 175, 55, 0.2);">
                    <p style="font-size: 0.85rem; color: #c5a028; font-weight: 700; margin: 0; font-family: 'Montserrat', sans-serif;">PHASE 3 — Intelligence</p>
                </div>
            </div>
        """, unsafe_allow_html=True)
        if st.button("🪄 Enter War Room", use_container_width=True, key="btn_intelligence"):
            st.session_state.active_mode = 'Intelligence'
            st.session_state.page = 'analyzer'
            st.rerun()

    # Benefits section
    benefits_html = """
    <div style="margin: 80px 0; position: relative; z-index: 2;">
        <div style="text-align: center; margin-bottom: 40px;">
            <h2 style="font-size: 2.2rem; font-weight: 800; color: #ffffff; margin: 0; letter-spacing: -0.5px; font-family: 'Playfair Display', serif;">
                Why Choose Our Platform
            </h2>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 24px;">
            <div style="background: rgba(212, 175, 55, 0.08); border: 1px solid rgba(212, 175, 55, 0.2); border-radius: 16px; padding: 28px; backdrop-filter: blur(20px); transition: all 0.3s ease;">
                <div style="font-size: 2.5rem; margin-bottom: 16px;">⚡</div>
                <h4 style="font-size: 1.1rem; color: #ffffff; margin: 0 0 12px 0; font-weight: 800; font-family: 'Playfair Display', serif;">
                    Lightning Fast
                </h4>
                <p style="color: #b8c5d6; margin: 0; font-size: 0.9rem; line-height: 1.5; font-family: 'Inter', sans-serif;">
                    Process multi-year financial statements in seconds with AI acceleration.
                </p>
            </div>
            <div style="background: rgba(74, 144, 226, 0.08); border: 1px solid rgba(74, 144, 226, 0.2); border-radius: 16px; padding: 28px; backdrop-filter: blur(20px); transition: all 0.3s ease;">
                <div style="font-size: 2.5rem; margin-bottom: 16px;">🎯</div>
                <h4 style="font-size: 1.1rem; color: #ffffff; margin: 0 0 12px 0; font-weight: 800; font-family: 'Playfair Display', serif;">
                    Precise Insights
                </h4>
                <p style="color: #b8c5d6; margin: 0; font-size: 0.9rem; line-height: 1.5; font-family: 'Inter', sans-serif;">
                    Get strategic investment thesis and detailed risk assessments from Google Gemini AI.
                </p>
            </div>
            <div style="background: rgba(26, 41, 66, 0.6); border: 1px solid rgba(212, 175, 55, 0.25); border-radius: 16px; padding: 28px; backdrop-filter: blur(20px); transition: all 0.3s ease;">
                <div style="font-size: 2.5rem; margin-bottom: 16px;">🔐</div>
                <h4 style="font-size: 1.1rem; color: #ffffff; margin: 0 0 12px 0; font-weight: 800; font-family: 'Playfair Display', serif;">
                    Enterprise Grade
                </h4>
                <p style="color: #b8c5d6; margin: 0; font-size: 0.9rem; line-height: 1.5; font-family: 'Inter', sans-serif;">
                    Bank-level security with confidential API key handling and data protection.
                </p>
            </div>
        </div>
    </div>
    """
    st.markdown(benefits_html, unsafe_allow_html=True)


    # Footer CTA
    footer_html = """
    <div style="margin-top: 100px; padding: 40px; text-align: center; background: linear-gradient(135deg, rgba(212, 175, 55, 0.12), rgba(26, 41, 66, 0.7)); border: 1px solid rgba(212, 175, 55, 0.25); border-radius: 16px; backdrop-filter: blur(20px); position: relative; z-index: 2;">
        <h3 style="font-size: 1.5rem; color: #ffffff; margin: 0 0 12px 0; font-weight: 800; font-family: 'Playfair Display', serif;">
            Ready to Master Your Financials?
        </h3>
        <p style="color: #b8c5d6; margin: 0; font-size: 0.95rem; font-family: 'Inter', sans-serif;">
            Analyze your financial statements like a professional analyst. Start today with zero experience needed.
        </p>
        <div style="margin-top: 24px; color: #d4af37; font-size: 0.85rem; font-weight: 700; letter-spacing: 1px; font-family: 'Montserrat', sans-serif;">
            🔒 SECURED BY GEMINI AI • 100% CONFIDENTIAL
        </div>
    </div>
    """
    st.markdown(footer_html, unsafe_allow_html=True)


    st.markdown('</div>', unsafe_allow_html=True)

def analyzer_page():
    st.markdown('<div class="main-content">', unsafe_allow_html=True)
    
    # Header with navigation
    st.markdown("""
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 40px; padding-bottom: 24px; border-bottom: 1px solid rgba(139, 92, 246, 0.2);">
            <div>
                <h1 class="title-gradient" style="font-size: 2.8rem; margin: 0; font-weight: 900; letter-spacing: -1px;">
                    Terminal Control
                </h1>
                <p style="color: #b0b0c0; margin: 8px 0 0 0; font-size: 0.95rem;">
                    Professional financial analysis workspace
                </p>
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    # Quick navigation
    nav_col1, nav_col2 = st.columns([3, 2])
    with nav_col1:
        st.empty()
    with nav_col2:
        nav_subcol1, nav_subcol2 = st.columns(2)
        with nav_subcol1:
            if st.button("🏠 Home", use_container_width=True):
                st.session_state.page = 'landing'
                st.rerun()
        with nav_subcol2:
            current_mode = st.session_state.active_mode
            target_mode = st.selectbox("Terminal", ["Extraction", "Computation", "Intelligence"], 
                                       index=["Extraction", "Computation", "Intelligence"].index(current_mode), 
                                       label_visibility="collapsed")
            if target_mode != current_mode:
                st.session_state.active_mode = target_mode
                st.rerun()

    # SYSTEM CONFIGURATION BOX
    st.markdown('<div class="config-box">', unsafe_allow_html=True)
    
    cfg_title, cfg_empty = st.columns([2, 1])
    with cfg_title:
        st.markdown("#### ⚙️ System Configuration")
    
    cfg_col1, cfg_col2, cfg_col3 = st.columns([1.4, 1.5, 1.1])
    
    with cfg_col1:
        st.markdown('<p style="color: #a78bfa; font-size: 0.85rem; font-weight: 700; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px;">🔑 AI Engine</p>', unsafe_allow_html=True)
        api_key = st.text_input("Gemini API Key", type="password", placeholder="sk-...", label_visibility="collapsed")
        
        # Initialize session state for models
        if 'available_models' not in st.session_state:
            st.session_state.available_models = ["gemini-1.5-flash", "gemini-1.5-pro", "gemini-pro"]
            
        col_m_1, col_m_2 = st.columns([3, 1])
        with col_m_1:
            if model_name_val := st.selectbox("Model", st.session_state.available_models, label_visibility="collapsed", key="model_selector"):
                model_name = model_name_val
        with col_m_2:
            if st.button("🔍", help="Scan for available models", use_container_width=True):
                if api_key:
                    with st.spinner("Scanning..."):
                        found_models = list_available_models(api_key)
                        if found_models:
                            st.session_state.available_models = found_models
                            st.rerun()
                else:
                    st.warning("⚠️ API Key required")
        
    with cfg_col2:
        st.markdown('<p style="color: #ec4899; font-size: 0.85rem; font-weight: 700; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px;">📤 Data Input</p>', unsafe_allow_html=True)
        uploaded_file = st.file_uploader("Upload Financial Report", type=["pdf", "xlsx", "csv"], label_visibility="collapsed")
        
    with cfg_col3:
        st.markdown('<p style="color: #06b6d4; font-size: 0.85rem; font-weight: 700; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px;">🚀 Demo</p>', unsafe_allow_html=True)
        demo_mode = st.button("Demo: Apple", use_container_width=True, key="demo_btn")
        st.markdown("""
            <div style="background: linear-gradient(135deg, rgba(6, 182, 212, 0.1), rgba(139, 92, 246, 0.05)); padding: 8px 12px; border-radius: 8px; border: 1px solid rgba(6, 182, 212, 0.2); text-align: center; margin-top: 8px;">
                <span style="color: #06b6d4; font-size: 0.75rem; font-weight: 700;">v1.2 PRO</span>
            </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    df = None
    if demo_mode:
        df = get_demo_data()
        st.toast("🍎 Loading Apple Inc. Financial Data...", icon="✨")
    elif uploaded_file:
        file_ext = uploaded_file.name.split('.')[-1].lower()
        with st.spinner("🔄 Processing document..."):
            try:
                if file_ext == "pdf":
                    tables = extract_tables_from_pdf(uploaded_file)
                    df = process_multiple_tables(tables)
                elif file_ext == "xlsx":
                    raw_df = pd.read_excel(uploaded_file)
                    df = process_multiple_tables([raw_df])
                elif file_ext == "csv":
                    raw_df = pd.read_csv(uploaded_file)
                    df = process_multiple_tables([raw_df])
            except Exception as e:
                st.error(f"❌ Processing failed: {str(e)}")

    if df is not None:
        valid, msg = validate_financial_data(df)
        if not valid:
            st.error(f"⚠️ {msg}")
        
        ratios_df = calculate_ratios(df)
        latest_year = str(df.index[-1])
        prev_year = str(df.index[-2]) if len(df) > 1 else None

        if st.session_state.active_mode == 'Extraction':
            # EXTRACTION LAB
            st.markdown("""
                <div style="margin-top: 40px;">
                    <h2 style="font-size: 2rem; color: #ffffff; font-weight: 800; margin-bottom: 24px;">
                        📄 Extraction Lab
                    </h2>
                    <p style="color: #b0b0c0; margin-bottom: 24px;">
                        Processed and normalized financial data ready for analysis
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            e_col1, e_col2 = st.columns([1.5, 1])
            with e_col1:
                st.markdown('<h3 style="color: #ffffff; font-weight: 700; margin-bottom: 16px;">Structured Data</h3>', unsafe_allow_html=True)
                st.dataframe(df.T.style.highlight_max(axis=0), use_container_width=True)
            with e_col2:
                st.markdown('<h3 style="color: #ffffff; font-weight: 700; margin-bottom: 16px;">Validation Report</h3>', unsafe_allow_html=True)
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(0, 255, 136, 0.08), rgba(6, 182, 212, 0.05)); padding: 28px; border-radius: 16px; border: 1px solid rgba(0, 255, 136, 0.2); backdrop-filter: blur(20px);">
                    <div style="display: flex; align-items: center; margin-bottom: 16px;">
                        <div style="font-size: 2rem; margin-right: 12px;">✅</div>
                        <h4 style="color: #00ff88; margin: 0; font-weight: 800;">Structure Verified</h4>
                    </div>
                    <div style="color: #b0b0c0; font-size: 0.9rem; line-height: 1.6;">
                        <p style="margin: 8px 0;"><strong>Lines:</strong> {len(df.columns)} items</p>
                        <p style="margin: 8px 0;"><strong>Periods:</strong> {len(df)} years</p>
                        <p style="margin: 8px 0;"><strong>Years:</strong> {', '.join(df.index.astype(str))}</p>
                    </div>
                </div>""", unsafe_allow_html=True)
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("➡️ Proceed to Analysis", use_container_width=True):
                    st.session_state.active_mode = 'Computation'
                    st.rerun()

        elif st.session_state.active_mode == 'Computation':
            # ANALYSIS DESK
            st.markdown("""
                <div style="margin-top: 40px;">
                    <h2 style="font-size: 2rem; color: #ffffff; font-weight: 800; margin-bottom: 24px;">
                        📊 Analysis Desk
                    </h2>
                    <p style="color: #b0b0c0; margin-bottom: 32px;">
                        Comprehensive financial metrics and growth analysis
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            # KPI Cards
            m_col1, m_col2, m_col3, m_col4 = st.columns(4)
            rev = df.loc[latest_year, 'revenue']
            rev_delta = f"{((rev/df.loc[prev_year, 'revenue'])-1)*100:.1f}%" if prev_year else None
            m_col1.markdown(custom_metric_card("Total Revenue", format_currency(rev), rev_delta, "🏦"), unsafe_allow_html=True)
            ni = df.loc[latest_year, 'net_income']
            ni_delta = f"{((ni/df.loc[prev_year, 'net_income'])-1)*100:.1f}%" if prev_year else None
            m_col2.markdown(custom_metric_card("Net Income", format_currency(ni), ni_delta, "💹"), unsafe_allow_html=True)
            fcf = ratios_df.loc[latest_year, 'Free Cash Flow'] if 'Free Cash Flow' in ratios_df.columns else 0
            m_col3.markdown(custom_metric_card("Free Cash Flow", format_currency(fcf), None, "💧"), unsafe_allow_html=True)
            roe = ratios_df.loc[latest_year, 'ROE (%)'] if 'ROE (%)' in ratios_df.columns else 0
            m_col4.markdown(custom_metric_card("Return on Equity", f"{roe:.1f}%", None, "📈"), unsafe_allow_html=True)

            # Charts section
            c1, c2 = st.columns([1.5, 1])
            with c1:
                st.markdown('<h3 style="color: #ffffff; font-weight: 700; margin-bottom: 16px;">📈 Growth Trajectory</h3>', unsafe_allow_html=True)
                fig = go.Figure()
                fig.add_trace(go.Bar(x=df.index, y=df['revenue'], name='Revenue', marker_color='#8b5cf6', opacity=0.85))
                fig.add_trace(go.Scatter(x=df.index, y=df['net_income'], name='Net Income', line=dict(color='#ec4899', width=4), mode='lines+markers'))
                fig.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)', 
                    plot_bgcolor='rgba(0,0,0,0)', 
                    font=dict(color='#d0d0e0'), 
                    margin=dict(l=0, r=0, t=0, b=0), 
                    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                    hovermode='x unified'
                )
                st.plotly_chart(fig, use_container_width=True)
            with c2:
                st.markdown('<h3 style="color: #ffffff; font-weight: 700; margin-bottom: 16px;">⚖️ Health Matrix</h3>', unsafe_allow_html=True)
                if 'Current Ratio' in ratios_df.columns:
                    fig_radar = go.Figure()
                    fig_radar.add_trace(go.Scatterpolar(
                        r=[ratios_df.loc[latest_year, 'Current Ratio']*10, ratios_df.loc[latest_year, 'ROE (%)'], ratios_df.loc[latest_year, 'Net Profit Margin'] if 'Net Profit Margin' in ratios_df.columns else 0], 
                        theta=['Liquidity', 'ROE', 'Margin'], 
                        fill='toself', 
                        marker_color='#8b5cf6',
                        line_color='#ec4899'
                    ))
                    fig_radar.update_layout(
                        polar=dict(bgcolor='rgba(139, 92, 246, 0.05)'), 
                        paper_bgcolor='rgba(0,0,0,0)', 
                        font=dict(color='#d0d0e0'),
                        margin=dict(l=0, r=0, t=0, b=0)
                    )
                    st.plotly_chart(fig_radar, use_container_width=True)
            
            # Ratios table
            st.markdown('<h3 style="color: #ffffff; font-weight: 700; margin-top: 32px; margin-bottom: 16px;">📋 Financial Ratios</h3>', unsafe_allow_html=True)
            st.dataframe(ratios_df.T.style.background_gradient(cmap='twilight'), use_container_width=True)
            
            if st.button("➡️ Proceed to AI Analysis", use_container_width=True):
                st.session_state.active_mode = 'Intelligence'
                st.rerun()

        elif st.session_state.active_mode == 'Intelligence':
            # AI WAR ROOM
            st.markdown("""
                <div style="margin-top: 40px;">
                    <h2 style="font-size: 2rem; color: #ffffff; font-weight: 800; margin-bottom: 24px;">
                        🧠 AI War Room
                    </h2>
                    <p style="color: #b0b0c0; margin-bottom: 24px;">
                        Deep forensic LLM analysis powered by Google Gemini
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            if not api_key:
                st.warning("⚠️ Connect Gemini API Key above to enable AI analysis")
            else:
                if st.button("🪄 Run Full AI Intelligence Suite", use_container_width=True):
                    with st.spinner("🔍 Analyzing financial data..."):
                        data_str = format_data_for_llm(df, ratios_df)
                        ai_results = get_llm_analysis(api_key, data_str, model_name=model_name)
                        if "error" in ai_results: 
                            st.error(f"❌ {ai_results['error']}")
                        else: 
                            st.session_state.ai_results = ai_results
                            st.success("✅ Analysis complete!")
                
                if 'ai_results' in st.session_state:
                    res = st.session_state.ai_results
                    
                    # Tabs for different analyses
                    it1, it2, it3 = st.tabs(["✨ Performance", "🚨 Risk Factors", "💪 Investment Thesis"])
                    
                    with it1:
                        st.markdown("""
                            <div style="background: linear-gradient(135deg, rgba(139, 92, 246, 0.1), rgba(168, 85, 247, 0.05)); padding: 28px; border-radius: 16px; border: 1px solid rgba(139, 92, 246, 0.2); backdrop-filter: blur(20px);">
                        """, unsafe_allow_html=True)
                        st.markdown(res.get('performance', ''))
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    with it2:
                        st.markdown("""
                            <div style="background: linear-gradient(135deg, rgba(239, 68, 68, 0.08), rgba(236, 72, 153, 0.05)); padding: 28px; border-radius: 16px; border: 1px solid rgba(239, 68, 68, 0.2); backdrop-filter: blur(20px);">
                        """, unsafe_allow_html=True)
                        st.markdown(res.get('red_flags', ''))
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    with it3:
                        st.markdown("""
                            <div style="background: linear-gradient(135deg, rgba(34, 197, 94, 0.08), rgba(6, 182, 212, 0.05)); padding: 28px; border-radius: 16px; border: 1px solid rgba(34, 197, 94, 0.2); backdrop-filter: blur(20px);">
                        """, unsafe_allow_html=True)
                        st.markdown(res.get('strengths', ''))
                        st.markdown("</div>", unsafe_allow_html=True)
                    
                    # Final verdict
                    st.markdown("""
                        <div style="margin-top: 32px; background: linear-gradient(135deg, rgba(139, 92, 246, 0.12), rgba(236, 72, 153, 0.08)); border: 1.5px solid rgba(139, 92, 246, 0.3); border-radius: 16px; padding: 28px; backdrop-filter: blur(20px);">
                            <h3 style="color: #ffffff; font-weight: 800; margin: 0 0 12px 0; font-size: 1.2rem;">📋 Final Investment Verdict</h3>
                            <p style="color: #d0d0e0; margin: 0; font-size: 1rem; line-height: 1.7;">
                    """, unsafe_allow_html=True)
                    st.markdown(res.get('verdict', ''))
                    st.markdown("</p></div>", unsafe_allow_html=True)
    else:
        st.markdown("""
            <div style="text-align: center; padding: 60px 40px; border: 1.5px dashed rgba(139, 92, 246, 0.2); border-radius: 24px; background: rgba(139, 92, 246, 0.05); backdrop-filter: blur(20px);">
                <div style="font-size: 3rem; margin-bottom: 20px;">📄</div>
                <h2 style="color: #ffffff; font-weight: 800; margin: 0 0 12px 0; font-size: 1.8rem;">Ready to Analyze?</h2>
                <p style="color: #b0b0c0; margin: 0; font-size: 1rem;">
                    Upload a financial report (PDF, Excel, or CSV) or click <strong>Demo: Apple</strong> to get started.
                </p>
            </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    if st.session_state.page == 'landing':
        landing_page()
    else:
        analyzer_page()
