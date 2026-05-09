import os
import re
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# -----------------------------
# LOAD JOB DESCRIPTION
# -----------------------------

def load_job_description(filepath):

    with open(filepath, "r", encoding="utf-8") as file:

        return file.read()


# -----------------------------
# LOAD RESUMES
# -----------------------------

def load_resumes(folder_path):

    resumes = []

    for filename in os.listdir(folder_path):

        file_path = os.path.join(folder_path, filename)

        with open(file_path, "r", encoding="utf-8") as file:

            content = file.read()

            resumes.append({

                "filename": filename,
                "content": content

            })

    return resumes


# -----------------------------
# CLEAN TEXT
# -----------------------------

def clean_text(text):

    text = text.lower()

    text = re.sub(r"[^a-zA-Z0-9 ]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text


# -----------------------------
# SKILLS DATABASE
# -----------------------------

skills_database = [

    "python",
    "sql",
    "power bi",
    "excel",
    "pandas",
    "machine learning",
    "statistics",
    "tableau",
    "data visualization",
    "java",
    "react",
    "html",
    "css"

]


# -----------------------------
# EXTRACT SKILLS
# -----------------------------

def extract_skills(text):

    found_skills = []

    for skill in skills_database:

        if skill.lower() in text.lower():

            found_skills.append(skill)

    return found_skills


# -----------------------------
# CALCULATE ATS SCORE
# -----------------------------

def calculate_similarity(job_description, resume_text):

    documents = [job_description, resume_text]

    tfidf = TfidfVectorizer()

    tfidf_matrix = tfidf.fit_transform(documents)

    similarity = cosine_similarity(

        tfidf_matrix[0:1],
        tfidf_matrix[1:2]

    )

    return round(similarity[0][0] * 100, 2)


# -----------------------------
# MAIN SCREENING FUNCTION
# -----------------------------

def screen_resumes():

    # Load Job Description

    job_description = load_job_description(

        "job_descriptions/data_analyst.txt"

    )

    cleaned_jd = clean_text(job_description)

    # Load Resumes

    resumes = load_resumes("resumes")

    results = []

    # Process Each Resume

    for resume in resumes:

        filename = resume["filename"]

        content = resume["content"]

        cleaned_resume = clean_text(content)

        # Extract Skills

        skills = extract_skills(cleaned_resume)

        # Calculate ATS Score

        score = calculate_similarity(

            cleaned_jd,
            cleaned_resume

        )

        # Shortlist Decision

        if score >= 50:

            status = "Shortlisted"

        else:

            status = "Rejected"

        # Store Results

        results.append({

            "Resume": filename,
            "ATS Score": score,
            "Skills": ", ".join(skills),
            "Status": status

        })

    # Create DataFrame

    df = pd.DataFrame(results)

    # Rank Candidates

    df = df.sort_values(

        by="ATS Score",
        ascending=False

    )

    # Save CSV Report

    output_path = "outputs/resume_ranking_report.csv"

    df.to_csv(output_path, index=False)

    # Print Results

    print("\n========== ATS SCREENING RESULTS ==========\n")

    print(df)

    print("\nCSV Report Saved Successfully!")

    print(f"\nLocation: {output_path}")


# -----------------------------
# RUN PROJECT
# -----------------------------

if __name__ == "__main__":

    screen_resumes()