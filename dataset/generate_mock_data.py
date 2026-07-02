import pandas as pd
import numpy as np

# Job roles to cover
JOB_ROLES = [
    "Frontend Developer", "Backend Developer", "Full Stack Developer",
    "Python Developer", "Java Developer", "Data Scientist",
    "Machine Learning Engineer", "DevOps Engineer", "Cloud Engineer",
    "Cybersecurity Analyst", "UI/UX Designer", "Data Analyst",
    "Business Analyst", "Android Developer", "Software Engineer"
]

def generate_resume_data(num_samples=1000):
    np.random.seed(42)
    data = []
    
    # Common skills dictionary for generating text
    skills_dict = {
        "Frontend Developer": ["HTML", "CSS", "JavaScript", "React", "Vue", "Angular", "Tailwind", "TypeScript"],
        "Backend Developer": ["Node.js", "Express", "Python", "Django", "FastAPI", "Java", "Spring Boot", "SQL", "MongoDB"],
        "Full Stack Developer": ["React", "Node.js", "MongoDB", "Express", "Python", "SQL", "TypeScript", "Docker"],
        "Python Developer": ["Python", "Django", "Flask", "FastAPI", "SQLAlchemy", "PostgreSQL", "REST APIs"],
        "Java Developer": ["Java", "Spring Boot", "Hibernate", "Microservices", "SQL", "Kafka", "REST"],
        "Data Scientist": ["Python", "Pandas", "NumPy", "Scikit-Learn", "TensorFlow", "SQL", "Statistics", "Machine Learning"],
        "Machine Learning Engineer": ["Python", "PyTorch", "TensorFlow", "Scikit-Learn", "NLP", "Computer Vision", "Docker"],
        "DevOps Engineer": ["AWS", "Docker", "Kubernetes", "CI/CD", "Jenkins", "Terraform", "Linux", "Bash"],
        "Cloud Engineer": ["AWS", "Azure", "GCP", "Docker", "Kubernetes", "Networking", "Terraform"],
        "Cybersecurity Analyst": ["Network Security", "Penetration Testing", "SIEM", "Wireshark", "Firewalls", "Linux"],
        "UI/UX Designer": ["Figma", "Adobe XD", "Sketch", "Prototyping", "Wireframing", "User Research", "CSS"],
        "Data Analyst": ["SQL", "Excel", "Tableau", "PowerBI", "Python", "Pandas", "Data Visualization"],
        "Business Analyst": ["Agile", "Scrum", "Requirements Gathering", "SQL", "Jira", "Stakeholder Management"],
        "Android Developer": ["Java", "Kotlin", "Android Studio", "XML", "REST APIs", "Firebase"],
        "Software Engineer": ["Java", "Python", "C++", "Data Structures", "Algorithms", "Git", "SQL"]
    }
    
    for _ in range(num_samples):
        role = np.random.choice(JOB_ROLES)
        
        # Generate some synthetic text
        relevant_skills = np.random.choice(skills_dict[role], size=np.random.randint(4, len(skills_dict[role])+1), replace=False)
        irrelevant_skills = np.random.choice(skills_dict[np.random.choice(JOB_ROLES)], size=np.random.randint(0, 3), replace=False)
        
        all_skills = list(relevant_skills) + list(irrelevant_skills)
        np.random.shuffle(all_skills)
        
        # Create a synthetic resume text block
        resume_text = f"Experienced {role} with a strong background in developing scalable applications. "
        resume_text += f"Proficient in {', '.join(all_skills)}. "
        resume_text += f"Worked on various projects utilizing these skills to deliver business value. "
        resume_text += f"Strong understanding of software development lifecycle and best practices."
        
        data.append({"Resume": resume_text, "Role": role})
        
    df = pd.DataFrame(data)
    df.to_csv("dataset/resume_dataset.csv", index=False)
    print(f"Generated dataset/resume_dataset.csv with {len(df)} samples.")

def generate_jobs_data(num_samples=150):
    np.random.seed(24)
    data = []
    
    skills_dict = {
        "Frontend Developer": "HTML, CSS, JavaScript, React",
        "Backend Developer": "Node.js, Python, SQL, REST APIs",
        "Full Stack Developer": "React, Node.js, MongoDB, Docker",
        "Python Developer": "Python, FastAPI, PostgreSQL",
        "Java Developer": "Java, Spring Boot, SQL",
        "Data Scientist": "Python, Pandas, Machine Learning, SQL",
        "Machine Learning Engineer": "Python, PyTorch, Docker, NLP",
        "DevOps Engineer": "AWS, Docker, Kubernetes, CI/CD",
        "Cloud Engineer": "AWS, Azure, Terraform",
        "Cybersecurity Analyst": "Network Security, SIEM, Linux",
        "UI/UX Designer": "Figma, Prototyping, Wireframing",
        "Data Analyst": "SQL, Excel, Tableau",
        "Business Analyst": "Agile, Jira, SQL",
        "Android Developer": "Kotlin, Android Studio, Firebase",
        "Software Engineer": "Java, Python, Algorithms, Git"
    }
    
    companies = ["Google", "Microsoft", "Amazon", "Meta", "Apple", "Netflix", "Tesla", "Uber", "Airbnb", "Spotify", "Startup Inc.", "TechCorp"]
    locations = ["New York, NY", "San Francisco, CA", "Seattle, WA", "Austin, TX", "London, UK", "Remote", "Berlin, DE"]
    
    for _ in range(num_samples):
        role = np.random.choice(JOB_ROLES)
        company = np.random.choice(companies)
        location = np.random.choice(locations)
        salary = f"${np.random.randint(60, 180)}k - ${np.random.randint(180, 250)}k"
        
        req_skills = skills_dict[role]
        description = f"We are looking for a skilled {role} to join {company}. You should be proficient in {req_skills}. "
        description += f"This is a {location} position offering {salary}."
        
        data.append({
            "id": f"job_{np.random.randint(1000, 9999)}",
            "title": role,
            "company": company,
            "description": description,
            "requiredSkills": req_skills.split(", "),
            "salary": salary,
            "location": location
        })
        
    df = pd.DataFrame(data)
    df.to_csv("dataset/jobs_dataset.csv", index=False)
    print(f"Generated dataset/jobs_dataset.csv with {len(df)} samples.")

if __name__ == "__main__":
    generate_resume_data()
    generate_jobs_data()
