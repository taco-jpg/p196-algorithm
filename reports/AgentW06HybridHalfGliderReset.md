# Agent W06: 44-step decimal interface and 0/9 synchronizing junction

**Status: COMPUTED, exactly the finite decimal scope below.** No infinite Lychrel number, certificate, closed regenerating interface, or result about the 196 orbit is asserted.

## Canonical seed and boundary
All pairword coefficients are least-significant first, each in 0..18. Use the existing p8/m20 rec0 exterior from N10: B=(17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13) and W=(17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13). Put H=B++W^320++9^180, P0=H++[18]++reverse(H), a **13,239-digit** valid decimal seed. Split each mirrored p as (min(9,p),p-min(9,p)), and the central 18 as decimal digit 9. Let n_t=reverse_add^t(n0); P_t its actual canonical palindromic pairword.

The clock is gamma=10101010. For each actual n_t define h_t as the **first pairword mismatch** against the 39-cell temporal B_t root followed by the periodic 20-cell W_t row, including the root in the index; K_t=P_t[h_t-40:h_t+80] (120 coefficients). W_t is the exact established p8/m20 temporal row, whose t+4 phase is a 10-cell spatial rotation of row t.

## Positive half-glider and independent 20k replay
Two arithmetic implementations run every state t=0..20,000: (1) a C++ positional digit vector using direct schoolbook reverse-and-add, and (2) an independent GMP mpz_class implementation using canonical decimal-string reversal and addition, with **separately embedded** temporal phase rows. Each checks nonpalindromicity of all 20,001 numbers, expected alternating length increments, and exact rooted phase agreement. Both report h0=6439, h898=6234, h20000=1894, final decimal length **23,239**, and the identical FNV-1a 64-bit hash of the entire most-significant-first final digit string **a2032887cdcb0524** (offset 1469598103934665603, multiplier 1099511628211).

For **every** 898<=t<=19,956 (19,059 comparisons), both independently check the literal 120-symbol equality **K_(t+44)=K_t** and the displacement **h_(t+44)=h_t-10**. This improves the known 88-step/-20 local interface to a measured *44-step/-10* return on this buffer species, rather than extending its lifetime by an unsupported extrapolation. The rooted W reserve still shrinks: 6439 -> 1894 mismatch index. No closed global symbolic edge or centre invariant has been found.

## Exhaustive finite interface/synchronizer table
Change the uniform buffer symbol in H from 9 to each of {0,4,8,9,12,16,18}, with K=120 lattice blocks, L=180 buffer cells and centre coefficient 18. Each of the seven seeds has 2,501 canonical digit-array states, no palindrome, zero clock deviations, and an exact K_(t+88)=K_t, h_(t+88)=h_t-20 over t=start..2412, with start values 898 (0/4/9), 1046 (8), 1003 (12), 1074 (16), 1098 (18). Values 0/4/9 additionally have the 44/-10 return for t=898..2456. Adding a **three-block inner W sector** behind the buffer produces exactly the same h_t and K_t at all t=0..2500 in each of the seven species (14 actual orbits).

A stronger interface reset was found: for the 0-buffer and 9-buffer variants, their **entire** P_1 words are equal, hence their **entire** canonical n_2 integers are equal, even though the initial integers are different. The separate reset_sweep.py exhaustively checks 16,500 cases with k=0..10 outer W blocks, L=1..50, centre C in {0,2,...,18}, inner W blocks in {0,1,3}. In **13,750** cases the full P_1 words agree and therefore n_2 coincide; in **2,750** they do not. On this finite box, the success predicate is exactly (C>=10 or inner>=1), with **zero classification discrepancies**. It also cross-checks 120 reproducibly selected cases by ordinary Python big integers, and tests an expected non-merger. This is a finite classification, **not** a proof for arbitrary k,L or arbitrary contexts. In the 2,500-step exterior-interface sweep, the 0 and 9 moving windows agree for all t>=1, while 4 and 9 agree for all t>=832.

## Proposed construction direction, explicitly undecided
Use the synchronizing 0/9 conversion to quotient junction carry states; the 44-step/-10 interface is a smaller candidate macroedge than the earlier 88-step/-20 wall. For an **infinite certificate**, one must still exhibit a second interface or regular central language that replenishes at least 10 W coefficients per 44 steps, and prove the whole pairword/number update, palindrome guard, and length constraints **for all unbounded band lengths**, not just 120 local coefficients for a finite trajectory. A moving glider by itself is not such a certificate.

## Reproduction and controls
From repository root:

~~~sh
g++ -O3 -std=c++17 calculation/new_structures/agent-W06/interface44.cpp -o /tmp/w06
/tmp/w06 long
/tmp/w06 sweep
g++ -O3 -std=c++17 calculation/new_structures/agent-W06/verify_gmp.cpp -lgmpxx -lgmp -o /tmp/w06gmp
/tmp/w06gmp 320 20000 180 9
python3 calculation/new_structures/agent-W06/reset_sweep.py
~~~

Source/data: calculation/new_structures/agent-W06/{interface44.cpp,verify_gmp.cpp,reset_sweep.py,observations.json}. Controls: 56+65=121 palindrome, deliberately incorrect -9 glider shift, 0/9 non-merger at centre C=0, independently constructed GMP phase rows, matching complete 23,239-digit final-number hashes. Repository-wide tools/verify.py --changed was unavailable from this sandbox (git clone blocked by GitHub DNS), and no Lean claim is made.
