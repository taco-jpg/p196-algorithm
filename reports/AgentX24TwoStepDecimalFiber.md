# Agent X24: exponentially branching two-step inverse fibre

**Status: COMPUTED** for decimal controls and the 20,000-step double-engine replay; the all-parameter collision identity below also has an elementary paper proof. Neither a decimal Lychrel number nor an infinite certificate is claimed.

## Construction

Let R(N)=N+reverse_decimal(N). Pair coefficients P(N) are the symmetric sums d_i+d_(n-1-i), in least-significant-first order. Use the existing rooted decimal p8/m20 exterior B0 (length 39) and W0 (length 20), included explicitly in the code. For any integer r>=1 and binary vector σ of length k>=1, set a_i=1+9σ_i, and set Cσ=[0,a1,...,ak,ak,...,a1,0]. Let Pσ=B0 ++ W0^r ++ Cσ ++ reverse(W0^r) ++ reverse(B0). Realize its digits with low d_i=floor(P_i/2) and reflected high digit P_i-d_i. All are valid decimal digits and the first high digit is nonzero.

The normalized incoming carry to Cσ from B0 W0^r is 1, for every r>=1; the outgoing carry is 0. The upper exterior emits an extra leading digit (overflow γ=1), unchanged by σ. Both statements follow from the fixed-point carry maps of the explicit B0 and W0 and are independently checked for finite cases in the accompanying programs.

## Exact collision identity (all k, all r)

Put L=2k+2. Let e_i be 1 exactly when Cσ_i=10 and 0 otherwise, with e_0=e_(L-1)=0; symmetry gives e_(L-1-i)=e_i. Normalizing the central coefficients with incoming carry 1 yields digits y_0=1; y_i=1+e_(i-1)-e_i for 1<=i<=L-2; y_(L-1)=e_(L-2); outgoing carry 0. Overflow γ=1 shifts the reflected digit partner of local position i to L-i. Therefore y_1+y_(L-1)=1, and for 2<=i<=L-2 the sum y_i+y_(L-i)=2. The y_0 contribution and every exterior digit are also σ-independent. Hence the entire pairword P(R(Nσ)) is identical for every σ, and so R²(Nσ) is the same actual decimal integer for all σ.

Distinct σ yield distinct Pσ. Their first numerical successors are also pairwise distinct: at the highest changed power of 10, the coefficient changes by ±9 and dominates the sum of all lower changed powers. This is a genuine 2^k-element fibre of **different pairwords**, unlike digit-allocation fibres that coalesce at the first step. Every seed and every first successor is nonpalindromic, witnessed by the odd coefficient in B0 and B1.

Thus the state at any prescribed t0>=2 (in particular t0=200) has at least 2^k distinct time-zero pairwords in this explicit family, all sharing the same rooted far field. This is a delayed inverse synchronizer, not a regenerative centre.

## Computed independent replay

For r=234,k=200, there are 2^200 distinct coefficient-word seeds, each 9840 decimal digits. Two extreme centres were checked with GMP: their first successors differ, while their second successors are identical. The representative orbit was advanced for 20,000 complete reverse-add transitions; at **every** transition, GMP arbitrary-precision addition was compared with a separately implemented positional decimal digit adder. All 20,001 states were checked for palindromicity and the B_(t mod 8) prefix plus the periodic W_(t mod 8) copies. No palindrome occurred, the final length was 19,840, and at least **six whole 20-coefficient lattice periods** remained matched at every state (minimum reached at t=20000). The same conclusion applies to all 2^200 seeds because t0 and t1 are safe and t>=2 is a single shared orbit.

The independent Python big-integer oracle exhaustively tested all 2550 instances for r in {1,2,5,12,20}, k=1..8 (40 parameter sets), plus 60 random large instances including k=200. Reproduce using packet_replay.cpp (GMP development library needed) and fiber_check.py; compact trace replay_k200_20k.log includes step hashes.

## Limit

This construction branches backwards but **collapses after exactly two steps**. It does not replenish the lattice reservoir, and no infinite safe invariant or decimal Lychrel number is inferred. A different noncoalescing recurrent branching interface would be needed for that.
