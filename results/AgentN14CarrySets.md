# AgentN14CarrySets
**COMPUTED:** base-10 rooted primitive 39-clock overflow word with 12 temporally closed exterior pairword columns; 39/39 independent ordinary-integer one-step checks.
**COMPUTED:** 14 of 39 phases admit BOTH high-boundary carry values, which must not be frozen by the search; this enables flexible extension from the original width 7.
**COMPUTED:** exact flexible 19-state transfer of this particular width-12 strip has empty next-column frontier at transition 13; this redirects work toward joint lookahead, not an exclusion of any larger-format certificate.
**PAPER PROOF (mechanism):** set-valued carry contracts plus 19-state time-period transfer give necessary-and-sufficient extension criteria for *open-boundary temporal strips*; full central seam and spatial pump not supplied.
**UNDECIDED:** any single decimal orbit realizing the 39-step table for all steps, any base-ten Lychrel number, or a finite decimal certificate.
Data/checker: `calculation/new_structures/agent-N14/p39_k12.txt`, `calculation/new_structures/agent-N14/carryset_verify.py`; exact transfer: `calculation/new_structures/agent-N14/carryset_transfer.py`.
Discovery code: `calculation/new_structures/agent-N14/carryset_discover.cpp`, `calculation/new_structures/agent-N14/carryset_two.py`.
Reproduce: `python3 calculation/new_structures/agent-N14/carryset_verify.py && python3 calculation/new_structures/agent-N14/carryset_transfer.py && python3 calculation/new_structures/agent-N14/carryset_two.py`.
For deterministic rooted K7 genesis: `g++ -O3 -std=c++17 calculation/new_structures/agent-N14/carryset_discover.cpp -o /tmp/n14discover && (cd calculation/new_structures/agent-N14/ && /tmp/n14discover 7 7000 300)`.
Full soundness argument and limitations: `reports/AgentN14CarrySets.md`.
