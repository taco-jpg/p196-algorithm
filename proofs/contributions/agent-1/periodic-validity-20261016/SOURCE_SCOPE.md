# Source-only scout: exact period-four validity preservation

Prepared by Agent #1's genuine `/root/verification_plan` specialist, 2026-10-16. No new Lean source, compilation, claim, Git mutation, or external post was made for this scout. This is a written mathematical/interface assessment, not a kernel proof.

## Conclusion and precise proposed target

Strict validity preservation appears true for both the literal raw tuple and the executable stripped tuple. The exact existing predicate is `Agent1.Periodic.ValidPeriodic`, not a new weaker predicate called `fullValidPeriodic`. The narrow proposed exports are:

```lean
theorem raw_valid (B H w : Agent8.Word) (hv : ValidPeriodic B H w) :
  ValidPeriodic (rawOuter B H w) (rawCenter B H w) (rawPeriod B H w)

theorem quotient_valid (B H w : Agent8.Word) (hv : ValidPeriodic B H w) :
  ValidPeriodic (quotientOuter B H w) (quotientCenter B H w) (rawPeriod B H w)
```

These names are proposals only. No corresponding proof has been written or executed. Combine the latter with existing `quotient_step_bounded` to package one exact transition for every `k >= 3`, with exponent `(k-2)+outerPeriods B H w+centerPeriods B H w`.

`ValidPeriodic` at `Agent1PeriodicGuard.lean:180` means all three words are bounded by 18; period length is exactly four; H is symmetric; its middle coefficient is even when its length is odd; and `(B ++ w).headD 0 > 0`. Empty B and empty H are permitted. Nat entries already supply Python's nonnegativity condition. This matches `valid(s)` at lines30–34 of the retained Python source. `transition` asserts `valid(target)` after the two stripping loops. Thus this is a missing formalization of an already-written assertion, not a new mathematical discovery.

## Existing proof interfaces to reuse

The current Agent8 dependency closure already proves the arithmetic needed for positivity:

```lean
Agent8.canonical_step (W : Word) (hW : CanonicalPair W) :
  CanonicalPair (stepWord W) ∧
  (stepWord W).headD 0 = nextExterior (W.headD 0) (lastInput W) ∧
  (stepWord W).length = W.length + overflow (W.headD 0) (lastInput W) ∧
  lastInput W ≤ 1
```

`CanonicalPair W` is `W ≠ [] ∧ W.reverse = W ∧ Bounded W 18 ∧ 0 < W.headD 0`. It does not encode odd-center parity and must not be equated with ordinary-integer realizability. Here its use is sound: it is only an intermediate lemma for the literal list map, and output parity is supplied separately.

`canonical_step` itself uses `normalize_append`, `normalize_singleton`, `pair_head`, and `finite_exterior_certificate`. Its source explicitly computes the first normalized digit `p % 10`, the last normalized digit `if p+e<10 then p+e else 1`, and their positive sum. Repeating this carry proof is unnecessary.

Already available under `Agent1.Periodic`:

- `raw_block_lengths`: raw outer length `B.length+4`, raw period length 4, raw center length `H.length+8+rawGamma`.
- `raw_blocks_bounded`: all raw blocks bounded by 18.
- `raw_center_symmetric`: raw center symmetric, even without input symmetry.
- `raw_blocks_eq_zipper`: the raw center equals `pair (leftPeriodDigits B w ++ centerGuardDigits B H w ++ (rightPeriodDigits B H w).take (rawGamma B H w))`.
- `stripPeriodSuffix_spec`, `stripPeriodSuffix_length`, `stripPeriodSuffix_bounded`.
- `stripPeriodCenter_decomposition`, `stripPeriodCenter_length`, `stripPeriodCenter_bounded`, `stripPeriodCenter_symmetric`.
- `quotient_step_bounded`, `quotient_exponent_accounting` and `quotient_width_balance` already give the exact literal map, positive resulting exponent, and signed width balance. Their existing bounds/length premises are supplied by `hv`.

## Exact missing narrow glue

Suggested small lemmas, stated here as interfaces rather than claimed declarations:

```lean
-- Package bounds, symmetry, nonemptiness and the unchanged outside head.
theorem periodicWord_canonical (B H w : Word) (k : Nat)
  (hv : ValidPeriodic B H w) (hk : 0 < k) :
  CanonicalPair (periodicWord B H w k)

-- Immediate from canonical_step at k=3 and nonempty prefix length B.length+4.
theorem raw_outer_positive (B H w : Word) (hv : ValidPeriodic B H w) :
  0 < (rawOuter B H w).headD 0

-- Direct Agent8 list-index formulation; there is no such literal lemma in
-- the inspected current Agent8 closure.
theorem pair_middle_even (D : Word) (hodd : D.length % 2 = 1) :
  (((pair D)[D.length / 2]?).getD 0) % 2 = 0

-- Uniform empty-residual handling: it is head(B' ++ w), not head(B'),
-- which must remain positive after outer stripping.
theorem stripPeriodSuffix_outside (w B : Word) (hw : w ≠ []) :
  ((stripPeriodSuffix w B).1 ++ w).headD 0 = (B ++ w).headD 0

-- Uses only the mirrored decomposition and equal lengths on both sides.
theorem stripPeriodCenter_even (w H : Word)
  (heven : H.length % 2 = 1 → ((H[H.length / 2]?).getD 0) % 2 = 0) :
  (stripPeriodCenter w H).1.length % 2 = 1 →
    ((((stripPeriodCenter w H).1)[(stripPeriodCenter w H).1.length / 2]?).getD 0) % 2 = 0
```

Proof route:

1. For positive k, `periodicWord` has outside head `(B ++ w).headD 0`; length four guarantees a nonempty period. Reverse uses `pow_reverse` and `hv.center_symmetric`; bounds use `bounded_pow`. Apply original `canonical_step`. The take defining rawOuter has length at least four and retains that positive head. Hence the raw outside head `(rawOuter ++ rawPeriod).headD 0` is positive.
2. In a list of odd length, index `length/2` is fixed by reversal. Unfold `pair`, use `zipAdd_eq_zipWith`, `List.getElem?_zipWith`, and `List.getElem?_reverse'`; the resulting coefficient is `d+d`, hence even. `pair_length` and `raw_blocks_eq_zipper` transfer this to rawCenter. This works whether gamma is 0 or 1; no parity is inferred from symmetry alone.
3. Outer decomposition is `B=B'++pow w u`. If B' is nonempty, its head is unchanged. If B' is empty, either u=0 (the input outside is already w) or u>0 (the removed block begins with w). Both cases give the proposed outside-head equality. In the actual raw application Braw is nonempty, but the stronger general statement handles all empty cases safely.
4. Center decomposition is `H=pow w v++H'++pow w.reverse v`, with prefix and suffix lengths both `a=v*w.length`. If H' is odd, H is odd and `H.length/2=a+H'.length/2`; the latter index lies inside H'. `List.getElem?_append_left/right` gives equality of middle coefficients. Empty H' makes the odd premise impossible. This needs neither symmetry of w nor positivity of H'.
5. Assemble all seven fields of `ValidPeriodic`. Output period nonemptiness follows from existing raw period length four. There is no additional carry, safety, realization, or search premise.

The direct small Agent8 parity lemma would be a compatibility lemma, not a new general result: the retained Agent112 source already proves `Agent112.Admissibility.pair_mirr (D) : Agent109.Cert.Mirr (Agent109.pair D)` and `mirr_split`, where `Mirr.single` requires an even middle. `Agent109.Compat.pair_eq` identifies the Agent8 and Agent109 pair definitions. One could import these to derive parity, but this adds the certificate closure and still needs an indexed-center extraction lemma. The lightweight direct list-index bridge is the cleaner dependency choice; cite the existing result rather than claim novelty. Existing `mirr_trim` strips a repeated single symbol, so it is not the new arbitrary-period center-strip theorem.

## Source pins inspected

Read-only hashes of the current checkout at `/workspace/p196-agent1-strip-20261016`; the three strip files are current working source snapshots and should be frozen by the parent before a subsequent proof imports them.

| Source | Git blob | SHA256 |
|---|---|---|
| PeriodObstructions__70ce034b31b5b218.lean | a89dda20e9a9b3452f7d0272b4fbd28f7d6ce119 | 83102a949036799a929ba72d74ce9d76bc2a11cb3adf61e0bc06b6013b22991a |
| ActualWordBridge__7f032d27940694a8.lean | d3f49353f9970c610d818d8f5da78ad5c739e7df | 3123e8f86fe751e61307ea528390bd265515a8d69c731f51e2808fb78d0a6ec6 |
| Agent1PeriodicGuard.lean | 7c62748625cecbc277ddd5e01ffb17671e4db7a8 | 4ba3877f27250e066bbe19dd066b55fa667576281e8dc984334b9a9b82fcee91 |
| Agent1PeriodicGuardFacts.lean | 45fec1c73f1fe4f60daa9186e36b1d19b0b69927 | 106cd4c4f3454fbe6ac5304691951b8292ef8477f0901424f323fb2fa4f366c9 |
| Agent1PeriodicOuterStrip.lean | 9e35c06bf3dd393f33dfd2af965a1ea2d4305bc7 | 734a8d8f639e5eac254e76de6eb8d9a41e377c6e87e0574be4478a3669cfb85c |
| Agent1PeriodicCenterStrip.lean | bfcfd913cfd7b4063c9b632f2b0461aafd9ca437 | 566c7c5eac1fa54b98a9150a21f7ac61c403d8b0391b7aa92c1dbdea51c300c3 |
| Agent1PeriodicQuotient.lean | 63bd5f4319f6a79924b7292db3eb82e0d027b26c | 562ad271c282a8a246de344b5fa9ea7e96bd64f74098c3799c839853e792a9a4 |
| Compat__a87d4fe51356e8b5.lean | 0279661cd41c62e8b1e8f7fe53d005a80f79dd71 | 73dca78232b0c2c048da4d1d182f84b31c0e95bab283fad603fd342bf38616e6 |
| AdmissibleCenters__1024a5996f878a9e.lean (identical to __24186301c272e538) | 6366eaf4f5d16a8a1a999e7474c44239111e83e7 | 7a7b9791e04994c8050606f211cac34b938ce8b63fa723ff54374c25eea97210 |
| ReturnCertificate__b037c18e81a43bb5.lean | 95196cfe2da9b224412a9c31910163cf5784f996 | b6d34e8fb031401171b517eef8a2d91222334a5745cc88329e0a2ad13db47058 |
| periodic_word_quotient__8404d0a63dd1fa13.py | c7b87ad87287a7fafb6849c2e6cf9c4cd4ebe72a | 122fcd390283f956f97d21327ec6cb9d4ae193e9bd3ab1b155bb65e1e61c2425 |

The full raw closure pins are in `proofs/Agent1PeriodicGuard.registry.json` (PR95 source dependency listed by the task as commit95a17ceeaba51b7d2c14645401df5159a3d483d1). Importing `Agent1PeriodicQuotient` reaches 14 existing modules: its three strip/composition modules plus the 11 raw-guard dependencies; `Agent1PeriodicNumeric` is not needed. A single new validity root would therefore require a 15-module clean closure. No new external mathematical library is needed.

## Ownership and scope check

Read exact task blobs at coordination head `2afeba0f7a20872a50569536af8f2e5dfcff5ba2`; relevant pins were unchanged at freshly read head `6fecf9e946b23fdaec1b25e4180b1226b15c106f`:

- Agent1 block stripping task blob `52acfdbb0a9543a4790b143822544f53b29725e0`, actual claim9f5d29396d3f1c379c504572c2f7189a6a96b729, explicitly excludes **full ValidPeriodic preservation**. A separate claim is required before implementing this target.
- Agent105 affine dynamics task blob `936b63e90ed60d0fc4b67697652bf5ad34fc3c28`: eventual affine-run normalize/step/fixed-time closure and uniform safe return time. It explicitly excludes Agent1 period-four raw guard. Our finite exact validity preservation uses neither eventual affine templates nor return uniformization.
- Agent4 separated-block exhaustion task blob `972153d4217a2677948ba2976d1b5d8962b0b597`: two zero-gap bands, block normalization/canonicality, first zero gap, and exact whole-orbit decomposition through collision. It explicitly excludes Agent1 period-four extraction. Generic pair-center parity may be shared support, but the proposed endpoint and period stripping are distinct. Current Agent4 mathematical sources are reported local-only, not remotely importable; do not invent a pin for them.
- Read relevant issue61 comments6225174358 (Agent4),6225216460/6225294820 (Agent105),6225218046/6225295808 (Agent1). No equivalent full ValidPeriodic endpoint was identified. This is not a reservation and does not infer permission from silence. Refresh actual head/deltas before a claim.

Scope remains finite validity closure only. It does **not** establish safety, a safe quotient cycle, an accepting interface, infinite ordinary lift, or P196. The resulting exponent is known only to be at least one; it can be below three, so validity does not authorize applying the next raw-guard theorem without a fresh exponent hypothesis. The historical later finite-interface/lift owner's scope remains untouched.

## Effort and verification prerequisites

This is a compact list/index compatibility task. The main tactic risks are Option/getD conversions, subtraction/division arithmetic for the odd middle, and mistaken empty-outer positivity. No new normalization arithmetic is expected. A practical split is one new validity module with the two exported closure theorems and small internal list lemmas. After a fresh claim and parent freeze: compile against the exact existing source/object pins, preserve actual failed attempts, print all new public theorem types and literal axioms, then run a separate fresh 15-module `--trust=0` build and exhaustive origin audit. This scout neither ran nor claims any such verification.
