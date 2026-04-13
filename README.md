# claude-iba-governor

**Full production governance for Claude Code.**

Thin IBA layer on top of claude-mem (or any memory plugin).

One-command install. Zero new dependencies. <5 ms overhead. Preserves 95%+ token savings.

## Features
- Cryptographic intent binding on every session
- Real-time enforcement before tool calls / memory writes
- Zero-drift protection + audit trail
- Works with claude-mem, claude-brain, etc.
- Team-ready (.iba.yaml config)

## Quick Install (inside any Claude Code session)
```bash
/plugin marketplace add Grokipaedia/claude-iba-governor
/plugin install claude-iba-governor
