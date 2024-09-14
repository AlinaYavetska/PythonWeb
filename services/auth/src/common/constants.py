import os

from dotenv import load_dotenv

load_dotenv()

GATEWAY_HOST = os.getenv("GATEWAY_HOST")
SITE_HOST = os.getenv("SITE_HOST")

ALGORITHM: str = os.getenv("ALGORITHM")
SECRET_KEY: str = os.getenv("SECRET_KEY")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
REFRESH_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES"))