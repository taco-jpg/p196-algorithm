# Agent18P8Rec2Width11
**COMPUTED.** Decimal p=8 `g=10101010`, spatial-period-48 rec2 bulk:
no indefinitely surviving centre of lower-half free-window width <=11
in any `n0=400+o`, `o=0..3`, under the exact margin-6 window model.
Horizon-mode SAT is UNSAT at `(o,H)` = `(0,50),(1,55),(2,58),(3,64)`.
These are sufficient exclusion bounds, not exact maximal lifetimes.
A periodic centre of any period would survive every horizon.
Width-8 control SAT maxima `(28,27,27,37)` and first UNSAT
`(29,28,28,38)` reproduced; width-11 SAT at H=40 for all phases,
with independent 40-step ordinary big-integer replay, no palindromes.
Code: `calculation/decimal_frontier/lattice_kinks/code/agent18_width11_*.py`.
Inputs: existing `data/lat2.txt`; new `data/agent18_width11_witness.json`.
Reproduce: `nice -n 10 python3 calculation/decimal_frontier/lattice_kinks/code/agent18_width11_reproduce.py`
Z3 system library required; exhaustive SAT runs use <=8 GiB per worker.
No claim for width >=12, an unrestricted centre, or a decimal Lychrel number.
