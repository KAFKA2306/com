# Registry rules

Registries contain control metadata only. They must remain small, reviewable, and machine validated.

## Repository entries

Add a repository only after confirming its current identifier and responsibility. Use `review-required` when visibility has not been verified. A canonical domain may belong to only one repository.

## Service entries

Add a service only after creating a recurring-service issue. Its target repositories and executor must already exist in their registries. Do not register a historical automation merely because configuration files exist.

## Schedule entries

A schedule references a registered service. An active schedule requires an active service. Record an IANA timezone and a human-readable trigger. Execution-engine-specific IDs belong in the service work item or target repository, not here, unless required for recovery.

## Capability entries

Capabilities describe executor classes and their restrictions. They are not credentials and do not grant permission by themselves.
