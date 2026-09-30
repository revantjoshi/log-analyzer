from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), default='analyst') # admin, analyst, auditor
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role,
            'created_at': self.created_at.isoformat()
        }

class RawLog(db.Model):
    __tablename__ = 'raw_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    source = db.Column(db.String(50), nullable=False) # apache, nginx, sshd, honeypot, custom
    log_level = db.Column(db.String(20), default='INFO')
    raw_text = db.Column(db.Text, nullable=False)
    parsed = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'source': self.source,
            'log_level': self.log_level,
            'raw_text': self.raw_text,
            'parsed': self.parsed
        }

class ParsedLog(db.Model):
    __tablename__ = 'parsed_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    raw_log_id = db.Column(db.Integer, db.ForeignKey('raw_logs.id'), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    log_type = db.Column(db.String(50), nullable=False) # web, ssh, honeypot, system, auth
    source_ip = db.Column(db.String(45), index=True)
    destination_ip = db.Column(db.String(45))
    user = db.Column(db.String(100))
    request_method = db.Column(db.String(10))
    path = db.Column(db.Text)
    status_code = db.Column(db.Integer)
    bytes_sent = db.Column(db.Integer, default=0)
    payload = db.Column(db.Text)
    error_message = db.Column(db.Text)
    attack_category = db.Column(db.String(100), default='Normal')
    severity = db.Column(db.String(20), default='Info')
    
    # Relationship to anomaly
    anomaly = db.relationship('AnomalyResult', backref='parsed_log', uselist=False, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'raw_log_id': self.raw_log_id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'log_type': self.log_type,
            'source_ip': self.source_ip,
            'destination_ip': self.destination_ip,
            'user': self.user,
            'request_method': self.request_method,
            'path': self.path,
            'status_code': self.status_code,
            'bytes_sent': self.bytes_sent,
            'payload': self.payload,
            'error_message': self.error_message,
            'attack_category': self.attack_category,
            'severity': self.severity,
            'anomaly': self.anomaly.to_dict() if self.anomaly else None
        }

class HoneypotLog(db.Model):
    __tablename__ = 'honeypot_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    honeypot_name = db.Column(db.String(50), default='HoneyTrap-Alpha')
    attacker_ip = db.Column(db.String(45), nullable=False, index=True)
    target_port = db.Column(db.Integer, nullable=False)
    service_emulated = db.Column(db.String(50), nullable=False) # SSH, HTTP, FTP, RDP, Telnet
    command_executed = db.Column(db.Text)
    payload_attempt = db.Column(db.Text)
    geo_location = db.Column(db.String(100), default='Simulated Location')
    session_id = db.Column(db.String(100), index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'honeypot_name': self.honeypot_name,
            'attacker_ip': self.attacker_ip,
            'target_port': self.target_port,
            'service_emulated': self.service_emulated,
            'command_executed': self.command_executed,
            'payload_attempt': self.payload_attempt,
            'geo_location': self.geo_location,
            'session_id': self.session_id
        }

class AnomalyResult(db.Model):
    __tablename__ = 'anomaly_results'
    
    id = db.Column(db.Integer, primary_key=True)
    log_id = db.Column(db.Integer, db.ForeignKey('parsed_logs.id'), nullable=False)
    anomaly_score = db.Column(db.Float, nullable=False) # 0.0 (normal) to 1.0 (extreme anomaly)
    is_anomaly = db.Column(db.Boolean, default=False)
    is_zero_day_candidate = db.Column(db.Boolean, default=False)
    novelty_score = db.Column(db.Float, default=0.0)
    feature_contributions = db.Column(db.Text) # JSON string
    detection_reason = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        fc = {}
        if self.feature_contributions:
            try:
                fc = json.loads(self.feature_contributions)
            except Exception:
                fc = {}
        return {
            'id': self.id,
            'log_id': self.log_id,
            'anomaly_score': self.anomaly_score,
            'is_anomaly': self.is_anomaly,
            'is_zero_day_candidate': self.is_zero_day_candidate,
            'novelty_score': self.novelty_score,
            'feature_contributions': fc,
            'detection_reason': self.detection_reason,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class AttackStory(db.Model):
    __tablename__ = 'attack_stories'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    attacker_ip = db.Column(db.String(45), index=True)
    start_time = db.Column(db.DateTime, default=datetime.utcnow)
    end_time = db.Column(db.DateTime, default=datetime.utcnow)
    severity = db.Column(db.String(20), default='High') # Low, Medium, High, Critical
    mitre_tactics = db.Column(db.Text) # JSON string array
    timeline_data = db.Column(db.Text) # JSON string array of steps
    graph_data = db.Column(db.Text) # JSON string object {nodes: [], edges: []}
    has_tampering_evidence = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(50), default='Active') # Active, Investigating, Resolved
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        mt, tl, gd = [], [], {'nodes': [], 'edges': []}
        try:
            if self.mitre_tactics: mt = json.loads(self.mitre_tactics)
            if self.timeline_data: tl = json.loads(self.timeline_data)
            if self.graph_data: gd = json.loads(self.graph_data)
        except Exception:
            pass
            
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'attacker_ip': self.attacker_ip,
            'start_time': self.start_time.isoformat() if self.start_time else None,
            'end_time': self.end_time.isoformat() if self.end_time else None,
            'severity': self.severity,
            'mitre_tactics': mt,
            'timeline_data': tl,
            'graph_data': gd,
            'has_tampering_evidence': self.has_tampering_evidence,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class SecurityAlert(db.Model):
    __tablename__ = 'security_alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    alert_type = db.Column(db.String(100), nullable=False) # Zero-Day Anomaly, Brute Force, Log Evasion, Honeypot Trigger
    severity = db.Column(db.String(20), default='Medium') # Low, Medium, High, Critical
    source_ip = db.Column(db.String(45))
    module_origin = db.Column(db.String(50), nullable=False) # Revant (AI), Janani (Cybersecurity), Ashna (Honeypot)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'alert_type': self.alert_type,
            'severity': self.severity,
            'source_ip': self.source_ip,
            'module_origin': self.module_origin,
            'is_read': self.is_read,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
