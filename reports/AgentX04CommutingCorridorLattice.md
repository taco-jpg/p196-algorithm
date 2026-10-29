# X04: independently commuting decimal lattice and vacuum insertions

**Status: COMPUTED for four explicit finite decimal orbits. No infinite certificate.**

The rooted temporal rows B_s (39 coefficients) and W_s (20 coefficients) come from N16. The coefficient alphabet is {0,...,18}, least significant first. Define the symmetric pair-coefficient seed
P(q,z) = B_0 ++ W_0^q ++ 0^z ++ reverse(W_0)^q ++ reverse(B_0).
For i in the lower half choose digit d_i=max(0,P_i-9), upper opposing digit d_{n-1-i}=min(9,P_i), and a central digit zero if z is odd. This defines an ordinary positive decimal integer for every tested (q,z).

Let F be ordinary decimal reverse-and-add on integers; let p(N) be the symmetric opposing-digit sum word. At every t=0,...,20,000 set A_t=p(F^t(N(300,14000))), B_t=p(F^t(N(301,14000))), C_t=p(F^t(N(300,14001))), D_t=p(F^t(N(301,14001))). Define I_W,t as insertion of W_(t mod 8) after the initial 39 coefficients and reverse(W_(t mod 8)) before the final 39 coefficients. Define I_0 as insertion of one zero coefficient at the centre. The **entire words**, not just their protected prefixes, satisfy
B_t=I_W,t(A_t), C_t=I_0(A_t), D_t=I_W,t(C_t)=I_0(B_t)
for all 20,001 observed states. Both operations commute on each observed A_t. This is genuinely mixed: I_W inserts 40 coefficients at mirrored cuts; I_0 inserts one at the middle. The phase W_(t mod 8) changes with time. All four ordinary integers are independently recomputed at each step by a grade-school digit-vector update; each is explicitly checked for nonpalindromicity and the same overflow gamma_t=1 exactly when t is even.

The baseline starts at 26,078 digits, ends at 36,078 digits; minimum exact N16-rooted prefix is 1,494 coefficients; the central zero corridor is 14,000 at t=0 and never increases, reaching its observed minimum 1,286 at t=20,000. The lack of growth is a measured obstruction to a **self-renewing corridor** in this instance, not a general impossibility theorem. The overflow word is (10)^10000. The middle zero buffer and the exterior lattice coexist without interfering over this horizon, including every interleaved state. Compact checkpoints record t, decimal digit count, exact exterior-prefix length, exact central-zero length and cumulative FNV-1a 64-bit checksum (initialized 1469598103934665603; per t hash t, n, prefix, zero, then the first 16 opposing pair coefficients; multiply 1099511628211 after each input). Final checksum: ce0a760d6c88fccd.

The independent engine uses GNU GMP mpz integers, obtains each decimal representation by mpz_get_str, reverses the digit string and executes mpz_add. It recomputes baseline exterior/zero/checksum for all 20,001 states, with exactly the same final checksum, same minimum widths and no palindromes. A second GMP run checks the complete quartet and both full-word insertion identities for 2,001 states, matching the digit-vector engine's independently calculated trace hash 7f6b9420e95d151b.

**Sound conditional two-counter cycle criterion (PAPER PROOF, no such cycle found).** Suppose a finite family of valid palindromic pair-coefficient templates T_s(q,z), phase-indexed s, is equipped with *universally checked* exact ordinary-decimal edges F(T_s(q,z))=T_{s'}(q+a_s,z+b_s) for all integer q>=q_min,z>=z_min, where F denotes the well-defined next **pairword** obtained by normalizing and reflecting the symmetric coefficient word. Assume every intermediate template realizes an integer, carries an odd pair coefficient (hence cannot represent a palindromic integer), and every edge's counter updates preserve the lower bounds. If the phase graph cycles, and its total changes A=sum a_s and Z=sum b_s are both nonnegative, then every seed instance has an infinite nonpalindromic orbit. Proof: iterate the exact equalities along the finite phase cycle, apply (q,z)->(q+A,z+Z), and induct using the lower bounds; odd paired sums exclude palindromes. A sound finite checker would certify the universal edge conditions by a two-slot finite carry transducer, including the mixed insertion square, **not** merely by comparing four sample exponents. The present observations establish no universal edge, finite phase closure, or nonnegative corridor drift.

The new actionable target is a centre/interface rule with z(t+period)>=z(t), ideally through a lattice-to-vacuum conversion pulse. Our measured square identities show that adding more initial zero buffer commutes with adding rooted spatial lattice buffer for 20,000 actual updates, but neither operation supplies recurrent replenishment.

Reproduce from repository root (C++17, libgmp):
```sh
g++ -O3 -std=c++17 calculation/new_structures/agent-X04/hybrid.cpp -o /tmp/x04
/tmp/x04 calculation/new_structures/agent-N16/rows.txt 300 14000 20000
g++ -O3 -std=c++17 calculation/new_structures/agent-X04/gmp_check.cpp -lgmp -o /tmp/x04g
/tmp/x04g calculation/new_structures/agent-N16/rows.txt 300 14000 20000 --single
/tmp/x04g calculation/new_structures/agent-N16/rows.txt 300 14000 2000
```
No Lean proof, no claims after step 20,000, and no claim about the 196 orbit.
