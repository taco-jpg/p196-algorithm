# W19: two-step non-gauge packet erasure on a decimal p8/m20 exterior

**PAPER PROOF:** an exact, universal base-10 two-step pairword collision for arbitrarily many independent packets. **COMPUTED:** deterministic hash synthesis, exhaustive controls, and independent 20,000-step decimal replays. No infinite base-10 Lychrel certificate, no periodic centre, no claim about 196 and no Lean verification.

## Construction and exact statement

All coefficient words are least-significant-first. Let T(P)=pairs(norm10(P,0)), with radix normalization and reflected digit pairing. Set B and W to the 39-column root and phase-zero 20-column lattice in calculation/new_structures/agent-W19/make_seed.py, copied from the independently tracked p8 table calculation/new_structures/agent-N26/p8_rec0_rows.txt. Let C0=(14,9,9,0), C1=(0,14,9,0). Given any m>=1, k>=0, g_1,...,g_(m-1)>=1, and bits e_i, construct H_e=B W^k C_(e_1) W^(g_1) ... W^(g_(m-1)) C_(e_m) and P_e=H_e reverse(H_e). Each coefficient is 0..18 and P_e[0]=17. Form the honest decimal integer seed N_e with paired least/most significant digits min(P_i,9) and P_i-min(P_i,9).

**Theorem (elementary carry proof):** All 2^m initial pairwords P_e are different, and all 2^m first images T(P_e) are different, but T²(P_e) is the same for every mask. Accordingly the true decimal reverse-and-add integers are distinct at steps 0, 1 and 2, and coalesce at step 3. The substitutions are non-gauge: C0 mod 9=(5,0,0,0), C1 mod 9=(0,5,0,0). Unlike the earlier N28 four-step eraser in a different period-three background, this is a two-step eraser in the rooted period-eight, period-20 decimal exterior.

## Finite carry-firewall argument

Since P_e ends in coefficient 17, radix normalization always appends overflow digit 1: gamma0=1. Its first output pair coefficient is 7+1=8, so the second normalization cannot overflow: gamma1=0. The 20-column W has suffix (15,9,7,13), so all low-side carry entrances to a packet are 1, regardless of preceding packets. The upper mirror-side entrances are similarly fixed because reverse W and the central packet boundary force their cut carries. This is verified directly with floor((x+c)/10) and (x+c) mod 10 for c in {0,1}, rather than assuming periodic core behaviour.

For any nonterminal packet, replacing C0 by C1 changes T(P) only in two mirror-related three-column windows. Each window is A=(9,4,9) versus B=(4,5,4), and is immediately preceded, on the normalization scan, by coefficient 11 on one side and 10 on the other. Thus the entering carry at both windows is exactly 1, independent of all other packet choices. The resulting digit triples are A -> (0,5,9) and B -> (5,5,4), each with outgoing carry 0. The high and low window digit triples have the same reflected pair sums (9,10,9). Since spacers contain at least one complete period-20 word, distinct windows and their carry firewalls are disjoint.

For the terminal packet next to the centre, the complete differing first-image window is (9,4,9,10,0,10,9,4,9) versus (4,5,4,10,0,10,4,5,4). The preceding coefficient 11 again forces carry 1. Its normalized decimal digits are respectively (0,5,9,0,1,0,0,5,9) versus (5,5,4,0,1,0,5,5,4). Both exit with carry 0; their reflected pair sum is identical (9,10,9,0,2,0,9,10,9). Thus toggling any one bit changes T(P) but not T²(P), regardless of the other bits. Toggle masks one bit at a time to prove exact erasure for arbitrary m,k,g_i. This is a finite local arithmetic proof, not an extrapolation from the replay horizon.

The normalization and pairing conventions include the actual length overflow in gamma0 and its absence in gamma1. The whole integer at step 3 is therefore equal, not merely an exterior or hash coincidence.

## Reproducible arithmetic evidence

Command: bash calculation/new_structures/agent-W19/run.sh, from repository root, with g++ C++17, Python3, GMP and gmpxx installed. search_centre.cpp performs the width-four two-step hash join and reports the collision after exactly 3516 candidates (1229 distinct second-image keys). erasure.cpp independently evolves actual decimal digit lists and checks every one of 4096 masks for 12 packets, exterior copies k=0 and 300, including distinct P0 and P1, same P2 and identical step-three digits. independent_mixed.py checks 256 masks and unequal spacers (1,2,3,1,4,2,5) for k=0,1,3 using literal ordinary Python integers. These are full exhaustive tests for the stated finite mask sets, not exhaustive over all packet words.

For m=12, k=300, g_i=1 the seed has 12,614 decimal digits. Both the digit-vector engine erasure.cpp and unrelated GMP mpz_class engine replay_gmp.cpp replay all 20,000 reverse-and-add additions. They independently check nonpalindromicity and complete outer p8/m20 coefficient agreement up to the first mismatch at each of the 20,001 states; this prefix stays at least 1494 coefficients long. Their identical FNV1a-64 checksums over numeric LSD-first decimal digits are:

| t | digits | first mismatch | FNV64 |
|---|---:|---:|---|
| 0 | 12614 | 6039 | 9790c31438971eb7 |
| 1000 | 13114 | 5812 | 5318277174888ccf |
| 10000 | 17614 | 3767 | 28eb57634c5867a7 |
| 20000 | 22614 | 1494 | a0bd5de6bae9f568 |

The GMP checker also directly compares the extreme masks after three independent literal integer additions. The root prefix follows the eight-phase p8 schedule on every checked state, but the unmatched centre grows, so its full symbolic template does not close. The observed finite-horizon nonpalindromicity is NOT an infinite Lychrel proof. The next productive target is a periodic emitter/recharger that regenerates packets faster than the p8 guard erodes, with finite-state closure proved for all time. A larger initial band alone supplies only a longer delay.

The experiment runtime could compile and run each standalone checker but could not clone the GitHub repository or run its tools/verify.py --changed; no repository-wide verification or Lean kernel check is claimed. This commit changes only new result and isolated computation files.
