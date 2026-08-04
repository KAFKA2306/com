# Scripts

`validate_control_plane.py` checks required files, JSON syntax, repository ownership, executor registration, recurring-service references, schedule activation, and Issue Form contract markers using only the Python standard library.

Keep scripts deterministic, non-networked, and free of secrets. Discovery of current external state belongs in connected-tool workflows, not in this validator.
