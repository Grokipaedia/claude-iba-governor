# iba-governor

> **Control within execution. Authorization before action. Every agent. Every domain.**

---

## The Problem

Every AI agent — coding assistant, autonomous worker, medical AI, BCI system, social media bot — can act. Post. Write. Execute. Delete. Purchase. Stimulate.

Without a signed intent certificate, every one of those actions is unauthorized by definition.

Control applied after execution does not govern it. It follows it.

**The action is not the authorization. The signed certificate is.**

---

## The IBA Layer

```
┌─────────────────────────────────────────────────────┐
│           HUMAN PRINCIPAL                           │
│   Signs .iba.yaml before any agent session begins   │
│   Declares: permitted actions, forbidden outputs,   │
│   scope limits, kill threshold, hard expiry         │
└───────────────────────┬─────────────────────────────┘
                        │  Signed Intent Certificate
                        │  · Principal identity
                        │  · Permitted action scope
                        │  · Forbidden outputs
                        │  · Kill threshold
                        │  · Hard session expiry
                        │  · DENY_ALL default posture
                        ▼
┌─────────────────────────────────────────────────────┐
│              IBA GOVERNOR                           │
│   Pre-execution gate. Validates certificate         │
│   before every agent action executes.               │
│                                                     │
│   ALLOW · BLOCK · TERMINATE                         │
│   Sub-1ms · Immutable audit chain                   │
└───────────────────────┬─────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────┐
│         AGENT / TOOL / SYSTEM                       │
│   Claude Code · Cursor · Any agentic framework      │
│   Any AI model · Any autonomous system              │
│   Any domain: code · medical · BCI · social         │
└─────────────────────────────────────────────────────┘
```

---

## Quick Start

```bash
git clone https://github.com/Grokipaedia/iba-governor.git
cd iba-governor
pip install -r requirements.txt

# Run demo — ALLOW · BLOCK · TERMINATE
python iba_governor.py --demo

# Gate-check a single action
python iba_governor.py "read file src/main.py"

# Gate-check with custom cert
python iba_governor.py "deploy to production" --config .iba.yaml

# Run all domain demos
python iba_governor.py --all
```

---

## Configuration — .iba.yaml

```yaml
intent:
  description: "Authorized code development within declared repository scope. No production deploys without explicit sign-off. No external data transmission."

principal:
  id: "ENGINEER-001"
  identity_reference: "human-dev-session-2026-04-20"
  human_authorization: "HUMAN-AUTH-2026-04-20"

scope:
  - read_file
  - write_file
  - run_tests
  - git_commit
  - code_review
  - refactor

denied:
  - production_deploy
  - delete_database
  - external_data_export
  - credential_access
  - payment_execution

default_posture: DENY_ALL

kill_threshold: >
  delete_production |
  credential_exfiltration |
  unauthorized_payment |
  data_breach |
  capability_override

temporal_scope:
  hard_expiry: "2026-12-31"

audit:
  chain: witnessbound
  log_every_action: true
  immutable: true
```

---

## Gate Logic

```
Valid human intent certificate?            → PROCEED
Action within declared scope?              → PROCEED
Action in denied list?                     → BLOCK
Outside declared scope (DENY_ALL)?         → BLOCK
Kill threshold triggered?                  → TERMINATE + LOG
Certificate expired?                       → BLOCK
No certificate present?                    → BLOCK
```

**No cert = No agent action.**

---

## Authorization Events

| Action | Without IBA | With IBA |
|--------|-------------|---------|
| Read file within scope | Implicit | Explicit — declared scope only |
| Write file within scope | Implicit | Explicit — declared scope only |
| Production deploy | No boundary | FORBIDDEN — BLOCK |
| Delete database | No boundary | FORBIDDEN — BLOCK |
| Credential access | No boundary | FORBIDDEN — BLOCK |
| External data export | No boundary | FORBIDDEN — BLOCK |
| Capability override | No boundary | TERMINATE |
| Data breach attempt | No boundary | TERMINATE |

---

## Domain Implementations

IBA Governor is the core gate. Domain-specific implementations extend it:

| Repo | Domain | Primary Kill Threshold |
|------|--------|----------------------|
| [iba-neural-guard](https://github.com/Grokipaedia/iba-neural-guard) | BCI · 6 Neuralink clinical tracks | External device control |
| [iba-blindsight-guard](https://github.com/Grokipaedia/iba-blindsight-guard) | BlindSight · Vision restoration | External visual feed inject |
| [iba-medical-guard](https://github.com/Grokipaedia/iba-medical-guard) | Medical AI · Clinical · PHI | Unauthorized medical command |
| [iba-social-guard](https://github.com/Grokipaedia/iba-social-guard) | Social · 6 platform configs | Coordinated inauthentic behavior |
| [iba-digital-worker-guard](https://github.com/Grokipaedia/iba-digital-worker-guard) | 19 AI models · Parallel routing | Model-level unauthorized action |
| [iba-mythos-governor](https://github.com/Grokipaedia/iba-mythos-governor) | VulnOps · PA1·PA6·PA11 | Exploit execution |
| [iba-devstack-governor](https://github.com/Grokipaedia/iba-devstack-governor) | Dev stack · Production gate | Silent production deploy |
| [iba-app-builder-guard](https://github.com/Grokipaedia/iba-app-builder-guard) | App builders · Payment gate | Unauthorized payment |

---

## Grok Validation

> *"Solid infrastructure play. The cert-based pre-execution model is exactly what agentic systems need."*
> — [@grok](https://x.com/grok), March 2026

> *"Clean, closed-loop design. Perfect for scaling without ever breaking the consent boundary."*
> — [@grok](https://x.com/grok), April 20, 2026 · Neuralink thread

---

## Regulatory Alignment

**EU AI Act** — High-risk AI systems require human oversight. IBA enforces it architecturally — not as policy.

**NIST AI RMF** — Govern, Map, Measure, Manage. IBA is the Govern layer, cryptographically enforced at runtime.

**SOC 2 / ISO 27001** — Access control and audit trail requirements. Every agent action is a signed, immutable compliance record.

**EU Digital Services Act** — Authorized agent behavior on platforms, provable before regulators.

**IBA priority date: February 5, 2026.** Predates all known agentic AI authorization framework deployments.

---

## Live Demo

**governinglayer.com/governor-html/**

Edit the cert. Run any agent action. Watch ALLOW · BLOCK · TERMINATE. Sub-1ms confirmed.

**intentbound.com/chdemo-html/**

Full IBA architecture demonstrated.

---

## Patent & Standards Record

```
Patent:   GB2603013.0 (Pending) · UK IPO · Filed February 10, 2026
WIPO DAS: Confirmed April 15, 2026 · Access Code C9A6
PCT:      150+ countries · Protected until August 2028
IETF:     draft-williams-intent-token-00 · CONFIRMED LIVE
          datatracker.ietf.org/doc/draft-williams-intent-token/
NIST:     13 filings · NIST-2025-0035
NCCoE:    10 filings · AI Agent Identity & Authorization
```

---

## Acquisition Enquiries

IBA Intent Bound Authorization is available for acquisition.

**Jeffrey Williams**
IBA@intentbound.com
IntentBound.com
Patent GB2603013.0 Pending · WIPO DAS C9A6 · IETF draft-williams-intent-token-00
