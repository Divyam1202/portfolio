import json
import re
from pdfminer.high_level import extract_text

def extract_resume_data(pdf_path):
    text = extract_text(pdf_path)
    
    # Extracting various sections of the resume using regex
    name = re.search(r'^[\w\s]+', text).group(0).strip()
    email = re.search(r'[\w\.-]+@[\w\.-]+', text).group(0).strip()
    linkedin = re.search(r'linkedin\.com/in/\S+', text).group(0).strip()
    github = re.search(r'github\.com/\S+', text).group(0).strip()
    phone = re.search(r'\+\d{2}\s\d{10}', text).group(0).strip()
    
    # Extracting sections based on headings
    education = re.findall(r'(EDUCATION\n[\s\S]+?)(?=\n[A-Z]+|\Z)', text)
    skills = re.findall(r'(SKILLS\n[\s\S]+?)(?=\n[A-Z]+|\Z)', text)
    projects = re.findall(r'(ACADEMIC PROJECTS\n[\s\S]+?)(?=\n[A-Z]+|\Z)', text)
    experience = re.findall(r'(INDUSTRY EXPERIENCE\n[\s\S]+?)(?=\n[A-Z]+|\Z)', text)
    certificates = re.findall(r'(CERTIFICATES\n[\s\S]+?)(?=\n[A-Z]+|\Z)', text)
    activities = re.findall(r'(EXTRA-CURRICULAR ACTIVITIES\n[\s\S]+?)(?=\n[A-Z]+|\Z)', text)
    
    def clean_section(section):
        return section.split('\n')[1:]  # Remove heading

    resume_data = {
        "name": name,
        "contact_info": {
            "email": email,
            "linkedin": linkedin,
            "github": github,
            "phone": phone
        },
        "education": clean_section(education[0]) if education else [],
        "skills": clean_section(skills[0]) if skills else [],
        "projects": clean_section(projects[0]) if projects else [],
        "experience": clean_section(experience[0]) if experience else [],
        "certificates": clean_section(certificates[0]) if certificates else [],
        "extra_curricular_activities": clean_section(activities[0]) if activities else []
    }
    
    return resume_data

# Specify the path to the PDF file
pdf_path = '/home/divyam/Downloads/Divyam_Resume.pdf'

# Extract resume data and convert to JSON
resume_data = extract_resume_data(pdf_path)
resume_json = json.dumps(resume_data, indent=4)
print(resume_json)
