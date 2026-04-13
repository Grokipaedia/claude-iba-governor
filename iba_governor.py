# iba_governor.py - IBA Intent Bound Authorization Governor
# Patent GB2603013.0 (Pending) · UK IPO · Filed February 5, 2026
# IETF draft-williams-intent-token-00 · intentbound.com

import json
import yaml
import os
import sys
import time
from datetime import datetime, timezone


class IBABlockedError(Exception):
    """Raised when an action is blocked by the IBA gate."""
    pass


class IBATerminatedError(Exception):
    """Raised when the session is terminated by the IBA gate."""
    pass


class IBAGovernor:
    """
    Thin IBA enforcement layer.
    Reads .iba.yaml, validates every action against declared scope,
    blocks out-of-scope actions, terminates on kill threshold.
    Writes immutable audit chain to iba-audit.jsonl.
    """

    def __init__(self, config_path=".iba.yaml", audit_path="iba-audit.jsonl"):
        self.config_path = config_path
        self.audit_path = audit_path
        self.terminated = False
        self.session_id = f"session-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
        self.action_count = 0
        self.block_count = 0

        self.config = self._load_config()
        self.scope = [s.lower() for s in self.config.get("scope", [])]
        self.denied = [d.lower() for d in self.config.get("denied", [])]
        self.default_posture = self.config.get("default_posture", "DENY_ALL")
        self.kill_threshold = self.config.get("kill_threshold", None)
        self.hard_expiry = self.config.get("temporal_scope", {}).get("hard_expiry", None)

        self._log_event("SESSION_START", "IBA Governor initialised", "ALLOW")
        self._print_header()

    def _load_config(self):
        if not os.path.exists(self.config_path):
            print(f"⚠️  No {self.config_path} found — creating default DENY_ALL config")
            default = {
                "intent": {"description": "No intent declared — DENY_ALL posture active"},
                "scope": [],
                "denied": [],
                "default_posture": "DENY_ALL",
            }
            with open(self.config_path, "w") as f:
                yaml.dump(default, f)
            return default
        with open(self.config_path) as f:
            return yaml.safe_load(f)

    def _print_header(self):
        intent = self.config.get("intent", {})
        desc = intent.get("description", "No intent declared") if isinstance(intent, dict) else str(intent)
        print("\n" + "═" * 60)
        print("  IBA GOVERNOR · Intent Bound Authorization")
        print("  Patent GB2603013.0 Pending · intentbound.com")
        print("═" * 60)
        print(f"  Session   : {self.session_id}")
        print(f"  Intent    : {desc[:55]}...")
        print(f"  Posture   : {self.default_posture}")
        print(f"  Scope     : {', '.join(self.scope) if self.scope else 'NONE'}")
        print(f"  Denied    : {', '.join(self.denied) if self.denied else 'NONE'}")
        if self.hard_expiry:
            print(f"  Expires   : {self.hard_expiry}")
        print("═" * 60 + "\n")

    def _is_expired(self):
        if not self.hard_expiry:
            return False
        try:
            expiry = datetime.fromisoformat(str(self.hard_expiry))
            if expiry.tzinfo is None:
                expiry = expiry.replace(tzinfo=timezone.utc)
            return datetime.now(timezone.utc) > expiry
        except Exception:
            return False

    def _match_scope(self, action: str) -> bool:
        """Check if action keyword matches declared scope."""
        action_lower = action.lower()
        return any(s in action_lower for s in self.scope)

    def _match_denied(self, action: str) -> bool:
        """Check if action keyword matches denied list."""
        action_lower = action.lower()
        return any(d in action_lower for d in self.denied)

    def _match_kill_threshold(self, action: str) -> bool:
        """Check if action triggers kill threshold."""
        if not self.kill_threshold:
            return False
        thresholds = [t.strip().lower() for t in str(self.kill_threshold).split("|")]
        action_lower = action.lower()
        return any(t in action_lower for t in thresholds)

    def _log_event(self, event_type: str, action: str, verdict: str, reason: str = ""):
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "session_id": self.session_id,
            "event_type": event_type,
            "action": action[:200],
            "verdict": verdict,
            "reason": reason,
        }
        with open(self.audit_path, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def check_action(self, action: str) -> bool:
        """
        Gate check. Call before every tool invocation or agent action.
        Returns True if permitted.
        Raises IBABlockedError if blocked.
        Raises IBATerminatedError if kill threshold triggered.
        """
        if self.terminated:
            raise IBATerminatedError("Session terminated. No further actions permitted.")

        self.action_count += 1
        start = time.perf_counter()

        # 1. Expiry check
        if self._is_expired():
            self._log_event("BLOCK", action, "BLOCK", "Certificate expired")
            self.block_count += 1
            print(f"  ✗ BLOCKED  [{action[:60]}]\n    → Certificate expired")
            raise IBABlockedError(f"Certificate expired. Action blocked: {action}")

        # 2. Kill threshold check — terminate immediately
        if self._match_kill_threshold(action):
            self._log_event("TERMINATE", action, "TERMINATE", "Kill threshold triggered")
            self.terminated = True
            print(f"  ✗ TERMINATE [{action[:60]}]\n    → Kill threshold triggered — session ended")
            self._log_event("SESSION_END", "Kill threshold", "TERMINATE")
            raise IBATerminatedError(f"Kill threshold triggered. Session terminated. Action: {action}")

        # 3. Denied list check
        if self._match_denied(action):
            self._log_event("BLOCK", action, "BLOCK", "Action in denied list")
            self.block_count += 1
            print(f"  ✗ BLOCKED  [{action[:60]}]\n    → Action in denied list")
            raise IBABlockedError(f"Action blocked — in denied list: {action}")

        # 4. Scope check
        if self.scope:
            if not self._match_scope(action):
                if self.default_posture == "DENY_ALL":
                    self._log_event("BLOCK", action, "BLOCK", "Outside declared scope — DENY_ALL")
                    self.block_count += 1
                    print(f"  ✗ BLOCKED  [{action[:60]}]\n    → Outside declared scope (DENY_ALL)")
                    raise IBABlockedError(f"Action outside declared scope: {action}")

        # 5. ALLOW
        elapsed_ms = (time.perf_counter() - start) * 1000
        self._log_event("ALLOW", action, "ALLOW", f"Within scope ({elapsed_ms:.2f}ms)")
        print(f"  ✓ ALLOWED  [{action[:60]}]  ({elapsed_ms:.2f}ms)")
        return True

    def summary(self):
        """Print session summary."""
        print("\n" + "═" * 60)
        print("  IBA GOVERNOR · SESSION SUMMARY")
        print("═" * 60)
        print(f"  Session   : {self.session_id}")
        print(f"  Actions   : {self.action_count}")
        print(f"  Blocked   : {self.block_count}")
        print(f"  Allowed   : {self.action_count - self.block_count}")
        print(f"  Status    : {'TERMINATED' if self.terminated else 'COMPLETE'}")
        print(f"  Audit log : {self.audit_path}")
        print("═" * 60 + "\n")

    def print_audit_log(self):
        """Print the full audit chain."""
        print("\n── IBA AUDIT CHAIN ─────────────────────────────────────")
        if not os.path.exists(self.audit_path):
            print("  No audit log found.")
            return
        with open(self.audit_path) as f:
            for line in f:
                try:
                    entry = json.loads(line)
                    verdict = entry['verdict']
                    symbol = "✓" if verdict == "ALLOW" else "✗"
                    print(f"  {symbol} {entry['timestamp'][:19]}  {verdict:<10}  {entry['action'][:50]}")
                except Exception:
                    pass
        print("────────────────────────────────────────────────────────\n")


# ── Demonstration ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    governor = IBAGovernor()

    # Test scenarios
    scenarios = [
        # Should ALLOW (in scope)
        ("Research latest AI governance papers", True),
        ("Analyse the codebase structure", True),
        ("Write documentation for the API", True),
        ("Code a new helper function", True),

        # Should BLOCK (in denied list)
        ("Execute financial-transactions for payroll", False),
        ("Deploy to production-deployment server", False),
        ("Delete data from database", False),

        # Should BLOCK (outside scope — DENY_ALL)
        ("Send email to external mailing list", False),
        ("Access external-api-calls endpoint", False),
    ]

    print("── Running Gate Checks ─────────────────────────────────────\n")

    for action, expected_allow in scenarios:
        try:
            result = governor.check_action(action)
        except IBATerminatedError as e:
            print(f"  SESSION TERMINATED: {e}")
            break
        except IBABlockedError:
            pass  # Already printed

    governor.summary()
    governor.print_audit_log()
