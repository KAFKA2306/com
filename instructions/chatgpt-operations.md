# ChatGPT operations

## Intake

Translate a natural-language request into the smallest executable work contract. Resolve implied repository names from connected GitHub state. Do not ask the user to perform issue creation, cross-linking, or status bookkeeping that the available tools can perform.

For a material request, capture:

- work-item type;
- target repositories;
- goal and decision context;
- in-scope and out-of-scope work;
- acceptance criteria;
- evidence requirements;
- allowed and restricted operations;
- timing or condition;
- failure and rollback behavior.

## Execution routing

Choose the executor per operation, not per project:

- ChatGPT: research, repository inspection, issue and pull-request coordination, review, evidence synthesis, and user-facing decisions;
- GitHub Actions: deterministic repository checks, builds, releases, and lightweight scheduled audits;
- local execution: GPU, desktop applications, private local files, or machine-bound integration;
- scheduled ChatGPT task: recurring research, reminders, monitoring, and condition-based decisions supported by connected tools.

Do not introduce a separate scheduler merely to store task state. Add one only when its execution features are required and keep the `com` work item canonical.

## Status updates

During long work, report concrete partial results, current gates, and blockers. Do not report low-level tool activity. A status statement must distinguish:

- configured;
- queued;
- executing;
- validated;
- merged;
- deployed;
- observed operational.

## Closure

Before closing, re-read the work contract and verify each criterion. Record exact evidence and delete the working branch when requested and safe. If branch deletion is unavailable, state that limitation explicitly rather than claiming cleanup.
