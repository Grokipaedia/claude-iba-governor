# iba-governor

**Full production governance for any agent.**

Thin IBA layer that adds cryptographic intent binding on top of any memory plugin or agent framework.

One-command install. Zero new dependencies. <5 ms overhead.

## Patent & Filings
- **Patent Pending**: GB2603013.0 (filed 5 Feb 2026, PCT route open — 150+ countries)
- **NIST Docket**: NIST-2025-0035 (13 IBA filings)
- **NCCoE Filings**: 10 submissions on AI agent authorization

## Features
- Cryptographic intent binding on every session
- Real-time enforcement before tool calls or memory writes
- Zero-drift protection + immutable audit trail
- Works with any memory plugin or agent system
- Team-ready configuration (.iba.yaml)

## Quick Start
```bash
git clone https://github.com/Grokipaedia/iba-governor.git
cd iba-governor
pip install -r requirements.txt
# Run inside your agent environment
python -m iba_governor
