# AgentX10FourSheetMultiGap20000
**COMPUTED**: exact base-10 two-parameter four-sheet mechanism for `N(q,r)=88*10^(3q+r)+37*10^q+75`.
For **every integer q,r >= 11984**, all 20,001 orbit states t=0..20,000 are nonpalindromic and satisfy the explicit four-sheet affine-digit recurrence.
The four slope vectors `(0,0),(1,0),(2,1),(3,1)` close under reversal about the leading `(3,1)` sheet; ordinary decimal carries stay within sheets under the checked separation guard.
The C++ symbolic engine certifies all 20,001 states; maximal lower-gap bound is 11,984; zero symbolic palindromes.
Explicit seed `q=r=11985` has 47,942 digits; at step 20,000 it has 56,196 digits.
An independent grade-school full-integer reverse-and-add implementation checked **all digits** against all four sheets at **every one** of 20,001 states: 20,001/20,001 exact and no palindromes.
Separate Python `int` reverse-and-add agrees with the two-parameter symbolic formula for all 264 steps at `(q,r)=(164,165),(179,191),(212,164)`.
At `q=r=200`, the model's separation guard expires at t=329 and its **first** actual-integer shape mismatch is t=329; this is a falsifiable finite-horizon mechanism.
Code: `calculation/new_structures/agent-X10/{four_sheet.py,four_sheet_fast.cpp,decimal_replay.cpp,reproduce.sh}`.
Compact data: same directory `{four_sheet_data.json,fast_20k.csv,replay_20k.txt,replay_collision.txt}`.
Reproduce: `bash calculation/new_structures/agent-X10/reproduce.sh`; requires Python3 and g++ (no third-party libraries).
Soundness of the parametric four-sheet decomposition and exact limitation: `reports/AgentX10FourSheetMultiGap20000.md`.
**NOT CLAIMED:** an infinite base-10 Lychrel orbit, a closing parameter-growth cycle, a proof for 196, or Lean verification.
