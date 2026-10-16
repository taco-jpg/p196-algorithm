# Exact seven-step boundary return, connected to actual decimal dynamics

**Verification: PASS. Fresh Lean 4.19.0 compilation checks all 29 public
theorems; their transitive axioms are restricted to Lean's standard
`propext`, `Quot.sound`, and `Classical.choice`.**

This contribution formalizes the boundary mechanism described in
[`../2026-10-14-seven-step-reset/SEVEN_STEP_RESET.md`](../2026-10-14-seven-step-reset/SEVEN_STEP_RESET.md).
It checks both the finite control table and the connection to the complete
decimal pair word. The control bits are actual whole-word carries.

Let \((L_t,q_t)=\operatorname{iterPairs}(q,L,t)\), where the initial whole
word is admissible, \(L\ge6\), and its first three pair coefficients are
\((4,4,0)\). Define

\[
c_t=\operatorname{carry}(q_t,L_t-3).
\]

The exact seven-step boundary return criterion is

\[
(q_7(0),q_7(1),q_7(2))=(4,4,0)
\iff c_0=c_1=c_3=c_5=0\ \land\ c_6=1.
\]

The two remaining controls \(c_2,c_4\) may each be zero or one. On a return,
the boundary trace is exactly

| Time | First three pair coefficients |
|---:|---|
| 0 | `(4, 4, 0)` |
| 1 | `(8, 8, 0)` |
| 2 | `(16, 16, 0)` |
| 3 | `(7, 14, 7)` |
| 4 | `(15, 8, 15)` |
| 5 | `(6, 14, 14)` |
| 6 | `(13, 9, 9)` |
| 7 | `(4, 4, 0)` |

The seven actual final-carry bits are exactly `[0, 0, 1, 0, 1, 0, 1]`.
Consequently the whole width increases by exactly three.

## Why the finite table describes the whole word

[`BoundaryTransducer.lean`](BoundaryTransducer.lean) normalizes the three
lower coefficients with incoming carry zero and the reflected three upper
coefficients with incoming carry `c`. Its two output alignments distinguish
overflow from no overflow. All 128 Boolean control sequences are classified
using Lean kernel reduction (`decide`), with no `native_decide` and no
additional axioms. Its seven theorem declarations have empty axiom sets.

[`ActualBoundary.lean`](ActualBoundary.lean) proves the link to the original
`DecimalDigits.carry`, `DecimalDigits.output`, and `FoldedDecimal.nextColumns`.
It derives the upper three coefficient values from whole-word symmetry,
expands their actual carry recurrences, and proves that its Boolean control
is exactly the real carry entering the upper boundary. In the overflow
branch the real final carry is proved to equal one, so the extra leading
digit and shifted reflection are included exactly.

[`SevenStepOrbit.lean`](SevenStepOrbit.lean) composes this local equality along
`iterPairs`, retaining the actual controls and changing widths, then transfers
the finite return classification to the actual orbit. Its numeric bridge
provides a canonical representation of the seventh ordinary reverse-and-add
iterate with returned boundary and decimal length exactly `L + 3`.

Admissibility is imposed on the whole word, not on a separately normalized
middle block. Thus a representation `(4,4,0) ++ W ++ (0,4,4)` may retain zero
padding at the ends of `W`. No trimming or replacement of its actual incoming
carry is justified or performed by these theorems.

## Verification

With Lean 4.19.0 available, run from the repository root:

```bash
python -B proofs/contributions/2026-10-14-seven-step-formal/check.py \
  --lean /absolute/path/to/lean
```

The checker rebuilds the base decimal development and all three new modules
in an empty temporary directory. It checks the base source's exact SHA-256,
scans the new proof sources for forbidden proof shortcuts, generates an axiom
audit for every public theorem, and rejects any transitive axiom outside
`propext`, `Quot.sound`, and `Classical.choice`. The source hashes, module
results, and complete theorem axiom sets are recorded in
[`verification.json`](verification.json); compiler output is in
[`compile.log`](compile.log).

## Remaining obligation

The theorem is an exact finite **criterion**. It does not assert that every
whole word beginning `(4,4,0)` supplies the required carries, that the returned
middle has the same form as the starting middle, or that the seven-step return
can be repeated indefinitely. Proving those properties for a concrete family
requires additional whole-word carry and recurrence arguments. No infinite
safe orbit, decimal Lychrel existence, or P196 conclusion is claimed here.
The boundary return criterion alone also does not establish palindrome
avoidance during all seven intermediate steps.
