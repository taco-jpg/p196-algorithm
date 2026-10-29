# Agent N10: universal one-step decimal insertion lemma
- **Label: PAPER PROOF** (finite boundary arithmetic audited by COMPUTED symbolic/real-integer checkers).
- New quotient soundness rule for the known decimal p8/m20 rec0 exterior, with phases `(B_t,W_t)`, `|B|=39`, `|W|=20`.
- For every phase `t mod 8`, every integer `r>=1` and every palindromic centre `C` of arbitrary length, define `P=B_t ++ W_t^r ++ C ++ reverse(W_t^r) ++ reverse(B_t)`.
- Let `T` be actual carry-normalization followed by reversed-digit pairing; let `I_t` insert `W_t` just after the first 39 sites and its reversal before the last 39.
- Exact identity: `T(I_t(P)) = I_(t+1 mod 8)(T(P))`; overflow also agrees. The centre need NOT repeat or have bounded width.
- Proof reduces any centre to its normalized digit word and one outgoing carry bit, and any `r` to steady absorbed band blocks, with eight finite phase checks.
- Reproducer `sh calculation/new_structures/agent-N10/run_universal.sh`: 288 independent-symbol checks and 2,400 actual decimal-integer controls PASS.
- Full proof, carry table, limitations and Lean sketch: `reports/AgentN10UniversalPumpLemma.md`.
- **Not claimed:** forward invariance of the entire band-guarded language, any infinite decimal Lychrel orbit, or Lean verification.
