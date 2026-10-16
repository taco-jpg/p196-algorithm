# Independent review of fixed window core

Reviewer: Agent #108 runtime, session b31b8818. Result: PASS for the exact public mathematical interface below.

The original attempt is retained byte-for-byte. Its aggregate `audit_pass=false` treated compiler execution declarations as mathematical declarations. This report corrects that classification using observed Lean `ConstantInfo` metadata; it does not expand the logical axiom allowlist.

## Fixed sources and clean build

| Module | SHA256 |
|---|---|
| Agent108WindowDefs.lean | `147ae208dce3b612c6eb23091eab123b77bd46c86d216ab8a6199913015f0aa0` |
| Agent108WindowProducts.lean | `2920c9da6e3c06c40a1d8478fe1af0d87b00627976f53856f75b90de32a1e584` |
| Agent108WindowEndpoints.lean | `ebabfbfd366729846656ff5a56891c22f9c7f0868fca9c5918be433e5d5fbc22` |

The three fixed sources were copied into the new empty `agent108-runtime/core-review-build/001` directory. Direct official Lean 4.19.0 compiled Defs, Products, Endpoints and the complete namespace audit; all four commands exited 0. `LEAN_PATH` contained only this new build. No Mathlib or other project module was imported. The source bytes were checked before and after. Exact commands, output and elapsed times are in `attempts/001/verification.json` and its logs.

The additional metadata collector ran with `--trust=0` and exited 0. It classified all 84 namespace declarations, including generated definitions and proof helpers. Public source declarations have a one-to-one correspondence with the 17 rows below.

## Every public source declaration

| Module | Declaration | Kind | Transitive axioms |
|---|---|---|---|
| Agent108WindowDefs | `windows` | def | none |
| Agent108WindowDefs | `buffer` | def | none |
| Agent108WindowDefs | `block` | def | none |
| Agent108WindowDefs | `blocks` | def | none |
| Agent108WindowDefs | `inputHalf` | def | none |
| Agent108WindowDefs | `targetHalf` | def | none |
| Agent108WindowDefs | `localBlock` | def | none |
| Agent108WindowDefs | `endpoint` | def | none |
| Agent108WindowDefs | `choices` | def | none |
| Agent108WindowProducts | `windows_nil` | theorem | none |
| Agent108WindowProducts | `windows_short` | theorem | propext |
| Agent108WindowProducts | `windows_append_overlap` | theorem | propext, Quot.sound |
| Agent108WindowProducts | `windows_eq_range_map` | theorem | propext, Quot.sound |
| Agent108WindowProducts | `windows_length` | theorem | propext, Quot.sound |
| Agent108WindowEndpoints | `endpoint_window_cross` | theorem | propext, Quot.sound |
| Agent108WindowEndpoints | `endpoint_window_tail` | theorem | propext, Quot.sound |
| Agent108WindowEndpoints | `endpoint_windows` | theorem | propext, Quot.sound |

All 17 public declarations are safe and nonpartial. Of all 84 namespace declarations, 45 are safe and nonpartial, 36 are unsafe compiler declarations, and 3 are partial compiler declarations. Every safe nonpartial declaration has only a subset of the allowlist `propext`, `Classical.choice`, `Quot.sound`.

`choices._cstage2` is an unsafe compiler definition. Its two unusual dependencies, `List.mapTR.loop._at.Agent108.WindowWeights.choices._spec_1` and `_spec_2`, are both explicitly marked unsafe axioms by Lean. Neither is a dependency of public `choices` or of a mathematical theorem. All 84 original axiom outputs and all metadata are retained. These two names were not added to the logical axiom allowlist.

## Mathematical correspondence

- `windows` enumerates complete unpadded windows. The public width convention is `b+1`, so width is strictly positive. No theorem claims the conventional empty-window count at width zero.
- `windows_short` removes starts that cannot supply a complete window. `windows_eq_range_map` identifies starts exactly as `0 ≤ i < length(w)-b`; `windows_length` counts the same starts.
- `windows_append_overlap` requires exactly `b` letters of overlap for width `b+1`. Each complete window has exactly one of the two represented starts; there is no double count and no omitted boundary window.
- `endpoint_windows` covers every natural `b,k,a`. There are `min(k,b)+1` windows meeting the distinguished letter and `k-b` wholly terminal windows. Their total is `k+1`, including `b=0`, `k=0`, and `k<b`. No `k≥b` hypothesis was silently inserted.
- The definitions record the literal half-word family only. They do not prove a decimal reverse-and-add transition, membership in a safe incoming family, or avoidance of palindromes for infinitely many steps.

## Long-buffer embedding feasibility (analysis only at the time of this review)

For any `p`, encode a bit list `es` as `false^p ++ flatMap (fun e => e :: false^p) es`. Its length is `m=p+(p+1)*length(es)`. Since the old false block is four nines, the unbuffered source at the encoded bits has exactly physical buffer `B=4p`. Original bits occur at indices `p+(p+1)*j`, giving recovery and injectivity. The old target has `4m+1 = length(es)*(4p+4)+4p+1` nines, matching the long-buffer target.

Taking `p=d` gives the proposed buffer `4d`. A width-`d` weight proof must keep physical buffer and window width independent; simply substituting `b=4d` into a width-`b+1` theorem would not prove an arbitrary-width claim. Extra pure-nine windows must be matched and cancelled in source and target. The embedding requires exact list/pointwise correspondence and subfamily inclusion, while the previously verified Agent13 arithmetic API supplies carry, transition and finite safety. No new carry proof is required.

Evidence: `review-result.json` is the classified final result; `attempts/001/verification.json` and the top-level `latest-verification.json` deliberately preserve the original unclassified aggregate failure.
