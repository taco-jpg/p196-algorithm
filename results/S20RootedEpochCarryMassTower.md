# S20RootedEpochCarryMassTower

**Label:** PAPER PROOF, all-width necessary condition; not a decimal Lychrel certificate.

**Exact missing-lemma contribution:** any physically rooted p12/m9 120-step return with unchanged finite-seam length must satisfy the exact weighted normalization-carry identity `K = ((2^120-1)/9)*(S0/2) - 15 - D/18`; consequently the stationary seam must satisfy `K = 7*S0 - 15 (mod 81)`, a sound fixed-point pruning clause requiring q classes modulo 27 and k classes modulo 3.

Let `S_t=2*digitSum(n_t)` and let `c_t` be the total number of actual decimal normalization carries, including terminal overflow, at step t. The exact digit-mass recurrence is `S_(t+1)=2*S_t-18*c_t`. Define `K=sum_(t=0)^119 2^(119-t)c_t`. For a target endpoint with coefficient mass `S_120=S0+270+D`, `18K=(2^120-1)S0-270-D`. Because `A=(2^120-1)/9` is integral, `S0` is even, and `18|D`, this is the exact integer condition `K=A*(S0/2)-15-D/18`.

Since `2^120=127 (mod 729)`, every exact return also satisfies `K=7*S0-15-D/18 (mod 81)`. For a stationary interface, `S0=614+120q+54k+2*sum(J)+sum(C)`, so `K=71+30q+54k+14*sum(J)+7*sum(C) (mod 81)`. This strengthens the earlier mod-9 projection and requires q mod 27 and k mod 3 classes. Combining with R05's independent mod-101 q,k mod-4 gates gives 108 q classes and 12 k classes. The higher 3-adic congruences are projections of the exact carry-mass identity, not independent laws.

**Independent physical controls:** `calculation/new_structures/S20/carry3adic.cpp` runs 12 true 120-step decimal orbits with `boost::multiprecision::cpp_int` and a separate LSD-first schoolbook carry engine. It cross-checks the rooted B34/W9 words against `calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt`, verifies every step, all 30 overflows, the exact mass recurrence, and the mod-81 gate for q=20,40,80,160 and k=2q, with the R02 J19, even-C, and odd-C controls.

**Scope and limitation:** the algebraic conditions are universal conditional necessities, not a fixed-point construction or no-go theorem. No two-epoch restored template is found; no ALERT is warranted.
