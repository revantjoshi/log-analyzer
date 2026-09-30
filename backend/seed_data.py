import os
import sys
from werkzeug.security import generate_password_hash

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.app import create_app
from backend.models import db, User
from backend.honeypot.simulator import AttackSimulator

def seed_database():
    app = create_app()
    with app.app_context():
        print("[Seeding] Resetting database tables...")
        db.drop_all()
        db.create_all()

        print("[Seeding] Creating default Analyst user...")
        admin = User(
            username='admin',
            password_hash=generate_password_hash('admin123'),
            role='admin'
        )
        db.session.add(admin)
        db.session.commit()

        print("[Seeding] Running initial Attack Simulation Scenarios (Revant, Janani, Ashna)...")
        # Run Web SQLi campaign
        from backend.routes.log_routes import process_and_save_log
        from backend.honeypot.honeypot_api import HoneypotManager

        scenarios = ['web_sqli_campaign', 'ssh_brute_force', 'log_tampering', 'zero_day_unseen', 'honeypot_trap']
        
        for sc in scenarios:
            logs = AttackSimulator.generate_scenario_logs(sc)
            for item in logs:
                if item['type'] == 'honeypot':
                    expected_key = app.config['HONEYPOT_API_KEY']
                    HoneypotManager.ingest_honeypot_event(item['hp_data'], expected_key, expected_key)
                else:
                    process_and_save_log(item['raw'], source=item['type'])

        print("[Seeding] Database successfully seeded with full cybersecurity demonstration dataset!")

if __name__ == '__main__':
    seed_database()
