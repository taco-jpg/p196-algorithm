# Independent semantic review preparation: spectral carry charge

Status: **PRELIMINARY_SOURCE_MATCH; FROZEN-SOURCE BUILD AND FINAL REVIEW PENDING**.

Reviewer: runtime_scout, a nonauthor of every U/S target source. All inspected candidate bytes are retained in `preliminary-source-reading/`. No candidate module has yet been compiled by this reviewer. The earlier LychrelDigitSums baseline is environment evidence and is not an import or dependency of this package.

## Source and ownership pins

The claimed target is `SPECTRAL-CARRY-CHARGE-ZERO`, reserved in coordination commit `9ff01fb85383833abe440d7f41bc7c249c332070`; the task-record blob is `70340af5e48d1c965d012180c04bc6ea01f90b21`.

The original repository snapshot is `5ff4f607535587d572fbc9e95ba9501d1fbe5fc5`:

- Original note: `creative_global_spectral_notes.md`, blob `cb1c355fa05916a770816a4d5ef680e54079cccb`.
- Original companion implementation: `creative_global_spectral.py`, blob `730acd722bf017b6bf1e51e5a0411169a7804da4`; current flattened path `proofs/creative_global_spectral__8de5a77a944d0d04.py`.

The note states that the integer weights defining J dominate the sum of smaller weights and that J vanishes exactly when the full carry polynomial equals its fixed-length reflection. The companion `carry_coordinates` function fixes the exact signs, parity formulas, and recurrence seeds. Both original files and the published claim record are retained unchanged beside this report.

## Exact mathematical contract

Let c be a finite list of binary carry values. Its entries are the outgoing carries, in least-significant-column-first order. The last entry is the outgoing carry h. The initial incoming zero is not an entry of c.

Define integer sequences U and S by U(0)=0, U(1)=1, S(0)=1, S(1)=21, and X(k+2)=20X(k+1)-X(k). The used odd weights are U(k+1); the even weights are S(k). For every index n, each used weight must be positive and strictly greater than the sum of the n preceding used weights.

For length 2m+1 the exact original charge is:

```text
J(c) = sum(i=0,...,m-1) (c[2m-i] - c[i]) * U(m-i).
```

For length 2m it is:

```text
J(c) = sum(i=0,...,m-1) (c[2m-1-i] - c[i]) * S(m-1-i).
```

Subtraction takes place in the integers after casting the carry entries. The center of an odd word does not occur in this sum. Reflection is with respect to the full list length even when the last carry is zero. The desired equivalence is J(c)=0 if and only if reverse(c)=c, under the binary-entry premise. The empty list is a labeled algebraic extension of the original positive-width setting.

## Preliminary signature and definition review

| Obligation | Candidate declaration or definition | Preliminary finding |
|---|---|---|
| Exact integer recurrence and seeds | `recurrence`, `U`, `S`, corresponding zero/one/step lemmas | Definitions use Int subtraction and the exact original seeds. |
| Correct first used weights | `oddWeight`, `evenWeight` | Odd starts at U(1), even at S(0), both equal 1 at index zero. |
| Strict domination over all earlier weights | `oddWeight_superincreasing`, `evenWeight_superincreasing`, `weightSum` | `weightSum w n` contains precisely indices 0 through n-1, and conclusions are strict. |
| Binary domain | `Binary` | Every member of the Nat list equals 0 or 1. No unproved realizability premise is inserted. |
| Fixed-length highest-weight coding | `weighted`, `weighted_injective_binary` | Leading coefficient receives the weight indexed by tail length; injectivity explicitly requires equal lengths. |
| Full-length reflection | `reverse_take_half_iff`, `halfCharge` | Reversal and both half-length takes use the complete list. No trimming or added incoming bit occurs. |
| Final universal equivalence | `carryCharge_zero_iff` | Its sole substantive premise is `Binary cs`; the conclusion is exact list reversal equality. |
| Ordinary finite-sum interpretation | `sumFirst_eq_range_sum` | The recursive summation is proved equal to the mapped `List.range` sum. |
| Exact original parity formulas | `carryCharge_eq_odd_source_sum`, `carryCharge_eq_even_source_sum` | Original signs, outer weight indices, both integer casts, and length equalities are present. |
| Equivalence stated directly for the original sums | `odd_source_charge_zero_iff`, `even_source_charge_zero_iff` | The original sum itself is equated to zero, with exact parity length and binary premises. |
| Boundary and convention controls | Nine `ChargeControls` declarations | Empty, singleton, two-entry, odd center, symmetry, 419-value, nonbinary, incoming-zero, and zero-overflow controls are explicit. |

All names in this table belong to `P196.Agent15.SpectralCarry`. The inspected copies contain five modules and 69 explicit public definitions/theorems. The independently extracted full list is in `expected-public-exports.txt`, with module attribution in `expected-public-exports-by-module.json`. This is a source inventory; it is not yet an executed export audit.

## Adversarial scope checks

The equal-length requirement in `weighted_injective_binary` is necessary: lists [1] and [0,1] have the same highest-first code when the unit weight is 1. Its actual statement retains the length premise, and the two halves extracted from one full word have equal lengths automatically.

The binary premise is necessary: for the even weights 21 and 1, the nonbinary list [1,0,21,0] has charge zero but is not symmetric. The candidate retains this fact as an exact kernel-computable control, not as a premise or proof of the universal theorem.

Full length matters when h=0. For example, [0,1,0] is symmetric with zero charge, while deleting its final outgoing zero changes the word to [0,1], whose charge is 1. Likewise, adding the incoming zero to [1,1] changes a zero-charge word into [0,1,1], whose charge is 1. The candidate definitions and controls preserve these distinctions.

The first used odd weight must be U(1), not U(0). The inspected `oddWeight` definition has the required shift. The source-sum bridge proves the reindexing under i<m; no truncated Nat subtraction is used for the signed coefficient difference.

The candidate does not require a zero odd center, a fixed overflow bit, symmetry as a premise, a bounded maximum length, or a supplied desired conclusion. It does not claim the excluded T/R injectivity theorem, a square-root spectral interpretation, the four-case evolution law, an orbit invariant, or a decimal Lychrel result. The generic carry-list equivalence can cover the original binary-word claim without replacing it by bounded enumeration.

## Independent execution gate prepared

`clean_review.py` requires a full immutable source commit, an explicit root module, the exact expected five-module closure, an explicit list of the 69 public exports, and required endpoint names. It compares every copied source with the committed Git blob through read-only Git commands. It uses a new evidence directory, copies only source, and sets LEAN_PATH to that new directory. Project objects from author runs and the decimal baseline cannot be imported from there.

Every target compiler invocation uses official Lean 4.19.0, release commit 6caaee842e94, with `-j1 -DElab.async=false --trust=0`. The executable, Lean shared libraries, directly imported standard objects, and all target source bytes are hashed and checked again after execution.

The audit enumerates constants by source module of origin. It checks the kernel's checked environment before collecting axioms. All safe definitions, theorems, opaque constants, inductives, constructors, recursors, private helpers, and generated safe declarations receive signature output and an actual `#print axioms` command. New safe axioms are rejected, and every safe declaration's transitive axioms must be contained in {propext, Classical.choice, Quot.sound}.

Lean also generates unsafe implementation constants such as `_cstage1` and `_cstage2`. They are inventoried, their signatures and actual axiom reports remain visible, and they do not count as mathematical declarations or expand the allowed mathematical axiom set. Explicit unsafe/partial source constructs are rejected. A separate source-origin audit covers every safe declaration, so an excluded axiom cannot be hidden behind an imported theorem.

The requested second pass will execute literal `#print` and `#print axioms` commands for all 69 explicit public exports. The final report will keep its coverage distinct from the larger origin-based inventory.

The audit mechanism passed an unrelated fixture: 22 total constants, 18 safe constants, four compiler implementation constants, and 22 matching actual `#print axioms` outputs. Failed infrastructure attempts 001 and 002 remain preserved. Attempt 001 exposed an unsupported pretty-printer option and an overbroad template replacement; attempt 002 exposed compiler-generated unsafe implementation constants. Neither is a U/S source failure.

## Storage and finalization state

The overlay filesystem became full during preparation. The parent authorized removal of exactly five regenerable .olean objects after recording their hashes and metadata; every source, failed source, log, command, and receipt remains. `environment-cleanup.json` records those deletions and explains why the earlier objects are no longer eligible for reuse.

The parent then authorized this memory-backed directory for review evidence. `copy-provenance.json` records byte-identical copies of the preparation sources and failures. The Lean distribution was not copied or altered. The frozen-source gate and the final semantic verdict remain pending the parent's explicit source-freeze signal.
