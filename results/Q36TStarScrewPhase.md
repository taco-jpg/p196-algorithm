# Q36TStarScrewPhase

**COMPUTED** — exact all-width local U3 transfer and exhaustive finite phase graph; base-10 Lychrel existence remains UNDECIDED.

For the 30 charge-zero rotations of (9,a,18-a), a=0,2,...,18, non-9 coefficients reset both carry streams. With Y− and Y+ the normalized digits of U and reverse(U) at their reset carries, Fγ(U)[r]=Y−[r]+Y+[(γ−1−r) mod 3].

Under γ_t=1 exactly at t mod 12 ∈ {0,4,8}, every protected U3 bulk state obeys U[t+40]=rot_left(U[t],1), U[t+80]=rot_left(U[t],2), and U[t+120]=U[t]; the 12-step macro graph has three 10-cycles, and every phase word has three distinct coefficients.

Cross-control: the Lean-verified base-9 merged band has m=4, Γ=4 over ten edges and no spatial phase shift; T*’s paired U3 bulk instead carries a three-state screw phase.

Scope: a necessary condition for a protected repeated U3 bulk only. It is not a physical seam return, an all-time nonpalindrome certificate, or a decimal Lychrel proof.

Reproduce from repository root: python3 calculation/new_structures/Q36/tstar_screw.py
