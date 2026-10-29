# N09 exact backwards regular-language synthesis
PAPER PROOF: From the decimal folded-pairword rational relation R, let Bad_0=PrePal and Bad_(h+1)=Bad_h union R^-1(Bad_h). Every Bad_h is regular and has an exact DFA construction. A finite-stage equality Bad_h=Bad_(h+1) plus a non-palindromic seed outside Bad_h would be a sound decimal Lychrel certificate.
COMPUTED: exact NFA product, subset determinization and Moore DFA minimization through h=4. Raw states 15,105,685,9137,85771; minimized states 5,36,523,7749,74981 (for 1..5 upcoming palindrome opportunities).
COMPUTED: all five DFAs independently match full decimal integer reverse-add on the 999 positive seeds 1..999, checking first h+1 steps; the 196 seed remains outside all five computed bad languages.
UNDECIDED: no finite fixed point has been reached; this does not prove a decimal Lychrel number, nor negate existence of one. Further state explosion motivates targeted inductive-invariant learning, not another exclusion census.
Source, counts, commands: `calculation/new_structures/agent-N09/learn_regular.py`, `backward_counts.txt`, `run_backward_checks.sh` (imports the immediately preceding N09 transducer result).
Explanation: `reports/N09BackwardSafetyAutomata.md`.
