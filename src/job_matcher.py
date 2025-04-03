import logging
from difflib import SequenceMatcher
import os
from pymongo import MongoClient

# Connect to MongoDB
MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client["job_matching_db"]
jobs_collection = db["jobs"]

def get_all_jobs():
    """Fetch all jobs from the MongoDB collection."""
    return list(jobs_collection.find({}, {"_id": 0}))  # Exclude MongoDB's default '_id' field


# In-memory database of jobs
# In a real application, this would come from a database
# def get_all_jobs():
#     """Return a list of all available jobs."""
    # return [
    #     {
    #         "id": 1,
    #         "title": "Senior Software Engineer",
    #         "company": "Tech Innovators Inc.",
    #         "location": "San Francisco, CA",
    #         "description": "Join our team to build cutting-edge software solutions.",
    #         "requirements": "Python, JavaScript, React, AWS, CI/CD",
    #         "skills_required": ["Python", "JavaScript", "React", "AWS", "CI/CD", "Software Development"]
    #     },
    #     {
    #         "id": 2,
    #         "title": "Data Scientist",
    #         "company": "Data Insights Corp",
    #         "location": "New York, NY",
    #         "description": "Analyze complex datasets to extract business insights.",
    #         "requirements": "Python, Machine Learning, SQL, Statistics, Data Visualization",
    #         "skills_required": ["Python", "Machine Learning", "SQL", "Statistics", "Data Visualization", "Data Analysis"]
    #     },
    #     {
    #         "id": 3,
    #         "title": "Full Stack Developer",
    #         "company": "Web Solutions Ltd",
    #         "location": "Remote",
    #         "description": "Develop and maintain web applications for our clients.",
    #         "requirements": "JavaScript, HTML, CSS, Node.js, MongoDB",
    #         "skills_required": ["JavaScript", "HTML", "CSS", "Node.js", "MongoDB", "Web Development"]
    #     },
    #     {
    #         "id": 4,
    #         "title": "DevOps Engineer",
    #         "company": "Cloud Systems Inc.",
    #         "location": "Seattle, WA",
    #         "description": "Optimize and automate our cloud infrastructure.",
    #         "requirements": "AWS, Docker, Kubernetes, CI/CD, Linux",
    #         "skills_required": ["AWS", "Docker", "Kubernetes", "CI/CD", "Linux", "Infrastructure"]
    #     },
    #     {
    #         "id": 5,
    #         "title": "Product Manager",
    #         "company": "Innovation Products",
    #         "location": "Austin, TX",
    #         "description": "Lead the development of our flagship product.",
    #         "requirements": "Product Management, Agile, User Research, Strategic Planning",
    #         "skills_required": ["Product Management", "Agile", "User Research", "Strategic Planning", "Leadership"]
    #     },
    #     {
    #         "id": 6,
    #         "title": "UX/UI Designer",
    #         "company": "Creative Designs Agency",
    #         "location": "Los Angeles, CA",
    #         "description": "Create beautiful and functional user interfaces.",
    #         "requirements": "Figma, Adobe XD, UI Design, UX Research, Prototyping",
    #         "skills_required": ["Figma", "Adobe XD", "UI Design", "UX Research", "Prototyping", "Design"]
    #     },
    #     {
    #         "id": 7,
    #         "title": "Machine Learning Engineer",
    #         "company": "AI Solutions",
    #         "location": "Boston, MA",
    #         "description": "Develop and deploy machine learning models.",
    #         "requirements": "Python, TensorFlow, PyTorch, ML Algorithms, Deep Learning",
    #         "skills_required": ["Python", "TensorFlow", "PyTorch", "Machine Learning", "Deep Learning", "AI"]
    #     },
    #     {
    #         "id": 8,
    #         "title": "Frontend Developer",
    #         "company": "Interactive Web",
    #         "location": "Chicago, IL",
    #         "description": "Build responsive and interactive web interfaces.",
    #         "requirements": "JavaScript, React, HTML, CSS, Responsive Design",
    #         "skills_required": ["JavaScript", "React", "HTML", "CSS", "Responsive Design", "Frontend"]
    #     }
    # ]

def match_jobs_with_skills(skills_data, all_jobs):
    """Match jobs with extracted skills."""
    try:
        candidate_skills = skills_data.get('skills', [])
        
        if not candidate_skills:
            logging.warning("No skills found in the CV")
            return []
        
        # Calculate job match scores
        job_matches = []
        for job in all_jobs:
            job_skills = job['skills_required']
            match_score = calculate_skill_match_score(candidate_skills, job_skills)
            print(job['title'])
            print(match_score)
            # Only include jobs with a match score above 0
            if match_score > 0:
                job_match = job.copy()
                job_match['match_score'] = match_score
                job_match['match_percentage'] = int(match_score * 100)
                job_matches.append(job_match)
        
        # Sort jobs by match score in descending order
        sorted_matches = sorted(job_matches, key=lambda x: x['match_score'], reverse=True)
        
        return sorted_matches
    
    except Exception as e:
        logging.error(f"Error matching jobs with skills: {str(e)}")
        return []

def calculate_skill_match_score(candidate_skills, job_skills):
    """Calculate match score between candidate skills and job skills."""
    if not candidate_skills or not job_skills:
        return 0
    
    # Normalize all skills to lowercase for better matching
    candidate_skills_lower = [skill.lower() for skill in candidate_skills]
    job_skills_lower = [skill.lower() for skill in job_skills]
    
    # Count direct matches
    direct_matches = 0
    for job_skill in job_skills_lower:
        for candidate_skill in candidate_skills_lower:
            # Direct match
            if job_skill == candidate_skill:
                direct_matches += 1
                break
            # Partial match (if the skill is contained within another skill)
            elif job_skill in candidate_skill or candidate_skill in job_skill:
                direct_matches += 0.8  # 80% of the value of a direct match
                break
            # Similarity match
            elif similarity_ratio(job_skill, candidate_skill) > 0.8:  # 80% similarity threshold
                direct_matches += 0.6  # 60% of the value of a direct match
                break
    
    # Calculate match score (normalize to 0-1 range)
    match_score = direct_matches / len(job_skills) if job_skills else 0
    
    return min(match_score, 1.0)  # Cap at 1.0

def similarity_ratio(str1, str2):
    """Calculate similarity ratio between two strings."""
    return SequenceMatcher(None, str1, str2).ratio()
