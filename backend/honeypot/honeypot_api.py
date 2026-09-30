from backend.models import db, HoneypotLog, RawLog, ParsedLog, SecurityAlert
from backend.ingestion.log_parser import LogParser
from datetime import datetime

class HoneypotManager:
    """
    Ashna's Honeypot Ingestion & Telemetry Manager.
    Receives incoming logs from honeypots, stores telemetry, and triggers security processing.
    """

    @classmethod
    def ingest_honeypot_event(cls, data_dict, api_key_provided, expected_api_key):
        """
        Validates API key and stores honeypot telemetry.
        """
        if api_key_provided != expected_api_key:
            return False, "Unauthorized Honeypot API key", 401

        attacker_ip = data_dict.get('attacker_ip', '127.0.0.1')
        target_port = int(data_dict.get('target_port', 80))
        service_emulated = data_dict.get('service_emulated', 'HTTP')
        command_executed = data_dict.get('command_executed', '')
        payload_attempt = data_dict.get('payload_attempt', '')
        session_id = data_dict.get('session_id', f"hp-session-{datetime.utcnow().timestamp()}")

        # 1. Create HoneypotLog record
        hp_log = HoneypotLog(
            honeypot_name=data_dict.get('honeypot_name', 'HoneyTrap-Alpha'),
            attacker_ip=attacker_ip,
            target_port=target_port,
            service_emulated=service_emulated,
            command_executed=command_executed,
            payload_attempt=payload_attempt,
            geo_location=data_dict.get('geo_location', 'Simulated Location'),
            session_id=session_id
        )
        db.session.add(hp_log)

        # 2. Convert to ParsedLog for unified correlation & ML processing
        parsed_dict = LogParser.parse_honeypot_log(data_dict)
        
        parsed_log = ParsedLog(
            log_type='honeypot',
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

        # 3. Generate Honeypot Security Alert
        alert = SecurityAlert(
            title=f"Honeypot Decoy Trapped Attacker {attacker_ip}",
            description=f"Attacker connected to honeypot service {service_emulated} on port {target_port}. Executed command/payload: '{payload_attempt or command_executed}'",
            alert_type='Honeypot Trigger',
            severity='High',
            source_ip=attacker_ip,
            module_origin='Ashna (Honeypot)'
        )
        db.session.add(alert)

        db.session.commit()
        return True, hp_log.to_dict(), 201
