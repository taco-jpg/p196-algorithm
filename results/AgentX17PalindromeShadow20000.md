# AgentX17PalindromeShadow20000
- Label: **COMPUTED**, genuine base-10 arithmetic; no Lean or infinite Lychrel claim.
- Seed: 10,001-digit palindrome `P` with LSD-first digits `83271645[min(i,10000-i) mod 8]`, plus `10^4999` off-centre perturbation.
- For all `t=0..20000`, the perturbed orbit is nonpalindromic, has exactly the baseline's length, and agrees with it in at least **2,202 exterior digits at each end** (hence the same exterior pair-sum word).
- For `t=1..20000`, an asymmetric baseline pair lies inside the matched exterior; `t=0` is nonpalindromic directly.
- Independent GMP big-integer and column-digit engines compare both **complete decimal words at each of 20,001 states**; 211 persisted checkpoints, final length **18,242**.
- Sound local carry-sync lemma: carry differences cross common pair-sum columns only while that sum is 9 (PAPER PROOF, conditional shadow-certificate format in report).
- The shadow is finite: first lost exterior witness `t=32581`, zero matched exterior `t=32608`, length divergence `t=32615`; no infinite claim.
- Code/data: `calculation/new_structures/agent-X17/`; detailed scope and format: `reports/AgentX17PalindromeShadow.md`.
- Reproduce: `bash calculation/new_structures/agent-X17/reproduce.sh` (C++17, GMP, Python 3); repo-wide verifier unavailable without local checkout/Lean.