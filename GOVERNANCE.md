# Governance

## Purpose

`com` supplies one auditable management layer for the KAFKA2306 repository portfolio while allowing each product repository to remain autonomous in implementation.

## Sources of authority

In descending order:

1. the user's latest explicit instruction;
2. repository-specific legal, security, and release constraints;
3. an accepted decision record in `com`;
4. the active directive or recurring-service contract;
5. portfolio policies in this repository;
6. executor defaults.

A lower source may not silently override a higher source.

## Work-item lifecycle

Use these logical states even when labels are not yet available:

- `inbox` — captured but not sufficiently specified;
- `ready` — target, scope, permissions, and acceptance criteria are executable;
- `running` — an executor is actively working;
- `review` — implementation exists and evidence is being checked;
- `blocked` — an external dependency prevents progress;
- `failed` — an attempted execution ended without satisfying the contract;
- `done` — every acceptance criterion has evidence;
- `cancelled` — intentionally stopped with a reason.

Only one lifecycle state may be active at a time.

## Completion

A work item is complete only when:

- the intended repository state exists;
- required tests and checks pass;
- requested merge or publication is complete;
- runtime evidence has been inspected when runtime behavior is in scope;
- unresolved limitations are stated;
- the work item links the final evidence.

Configuration, intent, or a pending workflow does not constitute completion.

## Cross-repository work

Create one parent directive in `com`. Create target-repository issues or pull requests only where implementation belongs. The parent must retain the dependency graph, shared acceptance criteria, and portfolio-level completion decision.

## Recurring work

A recurring service records purpose, cadence or condition, evidence policy, executor class, failure handling, and stop conditions. Normal runs should append compact evidence to the service record. Material failures create incidents. Code changes remain in target repositories.

## Decisions

Use a decision issue or ADR when a choice changes repository boundaries, data ownership, security posture, executor architecture, public interfaces, or completion policy. Record alternatives and consequences rather than only the selected implementation.
