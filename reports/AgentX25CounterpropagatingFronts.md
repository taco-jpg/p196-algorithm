# Agent X25: asymmetric 88/792-step clock-transduced fronts

## Novel computed observation and exact finite scope
**COMPUTED**, base 10 only, genuine orbits of three explicitly realizable decimal integers, not the orbit of 196. Construct a symmetric pairword P=B ++ W^q ++ (8,0,0,16,0,0,8) ++ reverse(B ++ W^q) from the corrected rooted p8/m20 exterior of N01 and the N18 seven-site core. Insert the mirror-symmetric eleven-coefficient species A=(6,1,0,1,11,14,10,6,11,16,1) or D=(16,0,9,11,1,10,8,5,14,18,0) at lower-half position x; these species were originally N21's p12/m9 packet symbols, but are now driven solely by the **actual p8 global clock**, not the incompatible independent p12 overflow schedule.

Write P0(t), PA(t), PD(t) for the full symmetric coefficient pairwords, and L_X(t),R_X(t) for the minimum and maximum lower-half positions at which PX(t) differs from P0(t). Define a *left window* as PX(t)[L_X(t)-80:L_X(t)+21], a *right window* as PX(t)[R_X(t)-20:R_X(t)+81], each **101 coefficients**. The two windows are measured in a co-moving frame and include unchanged exterior data across the active front.

With q=600, x=2500, three 24085-digit integer seeds (reference and A/D substitutions), exact full pairword radix-normalization arithmetic at all t=0..5000 verifies a shared global overflow g(t)=1 for even t and 0 for odd t, and the same rooted exterior first 39 coefficients. An odd coefficient persists in this prefix at every t for each seed, proving no integer can be a palindrome at any of those 5001 states (a palindrome would have all pair sums even). No global infinite theorem is inferred.

## Two distinct, reproducible moving clocks
At every integer t in each indicated *closed* interval, both the front coordinate and every coefficient of the 101-cell window repeat exactly after the stated temporal/spatial translation:

| species/front | time increment | spatial increment | all-success interval t | consecutive successful checks |
|---|---:|---:|---:|---:|
| A left | 88 | -20 | 397..4912 | 4516 |
| D left | 88 | -20 | 242..4912 | 4671 |
| A right | 792 | +540 | 422..4208 | 3787 |
| D right | 792 | +540 | 494..4208 | 3715 |

The complete sweep, including early sporadic matches and exact last-failure indices, is in dual_front_expected.txt. All shorter 88-multiple delays 88,176,264,352,440,528,616,704 with the corresponding +60-per-88 spatial shear have **zero** successful right-window matches on the full t range where both windows exist; hence 792 is the shortest observed right-front return in this finite search over multiples of 88. The (88,-20) left drift is related to N10's existing exterior glider, so the distinct result is its coexistence with a *different* (792,+540) outward right-front clock on the same real decimal packet orbit.

Changing to q=350, x=1500 and replaying t=0..3000 produces exactly the same four last-failure thresholds (396,241,421,493). That is a second finite seed parameter control, not an all-q pumping proof.

## Independent whole-number validation
The separate dual_gmp.cpp represents the three seeds as genuine canonical GMP arbitrary-precision integers and iterates each n -> n+reverse_10(n), using GMP decimal string conversion rather than the coefficient transition. For q=140, x=960 and t=0..1792, it checks the *complete* decimal digit pairword of all three integers against the separate radix-normalization engine at **every step**, rejects palindrome states, checks the alternating length overflow, and reconstructs the four moving windows and front positions independently. Total: 1793 states per orbit, 5379 full arithmetic comparisons, zero mismatches and zero palindromes; the seed has 5685 decimal digits and final length 6581. The detected last-failure positions are the same 396,241,421,493. In particular, all 579 t=422..1000 A-right comparisons and all 507 t=494..1000 D-right comparisons pass the 792-step shift, while the left-window 88-step periods also pass throughout their checked stabilized intervals. This is a genuine second arithmetic implementation, not a local SAT boundary approximation.

## Why it matters and what is missing
The packet has asymmetric outward/inward tip clocks with rational velocities +540/792=15/22 and -20/88=-5/22. Their relative closure speed is 10/11, matching X25's separately observed +180 spatial gap / +198 first-collision delay increments. Moreover 792=9*88 and 540=9*60, so the right tip has a larger internal temporal register than the rooted exterior alone. This suggests a finite 792-step carry-port *collision tile* assembled from 88-step exterior subtiles, with an extra 9-state internal schedule, rather than a p12 autonomous bulk embedded alongside p8.

**This is not a bounded soliton or an infinite certificate.** The active disturbance support broadens, the full wake is not periodic merely because a near-tip window repeats, and all checks stop at the stated finite times. In particular, a certificate requires (i) a finite two-ended carry-port transfer proving this tip recurrence for all admissible band lengths and all time, (ii) a nonlinear collision/reset tile that repairs the nonperiodic wake or creates a permanently growing safe centre, and (iii) a verified palindrome witness and nonshrinking counters across the resulting *entire* macrocycle. Neither a complete 792-row self-generating transfer nor a regenerative collision has been found. Lean verification is not claimed.

## Reproduce
From the repository root:

    g++ -O3 -std=c++17 calculation/new_structures/agent-X25/dual_front.cpp -o /tmp/x25_front
    /tmp/x25_front 600 2500 5000 > /tmp/x25_front.txt
    diff -u calculation/new_structures/agent-X25/dual_front_expected.txt /tmp/x25_front.txt
    /tmp/x25_front 350 1500 3000
    g++ -O3 -std=c++17 calculation/new_structures/agent-X25/dual_gmp.cpp -lgmpxx -lgmp -o /tmp/x25_gmp
    /tmp/x25_gmp 140 960 1792

Both stand-alone C++ executables and the GMP differential test were run locally. The sandbox cannot clone the live GitHub repository due to DNS and has no Lean 4.19.0 installation, so a repository-wide tools/verify.py --changed was not run. No Lean files changed.
