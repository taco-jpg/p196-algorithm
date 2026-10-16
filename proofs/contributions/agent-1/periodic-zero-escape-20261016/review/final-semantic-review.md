# Independent review: quantitative zero-period interface escape

**PASS at mathematical source `6145e2aa53861bdf6c7a820dd8ee78da9abc014f`.** Reviewer: Agent #1 specialist `/root/research_status`, a separate specialist in the same session and GitHub account, with no mathematical source authorship in this package. I inspected the exact source and independently executed the complete fresh closure. Author and parent runs are separate executions, not evidence of my own run. This is not an outside approval or an integration decision.

## Exact result

The public endpoint retains the original valid zero-period state and quantifies every natural cap:

```lean
theorem Agent1.Periodic.zeroStateOrbit_escape (s : ZeroState)
    (hv : ValidPeriodic s.1 s.2 [0,0,0,0]) (M : Nat) :
    ∃ t, t ≤ DecimalQuantitativeMass.escapeBound
        (periodicWord s.1 s.2 [0,0,0,0] (M+3)).length (9*M) ∧
      M < 2*(zeroStateOrbit s t).1.length+(zeroStateOrbit s t).2.length
```

`zeroStateOrbit` remains the exact executable maximal quotient on exterior and center, with literal period four zeros. `ValidPeriodic` is unchanged. There is no initial cap assumption, no requirement `M>0`, and no safety premise. If the initial interface already exceeds the cap, time zero is allowed. The conclusion gives a finite bound for exceeding an interface cap; it does not assert a palindrome hit, termination, nonzero-period behavior, or any result about 196.

The horizon uses the original `DecimalQuantitativeMass.escapeBound`, not a new numeric growth theorem. In the original source:

```lean
gapBound L B = max L (2*B+2)
widthBound L B = (2*B+1)*(gapBound L B+1)
escapeBound L B = 4*(widthBound L B-L)+5
```

Natural subtraction is retained exactly. Here `L` is the full initial coefficient-word length at exponent `M+3`, and the original positive canonical realization proves that it is also the actual initial ordinary decimal width.

## Semantic checks

1. **Finite prefix only.** `zeroExponent_guarded_prefix` assumes the interface cap through `N`, and concludes the guard and total-width lower bound only for `t≤N`. It does not call the earlier theorem requiring an all-time cap. In the successor proof, the current guard is established before using `zero_width_step`; the next cap is obtained only at `t+1≤N`.
2. **Endpoint arithmetic.** `zeroLiftWord_step_prefix` uses `t<N`; `zeroLiftWord_actual_prefix` reaches every `t≤N` using only transitions strictly before that endpoint. There is no omitted final step or assumption beyond `N`. The statements also make sense at `N=0`, where no transition is required.
3. **Literal exponent recursion.** The proof retains `(k-2)+u+v` and the original `M+3` start. The width invariant supplies the current threshold before natural subtraction is identified with the signed width balance. Individual negative shifts are allowed; they are not truncated away or assumed nonnegative.
4. **One fixed seed for the chosen cap.** The canonical seed is chosen once for the initial lifted word. Prefix induction transports the same original `Lychrel196.orbit n t`, exact canonical width and all in-range pair sums. A new digit representation may witness each successor, but the integer seed does not change within the prefix. Different caps may use different initial seeds, which the quotient-state theorem permits.
5. **Same initial width in the bound.** The realization and `digitSum_escape_of_canonical` use exactly `(periodicWord s.1 s.2 [0,0,0,0] (M+3)).length`. The horizon does not substitute a later width, a padded numeral, or the interface width alone. The original Canonical predicate ensures a positive leading digit. The positive seed returned by the realizer is not weakened to an arbitrary list evaluation.
6. **Factor nine.** `zero_interface_mass_le` derives `2*sum B+sum H ≤ 18*(2*|B|+|H|)` from the unchanged coefficient bounds. `zero_period_digitSum_le_width` combines that with the existing exact identity `2*digitSum n = 2*sum B+sum H`, obtaining `digitSum n ≤ 9*M`. No division rounding or missing factor two is hidden.
7. **Quantifiers and boundary cases.** Negating the final existential supplies the cap only through the exact chosen horizon. The original quantitative digit-sum theorem then provides a time within that same horizon, where prefix representation and the factor-nine bound contradict it. `M=0` and an initially oversized interface require no extra hypotheses. General empty centers remain allowed; original validity excludes empty or zero-headed exterior in the zero-period branch.
8. **Reuse and scope.** The proof calls original `DecimalQuantitativeMass.digitSum_escape_of_canonical` unchanged. Its finite escape statement does not require safety or stopping at a palindrome. The minimal dependency closure deliberately excludes `Agent1PeriodicZeroCycle`; this finite theorem does not infer a numerical bound from qualitative no-cycle or all-time unboundedness alone. The historical finite-interface/lift and other agents' generic mass-growth work are not reimplemented.

No unresolved semantic flaw was found in the frozen source.

## Independent execution

Fresh build directory: `/workspace/p196-agent1-session-20261016/periodic-zero-escape-review-clean-001`.

Official Lean 4.19.0 commit `6caaee842e94`, binary SHA256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. Every module and audit command used `--trust=0 -j1 -DElab.async=false`. Actual imports were independently traversed: precisely 26 modules, comprising the previous 24-module closure minus unused ZeroCycle, plus the three new modules.

* **26 modules plus one complete audit passed:** 27 successful commands, 73.48 seconds summed command time, first attempt. No existing object was copied or reused.
* **1,462 module-origin theorem constants** were audited, including private/generated theorem constants. The axiom union is exactly `propext`, `Classical.choice`, `Quot.sound`.
* **241 safe definitions/opaques** were audited, with axiom union only `propext`. No custom safe axiom or forbidden dependency was accepted.
* **111 public theorem types and axiom prints** were checked: six new exports, two in each new module, plus 105 prior exports. The new modules contain 20 theorem constants in total: Prefix 7, InterfaceMass 6, Escape 7.
* Generated implementation inventory remains separate: 976 nonsafe definitions, comprising 945 cstage and 31 `_unsafe_rec` helpers, with every unsafe-rec helper's safe base checked. There are zero unsafe opaques and14 unsafe implementation axioms: 13 from the original LychrelDigitSums and the already-inventoried ZeroState `List.sum` specialization. None appears in audited theorem/safe-definition dependencies. The three new modules introduce no such implementation entries.

The run archives all 26 actual source inputs and the exact executed replay driver during execution. Before compilation and after completion, source hashes matched the published mathematical commit; the build inputs, archived snapshots and checkout agree byte-for-byte. The source worktree's untracked author object was recorded and excluded. There was no source drift, failed compilation, failed audit, or repair to this independent run. No finite diagnostic or enumeration is substituted for the proof.

Full logs, commands, compiler identity, generated audit source, source snapshots and verification are under `clean-001/`. Verification SHA256: `8618b7116ce84c03381e839ca6c07d549334f4f8cd6c0e5e1b6afa8843c36404`.

## Frozen identities

Registry `proofs/Agent1PeriodicZeroEscape.registry.json` SHA256: `54cc0e278ae40252b15523e397f3446bfa2a9c1b37a16c053d9e4ff81473e728`. Every source path, blob, hash and actual import is recorded in `final-source-identity.json`; `clean-001/publication-source-receipt.json` checks all 26 against the published commit and both sets of compiled-source copies.

| New module | SHA256 |
|---|---|
| Agent1PeriodicZeroPrefix | `c922e0268511b93865a2a047d8c59599ebaf3463d713f6ff90351230f4eda5cb` |
| Agent1PeriodicZeroInterfaceMass | `a8da314abda733d33e3b29e3f205e6db5d3e88fc635f78a6f9740997b30aa529` |
| Agent1PeriodicZeroEscape | `e1c9b9f90b5b2fddf3a4642b29030b1db7ab507d155a092facc713de5aaf0969` |

Executed driver SHA256: `6c6d2d4b6b1460251ff0722d7b98f30aaa7b547a90f276f6d411e2b6359fbcf3`; the archived and review-directory copies are identical. The frozen result is ready for a formal COMMENT review after an actual PR and final evidence head are supplied. No PR review or integration is claimed by this report.
