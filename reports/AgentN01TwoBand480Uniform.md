# N01: 480 exact base-10 edges for all synchronized 20/48-band counts >=40

**COMPUTED**, finite temporal horizon, every band parameter k>=40. This does NOT establish a base-10 Lychrel number, a temporal certificate cycle, or a theorem in Lean. It extends the 128-step uniformly pumped construction in AgentN01TwoBand128StepChain and complements the explicit 20,000-step k500 independent replay.

## Seed and two synchronized gaps
Use coefficient words least-significant first. The explicit 39-coefficient root B, length-20 row W and length-48 row V are shared with calculation/new_structures/agent-N01/replay20k.cpp. Let H_k=B ++ W^k ++ [9] ++ V^k and P_0(k)=H_k ++ [9] ++ reverse(H_k), with N_0(k)=val_10(P_0(k)). Every k>=40 gives an ordinary canonical integer after carry normalization. The source has 81+136k pair-coefficients.

At each t from 0 through 480, write P_t(k)=H_t(k) ++ centre_t ++ reverse(H_t(k)), centre_t empty or one palindromic coefficient as dictated by parity, with the lower half FACTORIZED exactly as

    H_t(k)=A_t ++ W_t^(k-40) ++ J_t ++ V_t^(k-40) ++ C_t.

The precise fixed cuts (zero-based, halfword coefficients) are 0, 199, 20k-601, 20k+616, 68k-1304, floor(|P_t(k)|/2). A_t has length 199 and J_t has length 1217 at every t. C_t starts with length 1344 and reaches 1464 at t=480. W_t and V_t have spatial periods 20 and 48 and evolve under cyclic-carry bulk normalization using the alternating overflow gamma=1,0,1,0,... . The source t0 relation is literally B W^8, then the first moving W^(k-40), then W^32 [9] V^12, the second moving V^(k-40), then V^28 up to centre.

## Fully finite soundness check (paper mechanism, computational instance)
At each time step t the C++ code constructs Boolean transition matrices M_A, M_W, M_J, M_V, M_C using the two-ended 80-state transducer of AgentN01LockedTwoBandDiagonal (state = low incoming carry, high outgoing carry, previous high digit, observed nonpalindrome flag; guessed inner carry bits are constrained by terminal conditions). For gamma=1 a centre overflow shifts the mirrored pairing by one column; this is explicitly modeled in every symbol transition and terminal test. The Boolean 80-by-80 matrix of the full edge at r=k-40 is exactly

    M_A * (M_W)^r * M_J * (M_V)^r * M_C.

The code checks M_W^2=M_W and M_V^2=M_V separately on EACH of 480 edges, not only in the initial phase; therefore every r>=1 has the same Boolean product as r=1, while r=0 is the distinct empty-band case. For each edge both r=0 and r=1 pass the complete terminal acceptance, canonical overflow and nonpalindrome flag conditions. Hence a PAPER PROOF by induction over the 480 edges and the matrix semantics establishes the claimed all-k finite time range, conditional only on the easily auditable explicit transition implementation. Label is COMPUTED because no Lean/kernel verification is claimed.

The checker independently constructs the literal integer pair-coefficient words for k=40,41,42 and computes 480 ordinary digit-array reverse-and-add steps for each. At EVERY one of 481 times all three must have identical extracted A_t,W_t,J_t,V_t,C_t,centre_t despite different k, and the arithmetic canonical digits must equal normalization of their full coefficient words. This independent arithmetic also verifies the alternating overflow and nonpalindromicity. A further GMP mpz_class full-integer reverse-and-add replay for k=45 over 480 steps gives 6,442 decimal digits and FNV64 43d7778659e5a1ae.

## Genuine remaining obstruction and constructive next target
At t=480, with k=40, W_480=W_0, V_480=V_0 and A_480=A_0. Yet J_480 has 391 coefficients changed relative to J_0, all changed coefficients lying in offsets 530..933 of the fixed-length 1217 bridge. The centre suffix grows by 120 over the 480 steps and does not return to its initial form. This is a constructive wall/spreading-defect observation, not another no-go census: the new format should permit a travelling, regenerating bridge and an independently shifted centre counter. A pure finite-horizon persistence check cannot close the cycle.

## Reproducible commands
From the repository root (C++17 standard library for the main checker):
    g++ -O3 -std=c++17 calculation/new_structures/agent-N01/chain480.cpp -o /tmp/n01chain480
    /tmp/n01chain480

The checker reuses the seed arrays and ordinary digit arithmetic in replay20k.cpp, committed in the earlier N01 result. It prints PASS: EXACT 480 successive decimal edges for ALL k>=40 and centre suffix=1464, with six progress checkpoints.

Separate GMP control (GMP development library required):
    g++ -O3 -std=c++17 calculation/new_structures/agent-N01/replay_gmp20k.cpp -lgmpxx -lgmp -o /tmp/n01gmp
    /tmp/n01gmp 45 480

Expected compact machine-readable scope: calculation/new_structures/agent-N01/chain480_expected.json. Local program execution and independent GMP check completed; full repository verify.py and Lean kernel checking were unavailable. No stronger claim is made.
