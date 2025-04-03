# This file is included for potential future database integration
# Currently using in-memory job data in job_matcher.py

class Job:
    """Model representing a job posting."""
    
    def __init__(self, id, title, company, location, description, requirements, skills_required):
        self.id = id
        self.title = title
        self.company = company
        self.location = location
        self.description = description
        self.requirements = requirements
        self.skills_required = skills_required
        
    def to_dict(self):
        """Convert job to dictionary."""
        return {
            "id": self.id,
            "title": self.title,
            "company": self.company,
            "location": self.location,
            "description": self.description,
            "requirements": self.requirements,
            "skills_required": self.skills_required
        }

class Skill:
    """Model representing a skill."""
    
    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category
        
    def to_dict(self):
        """Convert skill to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category
        }
