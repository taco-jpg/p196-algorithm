# Independent Rebase interpretation review

Status: **PASS — independent interpretation review, one fresh canonical21 build, and a separate explicit trust0 full-import type-check/audit. All22 new explicit exports pass.**

The reviewer authored no Lean source in this task. Claim `e1bc61f552413f4a1ed6cef86c88265d39fd896d`, task blob `a277d7843d3509cf60a581ce06fb8d451975bea3`.

## Result and scope

For the original UpperDomain, the actual time2 component is corrected by the finite signed pattern `(1,-1,0,-1,1)` at columns `r+1` through `r+5`. The signed coefficients are proven nonnegative before `Int.toNat`; the resulting natural word C satisfies the original Admissible predicate at actual width `2r+7`. The whole actual time2 word, width `2r+8`, is exactly the one-column overlap of C. Every original canonical whole-input realization has this output pair prefix, and C has a positive ordinary canonical realization.

C is a different component: its valid column `r+1` exceeds the old actual component time2 column by1. This does not assert that C is the old component orbit, that ordinary output equals11 times a realization of C, or that later iterations keep a family invariant.

## Frozen source pins

- `proofs/Agent100GroupIIRebaseAlgebra.lean`: 5 explicit exports; SHA256 `d62f8769d9d2ee0ecf2ec3f0b0dffcd6c19cd5383692207e0e044b7649df02ff`; Git blob `d5185542692625baa8fc0dc171b58e86b53f6260`.
- `proofs/Agent100GroupIIRebaseProfiles.lean`: 11 explicit exports; SHA256 `2a95c9e88f315f3e317532e92a66afcc6dd09e1a97c2b5260fe97fae1c4b6771`; Git blob `68d13841fb475382422fe5b428306d60b9e2d874`.
- `proofs/Agent100GroupIIRebaseNumeric.lean`: 6 explicit exports; SHA256 `cecda22da5480e5b5fa5743f193a5aa68965cef707652e999d8da8087a0e0d41`; Git blob `2da082c6ebe444d3e8f2ed793428ff259e04abc4`.

## Detailed semantic checks

### Original domain and finite width — PASS

All intended rebase statements use original UpperDomain r>=1,p5..9,seven cores. Component width2r+7 and whole width2r+8 are actual upper-orbit widths, not guessed or widened windows.

### Signed correction and actual component — PASS

rebaseDelta is +1 at r+1,r+5 and -1 at r+2,r+4, zero otherwise. rebasedInt uses finiteNextComponent and is all-point identified with clipped actual componentOrbit time2 plus Delta.

### No negative truncation hidden by Int.toNat — PASS

rebased_nonnegative is proved for every Nat index before rebased_toNat_exact. At negative correction sites actual inner coefficient is2(u+v)-18>=2, so subtracting1 stays positive. At other positions nonnegativity is direct. Global cast(toNat)=signed identity is then explicitly proved.

### Bounds and original Admissible — PASS

Unmodified original Admissible is discharged: finite width positive, exterior unchanged/positive, every coefficient<=18, symmetry in width2r+7, and unchanged even center. The +1 flank uses exact2u-9 before correction; no raw redundant admissibility is assumed.

### Global support and boundary columns — PASS

rebased_zero_after_width proves C=0 for every i>=2r+7. The signed and Nat overlap statements cover i<2r+8 including i0 and the new rightmost whole column. previous is handled by zero/succ cases; finiteWord prevents reflected/clamped raw tails leaking into overlap.

### New component versus actual old component — PASS

rebased_differs_at_flank states Int cast difference1 at r+1. The proof explicitly knows r+1<actual width2r+7 before removing finiteWord. Thus C is a new valid component; the theorem does not identify C with old actualA2 or contradict old TwoStepOverlap iff.

### Arbitrary initial ordinary realizations — PASS

numeric_rebased_overlap and numeric_rebased_realization retain arbitrary original n,d with Canonical and full initial pair prefix. The actual output is orbit n2 at width2r+8. No favorable original representative is substituted.

### Existence and canonical corrected component — PASS

Positive C realization follows from proved original Admissible via valid_word_realizable. numeric_rebased_realization proves all-point equality of finiteWord applied to columnSum of actual canonical da with C, using both valid-prefix equality and proven zero tail. The final positive original-input existence is discharged by upper_initial_realizable.

### Exact scope limitations — PASS

The claims are pair-word/finite-overlap identities and positive canonical realizability. They do not state orbit n2=11*a as integers, that a is the old component iterate, any future rebase dynamics, invariant family, or infinite nonpalindromicity. Bounds<=9 were observed only in finite diagnostics; Profiles formally states<=18.

## Independent finite controls

One self-contained Python run checked 105 tuples: all seven cores, every p=5..9, and r in {1,2,7}. Each component and whole input had two distinct extreme canonical digit splits, including zero units digits, and all840 ordinary integer reverse-additions were retained. Every signed coefficient was nonnegative before Nat projection, each C passed the original admissibility conditions, and every complete Phi(C) equaled the actual whole time2 word. Every C differed from actualA2 at valid corrected sites. These observations remain bounded diagnostics, not universal theorems.

The complete1,344,046-byte JSON retains every input/output integer as an exact decimal string, every digit word, every pair word, the signed vector before conversion, all differences and positive C realizations. Its XZ archive was actually decompressed and compared byte-for-byte. See `reviewer-controls-manifest.json`; no diagnostic rerun was needed.

## Execution status

The actual21-module closure was built fresh from exact frozen source without author oleans, using the unchanged canonical verifier and official Lean4.19.0. All21 module compilations and the original ProjectAudit exited0:22 recorded commands, one fresh source build. The canonical commands did not explicitly set --trust=0 and are not described as doing so.

A separate actual invocation of the same ProjectAudit with --trust=0 -j1 -DElab.async=false over those same fresh21 imports also exited0. It typechecked all imported modules and re-audited every2661 local theorem constant. All theorem names and complete axiom sets match the canonical audit, and all source/fresh-olean posthashes are unchanged. This is an additional strict import audit, not a second source build.

Every one of the22 explicit new exports was matched between its complete multiline raw #print axioms list and the full module-origin ledger. The three new modules contribute85 theorem constants including generated declarations. Fourteen explicit new exports use propext and Quot.sound; eight additionally use Classical.choice. The actual complete closure union is exactly those three standard axioms. Fourteen inherited unsafe implementation declarations are separately reported and occur in no audited theorem dependency set. Both inherited historically corrected endpoints are verified with their complete three-axiom sets in this new run.

The actual run source HEAD was686cac2696e4e4e059c1b9d6a313f5519f6f4176. Complete mathematical source publication isbc178ab8735e9503ab25b325e5a8dc82bf1f1e37, tree9c59d8266aeba792f7a376c83c6f72d9aee24e25, DraftPR138. Independent immutable git show reads confirmed all21 published sources equal their current local files and fresh snapshots byte-for-byte. See verification/reviewer-post-build-source-identity.json. No shared accepted registry was modified and no repository-wide integration is claimed.

## Explicit exports that use Classical.choice

- `Agent100.GroupIIRebase.rebase_delta_overlap`
- `Agent100.GroupIIRebase.rebasedInt_overlap`
- `Agent100.GroupIIRebase.finite_whole_rebasedInt`
- `Agent100.GroupIIRebase.actual_whole_rebasedInt`
- `Agent100.GroupIIRebase.actual_whole_rebased`
- `Agent100.GroupIIRebase.numeric_rebased_overlap`
- `Agent100.GroupIIRebase.numeric_rebased_realization`
- `Agent100.GroupIIRebase.realized_rebased_overlap`
