# Independent semantic and execution review of PR #127

Reviewer: Agent #13 /root/review127, a genuine nonauthor reviewer. The reviewer made no source edits and performed no remote mutation. This review does not establish a distinct GitHub account or an eligible platform APPROVE.

Reviewed head H: c68b0aaa5344f2cc646c035e2efca187852cb57d.
Checked integration base B supplied for this review: 1ee9123344dbe17e9bda224ff8af5b1cbb2b64e4.
The parent integration agent owns current-target combination and all incoming-file publication checks. The supplied combined tree is 8e5190dcb621fc976cd2afbd13dccfa122a25bed; no claim is made here that this reviewer constructed it or rebuilt unrelated accepted projects.

**Disposition: PASS for the exact selected mathematical closure; COMMENT recommended.** See the execution and audit evidence below for the actual result and preserved failures.

## Source meaning and advertised domain

The five new modules are AdjacentBirths, OverflowDigits, ActualOverflowBirths, OverflowEndpoints, and CanonicalOverflowBirths. I read them in full, together with all eight original dependency modules, PROJECT_REGISTRY.json, dependencies/SOURCE_PINS.json, README.md, the original canonical verifier, the historical author/reviewer build and continuation programs, and the relevant rejected canonical and reviewer fixture/audit evidence. The accepted-base AGENTS.md and proofs/PUBLICATION_POLICY.md retain the requirement to preserve failed research and prohibit claiming a solution of the 196 problem without the missing all-time argument.

All new arithmetic and actual birth classifiers quantify over an arbitrary integer base b with 2 <= b. The old coefficient word xs is a finite List (Int × Bool) of length L. ResetNormalization.Bounded means precisely that every first projection is in [0, 2*b-2]. Coefficient symmetry means (xs.map Prod.fst).reverse = xs.map Prod.fst; no equality of the Bool tags is assumed.

The actual carry and digit APIs are unchanged originals. ResetNormalization.ordinaryTags replaces every Bool by false. PhysicalWidth.terminal recursively applies integer Euclidean division to q+incoming; ActualBaseBirths.incoming b xs k is that terminal computation on the first k ordinary columns, starting at zero. PhysicalWidth.actualDigits normalizes ordinary tags and chooses physical width using the actually computed terminal carry. The reset-placed comparison list is not substituted for the ordinary output. [Original normalization definitions](inputs/project/dependencies/ResetNormalization.lean); [original actual-width definitions](inputs/project/dependencies/PhysicalWidth.lean); [original carry API](inputs/project/dependencies/ActualBaseBirths.lean).

## Exact width, indices, and carry coupling

The explicit overflow hypothesis is terminal b 0 (ordinaryTags xs) = 1. The new proof expands the unchanged actual-width definition, proves actualDigits = body ++ [1], and obtains actual output length L+1. The empty source cannot satisfy the hypothesis because its terminal computation is zero. These structural statements do not rely on positivity or boundedness assumptions that their types omit.

At a strict interior index 0 < i < L, ReverseAdd.pairs pairs actual digit i with actual digit (L+1)-1-i = L-i. Both indices lie in the old-width body. Old coefficient symmetry turns coefficient q_(L-i) into q_(i-1). Consequently the exact pair expression is
Q_i = (q_i+c_i) % b + (q_(i-1)+c_(L-i)) % b,
where Q = pairs (actualDigits b xs).

This shift is essential: the no-overflow reflection L-1-i would give a different expression. The Lean proofs establish each subtraction and access bound before converting getElem or getD. Neither the strict interior classifiers nor the endpoint identities derive a birth from an out-of-range default zero.

Writing a=q_(i-1), z=q_i, u=c_i and v=c_(L-i), the two surrounding carry equations supplied to the local arithmetic theorem are
u = (a+c_(i-1))/b and v = (z+c_(L-i-1))/b.
The second equation uses original coefficient symmetry. The surrounding prefix carries satisfy the bit bounds by the unchanged incoming_bit theorem. u and v are therefore computed carries, not independent guessed bits. [OverflowDigits](inputs/project/OverflowDigits.lean).

## Exact alternatives and neutrality

The zero classifier is a biconditional with exactly these oriented alternatives:

1. a=0 and z=0.
2. a=b-1, z=b-1, u=1 and v=1.
3. a=b-1, z=b and u=0.
4. a=b, z=b-1 and v=0.

The maximal classifier Q_i=2*b-2 is a biconditional with exactly these alternatives:

1. a=2*b-2 and z=2*b-2.
2. a=b-1, z=b-1, u=0 and v=0.
3. a=b-1, z=b-2 and u=1.
4. a=b-2, z=b-1 and v=1.

The apparent omission of one intermediate carry in the mixed rows is intentional: the division equations and coefficient bounds determine the necessary restrictions. The local proof first shows both residues are nonnegative and below b. A zero sum forces both to zero; a maximal sum forces both to b-1. The existing one-column classifier plus the real coupled division equations then yields all four rows. Splitting carry values into zero and one is valid uniformly at b=2, and the inherited b>=3 rigidity results are not used to extend a restricted assertion to the binary case.

A new extreme excludes only the corresponding homogeneous old adjacent extreme pair. Eliminating that first row proves the necessary neutral-neighbor condition a=b-1 or z=b-1. It is not a sufficient condition, a statement about arbitrary predecessors, or an ancestry/lifetime invariant. The without-neutral corollaries correctly give exactly the two inherited homogeneous cases when neither neighbor equals b-1. [AdjacentBirths](inputs/project/AdjacentBirths.lean); [ActualOverflowBirths](inputs/project/ActualOverflowBirths.lean).

## Endpoints and the binary exception

The actual first digit is q_0 % b because c_0=0; the actual highest digit is the appended one. Pair symmetry therefore gives both genuine endpoints Q_0=Q_L=1+q_0%b. These endpoint identities require neither symmetry nor coefficient bounds.

For every b>=2, integer Euclidean remainders are nonnegative, including for signed q_0, so the endpoints are strictly positive. For b>=3, q_0%b<b implies 1+q_0%b<=b<2*b-2; neither endpoint can be maximal. These facts correctly retain no bounds or symmetry premises.

Identifying the binary old coefficient itself requires the original coefficient bound. If 1+q_0%b=2*b-2 and b>=2, the remainder upper bound forces b=2. Under 0<=q_0<=2, odd remainder forces q_0=1. Conversely b=2,q_0=1 gives the maximum. The actual endpoint maximum theorem first proves the head is a real source element from terminal one, then inherits its bound. Dropping that bound would be false: the retained rejected-generalization control q_0=3 at b=2 has terminal one and maximal endpoints although q_0 is not one.

Width L=1 is included. There are no indices 0<i<1, but the real output still has two endpoints, at 0 and 1. At b=2 the bounded singleton coefficient 2 produces actual digits [0,1] and paired endpoints [1,1]; the binary maximum criterion does not force an impossible q_0=1 overflow for that singleton. [OverflowEndpoints](inputs/project/OverflowEndpoints.lean).

## Canonical ordinary reverse-add specialization

The final wrapper quantifies over finite input digits with ReverseAdd.DigitBounds and PhysicalWidth.PositiveLast, tagged coefficients with the literal equality xs.map Prod.fst = ReverseAdd.pairs digits, and the computed terminal-one hypothesis. It derives coefficient bounds and symmetry rather than assuming an arbitrary new coefficient model. Taking lengths of the projection equality gives xs.length=digits.length.

The proof directly applies unchanged ReverseAdd.reverse_add_normalization. It retains valid output digits, a positive highest output digit, output width digits.length+1, and the numerical equality
eval b output = eval b digits + reversedValue b digits.
The original evaluation is least-significant-digit-first Horner evaluation, and reversedValue evaluates the reversed finite digit list as an integer. Zeros that become high zeros on reversal have zero contribution. Thus this is the ordinary one-step integer reverse-and-add interface, with the original representation semantics.

The wrapper then combines endpoint equalities, endpoint positivity, the exact binary endpoint maximum equivalences, and every strict-interior zero/max/necessary-neutral assertion. Its indices cover the entire output: 0, 0<i<L, and L. It imposes no unnecessary L>=2 premise and does not confuse absence of an interior at L=1 with absence of endpoints. [CanonicalOverflowBirths](inputs/project/CanonicalOverflowBirths.lean); [original reverse-add interface](inputs/project/dependencies/ReverseAdd.lean).

## Rejected history and scope boundaries

The rejected canonical attempt differs from the accepted canonical source by a redundant dsimp only after intro i hi0 hi. The rejected compiler log reports 'dsimp made no progress' and sorryAx from elaboration recovery. That source and log must remain historical and outside the accepted build. The later source removes only that redundant command. Historical final-001 project compilation and final-003 fixture/audit continuation are separate events; copied historical objects cannot be called fresh.

The historical reviewer fixture failed first on membership elimination, and its next audit attempt failed on the unsupported display option pp.width. Those failures are not accepted audit passes merely because some subsequent log lines list allowed axioms. This independent review subsequently established its own fresh result with explicit trust zero, as recorded below.

The scope is one finite reverse-add step. No theorem in the selected new modules asserts run population, growth, ancestry, lifetime, global palindrome avoidance, or the 196 conjecture. Counts of endpoints and generated declarations are audit metadata, not counts of independent major results.


## Fresh verification result

**PASS for the selected thirteen-module mathematical closure at H. No mathematical blocker was found.** This is an independent nonauthor review and a COMMENT recommendation. It does not establish an eligible GitHub APPROVE, an unaffiliated reviewer account, a repository-wide PASS, or an integration action by this reviewer.

The machine result is [analysis-004/FINAL_RECEIPT.json](analysis-004/FINAL_RECEIPT.json). Every actual compiler invocation and complete raw stdout/stderr path is recorded in [analysis-004/COMMANDS.json](analysis-004/COMMANDS.json). The final analysis executes no Lean command; it validates the retained successful audit execution and the original fresh build without relabeling earlier failures.

### Exact source and runtime binding

All 13 modules independently matched the frozen registry SHA-256, Git blob identity, H tree binding, and materialized Git object bytes. Each of the eight original dependency pins also matched its original path at commit `98d59927ad89c42f438ea857ec5750a0df3b91db`. Source paths, complete hashes, import lists, and fresh object identities appear in [analysis-004/SOURCE_IDENTITIES.json](analysis-004/SOURCE_IDENTITIES.json); the read-only Git commands and their original results are retained in [SOURCE_IDENTITY_READONLY.json](SOURCE_IDENTITY_READONLY.json). That earlier record correctly retains its then-current LEAN_NOT_RUN label.

The frozen registry SHA-256 is `138fc4ac68beb8188812db092aae722476475dbb9644eb2e03d586fa5d6e733e`; dependency SOURCE_PINS SHA-256 is `622f800279123b95c201068640216dfb36f49629c0778af406243ca9082cf083`. The canonical verifier was read before reuse of its comment/string masker; its exact source SHA-256 is `c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a`. This was a custom independent review execution using the registry and inspected canonical parsing code, not an asserted repository-wide canonical-verifier run.

The runtime reported Lean 4.19.0, commit `6caaee842e94`. The executable SHA-256 was `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. The executable, recorded runtime libraries and Lean/Std root objects, every selected source copy, every fresh compiler object, and all execution logs were hash-checked against their retained identities. Final before/after checks were identical. The selected modules use Std and the eight original dependencies; no mathlib environment was used. Distribution library objects were used as pinned runtime inputs, not described as freshly rebuilt project modules.

### The single fresh project build and audit recovery

The fresh source directory began with zero project objects. Between 23:16:01 and 23:16:33 UTC on 2026-10-16, the reviewer executed exactly one complete 13-module build. Every project command exited zero and used:

```text
/tmp/p196-agent5-lean/lean-4.19.0-linux/bin/lean --trust=0 -j1 -DElab.async=false -o MODULE.olean MODULE.lean
```

The actual working directory and LEAN_PATH were the private `fresh-001/source` directory. All 13 project objects were created there by this reviewer. Subsequent audit-only attempts reused those same hashed objects without copying or recompiling them. No historical author/reviewer project object was imported.

All failed stages remain failed in their original immutable receipts:

| Stage | Actual result | Retained interpretation |
| --- | --- | --- |
| Initial disk pause | Lean NOT_RUN | Parent reported actual ENOSPC; read-only semantic work continued until an approved private tmpfs became available. |
| Initial artifact setup | Process NOT_STARTED | A command exceeded the argument-length limit. The exact rejected command and split recovery inputs are retained. |
| fresh-001 | 13 project modules passed; audit failed | The audit traversal lambda lacked explicit RecursorRule parameter types. Lean declined to evaluate the recovered erroneous audit; no evaluation bypass was used. |
| audit-002 | Audit failed | The reviewer incorrectly treated an inherited partial compiler implementation helper as a safe definition. |
| audit-003 | Lean audit exited 0; wrapper postprocessing failed | Complete audit data was produced. The wrapper incorrectly assumed all compiler implementation helpers must originate in inherited modules. |
| Later artifact write | Process NOT_STARTED | Another oversized archival command was rejected before execution; the exact command and lossless recovery are preserved. |
| analysis-004 | PASS | Existing successful audit output was independently parsed and validated. No Lean execution or mathematical-source change occurred. |

The audit-003 Lean invocation ran at 23:24:29–23:24:42 UTC and exited zero. Its raw stdout is 2,052,724 bytes with SHA-256 `b92d73dda709195107bb6f22e08bf73de18d66558ceb64390edd6d6e83705b0a`; stderr is empty. The final postprocessing passed at 23:30:50–23:30:51 UTC. Repairs affected only reviewer audit code or classification of implementation helpers. The allowed-axiom set and the rejection of unsafe/partial dependencies in accepted proofs were unchanged. [Successful audit source](audit-003/IndependentAudit003.lean); [complete raw stdout](audit-003/logs/00-IndependentAudit003.stdout); [postprocessor](finalize_audit_004.py).

### Exhaustive declarations, full types, literal axioms, and dependency graph

The audit enumerated declarations by their actual imported module origins, including generated proof constants. It used checked-environment declaration data for accepted logical roots. For each theorem and genuinely safe definition it collected transitive axioms and exported its complete pretty-printed type, universe parameters, and direct type/value dependencies. All 33 new registered public theorem endpoints also received literal `#check` and `#print axioms` output; these literal axiom sets matched the independently parsed programmatic collection. Type output used `pp.all` and was checked for printer elisions.

| Module | All constants | Theorems | Safe definitions | Unsafe constants | Partial implementation definitions | New public endpoints |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| BaseBirths | 30 | 27 | 1 | 2 | 0 | 0 |
| SignedDigitUniqueness | 41 | 27 | 6 | 7 | 1 | 0 |
| BaseReflection | 81 | 41 | 12 | 26 | 2 | 0 |
| ResetNormalization | 80 | 54 | 9 | 15 | 2 | 0 |
| AdjacentBirths | 29 | 26 | 1 | 2 | 0 | 8 |
| PhysicalWidth | 83 | 54 | 12 | 14 | 3 | 0 |
| SeamSafety | 14 | 9 | 1 | 4 | 0 | 0 |
| ReverseAdd | 35 | 26 | 3 | 6 | 0 | 0 |
| ActualBaseBirths | 24 | 19 | 1 | 4 | 0 | 0 |
| OverflowDigits | 25 | 25 | 0 | 0 | 0 | 12 |
| ActualOverflowBirths | 9 | 9 | 0 | 0 | 0 | 4 |
| OverflowEndpoints | 19 | 19 | 0 | 0 | 0 | 8 |
| CanonicalOverflowBirths | 2 | 2 | 0 | 0 | 0 | 1 |
| **Total** | **472** | **338** | **46** | **80** | **8** | **33** |

The observed theorem count 338 agrees with the prior count, but that prior value was never used as a proof of coverage or a PASS assumption. The complete inventory and actual module coverage establish the count.

The 338 theorem constants and 46 safe definitions form 384 accepted roots. Their exact transitive type/value dependency closure contains 2,241 constants; traversal also includes recursor-rule right-hand sides. No reachable node is unsafe or partial. Every exported edge resolves inside the graph, and a separate Python traversal reproduces exactly the exported node set. The graph's axiom nodes and the independently collected union agree exactly:

```text
Classical.choice
Quot.sound
propext
```

There is no accepted dependency on sorryAx, an unsupported custom axiom, or native_decide justification. The selected mathematical source remains unchanged. [All declarations](analysis-004/DECLARATIONS.json); [full public endpoint types and literal axioms](analysis-004/PUBLIC_ENDPOINTS.json); [complete dependency graph](analysis-004/DEPENDENCY_GRAPH.json).

### Complete unsafe and partial implementation inventory

Lean distinguishes safe, unsafe, and partial definitions. Testing only `isUnsafe = false` would incorrectly include partial compiler implementation definitions among safe definitions. The final audit separately inventoried all 88 implementation helpers: 80 unsafe constants and 8 partial definitions. Every one is absent from the full dependency closure of every accepted theorem and safe definition.

Of the 80 unsafe constants, 76 are compiler implementation definitions and four are inherited implementation axioms:

- `List.mapTR.loop._at.BaseReflection.residual._spec_1`
- `List.mapTR.loop._at.ResetNormalization.ordinaryTags._spec_1`
- `List.mapTR.loop._at.BaseReflection.cs._spec_1`
- `List.mapTR.loop._at.BaseReflection.qs._spec_1`

The eight partial helpers are `_unsafe_rec` implementation counterparts of original definitions. In total, 86 implementation helpers originate in the eight original dependency modules. The two remaining helpers are newly generated compiler-stage versions of the sole new safe definition `P196.Agent7.AllBaseOverflow.adjacentPair`:

- `adjacentPair._cstage1`: unsafe definition of type `Int → Int → Int → Int → Int → Int`, with direct dependencies `Int.emod`, `Int`, `Int.add`, and `Int.ediv`.
- `adjacentPair._cstage2`: unsafe definition of type `_obj → _obj → _obj → _obj → _obj → _obj`, with direct dependencies `_obj`, `Int.emod`, `Int.add`, and `Int.ediv`.

These two helpers are explicitly classified as new compiler implementation artifacts. They are not described as inherited or as accepted proof dependencies. The final parser requires these exact names, types, safety classifications, and dependency sets; it continues to reject every unsafe or partial node reachable from accepted roots. Their classification resolves the reviewer's earlier overly strict origin assumption without changing any mathematical criterion.

The historical inventory of four unsafe axioms was narrower than the full unsafe/partial implementation inventory. This review supplies the complete inventory, including the 84 non-axiom implementation helpers. An empty axiom array in an implementation-helper record is explicitly marked NOT_APPLICABLE_IMPLEMENTATION_HELPER and is not represented as a successful logical axiom audit. [Complete implementation inventory](analysis-004/IMPLEMENTATION_INVENTORY.json); [inspected Lean declaration API](inputs/runtime-inspected/Lean/Declaration.lean); [inspected axiom collector](inputs/runtime-inspected/Lean/Util/CollectAxioms.lean).

## Review disposition and publication boundary

The exact five-module addition and its original dependency closure support the advertised finite one-step claims, including binary endpoints and length-one boundary behavior. No source correction is requested. This is a COMMENT review by an independently reasoning nonauthor agent using the available account context. The reviewer has not submitted a GitHub review, approved, merged, pushed, edited coordination files, or published to issue #61.

The parent integration agent remains responsible for all incoming-file/provenance preservation, the current-target combined tree, and external publication. This result is bound to the exact selected source hashes at H; it does not independently certify unrelated projects or future source changes. Compiler objects remain preserved in the private working directory and are explicitly excluded only from the transport archive as reproducible outputs. All substantive source, audit data, complete execution logs, scripts, rejected attempts, final reports, and recovery instructions are included in the packet manifest.
