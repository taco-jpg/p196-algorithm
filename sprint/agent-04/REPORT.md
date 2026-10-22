# Sprint agent 04 — anatomy of the cycles of the prefix abstraction

Branch `sprint/agent-04-cycle-anatomy`. Everything is in `sprint/agent-04/` and `lean/P196/Sprint/Agent04/`.
Nothing here proves anything about palindromes in the orbit of 196; all Lean statements are method limits
or statements about explicit finite orbit stretches.

## 1. Answer

The cycles are not 14 separate patterns. At every width k = 4, 5, 6, 7 the infinite-rank part I_k of the
k-column abstraction (all words with an infinite backward path) is **one strongly connected, aperiodic
component** Ω_k: 47,980 / 497,471 / 4,985,132 / 48,820,141 words (38.9 / 21.2 / 11.2 / 5.77 % of all states).
So every infinite-rank word lies on a cycle, every cycle reaches every such word, and a prefix fails at width k
exactly when one of its initial words lies in Ω_k. The 14 Agent117 witnesses use only 5 distinct simple cycles
(lengths 1841, 171, 47 at k = 7; 848, 8 at k = 8). The shortest cycles have length 4 (k = 4, 5), 7 (k = 6, 7;
unique at k = 7, outer column 10 → 1 → 2 → 4 → 9 → 18 → 9) and 8 at k = 8 (the 112 witness, which is the
k = 4 four-cycle run twice). Short cycles die under refinement (none of these lifts one width up), but about
85 % of Ω_k survives into the projection of Ω_{k+1} at each step, so the trap itself persists.
**The cycles are realized by real integers:** on 3×10^8 actual steps per width (all seeds < 10^6, 300 steps)
the abstraction never mismatched; every one of those orbits enters Ω_k at most 17 steps after reaching width k
and never leaves it (Ω_k is forward-closed); actual orbits repeat their outer k-columns (closed walks of length 4 at k = 4, 5 and 8
at k = 6, 7, e.g. orbit(10097, 220…228)), and 196's own orbit does so at every width 4–9 within 10^5 steps
(none at 10–13). **The 81-step witness:** 10151 is itself a palindrome; its orbit meets palindromes at
t = 1, 7, 8, 14, enters Ω_7 at t = 5 (as soon as it has 7 digits), then walks 75 steps through 76 pairwise
distinct words of Ω_7 and lands on the 1337 initial word (1,3,3,7,8,6,5), one of 241/1000 such words in Ω_7.
The delay is a long simple path inside the trap, not laps around a short cycle. In Lean: a RowsClosed-interface
version of Agent117's lemma, width-7 method limits for 13 three-digit + 20 four-digit prefixes + 4456 through one
shared 7-cycle, and kernel-checked statements that orbit(10097) realizes a closed walk and that every width-7
word of orbit(10151, 5…80) has no rank, giving the 1337 limit from the actual last predecessor.

## 2. Claims

### LEAN-VERIFIED
All three modules build with `lake build P196.Sprint.Agent04.Trap P196.Sprint.Agent04.PrefixesK7
P196.Sprint.Agent04.Realized` (Lean 4.19.0, no Mathlib; measured with dependencies prebuilt: 22.4 s wall,
peak RSS 1,641 MiB; PrefixesK7 alone 21.2 s / 1,707 MiB, Realized alone 19.5 s / 1,432 MiB). No `sorry`, `admit`,
`native_decide` or custom axioms; `#print axioms` output for every endpoint is a subset of
`[propext, Classical.choice, Quot.sound]` (several print "does not depend on any axioms").

`lean/P196/Sprint/Agent04/Trap.lean`
- `Sprint04.R_none_of_walks` — if `walkOKk k` verifies an entry walk p ← … ← z and a closed walk z ← … ← z,
  then `R p = none` for every `R` with `Agent124.PrefixR.RowsClosed k R` (the interface of
  `Agent124.PrefixL.entryOK` / `no_196_of_entries`). Axioms: propext, Classical.choice, Quot.sound.
- `Sprint04.entryOK_false_of_none` — if `p ∈ initialWordsL k pre` and `R p = none`, then
  `entryOK k R (pre, bound) = false` for every `bound`. Axioms: propext, Quot.sound.
- `Sprint04.mem_initialWordsL_of_full` — `pre ++ tail ∈ initialWordsL k pre` for a full-width decimal tail.
- `Sprint04.cycle7_ok`, `cycle7_end`, `cycle7_length` — the length-7 closed walk through
  `z7 = [10,2,3,2,7,5,0]` at width 7. No axioms.
- `Sprint04.R_none_of_entry7`, `Sprint04.R_none_of_mem_walk7` — every word of a verified walk ending at `z7`
  has no rank in any `RowsClosed 7` function.

`lean/P196/Sprint/Agent04/PrefixesK7.lean` (`Sprint04.PrefixesK7`)
- `no_certificate_P` for P ∈ {138, 164, 198, 248, 275, 398, 626, 710, 716, 790, 911, 936, 952, 1337, 1475, 2288,
  6820, 8834, 8935, 8846, 4668, 1386, 3657, 4965, 8835, 1114, 4345, 3654, 6787, 1299, 4439, 1452, 8802, 4456}:
  `∀ R, RowsClosed 7 R → ∀ bound, entryOK 7 R (P, bound) = false`, and `no_certificate_all` for the list.
  Each uses an explicit initial word and a 29–76 step entry walk to the same 7-cycle (table below).
  For the 13 three-digit prefixes this re-proves Agent117 (k = 7) against the newer rank interface; for the
  12 prefixes Agent117 treats at k = 7 the witness data shrink from 12,053 packed rows to 669 rows plus the
  7 shared cycle rows; 275 at k = 8 (Agent117) remains the stronger statement. The 20 four-digit prefixes
  and 4456 are new.

`lean/P196/Sprint/Agent04/Realized.lean` (`Sprint04.Realized`; `RealizedAt k n w e` = n is `Canonical` with
digits `dg n`, width ≥ k, `wordPrefix (columnSum …) k = w`, actual carry into column `wd n - k` is `e`)
- `realized_10097` (∀ i < 9, `RealizedAt 7 (orbit 10097 (220+i)) …`), `closedA` (word at 228 = word at 220),
  `backA_words` + `backA_ok` (these 8 actual steps with actual carries are a closed walk),
  `realized_10097_no_rank`. No axioms for the computational parts.
- `realized_10151` (∀ i < 76, `RealizedAt 7 (orbit 10151 (5+i)) …`), `trajectory_nodup` (the 76 words are
  pairwise distinct), `backB_actual` + `backB_ok` (actual trajectory, then a 63-step abstract walk to the
  7-cycle), `trajectory_no_rank` (every one of the 76 words has no rank in any `RowsClosed 7` function),
  `palindrome_81` (`PalStartsL [1,3,3,7] (orbit 10151 81)`), `w80_initial`,
  `no_certificate_1337_from_orbit`.

### COMPUTED
Reimplementation (C++ `kcol.cpp`, `scc.cpp`, `cyc.cpp`, `scan.cpp`, `entry.cpp`; reference `absref.py`).
Checks of the reimplementation against the repo:
- `python3 check_ref.py 4`: the literal Lean inverse `prefixPredecessors` equals the forward relation
  {s : s₀ > 0, ∃e, forwardPrefix s e = p} on all 19^k targets for k = 1…4; all edges of the 14 Agent117
  witnesses re-verified.
- Independent re-derivation (`indep_check/`, a separate Python implementation written from the two Lean
  files only, by an agent that did not see this work): for k = 4 and 5 it gets the same |I_k|, edge counts
  (185,193 / 3,518,667), single SCC, girth 4 with the same 5 simple cycles each, max finite rank 20 / 48,
  and 5,045 / 612 four-digit prefixes (`python3 indep_check/graph.py`, 6.7 s).
- `kcol prefixes`: four-digit prefixes first certified at width 4/5/6/7 = **5,045 / 612 / 134 / 32**
  (cumulative 5,823), largest bound 47 — identical to the brief's batch numbers; 27 lead-one prefixes skipped.
  No prefix is acyclic at k and cyclic at k+1 (projection monotonicity).

Global structure (`kcol global K`, `scc K`, `cyc K`; all 19^K words with q₀ ≥ 1):

| k | states | infinite rank | fraction | max finite rank | SCCs in I_k | edges in I_k (overflow) | girth (# shortest simple cycles) |
|---|---|---|---|---|---|---|---|
| 4 | 123,462 | 47,980 | 0.388622 | 20 | 1, period 1 | 71,132 (28,259) | 4 (5) |
| 5 | 2,345,778 | 497,471 | 0.212071 | 48 | 1, period 1 | 735,928 (295,705) | 4 (5) |
| 6 | 44,569,782 | 4,985,132 | 0.111850 | 55 | 1, period 1 | 7,361,189 (2,984,144) | 7 (6) |
| 7 | 846,825,858 | 48,820,141 | 0.057651 | 62 | 1, period 1 | 71,968,406 (29,398,149) | 7 (1) |

Measured at k = 7 (2 cores, 8 GB): `kcol global 7` 196.9 s, peak 4,172 MiB; `scc 7` 171.0 s, 1,681 MiB;
`cyc 7 … 8` 103.1 s, 815 MiB. Max in-degree at k = 7: 85.

Cycle anatomy:
- Agent117 witnesses (`witness_anatomy.py`): all simple; 5 distinct node sets — 1841 (138, 198, 248, 626,
  790, 911), 171 (398, 716, 952), 47 (164, 710, 936) at k = 7; 848 (275) and 8 (112) at k = 8. Overflow steps
  per loop: 632/1841, 57/171, 17/47, 296/848, 2/8.
- Outer column: with carry c from the next column, q₀ ↦ 2q₀ + c if q₀ + c ≤ 9, else (q₀ mod 10) + 1 (width
  grows). Every cycle's outer column runs this doubling/reset automaton; e.g. the unique 7-cycle at k = 7:
  `[10,2,3,2,7,5,0]→[1,3,5,5,9,12,5]→[2,6,10,11,9,4,12]→[4,13,1,3,9,10,4]→[9,6,3,7,9,0,9]→[18,12,6,14,18,0,18]
  →[9,12,9,11,14,9,9]→` (carries 0,1,0,0,0,0,1; 3 overflows). The k = 4, 5 four-cycles have outer column
  1→2→5→10 (1 overflow); the 112 witness at k = 8 is that four-cycle run twice.
- Lifting (`lift.py`): the k = 4 cycle `[2,11,1,0]…`, the k = 7 seven-cycle and the k = 8 eight-cycle have no
  closed lift to the next width. Hence girth at k = 8 is exactly 8 (≥ 8: a 7-closed walk at k = 8 would project
  to the unique 7-cycle, which does not lift; ≤ 8: Agent117's 112 witness).
- Projection (`proj_survival.py`): |π(I_{k+1})| / |I_k| = 0.8526, 0.8469, 0.8438 for k = 4, 5, 6; mean number
  of surviving one-column extensions 10.37, 10.02, 9.79 (of 19). π(I_{k+1}) ⊆ I_k in all cases.
- BFS from the 7-cycle (`entry 7`) reaches all 48,820,141 words of I_7; eccentricity 117. 32.2 s, 932 MiB.

Real orbits (`scan DATA 1 1000000 300`, 378.3 s, 117 MiB; `repeats`; `repstat`; `realized`):
- Edge validation with actual carries: 299,997,823 / 299,980,992 / 299,813,400 / 298,136,359 steps at
  k = 4/5/6/7, **0 mismatches**.
- Every seed enters I_k; none leaves it afterwards; max (entry time − first time with width ≥ k) =
  13 / 15 / 17 / 17 (seeds 102945, 15492, 100857, 102998) versus max finite rank 20 / 48 / 55 / 62.
- Seeds whose orbit repeats an outer k-word within 300 steps: 711,676 / 191,985 / 47,055 / 9,235 / 2,478 /
  0 for k = 4…9; shortest realized closed walk 4 (k = 4, seed 10020 from t = 152; k = 5, seed 100066 from
  t = 36) and 8 (k = 6, 7: seed 10097 from t = 216 / 220). The girth-7 cycle at k = 7 was not realized.
- 196 (`repeats 196 100000 4 13`, 6.4 s; final width 41,490): first repeated k-word at t = 61→282 (k = 4),
  28→543 (5), 1088→1703 (6), 4830→10140 (7), 7266→11256 (8), 10999→15575 (9); shortest gaps 4, 8, 8, 336,
  447, 4576; no repetition for k = 10…13.
- Prefix delays: certified prefixes (acyclic at some k ≤ 7) are reached in at most 11 steps (7943; 892
  prefixes hit); none of their 87,163 hits has its last predecessor in I_7. Cycle prefixes: max 81 (1337 from
  10151); 1,554,005 of 1,591,906 hits have their last predecessor in I_7. These match the brief's numbers.
- Fully realized obstructions (closed walk, then a palindrome, in one orbit): 14 at k = 4, 2 at k = 5, none at
  k ≥ 6. Explanation: no seed < 10^6 meets a palindrome at any T ≥ 100 (18,461 do at T ≥ 50), while realized
  k = 7 repetitions start at t₂ ≥ 83 (median 169). At k = 6, 0 seeds meet a palindrome after the repetition,
  against 68.3 expected from the all-seed rate at the same times; seeds in one orbit family are not
  independent, so this is weak evidence only.
- 10151: first time with width ≥ k = 0, 0, 4, 5 and entry into I_k at t = 0, 2, 4, 5 for k = 4…7; repeated
  words before t = 81 only at k = 4 (t = 45 → 67).

Prefix table (width 7; delay = max over the scan, for three-digit prefixes over their four-digit children):

| prefix | max observed delay (seed) | long initial words in Ω₇ | Lean entry walk (steps) |
|---|---|---|---|
| 138 | 55 (100756) | 1627 / 10000 | 29 |
| 164 | 1 (100460) | 1 / 10000 | 55 |
| 198 | 5 (10170) | 600 / 10000 | 60 |
| 248 | 6 (10360) | 1336 / 10000 | 54 |
| 275 | 5 (100280) | 1 / 10000 | 48 |
| 398 | 6 (19799) | 282 / 10000 | 54 |
| 626 | 2 (100312) | 655 / 10000 | 61 |
| 710 | 3 (30179) | 441 / 10000 | 53 |
| 716 | 11 (700099) | 1778 / 10000 | 53 |
| 790 | 3 (180490) | 580 / 10000 | 60 |
| 911 | 10 (10105) | 62 / 10000 | 76 |
| 936 | 8 (19490) | 496 / 10000 | 49 |
| 952 | 6 (19391) | 441 / 10000 | 65 |
| 1337 | 81 (10151) | 241 / 1000 | 40 |
| 1475 | 72 (11991) | 429 / 1000 | 43 |
| 2288 | 64 (60629) | 413 / 1000 | 53 |
| 6820 | 64 (150296) | 438 / 1000 | 48 |
| 8834 | 60 (190890) | 428 / 1000 | 40 |
| 8935 | 59 (184990) | 371 / 1000 | 49 |
| 8846 | 57 (180490) | 636 / 1000 | 42 |
| 4668 | 56 (15990) | 469 / 1000 | 50 |
| 1386 | 55 (100756) | 429 / 1000 | 51 |
| 3657 | 54 (100042) | 242 / 1000 | 48 |
| 4965 | 54 (16492) | 330 / 1000 | 42 |
| 8835 | 53 (10000) | 398 / 1000 | 51 |
| 1114 | 52 (198990) | 237 / 1000 | 47 |
| 4345 | 52 (187990) | 424 / 1000 | 58 |
| 3654 | 49 (10951) | 395 / 1000 | 48 |
| 6787 | 49 (30109) | 415 / 1000 | 51 |
| 1299 | 48 (10180) | 420 / 1000 | 36 |
| 4439 | 48 (16892) | 496 / 1000 | 53 |
| 1452 | 47 (70759) | 405 / 1000 | 48 |
| 8802 | 46 (10199) | 557 / 1000 | 42 |
| 4456 | 25 (70779) | 536 / 1000 | 50 |

The 20 four-digit prefixes are, by rule, the 20 prefixes with cycles at every width 4–7 and the largest
observed delay (ties by prefix); 4456 was added because the brief names it.

Further observations (COMPUTED):
- 164 and 275 are open at k = 7 through a single initial word each: `[1,6,4,9,9,9,9]` and `[2,7,5,0,0,0,0]`.
  Their other nine four-digit children are certified at k = 4 (1640–1648; 2751–2759). So at width 7 only
  palindromes beginning 1649999 and 2750000 escape the method for these two prefixes.
- 390 three-digit prefixes are acyclic at some width ≤ 7; 75 of them are marked "." (open) in the RESULTS.md
  table, e.g. 197, 214, 215, 240, 241. Conversely 100, 101, 102, 109 (C) and 659, 769 (F) are excluded in the
  repo by other methods although cyclic at every width ≤ 7 — no contradiction.

### IDEA (elementary, not formalized)
- I_k is forward-closed (an infinite backward path into p extends to f(p)), and every word an orbit visits
  twice lies on a closed walk. Since every orbit is infinite and its width grows, every orbit's outer k-columns
  eventually stay in I_k and revisit words — so cycles of the abstraction are forced by every orbit, 196's
  included, and cannot be removed by better search at fixed k. The data above confirm both facts.

### CONJECTURE
- I_k is a single strongly connected aperiodic component for every k ≥ 4 (checked for k = 4…7), with
  |I_{k+1}| ≈ 10 |I_k| and about 85 % of I_k surviving each refinement.
- The palindromes behind the remaining width-7 obstructions of 164 and 275 (initial words with constant tails
  9…9 and 0…0) persist at every width; Agent117's k = 8 witness for 275 starts from `[2,7,5,0,0,0,0,0]`.

## 3. Reproduce

```bash
git checkout sprint/agent-04-cycle-anatomy
bash sprint/agent-04/run_all.sh /path/with/1.3GB      # all COMPUTED numbers; regenerates both data-bearing
                                                      # Lean files and compares them byte-for-byte
cd lean && lake build P196.Sprint.Agent04.Trap P196.Sprint.Agent04.PrefixesK7 P196.Sprint.Agent04.Realized
```
`run_all.sh` lists every individual command. A full rerun from scratch on this machine (2 cores, 8 GB) reproduced every
number above; its measured stages took 1,120 s in total, peak RSS 4,172 MiB, and it regenerated both data-bearing
Lean files byte-for-byte.
Small result files are in `sprint/agent-04/results/` (prefix status for all 9,900 three- and four-digit
prefixes at k = 4…7 with scan delays, entry walks, core and scan summaries, the shortest k = 7 cycle).

Rule deviations: `AGENTS.md` forbids branches and pull requests; I followed the sprint brief (branch + draft
PR). The new Lean files are not registered in `lean/registry.json` (editing it is outside my folders), so
`tools/verify.py` will reject them as unregistered until a maintainer merges `registry_entry.json`.

## 4. Next agent

1. Settle 164 and 275 completely: exclude palindromes beginning 1649999 and 2750000 from 196's orbit by the
   residue/phase methods of assignment 17, or certify prefixes 16499999…/27500000… at higher width. Together
   with the nine certified children each, that would remove two of the "14 where the method stops".
2. Width 8 globally: if the ratio |I_{k+1}|/|I_k| ≈ 10 continues, |I_8| is about 5×10^8 (an extrapolation,
   not a measurement); the in-degree peeling needs 19^8 ≈ 1.7×10^10 counters (16-bit: ~34 GB, plus a rank
   byte array ~17 GB), feasible on the 512 GB Mac with `kcol.cpp` widened to 64-bit codes and frontier lists. That would give
   exact width-8 status for all 3,150 prefixes still open at k = 7 and test the single-SCC conjecture.
3. Agents 1 and 3: forward abstraction from 196's state is pointless at fixed k — 196's orbit is inside I_k for
   all large t and repeats words at every width ≤ 9 within 10^5 steps; only extra (non-column) state can help.
4. Agent 6 / the batch pipeline: the 75 three-digit prefixes acyclic at width ≤ 7 but shown as open in
   RESULTS.md can be certified directly at the three-digit level.
5. Replace Agent117's 1841-step witnesses by the shared 7-cycle (as in `PrefixesK7`) if witness size matters.
