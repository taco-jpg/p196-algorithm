# Agent N26: a constructive decimal centre-seam repair
**COMPUTED.** Exact scope: base 10, the listed finite seed family, the tested copy counts and finite horizons. NO infinite Lychrel certificate and NO claim of periodic centre closure.

## Seed and mechanism
Take the first 39 rooted exterior columns of the known decimal p8/rec0 lattice and c repeats of its 20 spatial-period columns; let A_c denote their phase-zero pair coefficients, least significant first. Instead of the plain final copy of the lattice block, append a 20-coefficient centre half-block
    R = [17,3,1,13,17,11,14,3,18,1,2,0,13,3,0,16,6,9,6,1].
Let P_c = A_c ++ R ++ reverse(R) ++ reverse(A_c), and realize it as an ordinary decimal seed by digit pairs (min(P_i,9), P_i-min(P_i,9)). Seed length = 118+40c digits. All data are committed in calculation/new_structures/agent-N26/.

With *the same seed length*, the plain lattice-core control uses R_plain equal to the rec0 20-column phase-zero bulk. Replacing R_plain by R changes the first time the 39-column exterior departs from its prescribed p8 schedule:
    t_plain = 88c+92,     t_repaired = 88c+252
in every individually checked c in {0,1,2,3,5,10,20,225}; the c=225 plain control is inferred from the separately observed plain shield c+1 and is not re-run here. Both use first mismatch at column 38, not a palindrome. For c=1, first mismatch goes from 180 to 340: 160 additional steps **without growing the centre width**. This is a *positive repair mechanism*, not an exclusion of another template family.

A seeded stochastic local search on these 20 centre coefficients with 39-column finite-horizon fitness finds R by iteration 2265 (initial plain score180, improved scores204,220,236,292,340). The mutation search is heuristic, not proof of optimality. Once proposed, R is independently checked using two distinct decimal implementations.

## Twenty-thousand-step result
For c=225, P_c determines an exactly specified 9,118-digit decimal positive integer. Ordinary GMP integer addition N <- N + decimal_reverse(N) confirms for each t=0..20000 that the integer is not a palindrome and the first 39 pair sums follow the 8-phase rooted exterior; digit length grows to 19,118. Even t has outer pair sum 17; odd t has leading/trailing decimal digits 1 and 7. The ordinary-integer FNV64 reproducibility hashes are step0 f25bf72a3ee4a6f1, step1000 13be423e820cd8df, step5000 b6d7ececfb299d3b, step10000 71e10db63f03c7c6, step20000 539c600da22a6c0. At t=20052 the first 39-column mismatch is seen at column 38 (same GMP checker). This step is NOT a palindrome claim after the shape stops matching.

## Reproduction from repository root
    cd calculation/new_structures/agent-N26
    g++ -std=c++17 -O3 -Wall -Wextra -Werror repair_gmp.cpp -lgmpxx -lgmp -o /tmp/n26_repair_gmp
    /tmp/n26_repair_gmp p8_rec0_rows.txt 225 20000 39 repair_core.txt
    /tmp/n26_repair_gmp p8_rec0_rows.txt 225 20060 39 repair_core.txt   # expected failure at t=20052
    python3 repair_check.py p8_rec0_rows.txt repair_core.txt --copies 1 --steps 400
    g++ -std=c++17 -O3 repair_opt.cpp -o /tmp/n26_repair_opt
    /tmp/n26_repair_opt p8_rec0_rows.txt 1 20 20000

The independent Python arithmetic advances literal little-endian digit arrays, rather than coefficient words. The GMP checker advances arbitrary-precision ordinary decimal integers. The optimiser instead advances pairword coefficients, and is intentionally independent from both final witnesses. No source code is left only in a sandbox.
