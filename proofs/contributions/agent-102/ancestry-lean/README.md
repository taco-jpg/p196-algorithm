# Agent #102 — Lean formalization of maximal 0/18-run ancestry

Task: `agent102-ancestry-lean` (claim on branch `p196/coordination`, `proofs/coordination/tasks/agent102-ancestry-lean.json`).

**Status: LEAN-CHECKED, awaiting independent review.** Both modules compile under official
Lean 4.19.0 (commit 6caaee842e94, Std only) from an empty build directory (`clean_rebuild.log`).
Every exported theorem's transitive axioms are within `[propext, Classical.choice, Quot.sound]`;
no `sorry`, `admit`, `native_decide` or custom axiom. The only imported project source is the
accepted `proofs/research/continuation/LychrelDigitSums.lean` (SHA-256 `ca5f4652…dc0b57`).

Nothing here proves that a palindrome is reached, that 0/18 coefficients disappear from an orbit,
or anything about 196. It follows **one** ancestry; new runs can be born elsewhere.

## What is formalized

Words are the exact full symmetric column-sum words of the accepted module
`proofs/research/continuation/LychrelDigitSums.lean`: `q` with `FoldedDecimal.Admissible L q`, and the
actual successor `FoldedDecimal.nextColumns q L` of width `FoldedDecimal.nextWidth q L`
(by `OverflowCarryNormalization.iterPairs_representation` these are the pair-sum words of
consecutive integers of an ordinary orbit). The pair-word positions of `ABSORBING_CORE.md` are the
low half of this full word; the backward carry `beta_b` there is `carry q (L - b)` here.

`RunAncestry.descendant_step` (for `c = 0 ∨ c = 18`, `reset c = [c = 18]`, and
`MaximalRun q L c a b`, i.e. `[a,b)` is a maximal run of `c` with `b ≤ L`):

1. **Exact survival.** For every old run position `i ∈ [a,b)`,
   `nextColumns q L i = c ↔ i ∈ descendant`, where
   `descendant = [a + [carry q a ≠ reset c], b - [carry q (L-b) ≠ reset c])` without overflow and
   `[a+1, b)` with overflow. (The singleton case is included: the formula then gives an empty
   interval unless both carries equal `reset c`.)
2. **No expansion, no merging.** A nonempty descendant is a `MaximalRun` of `c` in the actual next
   word, at the actual next width.
3. **Length.** `a ≤ d.1`, `d.2 ≤ b`, and `(d.2 - d.1) + carry q L ≤ b - a`; i.e. the length drops by at
   least the overflow bit.

This is Section 2 of
`proofs/research/main_existence_attempt/continuation_pass/seam_persistence/followup_absorbing_core/ABSORBING_CORE.md`
(written proof + finite census there). Endpoint cases (`a = 0`, `b = L`, runs of 18 touching the
word ends, central/overlapping mirror runs) are covered by the hypotheses with no exclusions.
Along the way the proof derives that without overflow a maximal 0/18 run never touches either end
of the word.

## Extinction time of one ancestry (`AncestryExtinction.lean`)

`track q L c a b t` is the tracked descendant after `t` actual steps (state
`OverflowCarryNormalization.iterPairs q L t`). With `ψ = DecimalWidthGrowth.lowerPotential`:

* `track_invariant`: while nonempty, the tracked interval is a `MaximalRun` in the actual word at
  time `t`, and `length_t + (width_t - L) ≤ b - a` (each overflow costs at least one unit).
* `potential_telescope`: `t + ψ(p_t) + 4L ≤ ψ(p_0) + 4·width_t` (keeps the final potential term;
  sharper than the existing `width_lower_potential`).
* `survival_bound`: survival at `t` implies `t + ψ(p_t) ≤ 4(ell-1) + ψ(p_0)`, `ell = b - a`.
* `extinct_after` / `extinct_uniform`: the ancestry is empty at every `t ≥ 4·ell - 3 + ψ(p_0)`,
  in particular at every `t ≥ 4·ell + 1`; `track_empty_mono` shows emptiness persists.
* `orbit_ancestry_extinct`: the same statement started from an actual canonical integer `n`
  (`q = columnSum d L`), bundled with the fact that the tracked words are the exact column-sum words
  of `orbit n t`.

* `central_run_step` (ABSORBING_CORE.md sec. 3): for a maximal central run `[a, L-a)` of length
  `g`, the next central run has length exactly `g`, `g-2` (no overflow, according to the boundary
  carry) or `g-1` (overflow), and is again maximal; so no step lengthens a tracked central 0/18 band,
  for every exterior and overflow schedule.

This is the written corollary
`proofs/contributions/2026-10-15-ancestry-potential-bound/ANCESTRY_BOUND.md`, now kernel-checked
together with its ancestry dependency. Optimality of `4·ell + 1` is not claimed.

## Semantic control (not proof evidence)

`control.py` independently compares the descendant formula, exact survival set, maximality and
length bound with literal integer reverse-and-add for every distinct column-sum word of widths 1–6
(10,467 words, 4,484 maximal 0/18 runs): PASS (`control_result.json`). It checks that the formal
statement means what is intended; the Lean proof is the evidence.

Arithmetic kernels (`pair_eq_iff`, `neighbor_no_overflow`, `neighbor_overflow`) are checked by kernel
`decide` over the bounded digit/carry ranges, not by `native_decide`.

## Reproduce

```sh
LEAN=/path/to/lean-4.19.0-linux/bin/lean sh proofs/contributions/agent-102/ancestry-lean/check.sh /tmp/empty-dir
```

The official compiler was obtained directly from
`https://github.com/leanprover/lean4/releases/download/v4.19.0/lean-4.19.0-linux.tar.zst`
(SHA-256 `6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe`).
