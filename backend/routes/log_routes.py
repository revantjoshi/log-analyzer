from flask import Blueprint, request, jsonify, current_app
from backend.models import db, RawLog, ParsedLog, AnomalyResult, SecurityAlert
from backend.ingestion.log_parser import LogParser
from backend.ml.feature_extractor import FeatureExtractor
from backend.ml.zero_day_engine import ZeroDayProfilingEngine
from datetime import datetime
import os

log_bp = Blueprint('logs', __name__, url_prefix='/api/v1/logs')

def process_and_save_log(raw_text, source='web'):
    """Helper to parse a raw log, run ML anomaly detector & save to DB"""
    # 1. Save raw log
    raw_log = RawLog(source=source, raw_text=raw_text, parsed=True)
    db.session.add(raw_log)
    db.session.flush()

    # 2. Parse log
    if 'sshd' in raw_text or source == 'ssh':
        parsed_dict = LogParser.parse_ssh_log(raw_text)
    else:
        parsed_dict = LogParser.parse_web_log(raw_text)

    parsed_log = ParsedLog(
        raw_log_id=raw_log.id,
        timestamp=parsed_dict['timestamp'],
        log_type=parsed_dict['log_type'],
        source_ip=parsed_dict['source_ip'],
        destination_ip=parsed_dict['destination_ip'],
        user=parsed_dict['user'],
        request_method=parsed_dict['request_method'],
        path=parsed_dict['path'],
        status_code=parsed_dict['status_code'],
        bytes_sent=parsed_dict['bytes_sent'],
        payload=parsed_dict['payload'],
        error_message=parsed_dict['error_message'],
        attack_category=parsed_dict['attack_category'],
        severity=parsed_dict['severity']
    )
    db.session.add(parsed_log)
    db.session.flush()

    # 3. Extract features & score with ML detector
    feats = FeatureExtractor.extract_features(parsed_dict)
    detector = current_app.config['ML_DETECTOR']
    ml_result = detector.predict(feats)

    # 4. Evaluate Zero-Day candidate status (Revant module)
    zero_day_eval = ZeroDayProfilingEngine.evaluate_zero_day_indicator(parsed_dict, ml_result)

    anomaly_rec = AnomalyResult(
        log_id=parsed_log.id,
        anomaly_score=ml_result['anomaly_score'],
        is_anomaly=ml_result['is_anomaly'],
        is_zero_day_candidate=zero_day_eval['is_zero_day_candidate'],
        novelty_score=zero_day_eval['novelty_score'],
        feature_contributions=str(ml_result['feature_contributions']).replace("'", '"'),
        detection_reason=zero_day_eval['detection_reason']
    )
    db.session.add(anomaly_rec)

    # 5. Create Security Alert if anomaly or zero day
    if zero_day_eval['is_zero_day_candidate']:
        alert = SecurityAlert(
            title=f"Previously Unseen Anomalous Activity (Zero-Day Candidate) from {parsed_dict['source_ip']}",
            description=f"Log event scored anomaly index {ml_result['anomaly_score']} with novelty score {zero_day_eval['novelty_score']}. Rationale: {zero_day_eval['detection_reason']}",
            alert_type='Zero-Day Candidate Anomaly',
            severity='Critical',
            source_ip=parsed_dict['source_ip'],
            module_origin='Revant (AI/ML)'
        )
        db.session.add(alert)
    elif ml_result['is_anomaly']:
        alert = SecurityAlert(
            title=f"Statistical Log Anomaly Detected ({parsed_dict['attack_category']})",
            description=f"Anomalous traffic pattern detected from IP {parsed_dict['source_ip']} on endpoint {parsed_dict['path']}.",
            alert_type='Statistical Anomaly',
            severity='High' if parsed_dict['severity'] == 'High' else 'Medium',
            source_ip=parsed_dict['source_ip'],
            module_origin='Revant (AI/ML)'
        )
        db.session.add(alert)

    db.session.commit()
    return parsed_log

@log_bp.route('/', methods=['GET'])
def get_logs():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 50, type=int)
    source_filter = request.args.get('source')
    search_q = request.args.get('search')
    anomalies_only = request.args.get('anomalies_only', 'false').lower() == 'true'

    query = ParsedLog.query

    if source_filter:
        query = query.filter_by(log_type=source_filter)
    if search_q:
        query = query.filter(
            (ParsedLog.source_ip.like(f"%{search_q}%")) |
            (ParsedLog.path.like(f"%{search_q}%")) |
            (ParsedLog.payload.like(f"%{search_q}%")) |
            (ParsedLog.attack_category.like(f"%{search_q}%"))
        )
    if anomalies_only:
        query = query.join(AnomalyResult).filter(AnomalyResult.is_anomaly == True)

    query = query.order_by(ParsedLog.timestamp.desc())
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)

    return jsonify({
        'logs': [l.to_dict() for l in pagination.items],
        'total': pagination.total,
        'page': pagination.page,
        'pages': pagination.pages
    }), 200

@log_bp.route('/upload', methods=['POST'])
def upload_log_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'Empty filename'}), 400

    content = file.read().decode('utf-8', errors='ignore')
    lines = content.splitlines()

    processed_count = 0
    anomalies_found = 0

    for line in lines[:500]: # process up to 500 lines per file upload
        if line.strip():
            log_item = process_and_save_log(line, source='upload')
            processed_count += 1
            if log_item.anomaly and log_item.anomaly.is_anomaly:
                anomalies_found += 1

    return jsonify({
        'message': f"Successfully uploaded and analyzed {processed_count} log entries.",
        'processed_count': processed_count,
        'anomalies_found': anomalies_found
    }), 200

@log_bp.route('/ingest', methods=['POST'])
def ingest_log():
    data = request.get_json() or {}
    raw_text = data.get('raw_text') or data.get('log_line')
    source = data.get('source', 'web')

    if not raw_text:
        return jsonify({'error': 'raw_text required'}), 400

    parsed_log = process_and_save_log(raw_text, source=source)
    return jsonify({
        'message': 'Log ingested and analyzed successfully',
        'log': parsed_log.to_dict()
    }), 201
