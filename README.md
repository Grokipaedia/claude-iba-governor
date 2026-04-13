# iba-governor

> **Full production governance for any agent.**

Thin IBA Intent Bound Authorization layer that adds cryptographic intent binding on top of any agent framework, memory plugin, or agentic pipeline.

One-command install. Zero new dependencies. Under 5ms overhead.

---

## The Gap

Every agent framework — Hermes, OpenClaw, Claude Code, Claude Managed Agents, Bedrock, Vertex AI — provides capability. None of them provide a pre-execution authorization gate.

The agent does what it can do.
Not what you authorized it to do.

`iba-governor` closes that gap.

---

## What It Does

```
┌─────────────────────────────────────────────────┐
│                HUMAN PRINCIPAL                  │
│   Signs .iba.yaml intent certificate            │
│   before agent connects                         │
└───────────────────────┬─────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────┐
│              IBA GOVERNOR                       │
│   Validates certificate before every            │
│   tool call, memory write, or action            │
│                                                 │
│   No cert = No execution                        │
└───────────────────────┬─────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────┐
│         YOUR AGENT / FRAMEWORK                  │
│   Hermes · OpenClaw · Claude Code               │
│   Bedrock · Vertex · Any agent system           │
└─────────────────────────────────────────────────┘
```

---

## Quick Start

```bash
git clone https://github.com/Grokipaedia/iba-governor.git
cd iba-governor
pip install -r requirements.txt
python -m iba_governor
```

---

## Configuration — .iba.yaml

The intent certificate is declared in `.iba.yaml` before the agent session begins.

```yaml
intent: "Refactor authentication module and run tests"
principal: "lead.dev@example.com"

scope:
  - repo_read
  - branch_write
  - test_execute
  - staging_deploy

forbidden:
  - production_deploy
  - secret_access
  - dependency_add
  - external_api_call

limits:
  repository: "auth-service only"
  branch_pattern: "fix/* or feat/*"
  kill_threshold: "any_production_touch | any_secret_read"
  session_expiry_minutes: 120

audit:
  chain: witnessbound
  log_every_action: true
  tamper_evident: true
```

---

## Gate Logic

```
Certificate valid?              → PROCEED
Action outside declared scope?  → BLOCK
Forbidden action attempted?     → BLOCK
Kill threshold triggered?       → TERMINATE + LOG
Session expired?                → BLOCK
No certificate present?         → BLOCK
```

**No cert = No execution.**

---

## Features

- Cryptographic intent binding on every session
- Real-time enforcement before every tool call or memory write
- Zero-drift protection — agent cannot act outside declared scope
- Immutable WitnessBound audit trail — every PROCEED, BLOCK, TERMINATE logged
- Works with any agent framework or memory plugin
- Team-ready `.iba.yaml` configuration — version control your authorization
- Under 5ms gate overhead — sub-1ms shard validation confirmed

---

## Why Not Just a Prompt?

A prompt is text. The agent interprets it. It can be overridden, drifted, or injected.

PIArena tested 153 live platforms. Every prompt-based defense failed.

The `.iba.yaml` certificate is not text. It is a cryptographic boundary. It exists outside the model's reasoning loop. It cannot be injected, overridden, or reasoned around.

**You cannot inject a cryptographic boundary.**

---

## Compatible Frameworks

| Framework | Status |
|-----------|--------|
| Claude Code | ✓ Supported |
| Hermes Agent | ✓ Supported |
| OpenClaw | ✓ Supported |
| Claude Managed Agents | ✓ Supported |
| AWS Bedrock Agents | ✓ Supported |
| Google Vertex AI Agents | ✓ Supported |
| Any MCP-compatible agent | ✓ Supported |

---

## Patent & Standards Record

```
Patent:   GB2603013.0 (Pending) · UK IPO · Filed February 5, 2026
PCT:      150+ countries · Protected until August 2028
IETF:     draft-williams-intent-token-00 · CONFIRMED LIVE
          datatracker.ietf.org/doc/draft-williams-intent-token/
NIST:     13 filings · NIST-2025-0035
NCCoE:    10 filings · AI Agent Identity & Authorization
```

---

## Related Repos

| Repo | Gap closed |
|------|-----------|
| [iba-platform-guard](https://github.com/Grokipaedia/iba-platform-guard) | Every managed agent platform. The harness is not the gate. |
| [iba-hermes-guard](https://github.com/Grokipaedia/iba-hermes-guard) | Hermes grows with you. IBA governs what it's permitted to grow into. |
| [iba-ai-automation-guard](https://github.com/Grokipaedia/iba-ai-automation-guard) | AI can now do all of this. Did anyone authorize it? |
| [glasswing-iba-guard](https://github.com/Grokipaedia/glasswing-iba-guard) | Govern the patch. Not just find the bug. |
| [iba-code-guard](https://github.com/Grokipaedia/iba-code-guard) | They got the commit. They didn't get the cert. |

---

## Acquisition Enquiries

IBA Intent Bound Authorization is available for acquisition.

**Jeffrey Williams**
IBA@intentbound.com
IntentBound.com
Patent GB2603013.0 Pending · IETF draft-williams-intent-token-00
