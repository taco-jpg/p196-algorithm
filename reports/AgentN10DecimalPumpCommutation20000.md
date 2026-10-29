# Exact whole-pairword decimal pumping: a constructive 20,000-step renormalisation

**Label: COMPUTED.** Base 10, finite horizon only. This result builds on `AgentN10DecimalQuotientShield20000` and the repository's pre-existing p8/m20 rec0 exterior; it does not claim a new lattice.

## Stronger structure than exterior agreement
Write `T(P)` for coefficient-word carry-normalization followed by reversal-pairing. For any palindromic pairword `P` with at least 78 coefficients define the phase-dependent insertion
`I_t(P) = P[:39] ++ W_t ++ P[39:-39] ++ reverse(W_t) ++ P[-39:]`.
This inserts **20 sites at each reflected side**, maintaining palindromicity and increasing the pairword length by 40. The `W_t` are the eight exact phase words generated deterministically in `phase.json`.

For each of four real positive decimal seeds from the previous result (initial copies k=300, C either empty, `[0,18,18,0]`, `[2,4,4,2]`, `[9,6,6,9]`), take the paired seed with k=301 and the SAME core. Evolve both by actual ordinary decimal digit-list reverse-and-add, without invoking the coefficient transition. For every integer t in [0,20000] the full pairwords satisfy
`P_t(301,C) == I_(t mod 8)(P_t(300,C))`.
This is an **exact full-word identity**, including the disordered growing core, not an asymptotic resemblance or prefix comparison.

For empty C, 20,001 time slices compare **342,382,118 exact coefficient positions** of the larger orbit with zero discrepancies. At t=0 the integer lengths are 12,078 and 12,118; at t=20,000 they are 22,078 and 22,118. Three other central cores all give zero discrepancies across the same 20,000 steps (342,462,122 coefficient comparisons each). The two real integer lengths differ by exactly 40 at every step.

## Independent verification and controls
The C++ program `pump.cpp` constructs the actual decimal digit arrays separately for k and k+1 and independently performs both `n+reverse(n)` additions on every step. It then explicitly checks the stated insertion equality at **every** pairword position, including reflected high-side coefficients.
A second implementation `pump_bigint.py` uses Python arbitrary-precision integers, decimal string reversal, and a different construction of the full pairword. For k=300, empty core, t=0..1000, all 1,001 full-word identities pass. Shorter buffer k=100 was observed to lose the relation at t=8804 (pilot, not presented as an exhaustive exclusion). This directs the next construction toward *replenishing* an inserted lattice period as the central front consumes the buffer.

Run the exact reproducer from the repository root:
```sh
sh calculation/new_structures/agent-N10/run_pump.sh
# or individually:
cd calculation/new_structures/agent-N10
python3 build_phase.py
g++ -O3 -std=c++17 -Wall -Wextra -pedantic pump.cpp -o /tmp/n10-pump
/tmp/n10-pump 300 20000 0
python3 pump_bigint.py 300 1000
```

## Soundness target for an eventual certificate format (UNDECIDED)
The observed finite commutation suggests a **pump-equivariant quotient**: a finite-state transition on a phase and carry-boundary class with a self-insertion map `I_t`, together with a finite checker for `T(I_t(P))=I_(t+1)(T(P))` uniformly for every admissible centre word P in a specified regular boundary language. An all-time certificate would additionally require closure of that boundary language and a nonpalindrome witness. None of these uniform universal closure conditions has been established here. The existing guarded-prefix lemma only supplies a one-step eroding bound, and the 20,000-step exact full-word identity remains COMPUTED at the specified seeds and horizon.

No Lean files have been added. The complete repository checkout was unavailable in the shell (GitHub DNS resolution failed), so `tools/verify.py --changed` was not run.
