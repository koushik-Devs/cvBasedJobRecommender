# CV Based Job Recommender

A Flask application that extracts resume skills and experience, then ranks jobs from MongoDB. Resume text is sent to the configured Groq API for extraction.

## Setup

1. Install Python 3.10+ and MongoDB (local or hosted).
2. Install dependencies: `pip install -r requirements.txt`.
3. Copy `.env.example` to `.env`, then configure `GROQ_API_KEY`, `MONGO_URI`, and a random `SESSION_SECRET`.
4. Start the app from the repository root with `python src/app.py`.

The app accepts PDF and DOCX files up to 16 MB. Temporary uploads are removed after processing. Resume contents are sensitive; use only with consent and avoid public deployment without appropriate privacy controls.
