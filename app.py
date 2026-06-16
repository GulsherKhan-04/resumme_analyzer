import streamlit as st
import pdfplumber
import re
import spacy

from skills_db import skills_db

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# --------------------------
# Load Models
# --------------------------

@st.cache_resource
def load_spacy_model():
    return spacy.load("en_core_web_sm")

@st.cache_resource
def load_sentence_transformer():
    return SentenceTransformer("all-MiniLM-L6-v2")

# --------------------------
# PDF Extraction
# --------------------------

def extract_pdf_text(pdf_file):

    text = ""

    with pdfplumber.open(pdf_file) as pdf:

        for page in pdf.pages:

            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text


# --------------------------
# Clean Text
# --------------------------

def clean_text(text):

    text = text.lower()

    text = re.sub(
        r'[^a-zA-Z0-9 ]',
        ' ',
        text
    )

    text = re.sub(
        r'\s+',
        ' ',
        text
    )

    return text


# --------------------------
# Extract Email
# --------------------------

def extract_email(text):

    emails = re.findall(
        r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}',
        text
    )

    return emails[0] if emails else "Not Found"


# --------------------------
# Extract Phone
# --------------------------

def extract_phone(text):

    phones = re.findall(
        r'\+?\d[\d\s-]{8,15}',
        text
    )

    return phones[0] if phones else "Not Found"


# --------------------------
# Extract Name
# --------------------------

def extract_name(text):

    nlp = load_spacy_model()
    doc = nlp(text)

    for ent in doc.ents:

        if ent.label_ == "PERSON":
            return ent.text

    return "Not Found"


# --------------------------
# Extract Skills
# --------------------------

def extract_skills(text):

    text = text.lower()

    found = []

    for skill in skills_db:

        if skill.lower() in text:
            found.append(skill)

    return sorted(list(set(found)))


# --------------------------
# Semantic Similarity
# --------------------------

def semantic_similarity(
    resume_text,
    jd_text
):

    model = load_sentence_transformer()

    resume_emb = model.encode(
        resume_text
    )

    jd_emb = model.encode(
        jd_text
    )

    score = cosine_similarity(
        [resume_emb],
        [jd_emb]
    )[0][0]

    return round(score * 100, 2)


# --------------------------
# ATS Keyword Match Score
# --------------------------

def keyword_match_score(
    resume_skills,
    jd_skills
):

    if not jd_skills:
        return 0.0

    matched = set(resume_skills) & set(jd_skills)

    return round(len(matched) / len(jd_skills) * 100, 2)


# --------------------------
# Missing Skills
# --------------------------

def missing_skills(
    resume_skills,
    jd_skills
):

    missing = list(
        set(jd_skills)
        -
        set(resume_skills)
    )

    return sorted(missing)


# --------------------------
# Recommendations
# --------------------------

def build_recommendations(
    resume_skills,
    jd_skills,
    missing
):

    recommendations = []

    if not jd_skills:
        recommendations.append("Add a job description to calculate match score.")
    elif not missing:
        recommendations.append(
            "Good match for the provided job description."
        )
        recommendations.append(
            "Resume contains all required technical keywords: "
            + ", ".join(sorted(jd_skills))
            + "."
        )
    else:
        recommendations.append(
            "Resume is missing some required keywords."
        )
        recommendations.append(
            "Add or highlight: "
            + ", ".join(sorted(missing))
            + "."
        )

    recommendations.extend([
        "Add links to GitHub projects.",
        "Quantify project achievements.",
        "Add internship or experience details if available.",
        "Mention Docker and Git usage inside project descriptions."
    ])

    return recommendations


# --------------------------
# Streamlit UI
# --------------------------

st.set_page_config(
    page_title="Resume Analyzer",
    layout="wide"
)

st.title("NLP Resume Analyzer")

resume_file = st.file_uploader(
    "Upload Resume PDF",
    type=["pdf"]
)

job_description = st.text_area(
    "Paste Job Description"
)

if resume_file and job_description:

    resume_text = extract_pdf_text(
        resume_file
    )

    cleaned_resume = clean_text(
        resume_text
    )

    name = extract_name(
        resume_text
    )

    email = extract_email(
        resume_text
    )

    phone = extract_phone(
        resume_text
    )

    skills = extract_skills(
        cleaned_resume
    )

    cleaned_jd = clean_text(
        job_description
    )

    jd_skills = extract_skills(
        cleaned_jd
    )

    ats_score = keyword_match_score(
        skills,
        jd_skills
    )

    semantic_score = semantic_similarity(
        resume_text,
        job_description
    )

    missing = missing_skills(
        skills,
        jd_skills
    )

    recommendations = build_recommendations(
        skills,
        jd_skills,
        missing
    )

    st.header("Candidate Details")

    st.write(
        f"Name: {name}"
    )

    st.write(
        f"Email: {email}"
    )

    st.write(
        f"Phone: {phone}"
    )

    st.header("Skills")

    st.write(skills)

    st.header("ATS Match Score")

    st.progress(
        int(ats_score)
    )

    st.metric(
        "Score",
        f"{ats_score}%"
    )

    st.write("**Semantic similarity:**")
    st.write(f"{semantic_score}%")

    st.header("Missing Skills")

    st.write(missing)

    st.header("Suggestions")

    for suggestion in recommendations:
        st.write(f"- {suggestion}")


    st.header(
        "Missing Skills"
    )

    st.write(missing)


    if missing:
        st.write(missing)
    else:
        st.success(
            "No Missing Skills Found"
        )

    st.header(
        "Suggestions"
    )

    if ats_score < 50:

        st.warning(
            "Resume is weak for this job."
        )

    elif ats_score < 75:

        st.info(
            "Add missing skills and improve project descriptions."
        )

    else:

        st.success(
            "Resume is highly aligned with the job description."
        )