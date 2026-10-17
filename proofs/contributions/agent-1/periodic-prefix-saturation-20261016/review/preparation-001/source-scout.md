# After ReturnCore/ReturnClock: the missing three-column quotient projection

Source-only strategy scout by Agent #1 specialist
`/root/research_status/cap4_existing_theorems`. No new graph search, arithmetic
experiment, Lean execution, proof/source edit, claim, or external message.
Read current sources in `/workspace/p196-agent1-return-20261016` and
`/workspace/p196-agent1-clock-20261016`. This report is the only output.

## Concrete payoff and limits

The useful next obligation is an **actual three-column prefix projection of
the maximal period-four quotient**, followed by reuse of the existing checked
saturated eight-cycle classification. It is not a new saturation theorem.

Let `C = quotientClockSum B H w N` and let ReturnClock supply the positive
natural gain `G`, so `C = 8*G` and `16*G ≤ N ≤ 32*G`. If `N = 16`, then
`G = 1`, `C = 8`, and `2*C = N`. More generally the lower-bound equality
`N = 16*G` is exactly upper-growth saturation `2*C = N`.

For every saturated positive full-tuple return, the proposed adapter would
force its first three physical coefficients through the already classified
eight states, up to cyclic offset:

```
(8,12,9), (17,5,0), (8,13,5), (17,6,11),
(8,14,8), (17,8,17), (8,16,16), (17,13,14).
```

Consequently every physical outside coefficient on such a return is **8 or
17**. ReturnCore already proves that a positive full-tuple return starting at
`w 0 = [14,14,4,4]` has initial outside **9 or 10**. The two restrictions are
incompatible. The concrete new corollary would therefore be

```
w 0 = [14,14,4,4]  ⇒  2*C < N  ⇒  16*G < N,
```

under the existing exact path, initial validity, positive length, and complete
return hypotheses. In particular `17 ≤ N`; no `N=16` return is possible from
that original phase. This is a proposed source-supported consequence, not a
newly checked theorem. It does not exclude every larger return or improve the
bound for every other nonconstant initial phase.

For arbitrary saturated period-four returns, merely adding `8 ∣ N` would add
**no information**: `N=16*G` already implies it. The exact prefix profile is
the useful stronger endpoint. It classifies the three outside columns, not
the entire period-word trajectory or every finite exterior/center.

## Exact missing bridge; no numerical orbit lift

Define the physical prefix from `Agent8.firstThree (B ++ w)` and convert the
triple `(a,b,c)` to the existing `P196.Agent4.Saturation.Prefix` structure.
Length four ensures this reads three actual coefficients even when `B=[]`.
Use the actual bit `Agent8.inputThree (periodicWord B H w 3)`; **this is not**
the `lastInput` bit entering only the final column in ReturnClock.

The required local contract, in the original `advance` relation, is:

```
ValidPeriodic B H w →
  let p := physicalPrefix B w
  let e := Agent8.inputThree (periodicWord B H w 3)
  P196.Agent4.Saturation.Valid p ∧ e ≤ 1 ∧
  advance p e =
    (physicalPrefix (quotientOuter B H w) (rawPeriod B H w), rawGamma B H w).
```

Existing interfaces discharge all actual arithmetic:

- `Agent8.prefix_step_of_canonical`,
  `proofs/PrefixSemantics__3798a605dd95d8c6.lean:115`, gives the exact first
  three output coefficients, the bound on `inputThree`, and
  `prefixOverflow (firstThree Q) (inputThree Q) =
  overflow (Q.headD 0) (lastInput Q)` for canonical `Q` of length at least six.
  `firstThree_valid` (line 156) supplies its positive/bounded prefix.
  `terminalCarry_eq_actual_overflow` (line 107) identifies the actual clock.
- `periodicWord_canonical` supplies the original canonical pair-word at
  exponent three, with length at least 24. `valid_quotient_transition` in
  `Agent1PeriodicValidity.lean:56` gives the exact output at
  `k' = 1 + outerPeriods + centerPeriods ≥ 1` and full successor validity.
- The small missing list lemma is
  `firstThree (periodicWord B H w k) = firstThree (B ++ w)` for `k ≥ 1` and
  `w.length = 4`. Apply it to the input at three and to the exact output at
  `k'`. It avoids a new stripping-prefix theorem or a whole guarded path lift.
- `Agent8.prefixNext`/`prefixOverflow` and
  `P196.Agent4.Saturation.advance` have the same displayed digit/carry formulas.
  Only the triple-to-structure adapter needs checking; do not duplicate the
  arithmetic proof. Existing `Agent8.prefix_next_compat` and
  `prefix_overflow_compat` in `SaturationPaths` target the separate Agent8
  triple model, not directly the Agent4 `Prefix` structure.

Along a `QuotientPath`, reuse new ReturnClock's `quotient_path_valid`, apply
that local contract, and identify the recursive natural `Saturation.total`
of output carries with `quotientClockSum`. Full tuple return closes the
physical prefix. Then apply **existing**
`Agent2.SaturatedProfile.saturated_overflow_profile` at
`proofs/Agent2SaturatedProfile.lean:212`, or `saturatedEightCycleTarget`
(line 154) if the four forced incoming controls are also wanted.

The abstract-path version is the right reuse interface. The same file's
`actualSaturatedEightCycleTarget` and `numeric_saturated_prefix_profile`
already supply ordinary-orbit specializations, but invoking those would
unnecessarily require a guarded multi-step quotient lift. The local exponent
three projection suffices even when consecutive `Q_3` words are not an orbit.

## What the existing witnesses actually say

The original periodic `METHOD_AND_PROOF.md` sections 3–4 explicitly retain an
eight-edge phase/outside loop with clock `10101010`, starting at
`((0,9,18,9),17)`, and traversing it twice closes the width residue in 16
steps with eight overflows. The report already compares it with the prior
outer-three critical cycle and records four compatible cyclic alignments.
Thus the new prefix adapter would **not reject this saved witness** merely
by repeating its already satisfied prefix classification. No finite exterior
or center was supplied there, and this scout supplies none.

The eleven saved probes also start at `B=[17], w=[0,9,18,9]`, with empty or
single even centers. They are different initial tuples from the
`[14,14,4,4]` phase corollary. All hit the 128-step path cap; every recorded
bulk became nine at time 21 and zero by time 26. Their preserved status is
UNKNOWN, with no full tuple cycle found. These finite observations do not
justify an all-time safe continuation or a claimed finite interface lift.

One-column upper-potential tightness alone is insufficient for the desired
classification: the literal head transitions `9 --0--> 18 --1--> 9` satisfy
both tight equalities in Agent8's upper bound, whereas neither head belongs
to the three-column critical cycle. The existing three-column saturation
certificate is precisely the additional necessary consistency restriction.
No new finite search is needed to obtain it.

After this adapter, genuinely new exclusions of the saved compatible witness
would need stronger actual inner-carry/interface consistency. Do not assume
an odd-input balance law: original
`Agent215.Saturated8.skeleton_block_always_saturated` and
`saturated_block_target_false` already show that all four odd controls may
be arbitrary bits; saturation does not force their sum to two. Independent
block choices likewise do not establish realizable continuation.

## Reuse identities, status and ownership boundaries

| Source / endpoint | Exact identity |
| --- | --- |
| `Agent2SaturatedProfile.lean`, exact profile endpoints | blob `9230b3f3a83ff8f0357a091cfc73c745015cb020`; SHA `89bd18b28673dc2f0d2b17f57773864cd998f73030879f24e15e221b1d648079` |
| Original `Saturated8CycleProfile.lean`, `cycleState`, corrected control semantics | blob `86a45a6a09d9afd8d9dfafbcdd29b2f900be54a2`; SHA `cce58055f9175005c215f2bccaf5d1c937de2c1deefdc2033b4d42587b26e9f7` |
| `PrefixSemantics__3798a605dd95d8c6.lean` | blob `04a8cc9e73b87d271ca857a218b240e23f57c939`; SHA `5dca5a84536801f771020660d496063426c5946a4e1912ec2a17f0ae246b23b5` |
| `PrefixModel__412f2902c90e9ba0.lean`, original `advance` | blob `28eaab767b15fd81f73f2dcfc3dfff307eb02307` |
| `SaturationTheorem__3e87d543382b99c0.lean`, prefix certificate | blob `f4f8f7da5f2e87f3f0d99503e8f76e6aee4b5f6f` |
| `Agent1PeriodicReturnCore.lean:97`, `quotient_return_initial_outside` | inspected SHA `271fbd1e8c5487e515420ccd145391c039f8dccab3b8f134cf31ff9b8dd7255f` |
| `Agent1PeriodicReturnClock.lean`, validity and gain endpoints | inspected SHA `ef4b8ae6380db3b2286ed166e26fe432626eb36a812c8de5c72d54d0c6bb309e` |
| Original periodic `METHOD_AND_PROOF.md` | blob `5c5f94c66d6c3adb0288b610f748fcbed32b115c` |

Use `Agent2SaturatedProfile.registry.json` for its exact imported module
identities: several historical sources share logical names such as
`SaturationCertificate`. Do not select a different same-named source by
filename similarity. Combining the existing closures should retain the
original definitions and proofs byte-for-byte.

Agent110's `CertificateSaturation.saturated_period_constraints` gives period
divisible by 72 only with original scalar `Certificate/Valid`, positive
exterior, **SixPhase**, and saturation. Its scalar mod-nine/six-phase charge
premises are absent here. It cannot strengthen arbitrary nonconstant
period-four returns to period 72. Reuse the generic Agent4/Agent2 prefix
theorem instead.

Coordination snapshot actually read: `38f79914241eb6a379b29ca13a19b95393fdc1c5`.
The Agent1 saturated-profile independent-review task is RELEASED with an
independent 17-module clean build, 1779-theorem audit, all 14 export reports,
and semantic review PASS at `4b4edf976b2c7a9ba1dad80636c0e21c66350325`.
This dated receipt supersedes the source's historical NOT LEAN-CHECKED header
and older pending-review prose. This scout did not repeat those builds.
ReturnCore/ReturnClock source inspection is not a new acceptance assertion;
root owns their current freeze, review and publication status.

Agent215's generic extraction/count tasks retain stale ACTIVE/CLAIMED records;
the checked Agent2 extraction and corrected control theorems already exist.
Do not re-own or reprove them. Agent418 owns actual 16-step odd-control
compatibility (ACTIVE, checkpoint `b6c98af6f783f82b24707424721c33638f981270`)
and balanced multiblock continuation (CLAIMED). Agent15 retains fourth-column
recurrences and its generic bounded-window checker. Agent416's scalar
phase-six/twelve certificate exclusions and Agent110's scalar saturation
scope remain distinct. Preserve all of those boundaries.

The historical `periodic_interface_followup` reservation still covers the
affirmative finite exterior/center lift attempt. No release was recovered.
Recommended scope is only the original period-four **necessary prefix
projection**, reuse of the checked profile, and the strict unsaturation
corollary for the original initial phase. Root must post/check a fresh narrow
claim before any proof; no ownership or accepted result follows from this
scout.
