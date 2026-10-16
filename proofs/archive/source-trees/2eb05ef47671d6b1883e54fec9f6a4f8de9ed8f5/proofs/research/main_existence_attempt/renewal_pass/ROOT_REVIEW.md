# Root review of the renewal pass

This is an audit record, not a solution of decimal Lychrel existence.
Completed results and outstanding checks are distinguished below. The
final aggregate and byte-hash review record accompany the completed pass.

## Completed gate review

The complete `lean/DelayedOverlapGate.lean` source was read, including its
symbolic carry profiles, finite widths, admissibility conditions, distinction
between actual and redundant words, instantiated integer-valued defect,
and ordinary-decimal representation bridge. Its parameter domain is
r>=1, 1<=p<=4, u>=1, v>=5, u+v<=8. The representation obligations are
discharged rather than assumed as an uninstantiated existence condition.

The new module and a separately generated 49-theorem axiom audit were
independently recompiled. The dependency modules were reused from the
agent's fresh source rebuild after their source copies were checked against
the recorded hashes. This is the exact scope of the root rebuild, not a
claim of a second independent compiler or a second dependency rebuild.
The result is PASS; every audited theorem has only the documented standard
logical axioms. `lean/root_recheck.py`, `root_compile.log`, and
`root_verification.json` retain the reproduction and evidence.

The gate certifies positive times 1 and 2, not time zero. Its formal
non-reuse theorem concerns the original six-core domain defined in that
source. The broader constructive family can permit a second compatible
repair; this does not contradict the formal theorem.

## Completed tail and inverse-ladder checks

The tail proof verifies actual decimal normalization by
D=Q+(x-10)C, then forms paired digits by reflection at the actual output
width. Nonpalindromicity is witnessed by a nonzero digit-difference run
whose length is positive throughout the nonnegative parameter domain.
The ordinary finite boundary cases complete the stated all-r domains.
The independently written polynomial checker is distinct from the affine
run generator. The publishing worker replayed it again from the staged
repository layout; its output was byte-identical.

The initial A->B->C->Q inverse ladder was also read and replayed by root,
including the 11-step tail certificate it uses. The log is
`language/root_inverse_ladder_replay.log`. The later prefix obstruction
and extended D->A link have separate checks in their final artifacts.

## Uniform-inequality correction

Root identified an extra proof obligation in the first draft of the
constructive classification. Two different affine run descriptions can
coincide at a special parameter value. Therefore structural inequality
of their lists, by itself, is insufficient to exclude equality for every
parameter. Finite sample agreement does not discharge that obligation.

The construction worker replaced that inference with a common comparison
routine: align the candidate and target runs using comparisons proved on
the entire parameter domain, subtract their coefficients, and exhibit a
nonzero interval with uniformly positive length for every negative claim.
The exact case table remained unchanged. Superseded source versions and
the correction rationale are retained in
`constructive/superseded_pre_uniform/` and `constructive/ATTEMPTS.json`.
The root separately replayed the corrected classification, composition,
and third-gate scripts; their logs use the `root_` prefix. The final review
record supplies their completed outcomes and hashes.

## Prefix obstruction: independently checked arithmetic

The language worker's new obstruction was independently derived before
formalization. For an output beginning in pair coefficients (2,12,4),
overflow would require input outer coefficient11; the second output pair
would then be at most11, contradicting12. Without overflow, the first
three output equations force input pair coefficients (1,6,2).

Conversely, output outer coefficient1 forces overflow and input outer
coefficient10. A second output coefficient6 then forces the next input
coefficient to be5 or14, according to the incoming carry at the high end.
The next high output digit is at least4, so the third output pair cannot
equal2. Short widths and reflection/center cases must be discharged in
the final written and Lean statements; they are not silently assumed away.

This blocks two-step ancestry of the (2,12,4) cylinder. It does not, by
itself, bound every possible inverse branch of the later Q family. The
reports must keep that distinction even if a further exact preimage
calculation yields a stronger result.

The complete prefix module has now been read and independently recompiled,
with all 16 theorem declarations audited. Its ordinary-decimal bridge
excludes this full-column prefix in every positive integer orbit at every
time at least two. Short widths and centers are discharged in the source.
The separate language checkers for the symbolic inverse ladder and local
prefix certificate both replayed successfully. The complete exploratory
archive checker also replayed successfully, including 2,659 safe inverse
edges and the explicit ancestor outside the selected A cylinder. Its log
is `language/root_exploration_replay.log`. This counterexample prevents
promoting the selected-cylinder obstruction to a universal ancestry bound.

## Completed generalized-gate and archive review

The full written carry proof in `constructive/STATUS.md` was read, including
all three core groups, the smallest allowed spacers, the common-overflow
transport law, the four actual consecutive repairs, and the time-six
outer-coefficient obstruction. The original six-core formal domain is
distinguished from the enlarged twenty-core written theorem.

The three corrected symbolic classification programs replayed successfully.
The additional independent integer formula checker also passed: 2,800
first-gate controls, 3,400 overflow controls and 137 double-return controls.
All 5,204 symbolic comparison records are preserved in three deterministic
gzip archives. Their decompressed hashes match the witness-stream hashes
in the reviewed classification results. This retains the actual negative
witnesses, rather than only their counts or checksums.

## Completed seam-algebra and local formal review

The arbitrary-list normalization identity `D=E+(x-10)K` was independently
derived from the actual-minus-isolated outgoing carry polynomial. The
all-nine terminal case, raw addition at shared columns, the actual final
reflection width, and the distinction between formal component pairing
and ordinary canonical components were checked in the report and source.
The exact mass loss is 18 times the number of active outgoing-carry
differences. The all-word proof is written; its 2,737 finite controls were
independently replayed and include 1,767 actual canonical integer controls.
The complete input and response stream is retained losslessly.

The entire `lean/incoming_carry/IncomingCarrySensitivity.lean` source was
read and independently recompiled, together with an independently generated
audit of all 28 declarations. It proves the actual arbitrary-offset local
carry identity, including first-non-nine and whole-nine cases. The fresh
dependency rebuild belongs to its original verification; root reused those
source-hash-checked dependencies while recompiling the new module and audit.
Neither build claims a Lean proof of the complete concatenated polynomial
theorem or a recurrent reset.

An additional review challenged whether the proposed conditional safety
shortcut, symmetric raw E with nonzero K, had any canonical instance.
The zero-overflow premise was shown impossible immediately. Root then
independently derived and checked the overflow prefix-imbalance recurrence:
`q_i=10C_i+R_i+9S_i`, with both endpoints of S zero. The local remainder
bound forces S to be 0 or 1, and a value 1 cannot return to zero. Hence
all S vanish, C is symmetric, and every q_i is 0 or 11. This proves the
shortcut's premise impossible under every partition of a canonical whole
pair word. The stronger equivalence, raw E symmetry iff actual output
palindromicity, follows by applying the same classification to the
single-block partition. The full proof in `seam_audit/METHOD_AND_PROOF.md`
was read; nonsymmetric counterexamples delimit its exact domain. The main
seam identity does not rely on the shortcut. Its earlier uninstantiated
paragraph is preserved in the exact report snapshot.

Root extracted the positive corollary: nonzero K alone implies a
nonpalindromic ordinary output. Its shorter direct proof uses the two
palindrome-predecessor classes: all-small inputs never create a carry,
while 0/11 inputs contain no nine run. Thus either palindromic class forces
K=0 for every partition. The seed 99900 and partition (9,9)|(18)|(9,9)
give the actual nonzero mask x^3+x^4. This is a concrete safety certificate;
it is not a proof of persistence. The corrected proof and handoff retain
that distinction. Root separately replayed the local arithmetic certificate
and all 58,221 archived short partitions, using the independent decimal-
conversion and polynomial-division checker.

Root additionally replayed the positive checker on all 2,495 canonical
active-seam cases, recomputing the mask from actual prefix carries and
checking the literal ordinary integer output. Its log is
`seam_audit/root_positive_safety_replay.log`; the entire case stream is
retained. This finite replay checks the implementation, while the
all-width proof uses the exact predecessor classes.

## Completed full raw-symmetry and positive-safety formal review

The complete final `RawSymmetryObstruction.lean` source was read. Its
arbitrary Boolean cuts represent all finite block partitions; the local
interval theorem connects reset carries to normalization of actual
blocks. The raw coefficient bridge includes placed terminal carries and
derives value conservation. Both actual output-width cases are covered.
In the overflow branch the endpoint condition is derived from the raw
reflection equations and zero extensions, not left as an uninstantiated
arithmetic premise. The no-overflow branch uses the existing bounded
symmetric-word injectivity theorem with all of its bounds discharged.

The positive theorem `numeric_nonzero_defect_safe` has no raw-symmetry
hypothesis. It directly applies the carry-agreement result for the two
palindrome-predecessor classes to any nonzero actual-minus-isolated
outgoing carry. The concrete seed 99900, its next output 100899 and its
nonzero defect at column 3 are kernel-checked instances. No indefinitely
recurring defect or positive invariant is assumed or concluded.

The fresh build compiled the decimal dependency, incoming-carry module,
new module and full 42-declaration axiom audit. Root then independently
recompiled the new module and a separately generated full audit, reusing
those freshly built dependencies after source-hash checks. Both passed
and agree on every theorem's axioms; only `propext`, `Classical.choice`
and `Quot.sound` occur. The final source SHA-256 is
`922b660e5b3ac42389cd6ea00885075327d4b44fb315b9cc496e1323890e9c87`.
The corrected auxiliary arithmetic hypothesis and every development
failure remain in the module's report and development archive.

## Shared-repository coordination

Root directly read the other contribution stream's
`proofs/contributions/COORDINATION.md` at commit
`8974c5a84ad38366b34316ee53f15e1da862e018`. It contained proposed gate,
run-erosion and finite-density work, not completed new theorems. The
overlapping tail result was shared at commit
`a7618a13c00c7058ce65f13f2d6b4619800a49e3` with source, certificate and
independent checks. The publishing worker uses fresh-head checks and
preserves the other contributor's exact bytes. Later observed results are
recorded in the final shared checkpoint; no access to a separate chat or
unpublished workspace is assumed.

The later external commit `b7fa911dc4ca943528f5d28b67f3fbd87c9404ca`
contained completed shorter finite-prefix, deterministic density-marker,
gate-lifetime and separation results. Root directly read those reports and
the two new Lean modules, compared their exact source hashes to the
published verification records, and freshly rebuilt all six required
modules. All 24 new supporting declarations passed a complete root axiom
audit. Evidence and the independent build script are in `external_review/`.
The external finite-density replay passed 99,999 exhaustive small inputs,
19,800 endpoint/center inputs, 360 exact refined-run inputs, and 1,856
random-background planted-block inputs. The external separation program
passed all 36 potential transitions, 3,000 block controls and 18 gate
separation trajectories. The counting and limit arguments were reviewed
as written proofs; they are not asserted to be Lean theorems.

The external contribution independently replayed our exact tail certificate
and reported agreement. Its next public request at
`fcc850c32cce32303302a06c4c4cd69e43ae6835` proposed a division of work:
our stream continues generalized gates and language obstructions, while
its stream studies actual post-collision resets for the remaining (1,7)
family. Our response and 49-theorem gate audit were published at
`7c699a370198a3e306524948f468ba319c620b18`. The reusable seam identity and
local formal bridge were developed in response to the separation theorem
and are supplied for that concrete reset obligation. No agreement beyond
these observable repository messages, and no completed reset, is assumed.

The later full external commit `a3914ba08e5facb59699d066fcb69f1bd37b6e6a`
was read at its collision report and finite-family report. Its raw P is
our E, its F is our K, and its common-width target T is distinct from its
component-width target S. Root checked the unrestricted deduction
`G(BHB)=S iff F=0 and e=a`, including the all-nine carry map and the
nonzero central block used to rule out cancellation of unequal widths.
The stronger verbal classification follows: both isolated carry bits
zero, or both outside coefficients at least 10. No positive-gap reset
follows from this polynomial identity.

Root then deduced the new written corollary in
`external_review/COLLISION_SAFETY_COROLLARY.md`: a palindrome predecessor
necessarily satisfies that S-closure, so failure of closure certifies
one safe output. This includes unequal component overflow bits with
zero F. The exact examples were independently computed from literal
ordinary integer steps and pair coefficients; a safe case with closure
is retained to show that the criterion is not necessary. The new
combined corollary itself is not claimed to have a Lean proof.

The language worker independently reviewed the new combined proof and
recomputed all three examples without running the root generator. It
returned PASS and supplied an excluded-domain counterexample showing
that H's positive outside coefficients are essential: B=(11,11), H=(0)
realizes 99022 -> 121121, with zero seam defect and unequal isolated
overflow bits. The fourth control explicitly records the noncanonical
central block; the whole pair word is canonical. Both the assumption
and its counterexample are now retained in the corollary and checker.
The external handoff's proposed seven-step reset is acknowledged as
forthcoming, with no checked reset theorem claimed in this release.

That sentence records the a391 checkpoint. During final integration the
other stream published the actual seven-step bundle at
`6889b717599343b6773d376e728ca5b03cf68527`, followed by the announced
four-return obstruction at `8a42fe14262fee12ce1c8b40bf25e97b94044742`.
The updated review below supersedes the earlier observation that the
conditional seven-step theorem was only forthcoming.

The final external finite-family proof improves its provisional 5079
threshold to r>=5078 because the last checked state may have zero gap.
Root checked the monotonic spacer-loss indexing, the zero-gap/no-overflow
transition case before the endpoint, and the restriction to outputs
through time 10000. The full 10,000-record trace audit is the external
stream's completed verification, not a root replay. Its five lossless
trace parts are preserved as existing Git objects with their published
sizes and SHA-256 inventory; connector size limits prevented a local
download of those binary parts. The final receipt distinguishes exact
Git-object preservation from local trace-byte verification.

Our positive active-seam handoff was then published atop that external
bundle at commit `e30848f6f4d40b360096f469b5c1c0dae175e4be`, making the
criterion available to the other stream before the full release. The
final publication also supplies the stronger combined closure-failure
corollary. These are substantive derivations from each other's actual
published work; all-time existence remains open in this checkpoint.

## Independent reconstruction of the latest seven-step obstruction

Root read the new exact conditional-return proof, its full padded-middle
formulas and safety tests, the formal-boundary scope report and both
coordination updates. The announced obstruction's complete certificate
was not yet in that observed external bundle. Root therefore constructed
its own complete six-prefix necessary graph directly from the boundary
formula. The generator imports no external graph implementation.

All 48,013 vertices, both possible deeper carry bits at each vertex, and
all 61,731 accepted labeled edges are retained. A separate implementation
uses literal base-ten integer evaluation and decimal extraction to verify
all 96,026 controls. It checks exact rank recurrences at every vertex,
not just the claimed maximum or a hash. All accepted edges strictly
decrease rank; the maximum rank at phase zero is 26. The complete 128-word
three-column control calculation is independently checked as well,
including all four successful schedules and every intermediate prefix.

The language worker independently derived the whole-word inclusion
argument, including overlap of six-column windows at widths 6 through 11.
The deeper control is the actual carry at L-6; the earlier return control
is at L-3 and is obtained after three columns of that upper normalization.
They are not conflated or assumed independently realizable. Actual
normalization supplies a permitted graph edge, even when overlapping
windows impose extra consistency restrictions. Hence four seven-step
returns require an impossible 28-edge phase path.

Root independently replayed the sharp external example using the ordinary
integer seed 4401198500000 and literal string reversal. The first three
returns are safe, the phase path has exactly 26 transitions before its
first deviation, and all 28 recorded positive outputs remain safe. Every
integer and pair word is retained. Leaving the phase graph is not
identified with reaching a palindrome.

The resulting full written theorem and finite certificate independently
corroborate the other stream's announced all-width obstruction. Neither
the graph's rank computation nor the complete new theorem is claimed
to have been checked in the Lean kernel by this reconstruction. The
135-declaration local formal count and the separate 24-declaration
external rebuild count are unchanged.
