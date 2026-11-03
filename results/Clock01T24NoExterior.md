# Clock01T24NoExterior

**Claim (COMPUTED under premise (B) of ReachDiskRounds6to8, 2026-11-03).** No decimal periodic left end with period 24 on overflow
clock (01)^12 (every phase, every height) reaches a 9-wire stream or a uniform band. Hence the capped census word (01)^12 of
`exterior_census/EXTERIOR.md` gives no exterior. Also, the capped word 00001110001100010000111000110001 is covered by
`UniformBandLeftEndsT32` (its targets include every 9-wire stream in every phase), so of the 54 capped words only (01)^16 remains open.
**Method.** Forward BFS pruned by co-reachability windows (w = 10, wrapped windows), frontier empty after height 3350,
500,036,674 orbits; soundness as in `uniform_bands/round9/last_cell/FINAL_R9U.md`. Controls and sources: `uniform_bands/round10/`.
**Not claimed:** (32, 01) (stopped at height 260, UNDECIDED); a proof of premise (B).
