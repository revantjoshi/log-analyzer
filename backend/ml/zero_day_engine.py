class ZeroDayProfilingEngine:
    """
    Revant's Zero-Day / Novelty Profiling Engine.
    Identifies previously unseen anomalous behavior that does NOT fit known signature patterns.
    
    Technical Scope:
    Accurately presented as 'Detection of previously unseen anomalous behaviour that may indicate zero-day activity.'
    """

    KNOWN_SIGNATURE_CATEGORIES = [
        'SQL Injection',
        'Cross-Site Scripting (XSS)',
        'Directory Traversal',
        'Command Injection',
        'SSH Auth Failure'
    ]

    @classmethod
    def evaluate_zero_day_indicator(cls, parsed_log_dict, ml_result):
        """
        Evaluates whether an anomaly constitutes a candidate for previously unseen / zero-day activity.
        
        Criteria for Zero-Day Candidate:
        1. High Anomaly Score (> 0.70)
        2. High Novelty / Entropy / Structural Deviation
        3. NO match to standard known signature patterns OR contains unusual obfuscated payloads
        """
        anomaly_score = ml_result.get('anomaly_score', 0.0)
        is_anomaly = ml_result.get('is_anomaly', False)
        attack_category = parsed_log_dict.get('attack_category', 'Normal Web Traffic')
        fc = ml_result.get('feature_contributions', {})

        entropy = fc.get('entropy', 0.0)
        encoded_flag = fc.get('encoded_payload_flag', 0.0)
        dev_score = ml_result.get('deviation_score', 0.0)

        # High anomaly + not standard known signature OR high obfuscation entropy
        is_known_signature = attack_category in cls.KNOWN_SIGNATURE_CATEGORIES
        
        is_zero_day = False
        novelty_score = 0.0
        reason = "Normal baseline pattern"

        if is_anomaly:
            if not is_known_signature and anomaly_score > 0.68:
                is_zero_day = True
                novelty_score = round(min(0.98, anomaly_score + 0.15), 3)
                reason = "High statistical anomaly without known signature match (Unseen Pattern)."
            elif encoded_flag > 0.0 and entropy > 3.0:
                is_zero_day = True
                novelty_score = round(min(0.99, anomaly_score + 0.2), 3)
                reason = "High entropy obfuscated payload indicating potential previously unseen exploit attempt."
            elif dev_score > 3.5:
                is_zero_day = True
                novelty_score = round(min(0.95, dev_score / 5.0), 3)
                reason = "Extreme structural feature deviation from baseline normal behavior model."
            else:
                novelty_score = round(anomaly_score * 0.5, 3)
                reason = f"Known attack signature matched ({attack_category})."

        return {
            'is_zero_day_candidate': is_zero_day,
            'novelty_score': novelty_score,
            'detection_reason': reason,
            'technical_label': "Detection of previously unseen anomalous behaviour that may indicate zero-day activity" if is_zero_day else "Known/Baseline Activity"
        }
