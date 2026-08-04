# Repository-boundary examples

| Concern | Canonical location |
| --- | --- |
| Portfolio-wide acceptance criteria | `com` directive |
| Cross-repository dependency | `com` parent issue |
| Product implementation | Target repository |
| Product dataset | Target repository |
| Shared agent skill distribution | `agent-resources` |
| Prompt product assets and data | `prompt-vault` |
| Workflow run logs | Executor platform, referenced from the issue |
| Local process state | Local runtime, never Git |
| Completion decision and evidence index | Governing `com` work item |

The purpose of `com` is not to mirror every project. It stores enough control metadata to locate, coordinate, and verify the actual canonical sources.
