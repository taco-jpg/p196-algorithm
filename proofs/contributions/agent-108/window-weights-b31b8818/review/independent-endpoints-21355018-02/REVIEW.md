# Independent endpoint review

**Disposition: PASS on the exact five-module closure recorded below.**

Reviewer: Agent #108 claims_inventory, a non-author specialist in the same session and shared authenticated account. This is internal independent review, not external peer review.

## Frozen source closure

| Module | SHA-256 |
|---|---|
| Agent108WindowDefs.lean | 147ae208dce3b612c6eb23091eab123b77bd46c86d216ab8a6199913015f0aa0 |
| Agent108WindowProducts.lean | 2920c9da6e3c06c40a1d8478fe1af0d87b00627976f53856f75b90de32a1e584 |
| Agent108WindowWeights.lean | 4dab41a584462ec298fcd745a304e301d237cf411f597af2c84aa8d705f7d95d |
| Agent108WindowEndpoints.lean | ebabfbfd366729846656ff5a56891c22f9c7f0868fca9c5918be433e5d5fbc22 |
| Agent108WindowEndpointWeights.lean | 21355018606cf7c2cfe8c33a008be815bd546bbafc31be69bc428624de0acab1 |

The Weight dependency is the author's retained exact three-declaration snapshot in endpoints/deps/. The parent was developing a larger Weight module during review; it was not silently substituted. A first source-guard failure, before any Lean command, is preserved in ../independent-endpoints-21355018/. That failure is not a mathematical or compiler rejection.

All five files were copied byte-for-byte and rebuilt from an empty build/ directory with pinned Lean 4.19.0 and **--trust=0**. All five compilation commands and the independent public-declaration audit exited zero. All **31 public declarations** in this exact closure were printed. The only transitive axioms reported are propext, Classical.choice and Quot.sound; elementary declarations report fewer or none. The two private real-product helpers are covered transitively by the public theorem audits.

## Literal endpoint semantics

The endpoint list is 9^b ++ [a] ++ 18^k, of length b+1+k. The actual window width is b+1, so the legal start positions are exactly 0 through k.

- Starts j with 0≤j≤min(k,b) give 9^(b−j) ++ [a] ++ 18^j. The assumptions j≤b and j≤k are explicit in endpoint_window_cross. No unavailable terminal digits are appended.
- Later starts satisfy b<j≤k and give exactly 18^(b+1). There are k−b such starts, where Nat subtraction clips to zero.
- The list equality endpoint_windows retains the original order and multiplicity. It does not just compare an unordered set or omit repeated windows.

### Boundary cases

| Boundary | Actual formula |
|---|---|
| b=0 | Windows are [a] followed by k copies of [18]. The crossing range has one element and the tail count is k. |
| k=0 | There is one complete window, 9^b ++ [a], and no all-eighteen tail. No k≥1 assumption is needed for this algebraic statement. |
| k<b | All k+1 windows meet the distinguished letter. The range stops at k and the all-eighteen tail is empty. |
| k=b | All b+1 windows meet the letter, ending with [a] ++ 18^b; the tail remains empty. |
| k>b | The final k−b windows are wholly in the terminal eighteen block. |

The reviewed statements retain all natural b, k and a where they are purely list/product identities. Coefficient bounds are introduced only when positivity of the potential is needed.

## Potential class and endpoint constants

PositivePotential b psi demands positivity only on lists of length b+1 whose entries are at most 18. Since entries are natural numbers, this is exactly the legal coefficient alphabet 0..18. There is no assumption that psi is positive on arbitrary-length lists or on out-of-alphabet data.

endpoint_product is a purely algebraic identity and makes no positivity assumption. It multiplies the product over the crossing range by psi(18^(b+1))^(k−b).

endpoint_ratio cancels this common terminal factor. The factor is nonzero because the all-eighteen window is legal and PositivePotential makes its potential strictly positive. When k−b=0, the common factor is 1; the same proof remains valid.

The denominator crossing word 9^(b−j) ++ [9] ++ 18^j is precisely 9^(d−j) ++ 18^j with d=b+1. Its length is d because the crossing range has j≤b. The first-window factor is psi([5] ++ 9^b)/psi([11] ++ 9^b), matching the original written constant.

The prefactor and denominator positivity proofs use only legal windows and the explicit bounds a≤18. The exact unpadded upper limit is min(k,b)=min(k,d−1). The constant has no r argument, so its independence from the number of binary blocks is represented directly.

## Scope

endpoint_constant_formula proves the head correction times the **local endpoint** product ratio equals the defined endpointConstant. It does not assert the global all-U-family/target ratio. That global identification still requires the separately developed word concatenation/product decomposition. Likewise, this endpoint package proves no actual buffered arithmetic transition or full incoming-fiber inclusion.

The parent subsequently froze a larger Agent108WindowWeights module at 5bc7f457187ad0af4a4f7a340acf7f827b8e89537d73624519805d232c762eae. Its separate independent combination verification belongs in ../independent-combination-5bc7f457/; this review's dependency version remains 4dab41a5.

## Evidence

build-results.json contains exact source paths, hashes, all commands and all 31 names. source/ contains the unchanged source snapshot and independent audit, while logs/ retains literal stdout/stderr. REVIEW_MANIFEST.json hashes the review package.
