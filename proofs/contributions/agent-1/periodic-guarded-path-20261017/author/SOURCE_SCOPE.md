# Source-only scout: guarded full quotient paths and one ordinary seed

Prepared 2026-10-17 by Agent1 specialist
`/root/research_status/numeric_bridge_review`. Only this report was written
for this scout. No Lean execution, new proof, orbit experiment, discovery
search, Git mutation, or external post was performed. All new interfaces
below are proposals, not checked declarations.

## Finding and smallest useful scope

General ordinary one-seed iteration soundness already exists. The useful
remaining work appears to be a small adapter from the recently introduced
literal `QuotientPath` and an explicitly guarded natural exponent schedule
to those existing semantics, with the consequential finite-horizon corollary
requested later by root: start at `2*N+3` to supply all finite guards. No
general numeric bridge, initial-realization
construction, certificate soundness theorem, or prefix-control solver needs
to be reproved.

In the inspected source and contribution scope, no declaration already
packages arbitrary finite period-four `QuotientPath` data with these exact
exponent guards and a fixed supplied ordinary seed. This is a scoped absence
finding, not an exhaustive theorem-equivalence claim. Parent should combine
this report with the complementary fresh ownership scout and perform the
normal coordination delta check before claiming anything.

## Existing declarations to reuse

All line references below refer to the exact pinned files listed later.

1. `OverflowCarryNormalization.iterPairs_representation`,
   `LychrelDigitSums__75febdc48f0ca802.lean:2400`, already says that a single
   supplied `n` with original `Canonical n d L` and all in-range pair sums
   realizes every `iterPairs q L k` state of **the actual `Lychrel196.orbit
   n k`**, with changing width. This is the generic one-seed theorem.
   Its recursion uses original `FoldedDecimal.representation_next` at1568.
2. `Agent1.Periodic.actual_step_representation`,
   `Agent1PeriodicZeroNumeric.lean:102`, is an existing arbitrary-word
   list/index adapter. Despite its filename, it has no zero-period premise:
   supplied original canonical representation and all column sums for `W`
   give a canonical representation and all column sums for `stepWord W`
   at the ordinary successor of the same `n`. This avoids rebuilding any
   list/index compatibility from the generic theorem above.
3. `Agent1.Periodic.quotient_step_bounded`,
   `Agent1PeriodicQuotient.lean:87`, identifies that exact `stepWord` with
   the maximally stripped successor template. Premises are the three
   original coefficient bounds, period length four, and `3 ≤ k`.
   The next exponent is exactly
   `(k-2) + outerPeriods B H w + centerPeriods B H w`.
4. `QuotientPath`, `Agent1PeriodicWidthPath.lean:17`, supplies the three
   coefficient bounds, period length, and **all three** literal next-block
   equalities at every `i < N`. It deliberately supplies neither an exponent
   schedule nor canonical ordinary realization.
5. `zeroLiftWord_actual_orbit`, `Agent1PeriodicZeroCycle.lean:17`, already
   provides same-seed all-time transport in the zero-period case under its
   all-time interface cap and the resulting specific guarded exponent.
   `zeroLiftWord_actual_prefix`, `Agent1PeriodicZeroEscape.lean:15`, already
   provides the finite-prefix version under a cap only through `N`.
   The new scope must not re-own either result.
6. `periodicWord_realizable`, `Agent1PeriodicRealizability.lean:50`, supplies
   a positive ordinary canonical input realizing every in-range column for
   one original-valid tuple and one positive copy count. The integer may
   depend on the chosen tuple and exponent. Reapplying this independently
   at each time does not give same-seed transport.
7. Strict positivity already follows from original canonicality:
   `DecimalDigits.Canonical` at907 includes positive length, positive leading
   digit, and `value d L = n`; `DecimalDigits.value_positive` at693 converts
   those fields to `0 < n`. `DecimalDigits.orbit_positive` at966 then gives
   `0 < Lychrel196.orbit n t` at every time. No new positivity arithmetic is
   needed and no extra `0 < n` premise is necessary.

The current `periodic_actual_step_canonical_width` and
`periodic_actual_step_decimalLength` in `Agent1PeriodicNumeric` identify
ordinary widths for positive copy counts, but do not identify all successor
columns with a quotient template at such small counts. They are insufficient
as a substitute for `quotient_step_bounded` with its stronger guard.

## Proposed exact adapter contract

Let `B H w : Nat → Word`, `k : Nat → Nat`, and `N : Nat`. Define only as
notation in the proposed statement

```text
Q i := periodicWord (B i) (H i) (w i) (k i).
```

The proposed hypotheses are:

```text
hp     : QuotientPath B H w N
hguard : ∀ i, i < N → 3 ≤ k i
hkstep : ∀ i, i < N →
  k (i+1) = (k i-2) + outerPeriods (B i) (H i) (w i)
                         + centerPeriods (B i) (H i) (w i)
hcan   : DecimalDigits.Canonical n d (Q 0).length
hrep   : ∀ j, j < (Q 0).length →
  DecimalDigits.columnSum d (Q 0).length j = ((Q 0)[j]?).getD 0
```

The proposed conclusion is:

```text
∀ t, t ≤ N →
  0 < Lychrel196.orbit n t ∧
  ∃ d', DecimalDigits.Canonical (Lychrel196.orbit n t) d' (Q t).length ∧
    ∀ j, j < (Q t).length →
      DecimalDigits.columnSum d' (Q t).length j = ((Q t)[j]?).getD 0.
```

The useful algebraic adapter immediately before it is the exact finite-step
identity `stepWord (Q i) = Q (i+1)` for `i < N`, obtained by substituting the
existing quotient theorem and the supplied successor equations. The numeric
statement should compose the existing `actual_step_representation`, not
reprove decimal normalization or `iterPairs_representation`.

Boundary and scope requirements:

* Guard only used sources `i < N`. No guard at the terminal `N` is required
  for representing that endpoint. Include `N = 0` without an artificial
  `k 0 ≥ 3` or positive-copy-count premise.
* `quotient_exponent_accounting` at131 proves only next exponent **at least
  one**, plus its equality to the signed shift. It does not imply the next
  source guard three. Do not cancel truncated natural subtraction or infer
  indefinite continuation from a positive initial exponent.
* Full initial `ValidPeriodic` is unnecessary for a **supplied** original
  canonical full-column realization: `hp` supplies the local algebraic
  bounds actually used. It becomes relevant only for a separately requested
  existential initial-seed corollary using `periodicWord_realizable`.
* No graph membership, graph path, independently chosen carry sequence,
  prefix return, or width return replaces the three exact full successor
  equations. This adapter therefore does not realize the ZeroWidthLoop's
  chosen abstract walk.
* No safety, initial nonpalindromicity, return, cycle existence, indefinite
  guard synthesis, infinitely safe seed, or 196 conclusion belongs here.

## Consequential finite-horizon corollary requested by root

The source-only follow-up search found no exact existing general declaration
for this proposed concrete finite bound. Define a natural exponent schedule
by the same literal update along the **supplied full path**, starting at
`k 0 = 2*N+3`. The proposed elementary guard certificate is

```text
∀ i, i ≤ N → 2*(N-i)+3 ≤ k i.
```

This is the conservative finite budget suggested by the existing update:
each step subtracts at most two and both added period counts are natural.
It requires no graph search, interface cap, signed prefix minimum, positive
cycle gain, or choice of inner carries. The inequality remains a proposed
Lean obligation in this scout; no proof script or numeric test was run.

With original `ValidPeriodic (B 0) (H 0) (w 0)` and `hp`, the useful resulting
new contract is:

```text
∃ n, 0 < n ∧ ∀ t, t ≤ N →
  ∃ d, DecimalDigits.Canonical (Lychrel196.orbit n t) d
        (periodicWord (B t) (H t) (w t) (k t)).length ∧
    every in-range original column sum equals that displayed template.
```

Use `periodicWord_realizable` once at the positive initial copy count
`2*N+3`, then the supplied-seed adapter above. Indeed every original initial
canonical full-column realization at that count should satisfy the adapter;
the existential wrapper merely chooses one existing witness. The endpoint
guard is also at least three for this particular schedule, although the
more general adapter does not need an endpoint guard. At `N=0` this
corollary reduces to an ordinary initial realization at copy count three.

This makes the finite guards concrete while preserving the decisive
quantifier order: **for each finite path/horizon there is a seed**. The seed
and its initial width may depend on `N`. Nothing permits exchanging those
quantifiers to obtain one seed for all horizons. Nor does it supply any
full path or solve whether a prescribed abstract graph walk admits one.

This follows the already written finite guard-selection principle in
original METHOD line164; retain that attribution. It is distinct from
ZeroEscape's existing zero-period interface-cap budget `M+3` and finite
same-seed theorem. No replacement or refactoring of the frozen zero module
is needed.

## Minimal source closure and pins

Direct imports `Agent1PeriodicWidthPath` and `Agent1PeriodicZeroNumeric`
give **20 existing modules**, hence **21 including a new adapter module**.
The count is a static DFS of exact existing registry entries and literal
imports, not a new build. The ZeroNumeric import already brings its
arbitrary-word adapter and the original generic arithmetic.

Adding the requested finite-horizon initial-seed corollary requires importing
`Agent1PeriodicRealizability`, increasing the closure to21 existing/22 total.
Thus **22 total modules** is the recommended closure for the enlarged
candidate. The 21-module option remains the supplied-seed adapter alone.
Do not import ZeroCycle/ZeroEscape, graph catalogs, ReturnCore, or ReturnClock
just to obtain a theorem already available in the smaller closure.

Twenty-module order:
`PeriodObstructions`, `ActualWordBridge`, `PrefixSemantics`,
`LychrelDigitSums`, `IncomingCarry`, `Agent1RepeatedBlock`,
`Agent1RepeatedBlockContext`, `Agent1PeriodicDigits`, `Agent1PeriodicSlices`,
`Agent1PeriodicGuard`, `Agent1PeriodicGuardFacts`, `Agent1PeriodicOuterStrip`,
`Agent1PeriodicCenterStrip`, `Agent1PeriodicQuotient`,
`Agent1PeriodicWidthPath`, `Agent1PeriodicParity`, `Agent1PeriodicPositivity`,
`Agent1PeriodicValidity`, `Agent1PeriodicZeroPeriod`,
`Agent1PeriodicZeroNumeric`.

Inspected local source worktree: `/workspace/p196-agent1-zero-width-loop-20261016`,
published HEAD `4c08e285a6c3ae05cc4953f1e7e0e52e1d4b2d9e` at readback.

| Module | SHA256 | Git blob |
| --- | --- | --- |
| WidthPath | `e97afd670460a3df90e836360fed59797cb60b339ee63e42d51de826c46a2241` | `ad3cee7e70fddbf0220c66313d8421e99f90678b` |
| Quotient | `562ad271c282a8a246de344b5fa9ea7e96bd64f74098c3799c839853e792a9a4` | `63bd5f4319f6a79924b7292db3eb82e0d027b26c` |
| ZeroNumeric | `8e561a621f18d783aa52ef0f2d6985b0a6cd0293b80fe4b174250665cee07b89` | `043300254bb2f95cae725f9963848a011cc2cd58` |
| Realizability | `cfa1fb0e7562976600e8f56e15d5ee9970979757eacb77c00c80df3de3625953` | `68a7b98e7d7ea9078c27a5df85061bcad994ce99` |
| ZeroCycle | `ffea963ec5895ef493c289430d5a50e81ae241014d2baf8756beaa6996a23fbd` | `b49d76e77da6ead4a9a96ff870102b1f028cc55c` |
| ZeroEscape | `e1c9b9f90b5b2fddf3a4642b29030b1db7ab507d155a092facc713de5aaf0969` | `7c61097e346506a079c2e75ad46f1563531f4d65` |
| Original LychrelDigitSums | `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57` | `8a865176625283648a8a20dd2411ed77670eb0a2` |

## Existing ownership and source comparison

Actual read-only API inspection used main snapshot
`74a1c3922eb7af438fe40b23d2105ad07556e3f5` (proofs tree3244 direct entries,
untruncated), coordination snapshot
`8f7445d5eb90f1461fa7deebd6bb8479794c12f2` (227 task records), and149 listed
branches. Relevant actual task blobs and published source were inspected;
this is not an exhaustive read of all227 task bodies. Complementary fresh
issue/ownership review is assigned to `/root/verification_plan`.

* Agent418 balanced continuation (`aa2047b6...`), multiblock compatibility
  (`cece5c4c...`), and saturated input audit (`e39a4913...`) concern exact
  prefix controls, concrete eight-/sixteen-step seeds, and continuation
  constraints. They do not supply or reserve this arbitrary full quotient
  path adapter. At actual published source `b6c98af6...`, submission tree
  `d7d5895d...` contains `Agent418ActualCarrySuppression` (blob`1c5de9f3...`)
  and `Agent418TwoBlockWitnesses` (blob`af25268f...`). Their actual declarations
  concern already canonical orbit windows and64 specific sixteen-step seeds.
  `every_pattern_has_finite_decimal_seed` in the separate saturated bundle
  (blob`47d77265...`) concerns16 specific eight-step patterns. No new pattern
  classification or balanced-continuation claim is proposed here.
* Existing `Agent109.pairWord_step` / `pairWord_orbit` at TemplateStep636/644
  already identify the complete ordinary orbit with its pair-word orbit.
  `Agent109.Cert.certificate_sound` at ReturnCertificate259 already gives
  same-seed all-time nonpalindromicity from an accepted complementary-band
  certificate plus its exact template realization and gap lower bounds.
  This is a different state/template and a stronger conditional invariant
  route, not a missing theorem to re-own.
* `Agent112.Admissibility.checked_positive_decimal_seed` at
  `AdmissibleCompat__f7177d4d859e88d5.lean:30` already proves the conditional
  accepted-certificate-to-positive-Lychrel-seed endpoint. Agent23's existing
  `checked_certificate_gain_integer_interface` composes it with gain bounds.
  Agent21 task blob`47bb2d0b...`, Agent211`d38db466...`, and
  Agent311`8d398228...` cover this certificate-realizability lane. The present
  supplied-seed adapter neither constructs nor accepts a ReturnCertificate.
* `Agent112.Eventual.original_arbitrary_eventual_realization` already
  transports arbitrary positive coefficient words after an existential
  transient to some ordinary seed. It does not preserve a specified initial
  seed at time zero. Its conditional safe-seed transfer is also already done.
* Agent1's published return-core research queue explicitly lists the
  supplied guarded finite quotient-path correspondence as an **unclaimed
  candidate**, with historical affirmative search excluded. The existing
  general `QuotientPath` source and zero-specialized transports are the
  contributions to reuse.

## Historical affirmative-interface boundary

Preserved original METHOD, blob`5c5f94c66d6c3adb0288b610f748fcbed32b115c`,
line212 states: “The sibling `../periodic_interface_followup/` owns the
subsequent finite exterior/center lift attempt and is outside this bundle.”
STATUS line13 and OUTCOMES line266 repeat that allocation. METHOD185–193
also already describes eleven finite128-transition ordinary replay controls
at their exact recorded exponent floors. Those are existing computational
evidence, not a uniform Lean quotient-path transport theorem.

No retained sibling implementation/source-map entry was recovered; the
available `git log --all` search for that directory and the literal
`affirmative_interface_followup` name returned no entries. This does not
establish release or abandonment. A narrow proposal should explicitly
exclude affirmative finite-interface construction/search, indefinite guard
synthesis, cycle discovery, and historical lane takeover. The finite
`2*N+3` budget for a supplied path does not solve those historical tasks.
It should seek any exact
already published adapter or active owner through the normal coordination
process before an accepted claim. No mathematical development has begun.
