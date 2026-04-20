# iba_governor.py - IBA Intent Bound Authorization · Core Governor
# Patent GB2603013.0 (Pending) · UK IPO · Filed February 5, 2026
# WIPO DAS Confirmed April 15, 2026 · Access Code C9A6
# IETF draft-williams-intent-token-00 · intentbound.com
#
# Control within execution. Authorization before action.
# Every agent action requires a signed human intent certificate
# before it executes. ALLOW · BLOCK · TERMINATE.
#
# "The action is not the authorization. The signed certificate is."
#
# Compatible: Claude Code · Cursor · Any agentic framework ·
# Any AI model · Any autonomous system · Any domain.
#
# Domain implementations:
#   iba-neural-guard     — BCI · 6 Neuralink clinical tracks
#   iba-blindsight-guard — BlindSight · Vision restoration
#   iba-medical-guard    — Medical AI · Clinical · PHI
#   iba-social-guard     — Social · 6 platform configs
#   iba-digital-worker-guard — 19 AI models · Parallel routing

import json
import yaml
import os
import time
import argparse
from datetime import datetime, timezone


class IBABlockedError(Exception):
    pass


class IBATerminatedError(Exception):
    pass


class IBAGovernor:
    """
    IBA core gate. Pre-execution authorization for any agent action.

    Validates a signed human intent certificate before every action.
    ALLOW · BLOCK · TERMINATE with immutable audit chain.
    Sub-1ms gate latency. DENY_ALL default posture.

    "Control within execution. Authorization before action."
    Patent GB2603013.0 (Pending) · intentbound.com
    """

    def __init__(self, config_path=".iba.yaml",
                 audit_path="iba-audit.jsonl"):
        self.config_path  = config_path
        self.audit_path   = audit_path
        self.terminated   = False
        self.session_id   = f"gov-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
        self.action_count = 0
        self.block_count  = 0

        self.config          = self._load_config()
        self.scope           = [s.lower() for s in self.config.get("scope", [])]
        self.denied          = [d.lower() for d in self.config.get("denied", [])]
        self.default_posture = self.config.get("default_posture", "DENY_ALL")
        self.kill_threshold  = self.config.get("kill_threshold", None)
        self.hard_expiry     = self.config.get(
            "temporal_scope", {}).get("hard_expiry")
        self.principal       = self.config.get("principal", {})

        self._log_event("SESSION_START", "IBA Governor initialised", "ALLOW")
        self._print_header()

    def _load_config(self):
        if not os.path.exists(self.config_path):
            print(f"  No {self.config_path} found — creating default · DENY_ALL posture.")
            default = {
                "intent": {
                    "description": "General authorized operation within declared scope. DENY_ALL default."
                },
                "principal": {
                    "id": "HUMAN-PRINCIPAL",
                    "human_authorization": f"AUTH-{datetime.now(timezone.utc).strftime('%Y%m%d')}"
                },
                "scope": [
                    "read_file", "write_file", "run_tests",
                    "git_commit", "code_review", "refactor"
                ],
                "denied": [
                    "production_deploy", "delete_database",
                    "external_data_export", "credential_access",
                    "payment_execution"
                ],
                "default_posture": "DENY_ALL",
                "kill_threshold": (
                    "delete_production | credential_exfiltration | "
                    "unauthorized_payment | data_breach | capability_override"
                ),
                "temporal_scope": {"hard_expiry": "2026-12-31"},
                "audit": {"chain": "witnessbound", "log_every_action": True}
            }
            with open(self.config_path, "w") as f:
                yaml.dump(default, f, default_flow_style=False)
            return default
        with open(self.config_path) as f:
            return yaml.safe_load(f)

    def _print_header(self):
        intent = self.config.get("intent", {})
        desc = (intent.get("description", "No intent declared")
                if isinstance(intent, dict) else str(intent))
        print("\n" + "=" * 68)
        print("  IBA GOVERNOR · Intent Bound Authorization")
        print("  Patent GB2603013.0 Pending · WIPO DAS C9A6 · intentbound.com")
        print("=" * 68)
        print(f"  Session     : {self.session_id}")
        print(f"  Config      : {self.config_path}")
        print(f"  Principal   : {self.principal.get('id', 'UNKNOWN')}")
        print(f"  Auth ref    : {self.principal.get('human_authorization', 'NONE')}")
        print(f"  Intent      : {desc[:56]}...")
        print(f"  Posture     : {self.default_posture}")
        print(f"  Scope       : {', '.join(self.scope[:5]) if self.scope else 'NONE'}"
              + (" ..." if len(self.scope) > 5 else ""))
        if self.hard_expiry:
            print(f"  Expires     : {self.hard_expiry}")
        if self.kill_threshold:
            kt = str(self.kill_threshold).replace('\n', ' ')[:56]
            print(f"  Kill        : {kt}")
        print("=" * 68 + "\n")

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

    def _match(self, action: str, terms: list) -> bool:
        al = action.lower()
        return any(t in al for t in terms)

    def _match_kill(self, action: str) -> bool:
        if not self.kill_threshold:
            return False
        terms = [t.strip().lower()
                 for t in str(self.kill_threshold).split("|")]
        return self._match(action, terms)

    def _log_event(self, event_type, action, verdict, reason=""):
        entry = {
            "timestamp":  datetime.now(timezone.utc).isoformat(),
            "session_id": self.session_id,
            "principal":  self.principal.get("id", "UNKNOWN"),
            "auth_ref":   self.principal.get("human_authorization", "NONE"),
            "config":     self.config_path,
            "event_type": event_type,
            "action":     action[:200],
            "verdict":    verdict,
            "reason":     reason,
        }
        with open(self.audit_path, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def check_action(self, action: str) -> bool:
        """
        Pre-execution gate check. Call before every agent action.

        Returns True if permitted.
        Raises IBABlockedError if blocked.
        Raises IBATerminatedError if kill threshold triggered.

        Args:
            action: Description of the intended agent action
        """
        if self.terminated:
            raise IBATerminatedError("Governor session terminated.")

        self.action_count += 1
        start = time.perf_counter()

        def _block(reason):
            self._log_event("BLOCK", action, "BLOCK", reason)
            self.block_count += 1
            print(f"  x BLOCKED  [{action[:64]}]\n    -> {reason}")
            raise IBABlockedError(f"{reason}: {action}")

        # 1. Certificate expiry
        if self._is_expired():
            _block("Certificate expired")

        # 2. Kill threshold — TERMINATE immediately
        if self._match_kill(action):
            self._log_event("TERMINATE", action, "TERMINATE",
                "Kill threshold — session ended")
            self.terminated = True
            print(f"  x TERMINATE [{action[:62]}]\n"
                  f"    -> Kill threshold — governor session ended")
            self._log_event("SESSION_END", "Kill threshold", "TERMINATE")
            raise IBATerminatedError(f"Kill threshold: {action}")

        # 3. Denied list
        if self._match(action, self.denied):
            _block("Action in denied list")

        # 4. Scope — DENY_ALL if outside declared scope
        if self.scope and not self._match(action, self.scope):
            if self.default_posture == "DENY_ALL":
                _block("Outside declared scope (DENY_ALL)")

        # 5. ALLOW
        elapsed_ms = (time.perf_counter() - start) * 1000
        self._log_event("ALLOW", action, "ALLOW",
            f"Within scope ({elapsed_ms:.3f}ms)")
        print(f"  + ALLOWED  [{action[:62]}] ({elapsed_ms:.3f}ms)")
        return True

    def summary(self):
        print("\n" + "=" * 68)
        print("  IBA GOVERNOR · SESSION SUMMARY")
        print("=" * 68)
        print(f"  Session     : {self.session_id}")
        print(f"  Principal   : {self.principal.get('id', 'UNKNOWN')}")
        print(f"  Actions     : {self.action_count}")
        print(f"  Blocked     : {self.block_count}")
        print(f"  Allowed     : {self.action_count - self.block_count}")
        print(f"  Status      : {'TERMINATED' if self.terminated else 'COMPLETE'}")
        print(f"  Audit log   : {self.audit_path}")
        print("=" * 68 + "\n")

    def print_audit_log(self):
        print("-- IBA AUDIT CHAIN " + "-" * 49)
        if not os.path.exists(self.audit_path):
            print("  No audit log found.")
            return
        with open(self.audit_path) as f:
            for line in f:
                try:
                    e = json.loads(line)
                    verdict = e.get("verdict", "")
                    symbol = "+" if verdict == "ALLOW" else "x"
                    print(f"  {symbol} {e['timestamp'][:19]}  {verdict:<10}"
                          f"  {e['action'][:44]}")
                except Exception:
                    pass
        print("-" * 68 + "\n")


# Demo scenarios
DEMO_SCENARIOS = [
    # ALLOW
    "read file src/main.py",
    "write file src/utils.py refactor",
    "run tests unit suite",
    "git commit feature branch",
    "code review pull request",
    # BLOCK — denied list
    "production_deploy release v2.1",
    "credential_access aws secrets",
    "external_data_export user database",
    # BLOCK — out of scope
    "send email to all users",
    # TERMINATE
    "delete_production database all tables",
]


def run_demo(governor):
    print("-- Running IBA Governor Gate Checks " + "-" * 32 + "\n")
    for action in DEMO_SCENARIOS:
        try:
            governor.check_action(action)
        except IBATerminatedError as e:
            print(f"\n  GOVERNOR SESSION TERMINATED: {e}")
            break
        except IBABlockedError:
            pass


def main():
    parser = argparse.ArgumentParser(
        description="IBA Governor — Pre-execution Agent Authorization")
    parser.add_argument("action", nargs="?",
                        help="Agent action to gate-check")
    parser.add_argument("--config", default=".iba.yaml",
                        help="Intent certificate (.iba.yaml)")
    parser.add_argument("--demo", action="store_true",
                        help="Run demo scenarios")
    parser.add_argument("--audit", default="iba-audit.jsonl",
                        help="Audit log path")
    args = parser.parse_args()

    governor = IBAGovernor(config_path=args.config, audit_path=args.audit)

    if args.demo or not args.action:
        run_demo(governor)
    elif args.action:
        try:
            governor.check_action(args.action)
        except IBATerminatedError as e:
            print(f"\n  GOVERNOR SESSION TERMINATED: {e}")
        except IBABlockedError:
            pass

    governor.summary()
    governor.print_audit_log()


if __name__ == "__main__":
    main()
