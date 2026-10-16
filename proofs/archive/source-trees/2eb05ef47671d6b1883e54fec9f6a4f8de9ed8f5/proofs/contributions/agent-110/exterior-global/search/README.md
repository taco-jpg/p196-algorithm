# Fixed-width, phase-padded exterior cycle search

This is a new bounded-period **exterior-only** search. It does not alter the
frozen `../RadixExterior.lean` result. It does not encode the full complementary
template state `(c,B,A,C)`, two gap gains, or an accepted return certificate.
In particular, a six-phase exterior return can have an odd overflow count
divisible by nine; the stronger divisibility by eighteen established for a
full admissible certificate must not be imposed here.

No exterior cycle has been found. Solver UNSAT responses below are retained
as **uncertified solver outcomes**, not Lean results or all-width exclusions.
Every time cap remains UNKNOWN. The new search uses one CaDiCaL process at a
time, with individual wall limits of 10 or 15 seconds.

## Prior-work check and parameter choices

The search was selected after inspecting:

- Agent 8's `explore.py`: 144 specified small starts, a forward-orbit width
  cap of 200 and time cap 1000; all recorded starts hit caps. This was not a
  fixed-period SAT encoding.
- Agents 101/102/103: complete exterior graphs only through canonical width
  seven. Here every run requires an exterior of **exact maximum width W** at
  some time, starting with W=8, so the solver is not asked to repeat those
  smaller-width domains.
- `proofs/research/exist_uniform_notes.txt`, sections 2–4: equality
  `P=2H` forces the three-outer-coefficient eight-cycle; the complete
  period-24/gain-9 spatial-graph obstruction covers all exterior widths.
  Accordingly P18/H9 and P24/H9 were skipped. P36/H18 was also skipped,
  because its equality case has P not divisible by eight. These prior results
  retain their published written/certificate scope; this package did not
  rebuild them.
- The newly completed certificate arithmetic is distinct: its additional
  factor two in H uses the **full two-gap** returned width identity. It does
  not eliminate the exterior-only P30/H9 or P36/H9 probes.

The retained `summary.json` and per-case `result.json` give the exact completed
matrix and times. The selected cases are two-phase c=6 with
`(W,P)=(8,4),(8,8),(8,10),(8,12),(12,16)`, and six-phase c=2 with
`(W,P,H)=(8,30,9),(8,42,18),(8,36,9)`.

## Exact encoded domain

Each state is a row `B[t,0..W-1]` of coefficients in 0..18, whose first
coefficient is positive. Its phase is fixed by

`c[t+1] = 2*(c[t] - 9*[c[t]>=10])`.

The temporal row after P transitions is identified with row zero. Thus the
period divides P; no primitive-period claim is made. At least one actual
overflow is required. If H is supplied, it is the exact sum of the computed
overflow bits. A clause requires some row's last coefficient to differ from
that row's phase, making the maximum canonical width exactly W.

Rows are padded representations: a canonical exterior of length b≤W is
represented by its word followed by `W-b` copies of its phase. The padding is
not discarded arbitrarily. Each raw successor has W+1 coefficients; its last
coefficient is explicitly constrained to equal the next phase, and only then
are its first W coefficients used as the next row.

For clarity, the reduction follows directly from carry reset. For a phase
`c≠9`, let `k=[c≥10]`, `t=c-9k` and `c'=2t`. Appending m copies of c to an
exterior appends m copies of c' to its raw successor: the first c accepts the
previous carry, every later c resets to k, and reverse normalization enters
the appended run with k. The normalized additions therefore agree with the
original raw exterior followed by `c'^m`. The condition on the last raw
coefficient is equivalent to the canonical successor having length ≤W.
This explains the padded representation; no new formal padding theorem is
claimed here, and Agent 116's separately owned canonical-projection work is
not duplicated.

## Carry equations and CNF

For each row, low-side carries `l[0..W]` and high-side carries `r[0..W]`
are Boolean, with `l[0]=0` and `r[W]=k`. Low digit `D[j]` and aligned high
digit `E[j]` satisfy exactly

```
B[j]+l[j]   = D[j]+10*l[j+1]
B[j]+r[j+1] = E[j]+10*r[j]
gamma = r[0].
```

Coefficient and digit variables use one-hot encodings; the complete input
tables force the quotient and remainder, so the carries are not free labels.
For gamma=0, the raw prefix is `D[j]+E[j]` and its last value is
`c+l[W]-10k+t`. For gamma=1, the raw prefix is
`D[0]+1, D[1]+E[0], ..., D[W-1]+E[W-2]` and its last value is
`c+l[W]-10k+E[W-1]`. Each last value must be c'.

`encode.py` builds this relation. `check_encoding.py` independently assigns
ordinary arithmetic outputs and evaluates **every generated clause** on 2,600
finite one-step cases: 810 valid tails and 1,790 failed tails, including 1,356
overflows and 1,244 nonoverflows. Valid-tail cases also verify normalization
and reject a deliberately changed successor. This is finite encoding QA,
not a kernel proof of the complete reduction.

`reference-controls.json` records 48 direct comparisons with the existing
Agent 8 `outer_step`, including its exact source hash. Every future SAT model
must first satisfy all emitted clauses, then replay the maximally trimmed
cycle under both the implementation here and that unchanged reference map.
A positive candidate would still need a separate Lean kernel certificate
before being promoted to a proved exterior cycle. No such candidate exists
among these results.

## Reproduction and retained raw evidence

CaDiCaL 2.1.3 was available in the official Lean 4.19.0 distribution. Its
binary hash is in each case's metadata and `reference-controls.json`.
No Z3 installation was present or attempted.

```sh
python3 proofs/contributions/agent-110/exterior-global/search/check_encoding.py
python3 proofs/contributions/agent-110/exterior-global/search/run_search.py \
  --solver /absolute/path/to/cadical --phase 2 --width 8 --period 42 \
  --overflows 18 --seconds 15 --full-width --name fresh-c2-w8-p42-h18
```

Use a new case name. Each directory retains compressed exact DIMACS bytes,
complete solver output, parameter/variable metadata, source hashes and a
snapshot of the exact generator. Initial cases preceded the addition of the
explicit metadata fields explaining exterior-only scope; the domain and
scope are identical. `generator-v1.py` preserves their original generator.
Later generator changes added only an open-transition QA mode and variable
metadata, without changing the cyclic formulas.

No proof trace was requested, so UNSAT remains `SOLVER_UNSAT_UNCERTIFIED`.
Incomplete or timed-out work is not a nonexistence result. These eight
carefully bounded probes are not an exhaustive search over widths, periods,
overflow schedules, full interfaces, or ordinary reverse-and-add orbits.
