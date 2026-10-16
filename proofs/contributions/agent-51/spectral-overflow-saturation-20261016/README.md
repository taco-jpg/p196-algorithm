# Exact overflow saturation for the retained spectral coordinates

This contribution formalizes the overflow part of Theorem 3 in the original `astra_spectral_carry_quotient.md` (blob `eac5b8f61385a615d9cc3e7796a4d698c66b716b`, archived source snapshot `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`, lines177–193).

## Mathematical result

For every natural width `L >= 18` and residue `s < 9`, `P196.Agent51.overflow_saturation` produces the same actual natural number `n` and least-significant-first decimal digit function `d` satisfying all of:

- `0 < n` and `DecimalDigits.Canonical n d L`;
- `n` is not a `Lychrel196.Palindrome`;
- the actual terminal decimal carry is exactly one;
- `Lychrel196.step n` is a palindrome;
- the actual extended output digits are canonical at width `L+1`;
- `(Q(1)/2) % 9 = s` and `(Q(-1)/2) % 11 = 0`, using literal finite coefficient sums and integer division.

The separate even and odd corollaries retain the source thresholds `L >= 18` and `L >= 19`. For `1 <= k <= 9`, the witness has `k` low digits equal to2, `k` high digits equal to9, and zeros between them. Its pair coefficients are11 in the symmetric outer pairs and0 elsewhere. The proof establishes `Q(1)=22*k` and `Q(-1)=22` exactly when both `L` and `k` are odd, with value0 otherwise. The residue selection is finite; the width proof remains unbounded.

## Source organization and provenance

- `OverflowDigits.lean`: explicit digits and their true reflected pair coefficients.
- `OverflowWitness.lean`: actual integer input, carry, palindrome and canonical-width bridges, reusing the original `DecimalDigits` and `FoldedDecimal` results.
- `ResidueSums.lean`: finite-sum helpers, literal polynomial evaluation and both signed residue coordinates.
- `Saturation.lean`: bounded coefficient extensionality for the actual column sums and complete quantified endpoints.

The original arithmetic foundation is reused unchanged from `proofs/LychrelDigitSums__0810ace083af80c5.lean`, Git blob `8a865176625283648a8a20dd2411ed77670eb0a2`. Root Agent51 authored the digit, integer-witness and composition modules. The genuine specialist `/root/claim_census` authored the residue module. The separate genuine nonauthors `/root/semantic_review` and `/root/environment_audit` perform source-semantic and execution reviews. Formalization authorship does not imply discovery of the source mathematics.

## Verification at this checkpoint

All five local sources have actual successful author builds with official Lean4.19.0 (commit prefix `6caaee842e94`), `--trust=0 -j1 -DElab.async=false`. The original foundation was freshly compiled from source. All three final endpoints printed only `propext`, `Classical.choice` and `Quot.sound`. A genuine nonauthor final semantic review is PASS and is retained at `review/FINAL_REVIEW.md`. The independent complete source rebuild and comprehensive module-origin safe-declaration audit are still running at this checkpoint.

The dedicated registry `proofs/Agent51OverflowSaturation.registry.json` explicitly includes the full five-module closure and all52 public new declarations. It is an additional scoped registry; this does not modify the global accepted catalogue or claim repository-wide coverage.

From a checkout of this contribution, the existing verifier implementation can be invoked directly with:

```sh
python proofs/verify_project__214bf7673efe116b.py \
  --lean /absolute/path/to/lean-4.19.0-linux/bin/lean \
  --output /absolute/path/to/a-new-output-directory \
  --registry proofs/Agent51OverflowSaturation.registry.json \
  --project agent51-overflow-saturation
```

This command uses the existing verifier's actual flags `-j1 -DElab.async=false`; it does not add a trust-zero flag. Its execution receipt is not yet included at this checkpoint. The repository's top-level `proofs/verify_project.py` is a historical-layout replay wrapper, so the preserved implementation is called directly for the current flattened paths. The separate strict build is the source-kernel check. Import-based type/axiom audits inspect the freshly generated environment; they do not recheck proof bodies stored in imported objects. Shipped Init/Std/Lean objects remain runtime dependencies.

All substantive successful and failed development attempts are retained under `evidence`. Failed elaboration output is historical evidence and is outside the registered accepted source closure. No accepted proof uses an admitted proof, a new mathematical axiom or compiler-trusted evaluation.

## Exact scope limits

The theorem concerns the next ordinary reverse-add step. It does not establish all-time palindrome avoidance or resolve the196 trajectory. The coordinate `r` is the source's `Q(-1)/2 mod11`; in even width it is not an assertion that `n mod11=0`. The full Laurent-polynomial defect ideal and the1782-element quotient classification remain separate unformalized obligations. Carryfree saturation and the T/R, U/S and carry-support results remain owned by their respective agents.

Task: `agent51-spectral-overflow-saturation-20261016`. Contribution PR: #148. Source snapshot: `54ac7c885e54ce74190b85ec82cceca2b23c2e38`. No main-write role is claimed.
