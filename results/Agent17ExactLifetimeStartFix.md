# Agent17ExactLifetimeStartFix

**COMPUTED (bug fix).** The legacy `lifet.py` assumes its initial `Hstart` is SAT; if it is already UNSAT, its printed `max SAT = Hstart-1` can be wrong.
For decimal p=12/m=9, width=8, phase=0, `Hstart=40` is UNSAT, so the legacy script would say 39; the published exact boundary is max SAT 33, first UNSAT 34.
New `calculation/decimal_frontier/lattice_kinks/code/agent17_lifetime_exact.py` brackets both SAT and UNSAT starting horizons, bisects a monotone boundary, and never treats UNKNOWN or a search cap as an UNSAT result.
The underlying SAT model and data remain the existing `code/sat_kink.py` and `data/lat_p12m9.txt`; no shared files are edited.
Independent deterministic control: `python3 calculation/decimal_frontier/lattice_kinks/code/agent17_lifetime_exact.py --selftest` (7,029 distinct boundary/start cases, plus cap/UNKNOWN checks).
Live control: `sh calculation/decimal_frontier/lattice_kinks/code/agent17_lifetime_exact_controls.sh` (requires `python-sat`/CaDiCaL).
Expected: `EXACT: max SAT horizon=33; first UNSAT horizon=34`.
Scope: a correctness repair for horizon reporting, **not** a new centre exclusion, a decimal certificate, or a claim about 196.
