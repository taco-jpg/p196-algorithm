# Agent N29: constructive 400-edge decimal geometric 9-band trajectory

**COMPUTED** (finite 400-edge family) and checked by the exact polynomial mechanism whose soundness is a **PAPER PROOF** in `AgentN29GeometricWords`. No infinite Lychrel certificate is claimed.

## New construction and exact scope
Start with `N_0(q)=12 9^q 34`. For **every integer q>=240**, states t=0..400 have the **complete** decimal word form

`N_t(q)=L_t ++ 9^(q+c_t) ++ R_t,`

with `c_t>=-240`. The literal strings `L_t,R_t` grow and change on each step: no fixed-width centre, no need to guess any carry itinerary. A concrete sample at q=600 produces proposed words, but each proposed step is then certified as **the exact polynomial identity**

`val(N_t(q))+val(rev(N_t(q)))=val(N_(t+1)(q))`

in `X=10^q` via `geometric_checker.py`. The same checker proves every one of the 401 state words nonpalindromic for **all** q>=240: clearing denominators and stripping X factors leaves an integer polynomial whose constant coefficient bounds possible powers `10^q` that could be roots. Across all 401 state differences, the **largest** candidate-root exponent bound is 239 (attained at t=400). Since q>=240, every nonpalindrome assertion is automatic once exact polynomial coefficient data are generated. In particular, these are not sampled-q extrapolations.

## Independent decimal evidence
At q=240, a second ordinary Python big-integer reverse-and-add replay starts from the literal 244-digit `12 9^240 34`, then checks the entire predicted word and nonpalindromicity at **each state 0..400**. At t=400, q+c_t=0, the literal packets have lengths 204 and 204 and the integer has 408 digits. The tested parameter is thus the **smallest allowed for this specific 400-edge affine 9-band representation**; smaller q gives a negative repeat count at the last edge state and is outside the claim, not proved impossible as an orbit.

At the q=600 mining sample the long 9-run decreases from 600 to 360; packet lengths grow from (2,2) to (204,204) over 400 steps, and the total integer length increases 604 to 768 digits. Every-25-step checkpoints are stored as `geometric_miner_checkpoints.tsv`. No data file beyond the published source and table is necessary.

Reproduce with `python3 calculation/new_structures/agent-N29/geometric_miner.py --q 600 --qmin 240 --steps 400 --out /tmp/n29-9band.json` (Python standard library only). The run independently checks literal integer arithmetic at q=240 on **every** state and calls the exact checker at every edge.

## What breaks, and the constructive redirect
For the minimal parameter q=240, the periodic 9 reservoir is **fully consumed at t=400** (while q=600 retains 360 digits). Nothing in this calculation establishes the transition at t=401 within the same one-band format. A second geometric-series band with compensating net **positive** repetition gain, not another short-centre exclusion search, is the next candidate for an infinite decimal cycle. This is a finite constructive mechanism and a sharp resource-exhaustion landmark for its chosen representation.
