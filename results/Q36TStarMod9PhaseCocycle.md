# Q36TStarMod9PhaseCocycle

**PAPER PROOF** — all-width phase-resolved necessary condition; decimal Lychrel existence remains UNDECIDED.

Let sigma(X)=sum_i X_i. For a decimal orbit, sigma(P_t)=2N_t (mod 9) and N_(t+1)=N_t+reverse(N_t) implies sigma(P_(t+s))=2^s sigma(P_t) (mod 9).

At rooted p12/m9 phases 0,4,8, (sigma(B),sigma(W)) mod 9 is (1,6),(5,6),(3,6). Every U3 word here has sigma(U)=27, so its repeated band vanishes mod 9.

For q_t=q+delta_t and K_t=2sigma(J_t)+sigma(C_t), exact phase expansion gives K_40=7K_0+4-3delta_40 and K_80=4K_0+2-3delta_80 (mod 9).

Hence K_40=K_0+1 and K_80=K_0+2 (mod 3), independent of centre parity and fixed integer q-shifts. A fixed J/C seam cannot span checkpoints 0,40,80.

Scope: affine phase families q_t=q+delta_t with sigma(U_t)=27. This is a necessary condition, not a physical seam return or a decimal Lychrel proof.

Reproduce: python3 calculation/new_structures/Q36/mod9_phase_cocycle.py
