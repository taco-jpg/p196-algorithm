# S42BandParityMod11

**PAPER PROOF.** Let A(X)=Σ(-1)^i X_i for LSD-first coefficient words and P=H C reverse(H), H=B W^q J U^k, using the rooted p12/m9 B,W with A(B)=A(W)=0 (mod 11), |B| even and |W| odd. For even palindromic C, A(P)=0 identically. For odd palindromic C, zero residue for every independent q,k requires and is equivalent to:

- odd |U|: A(U)=A(C) and 2A(J)+(-1)^|J|A(C)=0 (mod 11);
- even |U|: A(U)=0 and 2A(J)+(-1)^|J|A(C)=0 (mod 11).

This extends the U3-only gate without incorrectly pruning even-length repeated bands. The U6 phase-switch candidate (7,7,11,11,9,9) ↔ (11,11,7,7,9,9) passes the corrected gate and has zero cut charge, but its tested three-state seam still fails at the W9 boundary. **Scope:** a necessary all-width modular gate, not a physical seam return or decimal Lychrel certificate. Reproduce with python3 calculation/new_structures/S42/mod11_general.py.
