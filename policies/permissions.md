# Permission model

Classify the highest operation required by each work item:

1. **Read-only** — inspect public or connected data and produce analysis.
2. **Repository write** — create or modify version-controlled files, issues, branches, and pull requests.
3. **Publish or deploy** — merge, release, deploy, send a routine notification, or modify an external public surface.
4. **Destructive or consequential** — irreversible deletion, history rewrite, visibility change, credential action, spending, or external legal, financial, privacy, or employment effect.

The active directive must permit the highest class used. Executor capability does not imply user authorization. Apply least privilege and keep credentials scoped to the target operation.
