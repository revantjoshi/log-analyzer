import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'cybersecurity_log_analyzer_secret_key_2026')
    
    # SQLite default, easily configured for PostgreSQL or MySQL via environment variables
    # e.g., postgresql://user:password@localhost/dbname or mysql+pymysql://user:password@localhost/dbname
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL', 
        'sqlite:///' + os.path.join(BASE_DIR, 'log_analyzer.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Honeypot integration config
    HONEYPOT_API_KEY = os.environ.get('HONEYPOT_API_KEY', 'hp_secret_key_884920418')
    
    # File upload config
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max
    
    # Saved ML models folder
    MODEL_FOLDER = os.path.join(BASE_DIR, 'ml', 'saved_models')
