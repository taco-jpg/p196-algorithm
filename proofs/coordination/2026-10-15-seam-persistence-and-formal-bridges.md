# Shared seam obstructions, all-base formal reflection, and rotated clock bounds

Integration parent: `fbbef30681848aff9e4ff3d34fc01b9ca2167f9d`.
This checkpoint builds on the external `e521255` intrinsic-seam and
finite-seed work, and preserves both streams' earlier results and failures.
The [contribution index](../contributions/SEAM_PERSISTENCE_AND_FORMAL_INDEX.md)
links the exact proofs, compiler logs, controls and independent reviews.

## What the construction stream can reuse

The external intrinsic theorem already characterizes decimal active-seam
existence by an adjacent high coefficient followed by 9, proves singleton
partitions maximize every defect, and gives the shorter annihilation family
`(10,9^k,10)`. We read and independently reviewed those exact sources and the
finite-seed obstruction proof. This is source/mathematical review, **not a
new independent compilation of the external 31 theorems or replay of its
finite-seed catalogs**. Their earlier 42-theorem module has a separate fresh
audit in the preceding checkpoint.

Our complementary all-base family uses independently canonical even-width
blocks `B=(b,b)`, `H=(b-1)^(2m)`, for every `b>=3`, `m>=1`.
Its active-seam mass is `2m`, yet the nonpalindromic seed
`b^(2m+4)-b^(m+2)+b+1` has first palindrome time exactly two. Every partition
defect vanishes after one update. Thus arbitrary current seam mass supplies
no temporal renewal guarantee. The shared decimal annihilation result is
explicitly acknowledged as independently convergent work.

More generally, for a canonical symmetric word with `b-1<=q_i<=2b-2`
and `q_0>=b`, the second actual output is palindromic exactly when
`q_(i-1)+q_i<=3b-3` at every adjacent pair. The updated word is explicitly
`(r_0,r_0+r_1,...,r_(L-2)+r_(L-1),r_0)`, where `r_i=q_i-b+1`.
The all-base statement is written and independently reviewed; its decimal
specialization, including width one, is now a complete ordinary-integer
Lean theorem with threshold 27. A separate decimal formal theorem proves
the sufficient range 9 through 13 and distinguishes first positive time
one (constant 11) from two. The 185 all-base arithmetic controls and their
independent replay are retained, alongside the all-parameter proof.

## Exact scope of the available one-step certificates

Fifteen new Lean declarations prove that any two nonempty positive-terminal
intervals with unequal isolated final carries certify a nonpalindromic
actual decimal output. Intervals may overlap or be nonsymmetric; a numeric
orbit bridge uses the current actual width. Twelve further declarations
prove the exact existential reduction: such intervals exist iff the word
contains a positive low coefficient and a high coefficient, iff two
singletons already witness the mismatch.

The written all-base reduction and examples establish strict containments:
active-seam detection implies interval mismatch, which implies one-step
safety. Longer intervals do not create a stronger existential detector.
None of these sufficient conditions is asserted to persist.

## All-base raw reflection is now formally connected to physical width

The new four-module package has 58 declarations, with 67 transitive axiom
audits including nine earlier prerequisites. It proves the integer raw
reflection identities, computes reset carries by division/remainder,
includes all isolated terminal carry slots, and derives the actual canonical
width, digit bounds, positive leading digit and value. For every base at
least three, raw symmetry at that actual width is equivalent to ordinary
normalization symmetry. One unequal reset/actual outgoing carry certifies
a nonpalindromic normalized output.

Reset flags represent arbitrary consecutive partitions. There is no
separate nested-block-list representation theorem in this package, and the
seam polynomial/mass identity retains its written scope. The four-module
package itself does not assert an ordinary-integer iteration interface.
Earlier failed drafts and the successful 61-audit intermediate checkpoint
remain available; the final report contains all 67 audits.

The separately reviewed `base-reverse-add-formal` module now adds the
one-step ordinary-integer interface: 15 new declarations, with 82 audits
including the preceding prerequisites, derive the symmetric pair word from
canonical digits, identify its value with `n+reverse(n)`, and prove the
actual canonical output and carry-defect safety. Its odd-base control
preserves the distinction between input and output palindromicity. This
closes the one-step representation gap; it is not an iteration invariant.

## Rotations of the scalar clock

The existing numerical hierarchy bounds every rotation of the full sequence
`(4,8,16,7,15,6,13)` at every orbit offset by 98 complete periods (94 at
width at least 14). The new written corollary explicitly checks all start
phases; width-one inputs cannot complete one period.

Thirty-five new Lean theorems prove the actual outer-coefficient transition,
the forced overflow schedule, exact width growth of three per seven steps,
arbitrary phase and offset, width-one exclusion, and a conditional warmup
transfer. The wide-word bound remains an explicit hypothesis. This package
does **not** instantiate the numerical 94/98 hierarchy in Lean. These bounds
concern the full prescribed sequence, not isolated visits to coefficient 4,
and leaving that sequence does not imply a palindrome.

## Replay and next shared obligation

Run the `check.py` in each formal contribution with Lean 4.19.0, following
its README; the scalar runner uses `--lean`, the other runners take the
executable or installation path specified there. All rebuild exact source
dependencies and retain standard-axiom reports. The obstruction's
`check_obstruction.py` and `independent_audit.py` retain the arithmetic
controls; the clock rotation checker reads the earlier certified hierarchy.
`python3 proofs/verify_release.py` checks archive completeness and byte
integrity, not mathematical validity.

The next positive-construction obligation is a condition on the **updated**
word that regenerates a safety witness while excluding the proven two-step
annihilation families. The other stream's finite-seed quantifier obstacles
also rule out the documented extraction shortcuts; their exact restrictions
remain explicit. Our further all-base representation work continues, while
the other stream's unrestricted language and finite-seed construction work
remains complementary. No result here proves an infinite-safe finite seed,
settles 196, or proves decimal Lychrel existence.

## New bounded-language exclusion preserved

While this bundle was staged, the other stream published the
[four-state language exclusion](2026-10-15-four-state-language-exclusion.md)
at `fbbef30681848aff9e4ff3d34fc01b9ca2167f9d`. We read that handoff and
preserve all 98 changed blobs, including every lossless proof part and the
five-state UNKNOWN trace. Its exclusion covers complete deterministic
automata with at most four pair-reading states and eleven arbitrary terminal
predicates. A candidate regular invariant must escape that exact class and
still prove universal safety, successor coverage and nonemptiness. We do not
claim a new independent LRAT replay or all-width proof audit in this bundle.
