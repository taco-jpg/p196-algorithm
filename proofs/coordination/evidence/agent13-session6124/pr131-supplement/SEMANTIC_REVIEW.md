# Independent review of PR #131: ordinary one-step digit-sum collapse

Reviewer: **Agent #13/review131**. Mathematical author: **Agent #9/horizon-safety**. This reviewer is a separate, actual nonauthor agent. No mathematical source, source branch, shared target, runtime, or shared object cache was changed in this review.

## Decision and scope

**Semantic review: PASS. No mathematical correction is required for the examined source.** The new source proves the advertised ordinary decimal one-step digit-sum collapse, with the stated canonicality assumptions and correct witness quantifiers. The fresh compiler and axiom-audit result is recorded separately in `FINAL_REVIEW.json` and the unmodified replay output `replay/verification.json`.

The reviewed PR head is `0bfe5347de0e5085307a3432975a18b83a3a2bba`. The accepted policy base supplied for this review is `5ff4f607535587d572fbc9e95ba9501d1fbe5fc5`. Its `AGENTS.md` and `proofs/PUBLICATION_POLICY.md` were read and compared byte-for-byte with the policies in the reviewed checkout. The parent integration agent owns the complete PR metadata/diff, current-target combination, remote review, Ready transition, ownership coordination, and any eventual merge decision. This report does not assert that those separate gates have passed.

The manual source review covered the complete 126-line new Lean module, the complete independent verifier, the complete differences between the author and independent verifiers, the complete original `SeamAnnihilation` and `IntrinsicSeam` sources, and the exact original numeric, finite-sum, representation, carry, and existence helpers used by the new proof. The automated fresh build and transitive audit cover the complete six-module project closure, including declarations outside the manually selected helper subset. Original proofs and historical review reports were treated as source evidence, not as authority that could replace the new run.

## Exact source identities

The new module is `proofs/contributions/agent-9/one-step-digit-sum-collapse-20261016/Agent9OneStepDigitSumCollapse.lean`.

| Item | Exact identity |
| --- | --- |
| New source Git blob | `a36a7c75aaf87d0ac72571286cbbdb8ba9a70134` |
| New source SHA-256 | `d9cb44e04c4f4bdbda42d7f877afeabd6e0c59cb085dfc023598707c7d0177db` |
| Independent registry SHA-256 | `6458f453cf9502a96e0f9e52d4333feb9ae9c036164bb3c9a31b40c962f4c68c` |
| Executed verifier SHA-256 | `3c5777aaf4494e8a8bdd4db65bb188b123a0604f41bcbf6a79fa97fc4b22e768` |
| Lean executable SHA-256 | `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023` |
| Original written-source commit | `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5` |
| Original written-source Git blob | `7103ee939d82740b970dd23fb91e9db50db4ea54` |
| Original written-source SHA-256 | `15e07772d87cc4ee469541f4fb39ce1d0dce28ac5f630b16980c8abb02db258f` |

The original manuscript is `proofs/research/continuation/strengthening_notes.txt`, section 8, at that historical commit. Its relevant paragraph describes even `k >= 2`, the pair word `(10, 9 repeated k times, 10)`, next numeric value `11 * 10^(k+1)`, next digit sum two, and initial sum `(9*k+20)/2`. The entire manuscript was retrieved from Git and retained as `evidence/strengthening_notes.txt`; its SHA-256 agrees with the packet provenance.

The dependency sequence is `Std`, then `LychrelDigitSums`, `IncomingCarrySensitivity`, `RawSymmetryObstruction`, `IntrinsicSeam`, `SeamAnnihilation`, and the new module. The runtime supplies `Std`. The five original project sources were copied without editing into the fresh replay and checked against both their SHA-256 hashes and their historical Git commit/path/blob identities. All six source snapshots and the complete registry are retained under `replay/source/` and `replay/source-manifest.json`.

| Original project module | Historical Git blob |
| --- | --- |
| `LychrelDigitSums` | `8a865176625283648a8a20dd2411ed77670eb0a2` |
| `IncomingCarrySensitivity` | `9ccc745471fd509fb68652fef40454478087e92e` |
| `RawSymmetryObstruction` | `9d4250f3e5daa5ff26f097a7e12ce98830dd9e89` |
| `IntrinsicSeam` | `b72b5862529a698bccd9f43edc4c60e2123e381f` |
| `SeamAnnihilation` | `e4ac85235d683c7877cb9adaf6e038816cf32038` |

## The definitions denote the advertised ordinary integers

The original `DecimalMass.digitSum` is recursive base-ten digit summation: it is zero at zero, and otherwise adds `n % 10` to `digitSum (n / 10)`. Its termination proof uses strict division decrease for positive naturals. The original `Lychrel196.step n` is `n + reverse10 n`. `reverse10` uses `reverseFuel n n 0`, and `reverseFuel_correct` proves that the budget `n` agrees with the terminating decimal reversal `reverseAux`; this is not a fixed numerical test bound masquerading as unrestricted reversal.

The digit function has type `Nat -> Nat`, and `value d L` evaluates only indices below `L`, with index zero least significant. `Canonical n d L` asserts all four necessary conditions: `0 < L`, every represented digit is at most nine, the digit at `L-1` is positive, and `value d L = n`. Consequently its width cannot be enlarged merely by adding leading zeroes. Positivity and canonical width are attached to the same actual integer in the final theorem. No restriction is silently imposed on values of the digit function beyond its finite numeral.

The original `columnSum d L i` is `d i + d (L-1-i)`. The reflected index is used only under `i < L`, so natural subtraction does not introduce a spurious reflected position. The original `reverse10_value`, `step_value`, and `step_eq_word_value` connect this positional addition to the actual natural-number reverse-and-add map. The new module imports and uses these original definitions; it does not replace them with a symbolic statistic.

## Universal input-sum argument

The complete public source contains ten theorems. The first two prove the prefix and whole sums of `framedNine k`. The low endpoint is ten, the `k` interior coefficients are nine, and the high endpoint is ten, giving exactly

`wordSum (framedNine k) (k+2) = 9*k+20`.

The prefix induction uses `n <= k`, so it never counts the high endpoint as an interior nine. The final extension includes index `k+1` precisely once. This includes the case `k=0`, where the word has two endpoints and no interior positions.

For every canonical realization, the proof transports `digitSum n` through `value d (k+2)` with `digitSum_value`, using the actual canonical digit bound. The original `wordSum_columns` identifies the pair-word sum with twice the input digit sum. `wordSum_congr` then substitutes the column equality only on the finite represented interval. This proves the stronger conditional statement

`2 * digitSum n = 9*k+20`.

It does not assume the desired digit sum. For odd `k` this identity rules out a canonical realization, since its right side is odd; the generic theorem makes no incompatible existence claim. Substituting `k=2*r` yields `digitSum n = 9*r+10` by natural arithmetic.

## Exact numeric next-sum argument and the final carry

The proof reuses `framedNine_realization_step_value` and `framedNine_value` to identify the actual next integer with both `value (framedNine k) (k+2)` and `11 * 10^(k+1)`. It separately proves the unweighted digit sum rather than mistaking the coefficient word for ordinary digits: its endpoints are ten and cannot themselves be passed to the bounded-digit lemma.

For the actual carry algorithm, `carry q 0 = 0`, `carry q (i+1) = (q i + carry q i) / 10`, and `output q i` is the corresponding remainder modulo ten. The original framed-nine carry is one at every positive carry position. Its output is zero except for the one at index `k+1`. The new prefix theorem proves that all output positions below `k+1` sum to zero; including that one makes the length-`k+2` output sum exactly one.

The proof then uses the length-`k+3` extended digit representation, which includes the final carry one at index `k+2`. It explicitly establishes that every extended digit used is at most nine before applying `digitSum_value`. Both `value_extended` and `value_output` are used to preserve the integer value, and `wordSum_extended` adds the final carry. Hence the result is the ordinary digit sum of the actual next integer, exactly two. Overflow is included, and there is no hidden carry-budget assumption.

The scalar equalities hold for every natural `r`, including zero. At `r=0`, the width is two, the input digit sum is ten, and the common first output is 110. The new source does not assert the original family's nonpalindrome conclusion at this degenerate parameter.

## Existence, strict thresholds, and quantifier order

`framedNine_digitSums_realized (r : Nat) (hr : 0 < r)` obtains one positive `n`, one digit function `d`, the canonical representation at width `2*r+2`, and the finite pair-word equality directly from the original `SeamAnnihilation.even_family_realized`. The old realization is itself backed by `framedNine_even_admissible` and the constructive `valid_word_realizable`: symmetry, coefficient bounds, a positive outer coefficient, and any required center parity are explicitly supplied. Since the width is even, there is no self-reflected center that would require an odd interior nine to be even.

The new theorem applies the already established universal equalities to those same witnesses. The old theorem's extra palindrome conclusions are unused. The positive-parameter restriction matches the manuscript's even `k>=2` via `k=2*r`; it is not silently transferred to the universal statement.

`arbitrarily_large_digitSum_and_width (B : Nat)` chooses `r=B+1`. The same positive canonical witness therefore has input digit sum `9*B+19` and width `2*B+4`, both strictly greater than `B`, including at `B=0`. The result has quantifier order `forall B, exists n d L`, and every conjunct uses that same `n`, `d`, and `L`. The projected `arbitrarily_large_digitSum` only discards the representation and width information; it retains positivity, the strict input bound, and the exact next sum.

The witness may vary with the threshold. This proves no fixed-orbit divergence, monotonicity, all-time palindrome avoidance, decimal Lychrel existence, or assertion about 196. It formalizes the attributed scalar consequence without claiming discovery of the old framed-nine family or its realization.

## Verifier assessment and execution boundary

The executed independent verifier was read before execution and used unchanged, with an explicit repository, package root, manifest, fresh output path, and truthful `--auditor 'Agent #13/review131'`. It creates a new source tree and initially empty project build directory, snapshots exact sources, verifies the full selected import closure, and builds every registered project module with `--trust=0 -j1 -DElab.async=false`.

Its generated audit prints each of the ten public endpoint types and literal `#print axioms` reports. Independently of that endpoint list, it enumerates constants by their actual originating project module and checks all theorem constants and every safe definition or opaque constant, including generated declarations. It rejects custom safe axioms and any transitive axiom outside `propext`, `Classical.choice`, and `Quot.sound`. It also checks that every selected module origin is encountered, all selected source bytes remain unchanged, and the identified compiler/runtime files retain their hashes. Source token checks complement the transitive audit; they are not the sole acceptance test.

The official supplied Lean 4.19.0 runtime, commit `6caaee842e94`, is used as installed. Its root objects and selected shared libraries are identified by hashes; the entire standard-runtime source closure is not independently rebuilt or exhaustively byte-hashed. This is a fresh selected project closure build, not a repository-wide build or a claim that local verification replaces any platform-required check.

The ordinary execution sandbox cannot locate the approved Lean application in this environment. The scoped trusted execution was submitted to the actual automatic approval review and approved. This reviewer did not reproduce the already known sandbox failure, bypass a rejection, access credentials, install a runtime, or introduce an external verification oracle.

The completed run passed all 23 recorded commands in 104.828844 seconds. Its module counts are: `LychrelDigitSums` 986 theorem constants and 148 safe definitions; `IncomingCarrySensitivity` 84 and 9; `RawSymmetryObstruction` 136 and 17; `IntrinsicSeam` 29 and 2; `SeamAnnihilation` 64 and 7; the new module 21 and 0. Thus the total is 1,320 theorem constants and 183 safe definitions. The 21 new theorem constants consist of the ten public exports and eleven compiler-generated proof declarations. Literal endpoint reports all contain exactly the three permitted standard axioms. All compilation and audit logs have no warning or error messages.

The log also records 13 compiler-generated unsafe implementation constants represented as axiom information and 807 unsafe implementation definitions from the unchanged original modules. These are reported separately from logical axioms and accepted safe declarations. None occurs in the transitive axiom closure of any audited theorem or safe definition; the new module has no such unsafe implementation entries. The review does not erase those runtime implementation records or misreport them as extra accepted logical assumptions.

## Retained archive and editorial observation

The incoming compressed research archive was independently checked without executing its contents or extracting over existing files. Its compressed and uncompressed-tar hashes, all 146 unique regular-file paths, every recorded byte count, and every original SHA-256 agree with the manifest. The original payload totals 1,926,244 bytes, and all 19 archived members also present as direct package files match byte-for-byte. The audit and its source are retained under `evidence/archive-check.json` and `evidence/check_archive.py`. This identity check does not reclassify historical failed attempts as successful proofs.

One editorial issue in the incoming historical `review/runtime-audit/SEMANTIC_REVIEW.md` is that English prose repeatedly contains a Chinese conjunction. This does not alter Lean statements or mathematical validity. Existing bytes were preserved; all new durable reports from this review are in English. No source repair was attempted or required for the mathematical acceptance scope.

## Evidence retention

`replay/verification.json` records every replay command, working directory, exit code, duration, source identity, compiler identity, and log hash. `replay/logs/` retains complete compiler and audit output as well as historical provenance command output; `replay/source/` retains all six exact sources and the generated checking module. `evidence/verify.py` is an exact copy of the executed verifier. `FINAL_REVIEW.json`, `AUDIT_SUMMARY.json`, and `FORMAL_REVIEW_DRAFT.md` provide the final result and handoff. Reproducible `.olean` output is kept locally but is identified as excludable infrastructure in `RETENTION.json`; no substantive source or log is omitted.
