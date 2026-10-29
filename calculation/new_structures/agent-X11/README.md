# X11 exact golden Beatty arithmetic and proposed rotation-sheet certificate

All code and reports are in English. **Not** a decimal Lychrel certificate.

From the repository root, reproduce:

    python3 calculation/new_structures/agent-X11/torus_one_edge.py --max-width 2000
    python3 calculation/new_structures/agent-X11/rotation_bulk.py --width 1500 --steps 88 --negative-control
    python3 calculation/new_structures/agent-X11/rotation_bulk.py --width 1500 --steps 88 --phase-num 1 --phase-den 7
    python3 calculation/new_structures/agent-X11/rotation_bulk.py --width 1500 --steps 88 --phase-num 2 --phase-den 7
    python3 calculation/new_structures/agent-X11/rotation_bulk.py --width 1500 --steps 88 --phase-num 3 --phase-den 11
    python3 calculation/new_structures/agent-X11/make_seed.py 1500 > /tmp/x11-seed.txt
    g++ -std=c++17 -O3 calculation/new_structures/agent-X11/replay.cpp -lgmpxx -lgmp -o /tmp/x11-replay
    /tmp/x11-replay /tmp/x11-seed.txt 20000

The starting decimal seed is exactly `9^1500` followed by the reverse of digits `7+s_i` for `0<=i<1500`, where `s_i=floor((i+1)alpha)-floor(i alpha)`, `alpha=(sqrt(5)-1)/2`. Integer square root constructs the seed without threshold rounding. The GMP and digit-vector implementations compare the COMPLETE numeral after EVERY step. They do not call the cut-point engine. The checksums and four-phase results are in `data.json`.

The exact quadratic-number circle checker computes both left and right carries using the nearest non-nine reset, enumerates all rational-quadratic discontinuities and boundary points, and aborts if its radius 24 fails to reset. It checks *interior* pair coefficients only (indices 100..halfwidth-101), not a finite centre closure or infinite propagation.

`torus_one_edge.py` also tests an explicit exact-for-all-lengths identity in genuine base-10 digits, with both endpoints guaranteed nonpalindromic. Its output depends on two spatially reflected irrational phases. A full all-time rank-two torus verification algorithm is **described but not implemented** in the report; the finite length/growth certificate still has to be found. No Lean code or infinite decimal proof is asserted.
