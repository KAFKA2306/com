# Agent operating contract

This repository is the portfolio command repository. Apply these rules to ChatGPT and any other executor acting on KAFKA2306 work.

## Canonical state

1. Treat the user's current instruction as intent, not durable state.
2. For material work, create or update a `com` work item before claiming that the instruction is scheduled, delegated, blocked, or complete.
3. Keep implementation details in the target repository. Keep cross-repository intent, acceptance gates, dependencies, and evidence links in `com`.
4. Do not use a chat transcript, local queue directory, scheduler database, or model-specific memory as the source of truth.

## Default workflow

1. Resolve the target repository and current public or connected-source state.
2. Classify the work as a directive, recurring service, incident, or decision.
3. Write explicit scope, non-goals, permissions, acceptance criteria, and required evidence.
4. Perform implementation in the target repository through an intentional branch and pull request unless a read-only operation is sufficient.
5. Validate the result with the repository's tests, CI, deployment checks, and domain-specific evidence.
6. Record exact repository, issue, pull request, commit, workflow, deployment, and primary-source references.
7. Mark work complete only when every acceptance criterion is demonstrably satisfied.

## ChatGPT-first behavior

- ChatGPT is the normal interaction and orchestration surface.
- Convert natural-language requests into structured GitHub work items without asking the user to perform machine-executable bookkeeping.
- Use connected GitHub data for current repository state.
- Use current primary web sources for facts that may have changed.
- Prefer direct execution over instructing the user to copy commands, create files, or move issues when the connected tools can do it.
- Report partial completion truthfully. Never infer a successful merge, deployment, schedule, or runtime result from configuration alone.

## Evidence rules

- Every externally verifiable claim requires a supporting primary URL or connected-source reference.
- A pull request URL is not evidence that its runtime behavior works.
- A passing unit test is not evidence of a successful deployment.
- A deployed page URL is not evidence that its data is correct.
- Preserve exact dates, versions, numbers, and commit identifiers.

## Permission boundary

Permitted by default when required by the user's instruction:

- read repository content, issues, pull requests, actions, and deployments;
- create issues, branches, commits, pull requests, and non-destructive documentation;
- run repository-defined validation;
- merge and remove a work branch after all stated gates pass when the user requested end-to-end completion.

Require explicit user authorization recorded in the work item for:

- repository deletion or visibility changes;
- secret rotation or credential access;
- destructive data migration;
- production actions with financial, legal, privacy, or irreversible external effects;
- paid service purchase or materially increased spending.

## Repository boundary

Do not move product code into `com`. Do not duplicate a domain repository's canonical data in `com`. Registry entries may contain identifiers, roles, public URLs, capabilities, and control metadata only.
