# Agent N02 decimal transient reflecting-centre glider (20,000 integer steps)
Label: COMPUTED (finite literal arithmetic and pairword shape; no infinite proof).
New centre `C=[8,13,14,8,9,17,16,8,5,7,1,8,4,14,12,10,1,9,0,4,18,1,17,9,10,14,3,10,4,14,1,0,5,5,4,1,7,9,17,11,5,4,7,6,10,8,4]`.
Seed halfword `B_0 ++ W_0^224 ++ C`, mirrored even pairword, physical decimal digits from `d_i=min(a_i,9)` and `d_(n−1−i)=a_i−d_i`.
**9,132-digit seed**; GMP and independently calculated schoolbook decimal numbers agree at EVERY one of 20,000 reverse-add steps; zero palindromes; 19,132-digit final number.
The prescribed period-8 rooted exterior and maximal periodic spatial bulk match at EVERY checked step; last pre-step front index 67.
**Reflection:** for q=1,2,3,5,8,12 the front relative to t0 is 0,+1,0,+1,-7 at t=88,176,264,352,440.
Each tested small seed first breaks at `88q+412`, column 38, a positive +408 steps over the bare-seam family.
The SAME q224 integer loses this exterior at time **20,124**, column 38, not a claimed palindrome.
Reproduce `sh calculation/new_structures/agent-N02/glider_reflect_run.sh` (requires g++/GMP development libs).
Code/checkers/data: `calculation/new_structures/agent-N02/glider_reflect_{replay.cpp,independent.py,run.sh,data.json}`.
Detailed report: `reports/AgentN02DecimalReflectingGlider.md`.
This is not a base-10 Lychrel certificate, 196 result, all-q theorem, or LEAN-VERIFIED proof.
