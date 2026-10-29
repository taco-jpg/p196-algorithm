# Q36 session notes

- Read AGENTS.md, OPEN_PROBLEMS.md, FOCUS_SWARM.md, the last 40 FEED/COMBINE lines on read-only #474 pages 20-25, and current #475 coordination. Migrated the existing CLAIM to #475.
- Rejected a standalone 2^5 carry-reset corollary as duplicate of R25/T01; pivoted to a phase-coupled bulk invariant not in the latest FEED/COMBINE lines.
- Derived the exact U3 local transfer from two separate carry-reset streams: normalize U and reverse(U) with their stable carry states; pair the digits with offset (gamma-1-r) mod 3.
- Exhaustive exact phase-map check: all 30 charge-zero U3 rotations remain in the 30-state set; the 12-step macro graph has three cycles of length 10; every orbit obeys the 40/80/120-step screw relations and every phase word has three distinct coefficients.
- Independent schoolbook digit-array and ordinary BigInt controls: 28,800 T* edges across q=k=20,40,80,160, all 30 U rotations and odd/even centre controls. These controls verify arithmetic/clock only, not survival or closure.
- The reproduction script also rechecks the base-9 20-edge control and base-50 16-edge control at four widths.
- Remaining gap: a real physical seam/carry-state repair with positive growth and phasewise nonpalindrome proof. No decimal certificate or ALERT.
