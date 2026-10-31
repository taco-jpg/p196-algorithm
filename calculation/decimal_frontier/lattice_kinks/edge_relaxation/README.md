# Edge relaxation for lattice kinks (K1/K2)

Result note: `results/EdgeRelaxW9NoCentre.md`. Reproduce everything: `sh run_checks.sh` (about 10 minutes, < 2 GB, needs g++ and python-sat).

- `klib.py`: reference local rule (window of K lower-half cells with exact lattice below, free input above), validated against genuine pair-word evolution by `test_klib.py`.
- `export_tbl.py`: bulk lattice tables `lat_*.tbl` for the C++ tool.
- `kink6.cpp`: exact cyclic set of the relaxation R_K (frame moving like the centre), built incrementally from K-1 (projection lemma), plus the exact top-window centre check inside it (a complete centre search to depth K, all periods).
- `incr.py`, `exact_small.py`: independent Python versions of the incremental step and the exact centre check. `bin2txt.py` converts kink6 output.
- `relsat.py`: separate SAT encoding of R_K for a fixed period (CaDiCaL via python-sat).
- `validate_edges.py`: genuine-integer check of the transitions on the states that matter. `replay_kink.py`: big-integer replay of a reported centre.

Expected key lines: p12m9 `K=6 ... acceptingStates=0` (and K=5 `acceptingStates=978`), exact cycles 0; rec0 accepting states stay > 0.
