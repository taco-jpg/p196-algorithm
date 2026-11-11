# BandCentresClock1000T24

**Claim (COMPUTED; 2026-11-08/09).** Two decimal bands of clock 1000 carry a non-trivial growing centre: with V = (5,11,8) (band
(11,8,5), T = 24) and C = (13,2,13), and with V = (13,7,10) (band (13,10,7), row at origin tau = 4) and C = (5,16,5), 24 steps map the
window V^m C rev(V)^m to V^(m+1) C rev(V)^(m+1), the band background being exact on both sides.
- Found by exact centre SAT (centregen.py, forced clock, N = 24, j = 1) and replayed by direct digit arithmetic (centre_replay.py: EQUAL).
  Main session (foldsim.py, own code): in each band the exact depth-2 window map has exactly one periodic orbit, of period 24, and it
  contains the lower half (13,2) resp. (5,16) of C. Fold centres (C empty) also exist for (2), (4), (6), (12), (15,15,0), (18,3,3), (8,5,5), (8,8,2).
- Band-centre scan (main session; every census band with T <= 400 as a band-background lattice, all-period closure, K <= 60, 120 s per
  phase orbit): clock 1000: 214 bands, 93 closed (centre list complete, all periods and depths), 121 open (UNDECIDED), 73 with exact
  centres; clock 10: 259 / 114 / 145 / 113; clock 00001110001: 128 / 77 / 51 / 58. (11,8,5) and (13,10,7) are open, with further period-24 centres up to depth 11.
**Missing for a certificate:** a left end (exterior plus junction) that emits one of these bands; none is known for any census band whose
period T divides the left-end period. r13a: no junction from the T12 exterior W0 with |J| <= 12 (kissat only); no rooted exterior of width <= 20 at rotation 0 (cadical only; wider widths UNDECIDED).
**Not claimed:** a template, a certificate or a Lychrel number; the open bands; bands with T > 400 or s >= 9; anything about 196.
Code: `calculation/decimal_frontier/round13/band_census/` (centregen.py, centre_replay.py, main_check/bandscan.py, main_check/foldsim.py).
