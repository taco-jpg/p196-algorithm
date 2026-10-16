# Group II: the sharp exterior boundary

Agent #100, session `session20261016T2052Z`.
Task `agent100-groupII-overflow-sharpness-20261016` was claimed with an
expected-head nonforce update at
`3dff9cae7193784bf851b183a5f0ea531e36eccb` (task blob
`d308a57524a4ea5e2b0bfb1ed1809e299d50515f`).

## Complete mathematical source checkpoint

All five modules, comprising 52 new theorem exports, are now author
**LEAN-CHECKED** under Lean 4.19.0. The separate nonauthor reviewer has
examined all 52 statements and their interpretation; a fresh independent
18-module source build and full dependency audit are running. This
checkpoint does not claim that independent execution has finished.

The first 32-export source checkpoint is
`491b477889b6336f5386287e3665f6ce58a34d9b`. The present checkpoint adds
the complete transport composition, actual-orbit sharpness theorem and
ordinary-integer endpoints without changing those first two modules.

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

`Agent100GroupIIOverflowDefect` has six exports. It applies Agent #8's
unchanged common-overflow transport theorem to the exact middle and raw
redundant profiles. The old five-position defect becomes the six-position
signed defect `(1,0,-1,-1,0,1)` at indices `r+1` through `r+6`. The
concrete finite-component bridge is our `runtime_setup` specialist's
module above; the general transport theorem retains Agent #8's authorship.

`Agent100GroupIIOverflowSharpness` has nine exports. It uses the actual
component and whole pair orbits at their actual widths and explicitly
zero-extends the finite component before forming its overlap. The main
endpoint is `Agent100.GroupIIOverflow.two_step_overlap_iff`:

```lean
two_step_overlap_iff (r p u v : Nat) (h : FullDomain r p u v) :
  TwoStepOverlap r p u v ↔ p ≤ 4
```

Here `FullDomain` means `r>=1`, `1<=p<=9`, `5<=u<=8`, `5<=v<=6`,
and `u+v<=13`. For the upper branch the component and whole widths at
time two are `2r+7` and `2r+8`; the exact mismatch is witnessed at
`i=r+1`. The lower branch includes the finite-tail proof required to use
the previous exact-return result with the actual finite component.

`Agent100GroupIIOverflowNumeric` has five exports. Every canonical
ordinary-integer realization of the initial upper-domain whole word has
an actual second reverse-add output of width `2r+8`, with the same exact
signed difference at every valid column. `realized_overflow_defect`
also supplies a positive initial realization for every upper-domain
parameter tuple. This is not an assertion of an eleven-fold relation
between independently chosen integer representatives.

All 52 exports have literal `#print axioms` output. The author logs report
only `propext` and `Quot.sound`, except the final sharpness iff, which also
uses `Classical.choice`. Failed and successful development attempts are
retained outside the accepted source closure. The numeric candidate
snapshot and incomplete historical command receipt are identified as such
in the author-execution records. No candidate or environment failure is
counted as a proof.

## Shared dependencies and remaining verification

This checkpoint makes a documented source-only cherry-pick of unchanged
`Agent8DefectTransport.lean` from source
`8874b2ee291dc7a253b3b89fbbf0efd86812ae4d`, PR #84, retaining its path,
namespace and Git blob `91dd78320ea287b43d3fb9cf452b8c5fd684ea4e`.
All five prerequisite source blobs already exist in this checkout and
were checked against that source's registry. Exact pins are under
`dependencies/`; Agent #8 retains the general transport result's
authorship. The unused Agent8 Numeric/Witness modules are outside our
import closure.

The complete new source proves the actual finite two-step signed
difference represented by `x^(r+1) * (1 - x^2 - x^3 + x^5)`, the exact
criterion above, and its universal ordinary-integer realization endpoint.
Remaining gates are completion and publication of the independent clean
build, complete axiom ledgers and formal exact-head review.

PR #88 has now been integrated at main
`7b9e663b3c40aadfd7038f264729f6b7e3c7ce88`. Agent #11's additive evidence
correction at `c0534138ff90f9d276624aded3cc5cf00e6a4c11` fixes two
historical summarized axiom entries: `returnedComponent_core_table` and
`returnedComponent_not_same_shape` each depend on all three permitted
foundations. Their unchanged original raw logs already report this.
The new audit parses complete multiline axiom lists and compares them
against its own fresh full module-origin report.

The independent 420-case ordinary-arithmetic scout remains finite
diagnostic evidence in `controls/`. The branch starts from frozen PR #88
at `d591ce6d0cbf2bceab219fe915b1cebcc16a5879`; the third-gate PR #103 is
a separate task. Groups I/III, `p>=10`, later hit classification,
arbitrary overlap inverses, infinite-safe seeds and 196 are outside this
claim. The parent is the sole Git writer and holds no main integration slot.
