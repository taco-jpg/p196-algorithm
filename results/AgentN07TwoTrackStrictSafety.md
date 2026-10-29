# AgentN07TwoTrackStrictSafety
**PAPER PROOF:** A finite DFA over ordered low/high digit-pairs, forward-closed under an exact two-sided carry/overflow transducer and requiring a mismatch in every word, certifies a base-b palindrome-free reverse-add orbit.
This is strictly stronger than pair-sum DFA safety: decimal 196 step 8 is `1067869` (pair sums 10,6,14; middle digit 7) and the palindrome `5377735` has *identical* pair sums and middle digit.
Thus no pair-sum-only language whose every realization is nonpalindromic can contain that 196 iterate; the two-track language can separate it.
**COMPUTED:** Exact full-length DFA graph-closure prototype, independent checks on 95,698 arithmetic inputs and the strict expressivity witness pass.
The all-positive DFA is forward-closed but not palindrome-free; the mismatched-pair DFA is palindrome-free but not forward-closed (`10 -> 11`).
No decimal invariant, Lychrel certificate, infinite-orbit result or Lean endpoint is claimed.
Reproduce: `bash calculation/new_structures/agent-N07/two_track_reproduce.sh`.
Code: `calculation/new_structures/agent-N07/two_track_certificate.py` and `independent_two_track.py`; proof: `reports/AgentN07TwoTrackStrictSafety.md`.