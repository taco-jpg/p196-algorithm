# Agent W10: decimal cyclic-carry zero moat, 20,000 exact steps
- **COMPUTED**: seed N0 = int("5346" * 8000) has zero palindromes in states t=0..20000; length 32000 -> 40323, with 8323 leading overflows.
- At each of the 20001 states, both the digit word and symmetric pair-coefficient word have spatial period 4 in the guarded central region: LSB-first indices t+64 through n_t-t-68 for digit comparisons; there are 192 digit comparisons at t=20000.
- The distinct toroidal model modulo 9999 has a non-palindromic cycle 5346 -> 1782 -> 4653 -> 8217 -> 5346, a seed heuristic, NOT an ordinary decimal certificate.
- The actual central four-digit row first becomes 0000 at step 33, and its central periodic zero moat survives through step 20000.
- The four-cell cyclic-carry predictor agrees with actual central rows for 19,999 unique-carry transitions; one neutral ambiguous transition is not used to predict.
- Independent ordinary-decimal engines (digit-array vs GNU MP big-integer reverse-add) agree at 21 full-number checkpoints; both check every state for palindromes.
- Reproduce: bash calculation/new_structures/agent-W10/run.sh (C++17, GMP, Python3); data: calculation/new_structures/agent-W10/checkpoints.tsv.
- Full scope and carry-clock explanation: reports/AgentW10CyclicCarryMoat20k.md.
- **NOT CLAIMED**: infinite base-10 Lychrel orbit, closed decimal certificate, anything about 196, or survival beyond t=20000.
