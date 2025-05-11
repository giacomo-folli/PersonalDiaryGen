# Development Guide for Monthly Reflection Diary

This guide will help you set up and run the Monthly Reflection Diary application on your local development environment.

## Project Overview

Monthly Reflection Diary is a web application that:
- Generates printable monthly diaries with AI-generated reflection questions
- Allows users to add ChatGPT conversation links for personalized questions
- Provides a simple user authentication system
- Exports diaries as printable PDFs

## Prerequisites

- Python 3.11 or higher
- pip (Python package installer)
- Git
- A text editor or IDE (VS Code, PyCharm, etc.)
- An OpenAI API key (for question generation)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone [your-repository-url]
cd monthly-reflection-diary
```

### 2. Create a Virtual Environment

```bash
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the root directory with the following variables:

```
FLASK_APP=main.py
FLASK_ENV=development
SECRET_KEY=your_secret_key_here
DATABASE_URL=sqlite:///diary.db
OPENAI_API_KEY=your_openai_api_key_here
```

Replace `your_secret_key_here` with a random string for session security, and `your_openai_api_key_here` with your actual OpenAI API key.

### 5. Initialize the Database

```bash
flask db init      # Initialize migrations (first time only)
flask db migrate   # Generate migrations
flask db upgrade   # Apply migrations to the database
```

### 6. Run the Application

```bash
flask run
```

The application will be available at [http://127.0.0.1:5000](http://127.0.0.1:5000).

## Project Structure

```
monthly-reflection-diary/
├── app.py                  # Flask app configuration
├── main.py                 # Application entry point
├── models.py               # Database models
├── routes.py               # Application routes
├── requirements.txt        # Python dependencies
├── sample_data/            # Sample question data
│   └── questions.json
├── services/               # Business logic services
│   ├── chat_extractor.py   # Extract content from ChatGPT links
│   ├── openai_service.py   # OpenAI API integration
│   ├── pdf_generator.py    # PDF generation service
│   └── question_generator.py # Question generation service
├── static/                 # Static assets (CSS, JS)
│   ├── css/
│   │   └── styles.css
│   └── js/
│       └── main.js
└── templates/              # HTML templates
    ├── pdf/
    │   └── diary_template.html
    ├── base.html
    ├── chat_links.html
    ├── index.html
    ├── login.html
    └── signup.html
```

## Development Workflow

1. **Make your changes**: Modify code in your local development environment
2. **Test locally**: Run the Flask application and test your changes
3. **Add new dependencies**: If you add new dependencies, update `requirements.txt`:
   ```bash
   pip freeze > requirements.txt
   ```

## API Integrations

### OpenAI API

The application uses OpenAI's API for generating personalized reflection questions based on the user's ChatGPT conversation history. The integration is handled in `services/openai_service.py`.

Key features:
- Extracts content from ChatGPT conversation links
- Analyzes conversation content to identify themes and interests
- Generates personalized reflection questions

## Common Issues and Solutions

### Database Migrations

If you make changes to the database models, you need to create and apply migrations:

```bash
flask db migrate -m "Description of changes"
flask db upgrade
```

### OpenAI API Rate Limits

If you encounter rate limit errors with the OpenAI API, consider:
- Implementing caching for API responses
- Reducing the frequency or volume of API calls
- Using a paid OpenAI API plan with higher rate limits

## Testing

Run tests with pytest:

```bash
pytest
```

## Deployment

For production deployment, consider:
- Using a production WSGI server (Gunicorn, uWSGI)
- Setting up a proper database (PostgreSQL, MySQL)
- Configuring environment variables securely
- Setting up proper logging
- Using HTTPS with a valid SSL certificate

Example production setup with Gunicorn:

```bash
pip install gunicorn
gunicorn --bind 0.0.0.0:5000 main:app
```