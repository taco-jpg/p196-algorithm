# Q36 session notes

- Read AGENTS.md, OPEN_PROBLEMS.md, FOCUS_SWARM.md, the last 40 FEED/COMBINE lines on read-only #474 pages 20-25, and current #475 coordination. Migrated the existing CLAIM to #475.
- Rejected a standalone 2^5 carry-reset corollary as duplicate of R25/T01; pivoted to a phase-coupled bulk invariant not in the latest FEED/COMBINE lines.
- Derived the exact U3 local transfer from two separate carry-reset streams: normalize U and reverse(U) with their stable carry states; pair the digits with offset (gamma-1-r) mod 3.
- Exhaustive exact phase-map check: all 30 charge-zero U3 rotations remain in the 30-state set; the 12-step macro graph has three cycles of length 10; every orbit obeys the 40/80/120-step screw relations and every phase word has three distinct coefficients.
- Independent schoolbook digit-array and ordinary BigInt controls: 28,800 T* edges across q=k=20,40,80,160, all 30 U rotations and odd/even centre controls. These controls verify arithmetic/clock only, not survival or closure.
- The reproduction script also rechecks the base-9 20-edge control and base-50 16-edge control at four widths.
- Remaining gap: a real physical seam/carry-state repair with positive growth and phasewise nonpalindrome proof. No decimal certificate or ALERT.
- Extended the screw-phase result with a phase-specific odd-centre mod-11 gate. Direct expansion of A(P) gives A(C_t)=A(U_t) and 2A(J_t)+(-1)^|J_t|A(U_t)=-2A(B_t), assuming both q/k parities occur and the root compatibility 2A(B_t)+A(W_t)=0 holds.
- Exhaustively checked the mod-11 truth table over all 12 exterior phases, 30 U states, both J parities, and all residues A(J), A(C). At checkpoints 0/40/80 the required centre charges are always pairwise distinct; the J target is constant only in two recorded cases.
- Scope guard: this is an odd-centre condition only. It does not rule out even-centre phases, and a 120-edge certificate may vary J/C at the 40/80 checkpoints.
- Derived the all-centre mod-9 checkpoint cocycle. Since sigma(P_t)=2N_t (mod 9) and N advances by factor 2 mod 9, the 40/80-edge phase shifts force K40=7K0+4-3delta40 and K80=4K0+2-3delta80 mod 9 for K=2sigma(J)+sigma(C).
- Exact root sums at phases 0/4/8 are B=(307,311,264), W=(60,60,60); every U3 word has sum 27. Therefore K must advance by +1 and +2 mod 3 at checkpoints 40/80, for odd and even centres alike.
- This extends the endpoint-only mod-9 ledger: any fixed J/C or constant K seam is impossible across 0/40/80. The remaining search must implement the charge transport with actual carry-valid J_t/C_t words.
