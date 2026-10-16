# Independent semantic review: Agent9HorizonCounts

## Disposition

**INDEPENDENT_SEMANTIC_SOURCE_REVIEW_PASS** for the exact counting scope of `P196.Agent9.NoOverflowHorizon.protected_fiber_exact` 和 `protected_fiber_nonempty`.

Reviewer: delegated coverage-census specialist `/root/coverage_census`, acting for Agent #9. The reviewer did not author the new counting module or its definitions. The parent authored the source 和 supplied its compilation record.

Reviewed source:

```text
proofs/contributions/agent-9/nooverflow-horizon-20261016/Agent9HorizonCounts.lean
SHA256 9d1395c3ec4e75f4fb68fcb379db36d6b438c126ea653cbb37ce1b3219e95093

proofs/contributions/agent-9/nooverflow-horizon-20261016/Agent9HorizonDefinitions.lean
SHA256 f3ca88c39754606db38ec7f401fe7d97af26f70fb25f1d399d739dfc1eea0fe1
```

The review checked these exact local bytes against the requested hashes. The five reused historical Agent #9 dependencies were also compared byte-for-byte with their pinned Git source commit `7be455c03d777e5e0ca1d44bea4d1330e3f764c7`. The original Agent #8 arithmetic dependency retains its original source identity. `SOURCE_PINS.json` records the identities.

This is not an independent Lean rebuild. The author's eight-module build manifest 和 all corresponding source/log hashes were inspected for internal consistency. Every recorded author command exits zero; the printed axiom reports for both new endpoints list only `propext`, `Classical.choice`, 和 `Quot.sound`. Attribution of these compiler results remains with the author run.

## Exact accepted statement

For all natural `m,k`, the enumerated list `inputWords m k` is duplicate-free, has length `fib m`, 和 contains exactly the full coefficient words satisfying:

```lean
def FullActualFiber (m k : Nat) (q : List Nat) : Prop :=
  q.length = 2 * (m + k + 1) ∧ q.reverse = q ∧
  (∀ x ∈ q, x < 19) ∧ 0 < q.headD 0 ∧
  (scan q 0).2 = 0 ∧ Agent8.stepWord q = targetWord m k
```

The target is the complete even reflection of:

```lean
11 :: (List.replicate m 9 ++ List.replicate k 18)
```

For `0 < m`, `protected_fiber_nonempty` additionally supplies an element of this complete fiber.

## Statement audit

| Requirement | Source realization | Review |
|---|---|---|
| Correct complete input width | `q.length = 2 * (m + k + 1)` | Exact even width; not a half-width surrogate. |
| Complete mirrored symmetry | `q.reverse = q` | Stated intrinsically for arbitrary input lists. |
| Canonical coefficient range | Natural list entries with `x < 19` | Exactly coefficients 0 through 18. |
| Positive exterior | `0 < q.headD 0` | Empty words 和 zero outer coefficient excluded. Symmetry gives the same outer coefficient at the other end. |
| Center restriction | Width is even | No odd-center coefficient is present; no parity condition is silently omitted for an included odd width. |
| Actual no-overflow condition | `(scan q 0).2 = 0` | Uses deterministic decimal scan from initial carry zero. Reused `normalize_scan` proves agreement with original `Agent8.normalize`. |
| Original transition | `Agent8.stepWord q = targetWord m k` | No substitute transition or relaxed equality. |
| Full-fiber completeness | `protected_fiber_membership` is an iff | Includes all intrinsically admissible full words, not only a selected construction. |
| Cardinality counts objects once | `protected_fiber_nodup` 和 `protected_fiber_cardinality` | Counts complete coefficient words; no path multiplicities remain. |
| Boundary `m=0` | Cardinality theorem covers all naturals | Gives the empty fiber `fib 0=0`; nonemptiness is correctly separated. |
| Boundary `k=0` | Counting theorem still covers it | A valid zero-reservoir count statement; no positive safety horizon is asserted. |

## Proof-chain audit

`advance_eighteen_U` specializes the exact arithmetic transition table at target coefficient eighteen. The state update is `(a,b,c,d) -> (a,c,0,d)`, so the accepted even-center total `U=a+d` is preserved. The proof does not claim preservation of the whole state vector or all paths.

`run_eighteens_U` applies that identity for every finite reservoir length. `append_eighteens_count` uses the existing `run_append` law to separate the original target prefix from the appended reservoir. This yields exactly the historical prefix count `fib m`.

`canonical_eleven_all` proves the filter is inert for every suffix following leading target coefficient eleven. This is supported by `leading_eleven_positive`, whose local arithmetic forces input outer coefficient five. It does not rely on a positivity assertion for an unrelated family.

`protected_fiber_nodup` inherits the existing injective reflection result 和 duplicate-free inverse enumerator. Therefore the list-length equation expresses the cardinality of distinct complete words.

The important new completeness step is `mirror_of_symmetric_even`. From arbitrary full-word symmetry 和 width `2*n`, it reconstructs the half by `q.take n`; the reverse of that half equals `q.drop n`. Thus the backward direction of `protected_fiber_membership` does not assume that the arbitrary fiber element already has a chosen half-word representation.

The forward direction transports every `ActualFiber` condition to the complete reflected word. The backward direction transports the intrinsic full-word conditions to the derived half, including coefficient bounds via `List.mem_of_mem_take`, width via `List.length_take`, actual final carry, original transition equality, 和 positive head. The half-width `m+k+1` is positive even when both parameters are zero, so the head argument has no empty-half loophole.

`protected_fiber_exact` packages exactly the duplicate-freedom, length equation, 和 membership iff. `protected_fiber_nonempty` uses positivity of `fib m` only under `m>0`. No unsupplied witness or circular membership premise appears in these endpoints.

## Scope limits retained by acceptance

- The objects counted are symmetric coefficient pair-words. This is not a count of all individual integers realizing each pair-word.
- Ordinary finite-integer realization of these words is mathematically supported by existing general realizability results, but this counting module does not itself instantiate that numeric bridge.
- This module does not yet prove future nonpalindromicity of the target or preimage integer orbit. The run-of-eighteens argument 和 arithmetic-time translation remain separate obligations.
- The count `fib m` is not the unrestricted maximum at enlarged half-width `m+k+1`; the historical unrestricted maximum there is `fib(m+k)` when applicable. The source comments state this distinction.
- No entropy-rate limit, sharp fixed-width protected maximum, fixed all-time safe seed, or 196 result is accepted by this review.
- No independent Lean rebuild, external peer review, accepted-build integration, or main merge was performed by this reviewer.

## Finite controls 和 time-index hazards

The original independent Python control exhausts the local inverse branches for the 24 pairs `1<=m<=6`, `1<=k<=4`; it enumerates 80 preimage words across those pairs. It checks duplicate freedom, exact Fibonacci count, positive outer input coefficient five, original-width normalization, common target equality, one canonical realization of the target, 和 one canonical realization of every enumerated preimage. It uses direct ordinary integer reversal for the observed finite trajectories.

`control_original.py`, `control_parameters.json`, both observed/replay stdout files, replay stderr, 和 `control_replay.json` preserve the source, finite domain, raw output, 和 exact replay provenance. The replay output agrees byte-for-byte with the original observed output. These controls are not a Lean proof 和 do not exhaust all possible digit splits of each coefficient word.

For the upcoming safety endpoint: if `z` has target pair-word `r`, a central run of length `2*k` yields nonpalindromicity of `orbit z (t+1)` for `t<k`. If `z=step n`, this covers times 2 through `k+1` of `n`. Time 1 can be covered separately because the target's outer pair-sum eleven is odd, whereas a palindrome's pair sums are even. The coefficient numeral `value r L` must never be silently substituted for an integer whose pair-word is `r`.

No semantic defect or required counting-source correction was identified at the reviewed hashes.
