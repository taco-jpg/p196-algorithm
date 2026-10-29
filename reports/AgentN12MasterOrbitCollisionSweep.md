# Agent N12: exact master-orbit transfer and 257 decimal collision histories

Status: **COMPUTED** for finite trajectories and checked collision times; **PAPER PROOF** of the following transfer rule, based on the previously established central-zero padding lemma. NOT LEAN-VERIFIED. No proof of a decimal Lychrel number.

## Construction
Use ordinary base-10 reverse-add T(N)=N+reverse(N). Let P(N)_i=d_i+d_(n-1-i), least significant first, and let z(N)=n-2w where w is the shortest outer pairword half-width containing all nonzero coefficients. Thus P(N)=B++0^z++reverse(B). The seed family is N_k=39 ++ 0^(31000+k) ++ 43, k=0..256. All statements concern integer iterates t at or before the first t with z(T^t(N_k))=0.

## Transfer correctness (PAPER PROOF)
For a canonical positive digit word X with a symmetric central zero corridor of length >=4, Pad_delta(X) inserts delta central zeros, for delta>=0. The known digit-normalisation argument proves T(Pad_delta(X))=Pad_delta(T(X)) and that palindrome truth values are identical: each central zero pair coefficient consumes any carry and propagates zero through the inserted segment. Hence, if a master orbit U_t starts at Pad_delta(N_0), and all earlier U_s satisfy z(U_s)>=delta+4, then U_t=Pad_delta(T^t(N_0)) by induction and removing exactly delta central zeros recovers the true shorter-seed state. The induction uses the existing padding lemma on the *shorter* current state, whose z is z(U_s)-delta>=4. The guard may be changed to any bound >=4; activation at the first master t satisfying z(U_t)<=delta+100 is safe because all prior times have z(U_s)>delta+100 and the program explicitly verifies z(U_t)-delta>=4. On activation the algorithm constructs N_{k,t} by central unpadding and then runs actual decimal schoolbook reverse-add independently for that k until z=0, never borrowing future data from the master. Palindromicity before activation matches the master under padding; after activation every state is checked directly. The stored maximum earliest opposing-digit mismatch through collision covers both phases.

## Computed result
The ONE master trajectory is N_256 (31,256 central zeros). Source C++ is calculation/new_structures/agent-N12/master_gap_sweep.cpp. Every k=0..256 activates safely, then has a first z=0 at t in [51464,51886], with no palindrome at any earlier state or at collision. The maximum earliest opposing-digit mismatch is **exactly index21** for every k; the first 22 opposing digit pairs therefore always contain a nonpalindrome witness. Across 256 adjacent gaps, first-collision time moves down 42 times (none equal), despite net +422 steps. Successive time differences are -3 (7), -2 (6), -1 (29), +1 (55), +2 (90), +3 (34), +4 (28), +5 (7). In particular q=31003 collides at t51470 while q=31004 collides earlier at t51468. This is positive evidence of collision-phase-sensitive interacting fronts, not an exclusion census.

Selected checkpoints (q,t): (31000,51464), (31001,51465), (31002,51466), (31003,51470), (31004,51468), (31016,51487), (31032,51513), (31064,51565), (31096,51621), (31128,51671), (31160,51727), (31192,51785), (31224,51838), (31256,51886). Full 257-row CSV generated locally has SHA256 `b79a51e8aae26e2bfab60653b35c9635ca35fcae8fdc121f16cf0326d216c86f`. The run checks the master for palindromes at all 52001 states, every shorter seed's preactivation nonpalindromicity by exact transfer, and postactivation states with direct arithmetic until collision. It uses no state caps and no probabilistic test for the 257 results.

## Independent arithmetic and reproduction
From repo root, run:
```sh
bash calculation/new_structures/agent-N12/run_master_sweep.sh
g++ -O3 -std=c++17 calculation/new_structures/agent-N12/chunk_bigint_replay.cpp -o /tmp/n12_radix1e9
/tmp/n12_radix1e9 39 31004 43 51475 0 /tmp/n12_q31004.csv
/tmp/n12_radix1e9 39 31256 43 51890 0 /tmp/n12_q31256.csv
g++ -O3 -std=c++17 calculation/new_structures/agent-N12/master_gap_sweep.cpp -o /tmp/n12_master
/tmp/n12_master 256 52000 100 > /tmp/n12_sweep.csv
python3 calculation/new_structures/agent-N12/independent_master_check.py /tmp/n12_sweep.csv /tmp/n12_q31004.csv /tmp/n12_q31256.csv
```
Expected final line: AGENT_N12_MASTER_SWEEP_COMPLETE_PASS. The independent radix-10^9 limb algorithm begins from the *literal original seed* rather than a master snapshot, computes every integer transition up to/past collision for q=31004 and q=31256, and returns collision t51468/t51886 and max witness index21. The Python checker independently checks 16,000 random ordinary-bigint padding identities, recomputes summary statistics and SHA256, and checks both direct full-seed traces.

## Limits
A finite witness bound through one collision does NOT imply it remains bounded afterward, that any iterate is forever nonpalindromic, or that the k-dependence of collision times has a period/closed recurrence. This constructive transfer sweep is intended as a seed-family search instrument for discovering a *postcollision* renormalization mechanism. It does not decide any all-width K1/K2 exclusion.
