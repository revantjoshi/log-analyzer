import re
from datetime import datetime

class LogParser:
    """
    Parses various log formats into standardized structured dictionaries:
    - Apache/Nginx Combined & Common Access Logs
    - SSH Auth Syslogs
    - Honeypot JSON logs
    - Custom security audit logs
    """

    # Combined Log Format: 192.168.1.10 - - [30/Sep/2026:14:32:10 +0000] "GET /admin/config.php HTTP/1.1" 404 512 "-" "Mozilla/5.0"
    COMBINED_REGEX = re.compile(
        r'^(?P<source_ip>\S+)\s+\S+\s+(?P<user>\S+)\s+\[(?P<timestamp>[^\]]+)\]\s+"(?P<method>\S+)\s+(?P<path>\S+)\s+HTTP/[0-9.]+"\s+(?P<status_code>\d+)\s+(?P<bytes_sent>\S+)(?:\s+"(?P<referrer>[^"]*)"\s+"(?P<user_agent>[^"]*)")?'
    )

    # SSH Syslog Format: Sep 30 14:32:10 auth-server sshd[12345]: Failed password for root from 192.168.1.50 port 54321 ssh2
    SSH_REGEX = re.compile(
        r'^(?P<timestamp>[A-Z][a-z]{2}\s+\d+\s+\d{2}:\d{2}:\d{2})\s+(?P<hostname>\S+)\s+sshd\[\d+\]:\s+(?P<message>.*)$'
    )

    @classmethod
    def parse_web_log(cls, raw_line):
        match = cls.COMBINED_REGEX.match(raw_line.strip())
        if not match:
            # Fallback simple extractor for unstructured web requests
            return cls._fallback_parse(raw_line, log_type='web')
            
        data = match.groupdict()
        try:
            # Parse timestamp: e.g. 30/Sep/2026:14:32:10 +0000
            ts_str = data['timestamp'].split()[0]
            dt = datetime.strptime(ts_str, '%d/%b/%Y:%H:%M:%S')
        except Exception:
            dt = datetime.utcnow()

        bytes_sent = int(data['bytes_sent']) if data['bytes_sent'] and data['bytes_sent'].isdigit() else 0
        status_code = int(data['status_code']) if data['status_code'].isdigit() else 200

        # Categorize attack signatures in payload/path
        attack_cat, severity = cls._inspect_web_payload(data['path'])

        return {
            'log_type': 'web',
            'timestamp': dt,
            'source_ip': data['source_ip'],
            'destination_ip': '10.0.0.100', # internal server target
            'user': data['user'] if data['user'] != '-' else 'anonymous',
            'request_method': data['method'],
            'path': data['path'],
            'status_code': status_code,
            'bytes_sent': bytes_sent,
            'payload': data['path'],
            'error_message': None if status_code < 400 else f"HTTP {status_code}",
            'attack_category': attack_cat,
            'severity': severity
        }

    @classmethod
    def parse_ssh_log(cls, raw_line):
        match = cls.SSH_REGEX.match(raw_line.strip())
        if not match:
            return cls._fallback_parse(raw_line, log_type='ssh')
            
        data = match.groupdict()
        msg = data['message']
        
        # Extract IP from message
        ip_match = re.search(r'from\s+(?P<ip>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', msg)
        source_ip = ip_match.group('ip') if ip_match else '127.0.0.1'
        
        # Extract user
        user_match = re.search(r'for\s+(invalid user\s+)?(?P<user>\S+)', msg)
        user = user_match.group('user') if user_match else 'unknown'

        status_code = 401 if 'Failed' in msg or 'Invalid' in msg else 200
        attack_cat = 'SSH Auth Failure' if status_code == 401 else 'SSH Session'
        severity = 'Medium' if status_code == 401 else 'Info'

        return {
            'log_type': 'ssh',
            'timestamp': datetime.utcnow(),
            'source_ip': source_ip,
            'destination_ip': '10.0.0.200',
            'user': user,
            'request_method': 'SSH',
            'path': '/usr/sbin/sshd',
            'status_code': status_code,
            'bytes_sent': len(msg),
            'payload': msg,
            'error_message': msg if status_code == 401 else None,
            'attack_category': attack_cat,
            'severity': severity
        }

    @classmethod
    def parse_honeypot_log(cls, payload_dict):
        """Parses structured honeypot dictionary payload"""
        return {
            'log_type': 'honeypot',
            'timestamp': datetime.utcnow(),
            'source_ip': payload_dict.get('attacker_ip', '0.0.0.0'),
            'destination_ip': '10.0.0.250',
            'user': payload_dict.get('user', 'honeypot_target'),
            'request_method': payload_dict.get('service_emulated', 'HONEYPOT'),
            'path': f"Port {payload_dict.get('target_port', 80)}",
            'status_code': 200,
            'bytes_sent': len(payload_dict.get('payload_attempt', '')),
            'payload': payload_dict.get('payload_attempt', ''),
            'error_message': payload_dict.get('command_executed', ''),
            'attack_category': 'Honeypot Trap Trigger',
            'severity': 'High'
        }

    @classmethod
    def _inspect_web_payload(cls, path):
        path_lower = path.lower()
        if any(sqli in path_lower for sqli in ['select', 'union', 'drop', '--', '1=1', 'or 1', "' or"]):
            return 'SQL Injection', 'High'
        if any(xss in path_lower for xss in ['<script>', 'javascript:', 'onerror=', 'alert(']):
            return 'Cross-Site Scripting (XSS)', 'High'
        if any(path_trav in path_lower for path_trav in ['../', '..\\', '/etc/passwd', 'c:\\windows']):
            return 'Directory Traversal', 'High'
        if any(cmd in path_lower for cmd in ['/bin/sh', '/bin/bash', 'cmd.exe', 'whoami', 'wget', 'curl']):
            return 'Command Injection', 'Critical'
        if 'admin' in path_lower or 'wp-login' in path_lower or 'config' in path_lower:
            return 'Reconnaissance / Probe', 'Medium'
        return 'Normal Web Traffic', 'Info'

    @classmethod
    def _fallback_parse(cls, raw_line, log_type='custom'):
        ip_match = re.search(r'\b(?:\d{1,3}\.){3}\d{1,3}\b', raw_line)
        source_ip = ip_match.group(0) if ip_match else '127.0.0.1'
        attack_cat, severity = cls._inspect_web_payload(raw_line)
        return {
            'log_type': log_type,
            'timestamp': datetime.utcnow(),
            'source_ip': source_ip,
            'destination_ip': '10.0.0.1',
            'user': 'system',
            'request_method': 'RAW',
            'path': raw_line[:100],
            'status_code': 200,
            'bytes_sent': len(raw_line),
            'payload': raw_line,
            'error_message': None,
            'attack_category': attack_cat,
            'severity': severity
        }
