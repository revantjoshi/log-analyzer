import numpy as np

class NormalBehaviorProfiler:
    """
    Revant's Normal Behavior Profiling Engine.
    Establishes mathematical baseline boundaries (mean, std dev, min, max, percentile bounds)
    for normal log activity.
    """

    def __init__(self):
        self.feature_means = None
        self.feature_stds = None
        self.feature_bounds = None
        self.is_fitted = False

    def fit(self, feature_matrix):
        """Fits normal baseline statistics on clean normal logs matrix (N_samples x M_features)"""
        matrix = np.array(feature_matrix)
        if matrix.size == 0:
            return

        self.feature_means = np.mean(matrix, axis=0)
        self.feature_stds = np.std(matrix, axis=0) + 1e-6 # prevent div by zero
        
        self.feature_bounds = {
            'p95': np.percentile(matrix, 95, axis=0),
            'p99': np.percentile(matrix, 99, axis=0),
            'max': np.max(matrix, axis=0)
        }
        self.is_fitted = True

    def calculate_deviation(self, feature_vector):
        """Calculates normalized Z-score deviation from normal baseline"""
        if not self.is_fitted:
            return 0.0, {}

        vec = np.array(feature_vector)
        z_scores = np.abs((vec - self.feature_means) / self.feature_stds)
        mean_deviation = float(np.mean(z_scores))
        max_deviation = float(np.max(z_scores))

        details = {
            'mean_z_score': round(mean_deviation, 3),
            'max_z_score': round(max_deviation, 3),
            'max_deviating_feature_index': int(np.argmax(z_scores))
        }

        return mean_deviation, details
