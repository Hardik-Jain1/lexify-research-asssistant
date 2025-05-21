# app/config.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
basedir = os.path.abspath(os.path.dirname(__file__))
dotenv_path = os.path.join(basedir, '..', '.env') # Assuming .env is in the root directory
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    print(f"Warning: .env file not found at {dotenv_path}. Using environment variables directly.")

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'instance', 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or os.environ.get('SECRET_KEY') # Use SECRET_KEY if JWT_SECRET_KEY is not set
    JWT_ACCESS_TOKEN_EXPIRES = False # Or set a timedelta, e.g., timedelta(hours=1)
    # JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

    QDRANT_URL = os.environ.get('QDRANT_URL')
    QDRANT_API_KEY = os.environ.get('QDRANT_API_KEY') # Optional

    # LiteLLM model configuration
    LITELLM_MODEL_SUMMARIZE = os.environ.get('LITELLM_MODEL_SUMMARIZE', 'gemini/gemini-2.0-flash')
    LITELLM_MODEL_CHAT = os.environ.get('LITELLM_MODEL_CHAT', 'gemini/gemini-2.0-flash')
    # Embedding model (can be specified for LiteLLM or a separate sentence-transformer)
    EMBEDDING_MODEL_NAME = os.environ.get('EMBEDDING_MODEL_NAME', 'gemini/text-embedding-004') # Example

    # Directories
    PAPER_SAVE_DIR = os.environ.get('PAPER_SAVE_DIR') or os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'data', 'papers')
    PROMPTS_DIR = os.environ.get('PROMPTS_DIR') or os.path.join(os.path.abspath(os.path.dirname(os.path.dirname(__file__))), 'prompts')

    # Celery (Optional, for background tasks)
    # CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL') or 'redis://localhost:6379/0'
    # CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND') or 'redis://localhost:6379/0'

    # Other configurations
    MAX_ARXIV_RESULTS = int(os.environ.get('MAX_ARXIV_RESULTS', 5))

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = False # Set to True to see SQL queries

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False # Disable CSRF for testing forms if you use Flask-WTF

class ProductionConfig(Config):
    DEBUG = False
    # Add production specific settings, e.g., logging, security headers

config_by_name = dict(
    dev=DevelopmentConfig,
    test=TestingConfig,
    prod=ProductionConfig
)