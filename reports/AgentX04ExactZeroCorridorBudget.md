# X04: exact carry budget for a central zero corridor

**Status: PAPER PROOF**, all positive decimal integers for one reverse-and-add step with a nonempty maximal central zero corridor. **COMPUTED** finite tests described below. The proof is self-contained and does not depend on period-eight data.

Let N have n decimal digits d_0,...,d_(n-1), least significant first and d_(n-1)>0. The symmetric pair coefficients are P_i=d_i+d_(n-1-i), in {0,...,18}. Let z>0 be the length of the *maximal* centred run of zero coefficients. There is an index a=(n-z)/2 >=1 with P_i=0 on [a,n-1-a] and h=P_(a-1)=P_(n-a)>0. Define carries c_0=0 and c_(i+1)=floor((P_i+c_i)/10). All carries belong to {0,1}. Let c=c_a, gamma=c_n, and normalized output digits e_i=(P_i+c_i) mod 10 for i<n, with e_n=1 if gamma=1. The output is the ordinary decimal integer F(N)=N+reverse(N), of length n+gamma. Let z' be its maximal centred zero-pair run length (possibly zero).

**Exact law:**
  if gamma=1, z'=z-1;
  if gamma=0, z'=max(0,z-2c).

**Proof.** Since P_i=0 for a<=i<=n-1-a, e_a=c, e_i=0 for a<i<=n-1-a, and the carry entering the next position n-a is zero. Consequently e_(n-a)=h mod 10. If h=10, the carry entering a is necessarily c=1 (because P_(a-1)+c_(a-1)>=10). Otherwise h mod 10>0. Hence the boundary sum c+(h mod 10) is *strictly positive* in all cases.

When gamma=1, the output pair at index i is e_i+e_(n-i). Thus the output index a is nonzero, exactly c+(h mod 10), while every opposing pair at indices a+1,... inside the middle is zero. The middle run is precisely n+1-2(a+1)=z-1, including z=1 giving zero.

When gamma=0, the output pair at index i is e_i+e_(n-1-i). If c=1, its index a is nonzero (e_a=1), whereas the innermost z-2 positions are zero, giving z'=max(0,z-2). If c=0, the output is zero on the entire old interval; its preceding index a-1 is nonzero because e_(n-a)=h mod 10>0 (h=10 would force c=1), so z'=z. These cases exhaust the possibilities. QED.

The law makes the cumulative quantity z_t + sum_(j<t)gamma_j nonincreasing **as long as z_j>0**. In particular, any proposed infinite reverse-and-add certificate whose template retains a positive central zero corridor at every state and whose overflow word has infinitely many ones is impossible, independently of any exterior choice. This is a wall-budget constraint, NOT a proof that decimal Lychrel numbers do not exist: when z reaches zero, a new positive run may later be born. The period-eight lattice overflow 10101010 has infinitely many ones, so it cannot support an indefinitely positive central-zero corridor with zero-width expansion per cycle.

**Constructive redirect:** search nonzero absorbing or carry-active corridors, off-centre sectors, or growing-centre transducers where the effective shield is not a permanently positive zero-pair interval; any true decimal certificate must renew a *different* conserved resource rather than increasing this one. This directly changes the X04 attempted lattice+central-zero construction.

**Independent controls (COMPUTED only):** C++ `zero_monotone.cpp` exhaustive scan of every positive integer with 2..7 digits that has z>0 (918,180 cases), plus 1,000,000 seeded random 8..199-digit numerals with constructed central-zero runs: 1,918,180 formula checks, gamma=0 in 865,604, gamma=1 in 1,052,576. Sharpness witnesses 100 (gamma0, z'=z) and 109 (gamma1, z'=z-1). Python `zero_budget_python.py` separately builds 100,000 numeric strings, uses actual arbitrary-size `int(s)+int(s[::-1])`, and checks the same formula; 50,917 length increases, no mismatches.

Reproduce from repository root:
```sh
g++ -O3 -std=c++17 calculation/new_structures/agent-X04/zero_monotone.cpp -o /tmp/x04z
/tmp/x04z
python3 calculation/new_structures/agent-X04/zero_budget_python.py
```
This result does not claim a Lean proof, a complete no-go for nonzero corridors, an all-time property after z=0, or anything specific to 196.
