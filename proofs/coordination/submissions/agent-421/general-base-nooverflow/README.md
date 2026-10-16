# Agent #421: general-base no-overflow normalization

Status: LEAN_CHECKED, ready for independent semantic review and rebuild. Not independently reviewed, not integrated, and not a whole-repository build.

## Exact result

For every integer base b >= 7, every positive finite width L, and every symmetric pair-sum word q with 0 <= q(i) <= 2b-2 for i < L, if its complete ordinary carry word has final carry zero, there is a positive canonical base-b digit word d of the SAME width L with the SAME complete first carry word, whose second reverse-add output is a palindrome. Every carry position 0 through L is preserved. Both outputs are canonical, and exact integer reverse-add identities are supplied through the existing digit-evaluation interface.

The representative may differ from the original seed. This does not prove that every representative terminates. The palindrome is at positive time two; an earlier palindrome is allowed and iteration continues after palindromes.

Primary theorem: `Agent421NoOverflow.same_carries_two_step_palindrome`.
All-base endpoint: `Agent421NoOverflow.every_base_ge_seven_nooverflow`.
Source-range specialization: `Agent421NoOverflow.source_bases_nooverflow`.

## Source and proof contract

Source: `proofs/research/resume_general_base_normalization_proof.txt` at original commit `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`, the paragraphs beginning `Set s=1` and `Without overflow`. Inspected main was `9de08d78db6526e2ce2dd66cedd5e63f600424bd`; its generic-base source theorem was listed as written-only. Main's reorganized paths are not assumed identical to the original paths. Dependencies are retrieved from exact original Git objects, not guessed flattened filenames.

The complete source theorem includes overflow and four positive steps for even b>=10 / odd b>=17. That stronger theorem remains PARTIALLY_FORMALIZED here. The b>=7 strengthening applies ONLY to the no-overflow branch. Agent #422 separately owns width-five sharpness and generic numeric digit semantics; this package does not claim that assignment.

Quantifiers: b, L, q are universal; the representative d is existential after all assumptions. Hypotheses are base threshold, L>0, bounded nonnegative symmetric q, and final carry zero. No desired conclusion or witness realizability is assumed. A center-parity condition is proved for the normalized word. Width one is covered.

`DigitBounds`, `PositiveLast`, `eval`, `pairs`, `reversedValue`, and the actual-width normalizer are reused from the pinned repository. `stepDigits_semantics` proves canonicality and exact arithmetic equality. `terminal_word`, `body_word`, and `normalize_nooverflow` bridge the indexed carry view to the existing list implementation. `valid_word_realizable` constructs a positive canonical same-width representative. Thus this is not merely an abstract transition-system implication.

## Verified coverage

44 exported theorems in five proof modules plus one build root. These are supporting declarations and endpoints, not 44 distinct research claims.

Completed scopes: local carry normalization; exact indexed/list correspondence; all-width complete-carry preservation; positive same-width realization; canonical two-step arithmetic palindrome witness; even/odd/all-base specializations; impossibility of universal second-step safety for a complete no-overflow carry class. A kernel-checked base-six example refutes only the local low-output estimate used by this normalizer, not every possible base-six scheme.

Unfinished scopes: protected-run overflow closure, low-bound propagation, terminal schedules, full four-step normalization; exhaustive repository census. No decimal Lychrel existence or all-time seed196 assertion follows.

## Reproduce

Files `manifest.json`, `exports.json`, and `verify.py` specify the complete source-pinned build. Obtain this directory and a Git repository containing original commit `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`, then run:

```sh
python3 verify.py --repo /path/to/p196-algorithm --lean /path/to/lean-4.19.0/bin/lean --out /tmp/agent421-new-clean-check
```

The output directory MUST not already exist. The script verifies Lean 4.19.0 commit 6caaee842e94, reconstructs seven dependencies from exact Git blobs, validates source SHA256, rejects excluded proof shortcuts, builds all 13 modules in an isolated LEAN_PATH, and runs `#print axioms` for all 44 exports. Only `propext`, `Classical.choice`, and `Quot.sound` are allowed. No pre-existing .olean is imported from the research checkout. `verification-summary.json` records the actual successful run, and `axioms.log` preserves its actual transitive audit output.

Pinned proof-source commit: `5bf4830d6d822eab08380937985e16f214ed2678`. All six proof blobs were read back and matched the clean-checked local files. The exact final clean rebuild ran 2026-10-16T04:39:55Z through 04:40:04Z; all 13 modules returned exit 0. This was a self-rebuild, not independent review. `Local.lean` is a retained early checkpoint identical to `Agent421NoOverflowLocal.lean`; do NOT import both. The explicit build root is `Agent421NoOverflow.lean`, not a wildcard import of every checkpoint.

## Integration

Submission is on existing `p196/coordination`, not main. Apply only the designated Agent421 contribution files through the current integration writer after review. Do not merge the entire coordination branch. No permanent remote agent branch, main modification, approval, or merge is claimed. A contribution-path patch and full local logs are retained by Agent #421 for handoff. Check source-map and preservation requirements before integrating into the flattened main layout.
