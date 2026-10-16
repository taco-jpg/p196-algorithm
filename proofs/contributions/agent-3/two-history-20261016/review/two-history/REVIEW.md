# Independent review of the finite-horizon two-history package

**Result: PASS. No remaining blocker in the assigned proof, dependency, or statement scope.**

Reviewer: the runtime and independent review specialist working under Agent #3. This specialist did not author the two-history proof sources. This is an attributed specialist review within Agent #3's session; it does not claim a separate GitHub identity or formal GitHub approval. The parent agent relays the result to the coordination issue and the actual pull request.

The accepted final aggregate is `TwoHistoryTheorem.lean`, SHA-256:

```text
386b181e43ba96a90ca46bc22e40dd05d5cbccf8a683aa5e96e6a5709aa448ee
```

An earlier aggregate with hash `9da25b082dde0cbd0a18dbd101bba9af89b6d57cbdbd7e9aff9e167e0791cba2` was read for statement semantics but was not accepted as a compiled result. Its inaccessible private-helper reference was replaced by a local list-induction proof before this independent build began. Only the final hash above appears in the accepted build.

## Compiler and source verification

The independent run started at `2026-10-16T21:43:00.971999+00:00` and finished at `2026-10-16T21:44:33.241705+00:00`. All 23 proof/dependency modules compiled successfully, followed by a successful compiled-declaration inventory and axiom audit. Total recorded compiler time was 92.038 seconds.

The runtime was the independently verified executable:

```text
/workspace/scratch/4ce7c54d31f6/lean-runtime/lean-4.19.0-linux/bin/lean
Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)
SHA256 92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023
```

Every proof and audit invocation used `--trust=0`. Sources were copied into the previously nonexistent directory:

```text
/workspace/scratch/4ce7c54d31f6/agent3-two-history-independent-build/modules
```

`LEAN_PATH` contained only that fresh directory. No project `.olean` file was copied or reused. The runtime's own standard libraries remained available through Lean's ordinary installation. Every import was checked against the explicit topological source order. All original source hashes, staged source hashes, and freshly produced `.olean` hashes were checked again after the audit.

The 23 modules comprise ten dependencies, six inherited finite-horizon contribution modules, and seven new two-history contribution modules. The four vendored Agent #9 dependencies were checked against both SHA-256 and Git blob identities in `dependencies/agent9/SOURCE_PINS.json`. The original decimal core was built from `proofs/LychrelDigitSums__0810ace083af80c5.lean`; its SHA-256 is `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57`. The exact original-to-module mapping for every dependency is preserved in `verification.json`.

## Axiom coverage

The audit enumerated constants by their **compiled source-module ownership**, rather than merely by a public namespace prefix. It therefore included private constants and generated logical helpers.

| Contribution module | Explicit source declarations |
| --- | ---: |
| FamilyDefinitions | 4 |
| FamilyCardinality | 24 |
| FiniteHorizonOverflow | 18 |
| SafetyBridge | 12 |
| NormalizedSafety | 7 |
| FiniteHorizonTheorem | 4 |
| HistoryInterfaces | 3 |
| TwoLayerCertificate | 20 |
| ActualHistories | 42 |
| IntegerInterfaces | 17 |
| HistoryFamily | 16 |
| HistorySafety | 7 |
| TwoHistoryTheorem | 5 |
| **Total** | **179** |

All 179 explicit declarations were found exactly once, were safe and nonpartial, and received an axiom result. The private declarations were `jointData` and the inherited `nodup_map_of_injective` and `replicate_join` helpers. Exact internal Lean names are retained in the inventory.

Of 530 compiled constants owned by these 13 modules, all **304 safe logical constants** were audited, with exact equality between the expected safe inventory and the returned axiom records. The remaining 226 constants were Lean-generated unsafe or partial implementation symbols; they are separately recorded, and none corresponds to an explicit source declaration. They were not treated as mathematical axioms or silently omitted from the inventory.

The union of all audited axiom dependencies was exactly:

```text
Classical.choice
Quot.sound
propext
```

No audited declaration depended on `sorryAx`, `Lean.ofReduceBool`, or another nonstandard axiom. The finite certificate uses ordinary `decide`; its external table generator is not a logical dependency of the proofs.

## Certificate and full-word transition semantics

`TwoLayerCertificate` uses the unchanged Agent #9 `Local` relation. A state in `Fin 4` encodes the two boundary carries; `Local` imposes both quotient equations and the mirrored digit-sum equation. The two finite table assertions check every Boolean input and every pair of these carry states. The first emitted symbol is a predecessor of the chosen coefficient 5 or 14; the second emitted symbol is a predecessor of that first symbol.

The initial true bit takes joint state `(0,0)` to `(0,1)` and emits outer coefficients 7 and 3. For every joint state, the specified correction has exactly six bits and finishes at `(3,3)`. This is a proved finite table property, not an assumed ability to choose a correction. The suffix of eighteens stays at state 3 in each layer.

The existing `Path` predicate requires `low p = high p` at the empty even center. Thus the closure at state 3 supplies the actual matching-center condition. `WordBridge.path_realizes` relates the path to normalization of the entire mirrored word; `ActualWords.realizes_actual` then proves the original `Agent8.stepWord` relation. `HistoryInterfaces.scan_terminalCarry` identifies the retained scan carry with the original terminal-carry operation. The new construction therefore has complete full-word semantics, including the center and both external carry boundaries.

For a free Boolean list `xs` of length `m`, put `N = 2 * (m + k + 7)`. The definitions yield three words `w0`, `w1`, `w2`, with the following exact chain for `k > 0`:

| Input word | Actual next word | Final carry | Input width |
| --- | --- | ---: | ---: |
| `historyWord0 xs k` | `historyWord1 xs k` | 0 | `N` |
| `historyWord1 xs k` | `historyWord2 xs k` | 0 | `N` |
| `historyWord2 xs k` | `target (m + 6) k` | 1 | `N` |

All three words are canonical coefficient words and have even width. The first two outer coefficients are respectively 3 and 7. The source `historyWord2` is exactly the inherited protected input family applied to the free bits followed by their six correction bits. Consequently its final carry and common overflow image reuse the already proved normalization formula with the correct shifted parameter `m + 6`.

The final aggregate also proves the literal reservoir shapes for `w0` and `w1`: each equals a prefix of length `m + 7`, followed by `2*k` eighteens, followed by the reversed prefix. The shape theorem specifies a guaranteed central block; it does not assert that this block is a maximal run. Its final local list-induction proof is independent of inaccessible private declarations in another module.

## Exact family cardinality

The fixed length of the six-bit correction permits recovery of the original free prefix from `completedBits xs`. The proof of `completedBits_injective` first recovers equal free-prefix lengths from the total lengths and then cancels the suffixes. It does not assume that different joint states necessarily have different correction strings.

Inherited `inputWord_injective` then proves injectivity of `historyWord2`. If two initial words `historyWord0` are equal, applying the deterministic full-word map twice makes their protected images equal; injectivity of `historyWord2` recovers the same free bits. This proves injectivity of the initial family without assuming injectivity of the reverse-add map on arbitrary words.

Both families map the complete, duplicate-free enumeration of all Boolean lists of length `m`. Their lengths are exactly `2^m`, both are `Nodup`, and the membership equivalences cover every enumerated word. The list obtained by applying the actual two-step map to the complete initial family is exactly the protected family in the same order. The counted objects in the aggregate are these distinct coefficient words.

## Ordinary integer interpretation and endpoints

`IntegerRealizes n w` uses the unchanged `DecimalDigits.Canonical`: positive width, decimal digits bounded by 9, positive leading digit, and value exactly `n`. It also requires every coefficient of `w` to equal the corresponding mirrored digit sum. `even_canonical_admissible` explicitly uses even width to discharge the unpaired-center requirement. `even_canonical_realizable` supplies a positive ordinary realization for every initial coefficient word.

The existing ordinary integer step is `n + reverse10 n`, and `orbit n 0 = n`. The new interfaces prove that every canonical realization takes the same integer step represented by the original normalization of its coefficient word. They also prove that the resulting integer realizes the next coefficient word. These equalities are then composed with the two path-derived transitions.

For **every** ordinary realization of an initial word, the safety proof covers the endpoint inclusively:

| Ordinary time | Reason for the claim |
| --- | --- |
| 0 | The initial coefficient word has odd outer coefficient 3. |
| 1 | The first image word has odd outer coefficient 7. |
| 2 | The nonempty eighteen reservoir in the time-one coefficient word supplies the existing one-step safety certificate. |
| `3 + s`, for `0 <= s <= k` | Time three is exactly the normalized protected input value, whose inherited finite safety theorem covers all `s <= k`. |
| 4 | Every realization has the common value `digitValue (target (m + 6) k)`. |

The `t < 3` case split and the identity `3 + (t - 3) = t` cover all `t <= k + 3`, including zero and the final endpoint. The assumption `0 < k` is used where the reservoir must be nonempty and where the inherited overflow target formula applies. The aggregation replaces `xs.length` by `m` only after obtaining the exact membership witness.

This proves a finite family with a depth-two predecessor chain and a prescribed finite safe horizon. Total inverse-fiber cardinality, maximal predecessor depth, arbitrary history depth, a single seed safe for all time, and the seed 196 are outside the statements reviewed here.

## Evidence and reproduction

- `verification.json`: PASS result, executable identity, exact source mappings and hashes, all compiler commands, output hashes, declaration coverage, and post-build integrity checks.
- `compiled-declarations.json`: all 530 module-owned compiled constants, including private and compiler-generated names.
- `axiom-dependencies.json`: the complete 304-declaration safe logical axiom audit.
- `IndependentOwnershipAudit.lean`: the exact diagnostic Lean source used for the ownership audit.
- `logs/`: separate output from each of the 23 source compilations, the version check, and the complete audit.
- `verify_independent.py`: the independent rebuild and audit program.

The accepted invocation was:

```bash
python3 proofs/contributions/agent-3/two-history-20261016/review/two-history/verify_independent.py \
  --repo /workspace/scratch/4ce7c54d31f6/p196-history \
  --lean /workspace/scratch/4ce7c54d31f6/lean-runtime/lean-4.19.0-linux/bin/lean \
  --build /workspace/scratch/4ce7c54d31f6/agent3-two-history-independent-build \
  --aggregate-sha 386b181e43ba96a90ca46bc22e40dd05d5cbccf8a683aa5e96e6a5709aa448ee
```

A reproduction must choose a new empty build directory; the program refuses to erase or reuse an occupied one. Ordinary execution in this workspace required the already authorized escalation because the installed Lean runtime cannot locate its application inside the default sandbox. No proof source, Git index, commit, branch, or remote discussion was changed by this review.
