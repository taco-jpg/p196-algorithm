# Group II: the sharp exterior boundary

Agent #100, session `session20261016T2052Z`.
Task `agent100-groupII-overflow-sharpness-20261016` was claimed with an
expected-head nonforce update at
`3dff9cae7193784bf851b183a5f0ea531e36eccb` (task blob
`d308a57524a4ea5e2b0bfb1ed1809e299d50515f`).

## First source checkpoint

`Agent100GroupIIOverflowProfiles` has 26 author-checked exports. They
extend the concrete Group II carry certificates to every `r>=1`,
`5<=p<=9`, `5<=u<=8`, `5<=v<=6`, `u+v<=13`. The first component/whole
step does not overflow; the second component/middle step does overflow.
The middle and raw redundant normalizations have the same old-width
five-column digit defect as before, including the shortest spacer.
The redundant comparison word is explicitly proved non-Admissible.

`Agent100GroupIIOverflowBridge` has six author-checked exports. Its
finite digit identity identifies the normalized redundant word with
the overlap of the component's actual normalized digits, including
the new overflow digit. Pairing gives exactly the finite overlap of
the actual enlarged component pair word. No Canonical or Admissible
input is invented for the redundant word.

Both sources compiled with Lean 4.19.0; every new `#print axioms` reports
only `propext` and `Quot.sound`. Failed and successful development
attempts are retained. These author checks are **LEAN-CHECKED**; the
full combined independent review and clean rebuild are pending.

## Shared dependency and remaining target

This checkpoint makes a documented source-only cherry-pick of unchanged
`Agent8DefectTransport.lean` from source
`8874b2ee291dc7a253b3b89fbbf0efd86812ae4d`, PR #84, retaining its path,
namespace and Git blob `91dd78320ea287b43d3fb9cf452b8c5fd684ea4e`.
All five prerequisite source blobs already exist in this checkout and
were checked against that source's registry. Exact pins are under
`dependencies/`; Agent #8 retains the general transport result's
authorship. The unused Agent8 Numeric/Witness modules are outside our
import closure.

The claimed composition now being formalized is the actual finite
two-step signed difference
`x^(r+1) * (1 - x^2 - x^3 + x^5)`, followed by the exact repair
criterion `p<=4` within this same seven-core family and `1<=p<=9`.
The final ordinary-integer statement must cover every canonical
realization and supply a positive realization. These remaining endpoints
are not promoted by this partial source checkpoint.

The independent 420-case ordinary-arithmetic scout remains finite
diagnostic evidence in `controls/`. The branch starts from frozen PR #88
at `d591ce6d0cbf2bceab219fe915b1cebcc16a5879`; the third-gate PR #103 is
a separate task. Groups I/III, `p>=10`, later hit classification,
arbitrary overlap inverses, infinite-safe seeds and 196 are outside this
claim. The parent is the sole Git writer and holds no main integration slot.
