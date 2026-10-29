# AgentX03DelayedCentreRepair: off-phase decimal centre-bridge regeneration
- **Label: COMPUTED.** Base 10, exact N03 8-phase root `R` (45 columns), two closed spatial return words `A` (92) and `B` (97), state `(89,145,20576)`.
- New mechanism: take ANY tested history `w in {A,B}*`, append the first 2 or 63 columns of `A`, and close as an **odd-length** symmetric pairword with central digit half of the last coefficient.
- Although the entire phase-8 pairword first disagrees at time **3**, it **re-enters exactly at times 9 and 10**; the cut-63 version also matches at steps 5 through 8. This is **whole-word** agreement, not only an exterior prefix.
- Independent Python arbitrary-precision replays: **510 seeds**, every history of 0..7 return blocks and both cuts; exact 17-step profiles, no palindromes and overflow `1010101010101010` in every case.
- Independent C++ normal-digit replay: 200 alternating return blocks, cut 2, **37,893** starting digits, **20,000** steps, no palindrome, overflow `10` throughout; minimum matched exterior prefix **16,370** columns; full-word repair at steps 9 and 10.
- The matching complete pairword **fails again at step 11**. No closed bridge cycle, all-time template, Lean theorem, or decimal Lychrel number is claimed.
- Reproduction and compact data: `calculation/new_structures/agent-X03/`; proof obligations and exact limitations: `reports/AgentX03DelayedCentreRepair.md`.
