# Q36 target: phase-resolved odd-centre gate

Using the exact local U3 transfer in tstar_screw.py, prove the phase-specific
mod-11 gate for every phase-indexed T* family with independently variable q/k
parities and an odd palindromic centre:
A(C_t)=A(U_t) and 2A(J_t)+(-1)^|J_t|A(U_t)=-2A(B_t) (mod 11), where
A(X)=sum_i (-1)^i X_i and the p12 root satisfies 2A(B_t)+A(W_t)=0.

Combine the U3 screw phase U_(t+40)=rot_left(U_t,1) with exterior phases 0,4,8.
The centre-charge requirements at t=0,40,80 must be pairwise distinct for
every charge-zero U3 start. Check the complete finite state set and the
modular parity equations exactly.

Remaining problem: find actual phase-indexed J_t/C_t words satisfying the
required residues and all exact carry equations, or prove no such trajectory
exists. Even-centre phases are not excluded by this mod-11 gate.
