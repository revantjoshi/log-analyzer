import os
import sys
import numpy as np

# Ensure backend path is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.ml.feature_extractor import FeatureExtractor
from backend.ml.anomaly_detector import AnomalyDetector

def build_training_dataset():
    """Generates clean normal baseline samples + synthetic training matrix"""
    normal_samples = []
    
    # 1. Normal web browsing
    paths = [
        '/index.html', '/about.html', '/contact.php', '/services', '/assets/css/main.css',
        '/assets/js/app.js', '/api/v1/products', '/api/v1/user/profile', '/images/logo.png',
        '/favicon.ico', '/dashboard', '/reports/monthly'
    ]
    
    for i in range(250):
        path = paths[i % len(paths)]
        sample = {
            'path': path,
            'payload': f"param={i}&user=normal_user",
            'status_code': 200 if i % 10 != 0 else 404,
            'bytes_sent': 500 + (i * 12) % 3000,
            'request_method': 'GET' if i % 4 != 0 else 'POST'
        }
        feats = FeatureExtractor.extract_features(sample)
        normal_samples.append(feats)
        
    return np.array(normal_samples)

def train_and_save_models(output_dir):
    print("[Revant AI/ML] Building training dataset...")
    X_train = build_training_dataset()
    
    print(f"[Revant AI/ML] Training IsolationForest & Normal Baseline Profiler on {len(X_train)} samples...")
    detector = AnomalyDetector(model_dir=output_dir)
    detector.train(X_train)
    
    print(f"[Revant AI/ML] Models successfully trained and saved to: {output_dir}")
    return detector

if __name__ == '__main__':
    model_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), 'saved_models'))
    train_and_save_models(model_folder)
