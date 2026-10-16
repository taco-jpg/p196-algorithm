# Independent review of the rotated-clock corollary

The corollary is a sound consequence of the previously independently
audited component-specific hierarchy. No additional graph search or Lean
compile was needed.

The exact retained certificate has SHA-256
`ff7a70ee2a6ed677cb9176e212dc0a69acd14eed30425a42b543d7a50823b47e`.
Its scalar root job is at width one, contains all seven phase vertices in
one cyclic component, and gives start-phase vertex bounds
`[659,659,659,659,659,659,659]`. The actual-interval lifting and weighted
component argument applies to every starting vertex, not just phase zero.
Thus any cyclic rotation has at most 658 matching transitions when physical
width is at least 14, and at most `floor(658/7)=94` complete periods.

At each phase the outside coefficient is different from nine, so the actual
overflow is fixed independently of the interior carry. The schedule is
`0010101`; every seven consecutive phases in any rotation has three width
increases. The same preparation argument therefore adds at most four
periods for every starting width at least two, giving the uniform bound 98.

The width-one exception is complete: admissibility requires an even center,
leaving only initial values 4, 8, 16, and 6 among this clock's values.
Their first departures occur at times 4, 3, 2, and 1 respectively, so none
completes a period. The explicit trajectories in the note agree with literal
normalization and reflection.

An arbitrary time offset is handled by using the actual pair word and width
at that time; admissibility is preserved. The conclusion excludes an
eventual perpetual copy of any fixed rotation of this precise all-phase
clock. It neither treats isolated visits to outside coefficient four as a
full clock nor excludes switching to another clock.

The three-file producer package and its checker were read in full. Its
certificate extraction checks only the corollary data and correctly relies
on the earlier complete hierarchy audit. It makes no new numerical Lean
formalization claim.
