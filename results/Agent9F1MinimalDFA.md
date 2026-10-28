# Agent9F1MinimalDFA
**PAPER PROOF / exact finite-state computation.** The base-10 first-coordinate
F1 language of time-rooted cyclic overflow words is recognized by a minimal
241-state deterministic finite automaton (104 accepting states), starting
from the 434 reachable Boolean-relation states in the existing enumerator.
Partition refinement splits as 2,8,46,124,183,221,234,240,241,241.
Proof: quotient state/transition/accepting invariants checked on every original
state; all 241 quotient states are reachable and refinement separates all
distinct right languages, hence the quotient DFA is minimal.
**COMPUTED.** 12,000 random direct evaluations and exact accepted-root-word
counts for each length 0..60 agree with the original 434-state automaton;
published p36/p40/p60 necklace controls are reproduced.
Reproduce or generate 241-row JSON: `python3 calculation/decimal_frontier/exterior_census/py/f1_minimal_dfa.py /tmp/f1_241.json`.
**Not claimed:** any full exterior B-cycle, centre, or decimal Lychrel number.
