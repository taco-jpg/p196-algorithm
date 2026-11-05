# Chain6P32Chain8T48

**Claim (COMPUTED under premises (A) and (B); 2026-11-04).**
- Chain 6, clock (01)^16, P32: the 128 charge-0 cycles are unreachable (backward cone with A_8, frontier empty after layer 268,
  63,734,031 orbits).
- Chain 8, clock G = 110001001000: no 9-wire stream of any kind at T = 12, 24 (unfiltered complete search); at T = 48 no exterior
  reaches the PR381 centre stream (BB_10-filtered, frontier empty after height 78, 11,790,840 orbits, 0 window violations).
- Chain 8 K-head lifting: roots [9,17,4] and [9,17,17] have no periodic exterior of any width (core empty at K = 11, 27); root
  [9,17,5] has none of width <= 22.
Controls: N12 found at height 53 through the same filter at T = 12, 24; the lifting finds the base-4 clock-100 exterior at K = 7.
**Method.** `calculation/decimal_frontier/round11/chain6_chain8/FINAL.md`.
**Not claimed:** chain 6 P96 (backward cone TOO_BIG; BB_10 is target-independent); chain 8 T = 72 (run still going at commit time)
and all k; root [9,17,5] at width > 22.
