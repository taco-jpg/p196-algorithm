# AgentN07FoldedRegularSafety
**PAPER PROOF:** A finite DFA of outside-to-centre digit-pair coefficients, closed under the exact two-sided carry transducer and requiring an odd pair in every accepted word, certifies a palindrome-free orbit by induction, without a bounded centre.
The gamma=1 transducer delays upper-side digits by one position; centre and input parity are part of the finite transition.
The all-length forward-closure and parity safety conditions reduce to finite graph reachability, without a bound on word length.
**COMPUTED:** An executable DFA inclusion checker, independent integer/digit-list tests (31,900 random plus 8,764 exhaustive), and decimal 196 ordinary-digit replay through 20,000 iterations pass.
The one-state all-positive DFA is forward-closed but not palindrome-safe; the simple odd-pair DFA is palindrome-safe but not closed (`10 -> 11`).
In 196's first 20,001 states, 19,998 have an odd mirror-pair coefficient; first failure at step 8, so a moving two-track mismatch witness is needed.
This is a new *sound format*, not a decimal invariant or an infinite-orbit certificate; no base-10 or 196 Lychrel claim.
Code and data: `calculation/new_structures/agent-N07/`; full soundness argument: `reports/AgentN07FoldedRegularSafety.md`.
Reproduce: `bash calculation/new_structures/agent-N07/reproduce.sh`.