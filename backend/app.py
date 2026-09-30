import os
import sys
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

# Ensure project root is on Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.config import Config
from backend.models import db
from backend.ml.anomaly_detector import AnomalyDetector
from backend.ml.train_pipeline import train_and_save_models

from backend.routes.auth_routes import auth_bp
from backend.routes.log_routes import log_bp
from backend.routes.ml_routes import ml_bp
from backend.routes.security_routes import security_bp
from backend.routes.honeypot_routes import honeypot_bp

def create_app(config_class=Config):
    dist_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../frontend/dist'))
    app = Flask(__name__, static_folder=dist_path, static_url_path='')
    app.config.from_object(config_class)

    # Enable CORS for all API routes
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Initialize SQLAlchemy database
    db.init_app(app)

    # Initialize ML Detector (Revant Module)
    model_folder = app.config['MODEL_FOLDER']
    detector = AnomalyDetector(model_dir=model_folder)
    
    # Try loading existing trained models or train baseline
    if not detector.load_models(model_folder):
        print("[App Init] No saved ML models found. Training baseline models...")
        detector = train_and_save_models(model_folder)
        
    app.config['ML_DETECTOR'] = detector

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(log_bp)
    app.register_blueprint(ml_bp)
    app.register_blueprint(security_bp)
    app.register_blueprint(honeypot_bp)

    @app.route('/api/v1/system/info', methods=['GET'])
    def system_info():
        return jsonify({
            'project_title': 'AI-POWERED INTELLIGENT LOG ANALYZER',
            'team_modules': {
                'Revant': 'AI/ML & Zero-Day Profiling Engine',
                'Janani': 'Cybersecurity & Attack Story Reconstruction Engine',
                'Ashna': 'Honeypot & Attack Simulation Infrastructure'
            },
            'status': 'OPERATIONAL',
            'database': app.config['SQLALCHEMY_DATABASE_URI'].split(':///')[0]
        }), 200

    # Serve React App Frontend in production build
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_frontend(path):
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            if os.path.exists(os.path.join(app.static_folder, 'index.html')):
                return send_from_directory(app.static_folder, 'index.html')
            return jsonify({
                'message': 'AI-Powered Intelligent Log Analyzer REST API Backend is running.',
                'docs': '/api/v1/system/info'
            })

    with app.app_context():
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        os.makedirs(app.config['MODEL_FOLDER'], exist_ok=True)
        db.create_all()

    return app

# Expose app instance for Gunicorn WSGI server on Railway
app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    print(f"\n==================================================")
    print(f" AI-POWERED INTELLIGENT LOG ANALYZER BACKEND")
    print(f" Revant (AI/ML) | Janani (Cyber) | Ashna (Honeypot)")
    print(f" Server running at: http://127.0.0.1:{port}")
    print(f"==================================================\n")
    app.run(host='0.0.0.0', port=port, debug=True)
