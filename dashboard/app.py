import streamlit as st
import pandas as pd
import plotly.express as px
import re
import sys
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from PyPDF2 import PdfReader
from docx import Document


# =========================================================
# PATH FIX
# =========================================================

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

from src.enterprise_analysis import analyze_resume


# =========================================================
# FILE READING FUNCTIONS
# =========================================================

def read_pdf(file):

    text = ""

    pdf_reader = PdfReader(file)

    for page in pdf_reader.pages:

        extracted = page.extract_text()

        if extracted:

            text += extracted

    return text


def read_docx(file):

    doc = Document(file)

    text = ""

    for para in doc.paragraphs:

        text += para.text + "\n"

    return text


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(

    page_title="Enterprise AI Resume Intelligence Platform",

    page_icon="🚀",

    layout="wide"

)


# =========================================================
# ULTRA PREMIUM CSS
# =========================================================

st.markdown(
    """
    <style>

    .stApp {
        background: linear-gradient(135deg, #050816, #0F172A, #111827, #1E293B);
        color: #FFFFFF;
    }

    .main-title {
        font-size: 52px;
        font-weight: 900;
        text-align: center;
        padding: 28px;
        border-radius: 24px;
        background: linear-gradient(90deg, #7F5AF0, #2CB67D, #00C2FF);
        color: white;
        box-shadow: 0px 0px 35px rgba(127,90,240,0.6);
        margin-bottom: 25px;
        letter-spacing: 1px;
    }

    .highlight-box {
        background: linear-gradient(135deg, #111827, #1E293B);
        padding: 22px;
        border-radius: 22px;
        border: 2px solid #7F5AF0;
        box-shadow: 0px 0px 18px rgba(127,90,240,0.4);
        margin-top: 12px;
        margin-bottom: 18px;
    }

    .stMetric {
        background: linear-gradient(135deg, #111827, #1F2937);
        padding: 20px;
        border-radius: 18px;
        border: 2px solid #00C2FF;
        box-shadow: 0px 0px 15px rgba(0,194,255,0.3);
    }

    h1 {
        color: #00F5D4;
        font-weight: 900;
    }

    h2 {
        color: #7F5AF0;
        font-weight: 800;
    }

    h3 {
        color: #2CB67D;
        font-weight: 700;
    }

    p, label, div {
        color: #F8FAFC;
    }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #111827, #0F172A, #1E293B);
        border-right: 2px solid #7F5AF0;
    }

    .stButton>button {
        background: linear-gradient(90deg, #7F5AF0, #00C2FF);
        color: white;
        border-radius: 14px;
        border: none;
        font-size: 16px;
        font-weight: bold;
        padding: 12px 22px;
    }

    .stDownloadButton>button {
        background: linear-gradient(90deg, #F97316, #FACC15);
        color: white;
        border-radius: 14px;
        border: none;
        font-weight: bold;
        padding: 12px 20px;
    }

    div[data-testid="stDataFrame"] {
        background-color: #111827;
        border-radius: 18px;
        border: 2px solid #00C2FF;
        padding: 12px;
    }

    textarea {
        border-radius: 12px !important;
        border: 2px solid #7F5AF0 !important;
        background-color: #111827 !important;
        color: white !important;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# LOAD DATA
# =========================================================

try:

    df = pd.read_csv(
        "outputs/resume_ranking_report.csv"
    )

except:

    df = pd.DataFrame({

        "Resume": [],
        "ATS Score": [],
        "Skills": [],
        "Status": []

    })


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("🚀 Enterprise AI ATS")

st.sidebar.markdown("---")

st.sidebar.info(
    """
    Enterprise AI Resume Intelligence Platform

    ✅ ATS Resume Screening
    ✅ Resume Upload
    ✅ Recruiter Intelligence
    ✅ Career Guidance
    ✅ Interview Preparation
    ✅ Business Insights
    """
)


# =========================================================
# MAIN TITLE
# =========================================================

st.markdown(
    """
    <div class='main-title'>
    🚀 Enterprise AI Resume Intelligence & Career Optimization Platform
    </div>
    """,
    unsafe_allow_html=True
)


# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([

    "📊 Dashboard",

    "🤖 ATS Prediction",

    "📈 Insights",

    "📋 Reports",

    "🧠 Enterprise AI"

])


# =========================================================
# TAB 1 — DASHBOARD
# =========================================================

with tab1:

    st.markdown(
        "<div class='highlight-box'><h2>📊 ATS Dashboard Analytics</h2></div>",
        unsafe_allow_html=True
    )

    total_resumes = len(df)

    shortlisted = len(
        df[df["Status"] == "Shortlisted"]
    ) if len(df) > 0 else 0

    rejected = len(
        df[df["Status"] == "Rejected"]
    ) if len(df) > 0 else 0

    average_score = round(
        df["ATS Score"].mean(),
        2
    ) if len(df) > 0 else 0

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Resumes", total_resumes)
    c2.metric("Shortlisted", shortlisted)
    c3.metric("Rejected", rejected)
    c4.metric("Average ATS Score", average_score)

    st.markdown("---")

    if len(df) > 0:

        fig_bar = px.bar(
            df,
            x="Resume",
            y="ATS Score",
            color="Status",
            text="ATS Score"
        )

        st.plotly_chart(
            fig_bar,
            use_container_width=True
        )

        fig_pie = px.pie(
            df,
            names="Status",
            hole=0.5
        )

        st.plotly_chart(
            fig_pie,
            use_container_width=True
        )

        st.dataframe(
            df.sort_values(
                by="ATS Score",
                ascending=False
            ),
            use_container_width=True
        )


# =========================================================
# TAB 2 — ATS PREDICTION
# =========================================================

with tab2:

    st.markdown(
        "<div class='highlight-box'><h2>🤖 ATS Prediction System</h2></div>",
        unsafe_allow_html=True
    )

    jd = st.text_area(
        "Enter Job Description"
    )

    resume = st.text_area(
        "Paste Resume Content"
    )

    if st.button("Analyze Resume"):

        if jd and resume:

            documents = [jd, resume]

            tfidf = TfidfVectorizer()

            tfidf_matrix = tfidf.fit_transform(documents)

            similarity = cosine_similarity(
                tfidf_matrix[0:1],
                tfidf_matrix[1:2]
            )

            ats_score = round(
                similarity[0][0] * 100,
                2
            )

            st.success(
                f"ATS Score: {ats_score}%"
            )

        else:

            st.warning(
                "Please enter both Job Description and Resume."
            )


# =========================================================
# TAB 3 — INSIGHTS
# =========================================================

with tab3:

    st.markdown(
        "<div class='highlight-box'><h2>📈 Recruitment Insights</h2></div>",
        unsafe_allow_html=True
    )

    if len(df) > 0:

        highest_score = df["ATS Score"].max()

        lowest_score = df["ATS Score"].min()

        shortlist_rate = round(
            (shortlisted / total_resumes) * 100,
            2
        )

        b1, b2, b3 = st.columns(3)

        b1.metric(
            "Highest ATS Score",
            highest_score
        )

        b2.metric(
            "Lowest ATS Score",
            lowest_score
        )

        b3.metric(
            "Shortlist Rate",
            f"{shortlist_rate}%"
        )


# =========================================================
# TAB 4 — REPORTS
# =========================================================

with tab4:

    st.markdown(
        "<div class='highlight-box'><h2>📋 Reports & Downloads</h2></div>",
        unsafe_allow_html=True
    )

    if len(df) > 0:

        csv = df.to_csv(index=False)

        st.download_button(
            label="⬇ Download Resume Report CSV",
            data=csv,
            file_name="resume_ranking_report.csv",
            mime="text/csv"
        )

        st.dataframe(
            df,
            use_container_width=True
        )


# =========================================================
# TAB 5 — ENTERPRISE AI
# =========================================================

with tab5:

    st.markdown(
        "<div class='highlight-box'><h2>🧠 Enterprise AI Resume Intelligence Engine</h2></div>",
        unsafe_allow_html=True
    )

    company = st.selectbox(
        "Select Company",
        [
            "Google",
            "Microsoft",
            "Amazon",
            "TCS",
            "Infosys",
            "Accenture",
            "Wipro",
            "Startup"
        ]
    )

    role = st.selectbox(
        "Select Role",
        [
            "Python Developer",
            "Data Analyst",
            "AI/ML Intern",
            "NLP Engineer",
            "Frontend Developer"
        ]
    )

    job_descriptions = {

        "Python Developer":
        "Python SQL APIs Backend Development Automation",

        "Data Analyst":
        "Python SQL Excel Power BI Pandas Visualization",

        "AI/ML Intern":
        "Python Machine Learning NLP Scikit-learn TensorFlow",

        "NLP Engineer":
        "NLP TF-IDF Text Processing Machine Learning Python",

        "Frontend Developer":
        "React JavaScript HTML CSS UI UX"
    }

    selected_jd = job_descriptions[role]

    st.subheader("📋 Auto Generated Job Description")

    st.info(selected_jd)

    uploaded_file = st.file_uploader(
        "Upload Resume",
        type=["pdf", "docx", "txt"]
    )

    enterprise_resume = ""

    if uploaded_file is not None:

        file_type = uploaded_file.name.split(".")[-1]

        if file_type == "pdf":

            enterprise_resume = read_pdf(uploaded_file)

        elif file_type == "docx":

            enterprise_resume = read_docx(uploaded_file)

        elif file_type == "txt":

            enterprise_resume = str(
                uploaded_file.read(),
                "utf-8"
            )

        st.success("Resume uploaded successfully!")

    if st.button("Run Enterprise AI Analysis"):

        if enterprise_resume:

            combined_resume = enterprise_resume + " " + selected_jd

            result = analyze_resume(combined_resume)

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "ATS Score",
                result["ATS Score"]
            )

            c2.metric(
                "Recruiter Confidence",
                result["Recruiter Confidence"]
            )

            c3.metric(
                "Shortlisting Prediction",
                result["Shortlisting Prediction"]
            )

            st.subheader("✅ Skills")

            st.write(result["Skills"])

            st.subheader("❌ Missing Skills")

            st.write(result["Missing Skills"])

            st.subheader("💪 Strengths")

            for strength in result["Strengths"]:

                st.success(strength)

            st.subheader("⚠️ Weaknesses")

            for weakness in result["Weaknesses"]:

                st.warning(weakness)

            st.subheader("🚀 Career Roadmap")

            for item in result["Career Roadmap"]:

                st.info(item)

            st.subheader("🎯 Interview Questions")

            for question in result["Interview Questions"]:

                st.write(f"• {question}")

        else:

            st.warning(
                "Please upload a resume first."
            )


# =========================================================
# FINAL SUCCESS MESSAGE
# =========================================================

st.success(
    "🚀 Enterprise AI Resume Intelligence Platform Loaded Successfully!"
)