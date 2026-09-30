from flask import Blueprint, request, jsonify, current_app
from backend.models import db, HoneypotLog
from backend.honeypot.honeypot_api import HoneypotManager
from backend.honeypot.simulator import AttackSimulator
from backend.routes.log_routes import process_and_save_log

honeypot_bp = Blueprint('honeypot', __name__, url_prefix='/api/v1/honeypot')

@honeypot_bp.route('/ingest', methods=['POST'])
def ingest_honeypot():
    data = request.get_json() or {}
    api_key = request.headers.get('X-Honeypot-API-Key') or data.get('api_key')
    expected_key = current_app.config['HONEYPOT_API_KEY']

    success, result, status_code = HoneypotManager.ingest_honeypot_event(data, api_key, expected_key)
    if not success:
        return jsonify({'error': result}), status_code

    return jsonify({'message': 'Honeypot telemetry recorded', 'data': result}), status_code

@honeypot_bp.route('/logs', methods=['GET'])
def get_honeypot_logs():
    logs = HoneypotLog.query.order_by(HoneypotLog.timestamp.desc()).limit(100).all()
    return jsonify({
        'module_owner': 'ASHNA - Honeypot / Infrastructure',
        'total_telemetry_records': len(logs),
        'logs': [l.to_dict() for l in logs]
    }), 200

@honeypot_bp.route('/scenarios', methods=['GET'])
def list_scenarios():
    return jsonify({
        'module_owner': 'ASHNA - Controlled Attack Simulation Infrastructure',
        'scenarios': AttackSimulator.SCENARIOS
    }), 200

@honeypot_bp.route('/simulate', methods=['POST'])
def run_simulation():
    data = request.get_json() or {}
    scenario_key = data.get('scenario_key', 'web_sqli_campaign')

    if scenario_key not in AttackSimulator.SCENARIOS:
        return jsonify({'error': f"Unknown scenario: {scenario_key}"}), 400

    generated_logs = AttackSimulator.generate_scenario_logs(scenario_key)
    processed_items = []

    for item in generated_logs:
        if item['type'] == 'honeypot':
            # Ingest via HoneypotManager
            expected_key = current_app.config['HONEYPOT_API_KEY']
            _, res, _ = HoneypotManager.ingest_honeypot_event(item['hp_data'], expected_key, expected_key)
            processed_items.append(res)
        else:
            # Process via unified log pipeline
            p_log = process_and_save_log(item['raw'], source=item['type'])
            processed_items.append(p_log.to_dict())

    scenario_info = AttackSimulator.SCENARIOS[scenario_key]

    return jsonify({
        'message': f"Attack simulation '{scenario_info['name']}' executed successfully.",
        'scenario': scenario_info,
        'generated_events_count': len(processed_items),
        'events': processed_items
    }), 200
