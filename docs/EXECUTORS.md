# Executor selection

Select the executor for the operation being performed:

| Executor | Appropriate work | Not canonical for |
| --- | --- | --- |
| ChatGPT | research, connected-source inspection, coordination, review, evidence synthesis, scheduled monitoring | durable task state without a GitHub work item |
| GitHub Actions | deterministic tests, builds, releases, lightweight repository schedules | portfolio decisions or cross-repository truth |
| Local runtime | GPU, Blender, desktop applications, private local files, machine integrations | durable portfolio state or unredacted evidence storage |

Do not bind a project permanently to one executor. A single directive may route different bounded steps to different executors while retaining one governing work item.
