# Agent5Gamma0FirstDefectGate

**PAPER PROOF.** For any two distinct decimal palindromic coefficient
words of equal length, with common no-overflow and identical next pair
words, the first lower-half mismatch away from the centre (index j>=1)
obeys one of exactly four sharp carry gates: q->q' is 4->9 or 9->4 with
(lower,upper) incoming carries (1,0), or 9->14 or 14->9 with (0,1).
For the decimal p=12/m=9 bulk, **no gate** occurs at ANY spatial
residue in temporal phases 3,7,11. Therefore changing any number of
centre-side coefficients in a pure periodic-lattice baseline cannot leave
the next pair word identical if the first mismatch is safely inside the
bulk in one of those phases. This is an all-bulk-width, one-step obstruction.
Scope excludes other phases, first mismatches at the exterior/centre,
periodic-centre existence, decimal certificates, and 196.
Proof: `reports/Agent5Gamma0FirstDefectGate.md`; reproduce: `python3 calculation/decimal_frontier/lattice_kinks/code/gamma0_gate.py`.