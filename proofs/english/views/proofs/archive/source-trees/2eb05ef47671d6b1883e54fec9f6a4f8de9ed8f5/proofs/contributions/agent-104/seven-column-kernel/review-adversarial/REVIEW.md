# Seven-column 739 route: independent adversarial review

Task: `fa6b15e`; review-directory ownership: agent 104 / review-adversarial.

**Current conclusion: no mathematical counterexample was found within the stated domain. The pinned source was actually rebuilt for the projection, inverse enumeration, generic rank-certificate framework, last-step bridge, and terminal obstruction. The complete 739 depth-39 theorem and unconditional alltime196 corollary have not yet been accepted.** Those last two still require the concrete complete certificate checks, coverage of the initial set, short-boundary checks, and the final Lean composition with the orbit.

## Exact assumptions and review findings

| Item | Required condition or obligation | Review finding |
|---|---|---|
| Positive integers | Initial value `A > 0`; zero cannot support `T(n)>n` | Independent counterexample: `T(0)=0`. The current last-step bridge retains positivity. |
| Canonical digits | Digits in 0–9, exact positive length, nonzero most significant digit, and digit value equal to the integer | Without canonicality, the low-end-first list `[1,0]` incorrectly treats the reversal of integer 1 as 10, giving 11 instead of actual `T(1)=2`. `Canonical` states these conditions explicitly. |
| Raw sum word | Nonempty, symmetric, entries ≤18, positive outer entry, and even center at odd length | `Admissible` expresses the complete conditions; the singleton `[1]` and the central 9 in the five-digit word `73937` cannot be actual raw sum words. |
| Long prefixes | `0<k≤L`; high-side inner carry is actual `carry q (L-k)` | `actual_forwardPrefix` and `actual_mem_prefixPredecessors` were reviewed. The two seven-column prefixes need not be disjoint, so 7≤L≤13 is covered; at L=k the inner carry is 0. |
| Inverse enumeration | Enumerate all local carries; a final-column high-side carry must exist; the outer source sum must be positive | `LongCompatible` is equivalent in both directions to the executable list. Coverage of actual steps is provided separately by `ActualPrefix`; the two facts are not conflated. |
| Targets with zero first entry | Python inverse enumeration cannot claim exact equivalence for a zero first entry | Independent diagnostic: Python `prefix_predecessors((0,))` contains `(9,)`, whose actual completed words can output only `(18,)` or `(10,)`. Certificate nodes have positive first entries, so the frozen certificate is unaffected. The Lean overflow branch additionally requires `0<v` and proves that zero-first-entry targets have no predecessor. |
| Short-to-long boundary | Lengths 1–6 retain complete states; actual normalization has length L or L+1; only 6→7 crosses the seven-column threshold | Complete independent integer constructions checked 10467 short words, including 6498 six-digit words and 3429 overflow cases. `shortWords_complete` and `nextWord_wordOf` have correct semantics. |
| Last step | Positive source, canonical target, palindromic target, leading digit >1 | `PalindromeBridge` first proves no overflow, then invokes the no-carry palindrome lemma; equal width is not silently assumed. Removing the leading-digit/no-overflow restriction gives counterexample 29→121. |
| Table lookup | Do not merely trust injectivity of the word encoding, tree order, or the generator | A successful `lookupKey` compares the complete word; `lookup_all` connects successful lookup to a whole-tree assertion. The design is conservative. |
| Graph depth | Every actual reverse edge must be enumerated; every enumerated predecessor must be found with decreasing rank | Generic `backPath_rank` was rebuilt. Complete `CheckedRows` for the concrete 739 table has not yet been accepted in this review. |
| Palindrome depth 39 | The target palindrome's last step gives an initial word; the preceding chain has length ≤38; add 1 for the last step | Final composition must handle t=0, short targets, and every four-digit initial suffix. Merely stating a generic framework does not establish this conclusion. |
| All times for 196 | Uniform ancestry bound 39 plus a finite palindrome-free initial segment | `no_196_739_palindrome_of_ancestry_bound39` explicitly assumes the ancestry bound. Its semantics are correct, but it remains conditional. Independent integer computation confirms no palindromes at times 0 through 39. |

## Independent Python diagnostics

Commands run at the repository root:

```text
python proofs/contributions/agent-104/seven-column-kernel/review-adversarial/probe_independent.py
python proofs/contributions/agent-104/seven-column-kernel/review-adversarial/check_rank_transport.py
```

Both exit codes were 0. The scripts impose CPU/address-space limits; they did not repeat the author's million-integer scan or complete inverse-graph recomputation.

The expected-result side of `probe_independent.py` implements integer remainder-based digits, canonical integer construction, and integer reversal independently. For prefix `s`, it constructs two integers using the actually realizable complete sum words `s ++ [0,0] ++ reverse(s)` and `s ++ [18,18] ++ reverse(s)`, then directly computes `n+reverse(n)`. It does not use the reviewed program's `normalize`, `F`, or forward column formulas to generate expected answers.

- Widths 1, 2, 3: exhaust all admissible sources and targets, with 18, 342, 6498 respectively. Inverse-enumeration sets exactly equal the independently constructed actual-integer completion edge sets; edge counts are 27, 513, 9747.
- Width 7: 2916 threshold-focused sources using 0, 9, 18 and outer entries 1, 9, 10, 18, checking forward outputs and inverse-enumeration coverage.
- All 10467 short realizable words checked through independently constructed actual integers.
- Frozen-certificate samples: 282 targets and 389 long inverse edges, including maximum initial rank and terminal first three entries (1,9,6).
- Integer controls from 1 through 50000: 11115 palindromic outputs, including 11000 without overflow. Every nonoverflow output satisfies source sum word = complete target digits.
- Direct recomputation of the 196 orbit at times 0 through 39; the final value is 7197630720180367016.

`check_rank_transport.py` checks data transport only: it independently parses the tree expressions in 16 `Rank739DataNN.lean` files, traverses the root specified in `Rank739.lean`, and confirms that the multiset of complete-word/rank pairs for all 58501 reachable nodes exactly matches the frozen JSON and that each complete word can be looked up with its rank. This step does not verify predecessor closure and cannot count as certificate acceptance.

Complete outputs: `probe-results.json` and `rank-transport-results.json`. Both record source hashes; stdout and stderr are also retained.

## Pinned source and actual compilation

Toolchain: Lean 4.19.0, commit `6caaee842e94`. Working directory: `/workspace/scratch/7649db1e242c/build104-adversarial`. Standard command:

```text
LEAN_PATH=/workspace/scratch/7649db1e242c/build104-adversarial /workspace/scratch/7649db1e242c/toolchain/lean -j1 -o MODULE.olean MODULE.lean
```

Each module process was limited to 50 CPU seconds (hard limit 55 seconds), 58 wall-clock seconds, and 4GiB virtual address space. Exact commands, exit codes, and elapsed times are stored in execution JSON.

| Module | SHA-256 of source actually executed | Result |
|---|---|---|
| PrefixCertificate | `3ec68f313c6e48a8641e4456a5a0a3e5e8ff61f95f4919ad60a7c2736a2f7943` | exit 0; generic path-rank theorem |
| PalindromeBridge | `6c1de8cf02ec9381e80388e6b4915db6cfa4d1189d3e47c273400f0d37948093` | exit 0; last step and conditional 196 conclusion |
| PrefixInverse | `0a93622752fa22cf6c8de2efc8500dc313498d59831bb0e5381b3b351e0ab03e` | exit 0; includes absence of predecessors for (1,9,6) |
| ActualPrefix | `c136216ed9c4100a268643be9a471b6746320f63d0af2030b6418429e5551e76` | exit 0; actual long-prefix coverage |
| TerminalObstruction | `72a302ffe955315e0727d70a125da9da411df4b295a7edc53231152984724e47` | exit 0; all-width actual (1,9,6) obstruction |
| ShortBoundary development snapshot | `e3f2ed488efc4c55a6d5b1096675cced343cb7f3cf80c3fd6de4102df4139469` | exit 1, internal OOM at 37.538 seconds; no successful rebuild claimed, awaiting the author's final version |

The `#print axioms` queries for the listed key theorems in passing modules contain only `propext`, `Classical.choice`, and `Quot.sound`, with no `sorryAx`, `Lean.ofReduceBool`, or externally trusted oracle.

The `LychrelDigitSums` foundation was not successfully rebuilt from scratch in this review: 3GiB and 4GiB address-space limits triggered bad_alloc/OOM; another attempt with toolchain option `-M1536` was rejected as an unknown `max_memory` configuration. Complete failure records are retained. The existing `build104-base/LychrelDigitSums.olean` was then explicitly reused, with SHA-256 `69dc2ddcd2c17246e2c60ed61195436cc9aefff662f0c49eb769f94baec93978`. Its adjacent source is byte-identical to the pinned reviewed source, SHA-256 `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57`. Thus successful actual rebuilds above refer only to the new modules; another review handles an independent clean foundation build.

`snapshot-01` is a historical snapshot taken while the author was still developing. Its ActualPrefix had two carry-index simplification errors, and its ShortBoundary count had unclosed goals; these were promptly reported. They do not mean that the final projection version reported as rebuilt in this table failed. `snapshot-02` preserves the corrected reviewed source.

## Acceptance gates

Current acceptance covers only the pinned local modules that actually compiled and their exact semantics. Until all the following are complete, this report must not be described as a Lean pass for the complete 739 theorem or an unconditional alltime196 pass:

1. A kernel `CheckedRows` proof for every row of the concrete 739 tree.
2. Lookup and maximum-rank coverage for all 10000 long initial words and the unique short initial word.
3. Proof that the actual successors of all short sources avoid the set required by the certificate, or equivalent complete short-boundary handling.
4. Complete composition from an arbitrary positive-integer ancestry chain to the projected reverse path, including t=0 and the last-step +1.
5. Dependency audits and clean-compilation results for the final theorem.

This review does not establish the full P196 conjecture. Even completion of all the 739 gates would exclude only palindrome targets beginning with 739.
