# Agent 10: universal recovery of the first two pair coefficients

Eight complete carry observations determine the first two active pair coefficients of any two admissible ordinary-decimal coefficient words at the same initial width. This extends the exterior-coordinate result in `Agent10CarryObservability.md`. It requires no initial-nonoverflow premise.

The full thirteen-module closure is **LEAN_CHECKED**. It retains all earlier count, conditional full-reconstruction, smoothing, and concrete six-observation results. General reconstruction of every interior coefficient from eight observations is not a conclusion of this theorem.

## Exact endpoint

The final exported theorem is `Agent10ThreeColumnCarry.eight_carries_determine_first_two_active_pairs`. Its domain and conclusion are:

```lean
(hq : Admissible L q) (hr : Admissible L r)
(hc : ∀ t, t < 8 → ∀ i, i ≤ (iterPairs q L t).1 →
  carry (iterPairs q L t).2 i = carry (iterPairs r L t).2 i)
⊢ ∀ i, i < 2 → i < L → q i = r i
```

The observation indices are zero through seven, and every final overflow carry is included. Equal initial widths and those overflow observations synchronize later widths.

The separate endpoint `eight_carries_determine_second_pair` states `q 1 = r 1` with the necessary `2 <= L` premise. `eight_carries_determine_first_two_pairs` combines the two coefficients under the same premise. The active-coordinate version handles width one only at index zero; it assumes nothing about arbitrary function values beyond the initial width.

## What the finite graph checks

`Agent10ThreeColumnExclusion` records the first three coefficients and the shared incoming high carry at current index `L-3`. Compatibility checks low carries at indices 1, 2, and 3, the high carry at `L-1`, and the terminal carry at `L`. The exact actual arithmetic bridge derives these coordinates from the existing carry recurrence and reflection symmetry, then proves the graph update agrees with the unchanged `nextColumns`.

The kernel certificates cover all 5,184 starting pairs with difference `(0,1,-3)`:

```text
((p+1,a+1,b),(p+1,a,b+3))
p = 0,...,17; a = 0,...,17; b = 0,...,15.
```

Every possible shared Boolean control path is included. Eighteen certificates, each containing 288 starts, exclude eight-observation survival. Each finite family certificate is axiom-free. The negative orientation follows by exchanging the inputs and transporting the matched-width hypothesis.

The independent graph control gives survivor counts `[3870,2355,1345,774,413,160,42,0]` after one through eight observations. Checking only the low carries and terminal carry leaves thirteen starts at eight observations. Requiring all three reflected high carries gives a stronger auxiliary graph; that graph's counts must not be substituted for those of the relation actually formalized here.

The checked seven-observation graph survivor `(16,6,0)/(16,5,3)` describes a necessary projection. It is not a claim of a full-word or ordinary-integer collision.

## Why the encoding is sound

Direct repeated tuple evaluation exhausted the available process memory. The final implementation encodes `(p,a,b)` as `361*p + 19*a + b` and decodes it by exact quotient/remainder operations. `decode_encode3` proves recovery on every valid state. The actual-history induction supplies validity at every time, so it transports the original arithmetic trajectory through the encoding without dropping a possible actual history.

Both unsuccessful raw-recursion attempts and their execution classifications are preserved. The final encoded source completed successfully. A separate representative 288-start measurement passed with `--trust=0` in 2.814 seconds at 700,504 KiB peak RSS. That is a measured family, not a worst-case resource bound for the complete module.

## From the graph to the second coefficient

Let `f = cappedDiff q r L`. The earlier exterior result gives `f 0 = 0`. The seven-transition count theorem gives at least three nonoverflow steps.

If there are at least four nonoverflows, the existing endpoint injectivity theorem already recovers all coefficients. Otherwise there are exactly three. The matched-history identity and the final complete observation give `|f| <= 9` and `|smoothPow 4 f| <= 1`.

The existing `smoothPow_tail` theorem shifts these bounds to `g i = f (1+i)`, using the proved vanishing exterior coefficient. The checked leading-coefficient lemma says that `g 0 != 0` forces `(g 0,g 1)` to be `(1,-3)` or `(-1,3)`.

At width at least three, either case contradicts the new actual three-column exclusion. At width two, `f 2 = 0` by the finite-width zero extension, which contradicts either pattern directly. Hence the second active pair coefficient agrees.

## Verification

| Item | Recorded value |
| --- | --- |
| Tested isolated source commit | `b170358092047167fef8a5cee165366dbc1e8fd7` |
| Scoped registry | `Agent10TwoPairReconstruction.registry.json` |
| Registry SHA-256 | `201918b823708cd245e6c618dfbd758ae815130ee34c6837de4d64c3205817a8` |
| Source modules freshly compiled | 13 |
| Successful Lean commands, including the exhaustive audit | 14 |
| Distinct audited theorem declarations, including inherited/private/generated declarations | 1,244 |
| Registered endpoint types checked | 83 |
| Canonical report SHA-256 | `1697fa98fa01bd33ec990ca70858ad39182ff98c62dc82c3e811a0fb5d89e4cb` |
| `Agent10ThreeColumnExclusion.lean` SHA-256 | `965c4cb1dd1e32f6778fe144eb775814167d4379a9179e402f711cbc9bafce18` |
| `Agent10ThreeColumnCarry.lean` SHA-256 | `e884ec38e1561a27aa862ef857e7c65db99c0ed3c73fccefc2bec803cc51701d` |

The unchanged canonical verifier compiled the complete closure in a new empty directory. Its exhaustive module-origin audit permits only `propext`, `Classical.choice`, and `Quot.sound`; all theorem records passed. The thirteen unsafe implementation-specialization declarations inherited from the foundation are separately inventoried and occur in no theorem axiom dependency. The checker retains its historical `Agent #1` field; the actual build executor is Agent 10's parent, with separate specialist validation and semantic review.

All 83 registered endpoints are included in the exhaustive axiom audit. Eighty-one also have an explicit source `#print axioms` command; `observedBit3_value` and `state3_valid` are covered by the exhaustive audit without a separate print command. No endpoint is omitted from the mathematical audit.

Independent controls verify all 6,498 valid state encodings, 12,996 transitions against a digit-output formula, all 5,184 finite starts, and every admissible width-three and width-four projection, including overlapping reflected prefixes. Those finite controls accompany, rather than replace, the kernel proofs. Internal specialist review and source execution do not imply external GitHub approval or main integration.

## Reproduce

With the official pinned Lean 4.19.0 runtime described in `Agent10CarryObservability.md`, run from the repository root with a new output path:

```bash
python -B proofs/verify_project__214bf7673efe116b.py \
  --registry proofs/Agent10TwoPairReconstruction.registry.json \
  --project agent10-two-pair-reconstruction \
  --lean /absolute/path/to/lean-4.19.0-linux/bin/lean \
  --output /absolute/path/to/new-agent10-two-pair-build
```

The earlier eight- and eleven-module registries remain intact. These new sources continue to import the unchanged standalone foundation. The comments credit prior WholeWord and TwoDigit projection formulas; this package rederives only its needed arithmetic interface to avoid importing a duplicate foundation, and contributes the synchronized exclusion and reconstruction composition.

The preserved previous successful Carry revision is `d515d9a27d8b84e1a5397c30512f69a52155200c2353529362dced614dae13d3`. The final revision adds the all-width active-coordinate corollary. No proof of universal full eight-word reconstruction, optimal memory, infinite palindrome avoidance, or the 196 conjecture is claimed here.
