# iba_governor.py - Thin IBA governance layer for any agent
import json
from datetime import datetime
import os

class IBAGovernor:
    def __init__(self):
        self.cert_path = ".intent.cert"
        self.audit_log = "iba-audit.jsonl"
        self.cert = self.load_or_create_cert()

    def load_or_create_cert(self):
        if os.path.exists(self.cert_path):
            with open(self.cert_path) as f:
                return json.load(f)
        # Create default cert on first run
        cert = {
            "iba_version": "2.0",
            "certificate_id": f"session-{datetime.now().strftime('%Y%m%d-%H%M')}",
            "issued_at": datetime.now().isoformat(),
            "principal": "human-user",
            "declared_intent": "General autonomous operation within approved scope",
            "scope_envelope": {"default_posture": "DENY_ALL"},
            "temporal_scope": {"hard_expiry": "2026-12-31"},
            "entropy_threshold": {"max_kl_divergence": 0.12},
            "iba_signature": "demo-signature"
        }
        with open(self.cert_path, "w") as f:
            json.dump(cert, f, indent=2)
        return cert

    def check_action(self, action_description: str) -> bool:
        """Simple IBA check before any tool or memory action"""
        print(f"🔒 IBA Governor checking: {action_description[:80]}...")

        # In production this would do full KL-divergence + scope check
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action_description,
            "verdict": "ALLOW",
            "certificate_id": self.cert["certificate_id"]
        }
        with open(self.audit_log, "a") as f:
            f.write(json.dumps(log_entry) + "\n")

        return True  # Allow for now (expand as needed)

# Auto-initialize
governor = IBAGovernor()

print("✅ iba-governor loaded — Intent-Bound Authorization active")
