# Sprint agent 20 — red team of the prefix-exclusion chain and of `CertificateToLychrel`

## 1. Answer

I could not break the chain "certificate ⇒ no 196 palindrome with prefix P". The target family
`PalStartsL` means exactly what the prose says (LEAN-VERIFIED equivalence with the textbook
definition "the decimal expansion begins with the digit string"); the `t ≤ 100` base check and the
off-by-one in `no_196_of_entries` are right; and an independent re-implementation of the backward
column-sum abstraction, written from the mathematical description only, reproduces **every**
ancestry bound on GitHub exactly — all 2,494 four-digit entries (1,731 on `main` + 763 on branch
`prefix-k45-certificates`) and all 38 three-digit endpoints (COMPUTED). Forward falsification scans
(all seeds below 10^7, 2,000,000 random seeds below 10^13, 300 steps each, plus record-delay seeds)
found **0** palindromes reached later than a Lean bound allows; 968 bounds are attained exactly
(COMPUTED). `CertificateToLychrel`'s conclusion is exactly "some m ≥ 10 is a decimal Lychrel number"
in the repository's canonical definitions (LEAN-VERIFIED); its hypothesis is not shown satisfiable,
and every accepted certificate uses only even phases (LEAN-VERIFIED).

What I did find:

- **(a) `tools/verify.py` accepts a theorem that was never kernel-checked.** A false `1 = 2` passes
  its regex and its axiom audit ("does not depend on any axioms"); minimal reproducer in
  `repro/SkipKernelTC.lean`. Nothing like it is in the repository today, and `lean4checker` catches it.
- **(b) 24 four-digit and 23 three-digit prefixes can never be certified with the current 100-step
  base check, at any width** (LEAN-VERIFIED, `Sprint.Agent20.Delay.no_entry_certificate`): each has a
  real seed reaching a palindrome with that prefix after more than 100 steps. The brief lists only
  4456. Four-digit: 1222 1332 1354 1365 1443 1469 1485 1573 1599 2212 2344 3599 3674 3878 4456 4479
  4618 4862 5554 5831 6633 6634 6842 8938. Three-digit: 122 133 135 136 144 146 148 157 159 221 234
  359 367 387 445 447 461 486 555 583 663 684 893. **A claimed certificate for any of these 24
  four-digit prefixes in the Mac Studio packages would contradict a Lean-verified theorem**, i.e.
  indicate a generator bug (or, if it passed Lean, a pipeline hole like (a)) — please grep for them;
  I had no access to the packages.
- **(c)** The "x = this method provably cannot decide it" wording for the 14 cycle prefixes is stronger
  than what `Agent117RemainingCycles` proves (widths ≤ 7/8 only, three-digit level only; 74 of their
  four-digit children are excluded on `main`).
- **(d)** The 36 Mac Studio batch packages (5,823 prefixes) are not on GitHub, so the "sample 50 of the
  new batch" check could only be run on the batch that is on GitHub (all 763 of it).

Nothing here says anything about whether 196 is Lychrel.

## 2. Results

### LEAN-VERIFIED (Lean 4.19.0, core + Std; files build with `lake build`; axioms printed)

Files: `lean/P196/Sprint/Agent20/{PrefixFidelity,Controls,DelayWitnesses,TextbookPrefixes}.lean`.
No `sorry`, `native_decide` or custom axioms; every endpoint uses at most propext, Classical.choice,
Quot.sound (several use fewer or none).

| Theorem | Statement (informal) | Axioms |
| --- | --- | --- |
| `Sprint.Agent20.startsL_iff_decStarts` | for a well-formed prefix (lead ≠ 0, digits ≤ 9): `StartsL pre P ↔ ∃ r, num pre·10^r ≤ P < (num pre + 1)·10^r` | propext, Classical.choice, Quot.sound |
| `Sprint.Agent20.startsL_of_decStarts` | the direction the prose needs (textbook ⇒ `StartsL`) | same |
| `Sprint.Agent20.no_196_textbook` | `∀ t, ¬ PalStartsL pre (orbit 196 t)` with well-formed `pre` ⇒ `∀ t r, ¬(Palindrome (orbit 196 t) ∧ num pre·10^r ≤ orbit 196 t < (num pre+1)·10^r)` | same |
| `Sprint.Agent20.palStartsL_lead_zero`, `palStartsL_big_digit` | `PalStartsL` is identically false for a prefix with a leading 0 or an entry ≥ 10 (an "exclusion" of such a prefix would be vacuous) | propext, Quot.sound |
| `Sprint.Agent20.Textbook.f4_00 … f4_06`, `f5_00 … f5_04` | all 12 entry lists of `Agent124FourDigit` (1,730 prefixes) are well-formed (`decide`), so each excludes exactly the textbook family | propext, Classical.choice, Quot.sound |
| `Sprint.Agent20.Textbook.no_196_2641_textbook` | `∀ t r, ¬(Palindrome (orbit 196 t) ∧ 2641·10^r ≤ orbit 196 t < 2642·10^r)` | same |
| `Sprint.Agent20.Delay.witnesses_ok` | 47 rows `(pre, seed, t, r)`: `orbit seed t` is a palindrome in `[num pre·10^r, (num pre+1)·10^r)` and `t > 100` (kernel evaluation of every orbit) | none |
| `Sprint.Agent20.Delay.no_bound_le_100` | for each listed prefix every uniform ancestry bound `∀ A P t, 0 < A → PalStartsL pre P → orbit A t = P → t ≤ B` has `B > 100` | propext, Classical.choice, Quot.sound |
| `Sprint.Agent20.Delay.no_entry_certificate` | for each listed prefix, any `entryOK k R (pre, bound) = true` with row/short-closed `R` forces `100 ≤ bound`, so `no_196_of_entries` can never be applied | same |
| `Sprint.Agent20.no_ancestry_bound_4456` / `_445` | `261 ≤ B` (seed 1186060307891929990, step 261, 119-digit palindrome) | same |
| `Sprint.Agent20.no_entry_certificate_4456` | `entryOK k R ([4,4,5,6], bound)` with closed `R` forces `260 ≤ bound` | same |
| `Sprint.Agent20.no_ancestry_bound_6634` / `_663` | `289 ≤ B` (seed 13968441660506503386020, step 289, 142-digit palindrome) | same |
| `Sprint.Agent20.no_ancestry_bound_5554` / `_555` | `101 ≤ B` (seed 1702190, step 101) | same |
| `Sprint.Agent20.orbit_agree`, `palindrome_agree` | `Agent109.orbit = Lychrel196.orbit`, `Agent109.Palindrome ↔ Lychrel196.Palindrome` (the copies `CertificateToLychrel` is stated with) | propext |
| `Sprint.Agent20.certificate_gives_isLychrel` | `check cert = true → ∃ m, 10 ≤ m ∧ Lychrel196.IsLychrel m` | propext, Classical.choice, Quot.sound |
| `Sprint.Agent20.check_phase_even` | `check cert = true → ∀ i < cert.P, (cert.st i).c ∈ [2,4,6,8,10,12,14,16]` | propext, Quot.sound |

Measured build cost (single `lake env lean`, dependencies prebuilt, 2-core x86_64 sandbox, 8 GB):
`PrefixFidelity` 4.0 s / 520 MB, `Controls` 9.1 s / 1,117 MB, `DelayWitnesses` 23.8 s / 2,904 MB,
`TextbookPrefixes` 5.8 s / 742 MB. All within the repository's 8 GB / 20 min budget.

The delay obstructions are about the method with the current 100-step base check. If assignment 8
verifies a longer prefix of 196's orbit (N steps) and generalizes `no_196_of_entries` to
`bound + 1 ≤ N`, the obstruction for a listed prefix becomes `bound + 1 ≥ t` against `bound + 1 ≤ N`;
with N ≥ 289 none of the 47 rows obstructs any more.

### COMPUTED

Commands in §3, measured outputs in `RUNS.md`.

1. **Independent recomputation of every certificate on GitHub** (`scripts/recompute_ranks.py`,
   `scripts/inverse_long.py`). The model: column sums `q_i = d_i + d_{L-1-i}`, outer k of them for
   `L ≥ k`, the full word for `L < k`; low digits exact, one free carry into the top block,
   overflow branch, short words exact; rank = longest backward path; bound = max rank over all
   possible last-predecessor projections of a palindrome with the prefix.
   - Model check against real orbits: 120,000 actual steps at k=4 and 30,000 at k=5 (random seeds up
     to 10^24) are all abstract steps. The column-search inverse equals the forward-enumeration
     reverse index on all 6,001 (k=3) and 110,002 (k=4) targets, with no spurious predecessors on the
     other long states.
   - k=4: 2,024/2,024 entries (1,267 `Agent124FourDigit.A124F4Entries` + 757 `PrefixK45.NewK4`):
     recomputed bound = claimed bound. k=5: 469/469 (463 `A124F5Entries` + 6 `PrefixK45.NewK5`) equal.
     k=7: 2641 recomputed 5 = claimed 5. (k=5 run: 17.0 s, 632 MB.)
   - Three-digit endpoints (claimed t-bounds): my rank + 1 equals the claimed bound for 217 (23),
     218 (34), 777 (25), 739 (39) at k=7, for 620 (12) at k=5, and for all 33
     `Agent124PrefixFiveSix` classes (24 at k=5, the other 9 at k=6). At smaller widths my bounds are
     larger or infinite, as expected.
2. **Static audit of all entry lists** (`scripts/extract_entries.py`): 2,494 entries, 2,494 distinct
   four-digit prefixes, no leading zero, no digit > 9, all pass `noOverflowPre`, all `bound + 1 ≤ 100`,
   every list consumed by a `no_196_NN` theorem, no prefix listed twice; largest bound 47 (5157).
   Coverage figures reproduce exactly: 4,941 four-digit prefixes covered on `main` (RESULTS.md),
   5,704 with the k45 branch and 396 fully covered three-digit prefixes (k45 commit message).
3. **Forward falsification** (`scripts/fwdscan.c`; every palindrome at every step 1..300 counts,
   not only the first):
   - seeds 1 … 9,999,999: 23 min 35 s, one core, 2.4 MB RSS;
   - 2,000,000 random seeds in [10^7, 10^13) (fixed RNG seed 2020): 3 min 58 s;
   - record seeds (measured here): 89 → 24 steps; 187 → 23; 10911 → 55; 147996 → 58; 150296 → 64;
     1186060307891929990 and 1999291987030606810 → 261 (4456…); 1000000079994144385 → 259 (4456…);
     12000700000025339936491 → 288 (6634…); 13968441660506503386020 → 289 (6634…);
     1000206827388999999 → no palindrome within 400 steps.
   - Combined: 2,491 of the 2,545 claimed prefixes (13 two-digit, 38 three-digit, 2,494 four-digit)
     were hit by some palindrome; **0 violations**; 968 bounds attained exactly; largest delay of a
     certified four-digit prefix 20 steps (2973, seed 405784242604).
   - Prefixes with an observed delay > 100: the 24 + 23 listed in §1(b) (Lean-checked). For the 14
     "x" prefixes the largest observed delays are 112: 71, 138: 69, 164: 1, 198: 39, 248: 48,
     275: 14, 398: 49, 626: 29, 710: 46, 716: 60, 790: 44, 911: 16, 936: 31, 952: 30 — no delay
     witness shows them uncertifiable at every width.
4. **Verification pipeline.** `repro/SkipKernelTC.lean` adds `RedTeam.bad : False` with
   `debug.skipKernelTC` through `run_cmd … addDecl` and derives `RedTeam.boom : (1 : Nat) = 2`.
   `lake env lean` prints `'RedTeam.boom' does not depend on any axioms`; `verify.py`'s `BANNED` regex
   (with its own `strip`) has no hit. `lean4checker` (tag v4.19.0) on the compiled module reports
   `(kernel) declaration type mismatch, 'RedTeam.bad' has type True but it is expected to have type
   False` and exits 1. Current repository: no `skipKernelTC`, `run_cmd`, `run_elab`, `addDecl`,
   `implemented_by`, `extern` or `unsafe` under `lean/P196`; the only `import Lean…` is
   `Agent2SaturatedProfile/PrefixModel.lean` (`Lean.Elab.Tactic.Omega`). `lean4checker` re-checked
   all 231 modules in the import closure of everything audited here (the prefix framework, all
   F4/F5/K7/k45 certificates, `CertificateToLychrel`, the 100-step check, my modules): 231 OK,
   0 failed (27 min total).

### Statement-level observations (no soundness problem)

- **"x" cells / "cannot be handled this way".** `Agent117RemainingCycles` exhibits a reachable cycle
  in the width-7 abstraction (width 8 for 112 and 275) from one specific initial word each (e.g. 138
  from `[1,3,8,6,6,6,0]`). Its projection lemma goes from k+1 to k columns, so cycles are established
  for widths ≤ 7 (≤ 8), not for every width, and only for the three-digit family as a whole: 74
  four-digit children of these prefixes are excluded on `main` (1380–1384, 1640–1648, 1980, 1981,
  1985, 1988, 1989, 2480, …). Suggested wording: "the width-7 (8) backward abstraction has a cycle;
  four-digit refinements can still be excluded". The cases that really are out of reach at any width
  with the 100-step base check are those of §1(b).
- **Batch numbers in the brief are not reproducible from GitHub.** "Widths 4–7 (5,823 prefixes, 36
  packages) are fully Lean-verified" refers to packages on the Mac Studio. GitHub has 2,494 Lean
  four-digit entries (1,731 merged + 763 on the unmerged `prefix-k45-certificates`). My scripts take
  any Lean entry files (`extract_entries.py <repo> <extra .lean files or dirs>`), so the check is one
  command once the packages are pushed; k=6,7 entries need `inverse_long.py`.
- **Process conflict.** `AGENTS.md` forbids branches and pull requests and requires every Lean file
  to be registered; the sprint brief asks for a branch, a draft PR and files under
  `lean/P196/Sprint/`. I followed the brief. `verify.py` will report my four files as unregistered
  until `lean/registry.json` gets an entry (I did not edit files outside my folders).
- `IsLychrel` counts time 0, the stronger convention for existence, so nothing is lost in
  `certificate_gives_isLychrel`.

### CONJECTURE / IDEA

- IDEA: run `lean4checker` (tag v4.19.0) in `verify.py`/CI over every built module, and reject
  `import Lean` outside an explicit allow-list. Banning the string `skipKernelTC` alone does not
  suffice, since a `run_cmd` can set the option programmatically.
- IDEA: the phase map `c ↦ 2·tOf c` restricted to even phases has exactly the cycles
  (2 4 8 16 14 10) and (6 12), so a certificate's period is a multiple of 6 or of 2. Agent 10 can
  drop all odd phases (the even part is LEAN-VERIFIED: `check_phase_even`).
- CONJECTURE: more four-digit prefixes have > 100-step witnesses. The 10^7 consecutive seeds gave
  one (5554), the record seeds two (4456, 6634), and 2,000,000 random seeds up to 10^13 the other
  21. A delay-targeted search (assignment 5) should find more and let the batch generator skip them.

## 3. Reproduce

```bash
git fetch origin sprint/agent-20-red-team && git checkout sprint/agent-20-red-team
cd lean && lake build P196.Sprint.Agent20.PrefixFidelity P196.Sprint.Agent20.Controls \
  P196.Sprint.Agent20.DelayWitnesses P196.Sprint.Agent20.TextbookPrefixes && cd ..
# static audit + independent recomputation (repo root); to include the batch branch:
git fetch origin prefix-k45-certificates && git checkout FETCH_HEAD -- lean/P196/PrefixK45   # local only
python3 sprint/agent-20/scripts/extract_entries.py . > /tmp/entries.json
python3 sprint/agent-20/scripts/recompute_ranks.py 4 /tmp/entries.json
python3 sprint/agent-20/scripts/recompute_ranks.py 5 /tmp/entries.json
python3 sprint/agent-20/scripts/inverse_long.py --check 3 4
python3 sprint/agent-20/scripts/inverse_long.py 7 2641 5
python3 sprint/agent-20/scripts/three_digit.py 5
python3 sprint/agent-20/scripts/three_digit_k.py 6 276:31 277:31 278:31 377:8 385:8 785:40 786:27 856:38 857:25
python3 sprint/agent-20/scripts/three_digit_k.py 7 217:23 218:34 777:25 739:39
# forward scans
cc -O3 -o /tmp/fwdscan sprint/agent-20/scripts/fwdscan.c
/tmp/fwdscan 1 10000000 300 > /tmp/fwd_1e7.txt
python3 -c "import random; r=random.Random(2020); print('\n'.join(str(r.randrange(10**e,10**(e+1))) for e in (r.randrange(7,13) for _ in range(2000000))))" > /tmp/rand.txt
/tmp/fwdscan -s 300 < /tmp/rand.txt > /tmp/fwd_rand.txt
python3 sprint/agent-20/scripts/compare_fwd.py /tmp/entries.json /tmp/fwd_1e7.txt /tmp/fwd_rand.txt
# kernel-bypass reproducer; lean4checker
(cd lean && lake env lean ../sprint/agent-20/repro/SkipKernelTC.lean)
git clone --depth 1 --branch v4.19.0 https://github.com/leanprover/lean4checker && (cd lean4checker && lake build)
(cd lean && lake env ../lean4checker/.lake/build/bin/lean4checker P196.Agent117P2641.Agent124PrefixL)
```

(The one-liner reproduces the exact 2,000,000-seed file used here; checked with `cmp`.)

## 4. Next agent

1. Push the 36 Mac Studio packages (or their entry lists); grep them for the 24 four-digit prefixes
   of §1(b) (any hit means a bug); then rerun `extract_entries.py` + `recompute_ranks.py` /
   `inverse_long.py` on them.
2. Put `lean4checker` into `verify.py` (both `--changed` and nightly).
3. Agents 5 and 8: `DelayWitnesses.lean` is a reusable checker (`witnessOK`) for more witnesses; with
   a verified prefix of N ≥ 289 steps none of the current witnesses obstructs.
4. Owner: correct the "x" legend in RESULTS.md / README; register `Sprint.Agent20` if it is merged.
