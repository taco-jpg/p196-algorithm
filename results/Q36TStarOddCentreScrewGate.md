# Q36TStarOddCentreScrewGate

**COMPUTED** — phase-resolved odd-centre necessary condition; decimal Lychrel existence remains UNDECIDED.

Let A(X)=sum_i (-1)^i X_i. For an odd palindromic centre and independently variable parities of q,k, the exact mod-11 expansion of P=H C reverse(H) gives A(C_t)=A(U_t) and 2A(J_t)+(-1)^|J_t|A(U_t)=-2A(B_t), provided 2A(B_t)+A(W_t)=0.

The rooted p12/m9 data satisfy that outer compatibility in all 12 phases. The U3 screw lemma gives U_40=rot_left(U_0,1) and U_80=rot_left(U_0,2) while the exterior phases are 0, 4, 8.

For U_0=(9,a,18-a), the required centre charges at these checkpoints are 5-2a, 2a+2, and 9 modulo 11. They are pairwise distinct for every even a in {0,2,...,18}; other starting rotations only permute the triple. A single fixed odd C therefore cannot serve all three checkpoints.

The junction target 2A(J_t) is also phase-forced; it varies in 58/60 seed/parity cases, with exact exceptions U_0=(18,9,0), |J| odd and U_0=(0,9,18), |J| even.

Scope: this constrains phase-indexed odd-centre families only. Even centres evade this mod-11 gate; varying centres remain possible. No physical seam return or all-time decimal Lychrel proof is claimed.

Reproduce: python3 calculation/new_structures/Q36/odd_centre_phase_gate.py
