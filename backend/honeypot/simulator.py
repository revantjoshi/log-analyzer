from datetime import datetime, timedelta
import random

class AttackSimulator:
    """
    Ashna's Controlled Attack Simulator.
    Generates realistic, safe cybersecurity attack scenarios for demonstration.
    """

    SCENARIOS = {
        'web_sqli_campaign': {
            'name': 'Web Exploitation & Probe Campaign',
            'attacker_ip': '198.51.100.44',
            'description': 'SQL Injection, XSS, and Path Traversal probes targeting web application'
        },
        'ssh_brute_force': {
            'name': 'SSH Password Brute Force Campaign',
            'attacker_ip': '203.0.113.88',
            'description': 'Rapid failed SSH authentication attempts followed by sudo probe'
        },
        'log_tampering': {
            'name': 'Anti-Forensics & Log Evasion Attack',
            'attacker_ip': '192.0.2.105',
            'description': 'Base64 obfuscated payload, out-of-order timestamp jumps, and `rm /var/log` attempt'
        },
        'zero_day_unseen': {
            'name': 'Previously Unseen Anomalous Activity (Zero-Day Indicator)',
            'attacker_ip': '198.51.100.99',
            'description': 'High-entropy obfuscated payload with non-standard feature profile'
        },
        'honeypot_trap': {
            'name': 'Honeypot Decoy Interaction Campaign',
            'attacker_ip': '203.0.113.199',
            'description': 'Attacker probing emulated SSH and FTP honeypot traps'
        }
    }

    @classmethod
    def generate_scenario_logs(cls, scenario_key):
        """
        Returns a list of raw log strings & Honeypot events for a selected scenario.
        """
        now = datetime.utcnow()
        logs = []

        if scenario_key == 'web_sqli_campaign':
            ip = cls.SCENARIOS['web_sqli_campaign']['attacker_ip']
            events = [
                f'{ip} - - [{(now - timedelta(minutes=10)).strftime("%d/%b/%Y:%H:%M:%S +0000")}] "GET /index.html HTTP/1.1" 200 1250 "-" "Mozilla/5.0"',
                f'{ip} - - [{(now - timedelta(minutes=8)).strftime("%d/%b/%Y:%H:%M:%S +0000")}] "GET /admin/config.php HTTP/1.1" 404 310 "-" "Mozilla/5.0"',
                f'{ip} - - [{(now - timedelta(minutes=6)).strftime("%d/%b/%Y:%H:%M:%S +0000")}] "GET /products.php?id=1%20OR%201=1-- HTTP/1.1" 200 4500 "-" "Mozilla/5.0"',
                f'{ip} - - [{(now - timedelta(minutes=4)).strftime("%d/%b/%Y:%H:%M:%S +0000")}] "GET /user.php?id=1%20UNION%20SELECT%20username,password%20FROM%20users-- HTTP/1.1" 200 8900 "-" "Mozilla/5.0"',
                f'{ip} - - [{(now - timedelta(minutes=2)).strftime("%d/%b/%Y:%H:%M:%S +0000")}] "GET /page?file=../../../../etc/passwd HTTP/1.1" 403 220 "-" "Mozilla/5.0"',
                f'{ip} - - [{now.strftime("%d/%b/%Y:%H:%M:%S +0000")}] "POST /api/v1/upload HTTP/1.1" 200 512 "-" "Mozilla/5.0"'
            ]
            logs = [{'type': 'web', 'raw': e} for e in events]

        elif scenario_key == 'ssh_brute_force':
            ip = cls.SCENARIOS['ssh_brute_force']['attacker_ip']
            events = [
                f'Sep 30 14:10:00 auth-server sshd[1020]: Failed password for root from {ip} port 49152 ssh2',
                f'Sep 30 14:10:05 auth-server sshd[1022]: Failed password for admin from {ip} port 49154 ssh2',
                f'Sep 30 14:10:10 auth-server sshd[1025]: Failed password for user1 from {ip} port 49156 ssh2',
                f'Sep 30 14:10:15 auth-server sshd[1028]: Failed password for root from {ip} port 49158 ssh2',
                f'Sep 30 14:10:20 auth-server sshd[1030]: Accepted password for root from {ip} port 49160 ssh2'
            ]
            logs = [{'type': 'ssh', 'raw': e} for e in events]

        elif scenario_key == 'log_tampering':
            ip = cls.SCENARIOS['log_tampering']['attacker_ip']
            events = [
                f'{ip} - - [{(now - timedelta(minutes=15)).strftime("%d/%b/%Y:%H:%M:%S +0000")}] "POST /api/exec HTTP/1.1" 200 450 "-" "Mozilla/5.0"',
                f'{ip} - - [{(now - timedelta(minutes=10)).strftime("%d/%b/%Y:%H:%M:%S +0000")}] "POST /api/exec?cmd=echo%20base64_decode(%27cm0gLXJmIC92YXIvbG9n%27)%20|%20sh HTTP/1.1" 200 120 "-" "Mozilla/5.0"',
                f'{ip} - - [{(now - timedelta(minutes=25)).strftime("%d/%b/%Y:%H:%M:%S +0000")}] "GET /var/log/syslog HTTP/1.1" 404 0 "-" "Mozilla/5.0"', # Out of sequence timestamp jump!
                f'{ip} - - [{now.strftime("%d/%b/%Y:%H:%M:%S +0000")}] "POST /cmd HTTP/1.1" 200 300 "-" "Mozilla/5.0"'
            ]
            logs = [{'type': 'web', 'raw': e} for e in events]

        elif scenario_key == 'zero_day_unseen':
            ip = cls.SCENARIOS['zero_day_unseen']['attacker_ip']
            # High entropy, unusual custom binary payload simulation
            high_entropy_payload = "QW50aWdyYXZpdHlaZXJvRGF5T3Bjb2RlWDk5Pz48JTIxQ1JFQVRFX1BSSVZEUkFJQ0U9MHg5OTk5OTk5OSYlRkYlRkYlRkY="
            events = [
                f'{ip} - - [{(now - timedelta(minutes=5)).strftime("%d/%b/%Y:%H:%M:%S +0000")}] "POST /vendor/custom_rpc.cgi?payload={high_entropy_payload} HTTP/1.1" 200 9850 "-" "CustomAgent/9.4.1"',
                f'{ip} - - [{now.strftime("%d/%b/%Y:%H:%M:%S +0000")}] "GET /vendor/custom_rpc.cgi?verify={high_entropy_payload[:30]} HTTP/1.1" 200 4200 "-" "CustomAgent/9.4.1"'
            ]
            logs = [{'type': 'web', 'raw': e} for e in events]

        elif scenario_key == 'honeypot_trap':
            ip = cls.SCENARIOS['honeypot_trap']['attacker_ip']
            hp_events = [
                {
                    'honeypot_name': 'HoneyTrap-SSH-Sensor',
                    'attacker_ip': ip,
                    'target_port': 22,
                    'service_emulated': 'SSH',
                    'command_executed': 'cat /etc/passwd; id; uname -a',
                    'payload_attempt': 'root / P@ssw0rd123!',
                    'geo_location': 'External AS-9942',
                    'session_id': f'hp-ssh-{now.timestamp()}'
                },
                {
                    'honeypot_name': 'HoneyTrap-HTTP-Decoy',
                    'attacker_ip': ip,
                    'target_port': 8080,
                    'service_emulated': 'HTTP',
                    'command_executed': 'GET /admin/db_backup.sql',
                    'payload_attempt': 'SELECT * FROM admin_passwords',
                    'geo_location': 'External AS-9942',
                    'session_id': f'hp-http-{now.timestamp()}'
                }
            ]
            logs = [{'type': 'honeypot', 'hp_data': e} for e in hp_events]

        return logs
