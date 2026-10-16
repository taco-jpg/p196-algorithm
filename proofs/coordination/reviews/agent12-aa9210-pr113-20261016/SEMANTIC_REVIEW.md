# PR113 independent exact-source review

**Verdict: ACCEPT_EXACT_SOURCE_WITH_COMPLETED_INDEPENDENT_AUDIT** for `cd11afd68833051c81051df22573e8827ab6b671`. The new complete nine-module replay and expanded audit passed at explicit trust zero: 1,042 theorem constants, 164 safe definitions/opaques, and literal axiom reports for all 38 public endpoints. The four new modules contribute 86 theorem constants and one safe definition. No mathematical-source repair was needed. The historical safe-definition audit gap is repaired in independently attributed verification infrastructure only; the old records are preserved unchanged. The only accepted transitive axioms are `Classical.choice`, `Quot.sound`, and `propext`. Current-main combination and publication remain the parent integrator's separate responsibility.

Reviewer: **Agent #12 /root/review109**, independently reviewing PR113. This reviewer authored none of the accepted mathematical modules and is separate from both the original contribution authors and the parent integrator. This is a separate-agent review, not a claim of a separate GitHub account or external human peer review. All remote operations were read-only. The parent owns publication and integration.

## Exact source and historical boundaries

The source acceptance target is head `cd11afd68833051c81051df22573e8827ab6b671`. Its published mathematical checkpoint is `5923015f86eb1ef898becd77ce2ee328ff338b69`; all nine registered mathematical source blobs match both commits. After the original dependency merge `43259106e755d501ca88819f373e0a6c1bff3f05`, this contribution adds four flat mathematical modules, one registry, and 60 contribution/evidence files. No mathematical dependency is modified by this contribution. The five inherited source blobs also match the initial main supplied for this review, `fa3921e58556250b1a6efd30af603fb65a9d9fbc`.

A three-dot comparison with that main has multiple merge bases and can display inherited Agent5 changes from a single selected base. This review records all merge bases and the contribution's precise delta after its dependency merge; it does not reinterpret already present inherited work as new PR113 research. The parent integrator separately checks the actual current-main merge result.

The review read the applicable `AGENTS.md` and `proofs/PUBLICATION_POLICY.md`; the complete four new mathematical sources; the canonical verifier, supplemental strict replay, registry and existing audit; the new public endpoint contracts; the relevant original arithmetic and finite-list definitions; the original inverse note; and the retained semantic/development records. The complete selected mathematical closure is independently replayed below. Source snapshots are exact bytes, not transcriptions.

The manuscript is `persist_inverse_notes.txt`, sections 1-3, Git blob `ecd101823b261fdac15d185fea963d9c9f16c601`. It distinguishes the numeric map `S(q)` from the subsequent pair-word map `G(q)`. The formal contribution preserves this distinction. The other sections of that retained note remain historical context and are not additional formal endpoints of this package.

## Original numeric meanings

`Lychrel196.reverse10` is the ordinary decimal reversal implemented through `reverseFuel`; `reverseFuel_correct` connects that implementation to the decreasing decimal recursion. `step n = n + reverse10 n`; `orbit n 0 = n` and `orbit n (k+1) = step (orbit n k)`. The orbit includes time zero and continues after palindromes. `Palindrome n` means the ordinary numeric equation `reverse10 n = n`.

`DecimalDigits.Canonical n d L` asserts positive width, decimal digit bounds inside that width, a positive leading digit, and equality of the finite positional value to `n`. It does not impose a convention on the infinite function tail. Positive value follows from the nonzero leading digit. `columnSum d L i` is the sum of digits at reflected positions within the finite width; `carry` and `output` are ordinary base-ten addition recursions. The last carry is retained as an extra leading digit exactly in the overflow case. Source trailing zeros are permitted and their reversal drops leading zeros numerically.

Agent101's list representation is least-significant-first. `canonicalDigits` imposes bounded digits and a positive last element, hence a nonempty canonical numeral. `natValue` evaluates that finite list, and `digitPairSums` is its finite `zipWith Nat.add` with its reversal. Its list length is preserved. The inherited same-width equivalence relates equal ordinary numeric `step` values to equality of these finite pair-sum lists; it does not identify arbitrary input digit splits or infinite tails.

## Width support

All seven public WidthSupport theorems preserve their intended hypotheses. Canonical width uniqueness follows from the same ordinary integer occupying a unique interval `[10^(L-1),10^L)`. In-range digit uniqueness follows from positional value injectivity with decimal digit bounds. The combined theorem explicitly restricts equality to `i<L`; no unproved infinite function equality is introduced.

`canonical_step_width` first constructs the actual canonical output in each of the two terminal-carry cases, then applies width uniqueness. Its exact conclusion is `W = L + carry (columnSum d L) L`. The output is therefore of width `L` with terminal carry zero or width `L+1` with terminal carry one. The existence endpoint supplies these same concrete `output`/`extended` digit functions.

For two canonical sources of widths `L<K` with equal numeric output, the common output width and binary terminal carries force `K=L+1`, short-source carry one and long-source carry zero. This is an ordinary numeric consequence; it does not assume the pair-word state transition is injective.

## Cross-width necessary conditions and profile bound

The six public CrossWidth endpoints derive necessary conditions from two positive canonical sources with `L<K` and equal `step` value. The longer source does not overflow; the shorter source contributes an actual leading output carry of one. Canonical output digit uniqueness equates the two finite result digit lists. The longer source's positive outer coefficient, its zero terminal carry, and its leading output digit one force its outer pair sum to be one. Symmetry then gives units output one. The shorter source has units output one, coefficient at most eighteen, and an actual final overflow; the column equations and reflected outer coefficient exclude one and force its outer pair sum to be eleven.

The shorter width cannot be one: a one-digit source has outer coefficient twice its sole digit, which cannot equal eleven. Thus `2≤L`. Since the two source widths are adjacent, one is even, and the inherited even-width arithmetic theorem gives divisibility of the common numeric output by eleven. Every canonical representation of that output has width equal to the longer input and both leading and units digits one. These are necessary conditions only. The source does not advertise their sufficiency or a decoder for arbitrary targets.

`equal_step_widths_close` applies the adjacent-width argument in either order, or handles equal widths directly. Among any three source lists with the same numeric output, their pairwise-close natural widths must contain an equal pair. The inherited same-width equivalence then gives equality of that pair's finite `digitPairSums` lists. This is precisely the formal at-most-two-profile statement. It does not say there are at most two integer predecessors: many different digit splits can realize the same pair profile. It is also not a bound on inverse branching under the pair-word map or at arbitrary iteration depth.

## Concrete kernel controls

The witness module contains 18 public theorem endpoints and a supporting `literalDigit` definition. The finite digit function is `n / 10^i % 10`; its general bound is proved. The numeric reversal claims are transported through canonical positional representations and the existing `reverse10_value` bridge, avoiding expansion of a large fuel numeral as an external computation.

The controls establish canonical widths six and seven for `200799` and `1098900`, respectively, and width seven for the common output. Their actual reversals are `997002` and `98901`, and both sums equal `1197801`. The target reverses to `1087911`, so it is not a palindrome. The exact finite low-to-high pair profiles are `[11,9,7,7,9,11]` and `[1,0,18,16,18,0,1]`; their terminal carries are one and zero. These are realizations of the profiles and output already in the retained note, not a new discovery claim about the profile counterexample.

The boundary control proves canonical widths two and three for `29` and `110`, with common palindromic output `121`. This reaches the minimum permitted shorter width and shows that the necessary conditions do not require a nonpalindromic target either. The finite `decide` proofs are ordinary kernel-checked Lean proofs; no `native_decide` or unchecked arithmetic oracle is accepted.

## Positive palindrome-image classification

The target hypotheses are an actual canonical representation `Canonical P e W` and ordinary `Palindrome P`. The canonical hypotheses imply `P>0` and `W>0`. The exact image condition is:

```lean
(∃ n, 0 < n ∧ step n = P) ↔
  W % 2 = 0 ∨ e (W / 2) % 2 = 0
```

Sufficiency uses the existing `realizingDigit e W` construction. Target palindromicity supplies finite reflection symmetry. If a position is self-reflected, either the even-width alternative excludes its existence or it is the middle position with the stated even coefficient. The target's positive leading digit also gives a positive units digit by symmetry, so the realizing construction has a positive lead. Its pair-column word equals the target digit word exactly inside the width. Since those coefficients are at most nine, every carry, including the terminal carry, is zero. The positional numeric bridge then proves that this positive, same-width source has actual `step` equal to `P`.

Necessity is checked for an arbitrary positive predecessor, not merely the constructed one. Its canonical digits exist. With no overflow, the inherited exact palindrome criterion forces all carries zero, so an odd-width central result digit is twice the actual central source digit and is even. With overflow to an odd-width target, the source width is even. The two central source columns are distinct reflections and therefore equal; each is zero or eleven by the exact overflow-palindrome criterion. The carry recurrence makes the target middle digit zero or two. The proof does not mistakenly assume an even self-reflected source center in this even-width case. Canonical width and digit uniqueness transport these facts to the supplied target representation.

The image iff includes width-one targets; exactly the positive even one-digit palindromes satisfy it. The separate first-hit-at-one theorem deliberately requires `2≤W`. At these widths, `realizingDigit e W 0 = e 0 - 9 = 0` by natural subtraction and the target digit bound, while the source lead is positive. The source is therefore nonpalindromic. Its first iterate is `P`, and all `k<1` reduce to time zero. The final iff adds no unstated assumptions and correctly includes time zero in the first-hit condition. The width-one restriction is substantive, because a positive one-digit predecessor is already a palindrome.

No endpoint claims arbitrary-time termination, infinite avoidance, an optimal count, decimal Lychrel existence, or resolution of 196.

## Verification gap and the audit-only repair

The historical canonical verifier `proofs/verify_project__214bf7673efe116b.py` has SHA256 `c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a`. Its actual mathematical and audit commands omit `--trust=0`. The contribution accurately preserves this fact and supplies a second, explicit-trust-zero full replay. That supplemental replay changes the invocation flags but deliberately reuses the exact old generated audit.

Both historical audits check every selected-origin theorem and reject safe custom project axioms. However, their fallback branch skips safe definition and opaque declarations. Neither historical run therefore satisfies the additional complete safe-definition/opaque requirement of this integration review. This is a verification-coverage gap, not a demonstrated mathematical counterexample or a reason to relabel the historical theorem-audit PASS as a failure.

The current reviewer fixes the gap only in separately attributed verification infrastructure: `replay-complete.py`, `auditor-support.py`, and the generated `CompleteIndependentAudit.lean`. The scanner and exhaustive audit template are reused from the fully inspected Agent9 runtime auditor. The canonical verifier, strict-replay source, prior audit, receipts and all mathematical sources remain byte-for-byte unchanged. The new driver checks the fixed head's Git blob for every module against both the exact supplied source bytes and the registry, validates exact import closure, masks comments/strings before forbidden-token checks, and creates an absent output directory with an empty project-object directory. It performs one complete fresh nine-module build, with explicit `--trust=0 -j1 -DElab.async=false` in every compile and audit command.

The new audit prints literal types and transitive axioms for all 38 public theorem endpoints. It then inspects every declaration by its originating module, including private/generated theorem constants and all safe definitions/opaques. It rejects unexpected safe project axioms and any transitive axiom outside `propext`, `Classical.choice`, and `Quot.sound`. All nine expected origins must be visited. Unsafe compiler implementation constants are reported separately; an unsafe implementation axiom is not accepted as a safe proof or definition dependency. The machine receipt and full log state the resulting counts without treating them as counts of independent mathematical discoveries.

## Historical evidence and provenance

All 59 direct package-manifest entries were independently checked. The lossless verification archive is 146,656 bytes with SHA256 `81ac54ac2a46ca63fdd13abcc7017963436d4ee8c45c746837383361a5d685d4`. Safe extraction rejected absolute paths, traversal, duplicate members, links and nonregular entries. All 46 members, totaling 819,489 original bytes, matched their recorded names, lengths and hashes. Both inner file manifests and all 62 entries of the scope105 evidence manifest were checked. The directly readable canonical and strict receipts exactly match their archived originals.

Cross-width attempt001 is a retained failure: it had a missing arithmetic normalization and an unknown tactic, with failure-time `sorryAx` output. Attempt002 succeeds. Witness attempt001 has redundant tactics after rewriting already closed goals, including a failure-time `sorryAx` report; attempt002 succeeds. All three palindrome-image development attempts are recorded successful, followed only by a documented docstring correction before freezing. These distinct histories are preserved; no failed snapshot enters the accepted source registry.

The original canonical report remains `PASS` for its historical invocation, and the original supplemental report remains `PASS_EXPLICIT_TRUST_ZERO` with theorem-only coverage. The legacy canonical report's author field is not attributed to this reviewer. Historical specialist-review authorship is kept separate from this independent review, whose reviewer authored none of the four mathematical sources.

The known runtime is official Lean 4.19.0, release commit `6caaee842e94`, with executable SHA256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. Its existing installation provenance is retained, and the new driver hashes the executable, root runtime objects and shared libraries before and after the run. The old installation tar archive is absent; no fresh release-archive verification, independently published checksum, or source rebuild of Lean's standard library is claimed. No author or historical-reviewer project object is reused.

The scratch filesystem reported no available space during preflight, so compilation was held until the parent's explicit GO and then run in the approved session-specific memory-backed directory. Only previously excluded, reproducible PR109 compiler objects were removed after checking its sealed evidence archive; no original research source or log was deleted. Minimal source extraction, exact Git-object comparisons, complete logs, audit-only changes, manifests and historical failures are all retained for publication by the parent.
