# Agent #101 — Complete digit splitting and ordinary integer inverse fibers

Task: `agent101-digit-split-multiplicity-20261016`.

## Status and scope

All four new modules have compiled under the official Lean 4.19.0 release
(`6caaee842e94`). Their exported declarations have axiom reports containing
only the permitted foundational axioms `propext`, `Classical.choice`, and
`Quot.sound`. Source snapshots and the substantive failed attempts are retained
in this packet. The aggregate registry replay and separate complete semantic
review are being performed; their outcome is not assumed by this checkpoint.

This is a complete inverse-fiber result at a **fixed positive input width**.
It is not an infinite-orbit result or a proof of the 196 conjecture. The concrete
887 corollary additionally proves its own width exclusion, so that example is
complete across all input widths.

## Definitions and exact result

Finite digit lists are ordered from least to most significant digit. Define
`coefficientWord h c = h ++ c.toList ++ h.reverse`. A decimal list is canonical
when all entries are at most 9 and its last entry is positive. Empty lists do
not represent canonical positive integers.

`Agent101.canonicalWords h c` enumerates exactly the canonical lists whose
mirrored pair sums equal `coefficientWord h c`. Its membership theorem is a
bidirectional semantic characterization, not only a recursive specification.
The enumeration is duplicate-free.

`Agent101.numericFiber h c` maps those canonical lists to their ordinary
natural-number values. It is duplicate-free, and, when every coefficient is at
most 18, its membership theorem is:

```lean
n ∈ numericFiber h c ↔
  decimalWidth n (coefficientWord h c).length ∧
  Lychrel196.step n = natValue (coefficientWord h c)
```

Here `decimalWidth n L` is the ordinary interval condition
`0 < L ∧ 10^(L-1) ≤ n ∧ n < 10^L`. Neither side requires choosing an infinite
digit-function tail. The result also handles coefficient profiles with no
canonical realization.

For a nonempty half-profile `s :: h`, the exact count is

```lean
pairCount true s * centerCount c * natProduct (h.map (pairCount false))
```

For an internal pair, the factor is `s+1` for `s≤9`, `19-s` for `10≤s≤18`,
and zero otherwise. At the outermost pair the factor for `s≤9` becomes `s`,
because the highest digit must be nonzero. The center factor is one for no
center or a valid even center coefficient, and zero otherwise. The separate
single-digit and empty-profile clauses exclude the zero and empty numbers.

The exact count is at most `9 * 10^h.length`; the profile-level sharpness
theorems supply witnesses attaining this bound. This endpoint now counts actual
distinct integers, rather than unconstrained digit functions.

The checked concrete corollary is:

```lean
Lychrel196.step n = 887 ↔
  n ∈ [790, 691, 592, 493, 394, 295, 196]
```

## Source chain and attribution

- `Agent101DigitPairs.lean`: finite local pair choices, center cases, exact
  local counts. Written by the genuine `/root/runtime` specialist.
- `Agent101MultiplicityBounds.lean`: the profile formula and sharp uniform
  bounds. Written by the parent Agent #101; independently reviewed and rebuilt
  by `/root/runtime`.
- `Agent101SplitEnumeration.lean`: complete finite-list membership, no
  duplicates, exact product. Written by `/root/research_inventory`.
- `Agent101NumericFibers.lean`: finite-list/ordinary-integer correspondence,
  exact-width complete fibers, and the complete 887 example. Written by
  `/root/numeric_bridge`.

The only project foundation is the unchanged
`proofs/Lychrel196Research__c696e0ea3db39d92.lean`, compiled under its original
module name `Lychrel196Research`. Its SHA-256 is
`f8950d138fa4231b536059e2334d36b6496de3d25a806f4cf3925941aa05144c`.
The numeric bridge reuses the original `Lychrel196.step`, `DecimalDigits`
canonical-value semantics, `FoldedDecimal.step_eq_word_value`, and
`ReverseAddInverse.symmetric_value_injective` /
`same_width_step_eq_iff_pair_sums`. No replacement reverse-add operation is
introduced. Original authorship and source bytes are preserved.

## Reproduction and evidence

`proofs/Agent101Multiplicity.registry.json` pins all five source modules, their
imports, SHA-256 hashes, and Git blob hashes. It selects only this project's
complete dependency closure; it does not assert repository-wide acceptance.
Run the repository's unchanged verifier from the repository root:

```bash
python3 proofs/verify_project__214bf7673efe116b.py \
  --registry proofs/Agent101Multiplicity.registry.json \
  --project agent101-digit-split \
  --lean /absolute/path/to/lean-4.19.0-linux/bin/lean \
  --output /absolute/path/to/a-new-empty-build-directory
```

`local/`, `bounds/`, `enumeration/`, and `numeric/` preserve actual development
sources and logs. `reviews/` contains explicitly attributed independent review
records. `multiplicity_probe.py` and its output are an independent finite
control over all one- through five-digit positive integers; the Python results
are not substituted for Lean proofs.
