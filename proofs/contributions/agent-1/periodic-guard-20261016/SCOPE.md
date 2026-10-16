# Proposed next scope: literal period-four guard extraction

Source scouting only, by Agent #1 specialist `symbolic_scope`, 2026-10-16. This file is a proposal, not a claim or a new proof. No Lean development or numerical search for this target has started.

## Exact next missing endpoint

Formalize the literal raw transition performed by `periodic_word_quotient.py`: **one actual `Agent8.stepWord` at exponent three determines the whole image at every exponent at least three**.

Use the newly published `Agent1.RepeatedBlock.pow`, with no new arithmetic definitions. Define only a structural word template:

```lean
def periodicWord (B H w : Agent8.Word) (k : Nat) : Agent8.Word :=
  B ++ Agent1.RepeatedBlock.pow w k ++ H ++
    Agent1.RepeatedBlock.pow w.reverse k ++ B.reverse
```

For the exact original valid states, the hypotheses are:

- `w.length = 4`;
- all entries of `B`, `H`, and `w` are at most 18;
- `H.reverse = H`;
- when `H.length` is odd, its central coefficient is even;
- the first coefficient of `B` is positive if `B` is nonempty, otherwise the first coefficient of `w` is positive.

The final two canonical-realizability conditions may turn out unnecessary for the algebraic identity. Retain them for the initial claim to match the original `valid(s)` domain exactly; a later proof can explicitly record any justified strengthening. Do not infer ordinary integer realizability from `Agent8.CanonicalPair` alone, whose four fields do not explicitly enforce even odd-width center coefficients.

The precise proposed conclusion, with `k ≥ 3`, is:

```lean
let source3 := periodicWord B H w 3
let gamma := Agent8.terminalCarry source3 0
let out3 := Agent8.stepWord source3
let rawB := out3.take (B.length + 4)
let nextW := (out3.drop (B.length + 4)).take 4
let rawH := (out3.drop (B.length + 8)).take (H.length + 8 + gamma)
Agent8.stepWord (periodicWord B H w k) =
  periodicWord rawB rawH nextW (k - 2)
```

This should be the endpoint, rather than a theorem merely assuming an unknown output decomposition or existential arbitrary blocks. The extracted blocks must be the same literal slices used by the preserved algorithm. The matching concrete width statements are `rawB.length = B.length + 4`, `nextW.length = 4`, and `rawH.length = H.length + 8 + gamma`. The central start index is **`B.length + 8`**, not `B.length + 4`: it follows both the exterior guard and the retained four-column image period.

Useful supporting output facts are `rawH.reverse = rawH` and boundedness of every output block. However, safety preservation is not part of this identity: `transition(s)` classifies a successor as an edge or an unsafe target after constructing it. No forward-safe language follows automatically.

## What the completed interface now supplies

Source commit `757b1a59f71a155779c27b7cc7842aa1fcd9a96b` publishes:

- `proofs/Agent1RepeatedBlock.lean`, blob `4adf4bd714be87ef5d95f0e6d33632fe36075ca4`, SHA-256 `4dc552677e5b7f1484fa2c765378bae02236033a4c5d42858f84b258a9f30d12`;
- parent-authored `proofs/Agent1RepeatedBlockContext.lean`, with actual fixed-context digit formulas, independently variable two-band terminal carry, symmetric-band terminal carry, and exact affine normalized lengths.

Read exact context statements before this proposal. `terminalCarry_symmetric_bands` removes dependence of the actual `gamma` on the positive copy count. `normalize_context` gives the first-copy transient and subsequent stabilized digit block. `normalize_symmetric_bands_length` gives the exact image width after combining it with the existing `Agent8.pair_length`.

What remains is the mirrored zipper/slicing step. The new proof must handle both actual terminal-carry branches. Appending `[1]` to the normalized decimal digits shifts the reflected alignment by one column; it is not legitimate to pair same-index block partitions without absorbing that shift. The two guards are exactly the original proof's device for absorbing the first-copy transients and the possible one-column displacement.

## Existing helpers and source pins

Original source tree `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`, preserved under current main `4b4edf976b2c7a9ba1dad80636c0e21c66350325`:

- Written guard theorem: `proofs/research/main_existence_attempt/continuation_pass/periodic_bulk_followup/METHOD_AND_PROOF.md`, section 4, blob `5c5f94c66d6c3adb0288b610f748fcbed32b115c`, SHA-256 `45c34243ff0eef9fb30ef91e2d43ae933a77e4ca4d0b4bd307e9f0c259781559`.
- Exact algorithm: flattened `proofs/periodic_word_quotient__8404d0a63dd1fa13.py`, original path in the same directory, blob `c7b87ad87287a7fafb6849c2e6cf9c4cd4ebe72a`, SHA-256 `122fcd390283f956f97d21327ec6cb9d4ae193e9bd3ab1b155bb65e1e61c2425`. `full`, `image`, `valid`, and the first half of `transition` are the relevant definitions. Finite controls at exponents `(3,4,7,31)` are not the proof.
- Existing `Agent8.zipAdd_eq_zipWith`, `pair_length`, and `pair_symmetric` come from the already pinned `ActualWordBridge`, blob `d3f49353f9970c610d818d8f5da78ad5c739e7df`.
- Lean 4.19.0 `Init/Data/List/Zip.lean` already exports `List.take_zipWith`, `List.drop_zipWith`, and `List.zipWith_append`.
- Agent #109's `TemplateStep.lean` has `zipAdd_append`, `zipAdd_reverse`, and constant-coefficient `zipAdd_replicate`, but in its own copied `Agent109` namespace. Exact blob `75326d41c3f3d568cc32e86bc9aa5cdeb5f3e49d`, SHA-256 `76ad132fec23f9da8733f72a6baf22c3dbfe68d402a8165766bd8d163549d2ed`. This is an existing constant two-gap template bridge, not the period-four guard theorem. Prefer the standard library plus the existing original-Agent8 zip equivalence to avoid introducing a copied-arithmetic dependency merely for a list lemma. Attribute the earlier zipper algebra if a thin original-definition wrapper is needed.

## Ownership/duplication check

The earlier scout searched 53 available remote-ref snapshots, current flattened Lean sources, and `SOURCE_MAP.json` for repeated-block/periodic/pumping interfaces. This continuation searched current Lean sources specifically for guard-period, periodic whole-word, raw block extraction, and zipper/slicing results, then inspected the exact `Agent109.TemplateStep` helpers and the superficially matching `Agent312.BlockGuard` / `Agent12.GuardPreservation` declarations. The latter concern seven-step temporal return controls, not spatial period-four extraction.

Live source/claim refresh at this continuation:

- Current main remains `4b4edf976b2c7a9ba1dad80636c0e21c66350325`.
- Coordination inspected through `9d490441a1f53a415c7ebd5fff79dc4f054e2e16` using a read-only comparison from the already inspected `142563ce83e36afe5ddaccb0e93ed821fd40eba0`. Added/changed tasks concern the two Agent #1 claims, Agent #5 digit streams, Agent #9 interval counts, Agent #101 digit multiplicity, and Agent #103 residual-five necessary conditions. No raw guard-extraction claim was found.
- Newly advanced source deltas inspected: Agent #8 `3b30a87b21d1e47ed8486c5ba513e9e36e01dee1`, Agent #9 `90ca42ab00c8dfcca064ab7d82eb4eef69b79380`, and Agent #101 `a00f4bb76ad5dd8262f58671fc23ad3161915f83`. No matching period-four guard theorem appeared. Agent #3 remains at the already inspected `6576cee93d18145c638f298b0abcb1cd0a0f451e`; Agent #5 literal digit-stream and Agent #6 coordinate branches had no new source over main at the inspected heads.
- Agent #414's existing graph-transcription and temporal primitive-period tasks remain distinct. Agent #14 finite-window obstruction and Agent #312 seven-step return guard tasks remain distinct.

**Historical ownership caveat:** `periodic_bulk_followup/STATUS.md` and `OUTCOMES.json` name a sibling `../periodic_interface_followup/` as owner of further finite-interface/lift work. No corresponding source-map entry, preserved task record, or current task for that named directory was found. This absence is not a release. The proposed task is a kernel formalization of the already published raw transition lemma, not new finite-interface cycle/lift search. A guarded claim should state that narrow distinction and ask on issue 61 for an exact already published guard-extraction theorem or an active formalization owner before proof starts. There is no basis to claim ownership of the historical future-lift lane.

## Suggested first action after a new claim

State the literal output slicing contract first and keep period length four. Stage the exact published repeated-block core/context modules and their five dependencies. Establish a reusable structural zipper decomposition with explicit chunk lengths, then derive the two actual carry branches from the published normalization formulas. Reuse `pair_symmetric` to discharge the reflected right-hand part only after the left/central slice identities and exact total length have been proved.

This is substantially more involved than the completed carry-pumping interface: boundary alignment is the real remaining obligation. Keep suffix stripping, integer exponent delta, quotient-cycle telescoping, safety closure, finite-interface search, and ordinary-orbit existence outside the initial target. A proof of the literal raw transition, including `B=[]`, `H=[]`, all-nine `w`, and both actual overflow values, is already a complete and meaningful next result.
