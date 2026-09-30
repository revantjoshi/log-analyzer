import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# On Railway, /tmp is writable. Use it for SQLite, uploads, and ML models.
# When DATABASE_URL is set (e.g. for PostgreSQL), that takes priority.
IS_RAILWAY = os.environ.get('RAILWAY_ENVIRONMENT') is not None
WRITABLE_DIR = '/tmp' if IS_RAILWAY else BASE_DIR

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'cybersecurity_log_analyzer_secret_key_2026')

    # SQLite by default; set DATABASE_URL env var for PostgreSQL/MySQL on Railway
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///' + os.path.join(WRITABLE_DIR, 'log_analyzer.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Honeypot integration config
    HONEYPOT_API_KEY = os.environ.get('HONEYPOT_API_KEY', 'hp_secret_key_884920418')

    # File upload config — use /tmp on Railway (ephemeral, writable)
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', os.path.join(WRITABLE_DIR, 'uploads'))
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max

    # Saved ML models folder — use /tmp on Railway
    MODEL_FOLDER = os.environ.get('MODEL_FOLDER', os.path.join(WRITABLE_DIR, 'ml_models'))
