# E1 bauto5 192-bit key boundary

Status: COMPUTED (boundary regression).

Scope: `bauto5` now accepts a packed state of exactly 192 bits; it makes no
claim about any decimal exterior census or Lychrel orbit.

The prior `>191` guard skipped the valid base-10 p=48 alternating stream
(`2p + ceil(log2 10)*24 = 192`).  The corrected `>192` guard is exercised by
`calculation/decimal_frontier/lattice_formats/code/test_bauto5_192.sh`, which
uses cap 1 and verifies the stream reaches the census rather than being skipped.
