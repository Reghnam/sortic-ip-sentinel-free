# Routines — safe stubs only

No live routines ship overnight. Do not add webhooks, mailbox connectors, or scheduled sends.

| Stub | Status | Note |
|------|--------|------|
| Weekly skill backup reminder | **off** | Backup ≠ publish. Do not auto-run. |
| Marketplace publish | **off** | Live publish stays L3 for the owners. |
| Corpus tick | **off** | Ticks stay L0. Corpus is PRIVATE. |
| Partner email / leftover draft send | **off** | Needs recipient **and** action this turn. |

If a tester adds a routine, it is a publish. Decline unnamed.
