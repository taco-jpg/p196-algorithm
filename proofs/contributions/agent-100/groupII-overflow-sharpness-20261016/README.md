# Group II: the sharp exterior boundary

Agent #100, session `session20261016T2052Z`.
Task `agent100-groupII-overflow-sharpness-20261016` was claimed with an
expected-head nonforce update at
`3dff9cae7193784bf851b183a5f0ea531e36eccb` (task blob
`d308a57524a4ea5e2b0bfb1ed1809e299d50515f`).

## Complete mathematical source checkpoint

All five modules, comprising 52 new theorem exports, are frozen at complete
source commit `686cac2696e4e4e059c1b9d6a313f5519f6f4176` (tree
`6f25211e084ebee89ca964820e03258cd294b361`, Draft PR #125). Author checks
and a separate nonauthor interpretation review of all 52 statements passed.
The independent execution is now complete: **one fresh canonical 18-module
build, with all 19 commands passing, followed by one explicit `--trust=0`
full-import audit passing**. Both full audits cover the same 2,576
module-origin theorem constants and 52 new explicit endpoints.

The original canonical commands omitted `--trust=0`; the official compiler's
default trust level is `max`. They are not described as an explicit trust-zero
build. The additional actual strict audit took 57.486 seconds and typechecked
the imports from that fresh build. It was not a second fresh source build.

The first 32-export source checkpoint is
`491b477889b6336f5386287e3665f6ce58a34d9b`; the complete five-file source
publication above adds transport composition, actual-orbit sharpness and
ordinary-integer endpoints without changing those first two modules. This
final evidence checkpoint does not change any of the five mathematical sources.

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

## Shared dependencies and completed independent verification

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
The independent interpretation review, fresh canonical closure, complete
multiline axiom ledgers and explicit trust-zero imported-module check have
all passed. Publication of this final evidence checkpoint, formal review on
its exact published head and serialized integration remain separate steps.

The genuine independent executor and semantic reviewer was Agent #100
`scope_audit`, who authored none of these five Lean modules. Profiles and
Numeric were authored by `groupii_dynamics`; Bridge and Sharpness by
`runtime_setup` acting as a formalizer; Defect by the parent. The parent alone
publishes Git changes. This is a nonauthor review within the same session and
shared account, not a separate-account approval or external peer review.

The actual canonical execution used the unchanged `verification/replay.py`
and canonical verifier; its receipt is
`verification/independent01/independent-invocation.json`. The actual run HEAD
was `491b477889b6336f5386287e3665f6ce58a34d9b`, while the original branch
base was `d591ce6d0cbf2bceab219fe915b1cebcc16a5879`. Neither field is
silently treated as containing all five later source files. The registry pins
the bytes actually built. `verification/post-build-source-identity.json`
records independent immutable `git show` comparisons proving all 18 published
source files at `686cac2696e4e4e059c1b9d6a313f5519f6f4176` equal both
their fresh build snapshots and their post-run local files. The canonical
`source_tree_clean` field ignores untracked files and is not used to infer
that those files already belonged to the run HEAD.

The actual additional command was
`lean --trust=0 -j1 -DElab.async=false ProjectAudit.lean`, run in
`verification/independent01/groupii-overflow/source` with that exact source
directory as `LEAN_PATH`. Its report is
`verification/strict01/strict-import-verification.json`; exit status is 0,
elapsed execution is 57.486 seconds, and its full log is
`verification/strict01/ProjectAudit-trust0.log`. All 2,576 theorem names,
origins and complete axiom sets agree with the canonical multiline ledger;
all source/compiler/fresh-olean identities remain unchanged. The permitted
theorem-axiom union is exactly `propext`, `Classical.choice`, `Quot.sound`.
Fourteen existing unsafe implementation declarations are inventoried
separately; no audited theorem depends on them.

### Reproducible pins and retained evidence

- Registry: `verification/registry.json`, SHA256
  `ac68e397f5a12326ed7a788a0e021edda22be46216bcc98c5bc45f71933c6533`.
- Unchanged verifier: `proofs/verify_project__214bf7673efe116b.py`, SHA256
  `c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a`.
- Official Lean 4.19.0, release commit `6caaee842e94`, executable SHA256
  `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.
- Original complete canonical archive:
  `verification/independent01-complete-evidence.tar.xz`, SHA256
  `b371c559c185f1cf28e621633a0c87a04b5e9d193801839f16255fa8fccd0e5a`.
  This archive remains byte-identical; its historical commands are preserved.
- Separate actual strict amendment:
  `verification/strict01-evidence-amendment.tar.xz`, SHA256
  `a29f0ebcb127606f47120528c0612e6360d88cd0ab7d0140fff105d051f3d690`.
  Its separate member manifest records verified lossless decompression.
- Independent semantic review: `controls/overflow-semantic-review.md` and
  `.json`; complete execution details and ledgers: `verification/README.md`,
  `verification/complete-axiom-ledger.json` and the strict report above.

For future reproduction, use the additive `verification/reproduce.py` with
`--lean`, a nonexistent `--output` directory and the actual `--executor`.
See `verification/REPRODUCE-NOTES.md`. It invokes the unchanged canonical
verifier and then explicitly runs the strict import audit, keeping canonical
and raw ledger attribution labels intact while recording the current operator
separately. This future entry point has passed AST, CLI and command-construction
checks only; it has **not** been executed end-to-end. The actual evidence here
comes from the retained original replay plus the separately executed strict
follow-up, not from an invented run of the new launcher.

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
arbitrary overlap inverses, modified-component rebasing, infinite-safe seeds
and 196 are outside this claim. In particular, failure relative to the actual
time-two component is not a claim that no other component could represent
the whole word. There is no later-time or infinite-orbit assertion.

These are scoped author and independent checks, not a repository-wide PASS
or integration of PR #125. Exact-head formal review, Ready status and target
integration must be recorded only after their actual publication/actions.
The parent is the sole Git writer and holds no main integration slot.
