# Independently checked factorial escape bound

The frozen mathematical sources have passed independent semantic review and a fresh complete source-closure replay with official Lean 4.19.0, using `--trust=0`, one worker, and an initially empty project object directory. This publication status supplements the earlier author checkpoint; the historical checkpoint and its manifest remain unchanged.

## Result

For every natural `κ > 0`, a natural-valued sequence with `E 1 = 1` and the exact manuscript recurrence satisfies

```text
E M ≤ (4*κ)^(M-1) * M!    for M ≥ 1.
```

The generic theorem leaves `E 0` unconstrained. Its factorial has the ordinary recursion `0! = 1`, `(m+1)! = (m+1)*m!`. Instantiating the unchanged decimal recurrence at `κ = 5` gives the closed bound `20^(M-1)*M!`; its extra zero-index case is proved separately from the existing `E 0 = 0` clause.

For every positive ordinary-decimal seed `n` and all natural `B,s`, the numeric endpoint proves

```lean
∃ t, s ≤ t ∧ t ≤ s + 20 ^ (2 * B - 1) * factorial (2 * B) ∧
  B < DecimalMass.digitSum (Lychrel196.orbit n t)
```

The time interval is inclusive. Natural subtraction makes the closed horizon equal to one at `B = 0`, whereas the inherited exact horizon is zero. The unchanged total orbit continues after palindromes. The result supplies a coarse explicit finite escape bound; it does not assert optimality, pointwise digit-sum divergence, palindrome avoidance, a new general-base dynamics theorem, or the 196 conjecture.

## Independent gate

| Check | Result |
| --- | --- |
| Mathematical import closure | Nine unchanged dependencies and two new proof modules |
| Fresh source compilation | All eleven mathematical modules passed |
| Exhaustive theorem audit | 1,456 theorem constants |
| Exhaustive safe-definition audit | 182 safe definitions |
| Coverage of the two new modules | 19 theorem constants and five safe definitions, including generated auxiliaries |
| Literal authored export reports | All eleven named exports |
| Transitive axiom union | `Classical.choice`, `Quot.sound`, `propext` |
| Selected source, registry, and compiler hashes | Unchanged |

Agent #9/runtime-audit performed the independent complete compiler replay and semantic review. Agent #9/horizon-safety supplied an additional read-only algebra check, separately attributed and not counted as another compiler replay. The original source path, commit, blob, and every dependency pin were checked independently. The selected official runtime is identified in the raw record; this workflow does not rebuild the standard library from source.

| Evidence | SHA256 |
| --- | --- |
| Independent semantic review | `1738d5e31c49c53011094bb13f7a94fc268d1631a4397803819dff9eb8d4f20c` |
| Raw independent successful report | `cf8f2216ec521039dcffdf0cb760effb395e868be1b785d22c74166864f1f9f0` |
| Independent exhaustive audit log | `54fb78d30c611ad4b522fdd4aa9189d80e698167b31111007c0576a08533b027` |
| Reviewer evidence manifest | `575ded4526f8403a88008b119b5b9fe60b239ffddcb8b3b612d0b03422187b63` |

The full reviewer packet is under `review/runtime-audit/`. Read `SEMANTIC_REVIEW.md` for the exact hypotheses and endpoint checks. The reviewer's `verify.py` and `source-registry.json` provide the independent reproducible gate.

## Complete evidence preservation

The lossless archive and its per-file SHA256 manifest are under `evidence/`. They recover every file in this contribution except the evidence directory itself: source snapshots, provenance, verifier scripts, author and reviewer logs, raw statuses, and review records. Each extracted file was compared byte-for-byte with its recorded hash before publication. Compiled objects are reproducible outputs and are excluded.

The initial generic arithmetic attempt failed because it lacked a distributivity rewrite. Its exact source and compiler output remain under `development/generic-001/`; the corrected version passed in `generic-002/` and in both complete closure checks. The author report's wrapped module-origin list required a reporting-only parser correction. The original report and verifier snapshot were retained, with a separate supplement; the underlying Lean audit had already checked all eleven module origins. Neither item is concealed or relabeled as a successful attempt.

The manuscript provenance is `strengthening_notes.txt`, section 5, equation (9), original commit `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`, blob `7103ee939d82740b970dd23fb91e9db50db4ea54`. The source branch starts at `ae8bbdfd2a18e8910eebc25fd2a81661c01abc16` and changes only this contribution directory. No main integration slot is claimed.
