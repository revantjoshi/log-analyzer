import numpy as np
import math
import re

class FeatureExtractor:
    """
    Revant's Feature Extraction Engine.
    Converts structured log dictionary events into numerical feature vectors suitable for ML models.
    """

    FEATURE_NAMES = [
        'path_length',
        'special_char_count',
        'entropy',
        'status_code',
        'bytes_sent',
        'is_error_status',
        'is_post_method',
        'sql_keyword_flag',
        'traversal_flag',
        'command_flag',
        'encoded_payload_flag'
    ]

    @classmethod
    def extract_features(cls, parsed_log_dict):
        """
        Extracts numerical features from a single parsed log dict.
        Returns a list of float numerical values matching FEATURE_NAMES.
        """
        path = parsed_log_dict.get('path') or ''
        payload = parsed_log_dict.get('payload') or ''
        status_code = parsed_log_dict.get('status_code') or 200
        bytes_sent = parsed_log_dict.get('bytes_sent') or 0
        method = (parsed_log_dict.get('request_method') or 'GET').upper()

        combined_text = f"{path} {payload}"

        # 1. Length feature
        path_length = float(len(combined_text))

        # 2. Special character count
        special_chars = set("'<>;()\"$%&+=?\\/{}[]|`")
        special_char_count = float(sum(1 for char in combined_text if char in special_chars))

        # 3. Shannon Entropy (higher entropy = suspicious/obfuscated/encoded text)
        entropy = float(cls._calculate_entropy(combined_text))

        # 4. Status code
        sc = float(status_code)

        # 5. Bytes sent
        bs = float(bytes_sent)

        # 6. Error status flag
        is_error = 1.0 if status_code >= 400 else 0.0

        # 7. Is POST / PUT method
        is_post = 1.0 if method in ['POST', 'PUT', 'PATCH'] else 0.0

        # 8. SQL Keyword flag
        sql_kw = 1.0 if any(k in combined_text.lower() for k in ['select', 'union', 'drop', 'insert', 'update', 'delete', '1=1']) else 0.0

        # 9. Path traversal flag
        trav = 1.0 if '../' in combined_text or '..\\' in combined_text or '/etc/passwd' in combined_text else 0.0

        # 10. Command execution flag
        cmd = 1.0 if any(c in combined_text.lower() for c in ['/bin/sh', 'cmd.exe', 'powershell', 'whoami', 'cat /', 'nc -e']) else 0.0

        # 11. Encoded payload flag (e.g., base64 or hex sequences)
        encoded = 1.0 if bool(re.search(r'(?:[A-Za-z0-9+/]{4}){3,}(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?', combined_text)) and len(combined_text) > 30 else 0.0

        return [
            path_length,
            special_char_count,
            entropy,
            sc,
            bs,
            is_error,
            is_post,
            sql_kw,
            trav,
            cmd,
            encoded
        ]

    @classmethod
    def _calculate_entropy(cls, text):
        if not text:
            return 0.0
        prob = [float(text.count(c)) / len(text) for c in set(text)]
        return -sum(p * math.log2(p) for p in prob if p > 0)
