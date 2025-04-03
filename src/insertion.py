from pymongo import MongoClient

MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI)
db = client["job_matching_db"]
jobs_collection = db["jobs"]

sample_jobs =  [
        {
            "id": 1,
            "title": "Senior Software Engineer",
            "company": "Tech Innovators Inc.",
            "location": "San Francisco, CA",
            "description": "Join our team to build cutting-edge software solutions.",
            "requirements": "Python, JavaScript, React, AWS, CI/CD",
            "skills_required": ["Python", "JavaScript", "React", "AWS", "CI/CD", "Software Development"]
        },
        {
            "id": 2,
            "title": "Data Scientist",
            "company": "Data Insights Corp",
            "location": "New York, NY",
            "description": "Analyze complex datasets to extract business insights.",
            "requirements": "Python, Machine Learning, SQL, Statistics, Data Visualization",
            "skills_required": ["Python", "Machine Learning", "SQL", "Statistics", "Data Visualization", "Data Analysis"]
        },
        {
            "id": 3,
            "title": "Full Stack Developer",
            "company": "Web Solutions Ltd",
            "location": "Remote",
            "description": "Develop and maintain web applications for our clients.",
            "requirements": "JavaScript, HTML, CSS, Node.js, MongoDB",
            "skills_required": ["JavaScript", "HTML", "CSS", "Node.js", "MongoDB", "Web Development"]
        },
        {
            "id": 4,
            "title": "DevOps Engineer",
            "company": "Cloud Systems Inc.",
            "location": "Seattle, WA",
            "description": "Optimize and automate our cloud infrastructure.",
            "requirements": "AWS, Docker, Kubernetes, CI/CD, Linux",
            "skills_required": ["AWS", "Docker", "Kubernetes", "CI/CD", "Linux", "Infrastructure"]
        },
        {
            "id": 5,
            "title": "Product Manager",
            "company": "Innovation Products",
            "location": "Austin, TX",
            "description": "Lead the development of our flagship product.",
            "requirements": "Product Management, Agile, User Research, Strategic Planning",
            "skills_required": ["Product Management", "Agile", "User Research", "Strategic Planning", "Leadership"]
        },
        {
            "id": 6,
            "title": "UX/UI Designer",
            "company": "Creative Designs Agency",
            "location": "Los Angeles, CA",
            "description": "Create beautiful and functional user interfaces.",
            "requirements": "Figma, Adobe XD, UI Design, UX Research, Prototyping",
            "skills_required": ["Figma", "Adobe XD", "UI Design", "UX Research", "Prototyping", "Design"]
        },
        {
            "id": 7,
            "title": "Machine Learning Engineer",
            "company": "AI Solutions",
            "location": "Boston, MA",
            "description": "Develop and deploy machine learning models.",
            "requirements": "Python, TensorFlow, PyTorch, ML Algorithms, Deep Learning",
            "skills_required": ["Python", "TensorFlow", "PyTorch", "Machine Learning", "Deep Learning", "AI"]
        },
        {
            "id": 8,
            "title": "Frontend Developer",
            "company": "Interactive Web",
            "location": "Chicago, IL",
            "description": "Build responsive and interactive web interfaces.",
            "requirements": "JavaScript, React, HTML, CSS, Responsive Design",
            "skills_required": ["JavaScript", "React", "HTML", "CSS", "Responsive Design", "Frontend"]
        }
    ]

# Insert only if jobs collection is empty
if jobs_collection.count_documents({}) == 0:
    jobs_collection.insert_many(sample_jobs)
    print("Sample jobs inserted into MongoDB")
else:
    print("Jobs already exist in MongoDB")
