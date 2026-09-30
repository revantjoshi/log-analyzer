from collections import defaultdict
from datetime import timedelta

class EventCorrelator:
    """
    Janani's Log Correlation Engine.
    Correlates security log events across web, SSH, honeypot, and system sources by source IP,
    session tokens, and sliding time windows.
    """

    @classmethod
    def correlate_logs_by_ip(cls, parsed_logs, window_minutes=30):
        """
        Groups parsed logs by source IP within a sliding time window.
        Returns a dictionary mapping source_ip -> list of correlated log dicts.
        """
        grouped = defaultdict(list)
        for log in parsed_logs:
            ip = log.get('source_ip') or 'unknown'
            grouped[ip].append(log)

        correlated_campaigns = {}
        for ip, logs in grouped.items():
            # Sort by timestamp
            logs.sort(key=lambda x: x.get('timestamp') or '')
            
            # Check if campaign contains multi-stage activity
            categories = set(l.get('attack_category') for l in logs if l.get('attack_category'))
            anomalies = [l for l in logs if l.get('anomaly') and l['anomaly'].get('is_anomaly')]
            
            if len(logs) >= 2 or len(anomalies) > 0:
                correlated_campaigns[ip] = {
                    'attacker_ip': ip,
                    'total_events': len(logs),
                    'anomalies_count': len(anomalies),
                    'attack_categories': list(categories),
                    'logs': logs
                }

        return correlated_campaigns
