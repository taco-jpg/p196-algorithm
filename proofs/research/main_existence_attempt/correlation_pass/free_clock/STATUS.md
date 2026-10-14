# Free-clock synthesis and exact prefix-extension checks

No finite decimal Lychrel witness or safe closed family was obtained. This
branch generates candidate clocks from the actual outside-column arithmetic,
then attempts to connect them to a periodic interior. It does not assume an
alternating clock at discovery time. The strongest remaining candidate has
spatial period five and an alternating temporal clock; its full boundary
problem remains **UNKNOWN**.

## Candidate generation and all-length local equations

A state contains a finite outside pair-sum prefix P, a nonconstant periodic
bulk Q of spatial period r, and the core length modulo 2r. The full intended
word is P followed by that periodic core and reverse(P). Its reflection and
odd-center parity are checked at every phase. For a nonneutral bulk, the
nearest non-9 coefficient in each direction determines the corresponding
incoming carry. Thus its local update is exact independent of the number
of complete bulk periods, away from the unproved interface.

The outside prefix is normalized with low incoming carry zero and both
possible incoming high carries e in {0,1}. The high carry leaving its first
column determines the actual overflow h; it is not a free independent bit.
If l_i and u_i are the two resulting digits, the new outside coefficients
are l_i+u_i for h=0, and l_0+1, l_i+u_(i-1) for h=1. The bulk uses the same
h. Returning prefix/bulk/residue states supply candidate cycles, not a
connection between their unspecified interface carries.

The reproducibly seeded search yielded:

| Spatial period | Retained outside columns | Trials | Distinct candidate cycles |
|---|---:|---:|---:|
| 5 | 1 | 100,000 | 10 |
| 7 | 1 | 40,000 | 0 |
| 5 | 4 | 100,000 | 3 |

Each walk was limited to 1,000 steps and saved cycles to period at most 100.
These are samples, not exhaustive catalogs. The one-column period-five
cycles have temporal periods 20,22,24,26,28,30, each with gain 10. The three
four-column cycles have (period,gain)=(40,20),(48,20),(94,40).

The implementation was controlled by 14,400 ordinary-integer prefix cases
and 4,418 periodic-bulk cases, checking 109,211 interior positions. These
all pass. The carry-reset argument above, not those finite tests, supplies
the arbitrary-length interpretation.

## An exact one-column extension obstruction

For a prescribed periodic prefix P_t and overflow h_t, enumerate e_t=0,1
and retain those values producing exactly P_(t+1). Let a_t be the low carry
leaving P_t. The next unknown coefficient q_t is in 0,...,18; let v_t in
{0,1} be its high carry from farther inside. Necessarily

    e_t = floor((q_t+v_t)/10),
    q_(t+1) = (q_t+a_t) mod 10 +
      ((q_t+v_t) mod 10                         if h_t=0,
       (last(P_t)+e_t) mod 10                   if h_t=1).

For each phase this is a complete necessary relation on 19 coefficients,
including every choice of the deeper carry. Compose these relations over
one prescribed prefix period. Every actual extension supplies a path in
this 19-state macro graph. An infinite extension supplies an infinite path.

The checker repeatedly deletes sinks and assigns a rank strictly decreasing
on each remaining edge into deleted vertices. If all 19 vertices receive
ranks, no infinite extension is possible, regardless of the temporal
behavior of the deeper columns. This includes all temporal multiples and
aperiodic interiors; it is not restricted to equal-period extensions.

For one-column candidates 3 through 9, and four-column candidates 1 and 2,
the macro relation is actually empty. Those nine prescribed prefix
schedules cannot persist for even one complete cycle when an additional
column exists. The conclusion uses neither a SAT solver nor sampled
trajectories. The remaining four candidates are not excluded by this
test. `prefix_extension_audit.json` retains every 19-state relation and rank.

This is an exclusion of the explicitly listed prefix schedules. It does
not exclude free clocks, different prefixes, all period-five cores, or
Lychrel numbers. For a statement about an entire infinite orbit, sufficiently
large width supplies the additional column; for the proposed all-length
families it is present directly.

## Attempts to supply a complete boundary

The ten one-column candidates were substituted into the previously retained
exact all-length QF_BV encoding, with exterior width 32 and a 12-second
solver limit per instance. There were two solver-reported UNSAT results
(candidates 3 and 9) and eight UNKNOWN timeouts. No independently checked
SAT/UNSAT certificate is claimed from those solver statuses. The elementary
extension argument above is stronger for seven of these candidates.

Direct reverse column search for the three four-column candidates reached
the 50,000-predecessor cap at its first state. All three results are UNKNOWN.
An implementation bug that could mislabel a truncated final queue as complete
was corrected before publication and the searches rerun. The published
`transfer_cycles_p5_k4.json` records the corrected UNKNOWN outcomes only.

For the surviving four-column alternating candidate, the initial bulk is
(10,3,4,3,10), with 40 ordinary steps and total gain 20. The exact cyclic
inverse-language construction retains every temporal repetition of this
bulk/clock, rather than enumerating each fixed temporal power separately.
Its outer target is the alternating 8,17 column.

| Representation | Last completed inverse depth | Vertices | Edges | Stop |
|---|---:|---:|---:|---|
| Uncompressed | 8 | 9,956 | 55,228 | 300,000 raw graph cap |
| Forward bisimulation | 13 | 19,062 | 110,762 | 1,000,000 raw graph cap |
| Alternating forward/reverse bisimulation | 16 | 16,039 | 104,091 | 1,000,000 raw graph cap |

Every completed graph has no uniform outer-root cycle. No graph recurrence
or all-depth invariant was obtained. These are construction-search results,
not an independently replayed all-width exclusion. The caps remain UNKNOWN.
The original 32-column SMT timeouts likewise remain UNKNOWN.

## Why the graph quotients retain the relevant temporal correlations

The compression reuses the power-preserving bisimulation idea already
present in `boundary_resume/reverse525/`, applied here to a new spatial-
period-five candidate. It is not claimed as a new general automata theorem.

A strong forward-bisimulation quotient can introduce a closed walk labeled
w without a single original walk with exactly that period. It nevertheless
preserves the existence of a closed walk labeled w^k for some k>=1. Fix a
quotient w-cycle and lift a complete w block from every representative of
its starting class. Each lift returns to that class. Choosing lifts defines
a map on a finite set, whose cycle yields a walk labeled exactly w^k.
Sampling at full-block boundaries avoids any rotation issue. Projection
proves the converse. Reversing all edges gives the same result for reverse
bisimulation, and consecutive applications preserve the equivalence.

The spatial inverse relation is local and invariant under repeating the
complete cyclic option sequence. Thus lifting to a power repeats both old
and new labels and preserves its validity. Repeated inverse construction
and quotienting preserve periodic-trace existence at every completed depth.
A reconstructed positive boundary would have to repeat all previously
decoded columns whenever a lift enlarges the period. No root was found here.

The statement concerns a uniform-root cycle anywhere in the graph. It does
not claim a cycle through a designated original vertex, or exact-period
language equivalence. A complete all-depth exclusion would still require
a checked recurrence/fixpoint and checks of every preceding depth.

## Reproduction

From the project root, with the pinned Python requirements installed:

```sh
python3 -B main_existence_attempt/correlation_pass/free_clock/clock_search.py --period 5 --trials 100000 --steps 1000 --max-cycle 100
python3 -B main_existence_attempt/correlation_pass/free_clock/clock_search.py --period 7 --trials 40000 --steps 1000 --max-cycle 100
python3 -B main_existence_attempt/correlation_pass/free_clock/clock_search.py --period 5 --trials 100000 --steps 1000 --max-cycle 100 --prefix-width 4
python3 -B main_existence_attempt/correlation_pass/free_clock/check_prefix_extension.py
python3 -B main_existence_attempt/correlation_pass/free_clock/check_arithmetic_controls.py
python3 -B main_existence_attempt/correlation_pass/free_clock/close_candidates.py --period 5 --width 32 --seconds 12
python3 -B main_existence_attempt/correlation_pass/free_clock/close_by_transfer.py --seconds 20 --cap 50000 --edgecap 50000
python3 -B main_existence_attempt/correlation_pass/free_clock/alternating_language.py
python3 -B main_existence_attempt/correlation_pass/free_clock/alternating_language.py --bisim --layers 30 --cap 1000000
python3 -B main_existence_attempt/correlation_pass/free_clock/alternating_language.py --both --layers 30 --cap 1000000
```

Only `close_candidates.py` requires Z3. The other new scripts use the Python
standard library and retained research modules. The generated graph dumps
are reproducible scratch; small summaries, source, candidate cycles, and
the exact prefix-extension audit are the primary records.
