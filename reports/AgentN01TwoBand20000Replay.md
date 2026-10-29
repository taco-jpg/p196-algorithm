# N01: a decimal two-lattice orbit with 20,000 verified additions

**COMPUTED; one explicit finite orbit and its shape only.** This is not a proof of infinite palindrome avoidance, a periodic template cycle, or a result about the 196 orbit. No Lean proof is asserted. It is a new constructive decimal mechanism beyond exclusion/census results. The preceding exact all-k 128-edge family and finite 80-state carry edge soundness are in reports/AgentN01LockedTwoBandDiagonal.md and reports/AgentN01TwoBand128StepChain.md.

## Explicit seed
Use least-significant-first coefficient arrays B (39 entries), W (20 entries), V (48 entries) as given verbatim in replay20k.cpp and reproduce.py, with B corrected to exactly match the initial depth-39 rec0 exterior path in lattice_formats/p8_scc.txt. With k=500 set
  H=B ++ W^500 ++ [9] ++ V^500
  P_0=H ++ [9] ++ reverse(H)
  N_0=val_10(P_0).
P_0 has 68,081 coefficients in [0,18], and N_0 has 68,082 canonical decimal digits. This is an explicit ordinary decimal integer (not asserted to be an existing Lychrel number). For each t, D_t is the canonical decimal digit word of N_t, N_(t+1)=N_t+reverse_10(N_t), and P_(t+1)=pairs(D_t). All coefficients are least significant first.

## 20,000-step replay and exact two-band pairword shape
The C++ digit-array implementation independently performs true decimal reverse-and-add and normalizes every coefficient word P_t; it checks the full equality D_t=norm_10(P_t,0) at EVERY t=0..20,000 and confirms all 20,001 canonical D_t are nonpalindromic. It checks the overflow gamma_t=1 for even t and 0 for odd t at each time. The canonical decimal digit length at t=20,000 is 78,082; FNV-1a 64-bit hash over its digits in least-significant-first order, offset 1469598103934665603 and multiplier 1099511628211, is 3fc9680e7260649.

Let W_t and V_t be the rows from cyclic-carry bulk update as defined by function bulk(w,gamma), with initial rows W,V. At each of the 20,001 time states, the checker verifies the actual pairword P_t has the following *complete, literal* symmetric two-band decomposition, with H_t its lower half:

  H_t = A_t ++ W_t^50 ++ J_t ++ (rotate(V_t,24))^20 ++ C_t,
  P_t = H_t ++ [central coefficient if odd] ++ reverse(H_t).

The left W chunk occupies pairword positions [439,1439), exactly 1000 coefficients; the V chunk occupies [25040,26000), exactly 960 coefficients. Consequently A_t has length 439 and J_t has length 23601, while C_t is the remaining finite suffix to the centre (allowed to grow with t). This is a meaningful fixed-in-space two-bulk survival witness, **not** a bounded-width defect cycle; with arbitrary A_t,J_t,C_t it is not a sufficient infinite certificate. The checker compares every actual coefficient in BOTH long repetitive chunks to the expected temporal row at EVERY t, not only their first few cells. Pairword reflection is exact by construction from D_t and is used in every integer equality.

## Independent arbitrary-precision integer replay
Separately compiled replay_gmp20k.cpp constructs N_0 in GMP mpz_class, and for t=0..20,000 converts the full actual integer to its canonical decimal expansion, checks nonpalindromicity, reverses its decimal string, converts the reversal back to mpz_class, and adds it. This implementation does not use the coefficient normalization, periodic word update, or the carry-matrix checker for its arithmetic. After 20,000 additions it independently obtains **78,082 digits** and exactly the same full-digit FNV64 3fc9680e7260649. Reproducing the GMP control requires the installed GMP development library; the main 20,000-step replay needs only a C++17 compiler.

## Quantitative defect fronts: a mechanism, not a reset
An additional C++ full-orbit probe compares the entire original 10,000-cell W sector and 24,000-cell V sector to their corresponding bulk rows, and records the longest contiguous intact match at selected times. Exact lengths from fronts.csv:

| t | W longest contiguous intact run | V longest contiguous intact run |
|---:|---:|---:|
| 0 | 10000 | 24000 |
| 128 | 9970 | 23899 |
| 480 | 9890 | 23639 |
| 1000 | 9773 | 23241 |
| 2000 | 9545 | 22484 |
| 5000 | 8864 | 20206 |
| 10000 | 7728 | 16421 |
| 15000 | 6590 | 12633 |
| 20000 | 5455 | 8862 |

At t=20,000 the 20-band rooted intact run is [39,5494), whereas the 48-band longest intact run is [22265,31127). These measured invasion fronts advance approximately linearly over the finite observed horizon; no infinite speed law, extrapolated time of collision, or all-width exclusion is claimed. They redirect the next construction to **active regeneration of the shrinking interior band by a travelling defect, or exact temporal renormalization of a joint 20/48-period controller**. Merely increasing k only increases the finite survival horizon and cannot itself constitute a Lychrel certificate.

## Reproduction
From repository root, with no downloaded external data:

    g++ -O3 -std=c++17 calculation/new_structures/agent-N01/replay20k.cpp -o /tmp/n01_replay
    /tmp/n01_replay 500 20000
    g++ -O3 -std=c++17 calculation/new_structures/agent-N01/replay_gmp20k.cpp -lgmpxx -lgmp -o /tmp/n01_gmp
    /tmp/n01_gmp 500 20000
    g++ -O3 -std=c++17 calculation/new_structures/agent-N01/front_probe.cpp -o /tmp/n01_front
    /tmp/n01_front

The first two print FNV64=3fc9680e7260649, and the final probe prints the nine-row CSV captured verbatim in calculation/new_structures/agent-N01/fronts.csv. All computations use deterministic, explicitly defined seed arrays. Local replay completed; repository-wide verify.py was not available, and Lean is not claimed.
