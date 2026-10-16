# Decimal Lychrel research: carry encodings and inductive certificates

**Status: no proof or disproof of decimal Lychrel existence, and no proof that
196 is Lychrel.** This package contains exact reformulations, checked partial
theorems, and reproducible constructive searches. It makes no novelty or
publication-readiness claim.

## Latest return and correlation pass, 14 October 2026

The main existence claim remains unproved. New written results establish an
arbitrary-motif law up to the actual finite zero-gap collision, then show
why its natural adjacent-parameter return fails. Full-word observation
languages through depth four have independently checked empty safe kernels;
this excludes the specified tables, not all possible invariants. Exact
finite ensembles expose missing joint-distribution assumptions in proposed
probabilistic deductions. None supplies all-time palindrome avoidance.

See `main_existence_attempt/return_pass/RETURN_PASS_STATUS.txt` and the
branch reports beside it. New work is written mathematics and executable
integer certificates; the previously checked Lean theorem is unchanged.
Earlier pass descriptions below are preserved as historical context.

## Previous proof and construction pass, 14 October 2026

The exact uniform decimal digit-sum theorem is now fully formalized in Lean
4.19.0. Define E(0)=0, E(1)=1, and
E(M)=5*(2*(M-1)*E(M-1)+2*M-1) for M>=2. For every n>0 and every B,s,
some t in [s,s+E(2B)] satisfies S(T^t(n))>B. The bound is independent of
the initial number, its width, and the starting time. This includes 196,
but does not prove palindrome avoidance.

Nine new source modules and the unchanged standalone dependency were compiled
from source and axiom-audited. The final theorems use only Lean's standard
logical axioms; no admitted proofs, custom axioms, or native computation
oracle is used. Exact finite-profile isolation and the numeric embedding
are proved, not assumed. The eight-page manuscript now records this scope.

A new exact thirteen-step collision component increases digit sum by 126,
but its repeatable family return is missing. An independent audit rules out
the specified moving-front potential criterion at every finite state size.
Inverse counting supplies a length-16 obstruction to one proposed universal
contraction. None of these branches supplies a finite Lychrel witness.

The complete current report is
`main_existence_attempt/smart_pass/SMART_PASS_STATUS.txt`.
Formal statements, logs, hashes, and reproduction are in its `uniform_lean/`
subdirectory. Earlier checkpoints below are retained as historical context.

## Historical boundary pass, 14 October 2026

`main_existence_attempt/boundary_resume/BOUNDARY_RESEARCH_STATUS.txt` records
that pass. The previous unresolved936 boundary problem is now excluded
for **every finite width and every temporal period** in the prescribed
alternating8/17 construction. An exact eight-graph reverse-language
certificate, with1,940 vertices and7,442 edges, has independent rank and
projection checks. Root's separate arithmetic replay imports no search
code and verifies all52,520 raw edges. A finite-state argument also excludes
an indefinitely valid boundary of any one fixed width without an assumed
temporal period.

A supporting Lean exclusion has compiled for the explicit carry transducer.
Its finite certificate checks use `native_decide` and therefore
`Lean.ofReduceBool`; its generic logical soundness proof is separate.
See the final files under `main_existence_attempt/boundary_resume/lean/`
for exact scope, arithmetic correspondence, and reproduction. This does
**not** prove decimal Lychrel existence or settle196.

The same method excludes 76 of 190 periodic bulk motifs for a second
overflow clock. Constructive forward/backward searches exclude the
specified 525 exterior through width 17, and all 334 catalogued recurrent
length-three motifs through width 14, allowing arbitrary temporal periods.
Larger-width existence remains unknown in those searches. Exact exclusions
and search limits are distinguished in the current status. Earlier sections below
are preserved historical checkpoints; their arbitrary-width UNKNOWN
statement for this particular936 exterior is superseded by this result.

## Historical construction and conditional-invariant pass, 14 October 2026

`main_existence_attempt/COLLISION_AND_CONDITIONAL_STATUS.txt` records the
previous work. **No main existence proof or finite Lychrel witness was found.**
Exact safe center components now support a concrete conditional family in
periodic936-type blocks. Its necessary finite exterior is missing. All12
bulk variants have checked centers; exhaustive bounded reachability excludes
the specified exterior templates through prefix width72. Searches with
20million raw states and3million temporal-symmetry orbits remain UNKNOWN
for arbitrary width.

A digit-sum congruence rules out the earlier525 family at period24, and an
acyclic carry graph rules out the9/18 alternating outer branch at every
period. A corrected safe parametric family regenerates long18 bands in two
steps, but does not return to itself. A checked LRAT proof excludes genuinely
conditional XOR scores; the reset-map extension and any-seed conditional
threshold search remain unresolved. All these conclusions have explicit
scope. None is a new Lean existence theorem or a novelty claim.

## Resumed existence-targeted pass, 14 October 2026

`main_existence_attempt/RESUMED_STATUS.txt` gives the exact new results.
The rank-free finite-seed encoding repaired the previous search bottleneck.
The resumed one-tile search preserves **70,361** checked exclusions; the
adjacent-context search preserves **1,154** concrete, replayed derivations.
Both ended **UNKNOWN**, as did the direct universal safety-and-closure
solver. None produced a nonempty safe closed grammar or a finite witness.

An exact group-presentation certificate rules out the specified unconditional
one-row group-score invariant for every group, including every automorphism
update. The independent replay uses only group cancellation and unit
relators; it has also been rerun by Root. A separate Laurent-polynomial
certificate excludes the corresponding scalar score over every field.
The finite-defect construction was checked through 128 symbolic updates for
every parameter m>=256; it still supplies no recurrent safe family.

These are scoped computational and written results, **not a proof of the
main theorem or a new Lean existence theorem**. No novelty claim is made.
All resumed searches have finished. Earlier results below remain preserved.

## Latest existence-targeted pass, 14 October 2026

`main_existence_attempt/STATUS.txt` records the new searches and exact
remaining gaps. The direct and counterexample-guided all-length language
searches ended **UNKNOWN**, including an adjacent-context refinement.
No positive invariant or finite Lychrel witness was obtained. A written,
independently checked argument excludes all constant positive scaling
factors for the unconditional additive carry-tile ansatz on 196; this
does not settle 196. A two-step repair of the former ninth-step digit-block
failure still does not close into a recurrent family. No new Lean proof
was added. All searches in this pass have stopped.

## Prior continuation: uniform digit-sum escape, 14 October 2026

The strongest written result gives an explicit digit-sum escape time
depending only on the base and threshold, independent of the positive
starting integer, its width, or the starting time. For base b and threshold
B >= 1, every block of E_b(2B)+1 consecutive iterates contains a digit sum
greater than B. With kappa=1+ceil(log_2 b), the bound is E_b(1)=1 and
E_b(M)=kappa*[2(M-1)E_b(M-1)+2M-1]. The complete proof is in the eight-page
`continuation/UnboundedDigitSums.pdf`, with separate audits in
`uniform_effective_audit.txt` and `uniform_escape_audit.txt` under the same
directory. This uniform result is **not yet formalized in Lean**.

The standalone Lean 4.19.0 file `continuation/LychrelDigitSums.lean`
(`import Std` only) proves unbounded decimal digit sums on every tail and
an explicit escape bound that still depends on the initial decimal length.
Its principal declarations are
`DecimalUnboundedMass.digitSum_unbounded_after` and
`DecimalQuantitativeMass.digitSum_escape`.
All 61 added public declarations compiled and were separately axiom-audited,
including twelve quantitative declarations added in this revision.
Only `propext`, `Classical.choice`, and `Quot.sound` occur. The final theorem
has no unproved local carry-propagation premise. The written general-base
extension and sharp decimal bound liminf D_N/sqrt(N) >= 3/4, where D_N is
the running maximum, have separate audits but are not Lean theorems.
All orbit statements continue iteration after palindromes. The audits are
AI-assisted internal checks, not external human peer review.

This rules out the previous fixed-C moving-wall proposal for every finite
C: its all-time conditions would force constant digit sum. Exact safe
renewal families with increasing C were also constructed, but their attempted
repetition fails by a proved symbolic obstruction. There is still no decimal
Lychrel witness, proof for 196, or disproof of decimal existence. Neither
pointwise divergence of digit sums nor publication novelty is asserted.

`continuation/LychrelContinuationUpdate.txt` gives the complete scope,
reproduction commands, literature limitations, the earlier ten Astra Max
tasks, and four follow-up assignments. `continuation/verification.json` records the final source hash and
audit status. From the archive root:

```sh
cd continuation
lean -o LychrelDigitSums.olean LychrelDigitSums.lean
LEAN_PATH=. lean ContinuationAxiomAudit.lean
```

The older base `Lychrel196Research.lean` is preserved. The continuation
standalone includes that current base followed by the five new source
modules. Earlier reports below are historical records; their unclosed
fixed-C target is superseded by the new impossibility consequence.

## Previous Astra research pass: ten distinct tasks

`AstraResearchUpdate.txt` records the current pass and its exact limits.
`ExactLengthPalindromes.pdf` is a five-page proof note with its LaTeX source.
The `astra_*` files contain the ten task reports, source code, independent
audits, and computation records. All ten tasks used Astra with maximum
reasoning effort; at most six agents ran concurrently.

The main completed paper theorem constructs palindromes of every sufficiently
large compatible exact length in every residue class of an arbitrary fixed
modulus. Consequently no nonempty palindrome-free forward invariant can be
described solely by a fixed residue and exact digit length. This theorem has
a written proof and an independent mathematical audit; its all-moduli
construction is **not formalized in Lean**.

The current Lean file adds 33 completed theorems: 25 arithmetic/orbit results
and eight correlated-column results. In particular,
`AstraModular.orbit_mod11_eq_zero_of_six_le` proves that every positive orbit
is divisible by 11 from time six onward, and
`AstraModular.six_step_bound_sharp` proves the bound sharp using seed 100.
`AstraModular.large_width_compatible_residue` supplies actual arbitrarily
long orbit states meeting both residue compatibility conditions.

Reproduce the formal checks with Lean 4.19.0:

```sh
lean -o Lychrel196Research.olean Lychrel196Research.lean
LEAN_PATH=. lean astra_root_axiom_audit.lean
```

The imported sidecar `astra_lean_modular.lean` preserves the same modular
proofs under its original namespace `DecimalModular`; the integrated copy
uses `AstraModular`. The standalone language sidecar imports only `Std`.
The 33 new declarations were all axiom-audited; only `propext`,
`Classical.choice`, and `Quot.sound` occur.

Principal reproducible controls:

```sh
python3 astra_modular_palindrome_builder.py
python3 astra_root_palindrome_dp.py
python3 astra_counting_safe_fiber_certificate.py
python3 astra_spectral_carry_quotient.py
python3 astra_languages_complement_check.py
```

The all-time existence propositions remain unproved definitions. A successful
finite search, a solver timeout, and a checked all-length identity are
different kinds of evidence and are distinguished in the task reports.

## Proved results: normalization, reconstruction, and numerical injectivity

The standalone `Lychrel196Research.lean` now has 234 theorem declarations.
It compiles with Lean 4.19.0 using `import Std` only. The complete build and
new axiom audit are recorded in `astra_integrated_lean_check.log` and
`astra_root_axiom_audit.log`. Its SHA256 is
`f8950d138fa4231b536059e2334d36b6496de3d25a806f4cf3925941aa05144c`.
There are no proof holes, custom axioms, or native-decide assertions.
The older build logs and `CarryWordsResearch.pdf` document prior passes.

1. **Every complete first carry word has a same-width positive representative
   reaching a palindrome within four additions. Four is optimal.** This
   extends the earlier non-overflow theorem to every carry trace, including
   leading overflow. The theorem compares actual decimal integers and all
   carries, not just a symbolic abstraction. The sharp class has carry word
   `(0,0,0,1,1,1)`; its representative 99500 first reaches palindrome 2102012
   at step four, while every representative in this class avoids palindromes
   for the first three positive-time steps.
2. **Eleven consecutive complete carry words determine the entire initial
   mirrored pair-sum word**, at every finite digit length. They do not
   necessarily determine the initial integer, since digit splits are lost.
   The proof doubles the first differing coefficient at non-overflow steps,
   preserves it at overflow steps, and uses a checked outer-digit potential
   to force enough doublings.
3. **At fixed width, the numerical reverse-and-add value determines the
   entire mirrored pair-sum word.** The new `ReverseAddInverse` section proves
   this algebraically and supplies the bridge to ordinary decimal integers.
   This does not make the next-pair-sum map injective: its fibers can be
   exponentially large. The research note includes the proof and this
   distinction.

Principal theorems:
- `CarryWordTermination.every_positive_integer_has_fast_same_carry_representative`
- `CarryNormalizationSharpness.four_is_optimal`
- `CarryHistory.eleven_carry_words_determine_pair_sums`
- `ReverseAddInverse.symmetric_value_injective`
- `ReverseAddInverse.same_width_step_eq_iff_pair_sums`

## New continuation: complete period-four exterior refinement

`PeriodFourResearchUpdate.txt` records the preceding pass. The all-period
necessary-condition graph drops from25 recurrent components at two outer
pairs to three at three pairs; those three survive four pairs. Completing
the entire exterior gives no expanding safe cycle for exterior widths1..4,
at any temporal period. The width-four check covers11,831,968 recurrent
inputs and3,161,724 retained safe edges. Ordinary integer checks independently
reproduce all full-connector counts at widths1 and2.

This is a bounded-exterior exclusion with an explicit all-core-length proof,
not a decimal existence theorem. New larger-boundary candidates reached
solver timeouts or graph caps and remain unresolved. The concrete graph
calculation is not Lean-formalized; the canonical Lean source is unchanged.
Sources, results, and independent checkers use the `next_period4_*` prefix.

## Latest existence attempt and additional Lean theorem

No decimal existence witness was obtained. The new namespace
`DecimalWidthGrowth` proves, for every positive decimal seed and every step t,

    t + 4 L_0 <= 4 L_t + 4,     2 L_t <= 2 L_0 + t + 3,

where L_t is the actual decimal width. For 196 the constants improve to

    t + 11 <= 4 L_t,           2 L_t <= t + 7.

The upper bound uses the pre-existing outer potential; the lower bound uses
a second exact finite potential. Both are bridged to ordinary numeric
iteration and kernel checked. Neither implies palindrome avoidance.
See `exist_count_notes.txt` for a proof and for the precise missing estimate
in a possible counting argument.

The new `exist_*` sources pursue positive constructions using constant cores,
period-three and period-four cores, arbitrary overflow schedules, multiple
linearly growing runs, and tile languages with time-dependent constraints.
The strongest new complete graph result excludes every period-24/gain-9
uniform-core pump, at every finite exterior width; 1,077 overflow clocks were
independently replayed. Other exact graph searches exclude specified bounded
exteriors for every temporal period. Solver timeouts remain UNKNOWN.

The final period-four search produced genuine center-compatible components
also compatible with two outer digit pairs. Four representative clocks still
failed the complete exterior equations. This does not exclude every cycle
in the surviving strongly connected components. The affine-run checker
rediscovered a known binary expanding family, but found no decimal family.
The graph computations and the binary control are not formalized in Lean.

`ExistenceSearchUpdate.txt` distinguishes all-time Lean theorems, exact finite
graph results, solver-reported UNSAT, and incomplete searches. The archive
contains the new source, notes, result data, CNF encodings, and solver logs;
compiled binaries and runtime dependencies are not bundled.

## Further constructive work and exact obstructions

The `persist_*` files continue the search. A concrete 29-pair exterior reaches
a neutral pair-sum-9 band under an 11-step clock with four overflows. An
independently checked finite graph certificate excludes every finite periodic
center behind this particular interface, for all return periods 11k and all
center widths. Run `python3 persist_exterior_temporal_verify.py`; its two
invariant graphs have 47 and 73 vertices. The supplied Lean graph lemma is
only a generic proof skeleton: the concrete decimal certificate is not
instantiated in Lean.

A growing, nonperiodic center escapes that obstruction alone. Exact digit synthesis
found center `689689997999`, which preserves the required interface for 26
steps before its interface fails. Ordinary integer arithmetic and the independent spatial
transducer both validate its two complete 11-step returns. A separate width32
counterexample disproves a proposed one-return shrinking rule. The repaired
two-return argument is stronger: exact finite graphs force compensated
neutral-pair emissions. A final additional certificate gives a strictly
decreasing nonnegative integer potential, so no appeal to eventual cycles
is needed. Thus this particular neutral interface cannot support
any finite core forever, even one allowed to grow and change. See
`persist_neutral_interface_exclusion.txt`, `persist_wake_notes.txt`, the
`persist_wake_eroder_*` checkers, and `persist_root_compensation_check.json`.
Run `python3 persist_wake_eroder_check.py --all` to reproduce every finite
emission certificate. The concrete combined
theorem is not yet instantiated in Lean; generic graph and width arguments
are supplied separately. It excludes this construction, not decimal Lychrel
numbers. The signed-center map and bounded synthesis
are in `persist_arithmetic_signed_core.py` and `persist_root_signed_sat.py`.

The inverse-map notes prove sharp Fibonacci and power-of-two one-step fiber
bounds. Separately, exact rational dual certificates exclude two unconditional
additive carry-memory score templates for 196. These are supporting results
and limitations of specified methods; none decides decimal Lychrel existence.

`CarryWordsResearch.pdf` and its LaTeX source give a readable research note,
including a new direct run proof of the normalization bound. That paper proof
uses protected runs of nines; the independent Lean proof instead uses closed
37-state and 159-state certificates together with complete numeric semantics.
The work makes no publication-priority claim and does not settle decimal
Lychrel existence. The original conjectures remain unproved definitions.

Appendix B extends the mathematical four-step bound to every even base at
least 10 and every odd base at least 17, with sharpness for positive iteration
times. This general-base extension is proved in prose, not formalized in Lean.

See `PeriodFourResearchUpdate.txt` for the latest continuation and its exact
scope. `ExistenceSearchUpdate.txt` records the preceding constructive pass. `CurrentResearchStatus.txt` and `ResumedResearchStatus.txt`
record earlier checkpoints. The PDF predates this latest update.
Exact graph exclusions are distinguished from bounded UNSAT reports
and unresolved solver timeouts. In particular, no invariant or decimal
nonterminating seed has been obtained.

## Earlier constructive attempt: transfer an infinite orbit between bases

An affine digit encoder `E(d)=a*d+u` preserves the carries in one
reverse-and-add step from base b to base B whenever

    a*(b-1)+2*u = B-1,    a>=1, u>=0.

If c is the incoming carry, k the outgoing carry, and d' the source output
digit, the target output digit is exactly

    D' = a*d' + 2*u + (1-a)*c + (a*b-B)*k.

For binary-to-decimal dilation this becomes

    D' = 9*d' + 8*(k-c).

The defect is supported at carry transitions, which suggests correcting the
interfaces rather than encoding each digit independently. However, a leading
overflow digit is 1 in both bases and must be handled separately. These local
identities do not give a full-orbit conjugacy. The direct centered and dilated
binary examples tested here both eventually reach decimal palindromes.

The new Lean section `AffineCarryEncoder` proves ten exact local carry and
output identities for binary and base-four encoders. The general affine
formula and its proof are in `novel_encoding_analysis.md`.

The boundary investigation gives a useful necessary condition. If decimal
digit growth has bounded deficit from one digit per two steps, the outer
mirrored sum must eventually alternate 8 and 17. A complete finite prefix
graph then forces the familiar eight-step outer-three-pair cycle. Its existence
as a long-lived pattern was already described by Kevin Brown; no novelty is
claimed for the pattern. These graph results and growth arguments are not
formalized in Lean.

The constructive search now includes a 24-step boundary coupled to a
non-neutral repeating interior, and a slower 18-step family with irregular
overflow times. Neither has produced an exterior/center combination that
closes for every repetition count. Timeouts are recorded as unresolved,
not as impossibility results. See `novel_encoding_analysis.md` and
`novel_projective_notes.md` for exact restrictions and results.

## The positive existence strategy

Write a positive integer's decimal digits least-significant first as
`d[0], ..., d[L-1]`, and set `q[i] = d[i] + d[L-1-i]`.
The symmetric word `q` determines the next integer exactly. Its folded form
is `(p,c)`, where `p` lists the outer pairs inward, and `c` is absent for even
length or is the even central sum for odd length. For 196 it is `((7,),18)`.

A valid word has entries from 0 through 18, positive outer entry, and an even
center when present. Every such finite word is realized by a positive decimal
integer. That assertion has a constructive Lean proof.

Let `G` be the exact update of folded words. Let `B` be the following bad
language of palindrome predecessors:

1. Every unfolded entry is at most 9; or
2. The outer entry is 11 and every unfolded entry belongs to {0,11}.

The exact equivalence between membership in `B` and producing a palindrome
on the next numeric step was already established in the earlier formalization.

The desired witness is a regular language `A` satisfying

    A contains a valid finite word;
    A contains no valid word in B;
    G sends every valid word in A back into A.

These conditions give existence by an ordinary induction: realize an accepted
word by an integer n; every iterate's q word stays in A, so every positive-time
iterate of n is nonpalindromic. Therefore n + reverse(n) is a Lychrel number.
If A contains the word of 196, its separately checked nonpalindromic initial
state gives the stronger assertion for 196 itself.

Unlike a fixed repeating-block construction, a regular language can include
arbitrarily long nonperiodic words. There is no assertion that every Lychrel
orbit must possess a regular invariant.

## Why the global check is finite

For a sum q and incoming carry a define

    C(q,a) = (q+a) // 10,   D(q,a) = (q+a) % 10.

The transducer reads the folded word from outside inward. It keeps the actual
low carry a and guesses a high carry b backwards. Reading q, it chooses b_next
with `C(q,b_next)=b`, advances a to `C(q,a)`, and calculates the two output
digits `D(q,a)` and `D(q,b_next)`.

Without overflow it emits their sum. With overflow it emits the low digit
plus a delayed high digit, initially the new leading 1. This delay handles the
change in reflected alignment exactly. At the center it checks that the two
carry reconstructions meet, with the appropriate odd-center column equation.

The Lean proofs establish that passing this center check forces all guessed
carries, including the initial overflow, to be the actual decimal carries.
They also establish the exact emitted-column equations and canonical numeric
representations in both overflow branches.

The final Lean theorem `symbolic_language_seed_sound` proves the whole
symbolic-to-numeric implication, with explicit hypotheses. An admissible seed
q in an exactly closed, safe language gives the specific Lychrel witness
`value q L = sum(q[i] * 10^i, i < L)`. The theorem
`symbolic_language_implies_decimal_existence` packages nonemptiness and
admissibility into the existence conclusion. These hypotheses have no supplied
instance. They are not axioms, and the original conjecture is not assumed.

Safety is a reachability problem in the product of A and the small automaton
for B. Closure is reachability in the product of the transducer and two copies
of A, one for input and one for output. A reachable terminal state accepting
the input but rejecting the output is a counterexample. Exhausting that finite
graph therefore covers all finite word lengths, not a selected orbit bound.

**The Python graph checker and SMT encodings are not themselves formalized in
Lean.** The arithmetic semantics are proved, and finite implementation checks
are supplied. Any future positive certificate must still be independently
checked and connected to a fully verified checker before claiming a completely
Lean-certified existence proof.

## What the searches found

No accepted invariant was found. The exact transducer has 46 reachable states
and 872 labeled transitions. Exhaustive arithmetic validation covers all
75,447 canonical q words of digit lengths through seven, including both
length parities and overflow cases.

For an invariant required to contain 196, the SMT runs reported UNSAT for
pair-reading state counts through eight. Counts nine through thirteen reached
their time limits. An arbitrary-seed direct closure encoding reported UNSAT
at two and three pair-reading states and timed out at four. These are reports
from bounded solver models, not Lean-checked impossibility theorems.
Separate terminal acceptance flags are not included in the pair-reading-state
counts. See `creative_regular_status.json` and the detailed notes.

The state-merging search allows larger learned automata, intersects candidates
with the exact safe-word language, and submits each candidate to the same
universal closure checker. Its final log is included. Rejected candidates and
timeouts establish no general nonexistence result.

## A second representation: a full-word carry coordinate

`creative_global_spectral_notes.md` derives an exact coordinate using
beta = 10 + sqrt(99), where beta + 1/beta = 20. Integer Chebyshev weights encode
the entire q word, rather than discarding its middle or retaining a residue.
The coordinate A, together with length, is lossless. The carry coordinates H
and J record the symmetric and antisymmetric parts of the carry word.

The exact evolution is

    odd input length, no overflow: A_next = 2 A + 198 J;
    odd input length, overflow:    A_next = A - 9 H + 99 J;
    even input length, no overflow:A_next = 2 A + 9 J;
    even input length, overflow:   A_next = 22 A - 99 H + 99 J.

The equations expose a possible positive mechanism: nonzero J certifies that
the next output is nonpalindromic. The unresolved task is a global invariant
or renewal argument that excludes all palindrome targets indefinitely.
Neither persistence nor renewal has been proved. The spectral derivation is
not part of the Lean formalization; its independent implementation checks
85,447 admissible words.

## Reproduce

The standalone Lean file uses only Std and was checked with Lean 4.19.0:

```sh
lean Lychrel196Research.lean
```

No `sorry`, custom axiom, `native_decide`, or external computation supplies a
Lean proof. The existence assertions remain definitions of unproved
propositions. The file includes `#print axioms` audits and the build log.

The arithmetic/transducer validation uses Python's standard library:

```sh
python3 creative_regular_validate.py
python3 creative_global_spectral.py
```

SMT search additionally needs `z3-solver` (tested with version 5.1.0.0):

```sh
python3 -m pip install -r requirements.txt
python3 creative_regular_boolean.py 196 --min-states 8 --max-states 10 --seconds 40
python3 creative_regular_direct.py --objective any --min-states 2 --max-states 4 --seconds 60
python3 creative_regular_merge.py
```

A hypothetical JSON certificate containing `dfa` can be checked and its
finite numeric representative extracted with

```sh
python3 creative_regular_validate.py certificate.json
```

**No such certificate is included.** An empty accepted language does not count
as an existence witness; the validator explicitly checks nonemptiness.

The missing object is concrete: a nonempty safe closed language, a different
inductive family, or a persistent global obstruction. More finite orbit
evidence does not supply that object.

## Earlier sources for context

The one-step palindrome criterion is existing mathematics, not a claimed
discovery here. Relevant earlier discussions include:

- https://mathoverflow.net/questions/117104/status-of-the-196-conjecture
- https://www.mathpages.com/home/kmath004/kmath004.htm
- https://www.mathpages.com/home/kmath312/kmath312.htm
- https://en.wikipedia.org/wiki/Lychrel_number
