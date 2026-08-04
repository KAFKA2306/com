# Completion policy

A task may be reported as complete only when all applicable gates below have passed.

## Required gates

1. **Scope gate** — the implemented change matches the directive and does not silently expand scope.
2. **Repository gate** — the change is in the correct target repository and branch.
3. **Validation gate** — repository-defined lint, tests, schemas, and build checks pass.
4. **Review gate** — the final diff and unresolved review feedback have been inspected.
5. **Integration gate** — the pull request is merged when merge was requested.
6. **Runtime gate** — deployed pages, workflows, APIs, generated assets, or local runtime behavior have been directly verified when in scope.
7. **Evidence gate** — exact references and observed results are attached to the governing work item.
8. **Cleanup gate** — temporary branches and disposable artifacts are removed when requested and safe.

## Truthful partial states

Use `blocked`, `failed`, or `review` instead of `done` when any required gate remains. State which gate is missing and what evidence was obtained. Do not convert configuration existence, a queued run, a green unrelated check, or an expected deployment into a success claim.

## Domain-specific examples

- A web UI change requires responsive, keyboard, contrast, and deployed-page checks when those were acceptance criteria.
- A financial analysis requires primary-source provenance and reconciliation, not only successful rendering.
- A Blender or Unity asset requires visual evidence and the explicitly available runtime gates.
- A recurring service requires at least one observed execution before being described as operational, unless the directive explicitly limits scope to disabled installation.
