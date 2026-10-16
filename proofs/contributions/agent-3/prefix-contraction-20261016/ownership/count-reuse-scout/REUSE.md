# Read-only scout: finite binary survivor counts

**Reusable counting primitives exist. The missing project-level interface is a state-dependent continuation-count bound and its block recurrence.** The closest recent source is Agent #9's `Agent9FiniteProducts.lean`: its fixed-length word enumeration and concatenation lemmas are directly useful, but its fixed-block power theorem does not by itself handle different rejecting words at different automaton states.

This is a source and scope review by Agent #3's runtime/review specialist. The proposed survivor bound is unclaimed. No Lean compiler, generator, graph search, rejecting-path calculation, or certificate checker was run, and no new proof was implemented. The historical nine-column certificate premise remains unverified here.

## 1. Original mathematical contract

Section 2 of the preserved [constant-rho note](sources/original_constant_rho_note.txt) states the relevant elementary argument: the empty determinized subset is absorbing, and every reachable nonempty state has a rejecting continuation of length at most nine. Padding a shorter continuation after it reaches the absorbing empty state produces a rejected length-nine word. Thus at least one of the 512 nine-bit continuations is rejected from each live state.

The note deliberately omits center acceptance and counts necessary prefix conditions. Its broader claims cover multiple clocks and constant-rho values, but those computational assertions are not Lean theorems supplied by this scout. The original `decimal_counting_return_certificate.json` is absent from the available source captures; the parent's separate search found only omission metadata. Reading the note does not discharge its finite certificate premise.

The note's original source commit is `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`, Git blob `7f786de64953af35945df4e4a3bce063e788ab92`, SHA-256 `c30605969b2bf4852e9f2cccc64c3c9042f8d066dbf4b118e6db87105dc16727`. The preserved bytes were rechecked against the existing source manifest.

The [varying-rho boundary](sources/original_variable_rho_boundary.md) explicitly states that the constant-rho nine-column premise does not extend directly to arbitrary varying rho words; it records a finite 16-column obstruction to that extension. This scout read that boundary but did not replay its computational certificate. The [counting-gap note](sources/original_counting_gap.txt) also keeps finite language counts separate from all-time finite-seed survival.

## 2. Best recent reusable source

Source: [Agent9FiniteProducts.lean](sources/Agent9FiniteProducts.lean.txt), namespace `P196.Agent9.Ensemble`, importing only `Std`.

- Published commit: `cf7935d24ce8180d6181de01d1050fc02b66802c`.
- Repository path: `proofs/contributions/agent-9/finite-ensemble-marker-count-20261016/Agent9FiniteProducts.lean`.
- Git blob: `8b3f21db4c6d46e6ebc7c0e88e28f8054b698ccc`.
- SHA-256: `b4d3b1f4b910438533186b60c0a88e946887aaa47978d730b7eedc5352a10ccf`.
- Exact byte count: 7,277; the downloaded capture matches both published identities.
- A read-only GitHub ref lookup observed the same commit at `formalize/agent-9/finite-ensemble-marker-count-20261016` during this scout.

The [published checkpoint](sources/Agent9FiniteProducts-CHECKPOINT-001.md) reports an author `--trust=0` compilation and explicit audit of all 15 exports, using only the standard three axioms. It expressly leaves its whole marker-count task and independent full-closure gate in progress. This scout inspected the source and its recorded status; it did not independently compile that module.

All names in the next table have prefix `P196.Agent9.Ensemble.`:

| Declaration | Exact conclusion or interface | Assumptions relevant to reuse |
| --- | --- | --- |
| `wordChoices alphabet n` | List of all length-`n` words from the supplied alphabet list | Recursive finite list definition; no automaton assumptions |
| `mem_wordChoices` | `xs ∈ wordChoices alphabet n ↔ xs.length = n ∧ ∀ a ∈ xs, a ∈ alphabet` | None beyond the supplied alphabet/list/length |
| `length_wordChoices` | `(wordChoices alphabet n).length = alphabet.length ^ n` | No distinctness premise; this is initially a list-length identity |
| `wordChoices_nodup` | `(wordChoices alphabet n).Nodup` | `alphabet.Nodup` |
| `length_flatMap_map` | `(as.flatMap fun a => bs.map (f a)).length = as.length * bs.length` | No injectivity or uniform-word-length assumption |
| `nodup_flatMap_map` | The preceding mapped product is duplicate-free | Both input lists are `Nodup`; `f` is jointly injective on their members |
| `appendProduct as bs` | `as.flatMap fun a => bs.map (a ++ ·)` | Definition |
| `mem_appendProduct` | Membership iff `∃ a ∈ as, ∃ b ∈ bs, a ++ b = xs` | None |
| `length_appendProduct` | `(appendProduct as bs).length = as.length * bs.length` | None |
| `appendProduct_nodup` | Concatenated product is duplicate-free | Both lists are `Nodup`; every left word has the same specified length `r` |
| `blockChoices blocks suffixes J` | Concatenates exactly `J` words from one fixed block list, then one suffix | Definition; block list is independent of any state |
| `length_blockChoices` | Length is `blocks.length ^ J * suffixes.length` | No distinctness premise |
| `blockChoices_nodup` | The block enumeration is duplicate-free | Blocks and suffixes are `Nodup`; every block has common length `r` |
| `blockChoices_word_length` | Every member has length `J * r + q` | All blocks have length `r`; all suffixes have length `q` |
| `mem_blockChoices` | Membership iff total length is `J*r+q`, the suffix after `J*r` is allowed, and each block `(xs.drop (j*r)).take r` is allowed for `j<J` | The same block/suffix length premises; includes `J=0` |

With alphabet `[false, true]`, `wordChoices` supplies a complete duplicate-free binary enumeration of length `n` and exact size `2^n`. The product lemmas supply the finite-word partition machinery needed for a future prefix/suffix counting argument.

**Limitation of direct reuse:** a per-state rejecting witness does not give one common forbidden nine-bit word. The allowed block list can depend on the state reached by the preceding prefix. `length_blockChoices` treats one fixed list at every block position. A future proof must retain the state dependence or first prove a suitable encoding; simply using a single 511-element block list would leave an unjustified premise.

## 3. Already available Agent #3 enumeration

The existing namespace `P196.Agent3.OverflowHorizon` exports:

```text
allBits : Nat → List (List Bool)
allBits_length (m) : (allBits m).length = 2 ^ m
mem_allBits_iff (xs) (m) : xs ∈ allBits m ↔ xs.length = m
allBits_nodup (m) : (allBits m).Nodup
```

These declarations have no certificate or arithmetic-dynamics assumptions. They are in [FamilyCardinality.lean](sources/Agent3-FamilyCardinality.lean.txt), inherited baseline `89287c9d3eb7dd801c2b1a59eff03140d47d24ec`, Git blob `9523465561e0109f0e3b442f1689ea091a50af3c`, SHA-256 `dfded4df411694fcbe50487e7a963f45c7e0abe34e46ed828926aee9f329248d`.

This source already belongs to the current three-layer dependency closure and was covered by the completed earlier independent rebuild. Reusing it avoids adding another enumeration. The recent Agent #9 module offers a smaller `Std`-only import and generic product lemmas. An equality or permutation bridge between `allBits` and `wordChoices [false,true]`, or the needed concatenation decomposition for `allBits`, is not exported by either inspected source.

## 4. Exact Lean 4.19.0 list primitives

The installed checker archive contains no standard-library source tree, so the following source text was read from the official Lean repository. Tag `v4.19.0` was resolved to full commit `6caaee842e9495688c1567e78c0e68dbb96942aa`, matching the runtime commit used in earlier verification.

The strongest direct one-loss lemma is in [`Init/Data/List/Nat/Basic.lean`](sources/Lean419-List-Nat-Basic.lean.txt):

```lean
List.length_filter_lt_length_iff_exists :
  (filter p l).length < l.length ↔ ∃ x ∈ l, ¬ p x
```

Here `p : α → Bool`; there is no `Nodup` assumption. Applied to the complete length-nine enumeration and its Boolean nondead test, a rejected member gives a strict length bound below 512 and hence the natural bound 511. This is a proposed application, conditional on the rejecting witness.

Other exact reusable interfaces are:

| Namespace `List` declaration | Interface and role |
| --- | --- |
| `length_filter_le (p) (l)` | `(l.filter p).length ≤ l.length`; initial/remainder bound |
| `length_filter_eq_length_iff` | Equality with original length iff every member satisfies `p` |
| `length_flatMap` | `(l.flatMap f).length = (l.map fun a => (f a).length).sum`; state-dependent extension sum |
| `filter_flatMap` | `(l.flatMap g).filter f = l.flatMap fun a => (g a).filter f` |
| `filter_map` | Filtering a mapped list equals mapping the preimage filter |
| `foldl_append` | `(l ++ l').foldl f b = l'.foldl f (l.foldl f b)`; exact transition composition if word execution is defined by `foldl` |
| `countP_eq_length_filter` | Boolean predicate count equals filtered-list length |
| `countP_flatMap` | `countP p (l.flatMap f) = sum (map (countP p ∘ f) l)` |
| `countP_map` | `countP p (map f l) = countP (p ∘ f) l` |
| `countP_mono_left` | Pointwise implication on list members implies a count inequality |
| `length_eq_countP_add_countP` | Original length equals satisfying count plus failing count |
| `countP_pos_iff` | Positive predicate count iff a satisfying member exists |

The `length`/filter/fold lemmas were read in [List/Lemmas.lean](sources/Lean419-List-Lemmas.lean.txt); the `countP` lemmas were read in [List/Count.lean](sources/Lean419-List-Count.lean.txt). Exact captured SHA-256 and computed Git blob identities are in [source_manifest.json](source_manifest.json). The strict-filter source's Git blob was also independently matched against the official directory entry `336a17f7b4bc08be91f5358612966e1ca0668f51`.

## 5. Precise missing reusable interface

The following is a mathematical interface description, not newly implemented Lean source or an assertion that its premises have been checked.

Let `δ : Q → Bool → Q` be deterministic, with start state `q₀`, distinguished state `dead`, and word execution `run`. Require:

1. `δ dead b = dead` for both Boolean letters.
2. Word execution agrees with concatenation: execution of `u ++ v` is execution of `v` from the state reached after `u`.
3. Every state reachable from `q₀` that differs from `dead` has some word `u` of length at most nine with `run q u = dead`.
4. The count `S(n)` is the filtered length of a complete duplicate-free enumeration of binary words of length `n`, retaining exactly those with `run q₀ w ≠ dead`.

The finite cardinality of `Q` is useful for supplying/checking premise 3, but the conditional counting argument itself only needs the reachable states and these properties. Unreachable states need no rejecting witness.

The missing bridge must establish the exact split into length-`m` prefixes and length-nine suffixes. For each prefix, count surviving suffixes from its reached state. A dead prefix contributes zero by absorption. A live reachable prefix contributes at most 511 by its padded rejecting witness and the strict-filter lemma. Summing these contributions is the proposed route to

```text
S(m + 9) ≤ 511 * S(m).
```

I found no existing source declaration in the inspected corpus that packages this state-dependent recurrence. A generic bounded flat-map/count sum lemma could be added after a claim, or the sum estimate could be discharged by ordinary list induction while reusing the identities above.

The proposed finite iteration is then

```text
S(m + 9*q) ≤ 511^q * S(m),
S(n) ≤ 2^(n % 9) * 511^(n / 9).
```

The second formula additionally uses the elementary remainder bound `S(r) ≤ 2^r` and the quotient/remainder decomposition of `n`. No project theorem with this generic multiplicative-block iteration was located. This natural-number formulation avoids interpreting `511/512` as truncated natural division or introducing real-analysis infrastructure. It remains a finite-word bound, even though it quantifies over every finite length.

**Counted objects must remain explicit.** `S` counts nondead binary words, not reachable states or distinct inverse paths. Different words can reach the same state and must still contribute separately. If a separate terminal/center predicate defines accepted words, its count can be bounded above by `S` at each length, but the recurrence with that accepted count on both sides does not follow merely from the absorbing-state premise.

## 6. Nearby sources that do not close the gap

The original [Agent #9 PathCounts](sources/Agent9-PathCounts.lean.txt) exports `P196.Agent9.InverseFibers.length_extend`, `extend_nodup`, `preimages_length`, `preimages_nodup`, and `exact_fiber_bound`. Its source pin is Git blob `fac4c4090cf63c2ecdeb5791e6af8758a0821616`, SHA-256 `588890faa1a29739b00dbe660a5f39971ac5087d997550cb9a740194eb592a33`. `length_extend` proves a product length for prepending natural coefficients; the other results count original inverse label words for one fixed target, including center carry matching. Its Fibonacci bound does not count surviving binary target continuations. Its `run` propagates a four-entry count vector, which is a different interface from deterministic word execution.

[Agent423.FiniteEnsemble](sources/Agent423-FiniteEnsemble.lean.txt) has `finite_bounded_witnesses`, which derives some uniform natural bound from individual existential witnesses over a supplied finite list. It does not supply the specific value nine. Its `finite_survivors_stabilize` and extraction lemmas concern one fixed finite ensemble and have no quantitative exponential word-count conclusion. [Agent423.FiniteCertificate](sources/Agent423-FiniteCertificate.lean.txt) provides Boolean reflection/checker interfaces but no block-loss count.

[CoefficientContraction](sources/CoefficientContraction-original.lean.txt) contracts coefficient magnitude bounds under a symbolic step; it is unrelated to a loss in the number of words. [Counting](sources/Counting-original.lean.txt) counts a constructed safe numeric predecessor family. [FiniteGraph](sources/FiniteGraph-original.lean.txt) verifies a scalar graph-lift encoding and edge realization; it supplies no rejecting-word or survivor-count bound. Their exact source pins are retained rather than treating matching filenames as mathematical reuse.

## 7. Coverage and status

- Text-searched 1,860 local Lean paths representing 1,472 unique contents in `p196-coordination`; the recorded local head was `97b556fcb0d9f09f6dd7d529c3b029a96eeb4ca4`. Seventy paths matched the recorded semantic/counting search pattern. This was a source-text search, not a full semantic review of every file.
- Inspected the original written inequality and scope-boundary notes, the relevant inherited enumeration/path-count sources, adjacent finite-ensemble sources, and the complete recent Agent #9 finite-products module and its checkpoint report.
- Read the saved recent Agent #9 marker-count and Agent #101 multiplicity task declarations for scope; used the former to locate the generic source, then independently read its published source and current branch ref. No all-current-branch or ownership-clearance claim is made.
- Captured 16 source documents; verified seven local source Git blobs at explicit commits, both Agent #9 published document blobs, and the official strict-filter source blob. [source_manifest.json](source_manifest.json), [remote-read-provenance.json](remote-read-provenance.json), and [scan_inventory.json](scan_inventory.json) retain the details.

The next concrete proof obligation, if the parent later obtains a protected claim, is the conditional state-dependent counting interface plus the independently established automaton/certificate premises. The absent nine-step witness certificate remains a separate prerequisite; this scout supplies neither it nor a mathematical claim.
