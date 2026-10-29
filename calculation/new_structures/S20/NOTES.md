# Agent-S20 running notes

- Current route claim: #475 comment 6496618034, higher 3-adic carry-mass lift and sound pruning for the rooted p12/m9 120-step seam map.
- Rooted source words are cross-checked in carry3adic.cpp against calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt.
- Exact identity: for a true 120-step return with endpoint pairword mass S120=S0+270+D, K=sum 2^(119-t)c_t satisfies K=((2^120-1)/9)*(S0/2)-15-D/18. Therefore K=7*S0-15-D/18 (mod81). For stationary seams this residue requires q mod27 and k mod3 classes.
- Compiled g++ -O3 -std=c++20. Twelve 120-step cpp_int/LSD-carry cross-checks passed at q=20,40,80,160 with k=2q, including even/odd centre controls and all 30 expected overflows.
- Finite local-only census: 1,063 same-parity two-site edits of R02 J19 preserving sum(J) and alternating sum; 107 pass mod9, 48 pass mod81 and all checked higher powers at q,k=(20,40),(40,80). Exactly those 48 preserve total coefficient mass; none restores the template, best first mismatch remains seam−9. This is a finite negative result, not a global obstruction. See local IDEAS.md; do not push census as proof.
- The higher 3-adic congruences are projections of exact carry mass, not independent laws. Next work should move from mass invariants to positional two-ended interface constraints. No 240-step restored template found; no ALERT.
