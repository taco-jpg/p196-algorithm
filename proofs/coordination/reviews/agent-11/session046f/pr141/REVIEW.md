# PR141 independent source and retained-evidence review

**PASS for source/evidence acceptance at `c440e01ee4375384317cc2e428b7c43e8a04ecdf`. No blocking finding or mathematical repair identified.**

Reviewer: Agent 11 session `046f9285a650`, delegated specialist `/root/review141`. This reviewer authored none of the submitted mathematics, changed no submitted source, and performed no remote mutation. `AGENTS.md` and `proofs/PUBLICATION_POLICY.md` were read at the reviewed head. Integration, dependency ordering, final head/base checks, retargeting and the sole write slot remain the parent integrator's responsibility.

PR: https://github.com/taco-jpg/p196-algorithm/pull/141

| Identity | Exact value |
|---|---|
| Reviewed PR head | `c440e01ee4375384317cc2e428b7c43e8a04ecdf` |
| Reviewed stacked PR139 base | `5d3b027df045eb017a8e37d3826b10105a587e9b` |
| Original mathematical source commit | `6145e2aa53861bdf6c7a820dd8ee78da9abc014f` |
| New contribution | 181 added files; no modification or deletion relative to the stacked base |
| Actual import closure | 26 project modules: 23 unchanged inherited modules and 3 new modules |
| Fresh Lean execution by this reviewer | **NOT_RUN** |
| New Python checks | 684 checks passed; separate baseline/driver reconstruction passed; both commands exited 0 |

The runtime limitation was supplied by the parent: normal Lean launch was unavailable and escalation had already been rejected. I did not retry, bypass that restriction, or claim a fresh Lean run. The accepted proof execution below is an explicitly attributed, independently produced, exact-source historical execution whose raw evidence I checked anew.

## Exact theorem and semantic review

The new endpoint is the original source statement:

```lean
theorem zeroStateOrbit_escape (s : ZeroState)
    (hv : ValidPeriodic s.1 s.2 [0,0,0,0]) (M : Nat) :
    ∃ t, t ≤ DecimalQuantitativeMass.escapeBound
        (periodicWord s.1 s.2 [0,0,0,0] (M+3)).length (9*M) ∧
      M < 2*(zeroStateOrbit s t).1.length+(zeroStateOrbit s t).2.length
```

It is in namespace `Agent1.Periodic`. The theorem supplies a finite time at which the original zero-period quotient interface exceeds an arbitrary natural cap. Its hypotheses contain only the original validity record and the cap. There is no safety assumption, initial-cap assumption, positive-cap assumption, cycle premise, or claim about 196.

I inspected all three new mathematical modules and the relevant original definitions and bridge statements throughout their unchanged import closure. `ZeroState` is `Word × Word`; `zeroNext` applies the existing maximal `quotientOuter` and `quotientCenter` with literal period `[0,0,0,0]`; `zeroStateOrbit` iterates this map. The existing `ValidPeriodic` preserves coefficient bounds 18, period length four, center symmetry and odd-middle parity, and positive exterior. The ordinary numeric `Lychrel196.orbit` repeatedly applies `n + reverse10 n` without an imposed palindrome stopping rule.

The proof's critical obligations check out:

1. **Finite cap only.** Negating the conclusion produces `hbound` only through `N = escapeBound L (9*M)`. `zeroExponent_guarded_prefix` directly inducts over `t ≤ N`; it never imports an all-time cap into this argument. At a successor it establishes the previous exponent guard before applying `zero_width_step`, and uses the cap only at the next state, still within `N`.
2. **Endpoint and guard arithmetic.** The literal start is `M+3`. The invariant is `M+24 ≤ interfaceWidth(t)+8*zeroExponent s (M+3) t`; the next cap forces the next exponent to be at least three. The inherited recursion remains `(k-2)+outerPeriods+centerPeriods` with natural subtraction. The inherited signed balance is used only after the current guard is known; negative individual exponent increments have not been assumed away. `zeroLiftWord_step_prefix` requires `t<N`, while numeric transport reaches `t≤N`. At `N=0` no transition is needed.
3. **One fixed positive seed.** `periodicWord_realizable` is invoked once, at the initial lifted word of exponent `M+3`. It provides a positive ordinary integer with canonical width and every in-range column sum. `zeroLiftWord_actual_prefix` transports that same `n` through `Lychrel196.orbit n t`. Successor digit functions may differ, but the integer seed does not. The explicit positivity component is discarded syntactically by the endpoint; the retained `Canonical` witness still contains positive length, decimal digit bounds, nonzero leading digit, and exact value, which are precisely the original escape theorem's hypotheses.
4. **Exact mass factor.** Summing the original coefficient bound gives `2*B.sum+H.sum ≤ 18*(2*B.length+H.length)`. The unchanged `zero_period_digitSum` gives `2*digitSum n = 2*B.sum+H.sum`. Together with interface width at most `M`, these imply `digitSum n ≤ 9*M`. There is no rounding step or missing factor two. The mass lemma itself has no exponent guard and includes exponent zero whenever its other hypotheses hold.
5. **Exact initial width and horizon.** Here `L = (periodicWord s.1 s.2 [0,0,0,0] (M+3)).length = 2*s.1.length+s.2.length+8*(M+3)`. Both realization and the original arithmetic escape theorem use this same full initial width. The inherited definitions are `gapBound L B = max L (2*B+2)`, `widthBound L B = (2*B+1)*(gapBound L B+1)`, and `escapeBound L B = 4*(widthBound L B-L)+5`, retaining natural subtraction. The returned `t≤N` is exactly where prefix transport, validity and the factor-nine bound contradict the strict digit-sum escape.
6. **Boundary cases.** No assumption excludes `M=0` or an initially oversized interface. An oversized initial interface already admits `t=0`, with `0≤escapeBound L (9*M)`. Original zero-period validity forces a nonempty positive exterior, so `M=0` also escapes immediately. Empty centers remain allowed. The contradiction proof handles these cases without an extra premise.

The closure deliberately excludes `Agent1PeriodicZeroCycle`: the finite horizon is obtained from the original quantitative arithmetic theorem, not inferred from qualitative no-cycle or unboundedness. The result supplies an escape witness, not eventual monotonic growth, persistent escape, a palindrome hit, termination, an infinite safe orbit, or a nonzero-period classification.

## Reused execution and complete shortcut audit

The original strict execution is attributed to **Agent #1 specialist `/root/research_status`**, a separate nonauthor specialist in the original session/account. I reviewed the exact retained replay driver, raw commands and logs, audit source and manifests. Its build and evidence directories were created fresh, only source files were copied, and every project module was compiled in import order before the audit. Author increments and the parent canonical verifier remain distinct executions; neither is relabeled as this reviewer's fresh execution.

The retained compiler record is Lean 4.19.0, commit `6caaee842e94`, binary SHA-256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. I checked all **27 recorded commands**: 26 module compilations and `ReviewAudit`, all with `--trust=0 -j1 -DElab.async=false`, exit 0, and exact matching log hashes. Summed recorded command time is 73.484828654 seconds. This checks retained execution evidence; it does not independently rerun the compiler or attest a local compiler binary.

All 26 canonical source files match their Git blob and SHA-256 pins, the original mathematical commit, the independent `compiled-sources` snapshots and the parent source snapshots byte-for-byte. Traversing actual imports yields precisely the registry closure. All 23 inherited modules also match the stacked base. The archived replay-driver copies are identical; independently reconstructing its generated audit from the driver and pinned sources reproduces `ReviewAudit.lean` exactly.

I reparsed the raw multiline audit, retaining complete identifiers including Lean quotation syntax:

| Audit item | Independently recovered result |
|---|---|
| Module-origin theorem constants | 1,462 unique entries; all 26 module origins present |
| Theorem axiom union | Exactly `propext`, `Classical.choice`, `Quot.sound` |
| Safe definitions/opaques | 241 unique entries; axiom union exactly `propext` |
| Public named theorem types | 111 requested and printed in exact source order; all also have accepted raw axiom prints and full-audit entries |
| New public theorems | 6, two per new module |
| New theorem constants including helpers | 20: Prefix 7, InterfaceMass 6, Escape 7 |
| Nonsafe generated definitions | 976: 945 `_cstage1`/`_cstage2` helpers and 31 `_unsafe_rec` helpers |
| Unsafe-rec safe bases | All 31 present in the safe-definition audit |
| Unsafe implementation axioms | 14: 13 inherited from `LychrelDigitSums`, one inherited `ZeroState` list-sum specialization |
| Unsafe opaques | 0 |

No unsafe implementation axiom appears in any audited theorem or safe-definition axiom dependency. No such implementation entries originate in the three new modules. These generated implementation records are kept separate from accepted logical dependencies, rather than silently ignored or misreported as zero.

A nested-comment-aware source scan across all 26 modules found no active `sorry`, `admit`, `sorryAx`, custom `axiom`, `native_decide`, `Lean.ofReduceBool`, `Lean.ofReduceNat`, `unsafe`, `extern`, `implemented_by`, `partial`, or elaborator-command shortcut. The retained full audit traverses module-origin theorem and safe-definition dependencies and rejects any axiom outside the standard three, including unsupported custom axioms and computation-oracle axioms. All raw audit records parsed; their reported totals agree with the independently counted records. The 111 elaborated named types are retained in `audit-001/named-types.txt`.

Every review manifest entry, final review receipt hash, prefix-author evidence hash, parent package manifest entry and original parent manifest entry checked successfully. No source/log mismatch or unrecorded repair was found. Historical scope notes remain proposals; author increment receipts explicitly disclose reused dependencies.

## New review evidence and recovery

`audit_retained.py` and `check_baseline.py` are the only new audit programs. Their actual commands, exits and output hashes are in `execution-receipts.json`; full outputs are retained in `audit-001.log` and `baseline-001.log`. Neither invokes Lean. Both first attempts passed, with no failed new audit attempt, source edit, compilation attempt, or experimental result to omit.

The compact publication package contains this report, all new audit source and results, raw named types, execution logs/receipts and a byte manifest. `audit-001/source-recovery-map.json` maps every inspected retained source/evidence input to its exact Git commit, path, blob, byte count and SHA-256, with a lossless recovery instruction. Already preserved Git files are not copied into this new package; compiled objects and duplicate local source snapshots are reproducible infrastructure. No new substantive research output is discarded by that deduplication.

This is an independent source interpretation and exact retained-evidence acceptance review. It is not a claim of outside peer review, a new formal execution in this environment, a repository-wide complete catalogue, or an integration decision. The parent must still complete prerequisite integration and its final remote identity/write-slot gates before merging.
