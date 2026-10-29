# AC17: phase-8 endpoint short-junction cell

**Exact predicate.** Canonical B8/W8 from calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt; arbitrary J over 0..18 of length 3 or 4; all 30 rotations U of (9,a,18-a) with even a=0..18; arbitrary physically realizable palindromic coefficient centre C; independent q>=14,k>=100. Test exactly 120 actual decimal reverse-and-add steps from pairword P=H++C++reverse(H), H=B8++W8^q++J++U^k. A target same-J/C return P(q,k+5) requires restoration of the B8/W8 prefix at the endpoint, not at intermediate steps.

**Missing lemma:** prove or refute a full-phase-8, finite-reference-width fixed-J return that, via the phase-rotated T12 carry/insertion proof, supplies a valid all-width T* growing-U edge. No strict-per-phase W9 MDD or odd-centre-only modular gate may exclude an even-centre trajectory.
