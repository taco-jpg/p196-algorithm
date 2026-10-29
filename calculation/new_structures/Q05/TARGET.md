# Q05 target: T* rooted renewal obstruction unification

Exact target: prove a necessary-condition theorem for every all-width rooted p12/m9 T* return with 120 physical decimal steps, fixed W9 exponent q, and U3 exponent k→k+5. The theorem must jointly preserve (i) actual two-ended carry and overflow labels, (ii) nonnegative net drift for every unbounded run, (iii) the exact first-contact packet law and adjacent-support obstruction, (iv) the finite-reservoir budget and root reachability, and (v) centre parity at every phase.

New sublemma: for every physical template edge
P_t = H_t ++ C_t ++ reverse(H_t), H_t=B_t ++ W_t^q_t ++ J_t ++ U_t^k_t,
with lengths |B_t|=34, |W_t|=9, |U_t|=3, the actual overflow gamma_t satisfies
gamma_t = 18 Δq_t + 2 Δ|J_t| + 6 Δk_t + Δ|C_t|.
Therefore |C_(t+1)| = |C_t| + gamma_t (mod 2). On the 120-step T* clock, centre parity flips exactly 30 times. This eliminates any route that holds centre length/parity fixed at every phase.

Acceptance criteria: a proof with explicit quantifiers and correct scope, plus independent ordinary-integer controls at q=20,40,80,160. No finite-horizon survival statement, no generic graph theorem without a T* instance, and no global decimal existence claim.
