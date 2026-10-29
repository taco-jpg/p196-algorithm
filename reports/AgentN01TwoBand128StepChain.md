# N01: 128-step pumped decimal chain with two different lattice periods

**COMPUTED, finite-horizon scope.** No Lychrel or infinite-orbit claim; no Lean verification. The general soundness proof of the 80-state two-ended carry matrix is in reports/AgentN01LockedTwoBandDiagonal.md. This result uses that exact finite checker 128 times, with a shared unbounded gap parameter and two distinct spatial bulk periods.

## Constructive family and canonical number
The source is exactly the earlier decimal family P_0(k)=H_k ++ [9] ++ reverse(H_k), H_k=B ++ W^k ++ [9] ++ V^k, where |B|=39, |W|=20, |V|=48 and every coefficient is in 0..18; all arrays are in calculation/new_structures/agent-N01/reproduce.py. Let N_k=val_10(P_0(k)). For EVERY integer k>=12 the run proves that the next 128 ordinary reverse-and-add steps are nonpalindromic and that each of the 129 evolving symmetric coefficient words P_t(k), t=0..128, has the following precise two-band form:

    H_t(k) = B_t ++ (W_t)^(k-12) ++ J_t ++ (V_t)^(k-12) ++ C_t
    P_t(k) = H_t(k) ++ ([c_t] if c_t is present else []) ++ reverse(H_t(k))

B_t has length 160; J_t has length 616; W_t has length 20 and V_t length 48. The finite centre suffix C_t has lengths 80 initially and 112 at t=128. The centre digit c_t is present only for odd total lengths, exactly as derived from the plain-digit orbit. Both bulk words follow the decimal period-8 alternating overflow row maps and are rotated into their marked spatial cuts.

## Precise cut positions and why the two powers are independent
Let k>=12, and let h_t(k) be the lower half of the symmetric pairword P_t(k), in least-significant-first order. All positions below use zero-based halfword indices. The five chunks are separated at

    0, 160, 20*k-80, 20*k+536, 68*k-40, len(h_t(k)).

Their lengths are 160, 20(k-12), 616, 48(k-12), and |C_t|. The 20-band is the spatial row W_t rotated by 121 positions relative to its source coordinate 39, and the 48-band is V_t rotated by 496 positions relative to its source coordinate 20*k+40. Since the cuts differ linearly with k but each repeated block has its own fixed period, changing k simply inserts one whole 20-block and one whole 48-block in *disjoint* regions. At t=0 this is the literal re-association of B W^k [9] V^k (the source coefficients are explicit), valid for all k>=12, not an interpolation claim.

For each transition t->t+1 the checker independently derives B_t,J_t,C_t and the bulk rows from input k=12,13,14. It verifies exact equality of all three residual finite blocks and centre parity, and then certifies the unbounded diagonal identity by Boolean matrix products

    M(B_t,B_{t+1}) M(W_t,W_{t+1})^r M(J_t,J_{t+1}) M(V_t,V_{t+1})^r M(C_t,C_{t+1})

for EVERY r=k-12>=0. When a source odd centre becomes target even, the target's additional final halfword coefficient is checked as a terminal condition. The checker does not merely test sampled k: for each of the 128 edges the *pair of powers* has preperiod 1 and period 1, and verifies the two distinct matrix-power states r=0 and r=1 before accepting all r. The center carry consistency, actual length overflow and unequal-digit guard are part of every acceptance.

## Independent arithmetic control and finite-horizon boundary
The code also computes the ordinary integer N_20 and iterates precisely 128 times using an independently constructed big-integer decimal reversal: it asserts at *each* of 129 times the exact integer equals the value of the expected two-band coefficient word, its canonical decimal digits differ from their reversal, and the next integer is obtained by ordinary addition. This independent check does not call the carry-transducer. Source coefficient lengths are 81+136k; the k=20 source is 2801 coefficients, and its normalized integer has 2802 decimal digits.

The finite suffix |C_t| grows by 32 in 128 steps, exactly tracking one-fourth of the temporal growth in halfword length. There is no periodic return. A 34-step precursor with closer bands cut at source index 60 fails its *factorization* at t=35 because a defect reaches the first 20-band coefficient, NOT because a two-band cycle is excluded. Moving the cut to 160 and choosing k>=12 avoids that premature finite-boundary collision and enables the 128 exact edges. Future search should move the cut and normalize C_t by absorbing complete 20- or 48-period blocks, and seek an actual finite defect-state return over a compatible temporal superperiod, rather than claiming finite persistence proves an infinite orbit.

## Reproduction
Run from repository root:
    python3 calculation/new_structures/agent-N01/chain128.py
Requires Python 3 standard library and the earlier committed reproduce.py in the same directory. Source arrays and complete computation are in those two files, and the output must show 128 period-(1,1) matrix witnesses and the independent bigint control. Repository-wide verify.py and Lean kernel verification were unavailable in the local sandbox; no such check is claimed.
