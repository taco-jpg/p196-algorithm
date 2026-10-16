# Independently checked ordinary digit-sum collapse

The scalar consequence in strengthening-notes section 8 is now formally proved and independently reviewed. Both the author and the independent reviewer rebuilt the entire six-module project closure from fresh source directories with official Lean 4.19.0 and `--trust=0`. The mathematical source remained frozen throughout the independent gate.

## Exact result

Every canonical ordinary-decimal realization of `SeamAnnihilation.framedNine (2*r)` at width `2*r+2` satisfies

```text
digitSum n = 9*r+10
digitSum (Lychrel196.step n) = 2.
```

The universal scalar statement includes `r=0`. The existential result uses the unchanged original realization theorem for `r>0`, matching the manuscript's even interior length `k>=2`. Choosing `r=B+1` proves

```lean
∀ B : Nat, ∃ n d L, 0 < n ∧ DecimalDigits.Canonical n d L ∧
  B < DecimalMass.digitSum n ∧ B < L ∧
  DecimalMass.digitSum (Lychrel196.step n) = 2
```

The same positive finite integer exceeds both thresholds. Its canonical width is `2*B+4` and its initial digit sum is `9*B+19`. All natural thresholds, including zero, are included. The projected `arbitrarily_large_digitSum` theorem retains positivity and the two scalar conclusions.

The witness varies with the threshold. This is the manuscript's one-step collapse conclusion; it does not establish a statement about digit-sum divergence or palindrome avoidance along one fixed infinite orbit.

## Original results reused

The original `SeamAnnihilation` module already proves admissibility, positive canonical realization, the exact numeric first output `11*10^(k+1)`, and the two-step palindrome behavior. Those results are imported unchanged and retain their original attribution. The new proof uses the existing ordinary-digit-sum, pair-word-sum, carried-output, and value bridges.

The earlier scoped census incorrectly grouped the full example as unformalized. `CENSUS_AND_REUSE.md` records the expanded source/reference search and the correction: only the ordinary scalar consequence was missing. The existing `framedNine_mass` measures singleton seam defects, which is different from ordinary input digit sum.

## Acceptance gate

| Check | Independent result |
| --- | --- |
| Complete project closure | Five unchanged original modules and one new theorem module |
| Fresh source compilation | All six mathematical modules passed |
| Theorem constants audited by module origin | 1,320 |
| Safe definitions audited by module origin | 183 |
| New-module coverage | 21 theorem constants, including generated declarations; no new definitions |
| Named public exports | All ten have literal type and axiom reports |
| Permitted transitive axioms | `propext`, `Classical.choice`, `Quot.sound` |
| Selected source, registry, and recorded runtime identities | Unchanged |

Agent #9/horizon-safety authored the source. Agent #9/runtime-audit performed the independent semantic review and complete fresh compiler gate after the source freeze. The parent additionally read the complete source, without counting that reading as another compiler replay. The official runtime's standard objects were used as supplied; the workflow does not rebuild the Lean standard library or unrelated repository sources.

The frozen mathematical source has SHA256 `d9cb44e04c4f4bdbda42d7f877afeabd6e0c59cb085dfc023598707c7d0177db`, Git blob `a36a7c75aaf87d0ac72571286cbbdb8ba9a70134`.

| Final independent evidence | SHA256 |
| --- | --- |
| Semantic review | `e6f0d99dd662086775b957090a8d04bf1ceee623e5a10b409c42452e6427c02a` |
| Raw successful report | `c005ec5c0b392be38b7fa0b4ce92cc45154a9f9ce0a05a05e943db887ef6b854` |
| Exhaustive audit log | `0df88f1154598514a67fba9cce24f914a4e0e04359aaeb7e7bef423d34988a78` |
| Reviewer manifest | `5ef89d1ce343daa83761fe97e63352e1e0648d71bb6310f14840a6793cf1ff75` |

## Evidence and reproduction

The author packet preserves both complete attempts. The first failed on a redundant tactic after an already closed goal and on a missing `value_output` rewrite after `value_extended`. The second fresh run passed. The independent reviewer had separately identified the missing rewrite before that compiler result; this is attributed in the retained record. Failed sources, statuses, and full output remain intact.

Read `review/runtime-audit/SEMANTIC_REVIEW.md` and its raw `runs/full-001/verification.json` for the independent result. The author and reviewer each retain their source registry, verification driver, generated all-origin audit, runtime/source hashes, exact commands, and complete output. The evidence archive and per-file manifest recover every retained file in this contribution outside the evidence directory itself, with every recovered file hash checked. Reproducible compiled objects are excluded.

The manuscript is `proofs/research/continuation/strengthening_notes.txt`, section 8, original commit `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`, blob `7103ee939d82740b970dd23fb91e9db50db4ea54`. The original SeamAnnihilation blob is `e4ac85235d683c7877cb9adaf6e038816cf32038`. The exact source-main pin is `58afcada8047e015b8f4233b96c44c7c5b9c4162`.

The task was claimed at coordination `7b6c27c014bc00e55a75da530b8398b791451624` before implementation. `ROLLING_COVERAGE.json` separately records the current scoped continuation inventory, including completed and still-open endpoints. No main integration slot is claimed.
