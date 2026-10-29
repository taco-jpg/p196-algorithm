# N27: an overflow-clocked shrinking centre and its delayed failure

## Result and scope
**COMPUTED.** Consider the ordinary base-10 integer with symmetric least-significant-first pairword P0 = [12,9] ++ 9^g ++ [6] ++ 9^m ++ [6] ++ 9^g ++ [9,12], and nonzero leading decimal digit. The existing neutral-band update yields B_t,C_t,g_t as long as e1 != e2. Define S_t=sum of actual 0/1 decimal length overflows before time t, and q_t=length of the consecutive central 18-run in C_t, with q_t=0 when the centre is not 18. In the five specified ordinary decimal orbits below, for EVERY t with 1 <= t < the first S_t=m, the exact identity q_t=m-S_t holds. This is a finite verified identity, not a theorem for all m.

## All observed cases
| m | Outer gap g0 | First S_t=m | Precollision equalities | First failed e1 != e2 transition |
| ---: | ---: | ---: | ---: | ---: |
| 40 | 10000 | 96 | 95 | 273 |
| 80 | 10000 | 187 | 186 | 567 |
| 200 | 10000 | 478 | 477 | 1279 |
| 500 | 10000 | 1186 | 1185 | 3407 |
| 3000 | 12000 | 7256 | 7255 | 20629 |

For m=3000, the triples (t,S_t,q_t) are (1,1,2999), (100,42,2958), (1000,423,2577), (5000,2079,921), (7000,2897,103), (7254,2999,1), (7256,3000,0). At t=20000 the ordinary decimal orbit has 35,322 digits, outer gap 5037. At t=20629 there are 35,586 digits and the gap is 4839, and the pairword is still exact and the integer nonpalindromic; e1=e2 prevents using the neutral template on the next transition. It is not a claim that the next ordinary number is a palindrome.

## Constructive front mechanism
The coefficient 18 has an absorbing carry map: when normalized from incoming carry 1, it emits decimal digit 9 and outgoing carry 1. A uniform 18 plateau therefore has an interior stable under mirror pair sums (9+9=18), while a one-digit overflow shifts the mirrored overlap by one place. The boundary words may add or remove cells, so the equality is **not universal** for arbitrary boundary states. On the five exact trajectories, those boundary effects are balanced at every step before collision, and the net central contraction is exactly gamma per step, with gamma the true overflow. This is an explicit moving two-front mechanism controlled by the global length-increment clock, not a periodic bounded centre.

After collision, the centre becomes nonuniform but the outer neutral template survives many additional steps. Search should seek a regenerating inner 18 block or a mechanism changing the exterior carry trajectory at the collision, rather than another fixed-width kink. The central front law itself does NOT prove any infinite orbit.

## Reproduction and independent controls
The new front_check.cpp includes the previously committed replay.cpp implementation (in the same directory), which already independently compares ordinary decimal schoolbook addition and the exact neutral-template recurrence at every full pairword, including nonpalindromicity. front_check.cpp adds an independently evaluated central-run length and cumulative ordinary-digit overflow count, checks the identity at every eligible state, and records the first collision and carry-flip failure.
A completely separate Python arbitrary-precision-bigint engine independent_front.py reconstructs and adds actual decimal integers by string reversal, checks every coefficient of the full pairword, and validates the front law through collision for m=80,200 (collisions t=187,478); no C++ arithmetic is called. front_expected.json contains the exact observed counters.
Run from the repo root: sh calculation/new_structures/agent-N27/run_front.sh (standard Python3 and C++17).
No Lean verification, no infinite decimal Lychrel number, and no assertion about 196 is made.
