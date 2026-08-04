# Tests

Run:

```bash
python scripts/validate_control_plane.py
python -m unittest discover -s tests -v
```

Tests cover the repository's current valid state and key invariants such as a single command repository, unique canonical domains, and schedule-to-service activation consistency.
