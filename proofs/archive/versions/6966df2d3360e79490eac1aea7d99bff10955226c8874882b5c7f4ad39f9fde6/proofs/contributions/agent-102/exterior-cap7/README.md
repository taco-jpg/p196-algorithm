# Complementary-band exterior graph at cap 7 (Agent #102)

Task `agent102-exterior-cap7`. **Evidence label: checked finite computation (not Lean).**

Object and conventions are exactly those of `agent101-exterior-cap56` (replicated in
`../review-agent101-cap56/`): the autonomous outer map `(c,B) -> (c',B',gamma)` of
`2026-10-15-complementary-bulk-quotient/METHOD_AND_PROOF.md` (3),(4),(6),(7) with the sec. 6 suffix
trim, on `c ∈ {2,4,…,16}`, `B` empty or `B[0] ∈ 1..18`, coefficients `0..18`, `B[last] ≠ c`,
`|B| ≤ cap`; an edge exits when `|B'| > cap`; exit time counts the leaving step.

## Result (cap 7)

| states | internal edges | exit edges | cycles | sharp max exit time |
|---:|---:|---:|---:|---:|
| 6,774,606,864 | 1,975,927,004 | 4,798,679,860 | **0** | **24** |

The maximum 24 is attained by exactly three states, all with `|B| ≤ 6`:
`c=4, B=(3,16,8,15,0)`, `c=4, B=(3,18,13,17,0)`, `c=4, B=(3,18,13,14,15,1)`; the best
`|B| = 7` start has exit time 23 (e.g. `c=8, B=(7,17,8,10,15,13,3)`). Their full paths, recomputed
with the independent Python map `../review-agent101-cap56/outer_ref.py`, are in
`sharp_paths_cap7.json`. Exit-time histogram: `cap7.out`. Run time 278 s on 2 cores, ~400 MB.

Sharp exit times by cap are now 4, 5, 7, 9, 15, 20, 21, 24 (caps 0–7); no extrapolation is made.

**Consequence (conditional on the written projection bridge, i.e. that gamma and the trimmed
`B'` depend only on `(c,B)`, which follows from the Lean-checked identity (8) of Agent #109 plus the
trim): every whole complementary-band quotient cycle has `|B| ≥ 8` at some step**, irrespective of
`A`, `C` and both gap lengths. Larger exteriors remain UNKNOWN. Nothing about 196 or Lychrel
existence follows.

## Method and validation

`outer_cap7.c` (`gcc -O2 -fopenmp -DCAP=7 outer_cap7.c`) keeps a one-byte memo for every `|B| ≤ 6`
state and recomputes `|B| = 7` states along each path. Phase 1 starts from every memo state
sequentially and marks on-stack memo states (revisit ⇒ abort as CYCLE); runs of consecutive
length-7 states are bounded by a hard guard of 2,000 steps (exceeding it aborts as a potential
cycle; it was never reached). Phase 2 starts from every `|B| = 7` state in parallel against the
read-only memo. A cycle consisting only of length-7 states would exceed the guard; a cycle through
a memo state would be caught by the on-stack mark. The run exited 0.

The same source compiled with `-DCAP=4,5,6` reproduces the fully memoized caps 4–6 exactly,
including the complete exit-time histograms (`validate_cap4.out` … `validate_cap6.out`; compare
`../review-agent101-cap56/cap5.out`, `cap6.out` and Agent #101's tables).
