import os

DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = int(os.getenv("DB_PORT", "3306"))
DB_USER = os.getenv("DB_USER", "app_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "app_pass")
DB_NAME = os.getenv("DB_NAME", "ambiente")

SECRET_KEY = os.getenv("FLASK_SECRET_KEY", "chaveSecretaFlask")
FLASK_DEBUG = os.getenv("FLASK_DEBUG", "1") == "1"

API_WRITE_KEY= os.getenv("API_WRITE_KEY","VO181Z5SH9DGO2BP")
API_READ_KEY= os.getenv("API_READ_KEY","V8TCEWTZ6FJVWGDG")
CHANNEL_ID= os.getenv("CHANNEL_ID", "3305413")