# Sprint 19 — independent review of the 11 unreviewed results

Agent 19, 2026-10-22. Repository state reviewed: `main` at `c6902ac` (2026-10-21).

## 1. Answer

None of the 11 results is vacuous, and for every one of them the Lean endpoint says what a careful
reader would expect from its definitions: the target predicates (`Starts3`, `StartsL`,
`Starts739`) mean "the canonical decimal numeral has exactly these leading digits", `orbit` and
`Palindrome` are the plain definitions, and every main 196 endpoint is unconditional. I proved
this reading in Lean: each exclusion implies the plain statement "no palindrome iterate of 196
has a decimal truncation `orbit 196 t / 10^k` equal to the prefix" (`Sprint/Agent19/Fidelity.lean`,
`ArithTransfer.lean`). The problems are in the **prose** (README, RESULTS.md, registry scopes, and
this sprint's brief), not in the Lean statements. Three results get **statement-mismatch**:
**Agent117RemainingCycles** (the prose says 14 prefixes are "provably out of reach" of the
method; Lean only shows failure at one width, k = 7 or 8, and in a certificate format that is
not the one the certificates use — the format gap is now closed in Lean, the width gap is real,
and 74 four-digit children of 12 of these 14 prefixes are in fact excluded by the same method),
**Agent119EightFamilies** (README, RESULTS heading and the brief say "dd0…0dd"; Lean covers only
an even number of zeros, `dd 0^(2r) dd`), and **Agent118PrefixKernel** (the scope says 218 is
reached within 33 steps; Lean proves `t ≤ 34`, and "33 is attained" refers to a certificate rank,
not to an actual orbit). The other eight are **OK**. A forward scan of 14.9 million seeds found
no violation of any of the 1,769 ancestry bounds involved, and it found a new 19-step delay
witness for 777 (previous: 14), now Lean-verified.

## 2. Per-result verdicts

| Result | Verdict | Main endpoint(s) | Notes |
|---|---|---|---|
| Agent118PrefixKernel | OK (Lean) · **statement-mismatch** (prose, minor) | `Agent118.Finite217.no_196_217_palindrome`, `…218…`, `…777…` | Scope: "within 23, 33 and 25 steps". Lean: `ancestry_bound23`, **`ancestry_bound34`**, `ancestry_bound25`. `Controls218.bound33_attained` is `lookup ranks (targetInitialWord 2 1 8 9988) = some 33` — a rank in the tree, so the certified bound is 33 + 1 = 34; the largest known actual 218 delay is 15 (`Witnesses.depth15_218`). |
| Agent124Prefix620 | OK | `Agent124.CertPrefix620.no_196_620`, `ancestry_620 : … t ≤ 12` | Sharp: `Agent104P620Witness` seed 19014942070 reaches 62003033030026 at t = 12 (also reproduced by my scan). |
| Agent104Prefix739 | OK | `SevenColumnKernel.Finite739.no_196_739_palindrome`, `ancestry_bound39` | |
| Agent124PrefixFiveSix | OK | `Agent124.PrefixSummary.no_196_all`, `ancestry_all`, `classes_length` | 33 single three-digit prefixes ("classes" is only a name). Prefix 119 (leading 1) uses `Agent124.LeadOne`: an overflow palindrome has all digits ≤ 2, so digit 9 rules it out — correct. Bounds for 385 (8), 474 (7), 674 (5), 923 (7) are attained by actual seeds (scan), so those are sharp. |
| Agent124FourDigit | OK | `Agent124.CertF4.no_196_00…06`, `Agent124.CertF5.no_196_00…04` | 1,730 four-digit prefixes (F4, k = 4: 1,267; F5, k = 5: 463), all valid digit words, no duplicates, no parent already excluded; largest ancestry bound 48. README's "1731" = these 1,730 + 2641 (Agent117P2641). |
| Agent124ForwardInvariant | OK | `Agent124.FwdW3.no_196_excluded`, `excluded_length` | Reproduced independently (Python): the forward closure of the outer 3 pair sums of orbit(196, 100) has 4,194 words; exactly 277 three-digit words with `noOverflowPre` fall outside; per leading digit 34, 16, 47, 20, 31, 39, 37, 40, 13 — identical to Lean. 124 of the 277 are also excluded by other results. |
| Agent119EightFamilies | OK (Lean) · **statement-mismatch** (README, RESULTS heading, brief) | `Agent119.EightFamilies.orbit196_ne_fam`, `Agent423.TemporalResidues.*` | `fam d r = 11·d·(10^(2r+2)+1)` has exactly **2r zeros** (r ≥ 0, so `dddd` is included). Odd zero counts, e.g. 11011, are **not** covered for d ∈ {1,2,4,7,8}. The registry scope says `0^(2r)` correctly. d = 3, 6, 9 follow from "never divisible by 3"; the nontrivial content is d ∈ {1,2,4,7,8}. `phase_has_palindrome_representative` uses the two-digit palindromes 11…88, which is enough for the stated impossibility (`no_mod99_only_palindrome_exclusion`). |
| Agent113FiveLayer | OK | `Agent113.FiveLayer.no_196_full_pattern`, `five_layer`, `five_layer_strong`, `sharp_four` | Non-vacuous (80008 has the pattern). Scan: no seed orbit has `OuterPattern` at any 5 ≤ t ≤ 120. |
| Agent117RemainingCycles | OK (Lean) · **statement-mismatch** (README, RESULTS, scope) | `Agent117.Cycle*_k*.no_checked_tree_contains_p0`, `checkInitial_fails`, `forwardAdmitted_project` | See §2.1. |
| Agent315Orbit196Residues | OK | `Agent315.TemporalColumn99.not_dvd3_orbit196`, `not_dvd9_orbit196` | Same fact as `Agent119.EightFamilies.orbit196_not_dvd3` and `Agent423.TemporalResidues.orbit196_mod3_nonzero` (proved three times). |
| Agent9DigitSumWindows | OK | `DecimalUniformEscape.digitSum_uniform_window_196`, `…_sharp`, `P196.Agent9.FactorialEscape.digitSum_uniform_window_196_factorial`, `P196.Agent9.IntervalCounts.digitSum_interval_count_196` | True for every positive seed, so it carries no information specific to 196 (the scope says so). README's "the digit sum grows" means "exceeds every B in every window", not monotone growth. |

**Vacuity check (all 11): none vacuous.** The 196 endpoints have no hypotheses. Ancestry-bound
hypotheses are satisfiable (`A = P`, `t = 0`). All 2,040 listed prefixes (277 + 1,730 + 33) are
genuine digit words with leading digit ≥ 1 (Lean `excluded_valid` for the 277; Python for all;
Lean `*_valid` files for the other lists are written, see §3). `FullPattern` is inhabited
(`sharp_four`).

### 2.1 Agent117RemainingCycles in detail

What Lean proves (one witness each): for prefix P and width k (k = 7; k = 8 for 112 and 275) there
is an initial word `p0` (P followed by digits) with a verified backward entry walk into a verified
closed walk of the forward map, hence **no rank tree checked against the full inverse
`prefixPredecessors` contains `p0`**.

Prose: README "14 three-digit prefixes cannot be handled this way … need a different argument";
RESULTS "14 are provably out of reach of this method"; table marks them `x`.

1. **Width.** `forwardAdmitted_project` maps (k+1)-column edges to k-column edges, so a cycle at
   width k says nothing about widths above k. The brief's own data shows prefixes certified only
   at k = 8, 9, 10. Nothing in Lean says these 14 fail at k ≥ 9 (k ≥ 8 for twelve of them).
2. **Refinement.** The same method already excludes 74 four-digit children of 12 of these 14
   prefixes (`Agent124FourDigit`), e.g. 1380–1384 and 1640–1648, at k = 4 or 5 (COMPUTED,
   `check_lists.py` + listing in §4). Only the full three-digit class is blocked at that width.
3. **Format (closed here).** The certificates in use check rows only at the certificate width:
   `CheckedRows tree (longPred 7)` (Agent104/118) and `RowsClosed k R` (Agent124). Agent117's
   hypothesis `CheckedRows tree prefixPredecessors` is a different (stronger) requirement, so its
   theorem did not literally apply to them. `Sprint/Agent19/CycleFormats.lean` proves, for all 14:
   `no_rank_P : RowsClosed k R → R p0 = none`, `no_tree_P : CheckedRows tree (longPred k) →
   lookup tree p0 = none`, and `no_entry_P : RowsClosed k R → entryOK k R (P, b) = false` for every b.

Suggested wording: "for these 14 prefixes the k-column method fails at width k = 7 (k = 8 for 112
and 275) and at every smaller width; larger widths and longer prefixes are not ruled out".
(The "every smaller width" part follows from the projection lemma but is not itself a Lean
theorem yet.)

## 3. What is LEAN-VERIFIED, COMPUTED, CONJECTURE

### LEAN-VERIFIED (new files, all build on this branch with Lean 4.19.0; axioms printed)

All in `lean/P196/Sprint/Agent19/`. Every `#print axioms` line reports only `propext`,
`Classical.choice`, `Quot.sound` (some fewer). No `sorry`, `native_decide`, or new axioms.
Measured elaboration time on a 2-vCPU, 8 GB container: Fidelity 1.6 s, CycleFormats 2.8 s,
ArithTransfer 0.7 s, ArithLight 2.7 s.

- `Fidelity.lean`
  - `Sprint.Agent19.Fidelity.startsL_of_div` — if `n / 10^k = fromDigits pre` (pre nonempty,
    digits ≤ 9, leading digit ≥ 1) then `Agent124.PrefixL.StartsL pre n`.
  - `plain_of_palStartsL`, `plain_of_valid` — `¬ PalStartsL pre N` implies
    `Palindrome N → ∀ k, N / 10^k ≠ fromDigits pre`.
- `ArithTransfer.lean`
  - `transfer118`, `transfer124`, `transfer739`, `transferList` — the same plain reading for all
    four target formats used by the reviewed results.
  - `depth19_777 : ∃ A P, 0 < A ∧ PalindromeStarts3 7 7 7 P ∧ orbit A 19 = P`
    (A = 10000026100, P = 77798878687889777). Lower bound for 777 improves from 14 to 19;
    certified upper bound is 25.
- `ArithLight.lean`
  - `excluded_valid` — all 277 words are valid three-digit prefixes.
  - `forward_plain : ∀ T k, Palindrome (orbit 196 T) → ∀ w ∈ excluded, orbit 196 T / 10^k ≠ fromDigits w`.
- `CycleFormats.lean` — 42 theorems `no_rank_P`, `no_tree_P`, `no_entry_P` for the 14 prefixes
  (§2.1), via `none_of_walks` and `rowsClosed_of_checked`.

### Written, not yet compiled here (need the certificate modules built)

`Arith118.lean` (`plain_217`, `plain_218`, `plain_777`), `Arith620.lean`, `Arith739.lean`,
`ArithClasses.lean` (`classes_valid`, `plain_classes`), `ArithFourDigit.lean` (`*_valid`,
`plain_F4_*`, `plain_F5_*`), `AuditHeavy.lean` (prints axioms of all 60 endpoints of the five
certificate results). Each is a one-line application of a verified transfer lemma, but **until it
builds it is not LEAN-VERIFIED**. The container has 2 vCPUs and 8 GB; the modules these files
import (2,718 modules not yet built here, 39.8 MB of Lean source) did not finish in this session. `AuditLight.lean` (237 endpoints of the six
light results) is in the same state until `Agent113FiveLayer` finishes building here.

### Build and axiom status of the 11 results

- Built locally from source here, with all printed axioms within the allowed set:
  Agent315Orbit196Residues, Agent119EightFamilies, Agent9DigitSumWindows, Agent117RemainingCycles,
  Agent124ForwardInvariant (`lake build <roots>`, exit 0).
- Not rebuilt here (Agent113FiveLayer, Agent124FourDigit, Agent124Prefix620, Agent104Prefix739,
  Agent124PrefixFiveSix, Agent118PrefixKernel): COMPUTED by CI only — the nightly full
  `python3 tools/verify.py` run 39803889093 on commit c6902ac (2026-10-22 15:20–19:54 UTC) ended
  `[axioms] 6254 endpoints checked` / `ALL CHECKS PASSED`; its log shows e.g.
  `Agent118.Finite217.no_196_217_palindrome depends on axioms: [propext, Classical.choice, Quot.sound]`.
  CI restores built modules from a cache, so that run did not recompile everything from scratch.

### COMPUTED (scripts in `sprint/agent-19/`)

- `forward_invariant.py 3` → `k=3: start word (8, 8, 13); forward closure size 4194; excluded words 277; by leading digit 1..9: [34, 16, 47, 20, 31, 39, 37, 40, 13]`.
- `check_lists.py` → `F4 (k=4): … entries=1267 … max rank bound=20 … invalid=0 duplicates=0`,
  `F5 (k=5): … entries=463 … max rank bound=47 … invalid=0 duplicates=0`,
  `F4+F5: 1730 entries, 1730 distinct prefixes`.
- Union of excluded three-digit prefixes: 130 (two-digit children) + 5 kernels + 33 classes + 277
  forward = **321 distinct**, 124 of the 277 also excluded elsewhere — matches RESULTS.md. None of
  the 14 cycle prefixes is excluded. All 1,730 F4/F5 parents are outside the 321; 74 of them lie
  under 12 of the 14 cycle prefixes (all except 112 and 716).
- Falsification scan (`scan.c`, every t ≤ 120, palindromes of width ≥ 3, orbit continued past
  palindromes): seeds 1 … 9,999,999 (1 min 48.6 s, 14,834,616 palindrome hits) and the 4,906,044
  seeds below 10^13 with at most 4 nonzero digits (1 min 4.6 s, 7,936,484 hits).
  `compare_bounds.py` → `claims checked: 1769; prefixes reached by the scan: 1769; violations: 0`;
  651 bounds attained exactly. `OUTER` lines: 0 (no `OuterPattern` at 5 ≤ t ≤ 120).
  Max delays seen: 217 → 15, 218 → 3, 777 → 19 (seed 10000026100), 620 → 6, 739 → 12.

### CONJECTURE / IDEA

- IDEA: for the 14 cycle prefixes, rerun the batch generator at k = 9, 10 on the three-digit class
  and on its ten children; the 74 excluded children show the classes are not uniformly blocked.
- IDEA: the odd-zero families `dd 0^(2r+1) dd` (d ∈ {1,2,4,7,8}) are untouched; Agent 17 can
  try the same descent argument.

## 4. Reproduce

```bash
git checkout sprint/agent-19-review
cd lean
# LEAN-VERIFIED part (lake builds the imported results first; minutes)
lake build P196.Sprint.Agent19.Fidelity P196.Sprint.Agent19.ArithTransfer \
  P196.Sprint.Agent19.ArithLight P196.Sprint.Agent19.CycleFormats
# pending part (imports the large certificate results; hours on one core)
lake build P196.Sprint.Agent19.Arith620 P196.Sprint.Agent19.Arith739 \
  P196.Sprint.Agent19.ArithClasses P196.Sprint.Agent19.ArithFourDigit P196.Sprint.Agent19.Arith118
lake env lean P196/Sprint/Agent19/AuditLight.lean   # axioms of 237 endpoints
lake env lean P196/Sprint/Agent19/AuditHeavy.lean   # axioms of 60 endpoints
cd ..
# COMPUTED part
python3 sprint/agent-19/forward_invariant.py 3
python3 sprint/agent-19/check_lists.py
cc -O2 -o /tmp/scan sprint/agent-19/scan.c
/tmp/scan 1 10000000 120 > /tmp/scan_dense.txt
python3 sprint/agent-19/sparse_seeds.py 13 4 | /tmp/scan 0 0 120 > /tmp/scan_sparse.txt
python3 sprint/agent-19/compare_bounds.py /tmp/scan_dense.txt /tmp/scan_sparse.txt
```

`tools/verify.py` will report the `Sprint/Agent19` files as unregistered: the brief forbids editing
`lean/registry.json`, so they are not registered on this branch. (AGENTS.md forbids branches and
pull requests; this branch and its draft PR follow the sprint brief instead.)

## 5. For the next agent

1. Prose fixes (no Lean change needed):
   - Agent118PrefixKernel scope / RESULTS: "within 23, **34** and 25 steps"; "the certificate rank
     33 is attained" instead of "the 218 bound 33 is attained".
   - Agent119EightFamilies: README and RESULTS heading "dd 0^(2r) dd (an even number of zeros)".
   - Agent117RemainingCycles: README, RESULTS line "14 are provably out of reach", table legend
     `x`, open problem 2 — restrict to "at width 7 (8 for 112, 275)", and mention the 74 excluded
     children.
   - The sprint brief's "palindromes dd0…0dd never occur for d≠5" has the same over-reach.
2. Compile the pending `Arith*.lean` / `AuditHeavy.lean` on the Mac Studio (or any machine with
   the certificate modules built) and, if accepted, register `Sprint/Agent19` as a result.
3. Agents 4 and 6: the 14 cycle prefixes are open at k ≥ 9 (≥ 8 for twelve of them); their
   children are partly certified already.
