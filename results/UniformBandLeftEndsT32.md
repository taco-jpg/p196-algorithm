# UniformBandLeftEndsT32

**Claim (COMPUTED under premise (B) of ReachDiskRounds6to8, plus PAPER PROOF for two cells; 2026-11-02).** No decimal periodic left
end with left-end period T <= 32 (every binary overflow clock, every height) carries a uniform absorbing band.
- All cells except three: `ReachDiskRounds6to8` and `UniformBandLeftEndsT24`.
- (32, 0000111000110001): UNREACHABLE (COMPLETE) for the four uniform bands with period dividing 32 and for every 9-wire stream.
  Forward BFS pruned by co-reachability windows (w = 8: frontier empty after height 294, 13,065,715 orbits; w = 9 cross-check: same
  height, 6,331,756 orbits). Soundness: every interface on a bottom-to-target path has all its windows in BB_w (proof in
  `calculation/decimal_frontier/uniform_bands/round9/last_cell/FINAL_R9U.md`); wrapped windows checked on all 1.37e10 generated
  successors, 0 violations. Controls with the same code: (24, 0001) N12 twice at height 53, base 13 (55/75), base 4, (12, 0001).
- (24, 01) and (32, 01): {0} and {18} are excluded for every clock (results/E2ExtremeUniformIsolation, Lean); {6,12} on (01)^r is
  excluded for every r (#481 PRO-R02-d, PAPER PROOF); the 6-cycle band needs 9 | G, G = number of overflows per period (mass gate, #481 PRO-R02-d), and G = 12, 16 here.
**Not claimed:** 9-wire streams for (24, 01), (32, 01) (still open); T > 32; nonuniform bands; a proof of premise (B).
