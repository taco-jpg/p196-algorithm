# AgentX05AffineTwoCorridor20k
**COMPUTED.** Base-10 finite-horizon family `N_0(A,B)=val_10(9^(A+1) 18^2 9^B 0^2 9^B 18^2 9^(A+1))` (LSB-first coefficients).
For every **independent** A,B>=20000, exact affine-RLE carry/zip symbolic rules certify 20,000 real reverse-add transitions with no palindrome at times 0..19,999.
**Independent GMP ordinary-decimal replay:** A=20000,B=20017, all 20,000 arithmetic steps; every digit word agrees with exact symbolic pairword; no palindrome.
After step 20,000: 88,291 decimal digits (sample) and 51,821 symbolic terms; two symmetric independent 0-corridors length A-12048 and B-12070 survive.
All-length symbolic validity uses fail-closed affine sign/positivity guards, not finite sample extrapolation.
Reproduce: `bash calculation/new_structures/agent-X05/replay20k.sh` (C++17/GMP/Python3).
Code and compact checkpoint SHA-256 data: `calculation/new_structures/agent-X05/{affine_rle_fast.cpp,replay20k.sh,evidence20k.json}`.
Proof of exact local arithmetic/scope/limitations: `reports/AgentX05AffineTwoCorridor20k.md`; previous general symbolic soundness in `reports/AgentX05AffineTwoCorridor.md`.
No closed cycle, infinite Lychrel proof, Lean verification, or claim specific to 196.
