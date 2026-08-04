# Work-item state semantics

GitHub issue labels may represent these states after the label set is provisioned. Until then, include the current state explicitly in the issue body or latest status comment.

| State | Meaning | Exit condition |
| --- | --- | --- |
| inbox | Captured but incomplete | Scope and acceptance contract become executable |
| ready | Executable and permitted | An executor starts bounded work |
| running | Active implementation or investigation | Evidence is ready for review, or work blocks/fails |
| review | Implementation exists and gates are being checked | All gates pass, or fixes are required |
| blocked | External dependency prevents progress | Dependency resolves or work is cancelled |
| failed | Execution ended without satisfying the contract | A retry or corrective directive starts |
| done | Every applicable acceptance gate has evidence | Reopen only with new contrary evidence |
| cancelled | Intentionally stopped | New directive required to resume |

Only one state is active. Timing, risk, executor, repository, and priority are separate dimensions and must not be encoded as lifecycle states.
