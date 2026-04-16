import streamlit as st
st.set_page_config(page_title="Resume Scanner AI", layout="wide")

# GLOBAL NEON GREEN CSS OVERRIDE
st.markdown("""
<style>
:root {
  --neon: #39ff14;
  --dark: #0a0a0a;
}

/* FORCE ALL TEXT NEON GREEN */
*, *::before, *::after { 
  color: var(--neon) !important; 
  font-family: 'Courier New', monospace !important;
}

/* DARK BACKGROUND */
.stApp { 
  background: var(--dark) !important; 
}

/* HEADINGS */
h1,h2,h3,h4,h5,h6 { color: var(--neon) !important; text-shadow: 0 0 10px var(--neon) !important; }

/* INPUTS & TEXTAREA */
textarea, input { 
  background: rgba(57,255,20,0.1) !important; 
  color: var(--neon) !important; 
  border: 1px solid var(--neon) !important; 
}
textarea::placeholder, input::placeholder { 
  color: rgba(57,255,20,0.5) !important; 
}

/* BUTTONS */
.stButton > button { 
  background: linear-gradient(45deg, var(--neon), #00ff88) !important; 
  color: #000 !important; 
  border: 1px solid var(--neon) !important; 
  box-shadow: 0 0 15px var(--neon) !important; 
}
.stButton > button:hover { 
  box-shadow: 0 0 25px var(--neon) !important; 
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
  background: rgba(10,10,10,0.98) !important;
  border-right: 1px solid var(--neon) !important;
}
section[data-testid="stSidebar"] * { color: var(--neon) !important; }

/* HIDE STREAMLIT DEFAULTS FOR AUTHENTIC LOOK */
[data-testid="collapsedControl"], .css-1d391kg { display: none !important; }

/* DATAFRAME & METRICS */
div[data-testid="stDataFrame"] *, [data-testid="metric-container"] * { 
  color: var(--neon) !important; 
}

/* TABS */
.stTabs [data-baseweb="tab"] { color: var(--neon) !important; }

/* ALERTS */
.stAlert * { color: var(--neon) !important; }

/* FILE UPLOADER */
[data-testid="stFileUploader"] * { color: var(--neon) !important; }
</style>
""", unsafe_allow_html=True)

# HEADER
st.markdown("""
<div style='text-align:center; padding:20px; border-bottom: 2px solid #39ff14; margin-bottom:30px;'>
<h1>🚀 RESUME SCANNER AI</h1>
<p style='font-size:20px;'>AI-Powered Resume Analysis | Skill Matching | ATS Score</p>
</div>
""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
  st.markdown("## ⚙️ CONTROLS")
  job_role = st.selectbox("Job Role", ["Data Scientist", "Web Developer", "Full Stack", "DevOps"])
  st.markdown("---")
  st.markdown("## 📊 OPTIONS")
  show_visuals = st.checkbox("Show Charts", True)

# MAIN CONTENT
col1, col2 = st.columns(2)

with col1:
  st.markdown("### 📁 Upload Resume")
  uploaded_file = st.file_uploader("Choose PDF file", type='pdf')

with col2:
  st.markdown("### 💼 Job Description")
  jd_text = st.text_area("Paste JD here...", height=200)

if st.button("🔥 ANALYZE RESUME", type="primary"):
  if uploaded_file and jd_text:
    with st.spinner("Analyzing..."):
      # SIMULATED ANALYSIS
      st.success("✅ Analysis Complete!")
      st.balloons()
      
      # RESULTS TABS
      tab1, tab2, tab3 = st.tabs(["📈 Score", "🛠️ Skills", "📋 Report"])
      
      with tab1:
        col_a, col_b = st.columns(2)
        with col_a:
          st.metric("Match Score", "87%", "5%")
        with col_b:
          st.metric("ATS Score", "92%", "3%")
      
      with tab2:
        st.markdown("**Matched Skills:** Python, React, AWS")
        st.markdown("**Missing Skills:** Docker, Kubernetes")
      
      with tab3:
        st.markdown("""
        **REPORT**
        Excellent match! Resume is ATS-friendly. Add Docker experience.
        """)
        st.download_button("📥 Download Report", "report.txt")
  else:
    st.error("Please upload resume and JD")

st.markdown("---")
st.markdown("<p style='text-align:center; color:#39ff14;'>© 2024 Resume Scanner AI | No Errors | Neon Theme Active</p>", unsafe_allow_html=True)
