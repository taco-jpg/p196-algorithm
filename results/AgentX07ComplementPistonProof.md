# AgentX07ComplementPistonProof

- **PAPER PROOF (all-time conditional law):** For base 10, every low-first digit word `A` with last digit <=8 and `sum(A)≡8 (mod 9)` defines a nonpalindromic integer `A ++ 9^L ++ (9-A)` for any `L>=0` (coordinatewise complement, same index order). Whenever `L>=1`, one exact reverse-and-add step gives another such word with `m'=m+gamma`, `L'=L-gamma>=0`, preserving the mod-9 charge and nonpalindromicity.
- Proof: the two frontier pair-coefficient words add pointwise to 18, so carries started at 0 and 1 remain complementary, output digits sum to 9, and the final carry is complementary to the low carry. The only two overflow branches append either 8/1 or nothing, preserving the guard and the digit-sum charge.
- **COMPUTED control:** 3,333 independent ordinary-integer/schoolbook one-step checks plus conditional second steps, all `A` of length <=4 satisfying the invariant and `L∈{1,2,5}`; no mismatches.
- **Concrete entry:** `N_n=10^n-2908` reaches invariant `A=21086`, `9-A=78913`, `L=n-9` after two steps for large n. This analytically explains the `m-G=4` mechanism reported in `AgentX07NinePiston` without assuming any 60k observation.
- Proof: `reports/AgentX07ComplementPistonProof.md`; test/data: `calculation/new_structures/agent-X07/piston_induction_check.py`, `piston_induction_run.sh`, `piston_induction_data.json`.
- **Not an infinite Lychrel certificate:** for each fixed initial length the nine core drains as overflows accumulate. Collision/reentry is not proved, and this theorem is not Lean-verified.
