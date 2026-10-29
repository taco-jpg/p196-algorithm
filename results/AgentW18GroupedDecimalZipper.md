# AgentW18GroupedDecimalZipper
**PAPER PROOF.** A carry-exact mixed-radix, length-phase-aware *local zipper* represents true decimal reversal in grouped base `10^k` digits using only two adjacent source blocks, a finite `h` phase and one normal decimal carry; ordinary base-`10^k` reversal is never silently substituted.
The exact block recurrence handles partial leading blocks, odd decimal lengths and overflow. It yields a concrete finite-state grouped-fold closure format: a regular language closed under this local relation and excluding decimal palindromes certifies an infinite decimal Lychrel orbit.
A positive base-100 three-step edge family is proved for every Q>=2, seed `5(99)^Q4`, with literal pair-block formulas in the report; **no closed decimal automaton/cycle is found**.
**COMPUTED controls:** 66,847 exact decimal integer comparisons in bases 10, 100, 1000, including 700 steps per grouped base and Q=2..150 edge controls.
Restricted old neutral exterior `g=01` roots reproduced for b50/b146/b1286, not in b100/b1000; this redirects naive grouping to the exact h-phase zipper and is not a general no-go.
Reproduce: `bash calculation/new_structures/agent-W18/reproduce_zipper.sh`.
Code: `calculation/new_structures/agent-W18/zipper.py`, `root_probe.py`; report: `reports/AgentW18GroupedDecimalZipper.md`.
