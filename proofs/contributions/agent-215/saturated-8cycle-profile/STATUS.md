# Agent #215 — saturated eight-cycle temporal profile

Status: WIP.

Initial objective: find stronger temporal/column restrictions beyond the
existing saturation-composition bounds.

Established from the current main source by exact inspection:
- saturated_closed_prefix_period gives n % 8 = 0 for a closed saturated
  Prefix path.
- The tight-clock telescope shows that saturation forces the clock to
  advance by one modulo 8 at every edge.
- The clock definition identifies seven nonzero clock classes with the exact
  states (17,5,0), (8,13,5), (17,6,11), (8,14,8), (17,8,17),
  (8,16,16), (17,13,14).
- Exact evaluation of advance gives the eight-state cycle
  (8,12,9) -> (17,5,0) -> (8,13,5) -> (17,6,11) -> (8,14,8) ->
  (17,8,17) -> (8,16,16) -> (17,13,14) -> (8,12,9).
- On the even positions of that cycle, the incoming bit is forced:
  e = 1,0,0,1 at clock classes 0,2,4,6.
- At the four odd positions, both e=0 and e=1 produce the same next
  skeleton state and the same overflow gamma=1.
- Consequently, once the global temporal skeleton is kernel-proved, the
  saturation equation forces exactly two of the four odd-position inputs to
  be 1 in each 8-step block (because the four even positions contribute
  exactly two overflow-1 edges and saturation requires four overflow-1 edges
  per 8 steps).

The generic extraction theorem remains WIP. No claim about 196 is proved by
this contribution.

Agent #15 owns the distinct six-phase occurrence profile; this contribution
targets the stronger saturated eight-state skeleton and does not duplicate
that theorem.

Continuation checkpoint (Agent #215): added generic odd-position transition lemmas as WIP and an explicit `SaturatedBlockTarget` proposition. The target states exactly that, once the eight-state skeleton is followed and each odd input is in {0,1}, saturation over one 8-step block is equivalent to odd-input sum 2. Lean execution remains unavailable, so these declarations are not promoted beyond WIP.
Latest source commit: ea21aa5ca26e5ba4e76860859d81b0dbc3589f81.
