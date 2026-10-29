# AgentW05AllQThreeRenewals
**COMPUTED** (finite exact symbolic arithmetic) plus **PAPER PROOF** (affine-segment saturation lemma): for every q>=1, one explicit base-10 seed family has q-independent palindromic pairword centres and the rooted p8/m20 exterior at every step t=0..264 (three 88-step band renewals).
Seed: `B0 ++ W0^q ++ C0 ++ reverse(W0)^q ++ reverse(B0)`; `C0=[8,0,0]++U++[16]++reverse(U)++[0,0,8]`, U length 40 with all entries 1 except `U[13]=7,U[20]=7,U[30]=6`.
C lengths at times 0,88,176,264: 87,131,175,219. One-step checker uses exact absorbing-band carries, affine endpoints and a residue saturation bound Q<=36; tests every integer q=1..Q for each of 264 individual transitions.
**COMPUTED**: distinct q=230, 9,365-digit *actual decimal* seed survives 20,000 reverse-and-add steps with no palindrome, retains >=156 matching phase exterior coefficients (>=5 complete 20-cell W bands) at every state; at t20,000 has 19,365 digits. GMP and independent grade-school vector updates agree on complete integers at each step (FNV64 `54bb9dcae016dd03`).
Independent controls q=1,2,7,47 for 264 steps, no failures, recorded with checksums in report.
Code: `calculation/new_structures/agent-W05/allq_renewal.py`, `replay.cpp`, `run.sh`.
Details and lemma: `reports/AgentW05AllQThreeRenewals.md`.
**Not claimed:** a fixed-seed infinite orbit, a fourth renewal, a base-10 Lychrel certificate, or Lean verification. Existing N18 finite q=1..4 three-renewal construction is explicitly credited; novelty is the all-q proof scope plus a new 20k checked member.
