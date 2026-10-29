# Agent3FiveCellPhaseCovariance: standalone reproduction

All source and compact data are in this folder. C++17 standard library only;
no downloads, SAT solver, Lean, repository-relative imports, or external data.
Run from the repository root:

    c++ -O3 -std=c++17 calculation/decimal_frontier/lattice_kinks/agent3_fivecell_covariance/primary.cpp -o /tmp/agent3_five_primary
    /tmp/agent3_five_primary calculation/decimal_frontier/lattice_kinks/agent3_fivecell_covariance
    c++ -O3 -std=c++17 calculation/decimal_frontier/lattice_kinks/agent3_fivecell_covariance/independent_check.cpp -o /tmp/agent3_five_independent
    /tmp/agent3_five_independent calculation/decimal_frontier/lattice_kinks/agent3_fivecell_covariance

Expected primary: 76 carry states, 1444 edges, 9,904,396 length-four walks;
5,984 admissible 15-bit patterns, 1,312 connected 12-bit endpoints,
six loops; source and g0/g1 image ranks all 4,672, first attained at
samples 32,700 / 8,523 / 56,576; 113,152 output words
FNV64 `567a7f76b4b8de3f`; eight-phase rec2 return; eight-phase
covariance rank 37,376, kernel 224,768.

Independent: obtains admissible patterns by independently enumerating
521,284 physical four-column coefficient/carry assignments and gluing
compatible four-column masks, rather than the primary's 9,904,396-path
76-state graph. Replays every source and output as ordinary decimal digit
normalization on 384/386/387-digit integers, using lowest-bit GF(2)
elimination (primary uses highest-bit elimination). Asserts the same three
ranks and exact first-hit indices and FNV64. Independently checks eight
406-digit positive decimal rec2 examples with actual overflow bits,
96 interior output coefficients each, and deliberately wrong-overflow
negative controls. The primary independently regenerates the exact rec2
p8/m48 cyclic bulk row orbit from W0.

Both programs enumerate 56,576 deterministic SplitMix64 physical 48-cycles,
seed `0x6a09e667f3bcc909`; for each cycle, both overflow cases are
checked. `rec2_w0.txt` and `rec2_prefix.txt` are compact exact seed data
from the repository's period-8, spatial-period-48 rec2 lattice.

Local commands both PASS; primary 14.7 s / 13 MB RSS, independent 16.2 s /
13 MB RSS. Full `python3 tools/verify.py --changed` was not available
because the local environment cannot clone GitHub (DNS unavailable).
No Lean files, decimal certificate, or base-10 Lychrel conclusion.
