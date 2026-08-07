import os

from dotenv import load_dotenv

load_dotenv()

TRELLO_API_KEY = os.getenv("TRELLO_API_KEY")
TRELLO_API_TOKEN = os.getenv("TRELLO_API_TOKEN")
TRELLO_BASE_URL = os.getenv("TRELLO_BASE_URL", "https://api.trello.com/1")

if not TRELLO_API_KEY or not TRELLO_API_TOKEN:
    raise RuntimeError(
        "TRELLO_API_KEY and TRELLO_API_TOKEN must be set in .env"
    )
