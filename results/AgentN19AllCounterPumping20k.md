# Agent N19: all-counter finite-horizon decimal family
- **PAPER PROOF (conditional on checked finite reference):** for EVERY integer k>=15000, the seed 9 8^k 59 9^k 80 7^k 20 0^k 1 avoids palindromes for all t=0..20000, preserving exact pairword two-block pumping with junction/exterior independent of k.
- **PAPER PROOF:** 40-state folded carry-transducer pumping lemma; two aligned columns whose Boolean matrices satisfy M²=M can be expanded by any exponent without changing the true edge.
- **COMPUTED:** all 12 physical phase/gamma matrix cases idempotent, all 20000 reference edge overlaps (minimum 1820/1786), at least two odd coefficients at all 20001 states.
- **COMPUTED controls:** literal digit arithmetic for k=15000/15001 compares complete folded words after deleting two cells for each state; q=2,7 controls also run, independent GMP anchor previously validated.
- Reproduce: bash calculation/new_structures/agent-N19/run_allq.sh, using allq_matrix.py and bulk20k_pump_q.cpp plus previously committed unary_allk.py, counter_six.py, bulk20k_digits.cpp.
- Detailed soundness and limitations: reports/AgentN19AllCounterPumping20k.md.
- **UNDECIDED:** no infinite orbit certificate, no Lean verification, no claim about 196 or t>20000.
