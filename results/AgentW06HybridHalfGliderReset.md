# AgentW06HybridHalfGliderReset
- **COMPUTED**, finite decimal orbits only; no infinite base-10 Lychrel certificate.
- Explicit p8/m20 seed pairword H++[18]++reverse(H), H=B++W^320++9^180, 13,239 digits.
- Independent digit-array and GMP decimal-string reverse-add: **20,000** steps, no palindrome, overflow 10101010, final 23,239 digits, hash **a2032887cdcb0524**.
- For all t=898..19,956: exact 120-coefficient moving window return at **44 steps / -10 cells** (19,059 checks); rooted lattice shrinks, so not a certificate.
- Seven uniform-buffer interfaces (0,4,8,9,12,16,18) admit finite 88-step/-20 returns; 0/4/9 also 44-step/-10; 14 x 2,500-step control orbits.
- Exact finite **0/9 buffer synchronization**: 13,750/16,500 parameter combinations produce equal full P1 and hence equal N2; 2,750 cases do not. No all-length theorem claimed.
- Code: calculation/new_structures/agent-W06/{interface44.cpp,verify_gmp.cpp,reset_sweep.py,observations.json}.
- Details and exact reproduction: reports/AgentW06HybridHalfGliderReset.md.
