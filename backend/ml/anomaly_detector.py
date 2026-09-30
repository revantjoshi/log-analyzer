import os
import joblib
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
from backend.ml.feature_extractor import FeatureExtractor
from backend.ml.profiler import NormalBehaviorProfiler

class AnomalyDetector:
    """
    Revant's AI/ML Anomaly Detector.
    Uses Isolation Forest ensemble and Standard Scaling to score log events.
    """

    def __init__(self, model_dir=None):
        self.model_dir = model_dir
        self.scaler = StandardScaler()
        self.iso_forest = IsolationForest(n_estimators=100, contamination=0.1, random_state=42)
        self.profiler = NormalBehaviorProfiler()
        self.is_trained = False

    def train(self, feature_matrix):
        """Trains scaler, IsolationForest, and NormalBehaviorProfiler on training data"""
        X = np.array(feature_matrix)
        if len(X) < 5:
            # Not enough data, initialize with synthetic baseline
            X = np.random.normal(loc=[50, 2, 2.5, 200, 500, 0, 0, 0, 0, 0, 0], scale=[10, 1, 0.5, 10, 100, 0.1, 0.1, 0.05, 0.05, 0.05, 0.05], size=(100, 11))
            X = np.clip(X, a_min=0, a_max=None)

        X_scaled = self.scaler.fit_transform(X)
        self.iso_forest.fit(X_scaled)
        self.profiler.fit(X)
        self.is_trained = True

        if self.model_dir:
            self.save_models(self.model_dir)

    def predict(self, feature_vector):
        """
        Scores a single feature vector.
        Returns dict with:
          - anomaly_score (0.0 to 1.0)
          - is_anomaly (bool)
          - feature_contributions (dict mapping feature_name -> contribution score)
          - deviation_score (float)
        """
        if not self.is_trained:
            # Fallback heuristic score if model not trained yet
            return self._heuristic_predict(feature_vector)

        vec = np.array(feature_vector).reshape(1, -1)
        vec_scaled = self.scaler.transform(vec)

        # IsolationForest decision_function: lower means more anomalous (negative for anomalies)
        raw_score = self.iso_forest.decision_function(vec_scaled)[0]
        
        # Convert decision function score to 0.0 - 1.0 anomaly probability
        # Typical decision scores range from -0.5 (heavy anomaly) to +0.5 (normal)
        normalized_anomaly_score = float(np.clip(0.5 - raw_score, 0.0, 1.0))
        
        # Determine threshold
        is_anomaly = bool(normalized_anomaly_score > 0.65 or feature_vector[7] == 1.0 or feature_vector[8] == 1.0 or feature_vector[9] == 1.0 or feature_vector[10] == 1.0)

        # Feature contributions calculation based on Z-scores
        dev_score, dev_details = self.profiler.calculate_deviation(feature_vector)
        
        fc = {}
        for idx, name in enumerate(FeatureExtractor.FEATURE_NAMES):
            val = float(feature_vector[idx])
            mean_val = float(self.profiler.feature_means[idx]) if self.profiler.feature_means is not None else 0.0
            std_val = float(self.profiler.feature_stds[idx]) if self.profiler.feature_stds is not None else 1.0
            z = abs(val - mean_val) / std_val
            fc[name] = round(float(z), 2)

        return {
            'anomaly_score': round(normalized_anomaly_score, 3),
            'is_anomaly': is_anomaly,
            'feature_contributions': fc,
            'deviation_score': round(dev_score, 3)
        }

    def _heuristic_predict(self, feature_vector):
        path_len = feature_vector[0]
        spec_chars = feature_vector[1]
        entropy = feature_vector[2]
        is_error = feature_vector[5]
        sql = feature_vector[7]
        trav = feature_vector[8]
        cmd = feature_vector[9]
        encoded = feature_vector[10]

        score = 0.05
        if path_len > 150: score += 0.2
        if spec_chars > 10: score += 0.2
        if entropy > 4.5: score += 0.25
        if is_error > 0: score += 0.1
        if sql > 0 or trav > 0 or cmd > 0 or encoded > 0: score += 0.45

        score = float(np.clip(score, 0.0, 1.0))
        is_anomaly = score > 0.5

        fc = {name: round(float(val), 2) for name, val in zip(FeatureExtractor.FEATURE_NAMES, feature_vector)}

        return {
            'anomaly_score': score,
            'is_anomaly': is_anomaly,
            'feature_contributions': fc,
            'deviation_score': round(score * 2.5, 3)
        }

    def save_models(self, path):
        os.makedirs(path, exist_ok=True)
        joblib.dump(self.scaler, os.path.join(path, 'scaler.joblib'))
        joblib.dump(self.iso_forest, os.path.join(path, 'iso_forest.joblib'))
        joblib.dump(self.profiler, os.path.join(path, 'profiler.joblib'))

    def load_models(self, path):
        scaler_p = os.path.join(path, 'scaler.joblib')
        iso_p = os.path.join(path, 'iso_forest.joblib')
        prof_p = os.path.join(path, 'profiler.joblib')

        if os.path.exists(scaler_p) and os.path.exists(iso_p) and os.path.exists(prof_p):
            self.scaler = joblib.load(scaler_p)
            self.iso_forest = joblib.load(iso_p)
            self.profiler = joblib.load(prof_p)
            self.is_trained = True
            return True
        return False
