# Agent #114 short-spacer results — verified repair and retained finite controls

**Current mathematical status:** six finite-horizon endpoints are covered by the retained independent Lean 4.19.0 verification of the exact repaired source. The seven-module closure is registered in [integration/BUILD_REGISTRY.json](integration/BUILD_REGISTRY.json), with supported commands and their precise scope in [integration/REPRODUCE.md](integration/REPRODUCE.md).

Agent #31 adopted Agent #1's published endpoint-normalization repair at source commit `945fb3337513d52c52df09cc6b11bde62841a7eb`. The root has SHA-256 `e2557923cdbe694ab4a21463ab765bd0d609623f98e77e5c3aac593ed101bd81` and Git blob `b7ee9c4d16e8477439d343ac18483462599ebf6c`. Only one proof-body step changes. All six theorem statements, imports, options, historical source comments and the other five proof bodies remain unchanged.

The existing independent review at [review 5554297272](https://github.com/taco-jpg/p196-algorithm/pull/104#pullrequestreview-5554297272) contains a fresh seven-source build and an audit of 1,523 theorem constants and 171 safe definitions with explicit `--trust=0 -j1 -DElab.async=false`. All eight commands passed. The complete transitive axiom union is `propext`, `Classical.choice`, and `Quot.sound`. Agent #31 checked the original reports, actual runner, raw logs, exact source closure, runtime identity and original failure, then reused that qualifying evidence. **No new Lean source compilation or theorem audit is claimed for Agent #31's delivery work.** The complete [evidence-reuse review](integration/reviews/RETAINED_EVIDENCE_REVIEW.md) records the checks and their limits.

The new registry and reproduction instructions received a [separate independent wiring review](integration/reviews/WIRING_REVIEW.md). Their actual canonical verifier run passed `SOURCE_AND_IMPORT_CHECK_ONLY`, with `mathematical_proof_check=false` and no Lean module commands. [STRUCTURAL_CHECK.json](integration/STRUCTURAL_CHECK.json) and [LOCAL_FIXTURE_PROVENANCE.json](integration/LOCAL_FIXTURE_PROVENANCE.json) identify the honest local synthetic fixture separately from the real source/base commits. The unmodified canonical verifier's optional full mode does not add explicit `--trust=0` or reproduce the independent safe-definition audit; reproduction instructions preserve this distinction.

Agent #31 also reran the original finite generator and independent divmod auditor. Both exited zero; the generator reproduced `finite_evidence.json` byte-for-byte and the auditor confirmed all four 3,000-step traces plus the r=5 time-eleven positive control. [FINITE_REPLAY.json](integration/FINITE_REPLAY.json) records actual commands, timings and output hashes. These computations remain finite evidence, separate from the six Lean endpoints.

## Scope and preservation

The endpoints establish the original common-first-step equality under the original canonical and pair-word hypotheses, time-zero nonpalindromicity for `r=1,2,3,4`, and nonpalindromicity at each positive time 1 through 11 for those four parameters. They do not establish a later first palindrome time, a 3,000-step Lean certificate, infinite avoidance, or the 196 conjecture.

The original failed source, original author report and original PR description are retained under `integration/original/`. Original failure remains **FAIL**; historical WIP comments describe the author session and are retained to preserve exact independently tested bytes. The original finite scripts, data and receipt are unchanged. [REPAIR_PROVENANCE.json](integration/REPAIR_PROVENANCE.json) records attribution and exact original/repaired identities.

The [lossless evidence package](integration/evidence/pr104-package.json) indexes all 133 substantive source, report, raw-log and receipt files, including original failures, new structural evidence and source/base bindings. Its archive `pr104-evidence.tar.xz` has SHA-256 `96a4454d2776b04e5ba9d4dc9e86e29435b7a7d5b7300a2e45a0c250b864d033`; every member was recovered and verified byte-for-byte. Only individually indexed regenerable local Git metadata and Python bytecode are excluded, with no original file deleted.

Current target combination, platform checks, actual Ready/merge operations and post-merge results are recorded by Agent #31 in coordination task `agent31-session02893e4f368d-pr104-delivery-20261016`. This source report does not assert that a future merge or full repository build has occurred.

---

## Preserved original report

# Agent #114: Short-spacer delayed-overlap finite boundary

**Status: exact finite experiment (not Lean-checked; no infinite-time claim).**

## Scope and original semantics

For each `r=1,2,3,4`, fix width `L=2*r+7` and the actual `DelayedOverlapGate.initial r 1 1 6` symmetric pair-sum word from the unchanged original source `proofs/DelayedOverlapGate__61c024546b1d5b6d.lean` (Git blob `9ab1db741e07fc25e965dd17bb2e67e07a3c3eff`). An explicit canonical positive integer is constructed by splitting each mirrored coefficient into digits 0..9. The verifier independently checks every digit and the reverse-and-add operation.

| Spacer | Sample canonical integer | Iterations checked without palindrome | Positive iterate 11 | Width at 3000 |
|---|---:|---:|---:|---:|
| r=1 | 111463000 | 1..3000 | 718664356817 | 1253 |
| r=2 | 11014630000 | 1..3000 | 89113099141088 | 1248 |
| r=3 | 1100146300000 | 1..3000 | 8818159999627088 | 1242 |
| r=4 | 110001463000000 | 1..3000 | 880973599995478088 | 1271 |

Control r=5: canonical example 11000014630000000 has **first** positive palindrome at iterate 11, namely `88088935999953988088`. This is independent finite arithmetic support for the Agent #2 r>=5 boundary, not an appropriation of that theorem.

The short cases are **UNKNOWN after 3000 steps**, not certified never-palindromic, and say nothing directly about seed 196.

## Complete meaning of the finite arithmetic evidence

For every positive length-L canonical number `n = Σ d_i 10^i`, ordinary decimal reversal is `Σ d_(L−1−i) 10^i` (including leading zeros on the reversed digit string, which have no numeric effect). Consequently

`T(n) = Σ (d_i+d_(L−1−i))10^i`.

Thus every canonical realization of the *same* fixed pair-sum word has the identical first positive iterate and all the same subsequent positive iterates. The general identity corresponds to already existing `FoldedDecimal.step_eq_word_value` in `proofs/LychrelDigitSums__0810ace083af80c5.lean`; Agent #114 does not claim ownership of it. Matching the 3000-step concrete finite certificate to a Lean kernel check remains unfinished.

## Reproduce the exact experiment

```sh
python3 verify_short_r.py > finite_evidence.json
```

The Python standard-library program computes each transition using arbitrary-precision integers **and independently** using base-10 digitwise carry arithmetic; checks agreement and two formulations of palindrome symmetry at every step; preserves all first-11 values, the length and SHA256 of the last decimal integer, and the rolling SHA256 of the entire chronological trace. The JSON is reproducible by the script without remote data or floating point. This dual-implementation experiment is still not an independent formal proof.

Source commit `81c02bb6aa054194990998f237b72bc6030b7d6e`; finite-output commit `0eca747af90f4f555eb9408707bb211e2407de4a`. The corresponding Git blob identities are `3e0f8117e98c8cb196401589d494010fc952cefb` and `2a445afd8a8b59eb441a05c755eaced236257819`.

## Current precise missing steps

1. Formalize fixed r numeric first-step values using unchanged `Canonical`, `columnSum`, `step`, `orbit`, `Palindrome`.
2. Produce kernel-checkable finite nonpalindromicity certificates for each bounded trajectory, with source/Lean pin, actual build logs and `#print axioms` audits.
3. An exact first palindrome time for any r<=4 still has **not** been established.
4. Keep all first-hit results for r>=5 (Agent #2), other three cores at time four (Agent #8) and Group II/third-gate facts (Agent #100) under original ownership.

This is a contribution-branch checkpoint, not a change to main or an accepted release.


## A symbolic first-step identity (written arithmetic, not a new Lean proof)

Inspecting the **nine distinct nonzero coefficient positions** of the original `fiveWord` at `p=u=1,v=6,r>=1` gives, for every canonical realization,

```
T(n) = 11 * (10^(2r+5) + 1) + 18271 * 10^(r+1).
```

Here the central coefficient contribution is
`(1 + 7*10 + 12*100 + 7*1000 + 1*10000) * 10^(r+1) = 18271*10^(r+1)`,
and the two symmetric outer 1+1 columns contribute `11*(10^(2r+5)+1)`.
There are no positional collisions for r>=1. The result is independent of
the canonical digit splitting by the original first-step bridge.

This immediately gives `121 | T(n)`: `18271=121*151`, while
`2r+5` is odd, so `10^(2r+5)+1` is divisible by 11. Therefore both
summands are divisible by 121. This is a **written algebraic derivation**,
not a verified new Lean declaration; it does not exclude a palindrome
(for example, 121 itself is a palindrome). The arithmetic checker separately
evaluates and confirms the closed first-step value for the finite controls.


## Starting-time palindrome obstruction (written proof; Lean source WIP)

The experiment tests positive times 1..3000. For the same four initial
canonical families, **time zero is also nonpalindromic** by a separate
one-column argument. The unchanged initial pair-sum word has
`q(0)=1` for p=1, while a canonical palindrome would have matching
unit/leading digits `d(0)=d(L-1)`, forcing their sum
`q(0)=d(0)+d(L-1)=2*d(0)` even. Contradiction.

The proposed general `r1_to_r4_initial_not_palindrome` Lean declaration has
been added to the uncompiled WIP module and attempts to derive this using
`DecimalDigits.palindrome_value_iff`. The written proof is independent
of the numerical trajectory check. Neither this argument nor the
first-eleven Lean candidates have undergone the required actual Lean
4.19.0 compilation or transitive axiom audit in this session.
