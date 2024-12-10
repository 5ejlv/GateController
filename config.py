from dotenv import load_dotenv
import os

load_dotenv(override=True)

DB_HOST = os.environ.get("POSTGRES_HOST")
DB_PORT = os.environ.get("POSTGRES_PORT")
DB_NAME = os.environ.get("POSTGRES_DB")
DB_USER = os.environ.get("POSTGRES_USER")
DB_PASS = os.environ.get("POSTGRES_PASSWORD")

SECRET_AUTH = os.environ.get("SECRET_AUTH")
CONTROL_GPIO = int(os.environ.get("CONTROL_GPIO"))
OPEN_DURATION = int(os.environ.get("OPEN_DURATION"))