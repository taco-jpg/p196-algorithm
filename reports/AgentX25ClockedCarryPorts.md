# X25: finite 792-step mixed-clock four-carry-port interface

## Status and construction
**COMPUTED**, finite ordinary base-10 arithmetic only, not Lean-verified and not an infinite Lychrel certificate. Use the true rooted p8/m20 coefficient pairword P=B ++ W^q ++ (8,0,0,16,0,0,8) ++ reverse(B ++ W^q), with the corrected 39-cell B and 20-cell W of N01. Mutate the mirror-paired positions at x with species A=(6,1,0,1,11,14,10,6,11,16,1) or D=(16,0,9,11,1,10,8,5,14,18,0), the eleven-cell symbols borrowed from N21's p12/m9 packet train. The genuine global clock is p8's alternating overflow. A packet's former p12 label does not set the integer's overflow.

Our preceding X25CounterpropagatingFronts result showed each species' outward 101-coefficient window returns after a 792-step temporal shift and +540 spatial drift. That does not establish a two-ended carry boundary contract. This follow-on tests *both* low and high carry interfaces physically and proves an independent elementary local pinning lemma.

## Four physical gates
Let P_t be the whole symmetric pairword and n=|P_t|. Normalize by c_0=0, c_(i+1)=floor((P_t[i]+c_i)/10). For the rightmost lower-half position R_t at which the packet differs from the clean baseline, define l=R_t−20, h=R_t+80. At every t measure the four-bit gate (c_l,c_(h+1),c_(n−1−h),c_(n−l)). The latter two gates belong to the *mirror partner*, not to a fictional reflected carry; they are true forward-radix carries from the ordinary normalization of the entire word. The observed return requires both R_(t+792)−R_t=540 and exact four-bit equality.

For q=600, x=2500, the full pairword engine computes three explicit positive canonical decimal orbits, with 24,085 initial digits, t=0..5000. It checks global overflow shared by all three and a persistent odd coefficient among the first 39 positions, hence no palindromes within the reported horizon. The gate-and-front return results for the 4209 tested start times t=0..4208 are:

| Species | Passing comparisons (including early sporadic passes) | Last failing start | Guaranteed consecutive pass interval |
| A | 3929/4209 | 421 | 422..4208 (3787 comparisons) |
| D | 3856/4209 | 496 | 497..4208 (3712 comparisons) |

For example A's four gates read 1110 at t422 and t1214; D's read 1101 at t500 and t1292. An independently parameterized q=350, x=1500 pairword replay t=0..3000 gives the *same* 421/496 last-failure thresholds, a second finite-seed control but not a pumping theorem.

## Independent actual-integer carry oracle
The C++ GMP oracle (distinct implementation) constructs canonical ordinary decimal seed integers, evolves n->n+reverse_decimal(n), and reads the entire pairword from each integer at every step. Crucially its carries are NOT copied from the primary normalization: from the actual NEXT integer's decimal digits d_i, it recovers each carry by the integer equation c_(i+1)=(P_i+c_i−d_i)/10, checks the result is 0 or 1, and verifies the exact final overflow by the integer's next length.

For q=140, x=960, all three genuine integer orbits pass every full pairword and carry comparison at times t=0..1792 inclusive (5379 ordinary-number state checks, no palindrome). The independently reconstructed 792-step gate-and-front returns are A 721/1001, last failure 421, every t=422..1000 passes; D 648/1001, last failure 496, every t=497..1000 passes. Note that D's four-port contract becomes stable three steps AFTER the previously measured 101-coefficient digit window becomes stable (t494). Thus these boundary gates carry information not captured by the finite front coefficient window alone.

## Carry isolation lemma (elementary PAPER argument)
For base b>=2, x in 0..2b−2 and incoming carry c in {0,1}, the outgoing carry floor((x+c)/b) is always 0 if x<=b−2, always 1 if x>=b, and equals the incoming carry if x=b−1. Consequently, if the r coefficients immediately preceding a carry cut are b−1 and the immediately earlier coefficient x is not b−1, then the carry is determined by x alone, *independently* of every preceding coefficient: 0 when x<=b−2, 1 when x>=b. This follows by one forcing step and r identity-transmission steps. If there is no earlier non-(b−1) coefficient, c_0=0 is its root source. No SAT assumption is needed.

For all measured t=497..4208, the maximum numbers of immediately preceding 9 coefficients at the four gates are exactly (3,1,0,3), identically for both packet species. Therefore *during the tested interval*, every physical gate is fixed by at most four nearby preceding coefficients. The run-length bound is observational, not proved for arbitrary t. This is a concrete local-interface target for SAT/finite transfer certification.

## What remains
The finite two-ended four-port and moving-window recurrence is a plausible 792-row nonlinear mixed-clock tile, with independent 88-step p8 clock and an internal packet register. But the entire disturbance wake keeps spreading. A base-10 Lychrel certificate still needs a finite exact carry-port semigroup proof that works for arbitrary pumped buffer counts and guarantees a regenerative macrocycle with a palindrome guard. Neither an all-t proof of the observed front recurrence nor a wake-erasing collision cycle is provided; no claim about 196 or about base-10 infinite palindrome avoidance.

## Reproduce
From the repository root (C++17 and GMP installed):

    sh calculation/new_structures/agent-X25/run_ports.sh

The runner checks the exact fixture, q350 control, and independently derives all q140 GMP carries. No Lean files were changed. Shell GitHub DNS and Lean4.19.0 are unavailable in the sandbox, so repository-wide tools/verify.py --changed could not be run.
