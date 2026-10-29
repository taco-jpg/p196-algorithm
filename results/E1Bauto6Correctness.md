# E1 bauto6 packed-state and cycle-output correctness

**PAPER PROOF** (algorithmic bug fixes); bounded COMPUTED regressions only.
The fixed `bauto6` accepts exactly 192 packed bits in three 64-bit words; no bit 192 is addressed.
It marks any truncated qualifying back-edge list `CAPPED`, preventing a quota-induced false decided negative.
Any witnessed cycle during an incomplete search is `CYC_PARTIAL len_upper_bound=`, not a claimed minimum.
Directed root paths serialize only their real edges; cycle serialization alone closes the final edge.
Reproduce: `bash calculation/decimal_frontier/lattice_formats/code/test_bauto6_correctness.sh`.
Key test: 1024 bit-191 round-trips; decimal p48 `(01)^24` with cap 1 is admitted and CAPPED.
Controls: base13 `1010010000` visits 250302 states (cap 350000, `minc=1`, depth55);
base9 `1100011000` visits 956310 states (cap 1200000, `minc=1`, depth46).
Independent Python checks every printed automaton transition and cycle closure in both controls.
Base13 candidate limits 0 and 100 report CAPPED; limit 100 also reports a validated partial cycle.
No complete base-10 exterior census, decimal Lychrel certificate, or Lean verification is claimed.
