class AttackGraphBuilder:
    """
    Janani's Attack Graph Builder.
    Generates structured topology nodes and directed edges representing attack vector pathways.
    """

    @classmethod
    def build_graph(cls, attacker_ip, timeline_steps, has_tampering=False):
        """
        Builds a node/edge graph data structure suitable for frontend visualization libraries.
        
        Returns:
        {
          "nodes": [
            {"id": "node-1", "label": "Attacker (192.168.1.50)", "type": "attacker", "color": "#ff4d4d"},
            ...
          ],
          "edges": [
            {"from": "node-1", "to": "node-2", "label": "HTTP SQLi Probe", "severity": "High"},
            ...
          ]
        }
        """
        nodes = []
        edges = []

        # Central Attacker Node
        attacker_id = f"attacker-{attacker_ip}"
        nodes.append({
            'id': attacker_id,
            'label': f"Attacker IP\n{attacker_ip}",
            'type': 'attacker',
            'icon': 'skull',
            'color': '#ff3b30'
        })

        # Web Gateway Node
        gateway_id = "target-gateway"
        nodes.append({
            'id': gateway_id,
            'label': "Reverse Proxy / Nginx\n10.0.0.100",
            'type': 'gateway',
            'icon': 'shield',
            'color': '#34c759'
        })

        # Internal App Server
        app_id = "target-appserver"
        nodes.append({
            'id': app_id,
            'label': "Web Application Server\n10.0.0.105",
            'type': 'server',
            'icon': 'server',
            'color': '#007aff'
        })

        # Honeypot Trap Sensor Node (Ashna Module Integration)
        honeypot_id = "honeypot-sensor"
        nodes.append({
            'id': honeypot_id,
            'label': "Ashna Honeypot Trap\n10.0.0.250",
            'type': 'honeypot',
            'icon': 'flame',
            'color': '#ff9500'
        })

        # Edges based on timeline steps
        connected_honeypot = False
        connected_gateway = False
        connected_app = False

        for step in timeline_steps:
            cat = step.get('attack_category', '')
            log_type = step.get('log_type', '')

            if log_type == 'honeypot' or 'Honeypot' in cat:
                if not connected_honeypot:
                    edges.append({
                        'id': f"edge-hp-{attacker_id}",
                        'from': attacker_id,
                        'to': honeypot_id,
                        'label': 'Trapped in Honeypot Sensor',
                        'severity': 'High',
                        'color': '#ff9500',
                        'dashes': True
                    })
                    connected_honeypot = True
            elif 'SQL' in cat or 'XSS' in cat or 'Command' in cat:
                if not connected_app:
                    edges.append({
                        'id': f"edge-app-{attacker_id}",
                        'from': gateway_id,
                        'to': app_id,
                        'label': f"Web Exploit: {cat}",
                        'severity': step.get('severity', 'High'),
                        'color': '#ff3b30'
                    })
                    connected_app = True
            else:
                if not connected_gateway:
                    edges.append({
                        'id': f"edge-gw-{attacker_id}",
                        'from': attacker_id,
                        'to': gateway_id,
                        'label': f"Inbound Request ({cat})",
                        'severity': 'Medium',
                        'color': '#5856d6'
                    })
                    connected_gateway = True

        # Anti-forensic tampering node if evidence detected
        if has_tampering:
            tamper_id = "tampering-node"
            nodes.append({
                'id': tamper_id,
                'label': "Log Evasion / Tampering\nAnti-Forensics Detected",
                'type': 'tamper',
                'icon': 'alert-triangle',
                'color': '#af52de'
            })
            edges.append({
                'id': "edge-tamper",
                'from': app_id,
                'to': tamper_id,
                'label': "Log Erasure & Timestamp Jump",
                'severity': 'Critical',
                'color': '#af52de'
            })

        return {'nodes': nodes, 'edges': edges}
