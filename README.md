# Monthly Reflection Diary

A web application that generates printable monthly reflection diaries with AI-generated questions based on conversation history.

## Features

- **User Authentication**: Sign up and login system to manage your diaries
- **Monthly Diary Generation**: Create diaries for any month and year
- **AI-Generated Questions**: Daily reflection questions tailored to the month and season
- **ChatGPT Integration**: Add your shared ChatGPT conversation links for personalized questions
- **PDF Export**: Download your diary as a beautifully formatted, printable PDF
- **Responsive Design**: Works on desktop and mobile devices

## Screenshots

(Add screenshots of your application here)

## Tech Stack

- **Backend**: Python with Flask
- **Database**: SQLAlchemy with SQLite (configurable for PostgreSQL)
- **Frontend**: HTML, CSS with Bootstrap dark theme
- **PDF Generation**: WeasyPrint
- **AI Integration**: OpenAI API
- **Web Scraping**: Trafilatura for extracting conversation content

## Getting Started

See [DEVELOPMENT.md](DEVELOPMENT.md) for detailed setup instructions.

Quick start:
1. Clone the repository
2. Set up a Python virtual environment
3. Install dependencies from dependencies.txt
4. Set required environment variables
5. Run the application

## Required Environment Variables

- `SECRET_KEY`: For secure session management
- `DATABASE_URL`: Database connection string
- `OPENAI_API_KEY`: Your OpenAI API key

## Project Structure

The application follows a modular structure:
- `app.py`: Flask application setup
- `models.py`: Database models
- `routes.py`: API routes and views
- `services/`: Business logic modules
- `templates/`: HTML templates
- `static/`: Static assets (CSS, JS)

## License

[MIT License](LICENSE)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgements

- OpenAI for the GPT API
- Flask and its extensions
- Bootstrap for the UI components