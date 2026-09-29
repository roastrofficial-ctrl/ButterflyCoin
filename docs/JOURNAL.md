BF¢-I Experimental Journal

HYPOTHESIS

A monetary universe represented as fixed proportions of a single immutable whole U=1 may produce qualitatively different economic behaviour than conventional fixed-supply currencies. Specifically, ownership-as-relationship might affect valuation, growth representation, and dynamics when goods and productivity change.

EXPERIMENT 1 — Transfer semantics

EXPERIMENT
- Implemented `transfer_absolute` and `transfer_fraction_of_holder` and tested simple transfers, overdraw attempts, and replay.

OBSERVATION
- Both transfer semantics are necessary. Absolute transfers move a fixed share; fraction transfers scale with current holding and are non-linear over sequences.

FAILURE / SURPRISE
- None critical; both primitives coherent.

WHAT THIS FORCES US TO BELIEVE
- Distinguishing transfer semantics is essential to representing economic intent (fixed proportion vs relative rebalancing).

NEXT QUESTION
- How do sequences of fractional transfers affect long-term concentration?


EXPERIMENT 2 — Replay and identity

EXPERIMENT
- Recorded identical payloads twice; ledger creates unique event IDs by appending a counter when hashcollides.
- Performed identity split by ledger event and reassigning holdings.

OBSERVATION
- Replay requires external nonce or signature to be unambiguously identified as duplicate or genuine repaid transaction.
- Identity operations can be simulated but economic meaning depends on off-chain rules.

FAILURE / SURPRISE
- None; indicates need for richer event metadata.

WHAT THIS FORCES US TO BELIEVE
- Minimal ledger must carry provenance metadata for stronger claims about uniqueness and intent.

NEXT QUESTION
- What minimal metadata disambiguates replay vs genuine repeats without resorting to full distributed consensus?


EXPERIMENT 3 — Joining, leaving, lost access

EXPERIMENT
- Eve joined by receiving a transfer; Bob leaving without transferring his holdings is not implemented.
- Charlie lost access recorded but holdings remain.

OBSERVATION
- Joining is simple; leaving without reassigning holdings creates policy questions.
- Lost access functionally leaves the universe unchanged.

FAILURE / SURPRISE
- Model treats inaccessible holdings as still part of the money supply; economic consequences depend on whether agents can detect accessibility.

WHAT THIS FORCES US TO BELIEVE
- Accessibility information should be part of the ledger if the lab will probe economic effects of lost keys.

NEXT QUESTION
- How does the presence of dormant/inaccessible holdings affect trades and inferred valuations?
