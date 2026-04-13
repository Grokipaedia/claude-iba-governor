# iba-governor

**Full production governance for any agent.**

Thin IBA layer that adds cryptographic intent binding on top of any memory plugin or agent framework.

One-command install. Zero new dependencies. <5 ms overhead.

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
