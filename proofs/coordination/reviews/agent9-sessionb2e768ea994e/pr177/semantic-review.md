# PR #177 independent semantic review

## Verdict and identity

**SEMANTIC_REVIEW_PASS for the generic conditional DFA/Horn closure contribution at the exact source head below. No blocking mathematical defect was found within the reviewed scope.** This is an independent source and semantics review. It is not a Lean compilation result, a transitive kernel axiom-audit result, a platform approval, or authorization to merge without the remaining delivery gates.

| Field | Value |
| --- | --- |
| Repository | `taco-jpg/p196-algorithm` |
| Pull request | `177` |
| Source head H | `6f48ca108dee4c07588f8c5582bcfef55388537f` |
| Assigned base B | `74a1c3922eb7af438fe40b23d2105ad07556e3f5` |
| Review date | `2026-10-17` |
| Reviewer | Agent #9's genuinely independent nonauthor semantic-review subagent, task `/root/pr177_semantic_review` |
| Delivery owner | Agent #9, root session `b2e768ea994e` |
| Delivery record supplied with assignment | `proofs/coordination/tasks/agent9-sessionb2e768ea994e-pr177-delivery-20261017.json` |
| Accepted coordination commit supplied with assignment | `3460fe1416fe7289605bd8ffe0ce1c60780d9e09` |
| Source writer supplied with assignment | Agent #107, ACTIVE |
| Main writer supplied with assignment | Agent #31/session `02893e4f368d`; role blob `62de1daf0365fc361c8cd633e1858c6118371f4e` |
| Review artifact | `/workspace/scratch/b2e768ea994e/agent9-pr177/semantic-review.md` |

The reviewer did not author or modify the contribution, run compilation, mutate any external service, claim a source or main-write slot, publish a review, or spawn another reviewer. The review was explicitly delegated by the named delivery owner to fill the missing exact-source independent semantic evidence. It does not reopen an already satisfied review merely because delivery ownership changed. Source ownership, base compatibility, actual verification execution, platform requirements, and delivery remain with the root agent and current authorized writer.

The full role safeguards in `/workspace/scratch/b2e768ea994e/upload/Pasted text(20261017-045901).txt` were read before substantive work. This durable technical deliverable is in English. Conversational handoffs to the delivery owner used Russian.

## What was reviewed and what was executed

All seven new Lean modules were read in full: `Agent107DFA`, `Agent107DFAHorn`, `Agent107DFAChecker`, `Agent107DFAAlphabet`, `Agent107DFABoolean`, `Agent107DFARelation`, and `Agent107DFAArithmetic`.

The following inherited transducer modules were also read in full to assess the dependencies actually used by the new endpoints: `Agent107TransducerDefs`, `Agent107TransducerInput`, `Agent107TransducerPath`, `Agent107TransducerNumeric`, `Agent107TransducerGraph`, `Agent107TransducerOutput`, `Agent107TransducerReachable`, `Agent107TransducerBoundary`, and `Agent107TransducerTables`.

For `Agent107TransducerTablesData`, the state definitions, data structures, enumeration layout, boundary rows, and counting declarations were inspected directly. Every literal state, edge, and terminal row was then parsed and compared against an independent arithmetic enumeration of the original algorithm. For `Agent107TransducerTablesChecks`, the six proof templates were read, and all 46 blocks were checked to have exactly those templates under uniform index substitution. These are exhaustive finite-data checks, not a claim to have manually reread every repeated data line.

For the inherited `Lychrel196Research` module, the relevant definitions and proofs were inspected, including decimal reversal, the numeral-value/column-addition bridge, `Canonical`, `canonical_exists`, the folded carry and emission results, `Admissible`, `nextWidth`, `representation_next`, realizability, and `NormalizationBridge.canonical_admissible`. The unrelated remainder of that 4,445-line research module was not independently re-reviewed as mathematics. The active-source token scan did cover the entire file along with the other 18 Lean files.

The exact-head registry and `EXACT-HEAD-HANDOFF.md` were read. The latter accurately labels itself a reproducibility setup rather than a verification result; its historic environment observations were not treated as the present execution result. The registry contains 19 source modules and roots for the arithmetic, Boolean, relation, and boundary modules, including modules that would not follow from the arithmetic import alone. Root separately owns actual fresh pinned canonical and strict verification.

The three original Python sources were fetched through the supported GitHub connector at H and read in full. They were **not executed**, imported, or used as a solver oracle. Their returned source bytes were independently checked against the returned Git blob identities.

Executed by this reviewer:

1. Read-only source inspection and exact-head GitHub source fetches.
2. A Python standard-library identity check of all 22 files in the supplied source manifest, checking byte length, SHA-256, and Git blob SHA-1.
3. An independent finite-data comparison of the entire 46/872/251 literal graph, exact order, uniqueness, alphabet bounds, and terminal shape.
4. A structural comparison of every repeated finite-table proof block.
5. A comment-stripped active-token scan of all 19 Lean sources for prohibited proof escape hatches.

No Lean, Lake, repository Python program, Z3 solver, build script, or verification script was executed by this reviewer. The table checks and token scan supplement source review; they do not replace kernel checking or the transitive audit of the actual compiled declarations.

## Findings

### 1. The conclusion is unbounded in finite input length

`Agent107.FoldedDFA.horn_prefix_invariant` quantifies over arbitrary `L : Nat`, arbitrary input function `q : Nat → Nat`, arbitrary path `p : Nat → State`, and every `i ≤ L / 2`. Its proof is induction on `i`, beginning at the two Horn start clauses and applying a Horn edge clause for each consumed pair. `DFA.run_ofFn_succ` provides the required append-one transition identity. There is no fixed maximum width, finite collection of sample words, or assumption that an enumerated prefix approximates all lengths.

The passage from the literal transition relation to the finite edge list uses `Agent107.FoldedTransducer.graphAccepts_iff_accepts`, whose forward and backward directions rely on actual soundness and completeness of the literal edge and terminal tables. Thus the finite certificate obligation is a universal condition on a finite product graph; the all-length conclusion is established by induction, not by sample success.

`Agent107.FoldedDFA.horn_accepting_output` applies the invariant at `L / 2` and the corresponding terminal row. The resulting theorem is exactly acceptance preservation from `foldPrefix L q` to `pathOutput L q p` for a complete accepting transducer path. It does not assert that every arbitrary `q` or every arbitrary path is a valid decimal instance.

The lack of an admissibility hypothesis in the path theorem is appropriate: `Accepts` only reads the folded prefix and optional center. The unread half is irrelevant to this theorem. The numeric reverse interpretation correctly reconstructs the unread half with `symmetrize`, rather than asserting unsupported symmetry of the original infinite function.

### 2. The Horn structure does not assume the desired language closure

`Agent107.FoldedDFA.Horn` contains three local obligations only:

- Both initial transducer states relate the DFA start state to itself.
- Each literal edge carries any related input/output state pair to the pair obtained after its two labels.
- Each literal terminal carries input final acceptance to output final acceptance after consuming its optional extra pair.

There is no field asserting global language closure, numeric invariance, absence of palindromes, or the final theorem itself. The predicate `R` is universally parameterized, and the proof derives its values at path prefixes from the supplied local certificate. This is a genuine sufficient finite simulation condition.

The relation is allowed to overapproximate reachable product states. Unreachable entries do not weaken the forward proof, since the start and edge clauses force every actual product prefix into the relation. Setting every relation value false cannot satisfy the start clauses when a `DFA N` exists.

The conditions are not inconsistent. As a semantic consistency witness, a one-state automaton that accepts all centers and a relation that is always true satisfy all three families. This observation is mathematical reasoning, not a newly compiled Lean instance or a safe invariant. It also shows why closure alone does not imply safety.

### 3. The finite checker reflects exactly these obligations

`boolImplies_iff` establishes the direction and truth-value meaning of Boolean implication. `allFin_iff` uses the complete `List.finRange N` enumeration, not a partial selection of indices. `checkStarts_iff`, `checkEdges_iff`, and `checkTerminals_iff` then establish exact equivalences for the three families.

`checkHorn_iff` proves:

```lean
checkHorn M rb = true ↔ Horn M (fun s a b => rb s a b = true)
```

The checker enumerates the two initials, every literal edge, every literal terminal, and every `Fin N × Fin N` pair. It does not need to enumerate the infinite ambient `State` type: all graph-relevant states occur in the sound and complete finite table, and the inductive argument visits only them.

The terminal Boolean clause is `R → (inputFinal → outputFinal)`. Its nested implication is not reversed, and it does not require acceptance of inputs outside the recognized language. The edge clause advances both automaton states with the corresponding input and output labels.

### 4. Zero-state vacuity is excluded where it matters

Both `DFA N` and `Encoding.BooleanDFA N` contain `positive : 0 < N`. The start state is explicitly index zero with that proof. Consequently neither a `DFA 0` nor a `BooleanDFA 0` can be supplied under the ordinary consistent natural-number theory.

The generic helper `allFin` intentionally handles `Fin 0` and is vacuously true there. This is correct and is not an acceptance bypass, because the checker endpoint also requires an actual `DFA N`. The row checker is different: its outer `List.any` is false on an empty row, correctly rejecting the existence part of exactly-one. No additional hidden `N > 1` requirement appears; a one-state machine is a valid generic case.

### 5. One-hot extraction includes existence and uniqueness

`Encoding.BooleanDFA` has exactly the original `N × 19 × N` transition array and `N × 11` final array. `BooleanDFA.OneHot` requires, for each state and symbol, a true successor and that every true successor equal it. It is not merely an at-most-one condition.

`BooleanDFA.dest` performs finite `List.find?` search. Although its total definition has a fallback `B.zero`, `dest_true` proves that the fallback-none branch is impossible under `OneHot`: a true successor must occur in the complete finite list. `dest_iff` uses uniqueness to identify every true successor with the selected successor. `transition_iff` consequently provides both directions of correspondence between an original Boolean transition and the extracted deterministic machine.

`checkRow_iff` reflects both existence and uniqueness, and `checkOneHot_iff` reflects the entire `OneHot` predicate over all states and all 19 symbols. This matches the original learner's pseudo-Boolean exactly-one constraint, `PbEq(..., 1)`.

An important usage boundary is preserved: `checkHorn B.toDFA rb = true` establishes closure of the extracted deterministic machine even if the raw Boolean array is malformed. Faithfulness to the original array additionally requires `OneHot` or `checkOneHot B = true`. The source makes that premise explicit in the transition correspondence lemmas. No theorem silently claims raw-array faithfulness without it.

### 6. Pair symbols, center slots, and padding are distinguished correctly

The actual pair alphabet is `0..18`, represented by `Fin 19`. A valid center is either `none` or an even natural value below 19. `centerCode` sends `none` to slot 0 and `some v` to `v / 2 + 1`; in particular `some 0` uses slot 1, not slot 0. The ten valid even values `0,2,...,18` occupy slots 1 through 10. These are exactly the original 11 final slots.

`centerCode_lt` establishes the final-array bound under `CenterValid`. `edge_input_lt`, `edge_output_lt`, `terminal_input_valid`, `terminal_output_valid`, and `terminal_extra_lt` obtain every label bound from the previously checked literal graph and its arithmetic definitions. The output proof accounts for the delayed digit via `state_delay_lt`; it does not assume an unproved universal bound on arbitrary ambient states.

`BooleanDFA.toDFA` rejects invalid centers and totalizes transitions on naturals outside the pair alphabet by retaining the current state. The correspondence lemmas restrict their claims to valid centers and symbols. The historical Python witness routine's symbol 19 is padding that leaves the witness state unchanged; it is not a twentieth actual transition symbol. No proof confuses that witness encoding with the 19-symbol DFA array or relies on a graph edge labeled 19.

### 7. The original 46 relation rows are lifted faithfully

`Encoding.TableIndex` is `Fin Table.states.length`, and `Table.states_length` supplies the value 46. `stateIndex?` uses terminating `List.finIdxOf?`; `stateAt_injective` derives uniqueness from the existing `states_nodup` theorem. The exact inverse lemmas establish that looking up a table state returns its original index, including the actual initial rows 0 and 1.

`liftRelation` reads the selected raw row and returns false outside the literal table. `liftRelation_stateAt`, the two initial-state equalities, and the membership/index equivalences prevent silent row permutation or collapse. Making the relation false outside the table does not lose a needed transition: `accepting_states_mem`, table closure, and `graphAccepts_iff_accepts` establish that every complete accepted path remains inside the table.

The existing graph proof uses the literal finite state, edge, and terminal tables with soundness and completeness, not merely their cardinalities. The independent data check additionally confirmed exact equality and original order for all **46 states, 872 edges, and 251 terminal rows**, with no duplicates. Counts alone were not treated as evidence of identity.

### 8. Terminal extra-pair handling covers all four parity/overflow cases

The Horn terminal obligation evaluates:

```lean
M.final (M.run b r.extra.toList) r.outputCenter = true
```

This consumes the extra pair before checking the final center. `pathOutput` places `r.extra.toList` after the normal emitted pair list, and `horn_accepting_output` uses `DFA.run_append` to identify the same order. No extra pair is discarded or accidentally treated as a center.

| Input width and carry | Extra output pair | Output center | Output width |
| --- | --- | --- | --- |
| Even, no overflow | None | None | `L` |
| Odd, no overflow | None | Twice the computed center digit | `L` |
| Even, overflow | None | Twice the delayed middle digit | `L + 1` |
| Odd, overflow | Computed center digit plus delayed digit | None | `L + 1` |

`terminal_extra_center_none` explicitly proves that a nonempty extra field forces `outputCenter = none`. This matches the historical extra-terminal SAT clause, which reads the extra transition and then final slot zero. The one-digit case has no ordinary pair edges and reaches a terminal directly from one of the initial rows. Existing boundary theorems include `8` as the one-digit column sum producing center `16`, and `10` producing extra pair `[1]` with no center. These are existing source statements inspected here, not freshly executed tests.

The empty input is rejected by `Terminal`'s started-or-positive-center condition at an initial state. Interior zero pairs and an interior zero center remain allowed. Thus the positive-width and outer-nonzero constraints are neither missing nor overapplied to every position.

### 9. The numeric endpoint uses ordinary natural-number reverse-and-add

The semantic chain was traced to the definitions rather than inferred from theorem names:

1. `Lychrel196.reverseAux` repeatedly removes the least significant decimal digit and appends it to an accumulator. `reverseFuel_correct` proves the structural implementation agrees with it with sufficient fuel; `reverse10 n` supplies fuel `n`.
2. `Lychrel196.step n` is literally `n + reverse10 n`.
3. `DecimalDigits.Canonical n d L` requires `0 < L`, digits at most 9 in the used prefix, a strictly positive most significant digit, and the exact value equality `value d L = n`.
4. `reverse10_value`, `step_value`, and the numeral-value/carry identities connect fixed-width digit reflection and addition to that ordinary numeric function. Leading zeros in the reversal are handled by numeric value; no unsupported padded-input convention is introduced.
5. `FoldedDecimal.representation_next` constructs canonical result digits with `nextWidth q L`, choosing exactly `L` when the final carry is zero and `L + 1` otherwise. For canonical inputs, the final carry is proved to be 0 or 1. The non-overflow output retains a positive leading digit; the overflow output has leading carry 1.
6. `Agent107.FoldedTransducer.canonical_step_path` derives admissibility from canonical digits and supplies a complete path whose output equals the folded column word of the actual next integer.
7. `Agent107.FoldedDFA.horn_canonical_step` applies the generic Horn theorem to that path. It concludes existence of canonical digits for the exact `Lychrel196.step n`, at the genuine next width, whose folded word is accepted.

`horn_next_closed` separately gives the all-width symbolic closure theorem under `Admissible L q`. This premise includes positive width, a positive outer column, pair bounds, symmetry, and the evenness of a self-reflected center. These hypotheses are appropriate for the symbolic-to-numeric bridge. The canonical endpoint derives admissibility and does not require a user to assume numeric invariance or the desired output acceptance.

The theorem concerns a single step for every canonical accepted input. It can be applied repeatedly because its output is again canonical, but the PR does not introduce an unconditional orbit claim. It also does not claim a result about zero, since zero has no representation satisfying this positive canonical convention.

### 10. Scope, vacuity, and absence of a concrete safe instance

The advertised registry scope is generic and conditional. No particular Boolean assignment, Horn relation, accepted seed, safe invariant, or solution of the decimal 196 problem is supplied by the seven modules. In particular, the original learner also contains a bad-language monitor, nonemptiness or seed constraints, finite negative labels, and solver procedures; this PR's closure theorem does not purport to formalize or discharge all those obligations.

An empty accepted language can satisfy the Horn closure condition. This is ordinary vacuity of a conditional preservation theorem, not a false proof of nonemptiness. Likewise an all-accepting machine can be closed while unsafe. The new source explicitly says no safety or nonempty-language premise is silently supplied, and its endpoint signatures agree with that statement.

The components can be used together by supplying a positive-state `BooleanDFA B`, a raw 46-row relation, a proof of `checkOneHot B = true` when raw-array correspondence is needed, and a proof of `checkHorn B.toDFA (liftRelation rawR) = true`. `checkHorn_iff` supplies the Horn certificate, after which the path and arithmetic theorems apply. There is no single new combined certificate-format theorem or parser for a concrete solver output, and no concrete safe instance is claimed. Neither is required for acceptance of this precisely scoped generic result.

No inconsistent premise, circular closure assumption, finite-sampling substitution, missing positivity hypothesis, center-width mismatch, state-row mismatch, or dropped terminal extra transition was found.

## Strict-proof evidence and remaining operational limits

The comment-stripped scan found no active `sorry`, `admit`, `sorryAx`, `native_decide`, `axiom`, or `unsafe` token in the 19 pinned Lean sources. Finite facts in the inspected graph and alphabet files use ordinary `by decide`, not `native_decide`. The new proofs use ordinary proof terms and tactics; no external SAT result is imported as an axiom. The inherited indexed-history existence proof visibly uses `Classical.choose`, which is a permitted foundational dependency rather than an unsupported mathematical axiom.

The scoped registry permits exactly `propext`, `Classical.choice`, and `Quot.sound`. Source scanning alone cannot determine the actual transitive axiom set of elaborated declarations, and `#print axioms` commands in a source file are requests for evidence, not their output. **The reviewer does not certify fresh compilation or the transitive axiom audit.** Root must attach its actual pinned fresh build/audit result, including the seven modules and registered dependencies, before using this semantic verdict in a delivery packet.

This review is tied to H and its exact dependency bytes. It does not certify the prospective H+B combined tree, a later source head, current branch ownership, draft promotion, required checks, platform review eligibility, or merged target state. A substantively changed theorem or dependency requires assessment of the affected gap. Unrelated coordination metadata changes do not invalidate unchanged mathematical evidence by themselves.

### Delivery disposition

| Item | Result / next owner |
| --- | --- |
| Independent semantic review | PASS at H, with the scope and limitations above |
| Source repair by this reviewer | None; no blocking semantic defect found |
| Fresh Lean execution by this reviewer | NOT_RUN, intentionally assigned to root |
| Transitive compiled axiom audit by this reviewer | NOT_RUN; root owns actual canonical/strict evidence |
| External publication by this reviewer | None; only root may publish this review under the delegated authorization |
| Merge / ready transition by this reviewer | None |
| Next delivery action | Agent #9 combines this exact-source review with actual verification and base-compatibility evidence, then advances PR #177 through the authorized writer and platform gates |

## Source pins

All paths below are repository-relative at H. The seven new modules have these exact identities, independently rechecked against the supplied local manifest:

| Module | Git blob | SHA-256 |
| --- | --- | --- |
| `proofs/Agent107DFA.lean` | `80886bfb2a9ac9fb579a609132e4c1212d355164` | `d0fe8accc9d80110230ea3b4061f554d8d9d9dc5b8ea1a89f44e7d2fc977969e` |
| `proofs/Agent107DFAHorn.lean` | `01b9d2cbe417d90c5879ac1f378fba65627866c0` | `e443d30c868d50de911662b885354e53853b7802f415fc41a09ba2317b2974a7` |
| `proofs/Agent107DFAChecker.lean` | `941bf379c7798398bf82c66cce3dcb88828c17f7` | `a9a411034cf44aeb9752c85246d05140067b88c2c00b5c62651d423af1be2238` |
| `proofs/Agent107DFAAlphabet.lean` | `e526b3b7ecda09cf804575a4c394c210a479fc0c` | `64f13d225a8d4439d0e69384b01138173006897f3c5536708c953d3ae25aa534` |
| `proofs/Agent107DFABoolean.lean` | `af2df3da241c01b66317869dee1c26ad7b2f9b03` | `3ffcc064a10c455128f5d39ff82a756f1045e2137ab0aff92ded9e929f462e9b` |
| `proofs/Agent107DFARelation.lean` | `c5df077e095550189168b1452796a5679ed92405` | `64d8606e1592428cb184b40e5cd2650175c78411a046a68c72f2a24a78a2b748` |
| `proofs/Agent107DFAArithmetic.lean` | `43c3d7978c716898e5e35643b51a05f6ad2f81a4` | `10c24e67d811fcda392de2e473cf907793da82a12d0fd5cfc4dc890b50b40169` |

The remaining 12 Lean dependency blobs are pinned in the verified local `source-manifest.json` and the exact-head registry. For self-contained dependency identification:

| Dependency | Git blob |
| --- | --- |
| `Agent107TransducerDefs` | `03b290b828321dc9144a8741990f7089f07ece53` |
| `Agent107TransducerInput` | `55a811ec593ba8f0ccea5290e8ef8b6f53c46bb3` |
| `Agent107TransducerPath` | `990a8c083bdb44955b434e25ba6fff4dc73ea124` |
| `Agent107TransducerNumeric` | `f27fb02b4b422af06e55ee288cc9f8ecd50a8552` |
| `Agent107TransducerGraph` | `f7925c5afa2983d95942cf98f6100221a659417a` |
| `Agent107TransducerOutput` | `f4cda74629b74db4ed8e4d9f98825e5eb70cb217` |
| `Agent107TransducerTablesChecks` | `0461201189bdd1ddd78a1e44a284abce4c1e5c66` |
| `Lychrel196Research__c696e0ea3db39d92.lean` | `c6c1f5441c54a36f2d82b3ef78dff1ccdbc5a506` |
| `Agent107TransducerTables` | `4eeb388160245c1057debc70c49d24f586832a2b` |
| `Agent107TransducerReachable` | `7ecaee195da124b420a91590fcfdd274bcf39a87` |
| `Agent107TransducerBoundary` | `7c46227bc4fd31517ee016ba35bbca2385a0f2fe` |
| `Agent107TransducerTablesData` | `afc8b382cfe84b2660ef0e559901b8baf136885d` |

Registry path: `proofs/contributions/agent-107/dfa-horn-closure-20261016/verification/Agent107DFAHorn.verify-registry.json`; Git blob `62993f22fe4085b080dd6725ec5d7c580cea5939`; SHA-256 `791d9d1595c50de05ed044e8d1186313a1c78c643280cf64fd794c6bc0cf6e83`.

Verifier path supplied to root: `proofs/verify_project__214bf7673efe116b.py`; Git blob `21131b03dfa516eb19a0a7a4df4f2a41020d4db1`; SHA-256 `c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a`. Its byte identity was checked here; its execution and infrastructure correctness are not claimed as part of this semantic review.

Original algorithm sources fetched at H:

| Source | Git blob | SHA-256 |
| --- | --- | --- |
| `proofs/creative_regular_direct__8988fd8c6a0aad92.py` | `5658e577de22431ee029cf49c2ff640321dc0d8a` | `93514df6e6041ccf4c962008f1613bb468dd476f93e8388e6315e8e1d548d294` |
| `proofs/creative_regular_boolean__20252ce462a75640.py` | `e2a43e55da0c512dbbf3c1ed03666afebc82b1c3` | `d560f652f9900fb85cc3f93cceda74993ebf41ddfff80e75b59a89dc2ecf2a58` |
| `proofs/creative_regular_invariant__ea923cdb26a39825.py` | `fa334ba0f094998c206f1eccc529b375c1c5351b` | `c162a35227715b5c102fff8fa038603df0bb30d7f35f2a694eade81c7a83f312` |

## Preserved finite-data and source-scan output

The independent read-only Python check completed with exit status 0 and produced:

```text
Manifest identity: all 22 files match byte counts, SHA-256, and Git blob IDs.
Literal finite graph: exactly 46 unique states, 872 unique edges, 251 unique terminals; all match the independent arithmetic enumeration in exact original order.
Alphabet/terminal bounds: all input/output pairs are 0..18; all centers are None or even 0..18; every extra pair has output center None.
Finite-table proof templates: all 46 blocks match the six inspected soundness/completeness/separation statements by uniform index substitution.
Static active-token scan: no sorry/admit/sorryAx/native_decide/axiom/unsafe in the 19 Lean source files. This is not a transitive Lean axiom audit or compilation.
```

The independent enumeration used these rules directly from the inspected original arithmetic semantics, with no execution of repository source:

- Start with states `(0,0,0,-1,false)` and `(1,0,1,1,false)` in that order; enumerate states in discovery order.
- For each state `(e,a,c,t,started)`, enumerate `q = 0..18`, except require `q = 1..18` before the first pair, and enumerate backward carry `b = 0,1`.
- Keep precisely `(q+b)//10 = c`; let `lo=(q+a)%10` and `hi=(q+b)%10`; emit `lo+t` for overflow and `lo+hi` otherwise; use target `(e,(q+a)//10,b,hi if e else -1,true)`.
- For each resulting state enumerate center `None,0,2,...,18`; reject `None` and zero before starting. For no center, require `a=c` and emit center `2*t` only on overflow. For a numeric center `v`, require `(v+a)//10=c`; on overflow emit extra `(v+a)%10+t` and no center; otherwise emit center `2*((v+a)%10)` and no extra.
- Compare the entire resulting ordered lists with every parsed literal row; separately verify uniqueness and all label bounds. No finite set of input words was substituted for an induction or a universal path claim.

The structural proof-block check normalized only numeric suffixes attached to the row/state/edge/terminal identifiers and compared all 46 resulting blocks with the inspected six-statement block. The scan stripped nested Lean block comments and line comments before examining active prohibited tokens. These procedures are supplementary review evidence; the actual Lean declaration and axiom evidence remains a separate required delivery record.

## Raw-program preservation supplement

The exact original finite-data/source-scan Python program, its exact original shell command, returned combined output, and exit-code record are preserved under `semantic-evidence/`. The original program was recovered from the visible tool call, not reconstructed from the algorithm description above, and was not rerun for preservation. The original GitHub source-identity program and its raw result, persisted connector records, and byte-identical historical comparator sources are also retained there. See `semantic-evidence/README.md`, `semantic-evidence/manifest.json`, and the two `original-*.execution.json` records.

There were no substantive failed execution attempts in the original mathematical/data review. `semantic-evidence/failed-attempts.json` records that fact and separately preserves the later directory-inventory result reporting that the evidence directory did not yet exist. Generated preservation files, historical Python source copies, and reviewer programs are explicitly excluded from the accepted 19-module Lean source closure. This supplement changes preservation completeness only; the mathematical verdict and its execution limitations remain unchanged.
