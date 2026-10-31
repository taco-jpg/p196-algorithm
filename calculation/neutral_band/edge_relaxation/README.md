# Neutral band: no cap for the carry streams of the known decimal exteriors

Result note: `results/NeutralBandNoCapAllPeriods.md`; details: `reports/NeutralBandNoCapAllPeriods.md`. Reproduce: `sh run_checks.sh`.

- `up4.cpp`: upward transfer construction of periodic left ends (exteriors) under a 9-wire, complete when the interface set repeats.
- `wiretbl.py`: a wire carrying a fixed stream as a period-1 "lattice" table (cells 9, up carry = stream, down carry = complement).
- kink6 (from `calculation/decimal_frontier/lattice_kinks/edge_relaxation/kink6.cpp`): exact cyclic sets of the edge relaxation R_K with the
  frame moving like the centre, built incrementally (projection lemma), plus the exact top-window centre check.
- `wirebudget.cpp`: same with a frame allowed at most B shifts in any L steps (covers every drift in [0, B/L], all periods).
- `wirelat.py`: independent Python reference (klib rule, own SCC, own exact check). `edgesatg.py`: fixed-period SAT cap test.

Expected key lines: up4 p11 `NEW STREAM at height 29: 00111010011`, `RESULT CYCLE ... 60 ... 59`; p12 three streams at height 53, cycle 74/71.
Control: `EXACT CYCLE length 16 NON-LATTICE` at K=4 and K=5. kink6 accepting states p11 85, 151, 131, 0 (K=3..6); each p12 stream
63, 103, 69, 0; exact cycles 0. wirelat reproduces these. wirebudget: control stays > 0; p11 9617, 17848, 14814, 7782, 0 (K=3..7);
each p12 stream 346, 513, 437, 43, 0. edgesatg: T=11 K=8 `0:- 1:- 2:- 3:S 4:S 5:S`; T=22 K=12 UNSAT for shifts 0..6, SAT from 7.
