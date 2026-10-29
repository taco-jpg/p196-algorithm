# Agent3SevenCellSourceCycles

**COMPUTED.** For base-10 rec2 p=8/m=48, the exact seven-cell (21-bit) physical parity/carry graph has 124,512 admissible masks, 27,296 connected six-cell endpoints, six loops, and 97,216 independent even-length 48-cycle histogram rows.
The universal seven-cell GF(2) cyclic-zero function space has dimension **1,999,936 / 2,097,152**: 1,972,640 inadmissible-mask functions, 27,295 endpoint gradients, and one length-parity function. This is a complete seven-cell **source** classification only; g0/g1 image covariance and all-width centres remain UNDECIDED.
Every one of the 97,216 independent 48-cell witnesses is independently normalized as an ordinary 386-digit decimal reverse-and-add step; all eight genuine 406-digit rec2 phase controls pass.
Proof and exact scope: `reports/Agent3SevenCellSourceCycles.md`.
Self-contained C++17 primary, independent checker, compact rec2 data, SHA256-pinned regenerated <5 MB witness and commands: `calculation/decimal_frontier/lattice_kinks/agent3_sevencell_source/`.
Reproduce: `sh calculation/decimal_frontier/lattice_kinks/agent3_sevencell_source/run_checks.sh`.
No finite-centre no-go, base-10 Lychrel certificate, 196 claim or Lean verification.
