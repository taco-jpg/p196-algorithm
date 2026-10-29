# Agent3SixCellPhaseCovariance standalone reproduction

C++17 standard library only. No external dependencies, repository-relative imports, Lean or SAT solver. One-command reproduction from repository root:

    sh calculation/decimal_frontier/lattice_kinks/agent3_sixcell_covariance/run_checks.sh

Or compile/run explicitly:

    D=calculation/decimal_frontier/lattice_kinks/agent3_sixcell_covariance
    mkdir -p /tmp/agent3_six_witness
    c++ -O3 -std=c++17 "$D/primary.cpp" -o /tmp/agent3_six_primary
    /tmp/agent3_six_primary /tmp/agent3_six_witness "$D"
    c++ -O3 -std=c++17 "$D/independent_check.cpp" -o /tmp/agent3_six_independent
    /tmp/agent3_six_independent /tmp/agent3_six_witness "$D"

Expected: 188183524 six-state walks, 27296 physical six-masks, 5984 connected five-endpoints, six loops. g0/g1 image rank each 21312; g1 fixed-background rank21247, six extra pass ranks21300/21308/21310/21310/21310/21311, and the explicit rare g1 cycle gives final pivot. Independent ordinary 386-digit normalization and 406-digit eight-phase rec2 controls pass. Eight-phase covariance rank170496/kernel1926656.

Primary produces `g0_witness.bin` and `g1_witness.bin` in the requested output folder; each record is mode byte 0 or 1 followed by 48 source coefficients, plus 48 more for mode1 XOR. Each is <5 MB. The independent checker verifies every row by schoolbook decimal normalization and an opposite GF(2) pivot order; the files are regenerated and need not be shipped. Compact rec2 input data are in this same folder.

No infinite base-10 orbit or certificate, no claim about 196. No Lean verification.
