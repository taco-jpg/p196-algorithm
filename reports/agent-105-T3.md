# Agent 105 — T3: four-coefficient center-prefix limits

## Result 和 scope

**PAPER PROOF:** the finite prefix system below safely overapproximates canonical
neutral-center dynamics at arbitrary center widths.

**COMPUTED:** retaining 2, 3, or 4 center coefficients, the prescribed carry 和
overflow streams, the shared inward carry across the retained block, 和 the
exact closed-length budget still permits explicit abstract cycles for:

* p11: `e=10100110011`, `g=11100010000`, one repetition, total trim 2;
* p12: `e=101010010101`, `g=100010001000`, two repetitions, total trim 3.

Repeating these abstract cycles covers every positive p11 repetition 和 every
positive even p12 repetition. The three documented p12 rotations follow by
cyclically reindexing the 24-step walk by 0, 4, or 8 steps.

This rules out an all-k exclusion **from this particular prefix relaxation
through depth 4**. It does 不 assert full center feasibility, a limitation of
every possible finite-prefix method, or a base-10 certificate. The unknown
interior coefficients are 不 required to agree from one edge to the next.
There is 没有 new Lean theorem.

## Sources 和 attribution

Baseline: `eafbbbfd6b5b857597f95f68268c56dbd96b6bcb`.
The exact arithmetic comes from [the mirror](../calculation/neutral_band_search.py)
和 [A120Template.lean](../lean/P196/Drafts/Agent120NeutralBandCalibration/A120Template.lean).
The [neutral-band README](../calculation/neutral_band/README.md) supplies the
driver words 和 the existing identity `2*sum(v)=sum(g)`.

[Agent 7's normalization](https://github.com/taco-jpg/p196-algorithm/pull/315)
和 [canonical quotient](https://github.com/taco-jpg/p196-algorithm/pull/326)
justify maximal paired-neutral stripping without losing an accepted cycle.
Those results retain their prior attribution.

The [Agent 105 claim](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6432823109)
crossed [Agent 117's earlier head-language claim](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6432820476).
The agreed [scope split](https://github.com/taco-jpg/p196-algorithm/issues/289#issuecomment-6432898605)
leaves the one-head existential language with Agent 117; this report publishes
the distinct deeper-prefix construction. Agent 105's independent one-head
calculation serves only as corroboration 和 is 不 a competing deliverable.

## Necessary prefix system

Fix base `b>=2`, neutral coefficient `h=b-1`, 和 prefix depth `r>=1`.
A legal closed center cycle consists of symmetric words with coefficients
`0..2h`. Empty or all-neutral centers cannot flip the incoming carry.
After canonical normalization its first coefficient differs from `h`.
Symmetry then gives the required incoming carry

`e = 1 if C[0]<h else 0`.

A **LONG** abstract state stores the first `r` coefficients of a center whose
length is at least `r`; its exact length 和 interior are forgotten. A **SHORT**
state stores a complete symmetric center of length below `r`. For a LONG
state `x`, compute

`L = norm_b(x,e).digits`,

`R = reverse(norm_b(reverse(x),a).digits)`,

where `a` ranges over the carry bits 0 和 1, retaining only choices whose
right-block normalization exits with `1-e`. A concrete center supplies its
actual carry entering the last `r` columns, so this relaxation preserves
every genuine edge, including overlapping prefix/suffix windows.

The first `r` raw successor coefficients are exactly

`q[i] = L[i]+R[i]` if `g=0`,

`q[0] = L[0]+h*e`, `q[i] = L[i]+R[i-1]` for `i>0` if `g=1`.

For `g=1`, `q[0]!=h`; thus maximal center trimming is zero. Otherwise let
`j<r` be the first position with `q[j]!=h`, if it exists. Maximal trimming
then forces `v=j`. A LONG target begins with `q[j:]`, followed by `j`
unobserved coefficients. The model admits every such completion consistent
with the next carry. This is the deliberate loss of interior information.

For a possible SHORT target `S`, require `len(S)+2j>=r` 和

`(S ++ h^j)[:r-j] = q[j:]`.

These are precisely the visible coefficients of the full raw word
`h^j ++ S ++ h^j`. If every observed raw coefficient is neutral, a valid
target requires `v>=r`; the model admits every compatible target 和 every
such cost within the supplied trim budget. SHORT source states use exact
full-word arithmetic.

**Soundness:** concrete normalization supplies `a`, so the computed `q`
matches the actual raw prefix. The first nonneutral coefficient fixes the
canonical trim count; the LONG, SHORT, 和 entirely-neutral-prefix cases above
都 include the actual target. Thus every concrete center cycle projects to
an abstract closed walk with its actual trim costs.

For a driver repeated `k` times, the search requires total cost
`sum(v)=k*sum(g)/2`, together with return to the starting abstract state.
Timeout gives `UNDECIDED_TIMEOUT`, never an absence claim.

## Computed abstract witnesses

| Driver | k | r | Phase-0 abstract states | Search calls | Total v | Starting prefix |
|---|---:|---:|---:|---:|---:|---|
| p11 | 1 | 2 | 180 | 1,499 | 2 | `[4,0]` |
| p11 | 1 | 3 | 3,267 | 18,473 | 2 | `[5,2,6]` |
| p11 | 1 | 4 | 61,920 | 361,008 | 2 | `[5,3,15,9]` |
| p12 | 2 | 2 | 180 | 8,385 | 3 | `[2,0]` |
| p12 | 2 | 3 | 3,267 | 15,072 | 3 | `[2,0,9]` |
| p12 | 2 | 4 | 61,920 | 335,831 | 3 | `[2,0,9,6]` |

These searches stop at a positive abstract witness; the table is **不** an
exhaustive cycle count. Witness states 都 have length `r` (LONG).

Complete r4 p11 walk; row `t` maps to the next row, with row 10 returning to 0:

| t | Prefix | e | g | Inward a | v |
|---:|---|---:|---:|---:|---:|
| 0 | `[5,3,15,9]` | 1 | 1 | 0 | 0 |
| 1 | `[15,8,9,5]` | 0 | 1 | 0 | 0 |
| 2 | `[5,14,17,14]` | 1 | 1 | 0 | 0 |
| 3 | `[15,10,13,13]` | 0 | 0 | 0 | 0 |
| 4 | `[11,2,8,7]` | 0 | 0 | 0 | 0 |
| 5 | `[2,5,16,14]` | 1 | 0 | 0 | 0 |
| 6 | `[5,11,13,9]` | 1 | 1 | 0 | 0 |
| 7 | `[15,7,6,3]` | 0 | 0 | 1 | 0 |
| 8 | `[10,15,12,7]` | 0 | 0 | 0 | 0 |
| 9 | `[1,12,5,15]` | 1 | 0 | 1 | 0 |
| 10 | `[4,4,12,11]` | 1 | 0 | 0 | 2 |

At phase 10 the raw prefix is `[9,9,5,3]`; stripping 2 pairs retains `[5,3]`
和 admits the unobserved completion `[15,9]`. For p12 r4, the only trims are
`v[2]=v[11]=v[13]=1`; complete 24-edge prefix/carry data are printed by the
command below. Their raw prefixes are respectively `[9,13,9,3]`,
`[9,4,8,2]`, 和 `[9,6,1,9]`.

Both abstract walks also admit positive numerical length schedules:
starting at `m0=12`, use `m[t+1]=m[t]+g[t]-2v[t]`. The p11 schedule stays in
12..16; p12 stays in 10..13. Thus the witnesses do 不 depend on short-center
or overlapping-window cases. This does 不 supply consistent interior words.

## Reproduction 和 validation

From the repository root:

```bash
python3 calculation/agent-105/prefix_budget.py --selftest
python3 calculation/agent-105/prefix_budget.py --depth 4 --seconds 30
python3 calculation/agent-105/prefix_budget.py --depth 4 --e 101010010101 --g 100010001000 --repetitions 2 --seconds 30
python3 tools/verify.py --changed
```

Replace `--depth 4` by 2 or 3 to reproduce the other rows. The p11 和 p12
commands completed with `ABSTRACT_BUDGET_WITNESS`, periods 11 和 24, trim
totals 2 和 3. Runs are single-process, seconds-scale, with a 30-second cap.

Selftest output:

```text
{"mirror_projection_checks": 38770, "status": "PASS"}
```

These seeded checks cover bases 2,3,4,5,10,11,17,26 和 depths 1..4. Each test
constructs an exterior realizing the prescribed carry/overflow pair, compares
independently coded center arithmetic against the repository mirror, 和 checks
that the actual edge projects correctly, including shorter centers.

`verify_witness()` independently replays emitted LONG witnesses using separate
digit/carry loops, without the transition generator or its normalization
helper. An additional independent review replayed the 35 r4 witness edges
from literal column equations 和 checked their length schedules.

The repository gate returned `ALL CHECKS PASSED (changed files only, against
origin/main)`: 5,217 Lean files / 301 projects satisfy repository rules;
0 Lean modules changed, built, or axiom-audited. This validates the repository
change scope, **不** a new kernel proof of the paper reduction.

## Next concrete question

Can the newly exposed prefix coefficients at a trim be constrained jointly
with the forgotten inward carry by extending the source window through the
trimmed positions? The present model treats those completions independently.
An exact one-edge extension or a longer temporal interior constraint could
eliminate these abstract loops; the current result makes no claim about that
stronger model.
