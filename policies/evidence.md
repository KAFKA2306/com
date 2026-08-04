# Evidence policy

## Evidence classes

Use the strongest available evidence for each claim:

1. **Primary external source** — official filing, release, documentation, standard, dataset, or organization publication.
2. **Connected repository source** — exact file lines, issue, pull request, commit, workflow run, release, or deployment reference.
3. **Observed runtime evidence** — direct page inspection, API response, generated artifact, test output, or local runtime result.
4. **Derived analysis** — calculations or inferences whose inputs and method are recorded.

Secondary summaries may orient research but do not replace available primary evidence.

## Required recording

For material conclusions, record:

- exact source URL or connected-source reference;
- source date or commit SHA;
- observation date when freshness matters;
- relevant value, status, or result;
- derivation method for calculated values;
- limitations and unresolved conflicts.

## Claim discipline

- Do not retain a number, date, version, specification, or status that cannot be verified.
- Separate actuals, forecasts, estimates, simulations, and assumptions.
- Separate a successful implementation check from a successful runtime or business outcome.
- Reverify facts likely to change before publishing or acting on them.
- When sources disagree, preserve the disagreement and identify which source controls the decision.

## Compact evidence

Do not paste full logs or long documents. Store a concise result and a stable reference. Attach an artifact only when the reference cannot preserve the evidence and the artifact contains no restricted data.
