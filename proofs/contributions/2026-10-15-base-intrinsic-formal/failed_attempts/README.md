# Retained rejected drafts

- Carry attempt 1 did not simplify reset flags and addition by zero before
  supplying recursive carry-bit bounds; Lean rejected the corresponding
  pointwise comparison goals. Explicit normalization fixed the mismatch.
- Pattern attempt 1 asked integer arithmetic automation to prove the final
  distributive propositional equivalence in the arbitrary-incoming-bit
  induction. It was replaced by explicit case analysis; no premise changed.
- Reverse-add attempt 1 asked kernel decision reduction to synthesize a
  decision procedure for the opaque recursive `HighNeutral` proposition.
  The final proof unfolds that concrete pattern and checks the remaining
  numeric/list conjunction by kernel reduction.

The replay logs are fresh reruns of the exact rejected drafts against
frozen prerequisites. They are failure evidence, not accepted proof
certificates or declarations in the successful audit count.
