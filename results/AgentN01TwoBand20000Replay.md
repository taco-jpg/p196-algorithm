# AgentN01TwoBand20000Replay
**COMPUTED:** one explicit decimal two-band seed N_500 (periods 20 and 48) survives **20,000** ordinary reverse-and-add additions, all 20,001 canonical integers nonpalindromic.
All 20,001 pairwords have precisely checked 50-period W_t and 20-period V_t chunks at fixed disjoint locations, in a full symmetric two-band factorization; the remaining junction and core are not bounded.
The alternating length-overflow clock persists; final canonical decimal length 78,082; FNV64 of reversed final decimal digits `3fc9680e7260649`.
Independent C++ decimal digit-array plus coefficient normalization and GMP `mpz_class` big-integer arithmetic both verify all 20,000 steps and final hash.
The bulk fronts shrink: maximal intact W/V runs at time 20,000 are 5,455/8,862 coefficients. This is neither a temporal template cycle nor proof of a decimal Lychrel number.
Reproduce: `g++ -O3 -std=c++17 calculation/new_structures/agent-N01/replay20k.cpp -o /tmp/n01replay && /tmp/n01replay 500 20000`.
GMP cross-check: `g++ -O3 -std=c++17 calculation/new_structures/agent-N01/replay_gmp20k.cpp -lgmpxx -lgmp -o /tmp/n01gmp && /tmp/n01gmp 500 20000`.
Front data: `g++ -O3 -std=c++17 calculation/new_structures/agent-N01/front_probe.cpp -o /tmp/n01front && /tmp/n01front`.
Data/derivation: calculation/new_structures/agent-N01/replay20k_expected.json; calculation/new_structures/agent-N01/fronts.csv; reports/AgentN01TwoBand20000Replay.md.
