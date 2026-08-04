# Destructive-action policy

A destructive action is any operation that irreversibly deletes, rewrites, publishes, spends, exposes, or mutates external state beyond ordinary version-controlled development.

## Explicit authorization required

- deleting or transferring a repository;
- changing repository visibility;
- rewriting published Git history;
- deleting production data or releases;
- rotating credentials or changing account access;
- purchasing paid services or materially increasing spend;
- sending external communications with legal, financial, employment, or privacy consequences;
- merging a destructive migration without a tested rollback.

## Required contract

Record:

- target and exact operation;
- reason and expected benefit;
- affected systems and data;
- backup or rollback plan;
- verification method;
- authorization reference;
- post-action audit result.

Prefer reversible alternatives: archive before delete, branch before rewrite, dry-run before mutation, staged rollout before broad deployment, and read-only audit before repair.
