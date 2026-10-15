# Agent #102 — Lean formalization of maximal 0/18-run ancestry

Task: `agent102-ancestry-lean` (claim on branch `p196/coordination`, `proofs/coordination/tasks/agent102-ancestry-lean.json`).

**Status: WIP checkpoint.** `RunAncestry.descendant_step` compiles under official Lean 4.19.0
(commit 6caaee842e94, Std only) with axioms `[propext, Classical.choice, Quot.sound]`; no `sorry`,
`native_decide` or custom axiom. Not yet independently reviewed. The extinction-time corollary is
still in development.

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

Arithmetic kernels (`pair_eq_iff`, `neighbor_no_overflow`, `neighbor_overflow`) are checked by kernel
`decide` over the bounded digit/carry ranges, not by `native_decide`.

## Reproduce

```sh
LEAN=/path/to/lean-4.19.0-linux/bin/lean sh proofs/contributions/agent-102/ancestry-lean/check.sh /tmp/empty-dir
```

The official compiler was obtained directly from
`https://github.com/leanprover/lean4/releases/download/v4.19.0/lean-4.19.0-linux.tar.zst`
(SHA-256 `6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe`).
