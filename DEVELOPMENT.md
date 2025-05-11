# Development Guide for Monthly Reflection Diary

This guide will help you set up the project for local development.

## Prerequisites

- Python 3.8+ installed
- pip (Python package manager)
- A code editor (e.g., VS Code, PyCharm)
- Git (optional, for version control)
- An OpenAI API key for AI-powered question generation

## Local Development Setup

### 1. Clone or Download the Repository

```bash
git clone <repository-url>
cd monthly-reflection-diary
```

### 2. Create and Activate a Virtual Environment

#### On macOS/Linux:
```bash
python -m venv venv
source venv/bin/activate
```

#### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r dependencies.txt
```

### 4. Environment Variables Setup

Create a `.env` file in the project root directory using the example provided in `.env.example`:

```bash
cp .env.example .env
```

Edit the `.env` file and add your configuration:

```
# Flask configuration
FLASK_APP=main.py
FLASK_ENV=development
SECRET_KEY=your_secure_secret_key_here

# Database configuration (SQLite by default)
DATABASE_URL=sqlite:///diary.db

# OpenAI API configuration
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. Initialize the Database

```bash
flask run
```

This will automatically create the SQLite database and required tables on first run.

### 6. Run the Development Server

If the server isn't already running from the previous step:

```bash
python main.py
```

Access the application at http://localhost:5000 in your browser.

## Project Structure

- `app.py` - Flask application setup and configuration
- `main.py` - Application entry point
- `models.py` - Database models definition
- `routes.py` - Route handlers and API endpoints
- `services/` - Business logic modules
  - `chat_extractor.py` - Extracts content from ChatGPT shared conversations
  - `openai_service.py` - OpenAI API integration for AI features
  - `pdf_generator.py` - PDF generation functionality
  - `question_generator.py` - Generates reflection questions
- `static/` - Static assets (CSS, JS)
- `templates/` - HTML templates
- `sample_data/` - Sample data for the application

## Working with the Database

The application uses SQLAlchemy with SQLite by default. To interact with the database using Flask:

```python
from app import db
from models import User, Diary, DiaryEntry, ChatLink

# Query example
users = User.query.all()

# Create example
new_user = User(username="john", email="john@example.com")
new_user.set_password("password")
db.session.add(new_user)
db.session.commit()
```

## Using PostgreSQL Instead of SQLite

For production or if you prefer to use PostgreSQL:

1. Install PostgreSQL and create a database
2. Update your `.env` file with PostgreSQL connection details:
   ```
   DATABASE_URL=postgresql://username:password@localhost/diary_db
   ```

## OpenAI Integration

The application uses OpenAI's GPT models to generate personalized questions based on ChatGPT conversation history. You need a valid OpenAI API key to use this feature. Set it in your `.env` file:

```
OPENAI_API_KEY=your_openai_api_key_here
```

## Testing

To run tests (when available):

```bash
pytest
```

## Deployment Considerations

For deployment to a production environment:

1. Use a production-grade server like Gunicorn
2. Set `FLASK_ENV=production` in your environment
3. Use a more robust database (PostgreSQL recommended)
4. Set a strong, unique `SECRET_KEY`
5. Consider using environment variables management for production settings

### Example Production Startup

```bash
gunicorn --bind 0.0.0.0:5000 main:app
```

## Troubleshooting

### Common Issues

1. **Database connection issues**: Ensure your DATABASE_URL is correct and the database server is running.
2. **OpenAI API errors**: Verify your API key is valid and has sufficient credits.
3. **PDF generation issues**: Make sure WeasyPrint and its dependencies are correctly installed.

### Debug Mode

For more detailed error information during development, ensure `debug=True` in your app configuration:

```python
# In main.py, already configured
app.run(debug=True)
```

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request