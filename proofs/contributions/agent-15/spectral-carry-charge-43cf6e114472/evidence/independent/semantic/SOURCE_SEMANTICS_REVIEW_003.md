# Independent source semantics review — snapshot 003

## Disposition

The four mathematical modules inspected at this snapshot faithfully implement the original U/S binary carry charge and its zero/symmetry theorem. The new SourceFormula adapter resolves finding R1 from snapshot002 at the source-semantics level. Kernel acceptance remains a separate runtime gate; this reviewer did not execute Lean.

All inspected bytes were read directly from the current local package after the parent reported claim `9ff01fb85383833abe440d7f41bc7c249c332070`. Exact snapshots and hashes accompany this report. The reviewer remains a nonauthor and made no proof-source edits.

## Source identities

| File | SHA-256 |
| --- | --- |
| `SpectralWeights.lean` | `07b3831f17a0d2e43a7e27cfd8a63d364a98ccbbcef87362a20cfbf24fb49db1` |
| `BinaryCode.lean` | `8db88d52e00dddbd32610dc09b7f8833f1ec1dc623b82236060b67bd2c9171f9` |
| `ChargeSymmetry.lean` | `28d11217cf147750ec2d07e64dbc6dabeee7deec7e543987817da611201b60a3` |
| `SourceFormula.lean` | `355fe970a97bcbc6038730efc89355d2fcd8383cdc24a332c21265e39af61efb` |
| `check.py` | `eec984af53abbc6ae66ade29bf62a591a29cd61b3473ec67e380891127c3f561` |
| `README.md` | `c6116f96b14e4a4170148ca474887909d3ec6fe1c746882f7d98b7987f70e0d2` |
| `CONTRACT.md` | `56f7b80c8028ba15b07b5b514e9f071dd2b9281bc727b12a39792f084b252030` |

## Changes to previously reviewed modules

SpectralWeights adds only an explicit `change` in the positive-growth successor proof to normalize the displayed indices. Definitions and theorem statements are unchanged. The author reported that the earlier snapshot failed Lean elaboration; the earlier review was explicitly semantic and did not claim compilation. The new weight bytes are `07b3831f17a0d2e43a7e27cfd8a63d364a98ccbbcef87362a20cfbf24fb49db1`.

BinaryCode adds only `rw [← hlen'] at by' dy` to express both tail bounds with the same length. Definitions and theorem statements are unchanged, and the additional rewrite preserves the reviewed binary/equal-length argument.

ChargeSymmetry is byte-identical to snapshot002. Its complete-word symmetry endpoint, domain and parity conventions therefore retain the previous independent semantic PASS.

## R1 resolved: literal source-sum adapter

SourceFormula adds an exact finite-sum bridge, including:

- `sumFirst_eq_range_sum`, which identifies its recursive accumulator with the ordinary integer sum of `(List.range n).map f`.
- `weighted_eq_sumFirst` and `weighted_take_eq_sumFirst`, which expose the descending-weight evaluation at each literal list index.
- `halfCharge_eq_source_sum`, which gives the exact mirror-index difference at `L-1-i`, using integer subtraction and the complete original length.
- Odd/even specializations and two final `carryCharge` source-sum endpoints under the respective exact length equations.

These are meaningful bridges rather than a renamed zero-charge hypothesis. The optional-list-entry default is not hiding an invalid index: the accumulator covers only `i<m`, the half-word length is bounded by the full length, and the proofs use the applicable in-range reversal/take identities. In the odd case `m-1-i+1=m-i` is justified only within `i<m`, giving the required U(m-i) and never the unused U(0). The even case retains S(m-1-i). The mirror index is respectively `2*m-i` or `2*m-1-i`, with exactly the source sign.

Thus the explicit task correspondence obligation now has formal theorem statements in the inspected source. Whether those proofs compile is not inferred by this report; the separate build/axiom gate must establish it on these exact bytes or on separately reviewed later bytes.

## Verification-script inspection

The inspected check.py declares the four selected modules in dependency order, copies them to a new output directory, sets LEAN_PATH to that isolated source directory, checks the official Lean version/commit string, records source/compiler hashes, and builds with the required trust/parallelism flags. Its public-declaration axiom gate requires all extracted public names to be reported and permits only the three agreed foundational axioms. The script explicitly leaves the broader module-origin audit to the independent runtime reviewer. This report records source inspection only; it does not claim execution of check.py.

The currently inspected closure does not yet include a separate kernel-control module. The finite Python control comparison in the design report remains accurately labeled as a bounded semantic check, not a kernel-certified control package. Any later controls require their own exact-source and execution coverage.

## Infrastructure interruption and preservation

A read-only rg invocation failed before it could execute because sandbox setup could not allocate a synthetic marker directory: exit101, `No space left on device (os error28)`. An escalated read-only df command confirmed the overlay at32GB used and0 available. No mathematical source was implicated by this infrastructure error. Read-only escalated source access succeeded and the exact returned bytes were retained in the tool session for later persistence. No cleanup, deletion, remote operation or source mutation was performed by this reviewer.

## Boundaries

The review does not claim T/R ownership, H, algebraic beta interpretation, support only on coefficient9, four-case dynamics, an ideal quotient, a palindrome criterion, persistence or196. The full binary outgoing-carry word includes its final bit and excludes a separately prepended incoming zero. The mathematical claim remains all finite binary words, both parities, with the empty word explicitly an algebraic extension.
