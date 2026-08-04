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

## Image retention rules

- Treat user-requested images, adopted design assets, published images, comparison images, and render/review evidence as durable assets.
- Classify image assets as `KEEP`, `ARCHIVE`, or `DISCARD`. `KEEP` and `ARCHIVE` assets must not be deleted, overwritten, or silently replaced.
- When a new image supersedes an older image, preserve the older image at a stable repository path and record the relationship in a manifest or work item. Git history alone is not an acceptable archive.
- Never remove an image merely because it is unused by the current page, pipeline, or build.
- Deletion is permitted only for an asset explicitly classified as `DISCARD`, with the exact path and reason recorded, and with the user's explicit approval when the image was requested, selected, published, or used as evidence.
- Preserve original-resolution files when available. Derivative WebP, thumbnail, cropped, compressed, or annotated variants do not replace the original.
- Follow `docs/image-retention-policy.md` for repository-level implementation.

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
