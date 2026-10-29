# AgentX10FourSheetMultiGap20000 (strengthened exact polyhedral guard)
**COMPUTED**: base-10 four-sheet family `N(q,r)=88*10^(3q+r)+37*10^q+75`, two integer parameters.
For **EVERY q>=11984 and q+r>=12024** (r may be negative), all 20,001 states t=0..20,000 are nonpalindromic and follow the exact four-sheet recurrence.
Four closed exponent slopes `(0,0),(1,0),(2,1),(3,1)` with ordinary carry normalization; exact maximal guards `q>=11984`, `q+r>=12024`, `2q+r>=1884`, `3q+r>=1865`.
The last two constraints follow automatically from the first two. Independent checker proves all gap separations for all states, not merely sampled q,r.
Explicit boundary seed `(q,r)=(11984,40)`: 35,994 digits initially, 44,248 digits after 20,000 reverse-add steps.
Independent full-decimal schoolbook arithmetic checked **ALL 20,001 full words** against symbolic four-sheet values, zero mismatches and zero palindromes.
Independent full-word 20,000-step controls `(q,r)=(11985,11985)` and `(20000,-7976)` also pass, including a negative-r instance.
Independent Python `int` reverse-add reproduces all 264 steps at `(164,165),(179,191),(212,164)` (uniform q,r>=162 initial control).
At `q=r=200`, first actual guard failure and first integer/template mismatch both t=329, demonstrating finite-horizon exhaustion.
Code: `calculation/new_structures/agent-X10/{four_sheet.py,four_sheet_fast.cpp,poly_guard.cpp,decimal_replay.cpp,reproduce.sh}`.
Data: same directory `{four_sheet_data.json,fast_20k.csv,poly_guard.txt,replay_20k.txt,replay_wedge_20k.txt,replay_min_wedge_20k.txt,replay_collision.txt}`.
Reproduce: `bash calculation/new_structures/agent-X10/reproduce.sh` (Python 3 and C++17, no dependencies).
Proof and scope: `reports/AgentX10FourSheetMultiGap20000.md`.
**NOT CLAIMED:** an infinite base-10 Lychrel orbit, a closing parameter-growth cycle, 196, or Lean verification.
