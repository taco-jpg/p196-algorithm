# N09: Exact regular-language backwards synthesis

Status: PAPER PROOF of the hierarchy and stopping condition; COMPUTED for five bounded symbolic stages. No decimal Lychrel certificate, no Lean proof.

Building on the exact folded pairword relation R and regular PrePal from N09FoldedRationalInvariant, define Bad_0=PrePal and Bad_(h+1)=Bad_h union R^-1(Bad_h). For a valid folded pairword P(N), membership in Bad_h is **exactly** the existence of a palindrome among the first h+1 positive successors of N. This follows by induction on h because R represents the actual next pairword, and its image is unique for each valid P.

PAPER PROOF: Inverse image of a regular language under a rational transduction is regular: take the product of the transducer state with the DFA for the target language. Closure under union gives the claimed finite-state construction at every h. The supplied Python routine builds this product NFA (two nondeterministic high-carry values), determinizes by subsets, then minimizes by exhaustive partition refinement. Terminal rules distinguish even and odd original widths and permit one extra output pair at overflow. There is no fixed bound on word length.

Potential *positive* decimal certificate: if one reaches any exact fixed point Bad_(h+1)=Bad_h, the complement Safe_h among valid pairwords is closed under R, contains no predecessor of a palindrome, and is recognized by a finite DFA. If a non-palindromic decimal seed lies in Safe_h, soundness is immediate by the previous N09 finite invariant theorem. An equality assertion requires exact DFA language equivalence, not merely equal state counts. Neither equality nor the needed infinite orbit is claimed here.

COMPUTED: For h=0..4, 0-based bad stage denotes one through five future palindrome opportunities. Raw determinized DFA counts are respectively 15, 105, 685, 9137, 85771. After Moore equivalence minimization they are 5, 36, 523, 7749, 74981. All five stages independently agree with ordinary decimal reverse-and-add for every source integer 1..999, looking ahead h+1 ordinary integer steps. At each stage P(196) is outside Bad_h; the first 100 pairwords along the actual 196 orbit also remain outside. This is **finite**, not an induction over 196.

Controls: At h0, the complement Safe_0 is checked by the prior exact DFA product oracle and is NOT closed; a concrete one-digit folded counterexample is O(10), corresponding to decimal 5 -> 10 -> 11. This is a useful positive test of the counterexample-generating inclusion checker, not a negative result about the whole format.

Run from repository root: `bash calculation/new_structures/agent-N09/run_backward_checks.sh`. The script uses only Python3 and prior files in the same N09 directory. It compares full deterministic output against tracked `backward_counts.txt`, finishing with `AGENT_N09_BACKWARD_CHECKS_PASSED`. The source has an explicit 350,000-state cap per raw subset construction. The run reaches all claimed stages without reaching that cap; later stages are UNDECIDED and have not been represented as a no-go.

Next constructive refinement: use orbit-driven counterexample-guided state merging or a symbolic antichain representation instead of materializing each full bad-preimage DFA. The growth in raw states from 15 to 85,771 exposes a computational bottleneck, not a mathematical obstruction to a decimal certificate.
