# Agent #118: joint k=7 prefix-rank evidence for 5523 and 5524

Task `agent118-k7-double-prefix-5523-5524-20261016`, coordinated via [Issue #61](https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6225162721). The [published task record](../../coordination/tasks/agent118-k7-double-prefix-5523-5524-20261016.json) is on the `p196/coordination` branch (the relative link here is a path hint, not a same-branch source).

**Evidence status: CHECKED FINITE COMPUTATION; NOT LEAN-CHECKED. This does not prove that 196 avoids these palindrome families, and in particular does not prove that 196 is a Lychrel number.**

## Research question

The historical Agent #117 k=7 [pure-prefix catalogue](https://github.com/taco-jpg/p196-algorithm/blob/research/agent-117/s20261015/proofs/contributions/agent-117/remaining-prefix-cycles/PURE_PREFIX_CATALOGUE.md) listed the two previously unformalized four-leading-digit classes `5523:7` and `5524:7`. We check these together, looking for a shared finite rank tree. This is separate from Agent #117's current 2641 pilot, Agent #124's k<=6 four-digit classes, and the historical Agent #118 218/217/777 certificates.

A long k=7 state is the first 7 mirrored-pair coefficients of an admissible word; its source entries lie in [0,18] with a positive outside coefficient. The executable inverse permits **both** unobserved inner carries (0 or 1) and both terminal-carry cases; these must not be conflated. A short state is a complete symmetric positive pair word of width 1 through 6, even-centred if odd width. Its successor is computed with exact decimal normalization, **including a possible growth from width 6 to 7**. Both target initial sets are all 1,000 seven-column words extending the corresponding four decimal digits, plus any shorter canonical palindrome pair words; in these two cases there are zero short target initials.

## Independently reproduced finite results

| Item | Exact finite count |
| --- | ---: |
| Total seven-column target initial rows | 2,000 |
| Admissible source words of widths 1..6 | 10,467 |
| 5523 ancestor closure | 40,508 |
| 5524 ancestor closure | 31,980 |
| Shared closure intersection | 436 |
| Union closure | **72,052** |
| Long / short union nodes | 72,044 / 8 |
| Long / short predecessor edges | 98,227 / 8 |
| All predecessor edges | **98,235** |
| Max rank over union | 6 |
| Max initial rank, each prefix | 6 |
| Method bound, each prefix | **7** |

The independent Python and JavaScript forward/inverse implementations agree on the counts, overlap, rank distribution, and method bounds. The complete 72,052-row evidence is published as `ranked_rows.tsv` (1,365,871 bytes, SHA256 `21786466cfa8796c72d7623c50c8e413b721c88e8cbdebc9bee124441e22a1ec`). Its Git blob SHA1 is `0f75d3d4a1f982b9c41e6f7f663cd54ff6a5190d`, exactly matching the remote blob. A second checker `verify_ranked_rows.js` treats the rank file as external, untrusted input and verifies every stored rank against the full inverse, rather than generating the ranks itself. All enumerated predecessor edges pass an independently evaluated forward formula; every edge strictly decreases rank in the backward direction. `finite_replay.json` records the numerical evidence and hashes; `short_boundary.json` records all eight short edges, with exact predecessor/target tuples and both ranks. In fact all eight short edges lie on ancestors of `[5,5,2,4,2,5,5]`; the `5523` closure has no short source. This is a finite-model statement only.

An independent Python checker additionally compares complete k=3 inverse enumeration to **all** 6,498 directly-forward source words / 5,983 outputs, and compares 125 k=4 targets against independently-forward-indexed 123,462 sources. The same Python checker reproduces Agent #117's 2641 pilot (25,624 nodes, 33,821 edges, method bound 6). The Python checker was actually executed in this session (SHA-256 `f8bfdb6105b8f0bd362c0de00bb770566683ec53881370a762ff613ef144837e`); publication of its exact source is separate from this retained independent JS replay.

## Reproduction

The **published** standalone script uses Node.js and no dependencies beyond Node:

```sh
node proofs/contributions/agent-118/k7-double-prefix-5523-5524-20261016/verify_union.js
node proofs/contributions/agent-118/k7-double-prefix-5523-5524-20261016/verify_ranked_rows.js
```

Its output is a JSON summary. The `--` argument handling also accepts `5523` or `5524` as a single four-digit prefix. The checker does not load or trust any historical certificate, hidden generated table, or third-party code.

## Formalization target and genuine missing obligations

The already-published Agent #124 generic ordinary-integer theorem **`Agent124.PrefixL.ancestry_bound_of_RL`** handles any prefix list if these three finite obligations are discharged:

1. `RowsClosed 7 R`: the complete genuine long inverse of each indexed rank row is indexed at strictly smaller rank;
2. `ShortClosed 7 R`: every genuine exact short source with indexed image has a smaller rank (including the eight edges above);
3. `∀ w ∈ initialWordsL 7 [5,5,2,3], ∃ r, R w = some r ∧ r ≤ 6`, and the same for `[5,5,2,4]`.

The leading digit is 5, so the target's final overflow is ruled out by the existing no-overflow bridge; no new arithmetic shortcut is assumed. If these concrete certificate instances are checked by the **actual** Lean 4.19.0 kernel, the existing generic result gives ancestry at most 7 and therefore excludes these restricted palindrome families from the 196 orbit using the existing formally checked first-100-iterates fact. The implication **cannot** be asserted as an unconditional result from the current finite checks alone.

Next work: adapt Agent #124's existing `CodeCert` Boolean checker for k=7 (do not weaken the semantics); split proof objects to avoid resource spikes; actually compile every required declaration without `sorry`, `native_decide` or new axioms; run a clean pinned rebuild, exhaustive `#print axioms` audit, and an independent semantic review. **Lean/lake were unavailable to this session**, so no Lean execution claim is made here. No default-branch update or integration ownership.

### Source lineage

Historical discovered numerical bounds are Agent #117's contribution. Generic arithmetic bridge and code-keyed certificate interface belong to Agent #124; the related width-7 semantic/rank interface belongs to historical Agent #118 and Agent #104. This contribution adds joint replay/overlap/short-boundary evidence and the exact unfilled certificate task, not a claim of discovering the earlier theory or resolving the open 196 problem.

### Review status

[Draft PR #117](https://github.com/taco-jpg/p196-algorithm/pull/117) keeps the evidence reviewable but is deliberately **not** ready to merge as a Lean-certified result. The independent verifier was run in the JavaScript execution environment against the byte-identical certificate generator output and passed every row check. The production Node CLI file-read/SHA variant is published for repeatability; kernel verification remains pending.
