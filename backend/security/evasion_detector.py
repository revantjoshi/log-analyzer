import re

class LogEvasionDetector:
    """
    Janani's Log Tampering & Evasion Detection Engine.
    Detects anti-forensic techniques, timestamp manipulation, payload obfuscation, and log erasure signatures.
    """

    TAMPERING_PATTERNS = [
        (re.compile(r'rm\s+(-rf|-f)?\s*/var/log', re.IGNORECASE), "Log Erasure Command Detected (`rm /var/log`)"),
        (re.compile(r'history\s+-c', re.IGNORECASE), "Shell History Clearing Detected (`history -c`)"),
        (re.compile(r'journalctl\s+--vacuum', re.IGNORECASE), "Systemd Log Vacuum/Wipe Attempt"),
        (re.compile(r'>\s*/var/log/\S+', re.IGNORECASE), "Log File Truncation Attempt (`> /var/log/...`)"),
        (re.compile(r'set\s+\+o\s+history', re.IGNORECASE), "Shell History Logging Suppression"),
        (re.compile(r'base64\s+-d', re.IGNORECASE), "Base64 Obfuscated Execution Evasion"),
        (re.compile(r'eval\(base64_decode', re.IGNORECASE), "PHP Base64 Encoded Payload Evasion")
    ]

    @classmethod
    def detect_evasion_indicators(cls, parsed_logs):
        """
        Scans a list of parsed logs for log tampering and evasion indicators.
        Returns a list of evasion alerts and summary.
        """
        evasion_alerts = []
        previous_ts = None

        for idx, log in enumerate(parsed_logs):
            payload = (log.get('payload') or '') + ' ' + (log.get('path') or '') + ' ' + (log.get('error_message') or '')
            current_ts = log.get('timestamp')

            # 1. Anti-forensic pattern scanning
            for regex, desc in cls.TAMPERING_PATTERNS:
                if regex.search(payload):
                    evasion_alerts.append({
                        'log_id': log.get('id'),
                        'source_ip': log.get('source_ip'),
                        'timestamp': current_ts.isoformat() if hasattr(current_ts, 'isoformat') else str(current_ts),
                        'indicator_type': 'Log Tampering / Anti-Forensics',
                        'description': desc,
                        'payload': payload[:150],
                        'severity': 'Critical'
                    })

            # 2. Timestamp Out-of-Sequence / Jump Detection (Timestamp Spoofing)
            if previous_ts and current_ts and hasattr(previous_ts, 'timestamp') and hasattr(current_ts, 'timestamp'):
                diff_seconds = (current_ts - previous_ts).total_seconds()
                if diff_seconds < -300: # Time jumped backwards by > 5 mins
                    evasion_alerts.append({
                        'log_id': log.get('id'),
                        'source_ip': log.get('source_ip'),
                        'timestamp': current_ts.isoformat() if hasattr(current_ts, 'isoformat') else str(current_ts),
                        'indicator_type': 'Timestamp Manipulation',
                        'description': f"Negative timestamp jump of {abs(int(diff_seconds))} seconds detected (Timestamp Tampering).",
                        'payload': payload[:150],
                        'severity': 'High'
                    })

            previous_ts = current_ts

        return evasion_alerts
