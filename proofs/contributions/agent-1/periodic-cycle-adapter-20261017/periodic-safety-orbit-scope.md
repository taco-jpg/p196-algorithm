# Source-only scout: safe full quotient cycles and one ordinary orbit

Prepared 2026-10-17 by Agent1 specialist
`/root/research_status/numeric_bridge_review`. Only this report was written
for this scout. No Lean execution, new proof source, orbit experiment,
cycle search, Git mutation, or external post was performed. All prospective
statements below are scope proposals, not newly checked theorems.

## Conclusion

The repository already proves the exact exponent-stable safety criterion,
its ordinary next-output interpretation, generic all-time soundness of a
closed safe symbolic language, and conditional integer soundness of the
distinct complementary-band ReturnCertificate. Those results must be reused.

The potentially useful remaining adapter is specific: from one **supplied
finite exact period-four quotient path that returns all three blocks**, prove
that its repeated states admit one guarded exponent trajectory and therefore
one fixed ordinary orbit. With an explicit safety premise at every state of
that finite cycle, obtain a positive seed whose entire ordinary orbit avoids
palindromes. No such cycle is supplied or discovered by this implication.

The natural final witness is **the successor of the initially realized
integer**, because stored state safety excludes a palindrome in the next
output, not necessarily in the represented input. This timing distinction
is already explicit in the generic source soundness theorem.

## Exact safety predicate and existing APIs

The actual identifier is the Boolean `Agent1.Periodic.safePeriodic`, not a
new Prop named `SafePeriodic`. `Agent1PeriodicSafety.lean:16` defines

```text
safePeriodic B H w =
  not (all coefficients of B++H++w are at most9
       or (outside(B,w)=11 and every coefficient is0 or11)).
```

Here the outside is `(B++w).headD 0`. The two rejected cases are exactly the
original `FoldedDecimal.BadWord` patterns.

* `safePeriodic_iff_not_bad` at42 requires only `0<k` and `w≠[]`. It
  identifies the finite stored flag with exclusion of BadWord for the
  entire `periodicWord B H w k`. It has no coefficient-bound, symmetry,
  validity, or canonical-number premise. Thus the same stored flag applies
  at every positive exponent, including all exponents in a guarded orbit.
* `safePeriodic_strip` at59 preserves the flag under complete-period outer
  and center stripping. `safePeriodic_quotient_eq_raw` at68 compares the
  quotient flag with the **raw image** flag. Neither says the successor is
  safe because the predecessor is safe.
* `Agent1PeriodicSafetyBoundary.safe_valid_transition_counterexample`
  already supplies an original-valid safe tuple whose quotient is unsafe.
  `zero_exponent_counterexample` already shows why positive copy count
  cannot be omitted from the safety equivalence. No new boundary experiment
  is needed.
* `Agent1PeriodicSafetyNumeric.lean:14`,
  `safePeriodic_iff_next_not_palindrome B H w k n d hk hw hc hrep`, gives

  ```text
  safePeriodic B H w = true ↔ ¬ Lychrel196.Palindrome (Lychrel196.step n).
  ```

  Its premises preserve original `DecimalDigits.Canonical n d Q.length`
  and **every** in-range original column sum equal to the displayed template.
  Again it needs only positive k and nonempty w, not the stronger step
  guard3. Original period-four validity supplies nonempty w when applying it.

## Timing, positivity, and existing all-time soundness

Original `Lychrel196.IsLychrel n`, at LychrelDigitSums131, excludes a palindrome
at **all** times including zero. Safety at a represented state at time t
excludes `Palindrome (orbit n (t+1))`.

Consequently the direct all-time conclusion is

```text
∀ t, ¬ Palindrome (orbit n (t+1))
```

or equivalently `IsLychrel (step n)`, using the existing
`Lychrel196.orbit_from_step` at178. To conclude `IsLychrel n` itself, retain
an additional initial `¬Palindrome n` premise. Do not silently obtain it
from the periodic state flag. Original canonicality and
`DecimalDigits.value_positive` at693 establish `0<n`; the existing
`DecimalDigits.orbit_positive` at966 supplies positivity of its successor.

Several existing generic results already cover the numerical end of the
argument:

* `FoldedDecimal.representedBy_closed` at1599 transports a represented
  language closed under the exact next-width/next-column update.
* `representedBy_next_not_palindrome` at1606 handles the BadWord exclusion.
* `representedBy_step_lychrel` at1625 combines them for one supplied
  represented seed and explicitly concludes `IsLychrel (step n)`.
* `symbolic_language_seed_sound` at1642 starts from one admissible word
  in a closed safe indexed language and gives the explicit successor-value
  witness `value q L`; `symbolic_language_implies_decimal_existence` at1656
  packages nonemptiness and admissibility. Neither supplies such a language.

Thus a prospective new theorem is a **period-four full-cycle adapter** to
these results, not new generic certificate-to-integer or safety soundness.
If an indexed-language formulation is chosen, membership should retain only
the finite in-range q-values; the existing representation theory deliberately
does not assume equality of irrelevant infinite tails.

The same original file also already provides `BlockCertificate.sound` at1058,
`lychrel_of_shifted_family` at1080, and `expanding_family_certificate` at1100.
Their closure premise is exact equality of the **full ordinary natural
numbers** at a block boundary. Equality of mirrored pair words alone does
not identify arbitrary independently chosen initial realizers. An adapter
using these APIs must discharge that exact numeric equality, for example
through the already existing successor-value interface; it cannot simply
rename quotient-state closure as certificate closure. The generic soundness
and shifted-family proofs themselves are already done.

## Exact supplied-cycle inputs and repetition obligations

The intended premises are:

```text
B H w : Nat → Word
N : Nat
hp : QuotientPath B H w N
hv : ValidPeriodic (B0) (H0) (w0)
hN : 0 < N
hreturn : B N = B0 ∧ H N = H0 ∧ w N = w0
hsafe : ∀ i, i < N → safePeriodic (B i) (H i) (w i) = true
```

The cycle returns the complete **quotient state `(B,H,w)`**. Its exponent
is not part of that return equality: the copy count gains over a traversal,
so the complete finite coefficient word generally does not return.

`Agent1PeriodicReturnClock.lean:25`, `quotient_path_valid`, already propagates
original validity through the endpoint. `quotient_return_clock_gain` at84
already gives a natural `G>0` with clock sum `8*G`, signed quotient delta
sum `G`, and `16*G≤N≤32*G`. No graph catalog or safety premise is needed for
that result. It does not already establish a natural exponent trajectory.

The source-level obligations for a future adapter are precise:

1. Extend each supplied block sequence by its values at `t % N`. The
   original sequences are arbitrary beyond N; do not assume they already
   repeat. At the last phase, use all three endpoint equalities with the
   exact source transition at N−1. A projected graph cycle, width residue
   return, or outside return cannot replace these complete equations.
2. Use the literal natural update `(k-2)+outerPeriods+centerPeriods`. With
   `D_r := quotientDeltaSum B H w r`, the useful proposed repeat identity is

   ```text
   (k_(m*N+r) : Int) = (k0 : Int) + m*G + D_r,  for r<N.
   ```

   This identity and its guard proof are not yet present in the inspected
   period-four modules. Do not treat signed formal accounting as natural
   exponent evolution before the source guard3 has been established.
3. Original METHOD section4 line176 already supplies the sharp conceptual
   criterion: choose k0 at least three minus the minimum finite prefix delta.
   A conservative choice `k0=2*N+3` can reuse GuardedPath's checked finite
   lower bound for the first traversal; nonnegative total cycle gain permits
   later traversals to start no lower. Proving that block repetition and
   guard preservation is the remaining local obligation. No optimal bound
   or new prefix-minimum solver is necessary. The existing G>0 is stronger
   than the nonnegative gain needed merely to keep repeating the guards.
4. Choose one original positive canonical realization **once** at that k0.
   After the all-time repeat/guard certificate, use
   `quotient_path_actual_prefix` at arbitrary finite horizons with the same
   n,d,k0. Do not repeatedly apply `quotient_path_finite_realizable`, which
   chooses an initial copy count and potentially a new seed per horizon.
5. At each repeated state use hsafe at the residue, positive k, and the exact
   canonical full-column representation to rule out the next palindrome.
   Return `step n` as the all-time positive witness, or keep an explicit
   initial nonpalindrome assumption if the conclusion is about n itself.

This is an explicit repetition of one supplied finite certificate. It does
not exchange `∀finite horizon, ∃seed` into `∃seed, ∀horizon`. The additional
fixed full-cycle equations, nonnegative cycle gain, and finitely checked
safety data are exactly the extra hypotheses allowing the one-seed route.

## Recommended theorem boundary and import alternatives

The final conditional endpoint can be kept small:

```text
(hp, hv, hN, hreturn, hsafe as above) →
  ∃ m, 0 < m ∧ Lychrel196.IsLychrel m.
```

Its supporting transport theorem should expose that m is `step n` for one
positive initial canonical realization at a fixed finite k0. No concrete
hp/hreturn/hsafe witness is asserted, no particular integer is asserted to
be Lychrel, and no safety preservation theorem is inferred from validity.

The direct reuse route imports `Agent1PeriodicGuardedPath`,
`Agent1PeriodicSafetyNumeric`, and `Agent1PeriodicReturnClock`. Static DFS of
their pinned imports gives **27 existing modules**, hence28 with one new
adapter module. It avoids OuterCatalog, WidthLift, OuterRank, ReturnCore,
ZeroCycle, and graph discovery artifacts.

Alternatively, instantiating the existing generic indexed-language soundness
directly uses SafetyNumeric + ReturnClock + Realizability, a24-module union
before new modules. It saves three dependencies but requires the exact
closed-language membership/transport adapter, so a smaller module count is
not automatically simpler. Neither route should reprove generic arithmetic.

## Source pins and ownership boundary

| Module | SHA256 | Git blob |
| --- | --- | --- |
| GuardedPath | `66b821219ee88fa711a88eabc6985b33525e3ebaa0f224430395202e2012d916` | `e80d35796417b6c754067c53c16193d2fbc153b1` |
| Safety | `d779d12e1ab558bd9135840cbe562ef8a778938e7260a70c3ec1032158b2b979` | `1584e39d28a04c409eb078b4cacbf3f9bc830be8` |
| SafetyNumeric | `b874515ae6ea49613d82eb2b1e0f3cd2f433e13a90592c7b0a37645aebd53c38` | `3446b79a7ab7ccf073f14b0cc88bf5add119cccf` |
| SafetyBoundary | `41ff84ccf6b5affdf74540c1c4d9e2377876d08f1916dab55151336c8d54df31` | `6120d6930d9e2e306aaacb233ebd3f1a369e54ea` |
| ReturnClock | `ef4b8ae6380db3b2286ed166e26fe432626eb36a812c8de5c72d54d0c6bb309e` | `100736c98e2eaaf3dbf198b18de128c3b7538dfd` |
| WidthPath | `e97afd670460a3df90e836360fed59797cb60b339ee63e42d51de826c46a2241` | `ad3cee7e70fddbf0220c66313d8421e99f90678b` |
| Quotient | `562ad271c282a8a246de344b5fa9ea7e96bd64f74098c3799c839853e792a9a4` | `63bd5f4319f6a79924b7292db3eb82e0d027b26c` |
| Realizability | `cfa1fb0e7562976600e8f56e15d5ee9970979757eacb77c00c80df3de3625953` | `68a7b98e7d7ea9078c27a5df85061bcad994ce99` |
| LychrelDigitSums | `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57` | `8a865176625283648a8a20dd2411ed77670eb0a2` |

GuardedPath sources were read in `/workspace/p196-agent1-guarded-path-20261017`;
ReturnClock in `/workspace/p196-agent1-clock-20261016`. This report does not
claim any new execution of those modules. The exact generic soundness APIs,
local period-four declarations, safety boundary counterexamples, and retained
original METHOD were inspected. No exact period-four closed-cycle soundness
adapter was found in that scope; broader equivalence/ownership comparison
is the complementary task of `/root/verification_plan`.

Original METHOD blob`5c5f94c66d6c3adb0288b610f748fcbed32b115c`, lines168–176,
already states the conditional safe-cycle argument. Line212 reserves the
subsequent finite exterior/center lift attempt to `periodic_interface_followup`.
The new scope, if claimed, must be advertised as kernel formalization of
that existing conditional criterion, leaving affirmative cycle discovery,
interface construction, and the unresolved historical lane untouched.
Agent17's uniform-seed task and the existing ReturnCertificate-to-integer
soundness must not be re-owned. Parent should finish the fresh ownership
comparison and accepted claim before any new mathematical development.
