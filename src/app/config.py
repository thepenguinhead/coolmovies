import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL') or 'sqlite:///site.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OMDB_API_KEY = os.environ.get('OMDB_API_KEY') or 'your_default_api_key'
    CACHE_TYPE = 'simple'  # Use 'simple' cache type for Flask-Caching
    CACHE_DEFAULT_TIMEOUT = 300  # Set default timeout for cache
