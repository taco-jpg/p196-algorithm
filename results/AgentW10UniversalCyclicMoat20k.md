# Agent W10: universal 20,000-step family from cyclic-carry zero insertion
- **PAPER PROOF**, with reproducibly **COMPUTED** finite anchor: for every integer q >= 8000, the genuine decimal reverse-and-add orbit of N0 = int("5346" * q) has no palindrome at steps t=0..20000.
- Exact rational-affine polynomial identities prove the first 33 decimal transitions for every q >= 8, and all 34 states are nonpalindromic by exterior digit mismatches.
- At t=33 the decimal word is 406477799388690993172 ++ 0^(4q-30) ++ 162389106784007784593 for every q>=8.
- **PAPER PROOF**: insertion of four central zeros commutes with reverse-and-add while symmetric zero overlap absorbs carry; it preserves palindrome status whenever the output retains a centered zero band.
- **COMPUTED**: all 19,968 states t=33..20000 of q=8000 have an entirely zero centered core [t+64,n_t-t-65], with minimum 195 zero digits. q=8001 independently agrees with four additional zeros and identical exteriors at every state.
- Independent GNU MP arithmetic and full pair-word replay: previous COMPUTED result AgentW10CyclicCarryMoat20k, re-run as a positive control.
- Reproduce: bash calculation/new_structures/agent-W10/universal_run.sh; new sources symbolic_33.py, zero_insertion.cpp, fixture zero_checkpoints.tsv, and report reports/AgentW10UniversalCyclicMoat20k.md.
- **NOT CLAIMED**: an infinite base-10 Lychrel orbit, a closed certificate, anything about 196, or nonpalindromicity after t=20000.
