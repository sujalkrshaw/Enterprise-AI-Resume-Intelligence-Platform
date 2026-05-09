import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter


# -----------------------------
# LOAD CSV REPORT
# -----------------------------

df = pd.read_csv(
    "outputs/resume_ranking_report.csv"
)


# -----------------------------
# ATS SCORE BAR CHART
# -----------------------------

plt.figure(figsize=(10, 6))

plt.bar(
    df["Resume"],
    df["ATS Score"]
)

plt.title("ATS Score by Resume")

plt.xlabel("Resume")

plt.ylabel("ATS Score")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "outputs/ats_score_chart.png"
)

plt.close()


# -----------------------------
# SHORTLIST PIE CHART
# -----------------------------

status_counts = df["Status"].value_counts()

plt.figure(figsize=(6, 6))

plt.pie(
    status_counts,
    labels=status_counts.index,
    autopct="%1.1f%%"
)

plt.title("Shortlisted vs Rejected")

plt.savefig(
    "outputs/shortlist_pie_chart.png"
)

plt.close()


# -----------------------------
# SKILLS ANALYSIS
# -----------------------------

all_skills = []

for skills in df["Skills"]:

    # Handle empty or NaN values

    if pd.isna(skills):

        continue

    split_skills = str(skills).split(",")

    for skill in split_skills:

        skill = skill.strip()

        if skill != "":

            all_skills.append(skill)


skill_counts = Counter(all_skills)

skills_df = pd.DataFrame({

    "Skill": list(skill_counts.keys()),
    "Count": list(skill_counts.values())

})

skills_df = skills_df.sort_values(
    by="Count",
    ascending=False
)


# -----------------------------
# SKILLS BAR GRAPH
# -----------------------------

plt.figure(figsize=(10, 6))

plt.bar(
    skills_df["Skill"],
    skills_df["Count"]
)

plt.title("Most Common Skills")

plt.xlabel("Skills")

plt.ylabel("Frequency")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "outputs/skills_chart.png"
)

plt.close()


# -----------------------------
# TOP CANDIDATES GRAPH
# -----------------------------

top_candidates = df.head(5)

plt.figure(figsize=(10, 6))

plt.plot(
    top_candidates["Resume"],
    top_candidates["ATS Score"],
    marker="o"
)

plt.title("Top Candidate Rankings")

plt.xlabel("Resume")

plt.ylabel("ATS Score")

plt.grid(True)

plt.tight_layout()

plt.savefig(
    "outputs/top_candidates_chart.png"
)

plt.close()


# -----------------------------
# SUCCESS MESSAGE
# -----------------------------

print("\nVisualization Reports Generated Successfully!")

print("\nCharts saved inside outputs/")