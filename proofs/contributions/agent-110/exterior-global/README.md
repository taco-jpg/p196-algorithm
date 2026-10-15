# Ordered radix defects of the complementary exterior

This package proves an obstruction to a particular global strategy, using the
**unchanged exact exterior map** `P196.Agent6.advance`. It does not prove global
exterior acyclicity, exhibit an exterior cycle, or prove anything about 196.

The task is `agent110-exterior-global-cycle`, authorized on coordination commit
`7091843ad812657e7be29e2cd0f4d2fef4f340df`. The source baseline is main
`eec3d5f3646cab50abad6e610ea19626cd249070`. Agent 116 owns the separate
return-certificate/canonical-exterior projection task; this package does not
implement or claim that task.

## Result

For an exterior state `(c,B)`, with the first list entry the outermost
coefficient, define

\[
 Z(c,B)=9\sum_{i=0}^{|B|-1}B_i10^i-c(10^{|B|}-1).
\]

This quantity retains spatial order and is unchanged when any number of phase
letters `c` are appended to `B`. `centeredValue_formula` and
`observation_append_phase` prove these statements for every finite word.

The exact map has the following contiguous orbit segment. All six states
satisfy the existing `P196.Agent6.Canonical` predicate.

| Time | Phase | Exterior word, outside first | Z | Overflow on next step |
|---:|---:|---|---:|---:|
| 0 | 6 | `[13]` | 63 | 1 |
| 1 | 12 | `[4,10]` | -252 | 0 |
| 2 | 6 | `[9,1]` | -423 | 0 |
| 3 | 12 | `[18,2]` | -846 | 1 |
| 4 | 6 | `[9,11,5]` | -423 | 1 |
| 5 | 12 | `[10,1,7,11]` | -14508 | — |

Times 2 and 4 have identical `(c,Z)` but different words. Their next
observations differ: `(12,-846)` versus `(12,-14508)`. Thus:

1. No deterministic update function on `(c,Z)` represents every exact exterior
   step, even restricted to canonical states reached after a genuine overflow.
2. No potential depending only on `(c,Z)` can be nondecreasing on every such
   step and strictly increasing whenever the actual overflow is one. The
   two-step path from time 2 to time 4 contains one real overflow and returns
   its observed value. The formal statement permits an arbitrary target type
   and relations satisfying mixed transitivity and strict irreflexivity;
   an integer-valued corollary is also supplied.

This is different from the existing reversal-invariant and parity-permutation
obstructions: the present observable distinguishes `[1,5]` from `[5,1]`.
The two equal observations above arise from decimal carry equivalence, with
different word lengths, rather than a permutation of the same coefficients.

## Exact theorem interface

All new declarations are in namespace `Agent110.RadixExterior` in
`RadixExterior.lean`.

- `no_autonomous_radix_factor`: for any `F : (Nat × Int) → (Nat × Int)`,
  assuming `observation (advance s) = F (observation s)` for every canonical
  `ReachedAfterOverflow s` gives `False`.
- `no_overflow_strict_radix_observable`: for any target type, observation
  function `P`, weak and strict relations, mixed transitivity, and strict
  irreflexivity, the stated universal weak-progress and actual-overflow
  strict-progress assumptions give `False`.
- `no_overflow_strict_radix_potential`: the same with integer-valued
  `P : Nat → Int → Int`, ordinary `≤` and `<`.
- `witness_path`, `witness_overflows`, `witness_canonical`,
  `witness_after_overflow`, `witness_observation_return`,
  `witness_not_state_return`, and `witness_nonautonomy` expose every premise
  used in the argument. Exact finite equalities use ordinary kernel `decide`.

`ReachedAfterOverflow` means an actual finite iterate after the successor of a
canonical state whose **computed** overflow is one. It is not a freely chosen
overflow schedule. Its source map and canonical predicate are imported from
the existing Agent 6 sources. No ordinary-integer soundness theorem is newly
claimed here; the prior exact exterior bridge supplies that broader context.

## Reproduction and evidence

From the repository root, with an absolute official Lean 4.19.0 executable
(release commit `6caaee842e94`) and a nonexistent output directory:

```sh
python3 proofs/contributions/agent-110/exterior-global/check.py "$LEAN_BIN" \
  --evidence /tmp/p196-radix-exterior-clean
python3 proofs/contributions/agent-110/exterior-global/literal_check.py
```

The first command copies and recompiles all three unmodified source
dependencies plus the new module in a new directory, then queries the
transitive axioms of every new theorem. `evidence/final-clean/verification.json`
is the accepted author-run receipt, including source and log hashes. This is
not an independent review. The dependency `ExteriorCapTwo` is compiled because
the existing `Canonical` declaration is in `ExteriorCoverage`; the proof above
does not use cap-two enumeration.

The separate literal checker uses ordinary Python integer addition and decimal
reversal. It realizes the finite segment with three initial constant-core
lengths, including an odd length, and checks 15 actual additions. Full integers,
pair words through their asserted templates, exact overflow counts, and
observations are retained in `evidence/literal_controls.json`. These are finite
semantic controls, not a claim of a persistent or safe family.

`evidence/attempt-01` retains the first successful four-module compilation and
all 14 initial axiom outputs. Its receipt remains `INCOMPLETE`: the first
checker parser did not count Lean's separate “does not depend on any axioms”
output form. The corrected parser and the added exact radix formula are
covered by the later complete fresh run. No incomplete receipt is relabeled.

## Remaining global question

The actual open proposition is

```lean
∀ s : P196.Agent6.Exterior, P196.Agent6.Canonical s →
  ∀ p : Nat, 0 < p → P196.Agent6.iterate p s ≠ s
```

It remains **WIP/UNKNOWN**. The observed two-step return is explicitly not a
state return. This package rules out one spatially ordered quotient and its
specified potentials; it does not rule out other ordered observables,
nonmonotone arguments, more detailed carry memory, or longer-block methods.

Research choices, rejected guesses, and the small exact discovery procedure
are retained in `RESEARCH.md` and `development/`.
