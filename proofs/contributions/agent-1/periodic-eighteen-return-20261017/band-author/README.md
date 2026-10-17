# EighteenBand author evidence

Accepted task `agent1-periodic-eighteen-return-20261017`, claim `fcb20cb967483a96aa46261642d748fd32d4f5d6`; foundation `7f23ce839fcc88acb235b1816c2c57dc12e16a33`.

The two public results concern only the unchanged `periodicWord B H [18,18,18,18] k` and original `RunAncestry.MaximalRun`:

- `periodic_eighteen_band_run B H k hk` selects a maximal eighteen run `[a,b)` containing the entire left band `[B.length,B.length+4*k)`, with `a ≤ B.length` and `B.length+4*k ≤ b`, assuming only `k>0`.
- `periodic_eighteen_band_left_eq B H H' k k' i a b a' b' ...` equates the left endpoints of any two maximal runs containing the same anchor below both left-band ends, with the same exterior B. The interface retains the agreed `B.length ≤ i` premise; the proof actually works for common-prefix anchors as well, so Lean reports this one unused-variable warning. No linter is disabled.

Neither theorem assumes coefficient bounds, validity, symmetry, parity, exterior/center nonemptiness, or safety. Empty/all-eighteen B or H and runs joined through the center are included. The existence proof uses least natural witnesses privately to extend this specified constant band left and right. It exports no generic every-word interval constructor, run enumeration, or population theorem. The left-equality proof uses only equality of the two prefixes through the anchor and the original non-eighteen left-boundary condition, never a separate suffix formula or a right-boundary assumption.

Actual attempts, all preserved:

| Attempt | Result | Detail |
| --- | --- | --- |
| 001 | FAIL | `List.replicate_add` and tactic `by_contra` are unavailable in this Lean setup. Error recovery printed `sorryAx`; this is failed evidence, not an accepted theorem. |
| 002 | FAIL | An untyped local list index left a typeclass metavariable; two rewrites needed explicit beta reduction. Error recovery again printed `sorryAx`. |
| 003 | PASS | First strict source compile, both endpoint axiom prints standard-only. No full module audit was attached yet. |
| 004 | PASS | The identical source compiled again and the complete new-origin audit passed. All26 theorem constants, including private/generated proofs, use only the standard three axioms. There are no definition or opaque constants, custom axioms, or generated unsafe constants in this module. Both literal public types were printed. |

The official Lean4.19.0 compiler was invoked with `--trust=0 -j1 -DElab.async=false`, a600-second per-command timeout and4GiB address-space cap. Commands, compiler hash, exact source snapshots, logs, resource observations, dependency source/object hashes and actual exit codes are retained. The successful command resource records are in `attempt-004/commands.json`.

These checks reuse14 exact Periodic dependency objects from the successful pinned fresh Clock build and one unchanged original RunAncestry object freshly compiled by the Track author. The module's own logical closure is16 modules; the combined Return package has a different larger closure. This is an author incremental check, not a fresh dependency rebuild or independent verification. `dependency-provenance.json` records those distinctions; all15 source/object pins were rechecked at freeze. Root owns subsequent publication and combined fresh verification.
