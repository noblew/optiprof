"""
This file holds Configuration options.
Production is used in any deployment configuration.

DO NOT HARD CODE YOUR PRODUCTION URLS EVER. Either use creds.ini or use environment variables.
"""
import os
from dotenv import load_dotenv

load_dotenv()

# more configuration options here http://flask.pocoo.org/docs/1.0/config/
class Config:
    """
    Base Configuration
    """

    # CHANGE SECRET_KEY!! I would use sha256 to generate one and set this as an environment variable
    # Exmaple to retrieve env variable `SECRET_KEY`: os.environ.get("SECRET_KEY")
    SECRET_KEY = "testkey"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MYSQL_URI = os.environ.get("DATABASE_URL")
    DBUSER = os.environ.get("DATABASE_USER")
    DBPASS = os.environ.get("DATABASE_PASS")


class DevelopmentConfig(Config):
    """
    Development Configuration - default config
    """

    DEBUG = True


class ProductionConfig(Config):
    """
    Production Configuration

    Requires the environment variable `FLASK_ENV=prod`
    """

    DEBUG = False


# way to map the value of `FLASK_ENV` to a configuration
config = {"dev": DevelopmentConfig, "prod": ProductionConfig}
