# PR 118 exact-head source-scope review

## Decision and identity

**Result: no blocking source-scope finding. No mathematical source correction is requested.** The exact source supports the advertised complete finite folded transducer, unique consumed paths and table histories, reconstructed positive-integer realizability, and genuine ordinary reverse-and-add step correspondence. I found no concrete source gap that warrants another Lean execution.

- Reviewer: Agent #28, task `/root/pr118_scope`, independent of every author of the 11 new mathematical modules.
- Repository and PR: `taco-jpg/p196-algorithm`, PR 118.
- Reviewed head H: `90c639b8a782a9a832bc19f6a6978196e91a3d78`.
- Original mathematical baseline: `98d59927ad89c42f438ea857ec5750a0df3b91db`.
- Review type: source interpretation and exact-source integrity review. This reviewer ran **zero Lean commands** and did not claim a fresh kernel check.
- This review does not submit a GitHub review, approve a merge, acquire a main write slot, or attest to a later main tree. The integration owner controls those actions.

The existing attributed review at `https://github.com/taco-jpg/p196-algorithm/pull/118#pullrequestreview-5554276338` was inspected as existing evidence, not made into a new review-of-review requirement. Its finite-scope qualifications agree with the actual statements. Runtime receipts, manifests, and attribution are the separate evidence reviewer's remit.

## Exact objects and coverage

All 11 new `Agent107Transducer*.lean` modules and the complete registry were examined. For generated `TablesChecks`, the common six-theorem block was read and all 46 complete blocks were checked for exact normalized equality and correct internal index references; none differs except its consistent row/state number. All literal state, edge, and terminal rows in `TablesData` were read, along with the list assembly and length/Nodup endpoints. The small companion `SOURCE_SCOPE_CHECKS.json` records exact byte hashes, Git blob hashes, import lists, and structural checks; those checks are not a substitute for the retained Lean execution evidence.

The registry's 12-module closure consists of the 11 additions plus the original `Lychrel196Research` module. I recalculated every registered SHA-256 and Git blob from the staged exact-H bytes and checked every registered import list. All match. The two roots are `Agent107TransducerGraph` and `Agent107TransducerBoundary`; Graph imports Numeric and Reachable and thereby covers the other additions. All registered endpoint short names occur in the pinned sources. The explicit new theorem count is 407, including repeated finite checks and reachability witnesses; it is not a measure of independent mathematical ideas.

The following original sources were also inspected:

| Original source | Exact Git blob | Inspected interface |
|---|---|---|
| `proofs/Lychrel196Research__c696e0ea3db39d92.lean` | `c6c1f5441c54a36f2d82b3ef78dff1ccdbc5a506` | Ordinary reversal/step; canonical decimal representation; column sums, carry, output, extended digits; admissibility; folded trace and emission facts; realizability; representation-next; canonical admissibility |
| `proofs/creative_regular_direct__8988fd8c6a0aad92.py` | `5658e577de22431ee029cf49c2ff640321dc0d8a` | Two initials, ordered graph enumeration, transition and output arithmetic |
| `proofs/persist_spacetime_weighted__d53dd1c09dcfc34a.py` | `8274715ce60ab084b602a08184ed909ee41a1f28` | Ordered terminal enumeration and `history_path` indexing convention |
| `proofs/creative_regular_invariant__ea923cdb26a39825.py` | `fa334ba0f094998c206f1eccc529b375c1c5351b` | `C`, `D`, `fold`, `unfold`, `qstep`, `valid`, and `trans` |

The Python sources were retrieved through the connector at H. They were read to check the mathematical interpretation. I did not rerun either the author generator or the existing independent AST comparison.

## 1. Definitions preserve the intended algorithm

`State` retains all five original fields: final overflow, forward carry, backward carry, signed delayed high digit, and the started flag. The two legal initials are exactly `(0,0,0,-1,false)` and `(1,0,1,1,false)`. In particular, `delay : Int` preserves the original negative sentinel. A zero-overflow update continues to store `-1`; a nonzero-overflow update stores the newly computed high digit.

`Transition s q t` requires `q <= 18`, a positive first pair when `s.started = false`, `t.high <= 1`, the backward carry equation `(q + t.high) / 10 = s.high`, and equality of the whole target state with `nextState s q t.high`. This last equality fixes overflow, low carry, delay, and started, not merely the high component. Interior zero pair sums remain permitted. The original Python `C` and `D` are exactly integer division and remainder by 10, matching these natural-number formulas on the legal inputs.

`Terminal` retains the nonempty-input condition. An even input requires the two directional carries to meet. An odd center must be at most 18, even, and advance the low carry to the high carry. The rule permits a zero center after at least one pair but requires a positive center when there are no pairs. These distinctions agree with the original valid-word and terminal enumeration logic.

The type `State` is deliberately larger than the reachable graph. For arbitrary malformed states, `Int.toNat` on a negative overflow delay need not agree with unrestricted Python signed arithmetic. No published endpoint claims such unrestricted statewise equivalence. The numeric semantics use accepting paths, and the graph theorems restrict membership to the exact reachable table. The general Boundary formulas with premise `overflow != 0` are identities of the Lean definitions; they do not assert reachability or digit bounds for every such state.

## 2. Path existence and uniqueness have the correct quantifiers

`Accepts L q p` reads `p 0`, the `L / 2` pair transitions, and the terminal state `p (L / 2)`. `finitePath` has exactly `L / 2 + 1` states, including that terminal state. No claim constrains a state-function tail beyond this prefix.

Path first constructs `actualState` from the original carry functions. `actual_accepts` is universally quantified over every `L` and `q` satisfying `Admissible L q`. The accepting carry proof invokes the old unrestricted even/odd folded-trace soundness theorems: the forward carry starts at zero; the terminal meeting equation fixes the backward carry, including the initially guessed final overflow. The complete state equality then follows by induction from the exact initial state and exact next-state equality, so the started flag and delayed digit cannot vary independently.

`accepting_state_eq_actual` concludes equality only for `i <= L / 2`. `exists_unique_finitePath` quantifies a unique finite list represented by some accepting path; its nested existential path witnesses do not claim a unique total function `Nat -> State`. Graph's unrestricted `accepting_state_unique` removes the admissibility premise on the unread input by applying the reconstruction to both accepting paths. This gives the stronger finite-prefix result for any two paths accepting the same raw `q`, without assuming that raw `q` is already symmetric.

Local transitions are not claimed deterministic: different guessed high carries can initially produce branches. The claim is unique **complete accepting** finite history once the center constraint is met. `Boundary.accepted_tail_not_unique` explicitly exhibits distinct total functions with the same accepted one-column finite path. This is consistent with the advertised uniqueness.

## 3. Reconstruction establishes realizability without a hidden hypothesis

Acceptance alone cannot constrain the original high half of `q`. Input handles that explicitly by defining `symmetrize L q i` using the lower of `i` and its reflected index. The proofs preserve every pair and the odd center actually read by the transducer. They establish acceptance equivalence, input folded-word equality, and path-output equality for the reconstruction.

`reconstructed_admissible` derives every original admissibility clause from `Accepts`: positive width, positive outer column, finite column bound 18, symmetry, and even center. The upper-half bound is obtained by reflection into a read pair or the accepted odd center; the raw high half is not silently reused.

The original `valid_word_realizable` is substantive: it constructs decimal digits by distributing a pair sum between `q - 9` and `min q 9`, with the central digit `q / 2`; its positive leading digit and bounded digit proofs produce a canonical positive integer. Input invokes that theorem with the newly derived premises. Thus `accepting_input_realizable` is not vacuous or a restatement of a numeric witness assumption. Its existential `n,d` follow after `L,q,p` and the acceptance premise, as required.

No uniqueness of the decimal digit realization or of `n` is claimed. Multiple ordinary integers can have the same symmetric column-sum word. This is correctly separated from unique accepting carry paths.

## 4. Zero, one-column, parity, and overflow cases

Zero width is rejected by the actual `Terminal` nonempty condition at the initial state. Input derives positive width directly, and Boundary proves `empty_input_rejected` explicitly. An even-zero algebraic output identity can still be stated in Output without asserting an accepting or numeric zero-width input; it does not enlarge the numeric theorem's domain.

For `L = 1`, there are no pair transitions, but there is a required terminal row. `one_digit_accepts_iff` retains all conditions: a legal initial `h <= 1`, `p 0 = initial h`, positive `q 0 <= 18`, even `q 0`, and `q 0 / 10 = h`. Therefore it covers exactly the positive one-digit column sums 2 through 18 in steps of two. The retained examples check both branches: center 8 has output center 16, and center 10 has the extra output pair `[1]` and no center.

The output rules are proved as four separate equalities to the original `nextColumns`, before the general `actual_output` and `accepting_output` endpoints combine them:

| Input width | Final carry | Extra terminal pair | Output center | Output width |
|---|---:|---|---|---|
| `2k` | 0 | None | None | `2k` |
| `2k` | 1 | None | Twice the terminal delay | `2k + 1` |
| `2k + 1` | 0 | None | Twice the computed center digit | `2k + 1` |
| `2k + 1` | 1 | Computed center digit plus terminal delay | None | `2k + 2` |

The odd-overflow proof uses `ofFn_append_last` to append the last pair at the end of the finite list. It is neither lost nor misclassified as an output center. The accepted-path proof obtains the actual carry bound from admissibility, so the final carry split is exhaustively 0 or 1. Lower-level branch formulas sometimes require less than admissibility because they are arithmetic identities under a specified carry/symmetry premise; the final numeric theorems retain the required representation conditions.

## 5. Numeric endpoints represent the genuine ordinary step

The original `Lychrel196.step n` is `n + reverse10 n`; reversal consumes actual base-10 digits, and the baseline has the correctness link between its fuel-based and well-founded implementations. `Canonical n d L` requires positive width, digits at most 9 within the width, a positive leading digit, and decimal value exactly `n`. Consequently this package's canonical inputs are positive; it does not represent zero by a positive-width leading-zero encoding.

`canonical_step_path` starts from **every supplied canonical representation** and obtains admissibility from `NormalizationBridge.canonical_admissible`. There is no extra caller-supplied symmetry or admissibility hypothesis in that direction. Its path and canonical output witness represent the genuine `step n`.

`canonical_accepting_step` is universally quantified over `n,d,q,L,p`. Given the explicit canonical representation and finite column agreement, it applies the original `representation_next` to that same `n`, and obtains the complete finite output-column relation plus the folded output equality. This supports the advertised claim for every canonical realization satisfying the premises, not just the special realization chosen by `valid_word_realizable`.

Conversely, `accepting_numeric_realizable` assumes only a complete accepting path and derives some positive `n` with canonical input and canonical `step n` output. The output width is exactly `nextWidth (symmetrize L q) L`. This is crucial: the unexamined raw high half cannot influence the numeric width. The input and output folded words are those of the original accepted `q,p`, because the reconstruction preservation lemmas are carried through the result.

`indexed_numeric_realizable` transfers this same result to literal `historyOutput`. The reverse endpoint is existential, while the canonical forward endpoint is universal over the provided realization. Neither statement reverses these quantifiers or requires one realization to work for unrelated input words.

## 6. Literal tables, reachability, and histories are connected soundly

TablesData contains raw, reviewable literals. The ordered lists have 46 states, 872 edges, and 251 terminal rows. The file concatenates all source-state blocks in order 0 through 45; the structural check confirms these exact counts and concatenation order. State, edge, and terminal-row types retain every field needed by the semantic relations.

TablesChecks has six uniform finite facts per state: edge separation/Nodup, terminal separation/Nodup, edge soundness, edge completeness, terminal soundness, and terminal completeness. Edge candidates range over `Fin 19` inputs and `Fin 2` backward carries. Terminal candidates are `none` and all `some` values 0 through 18, with `Terminal` enforcing evenness and the carry/nonempty conditions. Every proof uses ordinary `by decide`, not native evaluation.

Tables promotes those facts to arbitrary `Nat` and `Option Nat` inputs by deriving the finite bounds from `Transition` or `Terminal`. `edge_mem_iff` explicitly requires `s` to belong to the listed states, and includes the exact emitted output equality. `terminal_mem_iff` likewise includes the source membership and both output fields. These are complete over the reachable source-state table; they do not claim enumeration of transitions from every possible record of type `State`.

The global Nodup proofs use distinct source-state block keys plus each block's Nodup and source-field fact. `states_closed` then derives target membership from semantic transition completeness and edge soundness. Reachable supplies both legal initials and explicit predecessor/input witnesses for every other listed state. The induction in the reverse direction uses closure. Thus `reachable_iff_mem_states`, together with length 46 and Nodup, establishes the exact finite-transition reachable set, not merely a closed overapproximation. It says nothing about safe invariant membership or reachability along the orbit from 196.

`GraphAccepts` and `Accepts` are equivalent through those soundness/completeness results. The initial-state premise is retained in both directions, so arbitrary listed paths cannot enter from an invalid start.

`IndexedAccepts` is a suitable independent input relation: it checks only edge source/input/target, terminal source/center, and the legal initial state. It does **not** assume that the selected edge's output or terminal outputs are correct. `indexed_edge_eq` and `indexed_terminal_eq` derive those full rows from table soundness. `indexed_output` then proves that reading the literal output fields yields `pathOutput`.

`accepting_indexed_exists` obtains row indices from membership. `indexed_history_unique` combines finite state equality with the two list Nodup proofs to show that both the finite edge-index function and the terminal index are equal. `admissible_unique_history` has the correct existence-then-universal-uniqueness order. A zero-length edge-index domain at one-column width does not bypass the terminal row requirement.

The Lean terminal index is local, in `Fin 251`. The original Python `history_path` emits the terminal coordinate offset by `len(FE) = 872`, so its final coordinate is 872 through 1122. Edge coordinates remain 0 through 871. The README and existing review state this distinction accurately. No theorem formalizes the entire Python interpreter, exception behavior, or returned list program. Likewise, the odd-overflow terminal extra pair changes the output word, not the number of input edge indices.

## 7. Existing evidence that can be reused

The source boundaries above agree with the exact-H README and registry. The registry accurately remains `catalogue_complete: false` and `SOURCE_PINS_ONLY_NO_VERIFICATION_ASSERTION`; its existence is not itself a proof-check receipt. It scopes the project to finite transducer and positive-integer one-step semantics and explicitly excludes infinite nonpalindromicity.

The following existing evidence is appropriate to reuse for these unchanged source hashes, subject to the separate evidence reviewer's receipt and manifest checks:

1. `semantic-review/clean-rebuild-20261016T214242.588596Z/manifest.json` and the final module-origin audit: the attributed reviewer reports a same-chain empty-directory rebuild of the full baseline and all 11 additions with official Lean 4.19.0 and explicit `--trust=0 -j1 -DElab.async=false`. The source SHA table in the accompanying final semantic review matches this registry. This current review does not relabel that historical execution as a new execution by Agent #28.
2. `semantic-review/compare_literal_table.py` and `literal-table-comparison.json`: the script selects original `C`/`D`, `fst_graph`, and terminal AST statements, parses the actual Lean state/edge/terminal literals, checks full ordered sequence equality, and verifies block concatenation order. It does not import the author generator or the author's extracted JSON. The result pins the exact TablesData SHA-256 `70bc2285605fb1b581bc0bc14adef8593ee451b312adb5f79fcf19cce83988ef`. This supports source provenance, not formal Python interpreter correctness.
3. `boundary-independent-review/REVIEW.md` and its manifest: the separate `lean_runtime` reviewer covers Boundary, which the main semantic reviewer authored. This cross-review is restricted to Boundary and does not claim independent author review of that reviewer's own Tables/Reachable modules. Its described reuse of an independently rebuilt baseline object is explicit and need not be rewritten as a completely fresh baseline build for that particular cross-review.
4. `canonical-verification-be8e612c/`: the retained original-verifier execution covers the pinned project at `be8e612ca0694d5d9d8473c784ab1956f93405b6`. Its relevance to H depends on the recorded unchanged mathematical source and registry bytes. Its command does not explicitly add `--trust=0`, so it must remain distinct from the independent explicit-trust-zero run. Its scoped result must not be turned into a repository-wide PASS.

The source review found no reason to invalidate those exact-source executions or to demand a duplicate rebuild merely because another reviewer has now read the same unchanged package. Source or dependency changes after H would require impact-specific revalidation. Current-main compatibility, CI metadata, full evidence integrity, and merge eligibility remain separate questions for the integration owner and evidence reviewer.

## 8. Remaining theorem boundaries

This package provides reusable finite arithmetic/transducer components. It supplies no safe closed language instance, no 196 entry certificate, no infinite accepting trajectory, and no proof of infinite nonpalindromicity for any fixed seed. It does not claim all decimal realizations are unique, full state-function tails are unique, arbitrary malformed states match Python arithmetic, or the complete Python execution environment is formally verified.

The original folded-trace, emission, realization, and representation-next proofs remain attributed to the pinned baseline. The new modules connect them to the literal graph and indexed histories. Their reuse is visible in the imports and theorem applications and is not presented as new proof ownership.

**Source disposition:** retain the exact H mathematical sources and registry. No blocking finding, no source edit, and no new Lean execution are requested by this review.

## Source acquisition note

Early exact-H `git cat-file` reads used the designated existing object store without an explicit fetch command. After the parent clarified its partial-clone status, further object reads used `GIT_NO_LAZY_FETCH=1`, and subsequent inspection used the parent's verified staged bytes or the GitHub connector. The reviewer did not issue checkout, fetch, source modification, or any remote write. The earlier calls did not explicitly disable Git's promisor-object lazy fetching, so this report does not claim that those reads could not have populated missing objects. This acquisition limitation does not alter the exact source hashes recorded here.

## Exact new-module pins

| Module | Git blob | SHA-256 |
|---|---|---|
| `Agent107TransducerBoundary` | `7c46227bc4fd31517ee016ba35bbca2385a0f2fe` | `cbdc094ba800bf4198bc5a1f2ece8b971aaea91ed2ceb2f1b36a24a978baa89c` |
| `Agent107TransducerDefs` | `03b290b828321dc9144a8741990f7089f07ece53` | `5df72daaa1a29f7df4d9b967215b735b7e39ebbd9245d1135d1073473178a530` |
| `Agent107TransducerGraph` | `f7925c5afa2983d95942cf98f6100221a659417a` | `b24422cb928ab6d9abc796478ab6c0c2631106f5c196385646c631a6f310b02a` |
| `Agent107TransducerInput` | `55a811ec593ba8f0ccea5290e8ef8b6f53c46bb3` | `91fbfa4d00f3c8ef8229c571f26847246b72502a24f4a7bd7de7692f898c873b` |
| `Agent107TransducerNumeric` | `f27fb02b4b422af06e55ee288cc9f8ecd50a8552` | `67d88fb4dea6639a0230c5d0f93d8ed778e6393c073679233ab0e792160e086a` |
| `Agent107TransducerOutput` | `f4cda74629b74db4ed8e4d9f98825e5eb70cb217` | `5e71e9bd7a693e19fed7716e71a951d4c06708f42cffc8b1afde4f65aa6e2d67` |
| `Agent107TransducerPath` | `990a8c083bdb44955b434e25ba6fff4dc73ea124` | `718a0a82b010f75949e02ed7665e61f1b5014c38c4661726cebd00ac0f6db21c` |
| `Agent107TransducerReachable` | `7ecaee195da124b420a91590fcfdd274bcf39a87` | `7e4dc0b05d441f27bc56f96d3c1cdc7fafa59393b5456fc1ad7feaa93180681b` |
| `Agent107TransducerTables` | `4eeb388160245c1057debc70c49d24f586832a2b` | `418febdd3cfcf513b2727543532b00e8add1881c1c826dc8112f96365523c67f` |
| `Agent107TransducerTablesChecks` | `0461201189bdd1ddd78a1e44a284abce4c1e5c66` | `3b87f981d86ed80d8870ea627c7459f7b3b0bffa987fe13378b2f29966b3a60b` |
| `Agent107TransducerTablesData` | `afc8b382cfe84b2660ef0e559901b8baf136885d` | `70bc2285605fb1b581bc0bc14adef8593ee451b312adb5f79fcf19cce83988ef` |

Registry Git blob: `167426452d3b05319c74b5ea29a09e1b25442d63`; SHA-256: `2a897d49fe54eba72f48e68e7888b3fe9d21aa2cc58f1abb2d48a0a68bd4b238`.
