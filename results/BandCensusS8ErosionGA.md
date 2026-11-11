# BandCensusS8ErosionGA

**Claim (COMPUTED census, with the generalised erosion Theorem GA as PAPER PROOF; 2026-11-08).** The decimal periodic bands of word
length s <= 8 (primitive, up to rotation) number 265 for clock 1000, 284 for clock 10 and 161 for clock 00001110001 (periods up to 10,752).
- Band: cyclic word V in {0..18}^s, every row with a letter != 9, returning under the periodic row maps of the clock (FINAL.md section 1);
  enumerated as the cycles of the period map on all 19^s words (bitset iteration), complete for s <= 8. The main session's own recount gives identical counts and period multisets for every (clock, s); SAT all-solutions enumeration agrees on 4 small (clock, s, T) cases.
- Theorem GA (generalises round 12's Theorem A from U3 to any band): if the one-epoch left-restoration instance L(V,W,tau,R,M) is UNSAT
  for every rotation W, then under the forced clock the band start moves right at every epoch, so the band has no stationary left
  junction with any exterior. Variants GA* (multi-epoch), GR / GR* (right ends, comoving centres) in FINAL.md section 2.
- ALLUNSAT for all rotations (3 solver/encoding pairs each; 20 instances re-checked with the main session's own encoding): clock 1000:
  (0), (18), (18,9,0), (9,18,9,0), (5,2,1), (11,9,2), (16,12,16,2,6,2); clock 10: (0), (18), (12,9,6), (9,12,6), (9,18,9,0),
  (12,9,9,6,18,9,0); clock p11: (0), (18). U3 = (18,9,0) erodes already per 40-step epoch (30/30 words UNSAT, each in at least 2 solver/encoding pairs).
Controls: the T12 row W0, the p8 lattice rows and the base-9 certificate rows pass L (SAT); 78 genuine big-integer validations of the encodings.
**Not claimed:** s >= 9 (W0, the p8 rows); the L/R sweep is incomplete (timeouts and NOT RUN ranges, FINAL.md section 8); bands passing L and R (necessary tests only); anything about 196.
Code: `calculation/decimal_frontier/round13/band_census/` (census/, bandsat.py, bandsat2.py, bandval.py, FINAL.md, main_check/).
