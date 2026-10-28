# Agent3FourStepSource

**PAPER PROOF.** For any genuine decimal reverse-and-add orbit starting
at even digit length with four overflow bits `1010`, the physically
correlated four-step midpoint source `22(2Z0+Z1)+2Z2+Z3` is `0 mod 9`,
for **every** centre width. The same holds over any `(1010)^k` segment.
For rec2 p8/m48, this makes the existing mod-9 centre-source return
condition automatically true in initial length classes `o=0,2`;
it cannot exclude a centre in those classes. No decimal certificate.
The bound is sharp at rec2 free half-width 5: all 11 multiples of 9
modulo 99 occur among 2,476,099 exact physical four-step centre words
in each even-length class (odd-length classes: 90 residues each).
Proof: `reports/Agent3FourStepSource.md`.
Reproduce: compile/run `calculation/decimal_frontier/lattice_kinks/code/agent3_fourstep_source.cpp` as in report.
