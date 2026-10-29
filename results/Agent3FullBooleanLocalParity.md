# Agent3FullBooleanLocalParity

**PAPER PROOF.** Decimal rec2 p8/m48, g=10101010: the complete eight-phase GF(2) local covariance ansatz of **all 64 Boolean functions** of six adjacent coefficient-parity/physical-carry bits has a 124-dimensional kernel on the 2,252 reference/one-site/adjacent-pair tests (exact rank **388/512**).
The **universal zero-function** kernel has dimension **112**: 14 independent 76-state/1,444-edge carry-graph coboundaries per phase, and 400 independent unrestricted physical-word covariance rows prove exact completeness.
The remaining **12** reference-test solutions modulo universal identities are false positives; 12 explicit coefficient masks and 12 real cyclic 48-cell word/phase witnesses give an invertible violation matrix. This extends Agent3CubicParityNoGo and shows why rec2-local fitting alone cannot prove an all-width centre invariant.
No centre-width exclusion, decimal certificate, orbit of 196, or Lean verification is claimed. Full proof: reports/Agent3FullBooleanLocalParity.md.
Self-contained raw lattice, four compact certificates, deterministic generator, exact primary and independent digit-normalization checkers, commands and controls: calculation/decimal_frontier/lattice_kinks/agent3_full_boolean/.
Reproduce: python3 calculation/decimal_frontier/lattice_kinks/agent3_full_boolean/generate.py && python3 calculation/decimal_frontier/lattice_kinks/agent3_full_boolean/verify.py && python3 calculation/decimal_frontier/lattice_kinks/agent3_full_boolean/independent_check.py
