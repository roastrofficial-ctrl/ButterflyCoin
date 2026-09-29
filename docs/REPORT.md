BF¢-I Report

Summary
-------
This document records the BF¢-I experiment: a deterministic lab implementing a closed monetary universe where holdings are proportions of a fixed whole U=1.

Canonical model
---------------
- Universe: a fixed total U = 1.0
- Holdings: each participant `i` has `p_i` where sum(p_i) == 1.0
- Primitive operation: TRANSFER
  - `transfer_absolute(from_id, to_id, amount)` — moves an absolute proportion of U.
  - `transfer_fraction_of_holder(from_id, to_id, fraction)` — moves `fraction * p_from`.

Invariants
----------
- Conservation: sum of all holdings == 1.0 (enforced to 1.0 by normalization)
- No minting/burning: operations only redistribute existing proportions

Implementation
--------------
Files of interest:
- `bfcoin/lab/universe.py` — `Universe` class implementing the invariant and transfer primitives.
- `bfcoin/lab/ledger.py` — append-only `Ledger` for recording events with deterministic IDs.
- `bfcoin/lab/experiments.py` — deterministic experiments exercising edge-cases.
- `bfcoin/lab/run.py` — runs experiments and emits JSON-serializable results.

Experiments and Results
-----------------------
Run with:

```bash
python -m bfcoin.lab.run
```

Captured outputs (abbreviated):

- Simple absolute transfer: Alice -> Bob 0.01
  - Resulting holdings: Alice 0.24, Bob 0.26, Charlie 0.25, Diana 0.25
- Fraction transfer (10% of Alice): Alice -> Bob
  - Resulting holdings: Alice 0.225, Bob 0.275, Charlie 0.25, Diana 0.25
- Replay detection (same payload recorded twice): ledger records unique event IDs (collision resolved by counter), repeated transfers both execute.
- Overdraw attempt: Alice tried to send 0.3 and failed with InsufficientProportion; ledger recorded attempt.
- Concurrent-like sequence: two transfers based on same initial snapshot both attempted; second may fail depending on ordering — simulation shows second executed after first caused available balance to drop; model enforces conservations strictly.
- Joining: new participant `Eve` can appear by receiving a transfer; no minting required.
- Lost access: event recorded but holdings remain; inaccessible holdings still part of the universe.
- Identity split: explicit ledger event allowed splitting an identity into two new identities with proportional holdings; implemented by reconstructing holdings and re-normalizing.

Observations
------------
- The proportional framing is computationally straightforward: tracking floating proportions and normalizing preserves conservation.
- Two semantic transfer primitives are necessary and distinct: absolute transfers and fraction-of-holder transfers are not equivalent.
- The ledger can record attempted transfers, including failed ones; failed attempts leave trace but do not alter holdings.
- Replay is not intrinsically distinguished by payload alone; identical payloads produce identical initial hash-based IDs, so the ledger appends a counter to ensure unique event IDs. Distinguishing genuine repeats from replays requires stronger metadata (e.g., nonce, signature, sequencing).
- Joining and leaving raise conceptual questions about identity vs holdings: introducing new identities is achievable by transfer; removing identities without re-assignment would require governance rules external to the model.
- Lost access demonstrates that unreachable holdings still count in the universe — economically this is indistinguishable within BF¢-I unless the model is extended to record accessibility or implement recovery rules.

Failures & Surprises
--------------------
- Floating point rounding appears in printed snapshots (e.g., 0.22999999999999998) but normalization enforces sum==1.0; if fixed precision is required, use rationals or Decimal.
- The proportional model by itself does not provide any mechanism to map holdings to purchasing power or price. Exchanges record revealed preferences but do not create a canonical price function.
- Identity operations (split/merge) are underspecified economically: they can be constructed as ledger events but the canonical meaning depends on off-chain semantics (who controls new keys, legal continuity, etc.).

Equivalences to known systems
----------------------------
- Mechanically, BF¢-I is equivalent to an equity/share registry where total shares = 1 and participants hold fractional ownership.
- It is not yet a currency in the conventional sense because it lacks a pricing mechanism between money and goods. If goods are later priced in proportions or in revealed-preference-derived exchange rates, the system approximates an internal market-cap weighted price mechanism.

Conclusions
-----------
- "A balance is a relationship, not a quantity" is operationally meaningful: the canonical state is proportional ownership, and quantity displays (e.g., "250,000 BF¢") are derived representations.
- However, conceptually BF¢-I maps to ordinary fixed-supply accounting (equity shares) unless additional primitives are introduced to relate proportions to external economic value.

Next experiments (driven by observations)
----------------------------------------
1. Replace floating-point with rational arithmetic (fractions) to remove rounding artifacts.
2. Add non-monetary scarce goods (apples, houses) and record exchange offers/trades to see if inferred relative valuations emerge solely from revealed trades.
3. Implement an agent-driven market simulator where agents trade goods for proportions and examine emergent price relationships.
4. Explore governance rules for identity join/leave and recovery of lost access.

Appendix: full raw run output is saved in the repository when `python -m bfcoin.lab.run` is executed.
