# Scripts

`validate_control_plane.py` checks required files, JSON syntax, repository ownership, executor registration, recurring-service references, schedule activation, and Issue Form contract markers using only the Python standard library.

`validate_evidence_gate.py <manifest.json>` evaluates one exact revision as `PASS`, `FAIL`, or `UNVERIFIED`. Exit codes are `0`, `1`, and `2` respectively. Any explicit `FAIL` fails the gate. Every required check and acceptance criterion must be `PASS` and carry at least one evidence reference, otherwise the gate is `UNVERIFIED`.

Keep scripts deterministic, non-networked, and free of secrets. Discovery of current external state belongs in connected-tool workflows, not in these validators.
