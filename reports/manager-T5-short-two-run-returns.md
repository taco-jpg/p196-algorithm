# Manager — literal decimal two-run returns need at least eight steps

**Status: LEAN-VERIFIED necessary condition.**

Fix finite decimal blocks U, M, V 和 fixed digits x, y. Write the literal
least-significant-first family

\[
W(r)=U\mathbin{+\!+}x^r\mathbin{+\!+}M\mathbin{+\!+}y^r\mathbin{+\!+}V.
\]

If r>=5, S>0, both W(r) 和 W(r+S) are canonical decimal words, 和 P
ordinary reverse-and-add steps send the first integer to the second, then
**P>=8**. Fixed block widths are unrestricted. The theorem requires only
one such return. In particular it excludes every eventual universal
positive common-increment family with P<=7: choose any permitted r>=5.

The exact endpoint is
`P196.ManagerShortTwoRun.twoRun_positive_return_period_ge_eight`.
`eventual_twoRun_period_ge_eight` states the eventual universal consequence
with its quantifiers explicitly. This strengthens [PR #371](https://github.com/taco-jpg/p196-algorithm/pull/371)
without changing that proof or its r>=3, P>=5 statement.

## Proof and imported results

The earlier theorem gives 4*S<=P. If S>=2 this already gives P>=8. For
P<=7 with S>0, only S=1 和 P=5,6,7 remain after the earlier period-four
obstruction. The exact canonical width increase is therefore two.

At r>=5 the first five low digits belong to U or the first run, 和 the
first five high digits belong to V or the last run. Increasing r leaves
these ten outside digits unchanged, including when a fixed outer block
is empty. The first five pair-column sums consequently return. The new
lemmas `twoRun_low_digit_k`, `twoRun_high_digit_k`, 和
`twoRun_outer_columns_stable` prove this for arbitrary k<=r.

Existing `SevenColumnProjection.actual_forwardPrefix` projects every
actual word transition exactly, using the word's actual inner carry.
`PrefixCycleLift.advance` enumerates all possible next coefficients when
one further outside column is retained. The new `candidates` enumerator
uses this unchanged arithmetic, retaining each complete temporal list
of P+1 rows, including the repeated final row. It adds one column to
every phase at a time. `candidates_complete` proves that every bounded,
positive-head, closed prefix trace with the stated weight occurs in
the resulting catalog. It does not assume a primitive period or choose
one phase rotation.

For successive outer coefficients a,b define

\[
\gamma(a,b)=
\begin{cases}
1,&a\ge10\ \text{or}\ (a=9\ \text{and}\ b=10),\\
0,&\text{otherwise}.
\end{cases}
\]

The finite singleton-prefix identity 和 the existing actual prefix
projection prove `actual_headGamma`: this weight is the actual outer
carry, hence the actual one-step width increase. `actual_traceGain`
telescopes it along the genuine full-word orbit. Thus a numeric width
increase of two supplies exactly G=2, rather than an extra carry-word
assumption.

The exact kernel-checked catalogs are:

| P | One column | Two columns | Three columns | Four columns | Five columns |
|---|---:|---:|---:|---:|---:|
| 5 | 10 | 5 | 5 | 20 | **0** |
| 6 | 12 | 3 | **0** | — | — |
| 7 | 7 | **0** | — | — | — |

Counts are complete correlated temporal traces, with all starting phases.
Each stage rewrites the previous checked catalog to its explicit small
list before reducing the next stage. The three final empty-catalog
theorems have **no axioms**. The generic coverage proof 和 actual numeric
bridge use only permitted standard axioms. No independent phase marginals
are substituted for a temporal trace.

Finally `iterPairs_representation` 和 canonical uniqueness identify the
specified numeric endpoint with the exact iterated pair-word state.
`numeric_short_prefix_obstruction` therefore excludes P=5,6,7 for every
actual width-gain-two return of the five-column prefix. Composing this
with the literal family's prefix stability 和 the prior 4*S<=P bound
proves P>=8.

Imported sources are unchanged from baseline
`eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`, except for the explicitly
stacked #371 proof at `672d45a9045e02ba7a3ec5a5c1b99edfdb21de25`:

- [ActualPrefix.lean](https://github.com/taco-jpg/p196-algorithm/blob/eafbbbfd6b5b857597f95f68268c56dbd96b6bcb/lean/P196/Agent104P620Witness/ActualPrefix.lean): exact arbitrary-width prefix projection.
- [PrefixCycleLift/Checker.lean](https://github.com/taco-jpg/p196-algorithm/blob/eafbbbfd6b5b857597f95f68268c56dbd96b6bcb/lean/P196/PrefixCycleLift/Checker.lean): executable one-column extension 和 its completeness theorem.
- [WholeWordBridge.lean](https://github.com/taco-jpg/p196-algorithm/blob/eafbbbfd6b5b857597f95f68268c56dbd96b6bcb/lean/P196/Agent2SaturatedProfile/WholeWordBridge.lean): existing actual width bounds, prefix potential 和 saturation theorem.
- [ManagerTwoRunObstruction](https://github.com/taco-jpg/p196-algorithm/tree/672d45a9045e02ba7a3ec5a5c1b99edfdb21de25/lean/P196/ManagerTwoRunObstruction): canonical numeric transport, literal family definition 和 P>=5 theorem.

This is a new short-period specialization and a small correlated catalog,
not a new claim to the imported prefix arithmetic or saturation potential.

## Why the fifth column matters

At three columns there is a surviving P5,G2 cycle, up to rotation:

```
(1,4,4) -> (2,8,8) -> (4,16,17) -> (9,13,15) -> (10,3,10) -> (1,4,4)
```

Its overflow word is 00011. Its four compatible inner-carry words are
01000, 01001, 01010, 和 01011. All four are retained in the independent
audit; fixing one would leave a coverage gap.

For example the four-column temporal rows
`(1,4,4,5),(2,8,8,11),(4,16,17,3),(9,13,15,7),(10,3,10,13)`
survive with inner-carry word 11000. There are four distinct complete
four-column row orbits at this selected starting phase, or twelve states
when the compatible inner-carry words are retained separately. Every
fifth-column extension fails. These are projection witnesses, not actual
numeric cycles or Lychrel certificates.

The independent standard-library audit
`calculation/manager/short_two_run_audit.py` performs 13,718 ordinary
integer one-step controls, retains all four inner-carry words, checks all
19 fourth-column 和 361 fifth-column initial extensions with all 32
five-step input words, 和 independently regenerates every Lean catalog
literal. All comparisons pass both normally 和 under Python `-O`.
Each integer control realizes an individual prefix edge; this is not a
claim that all edges can be realized by one closed integer orbit.

As a necessary scope control, the existing actual return
770 -> 176176 after seven steps remains valid: its width gain is three,
so it does not satisfy G=2. No unweighted period-seven obstruction is
claimed.

## Exact scope

Canonical endpoints require genuine decimal digits, a positive leading
digit 和 the stated integer value. Low zero digits remain allowed.
Artificial leading-zero width padding cannot meet the hypotheses.
There is no assumption about intermediate template forms, intermediate
run lengths, reachability from 196, or palindrome avoidance.

The stronger single-return statement uses **r>=5**. The proof does not
replace this by r>=3 or r>=4. Eventual universal families may choose a
larger r, so they are fully covered. Conventional most-significant-first
tuples map to the stated least-significant-first form by reversing the
fixed blocks 和 exchanging the two runs.

This result does not prove a decimal Lychrel number, decide arbitrary
periods, exclude the original A120 coefficient quotient format, or
exclude Agent3's different signed multi-band format. The finite-prefix
survivors at P8 remain a necessary abstraction only; they provide no
certificate existence claim.

## Reproduction and trust boundary

The new registered result is `ManagerShortTwoRunReturns`, with four
modules 和 eight endpoints. The proof uses the unmodified Lean 4.19.0
compiler 和 matching v4.19.0 `lean4checker`. No custom axioms, native
decision procedure, runtime patch, or change to an imported checker is
introduced.

From the repository root, for the isolated delta stacked on #371:

```bash
python3 calculation/manager/short_two_run_audit.py
python3 -O calculation/manager/short_two_run_audit.py
LEAN_NUM_THREADS=1 python3 tools/verify.py --changed 672d45a9045e02ba7a3ec5a5c1b99edfdb21de25
```

The finite checks are theorem proofs evaluated by the kernel; the Python
audit is an independent computational cross-check. Source-rule validation,
all four changed modules, their independent kernel replay, 和 all eight
registered endpoint axioms are covered by the unchanged verification gate.

Direct one-core elaboration measurements for the final four proof sources:

| Module | Seconds | Process-family peak RSS upper bound (KiB) |
|---|---:|---:|
| `CycleRefinement` | 1.997 | 457,932 |
| `ActualTrace` | 3.383 | 763,860 |
| `TwoRunPeriodEight` | 5.088 | 786,388 |
| `ShortCatalog` | 103.985 | 3,587,148 |

The RSS measurement is the cumulative maximum of completed child processes,
so later entries are conservative upper bounds for that module. Every file
is below the repository's per-file 20-minute, 8-GB limit. The scoped campaign
change leaves README 和 RESULTS untouched; the new scope is recorded here
和 in the registry.
