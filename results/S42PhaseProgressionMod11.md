# S42PhaseProgressionMod11

**PAPER PROOF.** For a phase-labelled seam whose fixed mode sees only k=k0+d n, the odd-centre mod-11 gate must be imposed on that reachable progression, not automatically on every k. With A(B)=A(W)=0, even C is unrestricted. For odd C and odd-length U, odd d forces both usual Q39 equations; even d requires only the single equation at k0's parity. For odd C and even-length U, the exact conditions are:

- 2A(J)+(-1)^|J|(2k0 A(U)+A(C)) = 0 (mod 11);
- 2d A(U) = 0 (mod 11).

Thus A(U)=0 follows only when 11 does not divide d. This prevents over-pruning a phase-cycled family whose same mode revisits only a k-progression with increment divisible by 11. The theorem is a necessary modular gate, not a physical seam return or decimal Lychrel certificate. Reproduce with python3 calculation/new_structures/S42/mod11_general.py.
