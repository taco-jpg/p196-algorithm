# Status: exact periodic quotient; no closed safe family found

The exact period-four interior graph from `(14,14,4,4)` has 59 reachable phases. Intersecting it with the actual outer coefficient rule gives 878 states. Tracking width modulo eight and reflected phase gives 7,024 states. These complete finite graphs are necessary conditions only: their interior clocks and boundary carry choices have not been joined by a finite canonical exterior and center.

The seven-step bulk loop with clock `1000111` cannot lift: repetition requires four consecutive overflows, whereas the exact outer relation allows at most three. A different 16-step, eight-overflow loop survives both filters and the prior eight-step outer-three boundary restriction. No finite whole-word lift is established.

The exact guarded quotient for `B w^k H rev(w)^k rev(B)` computes an actual whole-word transition for every `k>=3`. Any safe state cycle in this quotient would have positive exponent gain and would give an infinite safe family. No cycle was found among the eleven examined seeds.

All eleven seeds reached the explicit 128-step path cap and remain **UNKNOWN**. The 1,408 saved symbolic transitions are safe; the graph and interface limits were not hit. Every recorded bulk becomes constant nine at time 21 and constant zero by time 26. Full symbolic paths and eleven ordinary 128-addition decimal trajectories are retained.

The independent checker passed complete graph/SCC replay, rotation/reflection checks, 5,632 ordinary-integer transition controls, and all 1,408 additions in the ordinary trajectories. The finite controls validate code; the guard-period argument in `METHOD_AND_PROOF.md` proves the all-exponent identity.

This does not resolve decimal Lychrel existence, 196, or arbitrary regular or recursive safe languages. The sibling `periodic_interface_followup/` owns further finite-interface work. The earlier DFA and four-band bundles remain separate and frozen.
