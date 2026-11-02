# ReachDiskRounds6to8

**Claims (COMPUTED, Studio rounds 6-8, 2026-11-01; in the left-end interface graph of `uniform_bands/`).**
1. Uniform bands: for every binary overflow clock with left-end period T <= 31, and T = 32 except 2 tasks, no left end of any
   height reaches a uniform absorbing band; the only 9-wire streams are N11's and N12's (127 heavy tasks, 124 COMPLETE).
   Open: (24, 01), (32, 01), (32, 0000111000110001).
2. Chain 1 (neutral 9-band, clock 1000, Agent6 centres): no exterior emits the port words 01000101 / 10111010 /
   1000100001110111 at P = 24, 32, 40 (forward BFS, COMPLETE) or P = 48 (window-filtered backward cone, COMPLETE).
3. Chain 6: none of the 1024 cut interfaces of the 128 period-32 charge-zero self-mirror m = 8 cycles on clock (01)^8 is reachable
   (window-filtered backward cone, COMPLETE). Positive control: the same method recovers the base-9 LatticeBand left end at height 61.
4. EXTERIOR.md capped words: 51 of 54 decided; accepted streams only p11, p12, p22 (agrees with the census).
**Premises.** (a) Window filter (w = 10, w = 8 on clock 01): PAPER PROOF that it over-approximates the reachable set, plus 0
violations over every reachable successor at T = 12/24/32/40 (clock 0001) and T = 16 (clock 01). (b) reach graph = Agent120
exterior system: checked (bases 2-4 all orbits, decimal census), NOT proved.
**Not claimed:** P >= 56; chain-6 cycles of temporal period 96-608; any certificate. No candidate found. Details: `reports/ReachDiskRounds6to8.md`.
