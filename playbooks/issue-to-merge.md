# Issue-to-merge playbook

1. Read the governing `com` directive and the target repository instructions.
2. Verify the target's current default branch, open work, CI, and deployment state.
3. Create or reuse a target-repository issue when implementation discussion belongs there.
4. Create an intentional work branch.
5. Implement only the accepted scope.
6. Run repository-defined validation and inspect the diff.
7. Open a pull request linking the `com` directive.
8. Resolve review findings and rerun affected checks.
9. Merge only after required checks and evidence pass.
10. Verify deployment or runtime behavior when in scope.
11. Record the final PR, merge commit, runtime evidence, limitations, and cleanup status in the governing work item.
12. Remove the work branch when requested and supported.

A green pull request is not sufficient when publication, runtime behavior, data correctness, or visual quality is part of the acceptance criteria.
