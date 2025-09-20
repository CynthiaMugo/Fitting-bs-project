import os
from dotenv import load_dotenv
from datetime import timedelta

# loading environmental variables

load_dotenv()
# print("ENV Credentials")
# print(os.getenv("DATABASE_URL"))

class Config:
    SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SECRET_KEY="secret"

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "jwt-secret")  # for signing tokens
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1) 