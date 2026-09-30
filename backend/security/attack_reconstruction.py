from backend.security.evasion_detector import LogEvasionDetector
from backend.security.attack_graph import AttackGraphBuilder

class AttackReconstructionEngine:
    """
    Janani's Attack Sequence Reconstruction Engine.
    Transforms raw correlated log events into end-to-end MITRE ATT&CK story sequences and timelines.
    """

    MITRE_MAPPING = {
        'Reconnaissance / Probe': 'TA0043 - Reconnaissance',
        'SQL Injection': 'TA0001 - Initial Access (Exploit Public App)',
        'Cross-Site Scripting (XSS)': 'TA0001 - Initial Access',
        'Directory Traversal': 'TA0007 - Discovery',
        'Command Injection': 'TA0002 - Execution',
        'SSH Auth Failure': 'TA0006 - Credential Access (Brute Force)',
        'Honeypot Trap Trigger': 'TA0043 - Reconnaissance / Honeypot Telemetry',
        'Log Tampering / Anti-Forensics': 'TA0005 - Defense Evasion'
    }

    @classmethod
    def reconstruct_attack_story(cls, attacker_ip, logs):
        """
        Reconstructs a full attack story from a list of correlated logs for an attacker IP.
        Returns dictionary containing:
        - title
        - description
        - attacker_ip
        - start_time & end_time
        - severity
        - mitre_tactics (array)
        - timeline_data (array of steps)
        - graph_data ({nodes: [], edges: []})
        - has_tampering_evidence (bool)
        """
        if not logs:
            return None

        # Sort logs chronologically
        logs.sort(key=lambda x: x.get('timestamp') or '')

        start_time = logs[0].get('timestamp')
        end_time = logs[-1].get('timestamp')

        timeline_steps = []
        mitre_tactics = set()
        has_tampering = False
        highest_severity = 'Low'

        sev_map = {'Info': 0, 'Low': 1, 'Medium': 2, 'High': 3, 'Critical': 4}

        # Check for evasion indicators
        evasion_alerts = LogEvasionDetector.detect_evasion_indicators(logs)
        if evasion_alerts:
            has_tampering = True
            mitre_tactics.add('TA0005 - Defense Evasion')

        for idx, log in enumerate(logs):
            cat = log.get('attack_category', 'Normal Web Traffic')
            sev = log.get('severity', 'Info')
            
            if sev_map.get(sev, 0) > sev_map.get(highest_severity, 0):
                highest_severity = sev

            mitre_tactic = cls.MITRE_MAPPING.get(cat, 'TA0007 - Discovery')
            mitre_tactics.add(mitre_tactic)

            ts_str = log.get('timestamp')
            if hasattr(ts_str, 'isoformat'):
                ts_str = ts_str.isoformat()

            anomaly_info = log.get('anomaly') or {}
            is_zero_day = anomaly_info.get('is_zero_day_candidate', False)

            step = {
                'step_index': idx + 1,
                'timestamp': ts_str,
                'log_type': log.get('log_type'),
                'source_ip': log.get('source_ip'),
                'target': f"{log.get('destination_ip')}:{log.get('path') or ''}",
                'action': log.get('request_method') or 'ACCESS',
                'attack_category': cat,
                'mitre_tactic': mitre_tactic,
                'severity': sev,
                'payload': log.get('payload') or log.get('path') or '',
                'is_anomaly': anomaly_info.get('is_anomaly', False),
                'is_zero_day': is_zero_day,
                'novelty_reason': anomaly_info.get('detection_reason') if is_zero_day else None
            }
            timeline_steps.append(step)

        # Build attack graph
        graph_data = AttackGraphBuilder.build_graph(attacker_ip, timeline_steps, has_tampering)

        # Story title & summary logic
        tactic_count = len(mitre_tactics)
        if 'TA0002 - Execution' in mitre_tactics or highest_severity == 'Critical':
            title = f"Multi-Stage Cyber Campaign from {attacker_ip} (Critical Exploitation & RCE)"
            desc = f"Complex multi-stage attack campaign originating from IP {attacker_ip} encompassing {tactic_count} MITRE ATT&CK tactics, including remote code execution attempts and honeypot traps."
        elif 'TA0006 - Credential Access (Brute Force)' in mitre_tactics:
            title = f"SSH Brute-Force & Credential Access Campaign from {attacker_ip}"
            desc = f"Automated authentication brute-force attempt targeting SSH and administrative access vectors from IP {attacker_ip}."
        elif has_tampering:
            title = f"Suspicious Activity with Evasion & Log Tampering from {attacker_ip}"
            desc = f"Targeted attack sequence from {attacker_ip} exhibiting clear anti-forensic evidence, timestamp manipulation, and log deletion attempts."
        else:
            title = f"Reconnaissance & Vulnerability Probe from {attacker_ip}"
            desc = f"Automated scanning and vulnerability discovery sequence detected from external IP {attacker_ip}."

        return {
            'title': title,
            'description': desc,
            'attacker_ip': attacker_ip,
            'start_time': start_time,
            'end_time': end_time,
            'severity': highest_severity if not has_tampering else 'Critical',
            'mitre_tactics': list(mitre_tactics),
            'timeline_data': timeline_steps,
            'graph_data': graph_data,
            'has_tampering_evidence': has_tampering,
            'status': 'Active'
        }
