# Moving-front attempt: exact current criterion excluded

No finite decimal Lychrel seed or safe inductive finite family was obtained.
The main existence problem remains unproved. **Independent audit now proves
that the exact finite-window potential criterion in this folder is
inconsistent for every K and p.** Its conditional existence implication is
sound but vacuous, not merely uninstantiated. The separate free-clock
finite-family SMT queries at spatial periods five and seven remain UNKNOWN.
All processes have stopped; no new searches were run for this correction.

This attempt allowed a growing, nonperiodic wake instead of extending the
fixed-width 936 search. Its information-discarding local update nevertheless
has an unavoidable speed deficit, proved below.

`CONDITIONAL_FRONT_THEOREM.md` now leads with the all-K obstruction and
preserves the original finite-certificate implication and seed recipe as a
historical, vacuous implication. `INDEPENDENT_CRITERION_AUDIT.txt` contains
the independent source-reading and mathematical audit. The correction was
also checked directly against the `suffix_step` operation and the saved
cycle edges; no new search was required.

## All-K obstruction, superseding the potential search question

Let s_v and s_u be the old and new retained suffix lengths. The known
window begins at b=j-s_v. The implementation starts known output at b+h,
removes a matching periodic tail, and retains only the final K known
coefficients. If D>=0 coefficients are discarded from the left by that
cutoff, then exactly

    b'=b+h+D,
    Delta-s_u+s_v=h+D.

The identity holds for an empty suffix too. It follows directly from
`ns=start+h`, `newcut=ns+len(out)`, and `out=out[-K:]` after tail trimming.
For every directed cycle, suffix lengths telescope and give

    sum(2*Delta-h)=sum(h)+2*sum(D) >= sum(h).

The upper potential would require this sum to be at most zero. Hence no
cycle containing an overflow is possible. Finite nonempty closure under
both overflow choices forces an all-overflow cycle; closure under the
alternating clock likewise forces a cycle with overflows. Both contradict
the upper potential, independently of K, p, motif, safety, or center data.
The lower potential cannot help and is in fact unnecessary for physical
containment, since b_t>=b_0+H_t already.

Thus increasing K or completing a capped graph cannot produce this exact
certificate. The raw capped/transient/complete statuses below remain
historical execution results, while the model-level potential criterion
is now structurally excluded. This does not exclude a redesigned local
operation that recovers earlier known columns, correlated wake languages,
arbitrary moving boundaries, or decimal Lychrel numbers.

## Historical induction target

Let a periodic, nonneutral pair-sum row be B_t, with temporal phase t, and let
h_t be its overflow flag. "Nonneutral" here means that some coefficient of
B_t differs from 9. Each directional carry in the periodic row is then fixed
by the nearest non-9 coefficient in that direction.

At an inward cut j, retain a known suffix S immediately before the periodic
region. Its length is at most K. All earlier coefficients are arbitrary. Thus

    arbitrary wake | S | B_t B_t B_t ...

is an actual infinite collection of possible wake words, not one fixed
boundary. The suffix's starting index is j-|S|. The reference B_t is indexed
by absolute index modulo its spatial period p; this alignment is part of the
state. A finite graph state is

    (temporal phase, j modulo p, S).

To update one state, branch over both possible low carries entering S. The
high carry comes from the exact periodic tail. On an overflow, omit the
first output position, whose delayed high digit is outside the known window.
This omission moves the start of the known window one position inward.
Append two complete periodic blocks before computing the update; they reset
the low carry and cover the delayed high digit. Remove every matching tail
symbol at the right and retain at most the last K remaining suffix symbols.
If the entire known window matches the tail, an empty suffix is retained.
The next step can again branch over its entering low carry. No unknown wake
coefficient is silently assumed.

This produces an exact conservative transition with integer cut displacement
Delta=j'-j. Every real finite integer whose known window is separated from
its center by a complete nonneutral block follows one of these transitions.
The omitted left wake can change arbitrarily; a restricted actual wake may
follow only a small subset of the graph's paths.

Let H_t be the number of overflows so far. The doubled center coordinate of
a real symmetric q word increases by H_t. The relevant edge weight is

    w = 2*Delta - h.

Consequently

    2*j_t - H_t = 2*j_0 + sum(w along the path).

If a finite reachable graph admits integer labels R with

    w(u,v) <= R(v)-R(u),

then every path's accumulated weight is bounded above by max R-min R.
A sufficiently large initial separation from the center would therefore
remain positive at every time. The inequality is a finite potential
condition that would bound a growing wake. However, the all-K obstruction
proves that this operation cannot satisfy it when finite closure forces an
overflow cycle, as both-overflow and alternating-clock closure do.
The proposed induction target is therefore vacuous in this exact model.

To turn this condition into a finite Lychrel construction one must also
supply the actual overflow clock, compatible finite center geometry, safety
at every phase, and enough distance from the physical outside endpoint for
the retained local window. A reference bulk and a fitted speed do not supply
those obligations. No instance can satisfy the potential condition for the
exact both-overflow or alternating-clock closure, regardless of the other
obligations. Those
additional obligations do not repair the structural contradiction.

## Exact search and its limits

`front_language.py` implements the local transition and a complete reachable
graph search, with a 6,000-state cap per query. Bellman-Ford is used only to
search for an integer potential; every negative result carries an explicit
positive-weight cycle whose edge arithmetic can be replayed. A positive
cycle need not be a globally realizable finite integer orbit.
The independent structural audit explains why a positive cycle is
unavoidable in every complete finite graph under this update and clock.

The fixed clock in these local graph queries is N,O repeated. The pool has
51 written motifs: two primitive period-three controls, one period-four
control, 45 primitive period-five motifs, and three uniform motifs written
at length five. The period-five pool was generated from a reproducibly seeded
sample of reflection-shaped motifs, then advanced to recurrent bulk states.
It is not a complete period-five catalog. The phase check rejects a motif if
it has a transient when restarted in the supplied phase.

For K=1,2,3 and the listed one-coefficient initial profiles there were 1,146
queries:

| Outcome | Count | Meaning |
|---|---:|---|
| Complete local graph with a positive-weight cycle | 561 | The universal-carry potential fails for this model |
| 6,000-state cap | 516 | UNKNOWN |
| Restarted bulk has a transient | 69 | No query to a recurrent graph was accepted |

No query supplied a bounded-motion potential. The later structural proof
excludes that exact potential criterion for every retained-window bound,
spatial period, and finite closure that forces an overflow cycle. The
bounded computations
alone did not prove that fact. Correlated wake languages with a different
information update, other moving-boundary constructions, and decimal
Lychrel existence remain outside the exclusion.

The earlier half-infinite exploration in `moving_front.py` derives the
actual exterior overflow from its prefix, rather than imposing it. Its 35
short probes do not preserve the proposed alternating clock, and the tested
nonneutral trajectories penetrate farther inward relative to center growth.
Some period-four tails become all 9 and are stopped explicitly, because a
purely periodic all-9 tail has nonunique directional carries. These are
finite discovery observations, not all-time speed claims.

## Independent arithmetic checks

The half-infinite engine passed 3,506 ordinary-integer comparisons. The
moving local-window engine separately passed 996 ordinary-integer controls;
four all-9 input tails were skipped explicitly.

`audit_front_cycles.py` imports none of the transition, carry, graph, or
potential code. For every saved cycle edge it constructs an actual positive
finite integer by splitting a symmetric q word into decimal digits. A leading
q coefficient 8 or 17 forces the requested N or O step. An independently
chosen reset coefficient immediately before the known suffix forces either
incoming low carry. Two different finite tail lengths are used, and the
output is computed by literal decimal reversal and addition.

The audit passes all 561 cycles, with 17,606 cycle edges. It covers 35,212
edge/parameter instances; caching reduces these to 16,226 distinct ordinary
integer edge calculations (8,113 distinct local edges, two tail lengths).
Another 654 independent integer calculations reconstruct the periodic bulk
updates. Each cycle's exact summed weight is positive. The audit checks the
saved cycles' arithmetic; it does not independently reconstruct the entire
reachable graph or certify that a cycle's arbitrary carry history comes from
one persistent finite exterior.

The all-length justification for a local edge is the nonneutral carry-reset
argument above: increasing the repeated tail by any complete blocks leaves
the two interface carries and all known output coefficients unchanged. The
finite numeric controls audit the implementation; they are not substituted
for that general locality argument.

`criterion_obstruction_check.json` records the correction's consistency
replay over the already saved data: all 17,606 edges satisfy
Delta-|S_u|+|S_v|-h>=0, and all 561 cycle weights equal H+2*sum(D).
The summed discarded-column count is 1,911; the largest single-edge D is 3.
This uses no new graph search. The all-K result is the source-level algebra,
not extrapolation from those saved edges.

## Separate direct search for an actual finite return

`finite_pump_probe.py` reuses the established exact all-length carry and
center encoding in `exist_geom_periodic_qpump.py`. Its family has a finite
exterior E_t and a reflection-compatible repeated p-symbol interior. All
exterior coefficients, interior coefficients, and overflow flags are unknown
solver variables. Thus these were direct positive finite-family synthesis
queries, with no preselected 936 tail or alternating clock.

| Temporal period | Spatial period | Total digit growth | Exterior width | Result |
|---:|---:|---:|---:|---|
| 28 | 5 | 10 | 20 | UNKNOWN (5-second solver limit) |
| 30 | 5 | 10 | 20 | UNKNOWN (5-second solver limit) |
| 40 | 7 | 14 | 20 | UNKNOWN (5-second solver limit) |

No UNSAT statement, witness, or all-time conclusion follows from these
queries. No candidate was available for an independent symbolic family audit.
The recorded elapsed times include encoding and are slightly longer than the
solver limits. The runtime dependency is `z3-solver`; it is not bundled here.

Historical reproduction from this directory (the excluded local search
is retained for provenance, not as an open construction target):

```sh
python3 moving_front.py
python3 front_language.py
python3 audit_front_cycles.py
python3 finite_pump_probe.py
```

The first three commands use the Python standard library. The fourth requires
`z3-solver` and uses the pre-existing archive-root exact pump encoding. None
of these searches or supporting checks is a Lean existence theorem.
