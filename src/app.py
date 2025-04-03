import os
import logging
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from werkzeug.utils import secure_filename
import tempfile

from cv_processor import extract_text_from_cv, extract_skills
from job_matcher import get_all_jobs, match_jobs_with_skills

from pymongo import MongoClient

# Connect to MongoDB
MONGO_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["job_matching_db"]  # Database name

cv_collection = db["cv_data"]
jobs_collection = db["jobs"]

# Create Flask app
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_secret_key")

# Configure upload settings
ALLOWED_EXTENSIONS = {'pdf', 'docx'}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload_cv', methods=['POST'])
def upload_cv():
    # Check if file was uploaded
    if 'cv_file' not in request.files:
        flash('No file uploaded', 'error')
        return redirect(url_for('index'))
    
    file = request.files['cv_file']
    
    # Check if file is empty
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    # Check if file type is allowed
    if not allowed_file(file.filename):
        flash('Invalid file type. Please upload a PDF or DOCX file.', 'error')
        return redirect(url_for('index'))
    
    try:
        # Save file to temp directory
        filename = secure_filename(file.filename)
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            file.save(temp.name)
            temp_path = temp.name
        
        # Extract text from CV
        logging.debug(f"Extracting text from {filename}")
        cv_text = extract_text_from_cv(temp_path, file.filename)
        
        # Extract skills from text using Groq
        logging.debug("Extracting skills from CV text")
        skills_data = extract_skills(cv_text)
        
        # Store extracted CV data in MongoDB
        cv_data = {
            "filename": filename,
            "skills": skills_data.get("skills", []),
            "experience": skills_data.get("experience", []),
            "education": skills_data.get("education", []),
        }
        cv_collection.insert_one(cv_data)
        
        # Get all available jobs from MongoDB
        all_jobs = get_all_jobs()
        
        # Match jobs with extracted skills
        matched_jobs = match_jobs_with_skills(skills_data, all_jobs)
        
        # Store results in session for display
        session['skills'] = skills_data.get('skills', [])
        session['experience'] = skills_data.get('experience', [])
        session['education'] = skills_data.get('education', [])
        session['matched_jobs'] = matched_jobs
        
        # Clean up temp file
        os.unlink(temp_path)
        
        return redirect(url_for('results'))
    
    except Exception as e:
        logging.error(f"Error processing CV: {str(e)}")
        flash(f'Error processing CV: {str(e)}', 'error')
        return redirect(url_for('index'))


@app.route('/results')
def results():
    # Get results from session
    skills = session.get('skills', [])
    experience = session.get('experience', [])
    education = session.get('education', [])
    matched_jobs = session.get('matched_jobs', [])
    
    if not matched_jobs:
        flash('No results found. Please try uploading your CV again.', 'error')
        return redirect(url_for('index'))
    
    return render_template('results.html', 
                          skills=skills,
                          experience=experience,
                          education=education,
                          matched_jobs=matched_jobs)

@app.errorhandler(413)
def too_large(e):
    flash('File is too large. Maximum size is 16MB.', 'error')
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
