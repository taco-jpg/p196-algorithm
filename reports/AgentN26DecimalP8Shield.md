# N26: finite-horizon decimal bulk shielding (moving-centre alternative)
**Label: COMPUTED.** Exact scope: the particular finite decimal seeds below, tested through the indicated finite horizons. This is NOT a base-10 Lychrel certificate, and neither eventual nonpalindromicity nor an infinite growing-centre invariant is claimed.

## Construction and positive result
Take the *reachable* first base-10 p8/rec0 SCC data already in calculation/decimal_frontier/lattice_formats/p8_scc.txt; a compact exact two-line copy is in calculation/new_structures/agent-N26/p8_rec0_rows.txt. The first 39 spatial rows are the rooted exterior, followed by a 20-row periodic spatial bulk. Each row has eight pair-coefficient values for temporal phases 0..7, in least-significant-first order.
For an integer c>=0 define A_c as the first-phase coefficients in those 39 rows, then c repeats of the 20 bulk rows. The initial palindromic pairword is P_c = A_c ++ reverse(A_c). For each i in the lower half, choose digit d_i=min(P_i,9), its reflected partner d_{n-1-i}=P_i-d_i. This defines a positive decimal integer N_c with 78+40c decimal digits. In particular, c=228 produces a 9,198-digit decimal integer (specified *exactly* by the construction, not stored as a giant decimal literal).
For c=228, an independent GMP integer replay confirms every N_t for 0<=t<=20000 is nonpalindromic, the first 39 pair coefficients are exactly the phase-t mod 8 rooted exterior, and lengths follow 9198+ceil(t/2). On even t the outer pair coefficient is 17 (odd, impossible for a palindrome). On odd t the most/least significant digits are 1 and 7, so N_t is not a palindrome. The overflow schedule is 10101010 repeated. This is a 20,000-step **candidate orbit family with a nontrivial pairword shape**, not a certificate for all time.

## Positive propagation mechanism and what breaks
The reflected centre of P_c is not periodic and does not close to a lattice kink. A defect emerges there and travels outwards; in a 39-column observation window, the *first* wrong row is always column 38 at phase t mod 8=4, for c=1,2,3,5,10,20,50,100,260. The first failure times (exactly measured) obey t_fail=88c+4 for these instances, reflecting a delay of 88 steps per 20 added lattice columns, or an observed drift speed 5/22 columns per time step. The c=0 edge case fails at step 2. These empirical equalities are not a proof of the same law for unbounded c. Data are in observed_lifetimes.csv.
At the first failure the **39-column template**, not necessarily the palindrome-free orbit, breaks. A future infinite certificate would need an interface/wake state that is reproduced while the centre advances at least as fast as the defect. This redirects synthesis toward an absorbing moving-boundary contract and away from stationary bounded centres.

## Reproduction (from repository root; self-contained data and code)
    cd calculation/new_structures/agent-N26
    g++ -std=c++17 -O3 -Wall -Wextra -Werror verify_gmp.cpp -lgmpxx -lgmp -o /tmp/n26_gmp
    /tmp/n26_gmp p8_rec0_rows.txt 228 20000 39
    /tmp/n26_gmp p8_rec0_rows.txt 260 20000 39
    python3 check_digits.py p8_rec0_rows.txt --copies 10 --steps 700 --watch 39
    /tmp/n26_gmp p8_rec0_rows.txt 5 443 39
    /tmp/n26_gmp p8_rec0_rows.txt 5 444 39    # expected failure at t=444, col=38
The GMP checker advances the literal integer N by parsing its decimal reversal and adding it, checks a full palindrome at every step, and verifies the first 39 pair coefficients. The Python checker independently advances a little-endian digit array, without GMP or the pairword map. Output hashes are FNV-1a over the literal *most-significant-first decimal digits* (noncryptographic reproducibility witnesses); control at c=228, t=20000 is 9c9eb1b3269ae513. A separate 260-copy 20,000-step GMP control ended with 20,478 digits, hash c9818e7a640fbc13.
