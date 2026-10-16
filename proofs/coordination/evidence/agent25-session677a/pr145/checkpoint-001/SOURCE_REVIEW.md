# PR #145 — Exact-source semantics and build-contract review

## Disposition

**PASS for the delegated source-semantics and build-contract scope. No source amendment is requested.**

The five source modules at `e8d706dc8a67248e1531b0b828fbe05ff50052ed` implement the advertised finite binary carry-charge symmetry theorem and the literal historical odd/even sums without a detected statement weakening, missing parity, changed sign, truncated word, constrained odd center, or hidden orbit hypothesis.

This is Agent #25 / `/root/pr145_source`'s independent read-only integration-source assessment. The reviewer did not author or alter these sources. It supplements the existing author-team semantic and execution evidence; it is not a new mandatory review-of-review gate. No Lean command, canonical checker, historical executable, or expensive build was run in this assessment. No remote comment, review, branch update, or merge was performed.

Delivery owner remains Agent #25 / `/root`; source ownership remains Agent #15, session `43cf6e114472`. Integration, platform gates, retained execution-evidence assessment, and combined-target verification are assigned elsewhere in the parent team.

## Frozen scope and evidence

Repository: https://github.com/taco-jpg/p196-algorithm  
Pull request: https://github.com/taco-jpg/p196-algorithm/pull/145  
Source commit: `e8d706dc8a67248e1531b0b828fbe05ff50052ed`  
Contribution prefix: `proofs/contributions/agent-15/spectral-carry-charge-43cf6e114472/`  
Historical source snapshot: `5ff4f607535587d572fbc9e95ba9501d1fbe5fc5`

The PR metadata read reported the exact source head above, an open draft PR, and 32 added files. This assessment does not claim to have reviewed all archive members or every changed evidence file; those are the evidence specialist's scope. It covers the complete five-module mathematical source closure, build/checker declarations, scope documents, provenance declaration, exact historical notes and implementation, and current policy documents listed below.

Every listed file was read in full through supported GitHub connectors. The two historical paths were also resolved at their cited snapshot and returned their stated blob IDs. Sixteen exact UTF-8 snapshots were saved locally and independently recomputed Git object hashes matched every listed blob. The five source SHA-256 values and byte lengths were checked against BUILD.json; all matched. The canonical public-declaration scanner was applied as static text analysis and found exactly 69 declarations.

### Complete file identities

Paths in the first eleven rows are relative to the contribution prefix.

| File | Git blob SHA-1 |
| --- | --- |
| SpectralWeights.lean | 40afa93196976972e5c0f6772a18e50c1e635a3f |
| BinaryCode.lean | 35ba9bee5afb9bb47f39738e44860a02ea9b2469 |
| ChargeSymmetry.lean | f69efd4bc0642759dddf99834d5d093c929761a5 |
| SourceFormula.lean | 1db4a109629abddf355d12e8a14f2cfb0e26a39b |
| ChargeControls.lean | b7a1c9f7d0d175fb3f2abea93fcd23bd5eb082f8 |
| BUILD.json | 2db6888f25f2c0992ba755203e44324154b1aabd |
| check.py | ea730bac77298967a8be4e103b0de5b40cd2a5a8 |
| CONTRACT.md | a9835e4f64ec20177e329a5ffec159afb33570a0 |
| README.md | a0c08831e0991a33247b1585eb0eae94143af12c |
| CLAIM.json | 70340af5e48d1c965d012180c04bc6ea01f90b21 |
| lean-toolchain | 7aca1d8a939cc24c413eddd793671cdce7070b74 |
| proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/research/creative_global_spectral_notes.md | cb1c355fa05916a770816a4d5ef680e54079cccb |
| proofs/creative_global_spectral__8de5a77a944d0d04.py | 730acd722bf017b6bf1e51e5a0411169a7804da4 |
| AGENTS.md | 70369d40fb35e8afd8493bd19965efc6bd3ce5b8 |
| proofs/PUBLICATION_POLICY.md | 515b507a806c141ea30ac3bfb59200745a8c9e15 |
| proofs/README.md | 15d570ab8b6652b2ee11fb187bdd9d17a7e6536c |

The parent confirmed the three policy blobs against current main `1ed1a033be77ca2a1c91331ede67eb030b8ec6ca`. AGENTS.md was independently fetched from main and its returned blob matched. The other two policy blobs were fetched directly and read completely. This report does not treat a branch name as a permanent base pin.

## Exact mathematical endpoint

The public endpoint in ChargeSymmetry.lean, line 84, is:

```lean
theorem carryCharge_zero_iff {cs : List Nat} (hc : Binary cs) :
    carryCharge cs = 0 ↔ cs.reverse = cs
```

Here `Binary cs` means every member is 0 or 1 (BinaryCode.lean, line 10). This is a universal statement about every finite list satisfying that hypothesis. There is no upper length bound, enumeration premise, trajectory-membership condition, symmetry premise, zero-charge premise outside the equivalence, or inconsistent assumption.

The general supporting injectivity theorem explicitly requires equal lengths and binary coefficients, together with nonnegative and strictly dominating weights. The final endpoint supplies the required weight facts using proved U/S recurrence lemmas. Equal half-word length follows from taking the same floor half-length from a word and its reverse. The equal-length hypothesis is not silently removed.

The domain intentionally remains binary lists of natural numbers. It is not a theorem about arbitrary natural or integer coefficients. ChargeControls.lean, line 23, exhibits the nonbinary cancellation word `[1,0,21,0]`, which has zero charge without reversal symmetry.

## Source formula agreement

The historical implementation's `qstep` appends each outgoing carry in least-significant-first order and returns that complete list. It separately appends an output digit when overflow occurs; it does not append an extra entry to the carry word. Thus the final carry entry is the actual overflow bit, and the initial incoming zero is outside the outgoing-carry word.

The historical `carry_coordinates` sets `L = len(cs)`, `m = L // 2`. It uses:

- Odd length: `sum((cs[L-1-i]-cs[i])*u[m-i] for i in range(m))`, with U beginning 0, 1.
- Even length: `sum((cs[L-1-i]-cs[i])*s[m-1-i] for i in range(m))`, with S beginning 1, 21.

Both sequences obey `X(k+2) = 20*X(k+1)-X(k)`.

SpectralWeights.lean defines those exact integer recurrences. BinaryCode.lean evaluates lists highest-weight first. ChargeSymmetry.lean defines the charge as the weighted reversed outer half minus the weighted original outer half, selecting U(k+1) or S(k) according to the complete list's parity.

SourceFormula.lean proves the required bridge rather than leaving it as a prose identification:

- `sumFirst_eq_range_sum` (line 14) identifies the recursive finite sum with `List.range` summation.
- `weighted_eq_sumFirst` and `weighted_take_eq_sumFirst` expand the evaluator.
- `halfCharge_eq_source_sum` (line 65) gives all mirror differences with the full list length.
- `carryCharge_eq_odd_source_sum` (line 106) gives the literal U formula under `cs.length = 2*m+1`.
- `carryCharge_eq_even_source_sum` (line 115) gives the literal S formula under `cs.length = 2*m`.
- `odd_source_charge_zero_iff` and `even_source_charge_zero_iff` (lines 124 and 133) apply the universal equivalence directly to those displayed sums, with the explicit length and binary hypotheses.

The conversion is over Lean `Int`, so mirror subtraction is signed rather than natural truncated subtraction. Index arithmetic uses natural subtraction, but the sums only use indices below m. The proofs make the range restrictions explicit; odd weights therefore run from U(m) through U(1), never mistakenly through the zero weight U(0).

The historical notes' assertion “J=0 exactly when C=C*” is interpreted at the supplied complete length, matching its reflected carry polynomial convention. No numeric normalization or trimming changes that length.

## Boundary and convention checks

1. **Full length and final overflow:** All definitions use `cs.length`. No filtering, trimming, padding, insertion, or removal of a final zero appears. The retained-zero control compares `[0,1,0]` with `[0,1]` and distinguishes their charges.
2. **Incoming zero:** No incoming zero is prepended. A dedicated control distinguishes `[1,1]` from `[0,1,1]`.
3. **Odd center:** Outer halves omit the central position from the numerical difference, while full-list reversal compares that position to itself. `reverse_take_half_iff` proves the central-index case explicitly. Either binary central value remains admissible, as shown by `[0,0,0]` and `[0,1,0]`.
4. **Both parities:** The final endpoint selects the charge using the actual length modulo 2. The two literal source endpoints retain their exact odd/even length equations.
5. **Sign:** The right mirror bit minus the left bit agrees with the historical implementation. The controls give +1 for `[0,1]`, -1 for `[1,0]`, and +419 for `[0,1,0,0,1,1]`.
6. **Empty word:** The parity-selected extension gives zero and reversal fixes the empty list. CONTRACT and README expressly label it an algebraic extension, avoiding an assertion that an empty word is the outgoing carry word of a positive integer.
7. **Singleton:** The half-length is zero, so either binary singleton has zero charge and is symmetric.
8. **Physical extraction:** This package does not formalize a digit-extraction or qstep-to-list arithmetic bridge. Its theorem is stronger than a sampled-carry statement in the finite binary-list domain, but its connection to actual reverse-and-add dynamics remains semantic provenance rather than a newly proved all-time arithmetic result. The scope documents accurately exclude those further results.

## Proof structure and source soundness

The recurrence proof establishes positivity and growth by a factor at least 19, then derives that each used weight strictly exceeds the sum of all preceding weights. Binary weighted evaluation is bounded between zero and that preceding-weight sum. An unequal highest bit would contribute a whole current weight, too large for lower bits to cancel; induction yields equal-length binary-code injectivity.

The list lemma proves that agreement of the two outer halves is equivalent to full reversal symmetry, including the odd center and out-of-range option cases. Applying injectivity to the two binary halves yields the zero-charge equivalence. This argument is unbounded in list length.

All five source modules were read completely, including both private weight lemmas. No `axiom`, `sorry`, `admit`, `sorryAx`, `native_decide`, `Lean.ofReduceBool`, externally asserted oracle, or unsafe theorem shortcut was found in the contribution source. The nine finite controls use ordinary `by decide`, which is distinct from compiler-trusted native evaluation. They supplement, and are not used as a substitute for, the universal proof.

This source reading does not independently establish the compiled transitive axiom output. The separate retained execution audit remains the evidence for that fact; this reviewer did not rerun or claim to have rerun it.

## Build and checker semantics

The selected local import chain is exactly:

`SpectralWeights → BinaryCode → ChargeSymmetry → SourceFormula → ChargeControls`

SpectralWeights imports only `Std`. The other modules import their immediate local predecessor. No decimal baseline or unrelated repository Lean module is an imported dependency.

The checker is consistent with its advertised limited role:

- Creates a new output directory using `exist_ok=False`.
- Copies all five selected sources and records exact SHA-256 hashes and byte counts.
- Sets LEAN_PATH to the fresh copied-source directory.
- Requires Lean version 4.19.0 with compiler commit substring `6caaee842e94`.
- Compiles all five modules in dependency order using `--trust=0 -j1 -DElab.async=false`.
- Stops subsequent compilation after a failed command.
- Prints each scanned public declaration and its transitive axioms.
- Rejects axiom sets outside `propext`, `Classical.choice`, and `Quot.sound`.
- Requires the observed audited declaration-name set to equal the scanned public-name set.
- Preserves command arguments, return codes, combined output logs, hashes, and a PASS/FAIL receipt.
- Rechecks copied source hashes and the Lean executable hash at completion.

### Disclosed limits, with no new gate requested

The regular expression intentionally scans explicit public `def` and `theorem` declarations. It omits private and generated declarations; CONTRACT and README explicitly assign a separate module-origin audit before acceptance. The existing independent audit should be reused for that obligation. The public transitive checks also cover the private dependencies reachable from public results, but that fact does not turn the public-name scan into a complete module-origin census.

The checker records source pins dynamically rather than comparing them itself to BUILD.json or a commit ID. This assessment closes the exact-head mapping for the read source by checking the five recorded BUILD.json hashes and Git blob identities. Future runs must similarly retain and compare the resulting pins to the intended reviewed source.

The checker records the executable and, when present, shared-library hashes, but it is not a full distribution-provenance verifier. It does not hash every installed standard-library object or recheck the shared-library hash at the end. The separate trusted-runtime and module-origin evidence is the relevant existing obligation. No evidence found here requires a duplicate build.

These limitations are not defects in the advertised standalone checker scope. No source-only observation in this assessment invalidates the existing review or execution evidence.

## Current policy consistency and handoff

The package distinguishes formal finite-word results from the still-unproved 196 conjecture, preserves historical authorship, and explicitly excludes the real quadratic interpretation, H, transition laws, T/R coordinate injection, persistent nonzero charge, and all-time palindrome avoidance. Its status at the frozen source correctly describes the author build as completed while final independent reviews and repository integration were pending. Later evidence can supplement that frozen checkpoint without changing a theorem.

The current publication policy permits lossless archives while requiring source and substantive verification history preservation. The actual archive-byte and retained-log verification is delegated to the evidence specialist and is not asserted in this report. The root and contribution documents consistently reserve shared registry changes and main integration for the integration owner. A standalone package need not be falsely represented as covered by the old consolidation-core default verifier; proofs/README.md explicitly requires independent commands for other sources.

**Next action for the delivery owner:** combine this exact-source assessment with the already existing independent semantic/execution evidence and the evidence specialist's byte checks, refresh the intended integration tree and applicable platform state, then carry out the next authorized delivery action. This assessment introduces no further semantic review, source repair, or Lean rebuild requirement.

## Retained local outputs

- `source-review.md`: this report.
- `source-manifest.json`: all sixteen file identities, source refs, byte lengths, and SHA-256 values.
- `static-source-check.json`: PASS receipt for Git identities, five BUILD.json pins, and 69 public declarations; explicitly records Lean and checker execution as NOT_RUN.
- `snapshots/`: exact complete source, historical, and policy files read.

These outputs reside under the parent's approved private temporary-memory directory. Access from the ordinary sandbox did not expose that mount; parent retrieval should use the same approved execution environment used to create it. No existing data was deleted.
