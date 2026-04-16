import re

SKILLS_DB = [
    "python", "java", "c", "c++", "javascript", "html", "css", "react",
    "nodejs", "express", "mongodb", "sql", "mysql", "postgresql",
    "machine learning", "deep learning", "nlp", "data science",
    "tensorflow", "pytorch", "flask", "django", "streamlit",
    "git", "github", "docker", "kubernetes",
    "aws", "azure", "gcp",
    "power bi", "tableau", "excel",
    "linux", "api", "rest api",
    "firebase", "cloud computing", "cyber security"
]

def extract_skills(text):
    text = text.lower()
    found_skills = set()

    for skill in SKILLS_DB:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, text):
            found_skills.add(skill)

    return sorted(found_skills)