# ADR 0001: Use `com` as a ChatGPT-first command repository

- Status: Accepted
- Date: 2026-08-04

## Context

Most portfolio management, research direction, implementation instructions, reviews, and completion decisions originate through ChatGPT conversations. A scheduler-first design would invert the actual control flow and make operational queue state appear more authoritative than the user's decisions and repository evidence.

The existing `com` repository contained an unrelated static report and had no active management contract. Its previous main state was preserved at `archive/pre-kafka-com-20260804` before replacement.

## Decision

Use `KAFKA2306/com` as the durable command repository for the portfolio.

- ChatGPT is the primary interaction and orchestration surface.
- GitHub issues are the durable work-item surface.
- Registries and policies in `com` define portfolio boundaries and control metadata.
- Domain implementation remains in domain repositories.
- GitHub Actions, local runtimes, and scheduled tasks are replaceable executors.
- Executor state is not canonical and must return durable outcomes to GitHub.
- The initial service and schedule registries start empty; existing automation is not silently adopted without a defined contract and observed evidence.

## Alternatives considered

### New dedicated operations repository

Rejected because `com` already existed without a continuing product responsibility, and another repository would add naming and discovery overhead without improving the boundary.

### Product repository as control plane

Rejected because it would mix portfolio governance with product code, data, release concerns, and product-specific permissions.

### Scheduler or local queue as source of truth

Rejected because it does not capture the user's evolving decisions, cross-repository evidence, or review state and is difficult for ChatGPT to inspect consistently.

### Chat history as source of truth

Rejected because conversation state is not a sufficiently durable, diffable, auditable, or machine-validated contract.

## Consequences

- Material work requires a structured GitHub work item.
- ChatGPT must update durable state instead of merely reporting conversational intent.
- Cross-repository completion becomes evidence-gated.
- The repository must remain free of secrets and raw conversation archives.
- Existing recurring work requires explicit migration into service contracts rather than implicit inheritance.
