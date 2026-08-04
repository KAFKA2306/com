# Contributing

Use an Issue Form to establish the governing work contract before making material portfolio changes.

Implementation pull requests should:

- link the governing directive, service, incident, or decision;
- change only control-plane metadata, policy, validation, or documentation that belongs in `com`;
- keep domain code and canonical product data in the target repository;
- include deterministic validation and exact evidence;
- avoid secrets, private transcripts, local runtime state, and raw logs;
- state remaining limitations and cleanup status.

Run the standard-library validator and unit tests before merge.
