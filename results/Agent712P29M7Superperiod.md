# Agent-712: decimal p29/m7 absorbing cyclic bulk
**COMPUTED** — complete finite functional graph for base 10, primitive overflow `g=00001110001000110001000110001` (p=29, S=10), reflected axis-zero spatial period 7, every temporal multiplier.
All `19^4=130321` initial rows were processed by two independent exact cyclic-carry solvers over 7 periods (203 steps); both agree at every state. One all-9 row is excluded as neutral.
The 203-step map has 11 recurrent cycles (78 states); seven have genuine primitive spatial period 7 (68 states), with cycle lengths `2,2,2,6,6,24,26`.
Independent Python graph traversal, exact temporal replay, 71 big-integer interior-pairword checks and mod-9 cut-charge comparisons pass.
Five primitive-m7 cycles have zero mod-9 charge at their minimal 6-divisible time-ring lift; two have nonzero charge 3 and 6 (scoped obstructions, not all-superperiod exclusions).
Mandatory b9 `1100011000` full-SCC control (956310 states, m4 at depth61) and b13 `1010010000` (250302 states, singleton depths55/75) reproduced.
Details and seven representatives: `reports/Agent712P29M7Superperiod.md`.
Reproduce: `bash calculation/decimal_frontier/lattice_formats/code/agent712_p29_m7_reproduce.sh`.
Source: `calculation/decimal_frontier/lattice_formats/code/agent712_p29_m7.cpp`, `agent712_p29_m7_check.py`; bounded nice single-process execution, no state/time caps in the bulk census.
No canonical-root connection, finite decimal certificate, 196 assertion or Lean verification is claimed.
