# Fixed period-four full-return soundness: source and ownership scout

Agent #1 specialist `/root/verification_plan`, 2026-10-17 UTC. This is a
source-only report. No Lean proof, compilation, mathematical experiment,
cycle search, Git mutation, claim, or external message was performed. Only
this report was written. The complementary genuine specialist's arithmetic
report is `periodic-safety-orbit-scope.md`, SHA-256
`0630f8a7f69bbba3508a6abe6ee792b30078460d1fd443e7406fed0b018bdbca`.

## Conclusion

**Generic conditional all-time soundness is already proved.** The inspected
sources do not contain the narrower adapter from one supplied, positive-length,
closed **period-four full quotient path** to its repeated guarded trajectory.
The useful potential task is only that adapter and its application to the
existing safety/numeric theorems. It is formalization of the original METHOD's
already-written positive-cycle criterion, not a new criterion, a return
construction, a generic uniformity theorem, or an unconditional existence result.

The supplied tuple must return all of `B`, `H`, and `w`; an exterior/phase graph
cycle or width return is insufficient. Safety must be given at every state
of this fixed finite cycle. The repeated path must retain one initial copy
count and one ordinary seed for every traversal. The natural all-time witness
is the initial seed's **successor**, because `safePeriodic` classifies its
next output rather than its input.

No matching active claim was found in the bounded current ownership checks
below. Historical affirmative interface construction remains reserved and
unresolved. Root should make a fresh, explicit adapter-only claim before any
proof development; this scout neither reserves scope nor treats silence or
old statuses as release.

## Existing exact APIs: reuse these, do not reprove them

The original `LychrelDigitSums__75febdc48f0ca802.lean` already contains:

| Declaration | Exact existing obligation and result |
| --- | --- |
| `LychrelCertificates.BlockCertificate.sound` (1058) | A state family with positive block lengths, valid-state preservation, nonpalindromicity at every time inside each block, and exact **full natural-number equality** at the block boundary gives `IsLychrel (C.value s)`. |
| `LychrelCertificates.lychrel_of_shifted_family` (1080) | For `F : Nat → Nat`, positive fixed length `p`, universal block avoidance, and `orbit (F k) p = F (k+g)`, concludes `∀k, IsLychrel (F k)`. Positive `g` is not needed for this logical soundness theorem. |
| `LychrelCertificates.expanding_family_certificate` (1100) | Packages the same hypotheses plus `g>0` into all-family safety and decimal existence. It supplies no instance. |
| `FoldedDecimal.step_eq_word_value` (1556) | Every canonical realization of the same finite column word has the same next ordinary value. This is the relevant existing remedy for the arbitrary-representative issue below. |
| `FoldedDecimal.representedBy_step_lychrel` (1625) | An indexed word language closed under exact `nextWidth`/`nextColumns`, excluding `BadWord`, and containing a represented seed gives `IsLychrel (step n)`. |
| `FoldedDecimal.symbolic_language_seed_sound` (1642) | One admissible word in that closed safe language gives the explicit finite witness `IsLychrel (value q L)`. |
| `FoldedDecimal.symbolic_language_implies_decimal_existence` (1656) | Packages nonemptiness, admissibility, closure, and BadWord exclusion into decimal existence. It does not construct the closed language. |

`BlockCertificate.avoids` includes its starting time zero. A quotient-state
return gives equality of coefficient words at a shifted exponent; it does
**not** identify arbitrarily selected ordinary representatives. Thus setting
`F k` to an arbitrary canonical realizer does not discharge the certificate's
full-number `closes` field. Reuse the successor-value interface, an invariant
that carries the actual integer, or the existing indexed-language soundness.
Do not assume pair-word injectivity.

The already checked original scalar two-gap certificate route is also complete
conditionally. `Agent109.Cert.certificate_sound` in
`ReturnCertificate__3f43ec0db45b8fd7.lean:259` assumes `check cert = true`, an
actual realization of its first scalar template, and both lower band bounds;
it concludes `∀k, ¬Palindrome (orbit (step n) k)`. Its `LocalOK` includes each
scalar template transition, safety test, and next guard inequalities, and
`inv_step` already proves indefinite successor closure. It is a different
finite object from the arbitrary period-four `(B,H,w)` quotient. No conversion
from the latter into that scalar certificate was found or should be presumed.

`Agent112.Admissibility.checked_positive_decimal_seed` already supplies a
positive seed from an accepted scalar certificate. `Agent112.Eventual`'s
`original_arbitrary_safe_symbolic_positive_seed` also already transfers an
entire infinitely safe symbolic word orbit to positive decimal existence.
Neither fills the proposed period-four repetition/guard obligation.

## Exact supplied-cycle boundary and missing assembly

Use the existing definitions, not a new predicate named `SafePeriodic`:

```text
B H w : Nat → Agent8.Word
N : Nat
hp : Agent1.Periodic.QuotientPath B H w N
hv : ValidPeriodic (B 0) (H 0) (w 0)
hN : 0 < N
hreturn : B N = B 0 ∧ H N = H 0 ∧ w N = w 0
hsafe : ∀ i, i < N → safePeriodic (B i) (H i) (w i) = true
```

`quotient_return_clock_gain` already gives `∃G:Nat, G>0`,
`quotientClockSum ... N = 8*G`, `quotientDeltaSum ... N = (G:Int)`, and
`16*G ≤ N ≤ 32*G`. `quotient_path_valid` already propagates original validity.
Neither proves the natural copy trajectory or its source guards.

The first concrete proof obligation after a fresh claim would be the periodic
extension of the literal path: define each repeated block by its value at
`t % N`, and prove every update, including the `N-1` to zero transition using
all three endpoint equalities. The supplied sequences are unconstrained past
`N`; they must not silently be treated as already periodic.

Next retain the literal natural recurrence
`k(t+1) = (k(t)-2) + outerPeriods + centerPeriods`. With
`D_r := quotientDeltaSum B H w r`, the desired supporting identity is

```text
(k(m*N+r) : Int) = (k0 : Int) + m*G + D_r,   r < N,
```

together with `3 ≤ k(t)` for every source time. The conservative fixed
`k0 = 2*N+3` can use GuardedPath's first-traversal lower bound; the positive
total gain then supports subsequent traversals. This is a proposed local
proof route, not a theorem proved by this scout. Signed telescoping alone
does not justify natural subtraction before the source guards are established.
No optimal minimum-prefix computation is needed.

After that obligation, existing `quotient_path_actual_prefix` applies at an
arbitrary horizon with **the same** chosen `n,d,k0`. Its full canonical
representation includes every in-range column and changing word width.
Choose the initial realizer once using `periodicWord_realizable`. Repeatedly
using `quotient_path_finite_realizable` would instead reselect a horizon-
dependent copy count and potentially a different seed, so is not the argument.

`safePeriodic_iff_not_bad` requires only positive copies and nonempty period.
`safePeriodic_iff_next_not_palindrome` then interprets the stored finite flag
for every canonical realization as `¬Palindrome (step n)`. Its source-time
application gives nonpalindromicity at time `t+1`, including all positive
times; `orbit_from_step` gives `IsLychrel (step n)`. A conclusion `IsLychrel n`
would additionally need `¬Palindrome n`. Existing validity and the copied
period-four length supply period nonemptiness; existing positivity gives a
positive successor witness.

The useful final conditional endpoint is therefore

```text
(hp, hv, hN, hreturn, hsafe as above) →
  ∃ m, 0 < m ∧ Lychrel196.IsLychrel m.
```

Its supporting theorem should expose the fixed seed and its repeated exact
representations. The final statement remains conditional on an entire exact
safe closed quotient cycle, of which none is constructed here. This does
not infer a uniform seed from unrelated finite witnesses. It does not prove
safety preservation: the existing `safe_valid_transition_counterexample`
already refutes that assertion.

The complementary arithmetic specialist's static import analysis recommends
`Agent1PeriodicGuardedPath`, `Agent1PeriodicSafetyNumeric`, and
`Agent1PeriodicReturnClock`: 27 existing modules, hence 28 with one new
adapter. A direct indexed-language alternative has 24 existing modules but
requires finite-tail-aware language closure. These are source-derived counts,
not fresh builds by this scout.

## Current ownership and actual published source comparison

Latest coordination head read and reread:
`31e6b0e0a1300923a6459f62c057bb16b73b156a`.
Current main: `74a1c3922eb7af438fe40b23d2105ad07556e3f5`.
The 25-commit delta from the previous scout's `b15889e8…` added Agent1's
GuardedPath and upper-gap claims, Agent103's residual-five count, and delivery
or documentation updates; it did not change the related ownership records
below. Current recursive task and main trees were not truncated. Issue #61
pages 8–9 were inspected for the relevant delta through comment `6227491947`;
no fixed-cycle adapter acknowledgment or scope release appeared. The readback
still had that same last comment. This was a bounded targeted equivalence
check, not a review of every theorem on every retained branch.

| Owner / exact task blob | Scope and source comparison |
| --- | --- |
| Agent105 affine dynamics, `768a0d1ca7fbdd8e789e72323e4f7cde1acb1f8b` | Actual PR105 is merged, source head `b312815ba86b086fa195768d685a2a0f355801be`. Claim explicitly excludes Agent1 period-four work and **all-time palindrome avoidance**. Full current `UniformReturn`, `UniformReturnPlain`, and `UniformIntegerReturn` source was read. Their result is uniform finite safe return time for a fixed finite affine-run family, conditional on actual variable returns. No exported fixed-cycle all-time theorem occurs in these endpoint modules. |
| Agent17 uniform finite seed, `a6a11ab96687025a6eac6517941967fa92425f6f` | The task record is CLAIMED with null checkpoint, but the actual current branch `6031b2831a8a494ed501a3059857992bb8cd5815` contains `UniformFiniteSeed.lean`, blob `737dc56143720235deeb5d3be16f42197b0c96a0`. It proves `finite_uniform_extraction` from one fixed finite candidate list and a quantifier-swap counterexample. Source was read, not compiled here. Do not infer absence of source from stale metadata or re-own finite-ensemble compactness. |
| Agent217 uniformity, `6075a4683e1901b9a3e0ac02ddb626dc70230d53` | Current branch `b3a8ccc6b0516ed68590a47d8b6cbbf6c3de3c70`, source blob `28f7c72f68fd0d1e23658409c7131380feea9188`, gives `fixed_seed_uniformity_iff_all_time`; the seed existential is already outside the horizon universal. It assumes the missing uniformity and has no periodic path. Its record explicitly says no Lean execution was available. |
| Agent423 uniformity repair, `c7c14c495ed6aa1ba56c0575570b40d82e40b718` | Nonexclusive finite-ensemble extraction/stabilization and exact finite failure checker, with decimal semantics. Record checkpoint `6b4cd0c9863b384babdc1daeed3f77cd41d6987a`. Preserve Agent17/217/315/317 ownership; no fixed survivor ensemble or accepting return instance is supplied. The record was read; no new audit of its math sources is claimed. |
| Agent12 full-interface guards, `a3f57b466c0f41b9acef3f17dd7cbdf4647619ea` | ACTIVE seven-step guard persistence or exact counterexample, checkpoint `5522b5eeb69431ee9932673d19beaf4b38a0edbc`. Our input is a complete exact period-four closed path, not the assertion that one local/seven-step return guard is invariant. |
| Agent11 accepting certificate, `6bb41233af39f53e70023b6d6ca3e1ae13b76c1d` | Concrete accepted scalar return-certificate discovery; its record already says generic admissibility is solved and keeps Agent109 soundness/Agent110 budgets unchanged. No cycle discovery should be added to the proposed adapter scope. |
| Agent13 return slope, `cfb3aa0379beea572fb8488050f7b986e6a9da42` | Owns proportional signed gains for repeated returns of the same injective scalar two-gap family. Current branch `60ba0c8c31bec7b402ada3822ac13eb2f87d2dbe` exposes `qualifying_return_coordinatewise_nonnegative`, source blob `801d57980bae22cde091a0d8edb5739cb76dae20`. Do not generalize the proposed adapter into generic return-slope/translation determinism. |
| Agent21/211/311 | Their existing accepted-certificate realizability and eventual-symbolic-orbit lanes remain unchanged; exact current blobs are respectively `47bb2d0bdfba3de4a262914b6c5193d58036ee2f`, `d38db46668ae2b97b4d79ee08f505d3c29bf90eb`, `8d3982289b81d061f66529c29e634b78dc01c2b4`. Existing soundness must be reused. |

PR105's `uniform_integer_safe_return` quantifies over all realizers for each
large parameter and includes safety at all positive times through its one
uniform endpoint. It does not assert equality to independently selected
integer realizers or iterate its conclusion forever. Its source and claim
both say so. Moreover `wordAt rs k` is a fixed finite affine-run table; no
adapter encoding arbitrary copies of a nonconstant period-four block as that
fixed table was found. Importing its large closure is unnecessary for the
local full-cycle route.

Agent1's actual current GuardedPath branch is
`2d5cfe447811155e93cef173192e96f64ec824e1`; current Clock branch is
`ebcaf723d61f9513c8bae30440d02ba4a46343b4`. GuardedPath explicitly retains
finite-horizon quantifiers. Clock supplies positive gain but no repeated
natural schedule. Their conjunction still needs the proposed adapter.

## Original attribution and unresolved historical lane

The preserved METHOD path is
`proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/research/main_existence_attempt/continuation_pass/periodic_bulk_followup/METHOD_AND_PROOF.md`,
blob `5c5f94c66d6c3adb0288b610f748fcbed32b115c`, SHA-256
`45c34243ff0eef9fb30ef91e2d43ae933a77e4ca4d0b4bd307e9f0c259781559`.
Lines 168–176 already state the exact conditional positive-gain safe-cycle
argument, with initial exponent at least three minus the minimum prefix
delta. They explicitly state that no such cycle was found. Line 212 assigns
the subsequent finite exterior/center lift attempt to the sibling
`periodic_interface_followup/`.

Current main's complete recursive tree, the local SOURCE_MAP, and the
available local `git log --all -- '**/periodic_interface_followup/**'` yielded
no sibling source or release. This establishes neither current activity nor
abandonment. A claim must explicitly preserve affirmative search/lift
construction and formalize only the already-written implication for a
supplied exact full cycle. The substantive bottleneck after that implication
would still be a concrete qualifying safe closed tuple path.

## Exact source identities used in this scout

| File | Git blob | SHA-256 |
| --- | --- | --- |
| `LychrelDigitSums__75febdc48f0ca802.lean` | `8a865176625283648a8a20dd2411ed77670eb0a2` | `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57` |
| `ReturnCertificate__3f43ec0db45b8fd7.lean` | `95196cfe2da9b224412a9c31910163cf5784f996` | `b6d34e8fb031401171b517eef8a2d91222334a5745cc88329e0a2ad13db47058` |
| `Agent1PeriodicGuardedPath.lean` | `e80d35796417b6c754067c53c16193d2fbc153b1` | `66b821219ee88fa711a88eabc6985b33525e3ebaa0f224430395202e2012d916` |
| `Agent1PeriodicReturnClock.lean` | `100736c98e2eaaf3dbf198b18de128c3b7538dfd` | `ef4b8ae6380db3b2286ed166e26fe432626eb36a812c8de5c72d54d0c6bb309e` |
| `Agent1PeriodicSafety.lean` | `1584e39d28a04c409eb078b4cacbf3f9bc830be8` | `d779d12e1ab558bd9135840cbe562ef8a778938e7260a70c3ec1032158b2b979` |
| `Agent1PeriodicSafetyNumeric.lean` | `3446b79a7ab7ccf073f14b0cc88bf5add119cccf` | `b874515ae6ea49613d82eb2b1e0f3cd2f433e13a90592c7b0a37645aebd53c38` |
| `Agent1PeriodicRealizability.lean` | `68a7b98e7d7ea9078c27a5df85061bcad994ce99` | `cfa1fb0e7562976600e8f56e15d5ee9970979757eacb77c00c80df3de3625953` |
| `Agent105UniformReturn.lean` | `56af3389e169bf50592de52fc4f9246651efbfcd` | `fba98eb095ca439835e82a90315254090ed03935c3d17d9e6ae8ebe5bb7b7fa7` |
| `Agent105UniformReturnPlain.lean` | `05db00e40e247715efb46b9efdc2ba089ad5ddab` | `0d4d048c017966827be4d146ef52d50de8ea3fc777fd7f21220c73694f5155af` |
| `Agent105UniformIntegerReturn.lean` | `496f694e39854b6545d784dc8a11418d789d76ab` | `2e8f4163092c06ac683c112da149a616bad04e2316406f9854b44fe9456a6f98` |

GitHub blob responses were decoded and their actual Git blob identities
checked. Local sources were read from the GuardedPath and Clock worktrees;
source hashes were computed without modifying them. Existing verification
reports were not promoted into a new build claim. The remote heads can
advance after this report, so root must refresh ownership before claiming.
