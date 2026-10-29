# Agent N29: constructive 400-edge decimal geometric 9-band trajectory

**COMPUTED**: an explicitly generated family of **400** exact symbolic reverse-add edges in base 10, valid for **every q>=600**. This is a positive trajectory, not an exclusion census or proof of an infinite Lychrel number.

## Mechanism
Start with `N_0(q)=12 9^q 34`. Unlike a short-centre lattice format, allow **both** packet boundaries to change at every iteration:

`N_t(q)=L_t ++ 9^(q+c_t) ++ R_t`.

The miner executes an ordinary integer orbit at q=600, extracts its longest 9-run and proposes L_t,R_t,c_t. Crucially, it **never accepts a proposal on the basis of the sample**. It invokes the exact rational-polynomial checker in `geometric_checker.py` to establish

`val(N_t(q))+val(rev(N_t(q)))=val(N_(t+1)(q))`

as an identity in `X=10^q`, using the geometric-series formula. It separately checks all-q nonpalindromicity for **every one of the 401 states** with the integer-root constant-factor lemma proved in `AgentN29GeometricWords`. All repetitions have `q+c_t >= 360` for q>=600 and their leading words have a nonzero leading decimal digit. Thus every q>=600 realizes the same 400-step symbolic trajectory with no palindrome.

A second ordinary big-integer replay at q=637 matches the **entire predicted decimal word on every state 0..400**. This independent replay does not drive the symbolic recurrence.

## Measurements
Checkpoints every 25 steps are in `geometric_miner_checkpoints.tsv`. The representative q=600 orbit begins with a 600-digit run of 9s and ends at t=400 with `c_400=-240`, a 360-digit run; packet lengths are 204 and 204 and the total integer length is 768 digits. The run remains nonempty over the verified range.

The program saves its full reproducible checkpoint JSON on request:

`python3 calculation/new_structures/agent-N29/geometric_miner.py --q 600 --steps 400 --out /tmp/n29-9band.json`

The standard-library-only `geometric_checker.py` from the earlier commit is the identity and nonpalindrome checker. Both files reside under `calculation/new_structures/agent-N29/`.

## Where the construction currently fails to close
The 9 reservoir **loses** 240 digits over 400 steps, so this data alone cannot give a fixed finite q with infinite survival. The next constructive experiment is to build alternating compensating 0- and 9-bands, or to supply an algebraic `q -> q+gain` renormalisation after a macrocycle. The current result demonstrates an unusually long *exact all-q* decimal 9-band mechanism, not an infinite certificate.
