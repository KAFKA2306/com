# Repository boundary policy

## `com`

Store portfolio-level intent, governance, registries, cross-repository dependencies, recurring-service contracts, incidents, decisions, and completion evidence.

Do not store product implementation, canonical product datasets, generated media, or runtime queues.

## Domain repositories

Store product code, tests, schemas, product-specific data, assets, releases, and deployment configuration. A domain repository may reference a `com` directive but must remain independently buildable and understandable.

## Shared-resource repositories

Store reusable libraries, design systems, skills, or adapters only when reuse is their explicit product responsibility. They must not become implicit control planes.

## Executors

GitHub Actions, local runners, scheduled ChatGPT tasks, and other schedulers execute bounded work. Their internal state is operational data, not portfolio truth. Durable intent and outcomes return to GitHub work items.

## Duplication rules

Registry metadata may repeat a repository's identifier, role, public URL, visibility class, and capabilities. It must not duplicate the target repository's canonical business data or detailed architecture. Link to the target source instead.
