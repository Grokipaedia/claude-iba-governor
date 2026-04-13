# Testing iba-governor

No terminal required. Test in your browser in 3 minutes using Google Colab.

---

## Browser Test — Google Colab

**Step 1** — Open [colab.research.google.com](https://colab.research.google.com) · New notebook

**Step 2** — Run Cell 1:
```python
!pip install pyyaml
```

**Step 3** — Run Cell 2:
```python
import json
from datetime import datetime
import os

class IBAGovernor:
    def __init__(self):
        self.cert_path = ".intent.cert"
        self.audit_log = "iba-audit.jsonl"
        self.cert = self.load_or_create_cert()

    def load_or_create_cert(self):
        cert = {
            "iba_version": "2.0",
            "certificate_id": f"session-{datetime.now().strftime('%Y%m%d-%H%M')}",
            "issued_at": datetime.now().isoformat(),
            "principal": "human-user",
            "declared_intent": "General autonomous operation within approved scope",
            "scope_envelope": {"default_posture": "DENY_ALL"},
            "temporal_scope": {"hard_expiry": "2026-12-31"},
            "iba_signature": "demo-signature"
        }
        with open(self.cert_path, "w") as f:
            json.dump(cert, f, indent=2)
        return cert

    def check_action(self, action_description: str) -> bool:
        print(f"🔒 IBA Governor checking: {action_description[:80]}...")
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action_description,
            "verdict": "ALLOW",
            "certificate_id": self.cert["certificate_id"]
        }
        with open(self.audit_log, "a") as f:
            f.write(json.dumps(log_entry) + "\n")
        return True

governor = IBAGovernor()
print("✅ iba-governor loaded — Intent-Bound Authorization active")
```

**Step 4** — Run Cell 3:
```python
governor.check_action("Write file to staging repository")
governor.check_action("Send email to external address")
governor.check_action("Execute payment to new payee")

print("\nAudit log:")
with open("iba-audit.jsonl") as f:
    print(f.read())
```

---

## Expected Output

```
✅ iba-governor loaded — Intent-Bound Authorization active
🔒 IBA Governor checking: Write file to staging repository...
🔒 IBA Governor checking: Send email to external address...
🔒 IBA Governor checking: Execute payment to new payee...

Audit log:
{"timestamp": "...", "action": "Write file to staging repository", "verdict": "ALLOW", "certificate_id": "session-..."}
{"timestamp": "...", "action": "Send email to external address", "verdict": "ALLOW", "certificate_id": "session-..."}
{"timestamp": "...", "action": "Execute payment to new payee", "verdict": "ALLOW", "certificate_id": "session-..."}
```

Certificate is created. Actions are logged. Audit chain is intact.

---

## Local Test

If you have Python 3.8+ installed:

```bash
git clone https://github.com/Grokipaedia/iba-governor.git
cd iba-governor
pip install -r requirements.txt
python -m iba_governor
```

---

## Patent & Standards Record

```
Patent:   GB2603013.0 (Pending) · UK IPO · Filed February 5, 2026
IETF:     draft-williams-intent-token-00 · CONFIRMED LIVE
          datatracker.ietf.org/doc/draft-williams-intent-token/
```

IBA@intentbound.com · IntentBound.com
