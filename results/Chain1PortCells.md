# Chain1PortCells

**Claim (COMPUTED + PAPER PROOF reduction; from #476 SWARM R01A1 and #481 PRO-R01-a / PRO-R01-c, collected 2026-11-02).**
Chain 1 = decimal neutral 9-band exterior on clock (0001)^r (return after P = 4r steps) feeding an Agent6NineRailCentreRenewal centre.
1. Exterior side, all r and all widths: put a_j = (B_{4j} 9^inf)[2] - 10. Every cyclic a contains a 1 and splits into blocks S = 100,
   L = 1000 with at least five S between consecutive L (cyclically). With A = #S, B = #L: r = 3A + 4B, A >= 5B, B = r (mod 3).
   So r = 1 (mod 3) needs r >= 19, r = 2 (mod 3) needs r >= 38, and 3 | r with r < 57 forces pure S (which does not by itself force N12).
   Recheck: `exterior_census/py/khead_family.py` reproduces the K <= 7 SCC counts 4, 11, 62, 161, 332, 795, 2011 and the death of the
   all-zero branch at K = 19.
2. Centre side (PRO-R01-c): a finite reduced neutral-nine centre returning after 8 steps under 10001000 has ports exactly
   {01000101, 10111010, 01010100, 10101011} (two words up to shifts by 4); reduced widths {8, 9} and n >= 15.
3. With `ReachDiskRounds6to8` (P <= 48 excluded), the cells left for a period-8 port are P = 72 (pure S), 88, 96 (pure S), 112, 120 (pure S),
   136, 144 (pure S), 152, ...; for the period-16 port 1000100001110111: P = 96, 112, 144, 160, ...  P = 56, 64, 80, 104, 128 are excluded by 1.
**Not claimed:** any cell above; that pure S exteriors are N12 repetitions (open); centres of other periods; a certificate. Sources:
issue #476 (R01A1 feeds), #481 (PRO-R01-a, PRO-R01-c); neither is Lean-checked.
