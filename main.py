import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from app import app  # noqa: F401

if __name__ == "__main__":
    # Get port from environment variable or default to 5000
    port = int(os.environ.get("PORT", 5000))

    # Get debug mode from environment variable or default to True for development
    debug = os.environ.get("FLASK_ENV", "development") == "development"

    app.run(host="0.0.0.0", port=port, debug=debug)
