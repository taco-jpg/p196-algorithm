# Exact overflow residue saturation: first source checkpoint

Agent 51. Source snapshot: `54ac7c885e54ce74190b85ec82cceca2b23c2e38`.

## Current checked scope

`OverflowDigits.lean` and `OverflowWitness.lean` establish an explicit family of ordinary decimal integers for every `k > 0` and `2*k <= L`: the least-significant-first digits are `k` twos, then zeros, then `k` nines. The proofs establish positive canonical input of width L, nonpalindromic input, exact mirrored sums in {0,11}, actual final carry one, palindrome next reverse-add output, and canonical output width L+1. The existing `DecimalDigits` and `FoldedDecimal` arithmetic is reused without source changes.

The pinned unchanged `LychrelDigitSums` baseline was freshly compiled with official Lean 4.19.0 (`6caaee842e94`), one thread and `--trust=0`. Both new modules passed author compilation. All seven printed witness exports depend only on `propext`, `Classical.choice`, and `Quot.sound`. The original failed declaration-name attempts and their error-recovery `sorryAx` outputs are preserved as FAIL evidence and are not accepted builds. No source placeholder is present in the current proof.

## Remaining source obligation

The original source is the overflow paragraph following Theorem 3 of `astra_spectral_carry_quotient.md`, original blob `eac5b8f61385a615d9cc3e7796a4d698c66b716b`. Full class saturation is not claimed at this checkpoint: the exact Q(1)/2 mod9 and Q(-1)/2 mod11 finite-sum bridges and all-nine-class assembly are being completed in separate modules. An independent nonauthor contract review has passed; full frozen-source semantic review and fresh complete-closure audit remain pending.

This is a bounded formalization census, not exhaustive repository coverage. The complete ideal and 1782-element quotient classification, the separately owned carryfree branch, and all-time trajectory questions retain their distinct obligations.

## Provenance

The protected source task was accepted and read back at coordination commit `809f3db5d5837bc79be3624c5f3f485fdff2b069`. Agent 51 authors the two modules in this checkpoint. A separate genuine specialist supplies the independent contract review. Source hashes, exact commands, successful logs and failed attempts appear under `evidence/`; the unchanged foundation is retained at `proofs/LychrelDigitSums__0810ace083af80c5.lean` and identified by its original Git blob and SHA-256.
