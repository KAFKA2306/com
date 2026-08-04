# KAFKA COM

`KAFKA2306/com` is the command repository for work that spans the KAFKA2306 GitHub portfolio.

ChatGPT is the primary interaction surface. This repository is the durable, reviewable source of truth for directives, policies, repository boundaries, recurring services, decisions, incidents, and completion evidence. Product code and product data remain in their domain repositories.

## Operating model

```text
User instruction in ChatGPT
        |
        v
com directive / service / decision / incident
        |
        v
target repository issue, branch, pull request, workflow, or local execution
        |
        v
verification evidence recorded against the com work item
        |
        v
completion only after all acceptance gates pass
```

Chat conversations are not canonical state. A material instruction must be reduced to an auditable GitHub work item before it is treated as durable work.

## Responsibilities

`com` owns:

- portfolio-wide directives and acceptance criteria;
- repository and service registries;
- evidence, security, completion, and destructive-action policies;
- cross-repository dependencies and decisions;
- recurring-service definitions and incident records;
- machine-readable validation of the control-plane contract.

Domain repositories own:

- implementation code and tests;
- product-specific data and assets;
- branches, pull requests, releases, and deployed pages;
- repository-local architecture and operating instructions.

Executors such as GitHub Actions, local runners, and schedulers are replaceable execution mechanisms. They are not the source of truth.

## Work-item types

Use the issue forms under `.github/ISSUE_TEMPLATE/`:

- **Directive** — a bounded change or investigation with acceptance criteria;
- **Recurring service** — a repeated or condition-based responsibility;
- **Incident** — a failed run, broken deployment, incorrect result, or control failure;
- **Decision** — an architectural or governance choice with alternatives and consequences.

## Repository layout

```text
.github/             Issue forms and validation workflow
policies/            Mandatory portfolio-wide rules
instructions/        ChatGPT-facing operating procedures
registry/            Machine-readable repositories, services, schedules, capabilities
schemas/             Registry contracts
scripts/             Deterministic validators
playbooks/           Repeatable operating procedures
docs/adr/            Architectural decision records
tests/               Control-plane tests
```

## Validation

The repository intentionally uses only the Python standard library for its control-plane checks.

```bash
python scripts/validate_control_plane.py
python -m unittest discover -s tests -v
```

CI runs the same commands on every push and pull request.

## Security boundary

Do not commit credentials, authentication material, private conversation transcripts, personal data, local absolute paths, unpublished financial positions, or unredacted executor logs. Record the minimum durable decision, acceptance criteria, and evidence references required to reproduce the conclusion.

See [SECURITY.md](SECURITY.md), [GOVERNANCE.md](GOVERNANCE.md), and [AGENTS.md](AGENTS.md).
