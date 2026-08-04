# Status model

Lifecycle state is separate from execution and evidence state.

- Lifecycle: inbox, ready, running, review, blocked, failed, done, cancelled.
- Execution: not requested, queued, active, ended.
- Integration: uncommitted, committed, pull request open, merged, released, deployed.
- Evidence: missing, partial, sufficient, contradicted.

A work item may be `review` while its pull request is merged because runtime evidence is still missing. A scheduled execution may be `queued` while the service remains active. Keep these dimensions distinct to prevent false completion reports.
