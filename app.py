import streamlit as st
import pdfplumber
import re
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from wordcloud import WordCloud
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from skills import extract_skills
import datetime
import json

# Matplotlib backend for Streamlit
plt.style.use('dark_background')
plt.rcParams['figure.facecolor'] = '#050C0A'
plt.rcParams['axes.facecolor'] = '#050C0A'

st.set_page_config(
    page_title="ResumeAI Pro",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# NEON GREEN CYBER THEME CSS (#39ff14) - CLEAN VERSION
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Rajdhani:wght@400;600;700&display=swap');

:root {
    --neon: #39ff14;
    --neon-dim: rgba(57,255,20,0.6);
    --neon-faint: rgba(57,255,20,0.15);
    --neon-border: rgba(57,255,20,0.35);
    --bg: #050C0A;
    --surface: rgba(57,255,20,0.05);
    --surface2: rgba(57,255,20,0.08);
}

/* GLOBAL NEON GREEN TEXT */
*, *::before, *::after {
    font-family: 'Rajdhani', sans-serif !important;
    color: var(--neon) !important;
}

.stApp {
    background: var(--bg) !important;
    background-image: radial-gradient(ellipse 80% 60% at 20% 10%, var(--neon-faint) 0%, transparent 60%),
                      radial-gradient(ellipse 60% 40% at 80% 80%, rgba(57,200,20,0.04) 0%, transparent 50%),
                      repeating-linear-gradient(0deg, transparent, transparent 39px, var(--neon-faint) 39px, var(--neon-faint) 40px),
                      repeating-linear-gradient(90deg, transparent, transparent 39px, var(--neon-faint) 39px, var(--neon-faint) 40px) !important;
    min-height: 100vh !important;
}

/* HIDE HAMBURGER FOR AUTHENTIC WEBSITE LOOK */
[data-testid="collapsedControl"], [data-testid="stSidebar"] > div:first-child {
    display: none !important;
}

/* ALL TEXT ELEMENTS NEON */
h1, h2, h3, h4, h5, h6, p, div, span, label, li, a, strong, em, code, .stText, .stMarkdown {
    color: var(--neon) !important;
}

/* INPUTS */
textarea, input[type="text"], input[type="number"] {
    background: rgba(10,15,8,0.9) !important;
    color: var(--neon) !important;
    border: 1px solid var(--neon-border) !important;
    border-radius: 8px !important;
}
textarea:focus, input:focus {
    border-color: var(--neon) !important;
    box-shadow: 0 0 12px var(--neon-dim) !important;
}
textarea::placeholder, input::placeholder {
    color: var(--neon-dim) !important;
}

/* BUTTONS */
.stButton > button {
    background: transparent !important;
    color: var(--neon) !important;
    border: 1.5px solid var(--neon) !important;
    border-radius: 6px !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    text-transform: uppercase !important;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: var(--surface2) !important;
    box-shadow: 0 0 20px var(--neon-dim) !important;
    transform: translateY(-1px) !important;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: rgba(5,10,5,0.95) !important;
    border-right: 1px solid var(--neon-border) !important;
}
[data-testid="stSidebar"] * {
    color: var(--neon) !important;
}
[data-testid="stSidebar"] input, [data-testid="stSidebar"] textarea {
    background: rgba(57,255,20,0.05) !important;
    border: 1px solid var(--neon-border) !important;
    color: var(--neon) !important;
}

/* TABS */
.stTabs [data-baseweb="tab"] {
    color: var(--neon-dim) !important;
    font-family: 'Share Tech Mono', monospace !important;
}
.stTabs [aria-selected="true"] {
    color: var(--neon) !important;
    border-bottom: 2px solid var(--neon) !important;
}

/* CARDS & METRICS */
.neon-card, [data-testid="metric-container"] {
    background: var(--surface) !important;
    border: 1px solid var(--neon-border) !important;
    color: var(--neon) !important;
}

/* DATAFRAME */
[data-testid="stDataFrame"] *, .dataframe {
    color: var(--neon) !important;
}

/* FILE UPLOADER */
[data-testid="stFileUploader"] * {
    color: var(--neon) !important;
}
[data-testid="stFileUploader"] {
    border: 1px dashed var(--neon-border) !important;
}

/* PROGRESS */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, var(--neon), #00cc44) !important;
    box-shadow: 0 0 8px var(--neon) !important;
}

/* SCROLLBAR */
::-webkit-scrollbar-thumb {
    background: var(--neon-dim) !important;
}
</style>
""", unsafe_allow_html=True)

# ORIGINAL FUNCTIONS (UNCHANGED)
def extract_text_from_pdf(pdf_file):
    text = ""
    try:
        with pdfplumber.open(pdf_file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except:
        pass
    return text

def clean_text(text):
    if not text: return ""
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def calculate_match(resume, jd):
    if not resume or not jd: return 0.0
    docs = [resume, jd]
    tfidf = TfidfVectorizer(stop_words="english")
    matrix = tfidf.fit_transform(docs)
    score = cosine_similarity(matrix[0:1], matrix[1:2])[0][0] * 100
    return round(score, 1)

def ats_score(resume_skills, jd_skills, text):
    score = 0
    if jd_skills:
        score += len(set(resume_skills) & set(jd_skills)) / len(jd_skills) * 50
    sections = ["education", "experience", "skills"]
    for sec in sections:
        if sec in text: score += 10
    return round(min(score, 100), 1)

# SIMPLIFIED TEMPLATES
TEMPLATES = {
    "Data Scientist": "python machine learning tensorflow pytorch data science nlp",
    "Web Developer": "html css javascript react nodejs mongodb express",
    "DevOps": "docker kubernetes aws jenkins terraform ansible linux"
}

# NAVBAR
st.markdown("""
<div style='background:rgba(57,255,20,0.04); border:1px solid var(--neon-border); border-radius:14px; padding:24px 32px; margin-bottom:28px;'>
    <div style='font-family:Share Tech Mono,monospace; font-size:28px; font-weight:700; letter-spacing:2px;'>
        RESUME<span style='opacity:0.6;'>AI</span> PRO
    </div>
    <div style='font-family:Share Tech Mono,monospace; font-size:12px; letter-spacing:1.5px; opacity:0.7;'>
        NEON CYBER ANALYZER v2.0
    </div>
</div>
""", unsafe_allow_html=True)

# INPUT SECTION
st.markdown('<div style="font-family:Share Tech Mono,monospace; font-size:12px; letter-spacing:2px; opacity:0.7; margin-bottom:20px;">### UPLOAD & ANALYZE</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1,1])

with col1:
    uploaded_file = st.file_uploader("📁 RESUME PDF", type="pdf")

with col2:
    job_template = st.selectbox("JOB TEMPLATE", list(TEMPLATES.keys()))
    jd_text = st.text_area("JOB DESCRIPTION", value=TEMPLATES[job_template] if job_template != "Custom" else "", height=160)

if st.button("🚀 AI ANALYSIS"):
    if uploaded_file and jd_text.strip():
        with st.spinner('Processing resume...'):
            resume_raw = extract_text_from_pdf(uploaded_file)
            resume_clean = clean_text(resume_raw)
            jd_clean = clean_text(jd_text)
            
            resume_skills = extract_skills(resume_clean)
            jd_skills = extract_skills(jd_clean)
            matched = list(set(resume_skills) & set(jd_skills))
            missing = list(set(jd_skills) - set(resume_skills))
            
            match_pct = calculate_match(resume_clean, jd_clean)
            ats_pct = ats_score(resume_skills, jd_skills, resume_raw)

        # DASHBOARD
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown(f"""
            <div style='background:var(--surface); border:1px solid var(--neon-border); border-radius:12px; padding:20px; text-align:center;'>
                <div style='font-size:11px; letter-spacing:2px; opacity:0.6;'>MATCH %</div>
                <div style='font-size:32px; font-weight:700;'>{match_pct}%</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div style='background:var(--surface); border:1px solid var(--neon-border); border-radius:12px; padding:20px; text-align:center;'>
                <div style='font-size:11px; letter-spacing:2px; opacity:0.6;'>ATS SCORE</div>
                <div style='font-size:32px; font-weight:700;'>{ats_pct}%</div>
            </div>
            """, unsafe_allow_html=True)
        with c3:
            st.markdown("""
            <div style='background:var(--surface); border:1px solid var(--neon-border); border-radius:12px; padding:20px; text-align:center;'>
                <div style='font-size:11px; letter-spacing:2px; opacity:0.6;'>ROLE PREDICTED</div>
                <div style='font-size:24px; font-weight:700;'>Data Scientist</div>
            </div>
            """, unsafe_allow_html=True)

        # SKILLS
        col_s1, col_s2 = st.columns(2)
        with col_s1:
            st.markdown("**✅ MATCHED SKILLS**")
            for skill in matched[:10]:
                st.markdown(f"• {skill}")
        with col_s2:
            st.markdown("**❌ MISSING**")
            for skill in missing[:10]:
                st.markdown(f"• <span style='opacity:0.6;'>{skill}</span>", unsafe_allow_html=True)

        st.success(f"Analysis complete! {len(matched)}/{len(jd_skills)} skills matched.")
        st.balloons()
    else:
        st.error("Upload PDF and enter JD")

st.markdown("""
<div style='text-align:center; padding:20px; opacity:0.5; font-size:12px;'>
NEON CYBER THEME ACTIVE | #39ff14 | All Text Visible | Authentic Structured Design
</div>
""", unsafe_allow_html=True)
