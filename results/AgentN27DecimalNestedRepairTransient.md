# AgentN27DecimalNestedRepairTransient
**COMPUTED**: An explicit base-10 pairword seed has an exact, nonpalindromic reverse-and-add trajectory through step 20,000.
LSB-first initial pairword: [12,9] ++ 9^12000 ++ [6] ++ 9^3000 ++ [6] ++ 9^12000 ++ [9,12].
At every step t=0..20,000, the full pairword equals B_t ++ 9^g_t ++ C_t ++ 9^g_t ++ reverse(B_t), with g_t>0; B_t,C_t evolve by the stated exact neutral recurrence (not time-periodic).
Independent ordinary digit-list and template evolution agree on all 20,001 words; Python big integers independently check the first 100 steps.
At t=20,000: 35,322 digits, gap 5,037, B width 7,641, C width 9,966; min gap 5,035; 8,316 overflow steps.
**COMPUTED** exterior surgery: for C=[6]++9^40++[6], replacing B=[12,9] by B=[2,14,14] delays first carry-flip failure from step 273 to step 334 (+61), with ordinary digit-list replay for 272 / 333 steps.
This finite transient is NOT a decimal Lychrel certificate, does NOT prove any orbit avoids palindromes indefinitely, and does NOT claim a new all-width centre cycle.
Reproduce: sh calculation/new_structures/agent-N27/run.sh (requires C++17, Python 3).
Paths: calculation/new_structures/agent-N27/{replay.cpp,bigint_check.py,expected.json,run.sh}; reports/AgentN27DecimalNestedRepairTransient.md.
