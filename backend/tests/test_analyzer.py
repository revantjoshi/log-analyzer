import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.app import create_app
from backend.models import db, ParsedLog, AnomalyResult, SecurityAlert, HoneypotLog
from backend.ingestion.log_parser import LogParser
from backend.ml.feature_extractor import FeatureExtractor
from backend.ml.zero_day_engine import ZeroDayProfilingEngine
from backend.security.evasion_detector import LogEvasionDetector
from backend.security.correlator import EventCorrelator

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client

def test_log_parser_web():
    raw_log = '198.51.100.44 - - [30/Sep/2026:14:32:10 +0000] "GET /products.php?id=1%20UNION%20SELECT%20username,password%20FROM%20users-- HTTP/1.1" 200 4500 "-" "Mozilla/5.0"'
    parsed = LogParser.parse_web_log(raw_log)
    assert parsed['source_ip'] == '198.51.100.44'
    assert parsed['attack_category'] == 'SQL Injection'
    assert parsed['severity'] == 'High'

def test_feature_extractor():
    sample = {
        'path': '/admin/exec?cmd=cat%20/etc/passwd',
        'payload': 'cmd=cat /etc/passwd',
        'status_code': 200,
        'bytes_sent': 1500,
        'request_method': 'POST'
    }
    feats = FeatureExtractor.extract_features(sample)
    assert len(feats) == len(FeatureExtractor.FEATURE_NAMES)
    assert feats[8] == 1.0  # Traversal flag
    assert feats[9] == 1.0  # Command flag

def test_zero_day_profiling_statement():
    sample = {
        'path': '/unknown/rpc',
        'payload': 'QW50aWdyYXZpdHlaZXJvRGF5T3Bjb2Rl',
        'status_code': 200,
        'attack_category': 'Unclassified Pattern'
    }
    ml_result = {
        'anomaly_score': 0.85,
        'is_anomaly': True,
        'feature_contributions': {'encoded_payload_flag': 1.0, 'entropy': 4.2},
        'deviation_score': 4.1
    }
    eval_res = ZeroDayProfilingEngine.evaluate_zero_day_indicator(sample, ml_result)
    assert eval_res['is_zero_day_candidate'] == True
    assert eval_res['technical_label'] == 'Detection of previously unseen anomalous behaviour that may indicate zero-day activity'

def test_evasion_detector():
    logs = [
        {'id': 1, 'source_ip': '192.0.2.1', 'payload': 'rm -rf /var/log/syslog', 'timestamp': '2026-09-30T10:00:00'}
    ]
    alerts = LogEvasionDetector.detect_evasion_indicators(logs)
    assert len(alerts) > 0
    assert 'Log Erasure Command' in alerts[0]['description']

def test_system_info_endpoint(client):
    rv = client.get('/api/v1/system/info')
    assert rv.status_code == 200
    json_data = rv.get_json()
    assert json_data['project_title'] == 'AI-POWERED INTELLIGENT LOG ANALYZER'
    assert 'Revant' in json_data['team_modules']
    assert 'Janani' in json_data['team_modules']
    assert 'Ashna' in json_data['team_modules']
