# Development Guide for Monthly Reflection Diary

Quick guide to set up the project for local development.

## Prerequisites

- Python 3.8+
- Docker (optional, for containerized development)
- OpenAI API key

## Setup Options

### Local Python Setup

1. **Install dependencies**
   ```bash
   pip install -r dependencies.txt
   ```

2. **Set up environment**
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key and other config

3. **Run the app**
   ```bash
   python main.py
   ```
   
   Access at http://localhost:5000

### Docker Setup (Recommended)

1. **Build and run with Docker Compose**
   ```bash
   # Make sure your OPENAI_API_KEY is set in your environment
   docker compose up -d
   ```

2. **Or build and run manually**
   ```bash
   docker build -t reflection-diary .
   docker run -p 5000:5000 -e OPENAI_API_KEY=your_key reflection-diary
   ```

See `DOCKERFILE.md` for more detailed Docker instructions.

## Project Structure

- `app.py` - Flask app configuration
- `main.py` - Entry point
- `models.py` - Database models
- `routes.py` - API endpoints
- `services/` - Business logic modules
- `static/`, `templates/` - Frontend assets
- `sample_data/` - Sample questions data

## Key Features

- User authentication
- Monthly diary generation with reflection questions
- ChatGPT conversation history integration
- PDF export of diaries
- AI-powered personalized questions

## Database Options

- **SQLite** (default): No configuration needed
- **PostgreSQL**: Set `DATABASE_URL` in `.env` or as environment variable

## Troubleshooting

- **OpenAI API errors**: Check your API key validity
- **PDF generation**: WeasyPrint dependencies must be installed
- **For full logs**: Set `FLASK_ENV=development`

For more details, see `README.md`.