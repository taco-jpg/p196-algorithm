# AgentN27CentralOverflowFront
**COMPUTED**: A growing-centre decimal trajectory has an exactly overflow-driven central 18 plateau, not just an approximate wall velocity.
For symmetric neutral template B=[12,9], C=[6]++9^m++[6], gap g, let S(t) count decimal overflows and q(t) the length of the central contiguous 18-run in C_t.
In five genuine decimal orbits, every state 1 <= t < collision satisfies q(t)=m-S(t); each overflow removes precisely one central 18, while non-overflow steps preserve the plateau length.
m=40,80,200,500,3000: first collisions at t=96,187,478,1186,7256; checked against ordinary digit-list full-pairword calculations (7,255 pre-collision equalities in the m=3000 case).
For m=3000, after the plateau vanishes at t=7256, the outer neutral template remains valid through t=20629; its carry-flip condition first fails on transition t=20629 to t=20630.
Independent Python BIGINT calculations confirm the full orbit and front law for m=80 and m=200.
No universal all-m theorem, infinite orbit, Lean, 196, or Lychrel certificate claimed.
Reproduce: sh calculation/new_structures/agent-N27/run_front.sh
Sources: calculation/new_structures/agent-N27/{front_check.cpp,independent_front.py,front_expected.json,run_front.sh}; reports/AgentN27CentralOverflowFront.md.
