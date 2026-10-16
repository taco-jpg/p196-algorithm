# Exact mass / 9 bounds: independent semantic review

Reviewer: the real non-author subagent `/root/strategy_review`, for Agent #104.
The reviewer did not edit either new Lean proof module. All mathematical
statements below refer to the frozen sources:

| Module | SHA-256 |
|---|---|
| `Agent104ExactZeroGap` | `f8187cafd7210bdf63e360694d875b278b174516d81270ab47d2170a0b1d46bc` |
| `Agent104FiniteMassBound` | `1f9b28478ef73a90ee6145cf34e3f8a4322ce4d5279051948f469a0fd0f71ccb` |

The four imported foundation modules are pinned in the contribution's
`source-pins.json`; all six module fingerprints and all eleven public theorem
endpoints are independently registered in `proofs/Agent104ExactMass.registry.json`.
The mathematical source is the preserved `sparse_orbits_theorem.md`, sections
3--5, with the exact carry and width definitions of `LychrelDigitSums`.

## 1. Review conclusion and separate evidence classes

**Semantic review PASS.** The new statements express the retained mass-sensitive
zero-gap bounds and their finite ordinary-orbit consequences. No weakened
transition, artificial width, assumed non-palindromicity, or hidden all-time
digit-sum bound is introduced.

| Evidence | Scope and status |
|---|---|
| Non-author semantic review | Completed for both frozen modules and the exact imported interfaces used by their proofs |
| Independent Python arithmetic control | Completed for all 198,909 admissible words of widths 1..8; source and script fingerprints are retained |
| Author incremental Lean check | The frozen versions were reported and recorded as accepted; this is author evidence, separate from independent rebuilding |
| Non-author clean Lean rebuild | **PASS**: all six modules and the full module-origin audit exited 0 in `verification/independent-clean-001`; 1,254 theorem declarations, eleven public endpoints, only the three standard allowed axioms |

The Python control is a finite arithmetic control, not a proof of the universal
theorems. The semantic review is human-style mathematical reasoning. Only the
separate successful Lean build and axiom audit justify the kernel-check claim.

## 2. Actual finite-word semantics

`FoldedDecimal.Admissible L q` requires positive width, a positive outer
coefficient, all in-range coefficients at most 18, reflection symmetry, and
an even coefficient at an odd-width center. Values beyond `L` are irrelevant.
`DecimalZeroGap.ZeroBound q L K` bounds every nonempty all-zero interval within
the first `L` positions; it does not impose an arbitrary infinite extension.
The bound `K=0` is legitimate when no coefficient vanishes.

The update is exactly `FoldedDecimal.nextColumns`. Its branch is selected by
the actual final carry, and `nextWidth` is `L` or `L+1` accordingly. In the
overflow branch, the new outer carry digit is retained. The full word has
positive endpoints; the proofs never discard one in order to simplify the
interval geometry.

For a canonical positive integer, `q = columnSum d L` is its actual reflected
digit-pair word. The imported `iterPairs_representation` and
`iterPairs_wordSum` give canonical representations of the ordinary numerical
iterates and the identity

\[
\operatorname{wordSum}(q_t,L_t)=2S(T^t(n)).
\]

Here `T(n)=n+reverse10(n)`. Trailing zero digits are permitted, and the
numerical reversal's discarded leading zeroes do not change the integer value.
The orbit continues through palindromes; neither new module changes that rule.

## 3. Nine-mass lemma and the no-overflow bound

`interval_nine_mass` has no unnecessary admissibility or positivity hypothesis.
If `[a,a+k)` is inside the finite word and every coefficient there is nine,
then the interval contributes exactly `9*k` to a sum of nonnegative natural
numbers. The proof first bounds the prefix of length `a+k`, then uses
`wordSum_mono_length`. The case `k=0` is correctly included.

For no overflow, a zero interval in the next pair word gives simultaneous
forward and reflected zero output digits on the same interval. The proof
handles `k<=1` before invoking `simultaneous_zero_interval`, whose hypothesis
is `2<=k`. For a longer interval, the old coefficients are all zero or all
nine. The first alternative yields `k<=K`; the second yields `9*k<=M`, hence
`k<=M/9` with natural-number floor division. Thus the result is exactly

\[
\operatorname{ZeroBound}(q',L',\max(K,1,\lfloor M/9\rfloor)).
\]

No upper estimate is inferred from a lower estimate in the wrong direction,
and the mass hypothesis is on the old word, which is precisely what the carry
classification needs.

## 4. Overflow shift, natural subtraction, and short lengths

For a new zero interval `[a,a+k)` with `k>=3`, `next_zero_overflow` proves
`a>0` and `a+k<=L`. The simultaneous-zero overlap core is
`[a,a+k-1)`, of length `k-1>=2`. Both bounds are derived before any use of
subtraction identities or the old interval extension lemma.

If the core is all nine, its mass is `9*(k-1)`, giving
`k<=M/9+1`. If the core is all zero, `zero_core_extends` adds one old zero
column at each end, producing the old interval `[a-1,a+k)`. Its length is
`k+1`, not `k` or `k-1`, so `k+1<=K` and therefore `k<=K-1`.

Every subtraction is safe in its use:

- `a-1` occurs after `a>0` has been proved.
- The overlap core uses `k-1` after `k>=3` has been proved.
- The final inference from `k+1<=K` to `k<=K-1` supplies the necessary
  lower bound on `K`; it does not treat truncated subtraction as unrestricted
  integer subtraction.
- The old interval bound is `(a-1)+(k+1)=a+k<=L`, so the extension remains
  inside the old word even at either limiting internal position.

Lengths one and two are treated separately before the core classification.
The result is

\[
\operatorname{ZeroBound}
 (q',L',\max(K-1,2,\lfloor M/9\rfloor+1)).
\]

`K=0,1,2` does not invalidate this statement: an inherited long zero interval
would itself force `K>=4`, so that alternative cannot occur with a smaller
valid budget. Widths `L=1,2` cannot create a long internal overflow zero
interval; all relevant cases fall within the explicit short-length branches.
The independent exhaustive control includes every admissible word at both
widths, and in fact no such word has a nonempty new zero interval.

The common preservation theorem requires only `2<=K` and `M/9+1<=K`.
These dominate every maximum term in both branches, while `K-1<=K` is valid
for every natural `K`. It uses the proved binary bound on the actual final
carry to exhaust the two branches.

## 5. The finite-prefix hypotheses and initial gap budget

Write

\[
K=\max(K_0,2,\lfloor 2B/9\rfloor+1),\qquad
H=2B+(2B-1)K.
\]

`bounded_prefix_width` assumes a canonical representation, a concrete initial
property `ZeroBound (columnSum d L) L K0`, and

\[
S(T^t(n))\le B\quad\text{for every }0\le t\le N.
\]

This is an inclusive finite prefix. It includes time zero and the final time
`N`, with no assumption on later iterates. The propagation step to time
`t+1<=N` uses the mass at time `t`; the width estimate at `N` uses the mass at
time `N`. There is no omitted final-state mass condition or one-step indexing
shift.

`K0` is a supplied valid bound, not a hidden maximum or an arbitrary free
parameter. It may be zero, may be larger than the actual largest gap, and
need not equal the width. The two fully numerical wrappers safely choose
`K0=L`, since any interval inside a word of width `L` has length at most `L`.
They obtain `L=decimalLength n` from canonical uniqueness, rather than assuming
the length declared by an arbitrary digit array is canonical.

The width estimate uses `DecimalProfile.length_le_mass_gaps`, whose actual
hypotheses are positive width, positive endpoints, and the zero-interval
bound. It does not invoke the stronger `DecimalProfile.Valid` predicate.
Right-end positivity is derived by admissibility's reflection symmetry from
left-end positivity. This produces

\[
L_t\le \operatorname{wordSum}(q_t,L_t)
       +(\operatorname{wordSum}(q_t,L_t)-1)K
     \le 2B+(2B-1)K=H.
\]

Monotonicity of natural subtraction justifies the last mass substitution.
No illegal cancellation of `-1` is used.

## 6. Time, zero ceilings, and the escape horizon

The imported width theorem states

\[
N+4L\le4L_N+4.
\]

Combining it with the bounded-prefix width at time `N` gives
`N+4L<=4H+4`. The defined horizon is

\[
E=4(H-L)+5,
\]

where subtraction is natural subtraction. In the proof by contradiction,
absence of an escape for `t<=E` implies the bounded-prefix hypothesis.
Applying the width bound at time zero first establishes `L<=H`. Only then
does the time inequality contradict `E=4(H-L)+5`. Thus the `+5` strictly
exceeds the clock's `+4`, and `H-L` is not cancelled without its side condition.

Boundary checks:

- `N=0`: the prefix is the singleton initial state, not an empty hypothesis.
  Width induction starts with the explicitly supplied initial zero bound.
- `B=0`: `H=0` because `2*B-1` truncates to zero. A positive canonical seed
  cannot satisfy the bounded-prefix premise even at time zero, so the
  conditional width/time statements are vacuous. The escape conclusion is
  valid; time zero already has positive digit sum.
- `H<L`: an initial digit sum at most `B`, together with the valid `K0`, would
  imply `L<=H`. Therefore this case already entails an immediate escape.
  The defined natural-subtraction horizon becomes 5 and still includes time
  zero; the theorem does not claim that 5 is the earliest escape time.
- `n=0`: excluded in both fully numerical wrappers by `0<n`. In the canonical
  variants, positive width and a positive leading digit already enforce a
  positive represented integer.

## 7. Independent coefficient derivation for the square bound

Let `C=max(K0,2)+1`, `u=floor(2B/9)`. The elementary bound
`gapBound K0 B + 1 <= C+u` is valid also when `B=0` or `K0=0`.
Using only nonnegative products gives

\[
\begin{aligned}
H&\le2B(K+1)\le2B(C+u),\\
9H&\le18CB+2B(9u)\le18CB+4B^2.
\end{aligned}
\]

This is exactly `widthBound_scaled`; its coefficient 4 comes from
`(2B)*(2B)`, and the factor 18 is `9*2`.

The imported `runningMax n N` is the ordinary digit-sum maximum of the
`N+1` states at times `0..N`; it starts with `digitSum n`. Substituting
`D=runningMax n N` into the finite-prefix time inequality is justified by
`digitSum_le_runningMax`, including at time zero. Multiplying that inequality
by 9 and the scaled width inequality by 4 yields

\[
9(N+4L)\le36H+36\le16D^2+72CD+36.
\]

Thus all three published coefficients, **16, 72, and 36**, are correct. The
canonical statement retains the supplied `K0`; the positive-seed numerical
wrapper substitutes `K0=decimalLength n`. No real square root, real liminf,
or asymptotic limit is asserted by these Nat theorems.

## 8. Retained independent finite arithmetic control

`independent_zero_gap_control.py` is the saved implementation of the earlier
in-memory experiment. It imports only the Python standard library. It generates
the first half of a symmetric word directly from `0..18`, filters a positive
outer entry and an even odd-width center, and reflects it. The normalization
uses the ordinary decimal expansion of the integer `sum(q[i]*10**i)`; no Lean,
author carry implementation, or proof generator is called.

Both inequalities are checked with the exact old mass and exact longest old
zero interval, which are the smallest valid supplied budgets. Every larger
valid `M` or `K` only enlarges the right-hand sides. Universe counts are checked
against independently stated finite counts, not merely reported after a loop.

| Width | Admissible words |
|---:|---:|
| 1 | 9 |
| 2 | 18 |
| 3 | 180 |
| 4 | 342 |
| 5 | 3,420 |
| 6 | 6,498 |
| 7 | 64,980 |
| 8 | 123,462 |
| **Total** | **198,909** |

All tests passed, split into 93,931 no-overflow words and 104,978 overflow
words. The JSON retains equality examples and examples with initial gap
budget zero or one. The stored script was actually rerun and exited 0;
`independent_zero_gap_control.json` includes source/script SHA-256, Python
version, elapsed time, and an explicit finite-control evidence label.

Reproduce from the repository root:

```sh
python3 proofs/contributions/agent-104/exact-zero-gap-mass-20261016/review/independent_zero_gap_control.py
```

## 9. Source linkage, independent build, and limits

The independent build uses `proofs/verify_project__214bf7673efe116b.py` exactly
as mapped by `SOURCE_MAP.json`, with SHA-256
`c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a`.
Its `--help` was read before invocation. It has no `--source-repo` option;
the direct current-file path correctly anchors its own `ROOT` at the mass
worktree. The five-line replay wrapper `proofs/verify_project.py` is not used.

`verification/replay.py` checks that unmodified verifier fingerprint and invokes
it with the independent six-module registry. The output path must not exist;
the checker snapshots all six exact sources into a new source/build directory,
checks their registered SHA-256, Git blob and imports, compiles the complete
local closure, and audits all theorem declarations by their true module origin.
It does not reuse any project olean or the author's build directory.

The build began before the new publication was announced, while the worktree
HEAD was `ae8bbdfd2a18e8910eebc25fd2a81661c01abc16`. The verifier's
`source_tree_clean` field checks tracked files only because its command uses
`--untracked-files=no`; that field must not be interpreted as saying the new
proof files were already committed in this worktree. Its static `agent` label
is inherited unchanged from the original checker; the actual non-author
operator is recorded in this review and the independent registry.

The announced publication is commit
`1c3d7b7b9d45e2aa40f689690c188bb3878de891`. The retained published-source linkage
record separately compares each of the six published blobs with the exact
compiled snapshot. It does not rewrite the original build's source HEAD,
tracked-clean flag, command records, or status.

The published-source linkage completed successfully: all six published blobs
equal the actual compiled snapshots byte for byte, and the invoked unmodified
checker also equals its published blob. The independent summary rechecked all
seven successful command records, all command-log hashes, the complete retained
non-olean file inventory, and the true originating module of each of the eleven
public endpoints. The module theorem counts are 986 for `LychrelDigitSums`,
42 for `Agent104ExactZeroGap`, 145 for `ProfileDynamics`, 61 for
`SharpProfileBounds`, and 20 for `Agent104FiniteMassBound`; the definitions-only
`SharedProfile` owns zero theorem declarations and was nonetheless compiled and
included in the selected origin audit. These counts include generated private
proof declarations. The union of theorem axioms is exactly `Classical.choice`,
`Quot.sound`, and `propext`. See `verification/independent-review-summary.json`
for the separately retained non-author sign-off; the original verifier output
remains unchanged.

These results establish quantitative finite-prefix consequences for the actual
decimal reverse-and-add operation. They do not establish palindrome avoidance,
the existence of a Lychrel number, eventual divergence of every individual
digit sum, or optimality of the constants. Here “exact” means retaining the
original report's division-by-nine mass estimate and overflow interval shift.
