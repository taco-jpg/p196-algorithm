# Formalization contract: actual carry asymmetry is supported at nine

## Original source and ownership

Original snapshot: `5ff4f607535587d572fbc9e95ba9501d1fbe5fc5`. The original note is `proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/research/creative_global_spectral_notes.md`, blob `cb1c355fa05916a770816a4d5ef680e54079cccb`, lines58-66. The original script is `proofs/creative_global_spectral__8de5a77a944d0d04.py`, blob `730acd722bf017b6bf1e51e5a0411169a7804da4`: lines8-13 compute the carry word, lines28-38 define J, and lines51-53 check support at9 and the no-nine implication.

The original statement says that for symmetric bounded paired coefficients, an asymmetric pair of outgoing carries can occur only at coefficient9. Consequently, no coefficient9 implies J=0. Its converse is not asserted. This task supplies the exact arithmetic-to-list bridge and composes existing results; it does not claim discovery of that mathematics.

Protected task: `agent15-spectral-carry-support-43cf6e114472`, claim `3de89d0bd03534c92f65886a29b7996525571ff5`, task blob `2707332dbc4dc1274bb8470b15e17f6350618bba`. Only the new contribution directory is writable under this task. Existing source modules retain their original authors and hashes.

## Exact input and charge convention

Quantify over `q : Nat -> Nat` and `L : Nat`. The general bounds are `hb : forall i, i < L -> q i <= 18`. The support theorem additionally assumes `hs : forall i, i < L -> q i = q (L-1-i)`.

Use the existing `DecimalDigits.carry` recurrence. Define exactly:

```
outgoing q L = (List.range L).map (fun i => DecimalDigits.carry q (i+1))
actualCharge q L = P196.Agent15.SpectralCarry.carryCharge (outgoing q L)
```

The word has L entries. It includes the actual last outgoing carry `carry q L`, even when that bit is0, and excludes the separately known incoming zero `carry q0`. Do not insert, trim or normalize any entry. The existing charge retains its original odd/even U/S formulas and unbounded integer arithmetic.

## Required propositions

Namespace: `P196.Agent15.SpectralSupport`. Expected source: `ActualCarrySupport.lean`.

1. Prove the exact outgoing length, in-range index correspondence and Binary predicate under hb. Bounds are only required within the original width.
2. Under hb alone, prove `actualCharge q L = 0` iff every `i < L` satisfies `carry q (i+1) = carry q (L-i)`. No symmetry of q is needed for this adapter.
3. Under hb and hs, prove at every `i < L` that `q i != 9` implies that same reflected carry equality. Reuse `RawSymmetryObstruction.nonnine_binary_div`; do not reprove its arithmetic.
4. Under hb and hs, prove `actualCharge q L != 0` iff there is an `i < L` with `q i = 9` and `carry q (i+1) != carry q (L-i)`. This is the exact support statement composed with the already proved faithfulness of J.
5. Derive the literal no-nine corollary: if every in-range coefficient differs from9, then `actualCharge q L = 0`.
6. Specialize the support/zero consequence to `DecimalDigits.Canonical n d L` and `q = DecimalDigits.columnSum d L`, using the existing coefficient bounds and symmetry. Keep the canonical digit representation and existing carry computation explicit.

The general list/function theorem covers L=0 and L=1 as algebraic boundary cases. It needs no outer positivity, even-center predicate, no-overflow condition or orbit premise. The canonical wrapper inherits the existing definition's actual width and digit conventions. A central odd carry remains free, and both actual overflow values are included.

## Exact reused interfaces and dependency closure

The source pin for the charge package is `e8d706dc8a67248e1531b0b828fbe05ff50052ed` (PR145): `SpectralWeights`, `BinaryCode`, `ChargeSymmetry`, `SourceFormula`.

At the original main snapshot, reuse these unchanged modules:

| Module | Existing repository source | Git blob |
| --- | --- | --- |
| LychrelDigitSums | proofs/LychrelDigitSums__0810ace083af80c5.lean | 8a865176625283648a8a20dd2411ed77670eb0a2 |
| IncomingCarrySensitivity | proofs/IncomingCarrySensitivity__5d4952e23e746f6d.lean | 9ccc745471fd509fb68652fef40454478087e92e |
| RawSymmetryObstruction | proofs/RawSymmetryObstruction__5c1be305a04af2b7.lean | 9d4250f3e5daa5ff26f097a7e12ce98830dd9e89 |

The exact local chain is `RawSymmetryObstruction -> IncomingCarrySensitivity -> LychrelDigitSums -> Std`. `carry_bounded`, `columnSum_bounded`, and `columnSum_symmetric` already provide the arithmetic foundations. Instantiate `nonnine_binary_div` with `a=q i`, incoming carries `carry q i` and `carry q (L-1-i)`, then use symmetry and the existing recurrence. No reset-cut construction is needed.

A single new module importing `SourceFormula` and `RawSymmetryObstruction` gives an eight-module mathematical closure. The unrelated prior ChargeControls module is outside this new import closure; its original independent audit remains preserved in PR145.

## Verification and acceptance

Before final acceptance, compare the literal statements to this contract; preserve all failed attempts and exact source copies; rebuild the entire selected eight-module closure in a fresh directory with official Lean4.19.0 and `--trust=0 -j1 -DElab.async=false`; print all public declaration signatures and axioms; inspect all module-origin safe mathematical declarations, including private dependencies, with generated implementations reported separately. Permitted foundational axioms are only `propext`, `Classical.choice`, `Quot.sound`. No sorry/admit/sorryAx/native_decide/compiler oracle/new mathematical axiom is allowed.

Require genuine nonauthor semantic review and independent clean execution. Source present, author checked, independently reviewed, and integrated are distinct states. The root publishes checkpoints and preserves provenance. Main integration and shared registry changes remain with the designated integration owner.

## Explicit exclusions

This task does not establish `J=0 iff no coefficient9`, T/R injectivity, H, the four evolution laws, the real quadratic interpretation, quotient classification, Agent14's carryfree saturation witnesses, nonzero-charge persistence, a new palindrome criterion, or any all-time conclusion about196. It does not alter the frozen PR145 sources or replace the existing decimal carry recurrence by a newly convenient model.
