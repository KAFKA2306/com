# Evidence manifest producer

`python scripts/build_evidence_manifest.py SOURCE --output MANIFEST` converts declared required checks and observed results into the canonical evidence-gate manifest. Missing observations become `UNVERIFIED`; they are never treated as success. The generated manifest is evaluated by `scripts/validate_evidence_gate.py`.
