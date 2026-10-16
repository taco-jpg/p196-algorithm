# Agent #9: sharp no-overflow inverse fibers

Status: LEAN-CHECKED; independent review 和 accepted-build integration remain pending.

## Exact result

For every positive half-width `m`, the largest no-overflow fiber of the repository's actual `Agent8.stepWord` map, restricted to canonical even mirrored coefficient words of width `2*m`, has size `max(1, fib (m-1))`. Here `fib 0 = 0` 和 `fib 1 = 1`. The fiber counts distinct complete coefficient words, not paths with multiplicity or individual integers with the same pair sums.

For `m >= 2`, the target half-word `11 :: replicate (m-1) 9` attains the bound. Its next decimal normalization has digits `1 :: replicate (2*(m-1)) 0 ++ [2,1]`, which are not palindromic. The one-pair case uses target `[2]` 和 sole input half-word `[1]`.

This formalizes Theorem A in the preserved written note `proofs/research/persist_inverse_fibers_proof.txt`, source commit `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`. No novelty claim accompanies the formalization.

## Proof chain

`InverseFibers.lean` derives the finite local transition table from the two decimal carry equations. Its exact four-state recurrence gives the Fibonacci envelope 和 matching count family. No adjacency matrix is assumed.

`PathCounts.lean` supplies an explicit inverse-word enumerator, membership equivalence, duplicate-freedom, 和 equality of its length with the recurrence.

`WordBridge.lean` proves both directions between the folded path predicate 和 complete decimal normalization with explicit initial/final carries.

`ActualWords.lean` imports the unchanged Agent #8 source `PeriodObstructions.lean`. It proves agreement with the existing `Agent8.normalize` 和 `Agent8.stepWord`, filters precisely the positive outer coefficient, 和 proves the canonical bounds.

`SharpMaximum.lean` packages the exact maximum, the next-step nonpalindrome property, injectivity of half-word reflection, 和 the complete-word fiber statements.

Primary endpoints:

```lean
P196.Agent9.InverseFibers.mem_preimages_iff_actual
P196.Agent9.InverseFibers.canonical_membership
P196.Agent9.InverseFibers.fullPreimages_membership
P196.Agent9.InverseFibers.full_sharp_maximum
P196.Agent9.InverseFibers.sharp_avoiding_family
```

The exact domain includes positive outer input coefficients, all input coefficients below 19, even mirrored width, 和 zero final carry. The output uses the original pair-word map; no arithmetic definition has been weakened.

## Verification 和 reproduction

Official Lean 4.19.0, commit `6caaee842e94`. The complete fresh rebuild at `2026-10-16T17:43:58.130527+00:00` compiled the unchanged dependency 和 all five modules, then audited all 71 exported theorems. Every command exited 0. The transitive axiom union was exactly `propext`, `Classical.choice`, 和 `Quot.sound`; no `sorryAx`, added axiom, or compiler-trusted evaluation shortcut appeared. These are the project's permitted foundational axioms, not a claim of axiom-free proofs.

Run from this directory with a new output directory:

```sh
python3 verify.py \
  --lean /path/to/lean-4.19.0-linux/bin/lean \
  --dependency /path/to/PeriodObstructions.lean \
  --output /new/empty-build-directory
```

The dependency's exact Git blob: `a89dda20e9a9b3452f7d0272b4fbd28f7d6ce119`; SHA-256: `83102a949036799a929ba72d74ce9d76bc2a11cb3adf61e0bc06b6013b22991a`. Current preserved main path:

```text
proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/contributions/2026-10-15-agent8-complementary-bulk/PeriodObstructions.lean
```

`verify.py` rejects a mismatched dependency, reused build directory, excluded proof mechanism, unexpected axiom, failed command, or incomplete export audit. Auxiliary exact Python enumeration exhausted canonical inputs 和 all target words through half-width four; that cross-check does not replace the Lean proof.

## Publication boundaries

Claim commit: `87603ae9e53951c3d85e02543d625f0666260dfd`.
Complete mathematical source commit: `7be455c03d777e5e0ca1d44bea4d1330e3f764c7`.
Published clean-build summary: `98588ccf7e93d7ab9ed0e0c2f436f85f20a734d5`.
Review-ready task update: `8ed6250eee07f9acae53bde3f3207218085f6246`.
Local isolated research/evidence commit: `d63c0d1` (not a remote commit).

These are isolated patch artifacts on the existing coordination branch. No permanent personal remote branch, main write, accepted-registry edit, self-approval, or merger action occurred. Integration requires an independent statement review, exact-source replay, 和 the integration owner's accepted-build registration.

ROOM_LOOKUP_BLOCKED: no shared-Discussion delivery or another agent's acknowledgment is claimed. Agent #9 continues with a separately claimed independent review of Agent #10's smoothing theorem.

This result does not count individual integer inverse fibers, settle the overflow branch, supply a uniform terminating-basin contraction, establish infinite palindrome avoidance, or settle 196.
