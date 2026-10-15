# Semantic adversarial review: Agent #118 prefix kernel and the 218 instance

**Verdict: PASS WITH NOTES.** I found no blocking defect in:

- statement fidelity;
- the new short-descent induction;
- initial-family completeness;
- the wiring of the 218 instance.

One IMPORTANT item is about evidence, not mathematics. The committed dev-build logs cannot be tied to the committed bytes, so acceptance should wait for the clean pinned rebuild (Finding 1).

- **Reviewer:** independent semantic reviewer (subagent), 2026-10-15. Lean was not run.
- **Reviewed bytes:** commit `9e618cc`. The working tree equals HEAD for `agent-118/`, `agent-104/` and the core.

| File | SHA256 |
|---|---|
| `PrefixAncestry.lean` | `17a67ee1767abdbac0d0258176feba668de22164d538f8bda168c30efd6bb888` |
| `PrefixChecksBase.lean` | `e11160a2baff401be28010231ef7c36a3680399cce55919a879b05c28fc3bebe` |
| `README.md` | `7525cfa4f7b9952d977d255b1d4988d6fec4076b3ae5e44585d06464208cacf6` |
| `generate_instance.py` | `e66ad0e72c51b7a4c52aceb877575a27f7f15ff109452389c7e4e2d3aae46939` |
| `cert218/Conclusion218.lean` | `3348d64f4777004ba76aaef6ddb0a85039d3ce764edcceb76091381ac9a13d88` |
| `cert218/*.lean` (154 files, concatenated in sorted order) | `7685c3282cc181cff50c784159aca6fb07a478c7a422f46f4a02f7b3a32f73f2` |

## Answers to questions A to E

These are evidence summaries. There is no defect unless a finding below is cited.

### A. Statement fidelity

**Digit order.**
- `value d (L+1) = value d L + d L * 10^L` (`LychrelDigitSums.lean:513-515`). So `d 0` is the units digit and `d (L-1)` has weight `10^(L-1)`.
- `Canonical` (`:907-908`) requires every digit ≤ 9 and a nonzero `d (L-1)`.
- `canonical_unique` (`PalindromeBridge.lean:24-34`) makes the width and the digits unique.
- Therefore `Starts3 a b c P` (`PrefixAncestry.lean:37-39`) means exactly this: P has at least 3 decimal digits, and its three leading digits are a, b, c.
- `Palindrome` is `reverse10 n = n` (core `:118`). By `palindrome_value_iff` (`:780-791`) this is equivalent to symmetry of the canonical digits.

**The family is not empty.** 21812 belongs to the 218 family. It is reached in two steps: 10700 → 11401 → 21812. This path is the single short edge present in the 218 tree (see B).

**739 equivalence.** Substituting a, b, c := 7, 3, 9 into `PalindromeStarts3` gives, token for token, the bodies of `Starts739` and `PalindromeStarts739` (`PalindromeBridge.lean:109-116`).
- The `Iff.rfl` proof at `PrefixAncestry.lean:47-48` is logged as compiled with no axioms (`logs/PrefixAncestry-dev01.log`).
- That file has not changed since the log (`git diff ac9ba65 9e618cc` on it is empty).

**Final statements** (`cert218/Conclusion218.lean:13-26`).
- These two theorems are exactly claims (1) and (2) for prefix 218:
  - `ancestry_bound34 : ∀ A P t, 0 < A → PalindromeStarts3 2 1 8 P → orbit A t = P → t ≤ 34`
  - `no_196_218_palindrome : ∀ t, ¬ PalindromeStarts3 2 1 8 (orbit 196 t)`
- No extra hypotheses remain:
  - the finite premises are discharged by theorems (`ranks allRows shortDesc initialCovered`);
  - the only side conditions are `2 ≤ 2` and `33 + 1 ≤ 100`, both closed by `by decide` (lines 15 and 20).
- `orbit`, `Palindrome` and `Canonical` resolve to the core definitions. No other definitions with those names exist in the opened namespaces.
- `no_196_218_palindrome_unfolded` (lines 23-26) is proved by the folded theorem, so Lean confirms the unfolded statement is definitionally the same.

### B. Soundness of `ShortDescent`

**Checker and its soundness.** `shortDescentOK` (`PrefixAncestry.lean:53-56`) is true in one of two cases:
- the image `nextWord s` is not in the tree; or
- the source `s` is in the tree with a rank strictly below the image's rank (`checkBelow`, `PrefixCertificate.lean:78-81`).

`shortDescentOK_sound` (`:62-67`) extracts exactly this fact. `shortDescent_of_exclusion` (`:70-74`) correctly shows that Agent #104's old premise implies the new one.

**The induction** `actual_iterPairs_rank_desc` (`:79-119`) is Agent #104's `actual_iterPairs_rank` (`ActualAncestry.lean:57-88`) with a new short branch.

*Short branch (`:93-105`):*
- The source word is in `shortWords` by `shortWords_complete`.
- `short_next_width` gives `nextWidth ≤ 7`, so `project_short` also applies to the image in the 6→7 overflow crossing.
  - In that crossing the image key is the full 7-word.
  - That is the same key `project_long` uses for the 7-prefix of a long state, so the stored long node is found.
- `nextWord_wordOf` identifies the image with `nextWord`.
- The descent check gives the source a rank `k < r`, and the induction hypothesis gives `t ≤ k`.

*Long branch (`:106-119`):*
- It is identical to the accepted proof.
- Width never decreases (`width_le_nextWidth`), so a long source never has a short image.

**Short nodes.**
- Their long-row check is vacuous: `longPred` returns `[]` unless the word has length 7 (`LongRowsBase.lean:8-9`).
- This is sound, because a short node can only have short predecessors, and `ShortDescent` covers those.
- A 7-word node has two kinds of predecessors, and both are checked:
  - width ≥ 7 sources, through the row checks;
  - width-6 overflow sources, through `ShortDescent`.

**Short-word enumeration is complete.**
- `rawWords_complete` (`ShortBoundary.lean:45-95`) covers every admissible word of width 1 to 6:
  - positive outer sum;
  - sums ≤ 18;
  - symmetry;
  - even center for odd widths.
- Independently, Lean `shortWords` equals the verifier's `raw_words(1..6)` as a set (10,467 words).
- `ShortDescentAt` (`PrefixChecksBase.lean:18-25`) enumerates exactly `rawWords 2..6` for one outer sum, and `shortOne` covers width 1.
- In any case, `shortDescent_of_cases` concludes exactly the `ShortDescent` that the generic theorem uses, so a gap in the enumeration would stop it compiling rather than make it unsound.

**Python diagnostics (Lean semantics).**
- My port of `nextWord` agrees with the verifier's `F` on all 10,467 short words.
- For 218, exactly one short source has an image in the tree: `[1,0,14,0,1]` (rank 0) → `[2,1,8,1,2]` (rank 1). The rank descends.
  - So Agent #104's exclusion premise is genuinely false for 218, and the new premise is needed.
- Recounts for all five certificates match `README.md:64-67`. Every edge descends strictly.

| Prefix | Short edges into tree | 6→7 crossings |
|---|---:|---:|
| 218 | 1 | 0 |
| 217 | 3 | 1 |
| 620 | 6 | 0 |
| 739 | 0 | 0 |
| 777 | 17 | 1 |

### C. Initial family completeness

**Short widths.** `shortTargetAdmitted` (`PrefixAncestry.lean:137-142`) is exactly the admissibility condition for the last predecessor's pair-sum word of a width-3..6 palindrome with leading digits a, b, c.

| Width | Palindrome | Admitted when |
|---|---|---|
| 3 | `[a,b,a]` | c = a and b is even |
| 4 | `[a,b,b,a]` | c = b |
| 5 | `[a,b,c,b,a]` | c is even (the center sum is 2·digit) |
| 6 | `[a,b,c,c,b,a]` | always |

- `short_target_mem` (`:159-201`) proves membership from `Admissible`.
- For 218, widths 3 and 4 are excluded (8 ≠ 2 and 8 ≠ 1). The admitted short targets are `[[2,1,8,1,2],[2,1,8,8,1,2]]`.

**Widths ≥ 7** (`:205-230`).
- The projection is the first seven pair sums.
- There are no carries (`canonical_last_step`), so these sums equal the target's digits e0..e6.
- By symmetry those digits are a, b, c followed by four digits ≤ 9, so the index is below 10,000.

**Comparison with the Python verifier.**
- Lean `targetInitialWords 2 1 8` has 10,002 words.
- It is set-equal to the `initial` list in `certificate_218.json`, and to the verifier's `expected` construction (`verify_certificates.py:134-140`).
- The same equality holds for 217 (10,001), 620 (10,002), 739 (10,001) and 777 (10,002).

**Why this is self-checking.** A family that is too large would only add proof obligations. A family that missed a reachable word would make `short_target_mem` or `target_project_mem_initialWords` fail to compile.

### D. Wiring of the generated instance

**Same objects everywhere.**
- There is one `ranks` (`cert218/Rank218.lean:8`), used by `allRows` (`AllRows218.lean:110-112`), `shortDesc` (`Short218.lean:46`) and `initialCovered` (`Initial218.lean:19-20`).
- The bound 33 and prefix `2 1 8` are the same in `Initial218.lean:15-20` and `Conclusion218.lean:15,20`.
- Lean's type checking enforces this match.

**Tactics and forbidden constructs.**
- Tactics used: 2,453 `decide +kernel`, 3 `by decide` (the arithmetic in the conclusion), and one `omega` (a case split).
- None of the following appear in any agent-118 Lean file: `native_decide`, `sorry`, `admit`, `axiom`, `unsafe`, `implemented_by`, `extern`, notation, macro or attribute overrides, `debug.*` or `skipKernelTC` options.
- No `debug` or `skipKernelTC` option appears in the imported agent-104 or core files either.

**Independent replay.** I parsed the tree from the Lean source, not from the JSON, and replayed the checks in Python.
- **Nodes:** 38,587 (38,584 seven-words and 3 short words). The word → rank map is identical to the JSON.
- **Lookup tree:**
  - `pivot = wordCode` for every node;
  - the binary-search-tree order holds;
  - `lookup` finds every stored word with its own rank.
- **Long edges:** all 38,798 long predecessor edges (`fastLongPred 7`) land in the tree with strictly smaller rank.
- **Inverse cross-check:** on every long node, `fastPrefixPredecessors`, `prefixPredecessors` and the verifier's `prefix_predecessors` give the same set (0 differences).
- **Initial words:** all 10,002 are present. The maximum rank is exactly 33, so 32 would fail.

**Consistency of totals.**
- 38,798 + 1 short edge = 38,799 edges, and 38,587 nodes. Both match `P196_739_Proof.md:209`.
- `palindrome_height_bound` 34 = 33 + 1, which `generate_instance.py:66-67` asserts.

**Agent #104 modules.** The SHA256 of ten modules used equals the accepted pins in `agent-104/seven-column-kernel/integration-verified/verification.json`: `LychrelDigitSums`, `PrefixInverse`, `FastInverse`, `PrefixCertificate`, `ActualPrefix`, `ShortBoundary`, `LongRowsBase`, `FastRowsBase`, `PalindromeBridge`, `ActualAncestry`. `RowBoolean` is the exception (Finding 2).

### E. Other checks

- **Leading digit.** `2 ≤ a` is used only to rule out a final overflow (`PalindromeBridge.lean:39-54`). For 218, a = 2.
- **t = 0** is handled (`PrefixAncestry.lean:269-270`).
- **196 corollary.** It uses `no_palindrome_through_100` (core `:245-248`) through `no_196_target_of_ancestry_bound` (`PalindromeBridge.lean:148-155`), with B = 34 ≤ 100.
- **Intermediate palindromes.** The bound counts orbits that pass through earlier palindromes. This matches H(P) in `P196_739_Proof.md:23-25`.
- **README.** It makes no Lychrel claim (`README.md:6`) and states that the clean rebuild and independent review are pending (`:14-15`).

## Findings

**1. IMPORTANT — Wait for the clean pinned rebuild of the committed bytes before accepting.**
The dev-build records do not pin source hashes:
- `logs/dev218/full218-dev01.jsonl` and `pilot218.jsonl` record only module, exit code, seconds and RSS.
- Their modification times (12:01:05) are earlier than those of the committed `cert218/` sources (12:01:47).
- `generate_instance.py` also changed after my first read. It is now 281 lines and adds `sys.dont_write_bytecode` at line 19.

So "LEAN-CHECKED (dev build)" (`README.md:15`) and "now kernel-checked" (`:33`) cannot yet be tied to these exact bytes. Everything I can check without Lean is consistent with them compiling: my replay of the committed sources passes every obligation.

Action: accept only after `check.py --require-committed` on `9e618cc` (or later) reports PASS, with all three `Agent118.Finite218` theorems depending only on {`propext`, `Classical.choice`, `Quot.sound`}. Record that run's source pins in the README.

**2. MINOR — `RowBoolean` is outside Agent #104's accepted import set.**
- `PrefixChecksBase.lean:2` imports `agent-104/.../certificate/RowBoolean.lean` (unchanged, SHA256 `f3efdbde673f…`).
- `RowBoolean` is not one of the 383 accepted, independently verified sources: it is absent from `integration-verified/verification.json`.
  - Its only earlier use is the non-accepted pilot `BooleanPilotRows739.lean`.
  - Agent #104's accepted `Rows739_*` decided `RankTree.All` directly instead.
- `README.md:69-72` says that only the closure of `ActualAncestry` is imported.
- This is not a soundness concern. The file is 22 lines, `checkRowsBlock_sound` is a direct induction (I read it in full), and the build kernel-checks it.

Action: list `RowBoolean` (and `FastRowsBase`/`FastInverse`, which it brings in) under Dependencies, and say it is first verified in this contribution.

**3. MINOR — The README module count is wrong.**
- `README.md:15` says "all 133 instance modules compiled", but `cert218/` has 154 modules. The README's own counts at `:39-40` add up to 154 (16 + 105 + 10 + 18, plus 5 aggregators).
- The 133 are the full run. The pilot run covers the other 21, all with exit 0:
  - `Rank218Data00` to `Rank218Data15` and `Rank218`;
  - `Initial218_00`, `Rows218_000`, `Rows218_041` and `Short218_00`.
- Together the two runs cover all 154 modules, with no overlap.

Action: correct the count, or say "133 in the full run plus 21 in the pilot".

**4. MINOR — The build runner can be hardened (inherited from Agent #104).**
- `check.py:45` (`FORBIDDEN`) rejects `sorry`, `admit`, `axiom`, `native_decide` and `sorryAx`.
- It does not reject `debug.skipKernelTC` (or `set_option debug.*` in general). That option would skip kernel checking and leave no trace in `#print axioms`.
- No such option appears in any source in the import closure, so there is no current impact.

Action: add it to `FORBIDDEN` before reusing the runner for 777 and 217.

**5. MINOR — Statement cosmetics; no action required.**
- (a) The hypothesis `0 < A` in `ancestry_bound34` (`Conclusion218.lean:14`) is not needed: `orbit 0 t = 0` is never in the family. The stated theorem is therefore slightly weaker than "for all A", but just as true.
- (b) The generic theorem does not require a, b, c ≤ 9. For parameters that are not digits, the family is empty and the theorem is vacuous. `README.md:23` correctly says "digits".

## What I did NOT check

- **Lean.** I did not run Lean, as instructed. I did not establish any of these:
  - that the code compiles;
  - that the kernel accepts the 2,453 `decide +kernel` obligations;
  - the axiom reports.

  I have not verified the coordinator's report (133 modules compiled; standard axioms only). I only read the committed logs, which have no source hashes (Finding 1).
- **Agent #104 and the core.** I did not re-verify the proofs in Agent #104's accepted modules or the core. I read the definitions and statements used, and relied on their acceptance and their matching hash pins. The exception is `RowBoolean`, which I read in full.
- **Python replay limits.** The Python replay is my own port of the Lean definitions, so it is a diagnostic, not a proof. I cross-checked it against the independent verifier (`nextWord` vs `F`; `prefixPredecessors` vs `prefix_predecessors`), but a porting error could still hide a discrepancy. Only kernel checking is authoritative.
- **Generated files read individually.** I did not read every generated file line by line. I read these in full:
  - `Rows218_000`, `Rows218_049` and `Rows218_104`;
  - `Short218_00`, `Short218_17`, `Initial218_00` and `Initial218_09`;
  - all of the aggregation modules.

  For the rest I checked the theorem headers, tactics and tokens with grep. Lean's typing enforces that they fit together.
- **Regeneration and full verifier run.** I did not run `verify_certificates.py` end to end, including its integer dynamic-programming control up to 10^6; I relied on the recorded `verification_results.json` (PASS). I did not regenerate `cert218/` to check that the generator's output is byte-for-byte reproducible.
- **Other prefixes.** I did not check the 777 and 217 instances (they have not been generated) or 620.
- **Toolchain and runner.** I did not check the Lean binary or archive pins, the environment, or how `check.py` behaves at runtime. I only diffed it against Agent #104's runner; the only change is module lookup.
- **Other records.** I did not check the README's CPU and memory figures, or the coordination and task records.

## Reproducing the diagnostics

The scripts are outside the repository, in a temporary session folder:

- `/tmp/claude-0/-home-claude/88b9065f-2003-50b8-aa17-0286a306196c/scratchpad/review118/lean_sem.py` (Lean definitions ported to Python)
- `/tmp/claude-0/-home-claude/88b9065f-2003-50b8-aa17-0286a306196c/scratchpad/review118/parse_tree.py` (rebuilds `ranks` from `Rank218Data*.lean`)
- `/tmp/claude-0/-home-claude/88b9065f-2003-50b8-aa17-0286a306196c/scratchpad/review118/replay218.py`
- `/tmp/claude-0/-home-claude/88b9065f-2003-50b8-aa17-0286a306196c/scratchpad/review118/short_edges_all.py`

Run them with `python3 -I -B`. `replay218.py` takes about 5 seconds; `short_edges_all.py` takes a few minutes. None of them writes into the repository.
