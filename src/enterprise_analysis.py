import re


# -----------------------------------
# SKILLS DATABASE
# -----------------------------------

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
    "css",
    "aws",
    "azure",
    "tensorflow",
    "numpy"

]


# -----------------------------------
# CLEAN TEXT
# -----------------------------------

def clean_text(text):

    text = text.lower()

    text = re.sub(r"[^a-zA-Z0-9 ]", " ", text)

    text = re.sub(r"\s+", " ", text)

    return text


# -----------------------------------
# EXTRACT SKILLS
# -----------------------------------

def extract_skills(text):

    found_skills = []

    for skill in skills_database:

        if skill.lower() in text.lower():

            found_skills.append(skill)

    return found_skills


# -----------------------------------
# ATS SCORE ENGINE
# -----------------------------------

def generate_ats_score(skills_count):

    score = 40 + (skills_count * 5)

    return min(score, 95)


# -----------------------------------
# RECRUITER CONFIDENCE
# -----------------------------------

def recruiter_confidence(score):

    if score >= 85:

        return "High"

    elif score >= 65:

        return "Medium"

    else:

        return "Low"


# -----------------------------------
# SHORTLIST PREDICTION
# -----------------------------------

def shortlist_prediction(score):

    if score >= 85:

        return "Highly Recruitable"

    elif score >= 70:

        return "Strong"

    elif score >= 55:

        return "Average"

    else:

        return "Beginner"


# -----------------------------------
# SKILL GAP ANALYSIS
# -----------------------------------

def missing_skills(candidate_skills, required_skills):

    return list(

        set(required_skills) -

        set(candidate_skills)

    )


# -----------------------------------
# RESUME STRENGTHS
# -----------------------------------

def resume_strengths(score, skills):

    strengths = []

    if score >= 80:

        strengths.append(

            "Strong ATS compatibility"

        )

    if "python" in skills:

        strengths.append(

            "Python skill is highly valuable"

        )

    if "sql" in skills:

        strengths.append(

            "SQL is industry relevant"

        )

    if len(skills) >= 5:

        strengths.append(

            "Good technical skill diversity"

        )

    return strengths


# -----------------------------------
# RESUME WEAKNESSES
# -----------------------------------

def resume_weaknesses(score, missing):

    weaknesses = []

    if score < 70:

        weaknesses.append(

            "ATS score is below competitive level"

        )

    if len(missing) > 0:

        weaknesses.append(

            "Important skills are missing"

        )

    if len(missing) >= 3:

        weaknesses.append(

            "Resume lacks multiple industry keywords"

        )

    return weaknesses


# -----------------------------------
# CAREER ROADMAP
# -----------------------------------

def career_roadmap(missing):

    roadmap = []

    for skill in missing:

        roadmap.append(

            f"Learn {skill} through projects and certifications"

        )

    return roadmap


# -----------------------------------
# INTERVIEW QUESTIONS
# -----------------------------------

def generate_interview_questions(skills):

    questions = []

    if "python" in skills:

        questions.append(

            "Explain Python OOP concepts."

        )

    if "sql" in skills:

        questions.append(

            "Explain SQL joins."

        )

    if "machine learning" in skills:

        questions.append(

            "Explain overfitting in ML."

        )

    questions.append(

        "Explain your strongest project."

    )

    return questions


# -----------------------------------
# MAIN ANALYSIS ENGINE
# -----------------------------------

def analyze_resume(resume_text):

    required_skills = [

        "python",
        "sql",
        "power bi",
        "excel",
        "pandas",
        "machine learning"

    ]

    cleaned_resume = clean_text(

        resume_text

    )

    skills = extract_skills(

        cleaned_resume

    )

    score = generate_ats_score(

        len(skills)

    )

    confidence = recruiter_confidence(

        score

    )

    prediction = shortlist_prediction(

        score

    )

    gaps = missing_skills(

        skills,
        required_skills

    )

    strengths = resume_strengths(

        score,
        skills

    )

    weaknesses = resume_weaknesses(

        score,
        gaps

    )

    roadmap = career_roadmap(

        gaps

    )

    interview_questions = generate_interview_questions(

        skills

    )

    return {

        "ATS Score": score,

        "Recruiter Confidence": confidence,

        "Shortlisting Prediction": prediction,

        "Skills": skills,

        "Missing Skills": gaps,

        "Strengths": strengths,

        "Weaknesses": weaknesses,

        "Career Roadmap": roadmap,

        "Interview Questions": interview_questions

    }


# -----------------------------------
# TEST ENGINE
# -----------------------------------

if __name__ == "__main__":

    sample_resume = """

    Python SQL Pandas Excel Machine Learning

    """

    result = analyze_resume(

        sample_resume

    )

    for key, value in result.items():

        print(f"\n{key}:")

        print(value)