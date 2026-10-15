# Independent final mathematical review of the 739 certificate

Reviewer: the independently executing `agent104_final_review` specialist.
Scope: the exact source statements in `ActualAncestry`, `ShortBoundary`,
`ShortChecksBase`, `PrefixInverse`, `FastInverse`, `ActualPrefix`,
`PalindromeBridge`, `PrefixCertificate`, `LongRowsBase`, `FastRowsBase`,
`AllRows739`, `Initial739`, `Short739`, and `Conclusion739`, together with the
ordinary-integer definitions and representation theorems they use from the
pinned `LychrelDigitSums` base.

**Semantic verdict: no mathematical gap or counterexample found in this
source chain. The advertised restricted endpoint is the actual statement of
`ancestry_bound39` and `no_196_739_palindrome` exported by `Conclusion739`.
Acceptance as a complete kernel-checked result is still pending the final
fresh compilation and independent endpoint audit at the time of this report.**
This status will be updated when those executions finish. The numerical
diagnostic below has actually run and passed; it does not replace compilation.

## Exact endpoint and limitations

The two final statements, in namespace `SevenColumnKernel.Finite739`, are:

```lean
ancestry_bound39 :
  ∀ A P t, 0 < A → PalindromeStarts739 P → orbit A t = P → t ≤ 39

no_196_739_palindrome :
  ∀ t, ¬ PalindromeStarts739 (orbit 196 t)
```

Here all three variables are natural numbers, `step n = n + reverse10 n`,
`orbit n 0 = n`, and `orbit n (t+1) = step (orbit n t)`. Decimal reversal is the
ordinary repeated division/remainder construction; `reverseFuel_correct`
connects its kernel-evaluable implementation to the terminating ordinary
reversal. `Palindrome n` means `reverse10 n = n`.

`PalindromeStarts739 P` is the conjunction of this whole-number palindrome
predicate with the existence of a **canonical** decimal representation of
`P`, of width at least three, whose three most significant digits are 7, 3,
and 9. `Canonical` explicitly requires positive width, digits at most 9,
nonzero most significant digit, and exact numerical value. Thus the prefix
predicate is about the ordinary numeral, not a pair-sum prefix or a padded
representation. There is no upper bound on decimal width in either theorem.

The result does **not** prove `IsLychrel 196`, `Decimal196Conjecture`, or
avoidance of palindromes with other leading digits. It does not claim that
every locally admitted inverse word is realizable by an integer, that 39 is
an attained optimal bound, or that the inverse graph is exact outside its
stated local relation. None of these stronger statements is needed.

## Ordinary integers and the last step

The base theorem `canonical_exists A hA` applies to every positive starting
integer, including integers ending in zero. `canonical_admissible` gives the
pair-column word `q i = d i + d (L-1-i)` positive width, positive outside sum,
entries at most 18, reflection symmetry, and an even middle entry at odd
width. `iterPairs_representation` supplies an exact canonical representation
of `orbit A t` at **each changing width**, with equality of all in-range pair
columns. It does not identify a fixed-width encoding with an ordinary orbit.
The proof uses `representation_next`, whose two branches are the genuine
nonoverflow and overflow canonical next-number constructions.

`canonical_last_step` has two independently given canonical representations,
the actual equality `step n = P`, palindromicity of `P`, and target leading
digit greater than one. Width equality and carry freedom are conclusions,
not assumptions. If the addition overflows, its canonical new leading digit
is 1; canonical uniqueness contradicts the target's leading digit 7.
With no final carry, the base symmetric-column lemma proves every carry zero
and every source pair sum equal to the corresponding output digit.

Palindromicity then reflects the three leading target digits into low-index
source pair sums 7, 3, 9. This correctly distinguishes integer digits from
pair sums; the latter are used only at the final predecessor. The familiar
overflow example `29 → 121` shows why eliminating the leading-digit condition
would invalidate the bridge. That condition is present here.

## Completeness of the long inverse

`NoOverflow` records the two local digit equations with low incoming carry
and high outgoing carry. Each inner high carry is explicitly in `{0,1}` and
each source sum is in `0..18`. Its unconstrained terminal carry state permits
an overapproximation, which is safe for bounding all genuine predecessors.
`OverflowTail` records the shifted high digit after the new leading carry;
its terminal constructor still checks the final high-column carry exists.
`LongCompatible` also requires a positive exterior source sum.

`prefixPredecessors` exhausts those equations. The overflow outside sum is
uniquely recovered by `overflowFirst_eq` **using the actual terminal/outside
carry condition**. The zero-prefix guard and the exceptional outside sum 9
are handled explicitly. `mem_prefixPredecessors_iff` is a global equivalence
with this local relation, not with full-number realizability.

`ActualPrefix.actual_mem_prefixPredecessors` establishes the separate
completeness implication needed by the application: every actual admissible
transition of width `L ≥ k > 0` has its retained source prefix in the list.
The high-side inner carry is taken from the actual word at `L-k`. The proof
does not assume disjoint boundary blocks; it covers widths 7 through 13 and
the full-width case `L=k`, where the inner carry is zero. Thus no overlap or
hidden interior restriction removes an actual predecessor.

The faster inverse guesses the next low carry and solves for a source sum.
Natural-number truncated subtraction cannot silently introduce a trusted
solution: all original equations are guarded again, and the exact candidate
recovery lemmas establish completeness. The next low carry is bounded because
the source sum is below 19 and its incoming carry is below 2.
`fastPrefixPredecessors_mem_iff` proves membership equivalence on all list
arguments. `checkedRows_fast_to_long` uses the correct inclusion direction:
every original predecessor is covered by the enumeration that was checked.

## Short words, crossing the seven-column boundary, and all roots

The complete short family has positive widths 1 through 6. Its respective
counts are 9, 18, 180, 342, 3420, and 6498, totalling 10,467. Outer sums range
over `1..18`, interior pair sums over `0..18`, and odd centers over even
values `0..18`; width one instead requires a positive even value. The formal
`rawWords_complete` proof obtains every actual short word from admissibility.
It never assumes all arbitrary six-tuples are genuine pair words.

`nextWord_wordOf` equates updating the finite reification with the exact core
update. It proves independence of the values outside the finite word via
carry/output congruence. `short_next_width` bounds the successor by seven;
the only crossing is six columns to seven on overflow. `ShortAt` and
`shortChecked_of_cases` include all five widths with a fixed positive outer
sum, and `shortOne` adds every legal width-one case. The resulting
`shortChecked` is exactly the premise consumed by ancestry induction:

```lean
∀ s ∈ shortWords, lookup ranks (nextWord s) = none
```

This checks the **full successor**, including its possible seventh column.
There is no omission of a short-to-long transition and no attempt to use a
seven-column inverse on a shorter source.

For the final predecessor, the no-carry bridge makes every pair sum at most
9. If its width is below seven, symmetry rules out widths three and four,
and the odd-center parity condition rules out width five. Width six is
exactly `[7,3,9,9,3,7]`. Widths one and two are excluded by the target prefix's
width requirement. Every width at least seven is projected to
`[7,3,9,a,b,c,d]` with all four free entries in `0..9`.

`targetInitialWords` contains the unique short word plus all 10,000 decimal
indices. `target_project_mem_initialWords` proves coverage symbolically;
it does not infer it from an empirical list of reachable targets.
`initialWord` and `targetInitialWord` have definitionally identical formulas.
The initial assembly covers every index from 0 through 9999 and checks rank
at most 38, while `initialShortChecked` checks the separate six-column word.
It is harmless that this initial family contains impossible long targets.

## Lookup, finite rows, and rank induction

`lookupKey` uses the numerical pivot only to choose a search path and compares
the **entire stored word** before returning a rank. `lookupKey_all` proves
that any successful result satisfies the assertion at the encountered tree
node. Neither key injectivity, sorting, uniqueness of words, nor the data
generator is a trusted hypothesis. A malformed tree could fail to find a
word, but initial coverage and predecessor checks must still pass through
that same lookup function; a false positive is ruled out by word equality.

`CheckedRows ranks (longPred 7)` means **every node** of the actual rank tree
passes a check over the entire executable predecessor list. It does not mean
only that a supplied list of stored edges descends. `checkBelow_sound` and
`checkedRows_closed` require each such predecessor to be found with a
strictly smaller natural-number rank. The six-column node has no long-row
obligation because `longPred 7` is empty there. This is sound: a long source
cannot shrink to six columns, and all short predecessors are separately
excluded by `shortChecked`.

`allRowsFast` assembles the 1024 leaf-subtree proofs and 1023 intervening node
proofs into the exact `RankTree.All` conjunction for the root. Its final
type, once compiled, prevents a missing subtree or a swapped conclusion.
The source-level diagnostic independently confirmed that every named leaf
and intervening branch occurs exactly once. Splitting resource-heavy row
batches 57, 58, 85, and 97 changes proof organization, not the leaf statements.

`actual_iterPairs_rank` is an induction on the actual elapsed time. At zero
the rank bound is automatic. At a successor, admissibility of the previous
exact state is available. If it is short, its full successor's lookup is
`none`, contradicting the assumed endpoint lookup. If it is long, actual
inverse completeness and the checked row provide a predecessor rank `s<r`;
the induction hypothesis gives `t≤s`, hence `t+1≤r`. No ancestry bound,
graph acyclicity assertion, or unverified reachability restriction is assumed.

The ordinary theorem separately treats `t=0`. For `t=u+1`, the pair state at
ordinary time `u` is the final predecessor, so its projection is a certified
initial word of rank at most 38. The rank induction bounds `u≤38` and the
last ordinary step gives `t≤39`. This checks the potential off-by-one issue
at the exact state/time correspondence.

The 196 consequence invokes this universal bound with `A=196` and combines
`t≤39` with the independently established finite ordinary-orbit theorem
`no_palindrome_through_100`. It does not assume the desired infinite
avoidance result. `TerminalObstruction` is not needed in the conclusion's
import closure; the pair-sum prefix `[1,9,6]` is not confused with the
ordinary integer 196 in this argument.

## Independent execution performed by this reviewer

`check_independent.py` is a separately written diagnostic. It imports none of
the author's Python generator/verifier, JSON certificate, fast candidate
formulas, or previous review programs. It parses only the literal Lean
`RankTree` constructor language and follows the actual named root. It
implements the exact full-word comparison in lookup. For the inverse it
enumerates all 19 source sums and both high incoming carries directly from
decimal quotient/remainder equations, including all possible outside source
sums in the overflow branch. For short words it independently constructs a
canonical positive integer, performs ordinary string-based decimal reversal
and addition, and extracts its new symmetric pair sums.

The process ran with a 90-second CPU budget and 1 GiB address-space cap and
finished successfully in approximately 0.91 seconds. `diagnostics.json`
records these actual results and SHA-256 pins for all 382 local Lean modules
in `Conclusion739`'s import closure:

| Check | Actual result |
|---|---:|
| Reachable literal nodes, all exact words uniquely retrievable | 58,501 |
| Complete distinct predecessor edges, all with strict rank descent | 68,152 |
| Rows with no long predecessors | 13,973 |
| Maximum distinct predecessors of one row | 69 |
| Long initial words checked | 10,000 |
| Maximum long initial rank | 38 |
| Unique six-column initial rank | 0 |
| Short words checked by actual integer realization | 10,467 |
| Six-to-seven crossings included in that check | 3429 |
| Short successors found in the rank lookup | 0 |

These are finite independent consistency checks, not additional Lean
theorems or a substitute for the kernel proof. The closure source pins were
checked unchanged at process completion.

## Kernel and excluded-axiom acceptance boundary

The previously supplied `review-clean/root03/verification.json` records a
successful fresh structural build and transitive axiom audit of 1333 theorem
constants, allowing only `propext`, `Classical.choice`, and `Quot.sound`.
That is inherited evidence, not an execution by this reviewer, and does not
alone establish the final numerical instance. The final clean specialist
is separately rebuilding the full chain from source.

This reviewer will compile the final module and an explicit endpoint audit
against pinned copies of that independently rebuilt dependency set. Such an
execution reuses dependency objects and will be recorded as an independent
**endpoint recompilation**, not as a second fresh build of all dependencies.
The endpoint audit must print the exact unrestricted theorem types and
transitive axioms of both endpoints and the concrete three premises. Any
`sorryAx`, compiler-evaluation axiom such as `Lean.ofReduceBool`, custom
logical axiom, or other axiom outside the three foundational ones is a
rejection. Generated unsafe runtime implementation declarations are not
proof oracles unless they occur in the theorem dependency chain.

No independent Lean compiler execution is claimed in this initial version
of the report. Final execution records and the acceptance verdict remain
pending. No Lean source, Git state, or author-owned file was modified by
this reviewer; all reviewer-owned artifacts are under `review-final/`.
