# Agent6P12M9Widths10to11
**COMPUTED.** Decimal overflow `g=100010001000`, period 12, reachable
spatial-period-9 absorbing lattice in `lattice_kinks/data/lat_p12m9.txt`.
The exact horizon-SAT free-window model (n0=400+o, o=0,1,2) excludes
indefinitely surviving centres at lower-half widths 10 and 11:
- Width 10: H=48 UNSAT for all o=0,1,2; H=40 SAT for all three.
- Width 11: o0 H=56 UNSAT (H=48 SAT), o1 H=48 UNSAT (H=46 SAT);
  o2 H=56 UNSAT (H=48 SAT).
Every infinite centre would survive all finite horizons, regardless of time period.
Controls: width-8 SAT/UNSAT horizons agree with the published Agent306 result.
Reproduce each (width, o, H) with `python3 calculation/decimal_frontier/lattice_kinks/code/sat_kink.py calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt WIDTH O hor H` (python-sat/CaDiCaL).
An independent Z3 4.13.3 Boolean encoding produced the listed UNSAT decisions
without a state cap, at the specified exact finite horizons; each solver run
used <=4.5 GB process-address-space limit; timeout/UNKNOWN never counts as UNSAT.
Not claimed: centres of wider width, other exteriors, or a base-10 Lychrel number.
