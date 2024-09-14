import os 

from dotenv import load_dotenv

load_dotenv()

AUTH_SERVICE_HOST = os.getenv("AUTH_SERVICE_HOST", "localhost")
AUTH_SERVICE_PORT = os.getenv("AUTH_SERVICE_PORT", 8000)