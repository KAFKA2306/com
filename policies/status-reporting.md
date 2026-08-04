# Status-reporting policy

Status reports must describe observed state rather than anticipated state.

Use these terms precisely:

- **defined** — a contract or configuration exists;
- **queued** — an execution request was accepted but has not started;
- **running** — execution is currently active;
- **validated** — named checks completed successfully;
- **merged** — the pull request was merged and the merge commit exists;
- **deployed** — the deployment system reports success for the intended revision;
- **observed operational** — the requested runtime behavior was directly inspected;
- **complete** — every applicable acceptance gate has evidence.

Do not collapse these states into “done.” Include exact dates, commit identifiers, URLs, and remaining gates. A configuration-only implementation must be labelled as such.
