# Author completion record: actual carry support at nine

Recorded: 2026-10-16T23:36:28.828824+00:00

## Identity and verification boundary

- Protected task: `agent15-spectral-carry-support-43cf6e114472`.
- Claim commit: `3de89d0bd03534c92f65886a29b7996525571ff5`.
- Task blob: `2707332dbc4dc1274bb8470b15e17f6350618bba`.
- Mathematical source: `ActualCarrySupport.lean`.
- Final source SHA256: `4c06522efae7aa254b6281003d042e49f6b60162d01d00881d50052c7a73c646`.
- Final source Git blob: `c0e5562e1661570546bced3dca82dd4fb459fa5f`.
- Namespace: `P196.Agent15.SpectralSupport`.
- Author status: `AUTHOR_CHECKED`, with a successful author public signature and transitive axiom audit.

This record reports author work only. The coordinator owns publication, independent semantic review, the separately executed fresh eight-module closure, all-origin declaration audits, and any integration status. Author compilation is not presented as independent acceptance. No Git reference, remote, protected claim, existing foundation, or shared registry was modified by this author.

The final source is frozen at the hashes above. The final change was the semantic reviewer's documentation correction relayed by the coordinator: `outgoing_last` applies even to unbounded coefficients, so its result is called the actual final outgoing carry, rather than universally a bit. No theorem statement or proof changed in that correction.

## Exact completed contract

The two definitions are literal adapters to existing objects:

```lean
def outgoing (q : Nat → Nat) (L : Nat) : List Nat :=
  (List.range L).map (fun i => DecimalDigits.carry q (i + 1))

def actualCharge (q : Nat → Nat) (L : Nat) : Int :=
  P196.Agent15.SpectralCarry.carryCharge (outgoing q L)
```

Let `hb` be `∀ i, i < L → q i ≤ 18` and let `hs` be `∀ i, i < L → q i = q (L - 1 - i)`. The complete required propositions are proved as follows.

| Contract obligation | Public theorem(s) | Hypotheses and exact conclusion |
| --- | --- | --- |
| Length, in-range indexing, binary values | `outgoing_length`, `outgoing_getElem`, `outgoing_getElem?`, `outgoing_binary` | The length is exactly `L`; index `i` equals `carry q (i+1)`; only binary membership uses `hb`. |
| Final outgoing carry retained | `outgoing_last` | For `0 < L`, the last entry is `carry q L`; no bound or overflow assumption is added. |
| Charge-zero adapter | `outgoing_reverse_iff`, `actualCharge_zero_iff` | Under `hb` alone, charge is zero exactly when every `i < L` satisfies `carry q (i+1) = carry q (L-i)`. |
| Local support outside nine | `outgoing_reflected_eq_of_nonnine` | Under `hb`, `hs`, `i < L`, and `q i ≠ 9`, the same reflected carry equality holds. |
| Exact nonzero support | `actualCharge_nonzero_iff_nine_asymmetry` | Under `hb` and `hs`, nonzero charge is equivalent to `∃ i, i < L ∧ q i = 9 ∧ carry q (i+1) ≠ carry q (L-i)`. |
| Literal no-nine implication | `actualCharge_zero_of_no_nine` | Under `hb`, `hs`, and no in-range coefficient nine, charge equals zero. |
| Real canonical specialization | The four `canonical_*` theorems | Each retains `DecimalDigits.Canonical n d L`, sets `q = DecimalDigits.columnSum d L`, and uses the existing coefficient bound and symmetry. |

There are no outer-positivity, even-center, no-overflow, or orbit assumptions in the general support theorems. The list includes `carry q L` even when zero and never inserts `carry q 0`. The charge is the existing exact unbounded integer expression with its original parity selection. The canonical wrappers retain the original positive-width canonical definition instead of redefining digit realizability.

## Proof composition

The exact in-range list entries come from `List.range` and `List.map`. List reflection changes index `i` into `L - 1 - i`; the outgoing shift then yields `(L - 1 - i) + 1 = L - i`. This equality is established only for the required in-range indices.

`DecimalDigits.carry_bounded` proves each relevant computed carry is at most one from coefficients bounded only within `L`. The existing `carryCharge_zero_iff` is then composed with the list-reflection bridge. This step does not assume symmetry of `q`.

For local support, the proof instantiates `RawSymmetryObstruction.nonnine_binary_div` with coefficient `q i` and the actual incoming carries `carry q i` and `carry q (L - 1 - i)`. Existing carry bounds discharge its bit hypotheses; `hs` identifies the paired coefficients; unfolding the existing carry recurrence identifies the two quotients as the outgoing carries. No division arithmetic is reproved and no new carry model is introduced.

The global nonzero theorem composes this local equality with charge faithfulness. A violated reflected equality must therefore occur at nine. The reverse implication uses the same faithfulness adapter. The no-nine theorem is the stated one-way corollary. The canonical wrappers supply bounds and symmetry using `columnSum_bounded` and `columnSum_symmetric`.

## Boundary and concrete kernel controls

| Declaration | Actual coefficient values within the width | Computed outgoing word | Charge |
| --- | --- | --- | --- |
| `actualCharge_width_zero` | Any `q`, width 0 | Empty word | 0 |
| `actualCharge_width_one` | Any `q`, width 1 | Its single actual outgoing carry | 0 |
| `Controls.nine_zero_charge` | `[9, 9]` | `[0, 0]` | 0 |
| `Controls.even_overflow_zero_charge` | `[10, 10]` | `[1, 1]` | 0 |
| `Controls.odd_free_center` | `[8, 18, 8]` | `[0, 1, 0]` | 0 |
| `Controls.odd_nine_asymmetry` | `[9, 18, 9]` | `[0, 1, 1]` | 1 |

The nine-zero control explicitly proves an in-range coefficient equals nine. It prevents interpreting the support theorem as a converse from the mere presence of nine. The four concrete controls use ordinary kernel-checked `decide` and their axiom reports are empty. The general theorem remains universal; these controls do not replace it.

## Reused source closure and author compilation

Every Lean invocation used the official compiler at `/tmp/p196-agent5-lean/lean-4.19.0-linux/bin/lean` with `--trust=0 -j1 -DElab.async=false`.

The author first copied and hash-verified the seven unchanged dependency sources into a newly created owned build directory, preserving their bytes. The three legacy Git blobs matched the contract. The four spectral files matched `e8d706dc8a67248e1531b0b828fbe05ff50052ed` through read-only Git object queries. No `ChargeControls` module is imported by the target.

- `dependency-build-0001`: `LychrelDigitSums`, `IncomingCarrySensitivity`, `RawSymmetryObstruction`; all exit 0.
- `dependency-build-0002`: `SpectralWeights`, `BinaryCode`, `ChargeSymmetry`, `SourceFormula`; all exit 0.
- The new target is the eighth module of the selected mathematical closure.

Each dependency group preserves source paths, exact SHA256 and Git-blob hashes, command arrays, working directory, `LEAN_PATH`, stdout, stderr, exit code, and elapsed time. Subsequent author attempts explicitly reuse only those compiled dependency objects. These are author iterations, not fresh independent acceptance runs.

## Preserved attempts and audit results

| Record | Result | Interpretation |
| --- | --- | --- |
| `attempt-0001` | Lean exit 1 | Complete first source attempt. Failures: missing beta reduction before a list-index rewrite, unavailable `by_contra` tactic in this Std environment, and two unsuccessful `rfl` boundary proofs. |
| `attempt-0002` | Lean exit 0 | Elaboration corrections only: explicit type change, `Classical.byContradiction`, and simplification for the two boundary controls. |
| `attempt-0003` | Lean exit 0 | Documentation-only correction to `outgoing_last`; this is the frozen final source. |
| `audit-0001` | Lean exit 1 | Audit configuration error: unsupported `pp.width` option. Its full audit source and output remain preserved. |
| `audit-0002` | Lean exit 0 | Public audit with the unsupported optional formatting directive removed. |
| `audit-0003` | Lean exit 0 | Public audit against the final source bytes. Its complete signature and axiom output is byte-identical to the successful pre-documentation audit. |

All source attempts and audit attempts are separate immutable snapshots. Each has its exact source copy, command and result records, full stdout, and full stderr. The theorem source was never replaced by a weakened proposition or an oracle conclusion.

The final public audit covers 22 declarations: 2 definitions and 20 theorems. The only transitive foundational axioms reported are `propext`, `Classical.choice`, and `Quot.sound`. The two definitions and four concrete controls have empty axiom reports. No forbidden axiom or compiler-trusted evaluation shortcut is used by an exported target declaration. Full all-origin dependency auditing, including private mathematical declarations and separate generated implementations, belongs to the independently executed acceptance evidence.

## Public export list

The following names are under `P196.Agent15.SpectralSupport`:

```text
outgoing
actualCharge
outgoing_length
outgoing_getElem
outgoing_getElem?
outgoing_last
outgoing_binary
outgoing_reverse_iff
actualCharge_zero_iff
outgoing_reflected_eq_of_nonnine
actualCharge_nonzero_iff_nine_asymmetry
actualCharge_zero_of_no_nine
canonical_actualCharge_zero_iff
canonical_outgoing_reflected_eq_of_nonnine
canonical_actualCharge_nonzero_iff_nine_asymmetry
canonical_actualCharge_zero_of_no_nine
actualCharge_width_zero
actualCharge_width_one
Controls.nine_zero_charge
Controls.even_overflow_zero_charge
Controls.odd_free_center
Controls.odd_nine_asymmetry
```

## Scope and handoff

The claimed arithmetic-to-list bridge and support theorem are complete at author-check status. This module does not assert `J = 0` iff no coefficient nine, charge persistence, a new palindrome criterion, the four evolution laws, T/R injection, H, quotient classification, carryfree residue saturation, or a conclusion about 196.

All new author writes are confined to `ActualCarrySupport.lean` and `development/author/` within the owned contribution. Coordination messages were sent only to the parent for relay through issue #61. No external message or Git mutation was made by this author. There was no approval denial and no workaround around an approval boundary. The initial absent-dependency-path event is recorded separately in `PREPARATION.md` as preparation, not as a Lean failure.
