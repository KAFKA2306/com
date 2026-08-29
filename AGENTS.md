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

## Small-context execution contract

Design executable work so an agent with limited context can finish one unit without reading the chat history, a long parent Issue, or unrelated repository history.

### Execution packet

Every executable Issue should contain only the smallest sufficient packet:

1. **Goal** — one observable outcome.
2. **Current truth** — current repository/production state, preferably with exact paths, revisions, or direct evidence.
3. **Next action** — exactly one bounded implementation or verification action.
4. **Allowed scope** — files/surfaces the agent may change; state important non-goals only when needed to prevent a wrong change.
5. **Inputs** — exact file paths, commands, URLs, IDs, or direct predecessor Issue needed for this unit.
6. **Done** — a short checklist of observable completion criteria.
7. **Verify** — canonical tests/CI/runtime/read-back required before completion.
8. **Block/stop** — conditions that require `BLOCKED`/`UNVERIFIED` instead of guessing, fallback, broadening scope, or retrying indefinitely.

### Size and dependency rules

- One agent run handles one executable Issue and one primary outcome.
- Target an executable Issue body of about **3,500 characters or less** and **7 acceptance checks or fewer**. If preserving correctness, safety, or evidence needs more, split the work instead of deleting constraints.
- A child Issue must be executable without reading its parent body. Parent trackers contain only purpose, current state, dependency graph, and child completion state.
- List only direct dependencies. Do not require an agent to recursively read an Issue tree.
- Historical investigation, superseded plans, long logs, and large evidence dumps belong in comments or linked artifacts. Keep the Issue body as the current handoff packet.
- When state changes materially, rewrite the Issue body to the current truth instead of appending another historical section.
- Re-read current code, CI, deployment, or external state before acting. Stale Issue prose never overrides current observable state.
- If two tasks can fail independently or require different tools/environments, they are separate executable Issues.
- If an external setting or human-only action blocks execution, reduce the Issue to that exact blocker and its read-back test; do not retain already-completed implementation steps as open scope.

### Continuation record

At the end of a run, persist only what the next small-context agent needs:

- result: `DONE | BLOCKED | UNVERIFIED`;
- exact revision/state observed;
- files or external state changed;
- validation/read-back result;
- first unresolved blocker, if any;
- next executable Issue or one next action.

Do not use hidden model memory, prior conversation context, or an ever-growing parent Issue as continuation state.

## GitHub write-path portability

- `gh` is optional tooling, never a required execution dependency.
- Missing or unavailable `gh` must not be treated as a blocker when an authenticated GitHub connector or GitHub REST/GraphQL API path is available.
- For repository writes, prefer the connected GitHub capability when available. Otherwise use an authenticated GitHub API client. Use `gh` only as a convenience wrapper when it is already available.
- A missing CLI must not cause implementation work to be downgraded into placeholder Issues, documentation-only work items, or manual instructions when the requested branch, commit, pull request, issue, label, merge, or cleanup operation can be performed through the connector or API.
- Cross-repository or bulk changes must use the same transport-independent sequence: resolve repository and default branch, create an intentional branch, write the change, create the pull request, validate, merge when authorized and gates pass, then remove or otherwise clean up transient work state when supported.
- Repository automation that publishes GitHub Issues or Pull Requests must not silently skip publication merely because `gh` is absent. Implement an authenticated API fallback and fail explicitly only when no authorized GitHub write transport is available.
- Do not add `gh` installation as a product/runtime prerequisite solely to perform GitHub API operations that can be completed through HTTPS APIs.
- Record the actual transport used and the resulting GitHub URLs or identifiers as evidence. Completion is based on GitHub state, not on CLI availability.

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
