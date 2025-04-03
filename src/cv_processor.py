import os
import logging
import json
from PyPDF2 import PdfReader
import docx
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq client with a recommended model
MODEL = "llama3-70b-8192"  # Using LLama3 70B model
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
groq_client = Groq(api_key=GROQ_API_KEY)

def extract_text_from_cv(file_path, original_filename):
    """Extract text from PDF or DOCX file."""
    try:
        file_extension = original_filename.split('.')[-1].lower()
        
        if file_extension == 'pdf':
            return extract_text_from_pdf(file_path)
        elif file_extension == 'docx':
            return extract_text_from_docx(file_path)
        else:
            raise ValueError(f"Unsupported file format: {file_extension}")
    
    except Exception as e:
        logging.error(f"Error extracting text from file: {str(e)}")
        raise

def extract_text_from_pdf(file_path):
    """Extract text from PDF file."""
    try:
        with open(file_path, 'rb') as file:
            pdf = PdfReader(file)
            text = ""
            for page in pdf.pages:
                text += page.extract_text()

            print(f"\n\n\n\n{text}\n\n\n\n")
            return text
    except Exception as e:
        logging.error(f"Error extracting text from PDF: {str(e)}")
        raise

def extract_text_from_docx(file_path):
    """Extract text from DOCX file."""
    try:
        doc = docx.Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    except Exception as e:
        logging.error(f"Error extracting text from DOCX: {str(e)}")
        raise

def extract_skills(cv_text):
    """Extract skills and other relevant information from CV text using Groq."""
    if not GROQ_API_KEY:
        logging.error("Groq API key not found")
        return {
            "skills": ["Error: API key required"],
            "experience": ["Error: API key required"],
            "education": ["Error: API key required"]
        }
    
    try:
        logging.debug("Calling Groq API to extract skills")
        
        # Create the system prompt for Llama3
        system_prompt = """
        You are a skilled HR professional and resume analyzer. Extract the following information from the provided CV/resume:
        
        1. A comprehensive list of technical and soft skills
        2. Professional experience highlights (job titles, companies, key achievements)
        3. Educational qualifications
        
        Format your response as a JSON object with the following structure:
        {
            "skills": ["skill1", "skill2", ...],
            "experience": ["experience1", "experience2", ...],
            "education": ["education1", "education2", ...]
        }
        
        Be thorough in your analysis and ensure all relevant information is captured.
        Only respond with valid JSON, no additional text or explanations.
        """
        
        # Call the Groq API
        response = groq_client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": cv_text}
            ],
            temperature=0.1
        )
        
        # Parse the response
        response_content = response.choices[0].message.content
        try:
            # Strip any non-JSON content (in case model includes explanations)
            print(f"\n\n\n\n{response_content}\n\n\n\n")
            json_str = response_content
            # Find the first { and last }
            start_idx = response_content.find('{')
            end_idx = response_content.rfind('}')
            if start_idx >= 0 and end_idx >= 0:
                json_str = response_content[start_idx:end_idx+1]
            
            skills_data = json.loads(json_str)
            logging.debug(f"Extracted skills data: {skills_data}")
            
            # Ensure expected fields are present
            if not all(k in skills_data for k in ["skills", "experience", "education"]):
                missing_keys = [k for k in ["skills", "experience", "education"] if k not in skills_data]
                for key in missing_keys:
                    skills_data[key] = []
                logging.warning(f"Some keys were missing in the response: {missing_keys}")
                
            return skills_data
        except json.JSONDecodeError:
            logging.error(f"Failed to parse JSON from response: {response_content}")
            return {
                "skills": ["Error parsing response"],
                "experience": ["Error parsing response"],
                "education": ["Error parsing response"]
            }
    
    except Exception as e:
        logging.error(f"Error extracting skills with Groq: {str(e)}")
        # Return error information in case of API failure
        return {
            "skills": ["Error extracting skills"],
            "experience": ["Error extracting experience"],
            "education": ["Error extracting education"]
        }
