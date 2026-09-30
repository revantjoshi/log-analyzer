from flask import Blueprint, jsonify, request
from backend.models import db, ParsedLog, AttackStory, SecurityAlert
from backend.security.correlator import EventCorrelator
from backend.security.attack_reconstruction import AttackReconstructionEngine
from backend.security.evasion_detector import LogEvasionDetector
from datetime import datetime

security_bp = Blueprint('security', __name__, url_prefix='/api/v1/security')

@security_bp.route('/attack-stories', methods=['GET'])
def get_attack_stories():
    """Correlates all stored parsed logs and generates active attack stories"""
    all_parsed = ParsedLog.query.order_by(ParsedLog.timestamp.asc()).all()
    parsed_dicts = [p.to_dict() for p in all_parsed]

    # Correlate logs by source IP
    correlated = EventCorrelator.correlate_logs_by_ip(parsed_dicts)

    stories = []
    for ip, group in correlated.items():
        if ip in ['127.0.0.1', '0.0.0.0', '10.0.0.1']:
            continue
            
        story = AttackReconstructionEngine.reconstruct_attack_story(ip, group['logs'])
        if story:
            stories.append(story)

    # Sort stories by severity weight
    sev_weight = {'Critical': 4, 'High': 3, 'Medium': 2, 'Low': 1}
    stories.sort(key=lambda x: sev_weight.get(x['severity'], 0), reverse=True)

    return jsonify({
        'module_owner': 'JANANI - Cybersecurity / Attack Story Reconstruction',
        'total_stories': len(stories),
        'stories': stories
    }), 200

@security_bp.route('/evasion-alerts', methods=['GET'])
def get_evasion_alerts():
    all_parsed = ParsedLog.query.order_by(ParsedLog.timestamp.asc()).all()
    parsed_dicts = [p.to_dict() for p in all_parsed]

    evasion_alerts = LogEvasionDetector.detect_evasion_indicators(parsed_dicts)
    return jsonify({
        'module_owner': 'JANANI - Cybersecurity / Evasion & Tampering Engine',
        'total_alerts': len(evasion_alerts),
        'alerts': evasion_alerts
    }), 200

@security_bp.route('/alerts', methods=['GET'])
def get_alerts():
    alerts = SecurityAlert.query.order_by(SecurityAlert.created_at.desc()).limit(50).all()
    return jsonify([a.to_dict() for a in alerts]), 200

@security_bp.route('/summary-report', methods=['GET'])
def generate_summary_report():
    total_logs = ParsedLog.query.count()
    total_alerts = SecurityAlert.query.count()
    critical_alerts = SecurityAlert.query.filter_by(severity='Critical').count()
    
    all_parsed = ParsedLog.query.order_by(ParsedLog.timestamp.asc()).all()
    parsed_dicts = [p.to_dict() for p in all_parsed]
    correlated = EventCorrelator.correlate_logs_by_ip(parsed_dicts)
    evasion_alerts = LogEvasionDetector.detect_evasion_indicators(parsed_dicts)

    return jsonify({
        'report_title': 'Executive Cybersecurity Incident & Log Analysis Report',
        'generated_at': datetime.utcnow().isoformat(),
        'platform_status': 'UNIFIED INTELLIGENT LOG ANALYZER - ACTIVE',
        'metrics': {
            'total_logs_analyzed': total_logs,
            'total_security_alerts': total_alerts,
            'critical_incidents': critical_alerts,
            'active_attack_campaigns': len(correlated),
            'log_tampering_indicators': len(evasion_alerts)
        },
        'executive_summary': f"The Unified AI-Powered Log Analyzer monitored {total_logs} log events. Janani's Correlation Engine identified {len(correlated)} distinct attack campaigns across internal servers. Revant's Zero-Day engine flagged {critical_alerts} critical anomalous patterns. Ashna's honeypots recorded active attacker interactions.",
        'recommended_mitigations': [
            "Block identified hostile source IP addresses at perimeter firewall.",
            "Apply security patch for web application injection vectors.",
            "Enforce Multi-Factor Authentication (MFA) on SSH authentication gateways.",
            "Enable immutable append-only syslog forwarding to prevent log tampering evasion."
        ]
    }), 200
