# Final independent semantic review: complete binary spectral carry charge

## Decision and exact reviewed target

**PASS — independent source-semantics review, with no remaining semantic blocker in the reviewed scope.** Finding R1 is resolved by explicit source-formula correspondence theorems and the two literal zero-if-and-only-if endpoints.

Reviewer: `/root/ownership_scout`, continuing the ownership and semantic-review assignment for Agent15 session `43cf6e114472`. The reviewer is a nonauthor: no author Lean source, task claim, Git branch, remote issue, or remote review was written or modified by this reviewer. The scope reservation was reported by the parent at coordination commit `9ff01fb85383833abe440d7f41bc7c249c332070`, task-file blob `70340af5e48d1c965d012180c04bc6ea01f90b21`.

The reviewed frozen source is:

- Repository: `taco-jpg/p196-algorithm`.
- Commit: `e8d706dc8a67248e1531b0b828fbe05ff50052ed`.
- Tree: `2d447634e0ff42b4275d34bfb169101bba0ed130`.
- Package: `proofs/contributions/agent-15/spectral-carry-charge-43cf6e114472`.
- Source review snapshot: `source-snapshot-004`.

This decision is a semantic judgment about the exact source below. The reviewer did not run Lean, `check.py`, a public-axiom audit, or a module-origin audit. Independent kernel and audit acceptance belong to the separate runtime reviewer; this report does not substitute for those gates.

## Frozen-source identity verification

After the parent froze the remote commit, the reviewer independently fetched all eleven top-level package files through the GitHub connector with that exact commit as `ref`. Every response was preserved. For each file, the reviewer encoded the returned content as UTF-8, recomputed both SHA-256 and Git's SHA-1 blob hash, compared the blob hash with the API's reported SHA, compared the complete bytes with snapshot004, and compared those bytes with the corresponding object read from the local frozen Git commit.

All eleven files passed all three identity comparisons: API blob identity, prior reviewed snapshot bytes, and frozen Git object bytes. The commit's tree was separately read as `2d447634e0ff42b4275d34bfb169101bba0ed130`. No ancestry conclusion is drawn from the local shallow checkout.

| Mathematical source | Git blob | SHA-256 |
| --- | --- | --- |
| `SpectralWeights.lean` | `40afa93196976972e5c0f6772a18e50c1e635a3f` | `07b3831f17a0d2e43a7e27cfd8a63d364a98ccbbcef87362a20cfbf24fb49db1` |
| `BinaryCode.lean` | `35ba9bee5afb9bb47f39738e44860a02ea9b2469` | `8db88d52e00dddbd32610dc09b7f8833f1ec1dc623b82236060b67bd2c9171f9` |
| `ChargeSymmetry.lean` | `f69efd4bc0642759dddf99834d5d093c929761a5` | `28d11217cf147750ec2d07e64dbc6dabeee7deec7e543987817da611201b60a3` |
| `SourceFormula.lean` | `1db4a109629abddf355d12e8a14f2cfb0e26a39b` | `be165a538963922f6096e63934e5f3c1010d760cabc9e08baa96a0bb43c105d8` |
| `ChargeControls.lean` | `b7a1c9f7d0d175fb3f2abea93fcd23bd5eb082f8` | `bb23522ad6792dcf6b30ef010837eb1703f7eba59f4448e355282f8eb27f668c` |

The complete eleven-file list and all comparisons are in [the remote identity manifest](remote-freeze-e8d/MANIFEST.json). The other six files are `check.py`, `CONTRACT.md`, `README.md`, `BUILD.json`, `CLAIM.json`, and `lean-toolchain`. In particular, the reviewed checker has SHA-256 `f0da79f56ca4c2e24ff90700f3491d4999247f9b88db6cc306074ac84c646ab3`.

## Original mathematical source and exact scope

The original research source was inspected at main commit `5ff4f607535587d572fbc9e95ba9501d1fbe5fc5`, under:

`proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/research/`

| Original source | Exact blob | Reviewed role |
| --- | --- | --- |
| [creative_global_spectral_notes.md](https://github.com/taco-jpg/p196-algorithm/blob/5ff4f607535587d572fbc9e95ba9501d1fbe5fc5/proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/research/creative_global_spectral_notes.md) | `cb1c355fa05916a770816a4d5ef680e54079cccb` | Complete outgoing-carry convention and the stated domination/zero-symmetry claim. |
| [creative_global_spectral.py](https://github.com/taco-jpg/p196-algorithm/blob/5ff4f607535587d572fbc9e95ba9501d1fbe5fc5/proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/research/creative_global_spectral.py) | `730acd722bf017b6bf1e51e5a0411169a7804da4` | Exact U/S recurrences, parity, sign, mirror indices, and literal charge in `carry_coordinates`. |
| `astra_spectral_carry_quotient.md` | `eac5b8f61385a615d9cc3e7796a4d698c66b716b` | Adjacent research context; wider quotient/dynamical conclusions are outside this review. |

The original script has SHA-256 `393545516c13d41c0416e560ec37bab6b1c1655357ae351b0f960dea76ff7448`. Its blob was independently checked before the bounded design comparison. The original notes use the complete length-L outgoing carry word, including the last overflow bit. The separately specified initial incoming zero is not an extra first element of that word. A last bit equal to zero remains an element of the word.

For a complete word `cs`, let L be its length and m = floor(L/2). The claimed charge is:

- If L = 2m + 1: the sum over 0 <= i < m of `(cs[2m-i] - cs[i]) * U(m-i)`.
- If L = 2m: the sum over 0 <= i < m of `(cs[2m-1-i] - cs[i]) * S(m-1-i)`.

Subtraction and weights are integers. Both sequences satisfy `X(n+2) = 20*X(n+1) - X(n)`; U starts at 0, 1 and S starts at 1, 21. The formal endpoint says that this exact charge is zero if and only if the complete finite binary word equals its reversal. It applies to arbitrary binary words; it does not establish that any supplied word is extracted from a particular reverse-and-add computation. The empty word is an explicitly covered algebraic boundary case.

## Semantic assessment of the mathematical modules

### Recurrence weights and fixed-length binary evaluation

`SpectralWeights.lean` preserves the exact recurrence seeds and uses `oddWeight n = U(n+1)` and `evenWeight n = S(n)`. The shift in oddWeight is essential: the half-word evaluation must use U(m), ..., U(1), never an extra U(0) place. The positivity, growth, and strict prefix-sum domination statements supply the hypotheses needed by the binary coding argument.

`BinaryCode.lean` defines binary entries by the explicit predicate that each natural-number entry is 0 or 1. Its integer evaluation of `a :: xs` weights the head by `w xs.length`, so equal-length words are read with the highest applicable weight first. The injectivity theorem retains both binary-domain hypotheses, the equal-length hypothesis, nonnegative weights, and strict domination of the sum of smaller weights. A differing head contributes more than either allowable tail difference, while matching heads reduce the comparison to equal-length tails. The inspected source does not replace the binary restriction by an unrestricted natural-digit claim.

### Charge and full reversal

`ChargeSymmetry.lean` evaluates `cs.reverse.take m` minus `cs.take m`. Thus the sign is reflected right entry minus left entry, as in the original script. The ith place of either half receives weight `w(m-1-i)`; this becomes U(m-i) in odd length and S(m-1-i) in even length.

The half-word lengths are both m, which makes the fixed-length injectivity theorem applicable. The independent list argument `reverse_take_half_iff` then relates equality of those two halves to reversal of the complete word. It covers lower-half indices, reflected upper-half indices, the odd middle index, and the empty/singleton cases. The middle entry reflects itself, so no additional hypothesis fixes it. No condition forces the terminal carry to zero, and no leading incoming zero is inserted.

The exposed `carryCharge_zero_iff` retains the binary hypothesis and states symmetry of the entire supplied word. It does not assume the desired symmetry or a renamed zero-charge conclusion among its hypotheses.

### R1 resolved: exact original finite sums and their zero endpoints

The earlier source review identified R1 because a correct descending-weight implementation still lacked a literal formal correspondence with the original indexed sum. The frozen `SourceFormula.lean` now resolves that concern.

`sumFirst_eq_range_sum` identifies the recursive finite accumulator with the ordinary sum of the mapped `List.range`. The weighted-evaluation adapters expose the original indices, and `halfCharge_eq_source_sum` gives the complete-length mirror difference. The odd and even specializations retain their exact length equations, the right-minus-left sign, the shifted U weights, and the unshifted S weights.

The optional-entry default does not conceal an out-of-range term: the sum ranges over i < m, where both the direct and mirrored entries are in range. Empty sums use no entries. The odd arithmetic normalization from `m-1-i+1` to `m-i` is justified on the actual summation range.

Finally, `odd_source_charge_zero_iff` and `even_source_charge_zero_iff` state zero-if-and-only-if-full-reversal for those literal sums. Their hypotheses are the corresponding exact length equation and the binary predicate. The correspondence endpoints and these two corollaries close R1 at source-semantics level. Kernel acceptance of the proofs is a separate reported runtime result, not inferred here.

## Controls and what was actually executed

The frozen `ChargeControls.lean` contains nine named `by decide` theorem declarations. Their statements were inspected as part of the source review.

| Control statement | Purpose |
| --- | --- |
| Charge of the empty word is 0. | Empty boundary. |
| Charges of [0] and [1] are 0. | Singleton boundary. |
| Charges of [0,1] and [1,0] are respectively 1 and -1. | Sign and length-two weights. |
| Charges of [0,0,0] and [0,1,0] are 0. | Free odd center. |
| Charge of [1,0,0,1] is 0. | Even symmetry. |
| Charge of [0,1,0,0,1,1] is 419. | Literal asymmetric source example. |
| [1,0,21,0] has charge 0 and differs from its reverse. | The binary-domain restriction is material. |
| [1,1] has charge 0, while [0,1,1] has charge 1. | Prepending an incoming zero changes the convention. |
| [0,1,0] has charge 0, while [0,1] has charge 1. | Removing a zero final outgoing carry changes the convention. |

This reviewer did not execute those Lean declarations. Their checked acceptance must be established by the runtime reviewer on the five frozen modules.

After the successful reservation was reported, this reviewer did execute a separate bounded Python comparison of the proposed design with the original script's `carry_coordinates` function. It checked all **8,191 binary words of lengths 0 through 12**, with zero formula mismatches and zero mismatches between charge-zero and complete reversal. It also checked six specified literal cases, including charge 419 and the nonbinary counterexample. The original script was loaded without running its main routine or its larger experimental program.

The exact command and complete execution result are preserved in [design-controls-execution.json](design-controls-execution.json). That run checked the design; it was not a Lean compilation or a universal proof. The original labels mentioning 196 or 187088 referred to supplied literal words and did not verify carry extraction, orbit time, persistence, or any conjecture about those integers.

## Checker and evidence boundaries

The frozen `check.py` was inspected as source. It lists all five mathematical modules in dependency order, prepares a fresh output directory, sets the isolated import path, checks the official Lean toolchain identity, records source/compiler hashes, and selects the required trust and execution flags. Its explicit-public-name checks and allowed-axiom checks are distinct from the independent runtime review's broader module-origin audit.

The package has 69 explicit public declarations in the inspected source: 13 definitions and 56 theorems, including the nine finite controls. This count describes declarations, not 69 independent research results.

This review does not claim an independent execution of the checker, compiler, public export audit, private/generated declaration audit, or archived development attempts. The remote `evidence` directory was inventoried read-only; its runtime claims are not promoted to this reviewer's own execution. Publication, integration, and runtime gate decisions remain with the parent and runtime reviewer.

Earlier snapshots remain historical. In particular, the initial weight snapshot was later reported to have failed elaboration before a small index-normalization change. The review of that snapshot was explicitly semantic. The frozen weight hash in this report is the corrected `07b3831f...` source, and no earlier compilation failure is erased or converted into a successful execution by this report.

## Ownership coverage and excluded conclusions

The independent ownership census fetched and byte-verified **162 of 162** task records at coordination commit `b0ee3d25fb1ddea0f741326b6401d81ae3d27626`, with zero missing records or blob mismatches. Every task was assessed by its substantive scope regardless of status or numerical agent ID. The first parent-provided delta through `d8aab676e88fa0a42a3a660687e4a7a4d26e64c4` added seven inspected versions: six existing paths and one new path. Thus this reviewer's preserved census covers 169 versions across 163 distinct paths. The parent independently handled later coordination updates; they are not represented as this reviewer's exhaustive census.

No equivalent U/S complete binary-carry zero/symmetry reservation was found in that inspected set. The initial absence of a T/R reservation became stale when Agent14 took T/R; the parent explicitly yielded that scope before the current U/S claim. Older tasks numbered Agent15 were treated as earlier-session work and were not assumed to authorize this session.

The complete original task JSON, byte-verification manifest, English 162-row scope index, and historical ownership report remain under `scout/ownership` in the shared session workspace. They document the exact census boundary and adjacent owners. The successful U/S reservation is the parent's later coordinated action, not a claim made by this reviewer.

This semantic PASS does not cover T/R coefficient encoding, H, an algebraic beta/roots interpretation, support only at coefficient 9, the four-case charge evolution, the universal carry-blind ideal or quotient of order 1782, general carry normalization, a palindrome criterion, persistence, or 196. It covers the exact integer U/S charge of complete finite binary outgoing-carry words and the stated zero/reversal equivalence.

## Final disposition

No source-semantics blocker remains at commit `e8d706dc8a67248e1531b0b828fbe05ff50052ed`. R1 is closed, source conventions are explicit, and the eleven reviewed top-level files are byte-identical across the reviewed snapshot, remote fetches, and frozen Git objects. Any later change to mathematical bytes requires a new delta review. Independent Lean/axiom acceptance and any final integration decision must retain their own attribution.
