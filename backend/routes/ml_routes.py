from flask import Blueprint, jsonify, current_app, request
from backend.models import db, AnomalyResult, ParsedLog
from backend.ml.train_pipeline import train_and_save_models

ml_bp = Blueprint('ml', __name__, url_prefix='/api/v1/ml')

@ml_bp.route('/status', methods=['GET'])
def get_ml_status():
    detector = current_app.config['ML_DETECTOR']
    total_analyzed = AnomalyResult.query.count()
    anomalies_count = AnomalyResult.query.filter_by(is_anomaly=True).count()
    zero_day_count = AnomalyResult.query.filter_by(is_zero_day_candidate=True).count()

    return jsonify({
        'module_owner': 'REVANT - AI/ML & Zero-Day Profiling',
        'is_trained': detector.is_trained,
        'algorithm': 'Ensemble Isolation Forest + Standard Scaler + Baseline Profiler',
        'technical_statement': 'Detection of previously unseen anomalous behaviour that may indicate zero-day activity',
        'total_logs_profiled': total_analyzed,
        'anomalies_detected': anomalies_count,
        'zero_day_candidates': zero_day_count,
        'anomaly_rate_percent': round((anomalies_count / max(1, total_analyzed)) * 100, 2)
    }), 200

@ml_bp.route('/zero-day-candidates', methods=['GET'])
def get_zero_day_candidates():
    results = AnomalyResult.query.filter_by(is_zero_day_candidate=True).order_by(AnomalyResult.created_at.desc()).all()
    
    candidates = []
    for r in results:
        log = ParsedLog.query.get(r.log_id)
        if log:
            cand = r.to_dict()
            cand['log'] = log.to_dict()
            candidates.append(cand)

    return jsonify({
        'technical_scope': 'Detection of previously unseen anomalous behaviour that may indicate zero-day activity',
        'total_candidates': len(candidates),
        'candidates': candidates
    }), 200

@ml_bp.route('/anomaly-stats', methods=['GET'])
def get_anomaly_stats():
    # Distribution buckets for Chart.js / Recharts
    bucket_0_2 = AnomalyResult.query.filter(AnomalyResult.anomaly_score < 0.2).count()
    bucket_2_4 = AnomalyResult.query.filter(AnomalyResult.anomaly_score >= 0.2, AnomalyResult.anomaly_score < 0.4).count()
    bucket_4_6 = AnomalyResult.query.filter(AnomalyResult.anomaly_score >= 0.4, AnomalyResult.anomaly_score < 0.6).count()
    bucket_6_8 = AnomalyResult.query.filter(AnomalyResult.anomaly_score >= 0.6, AnomalyResult.anomaly_score < 0.8).count()
    bucket_8_10 = AnomalyResult.query.filter(AnomalyResult.anomaly_score >= 0.8).count()

    return jsonify({
        'distribution': [
            {'range': '0.0 - 0.2 (Normal)', 'count': bucket_0_2},
            {'range': '0.2 - 0.4 (Low)', 'count': bucket_2_4},
            {'range': '0.4 - 0.6 (Moderate)', 'count': bucket_4_6},
            {'range': '0.6 - 0.8 (Anomalous)', 'count': bucket_6_8},
            {'range': '0.8 - 1.0 (Critical / Zero-Day Candidate)', 'count': bucket_8_10}
        ]
    }), 200

@ml_bp.route('/retrain', methods=['POST'])
def retrain_model():
    model_folder = current_app.config['MODEL_FOLDER']
    detector = train_and_save_models(model_folder)
    current_app.config['ML_DETECTOR'] = detector
    return jsonify({
        'message': 'AI/ML Anomaly Detection Model retrained successfully on updated normal baseline dataset.',
        'is_trained': detector.is_trained
    }), 200
