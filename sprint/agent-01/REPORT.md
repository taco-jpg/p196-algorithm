# Sprint agent 01 — Forward abstraction from 196's own orbit

Assignment 1: from 196's actual outer-k state, compute the forward-reachable set of the
k-column abstraction (unknown middle carry = nondeterminism), intersect with each open
prefix's backward closure / infinite-rank part, report counts and whether branching makes the
forward set "everything".

## 1. Answer

**Negative, and exact.** The forward set is *not* everything — at width k it is a vanishing
fraction of all admissible words (64.5 % at k=3, 1.46 % at k=9, roughly halving per column) —
but it is **exactly the infinite-history core** C_k of the abstraction: the set of words that
have arbitrarily long backward paths (equivalently, the backward method's obstruction set). For
k = 3..8 the forward closure from orbit(196,100) equals C_k word for word, C_k is a single
strongly connected component (checked k = 3..8), and the forward closure from 196's state at
t = 1,000, 10,000, 100,000 and 300,000 is the same set. Consequently, prefix by prefix, the
forward test ("no initial word of P is forward-reachable") and the backward test ("no initial
word of P lies on or after a cycle") give **identical** answers at every width k = 4..9, and the
forward abstraction yields **zero exclusions beyond the backward method**. Using a later start
time (extending the verified palindrome-free range) does not help either. The abstraction
carries no 196-specific information beyond "this orbit has a long history": any seed whose
width-k state has a backward history longer than the core's peel depth (9, 20, 48, 55, 62 steps
at k = 3..7) gets the same forward set. Side results: an independent, cap-free reproduction of
the batch counts 5,045 / 612 / 134 / 32 / 16 at widths 4–8; an exact width-9 classification of
all 9,000 four-digit prefixes (7 newly excluded at k=9 — one more than the batch's 6@k9, every
other prefix decided as "cycle at width 9", so none undetermined at k ≤ 9); and a Lean-verified
negative theorem: for 3,145 four-digit prefixes an explicit forward walk shows the
`Agent124.Forward` method at width 8 from time 100 cannot exclude them.

## 2. Results by label

### LEAN-VERIFIED

Module `lean/P196/Sprint/Agent01/` (builds against the repo lakefile; Lean 4.19.0, core only;
`decide +kernel`, no `native_decide`, no `sorry`, no axioms beyond the allowed three).

* `Sprint.Agent01.forward_cannot_exclude` (ForwardWalk.lean) — generic: if a Boolean-checked
  list of inner carries walks from `wordPrefix q100 k` to a full-width digit word beginning with
  `pre`, then every code set `t` with `t.All (fun c _ => fwdOK t k c = true)` and
  `Mem t (wordPrefix q100 k)` contains a word of `initialWordsL k pre`.
  Axioms: `[propext, Classical.choice, Quot.sound]`.
* `Sprint.Agent01.forward_obstruction8` (W8Final.lean) — instantiated at width 8 for the 3,145
  four-digit prefixes in `obstructed8` (`obstructed8_length : obstructed8.length = 3145`,
  `obstructed8_nodup`). Meaning: no forward-closed width-8 set built from time 100 can exclude
  any of these prefixes (statement about the abstraction only; it says nothing about whether
  196 has such palindromes). The 3,145 = 3,134 prefixes with `noOverflowPre` + 11 lead-one.
  Axioms printed by `#print axioms`: `forward_obstruction8` [propext, Classical.choice,
  Quot.sound]; `blocks8_ok` [propext]; `obstructed8_nodup` [propext]; `obstructed8_length`
  none; each block check `b8_###_ok` none.
* `Sprint.Agent01.start8_eq : wordPrefix q100 8 = [8,8,13,9,14,14,14,3]` — no axioms.

Build cost (measured on this sandbox: x86_64, 2 cores, 8 GB): see §3 table.

### COMPUTED

All numbers below are exact (no sampling, no node caps). Programs in `sprint/agent-01/`.

**Forward step = converse of the Lean inverse.** `check_ref.py`: for every source word at k=3
(6,498 sources × 6,859 targets) and 3,000 random words at k=4,5,
`s ∈ prefixPredecessors p ⇔ p ∈ {forwardPrefix s 0, forwardPrefix s 1}` — 0 mismatches; along
196's real orbit (t < 400, k = 3..10, 3,140 transitions) the true next projection is always one
of the two successors.

**Forward closure F_k from orbit(196,100), core C_k, and prefix hits.**
Admissible = 18·19^(k-1) words with q_0 > 0. "Hit" = some word of F_k with all entries ≤ 9
begins with the prefix (the possible last predecessors of a non-overflow palindrome).

| k | \|F_k\| | \|F_k\|/admissible | \|C_k\| | F_k = C_k | single SCC | digit words in F_k | 4-digit prefixes hit | first excluded at k (noOverflowPre) | cumulative | batch (brief) |
|---|---|---|---|---|---|---|---|---|---|---|
| 3 | 4,194 | 0.64543 | 4,194 | yes | yes | 620 / 900 | – (3-digit: 620 hit) | – | – | – |
| 4 | 47,980 | 0.38862 | 47,980 | yes | yes | 3,940 | 3,940 | 5,045 | 5,045 | 5,045 |
| 5 | 497,471 | 0.21207 | 497,471 | yes | yes | 23,360 | 3,327 | 612 | 5,657 | 612 |
| 6 | 4,985,132 | 0.11185 | 4,985,132 | yes | yes | 137,214 | 3,193 | 134 | 5,791 | 134 |
| 7 | 48,820,141 | 0.05765 | 48,820,141 | yes | yes | 785,927 | 3,161 | 32 | 5,823 | 32 |
| 8 | 470,163,112 | 0.02922 | 470,163,112 | yes | yes | 4,452,206 | 3,145 | 16 | 5,839 | 16 |
| 9 | 4,466,505,279 | 0.01461 | not computed | F_9 ⊆ C_9 (see below) | – | 24,965,162 | 3,138 | 7 | 5,846 | 6 |

* k=3 reproduces `Agent124ForwardInvariant` exactly: my F_3 equals the Lean `fset` key set
  (4,194 keys incl. the 15 internal tree nodes), and 280 three-digit words are not hit, 277 of
  them with `noOverflowPre` = the Lean list of 277.
* Cross-check against Lean-verified lists: all 1,267 width-4 and 463 width-5 entries of
  `Agent124FourDigit` are outside C_4 / C_5, and my long-regime peel depth is ≤ their rank
  bound + 1 for every entry.
* Peel depth (longest backward path to a non-core word, long regime) = 9, 20, 48, 55, 62 at
  k = 3..7. Any width-k state with a longer actual history is in C_k.
* Later start times: 196's projections at t = 1,000 / 10^4 / 10^5 / 3·10^5 lie in F_k and in
  the backward-reach of w100 for k = 3..8, so F_k(t) = F_k(100) = C_k (k=8 single-SCC check:
  `layer 8 … fs`, 54 Gauss–Seidel sweeps, 1,490 s, `results/L8scc.log`). At k=9 they lie
  in F_9; at k=9 the forward closure from t=1,000 has exactly the same size (4,466,505,279) and
  contains w100, hence F_9(1000) = F_9(100) and w100 lies on a cycle, so F_9 ⊆ C_9.
* k=9 prefix equivalence: hit by F_9 ⇒ hit by C_9 (F_9 ⊆ C_9). For the 7 prefixes first
  excluded at k=9 (3537, 3899, 3984, 4307, 5838, 6311, 9123) `backcore` computes the backward
  closure of their initial words inside π⁻¹(C_8): 27 / 592 / 83 / 109 / 366 / 100 / 556 nodes,
  no cycle. So forward and backward-core classifications coincide at k=9 as well.
* Width-8 newly excluded (16): 2342 3749 3958 3986 4258 4347 4673 5967 6676 7383 7386 7699 7700
  9137 9149 9523.
* **Discrepancy to check:** at k=9 I get 7 newly excluded prefixes, the batch brief reports
  6@k9 (cumulative through k=9: mine 5,846, batch 5,845). All 7 are cycle-free at width 9.
  Full long-regime backward closures (`fullback 9 60000000 …`, hash set, no cap reached):

  | prefix | \|B_9(P)\| | longest long-regime backward path to an initial word |
  |---|---|---|
  | 3537 | 6,240,696 | 18 |
  | 3899 | 17,381,686 | 15 |
  | 3984 | 8,315,112 | 17 |
  | 4307 | 1,112,733 | 16 |
  | 5838 | 2,082,586 | 26 |
  | 6311 | 3,100,147 | 18 |
  | 9123 | 3,231,156 | 24 |

  All are below 30M nodes, so the 30M node cap alone does not explain the difference (unless
  the batch counts nodes differently, e.g. including short words or across widths). I cannot
  resolve it without the batch lists: whoever holds them should diff against these 7.
* No prefix is "undetermined" at k ≤ 9: 3,127 noOverflowPre prefixes (+11 lead-one) are hit
  at every width 4..9, i.e. have a cycle at width 9 (C_9 ⊇ F_9).
* Lead-one prefixes (27, `noOverflowPre` false): 16 are not hit by digit words at k ≤ 5
  (1000 1001 1002 1010 1011 1012 1020 1021 1022 1110 1120 1121 1200 1201 1202 at k=4, 1212 at
  k=5); 11 are hit at every k ≤ 9 (1100 1101 1102 1111 1112 1122 1210 1211 1220 1221 1222).
  Caveat for agent 7: lead-one prefixes also have overflow-type last predecessors
  (q_0 = 11, entries in {0,11}); 3 of the 64 such width-7 words lie in C_7, so the overflow case
  is not excluded wholesale.
* Forward walks (BFS from w100, shortest): width 7: 3,161 walks, max length 89; width 8: 3,145
  walks, 186,947 steps in total, max 97, BFS depth 132. Examples at width 8: 1337 needs 53
  abstract steps, 4456 needs 34. Every walk re-checked by the independent Python reference
  (`verify_walks.py`: 0 failures).

### Independent cross-check (REPORTED by a separate run on the Mac Studio, not reproduced here)

A separate agent (`~/p196-forward-check` on the Studio, own code `rinf.cpp` / `glob.cpp`, full
uncapped k=7 graph) reported: state space 846,836,325 nodes (= my 846,825,858 long words + the
10,467 admissible short words of widths 1–6); exactly one nontrivial SCC, of 48,820,141 nodes,
equal to its infinite-rank set (= my C_7 = F_7); R(P,7) = whole space for all 3,134 open
four-digit and 14 open three-digit prefixes; 196's orbit in that set at 199,993 of 200,001
steps, first at t = 8 (the first 7-digit iterate, 1067869), and two random control orbits
likewise (199,997 and 200,000 steps). Its 20M-node-capped per-prefix runs hit the cap for every
open prefix, which the single-SCC structure explains. Every overlapping number agrees with §2.

### CONJECTURE

* F_k = C_k and C_k strongly connected for every k ≥ 3 (verified k = 3..8 for both). If
  true, the forward abstraction (from any time ≥ 100) is equivalent to the backward
  acyclicity test at every width, and only enriched states (assignment 3) can do better.
* The number of hit four-digit prefixes converges to a positive limit (3,940 → 3,327 → 3,193 →
  3,161 → 3,145 → 3,138; increments 613, 134, 32, 16, 7). If the limit is > 0, the k-column
  prefix method (forward or backward) can never finish the four-digit level.

### IDEA

* Layered certificates: for the 7 width-9 exclusions, the backward closure *inside*
  π⁻¹(C_8) has ≤ 592 nodes while the full closure is much larger; nodes outside π⁻¹(C_{k-1})
  have finite history bounded by the width-(k-1) peel depth. A certificate format that ranks
  only the in-core part and bounds the rest by the (k-1)-level depth would beat the node cap.
* Since the core is one SCC, enrichments that are themselves functions of the outer block plus
  free carries are unlikely to split it; the added component must carry information the free
  inner carry cannot fake (e.g. a quantity coupled to the middle of the number).

## 3. Reproduce

From the repository root (Linux or macOS, any C compiler, Python 3):

```bash
bash sprint/agent-01/run_all.sh 9        # everything in §2 COMPUTED (k ≤ 9)
cd lean && lake build P196.Sprint.Agent01.W8Final   # Lean endpoints in §2
```

Individual steps and their measured cost on this sandbox (x86_64, 2 cores, 8 GB RAM; memory is
the allocated array size unless "peak RSS" is stated):

| step | command | time | memory |
|---|---|---|---|
| cross-check | `python3 sprint/agent-01/check_ref.py` | 1.3 s | small |
| dense closure k=7 | `./fwdclosure 7 out/F7.t100 8,8,13,9,14,14,14` | 3 s | 224 MB |
| core k=7 | `./peel 7 out/F7.t100.bits out/peel7` | 85 s | ~3 GB |
| SCC k=7 | `./sccchk 7 out/F7.t100.bits <w100> <later states>` | 117 s | 224 MB |
| SCC k=8 | `./layer 8 out/F7.t100.bits out/L8scc fs <w100> <later states>` | 1,490 s | ~0.35 GB RSS (ps) |
| width 8 forward+core | `./layer 8 out/F7.t100.bits out/L8 fdc <w100> ...` | 54 s + 143 s | ~2.6 GB |
| width 9 forward | `./layer 9 out/L8.bits out/L9 f <w100> ...` | 550 s | ~4.6 GB |
| width 9 from t=1000 | `./layer 9 out/L8.bits out/L9from1000 f <w1000> ...` | 550 s | ~4.6 GB |
| k=9 backward cores | `./backcore 9 out/L8.bits 3537 3899 3984 4307 5838 6311 9123` | 30 s | ~4.5 GB |
| walks k=8 | `./witness 8 out/F7.t100.bits 8,8,13,9,14,14,14,3 out/walks8.tsv` | 65 s | ~1.3 GB |
| Lean data chunk (200 walks) | `lake env lean P196/Sprint/Agent01/W8Data000.lean` | 39 s | peak RSS 1,769 MB |

Lean build of the width-8 obstruction (one file at a time, `python3 sprint/agent-01/measure.py
lake build P196.Sprint.Agent01.<M>`, peak RSS of the build process tree): each `W8Data###`
file holds 8 blocks of 25 walks, one `decide +kernel` per block; measured files took 33–70 s
and 1,636–2,031 MB (W8Data011–015; W8Data000 alone: 39 s, 1,769 MB); `W8Final` 7.9 s, 902 MB.
A first attempt with one kernel check per 200 walks peaked at 5,482 MB per file, and two such
files in parallel were killed for memory — hence the 25-walk blocks. With the entry of
`sprint/agent-01/registry_entry.json` merged into a scratch copy of `lean/registry.json`,
`python3 tools/verify.py --changed origin/main` printed `ALL CHECKS PASSED` (5 endpoints audited);
the registry file itself was restored and is not part of this branch.

Width 10 (not run here): `layer 9 out/L8.bits out/L9 fd ...` writes the dense width-9 bitset
(19^9 bits = 40.3 GB), then `layer 10 out/L9.bits out/L10 f ...` needs 40.3 GB + 2.5 GB rank
index + 2 × 10.6 GB bitsets (|U_10| = 19·|F_9| = 84.9e9 bits) ≈ 64 GB; time not measured
(width 9 took 550 s single-threaded for 4.47e9 words; width 10 has ~10× more). On macOS build
with `cc -O3` (no `-march=native` needed).

Not registered: per the sprint rules I did not edit `lean/registry.json`, so
`tools/verify.py` will report the `P196.Sprint.Agent01.*` files as unregistered until a
maintainer adds `sprint/agent-01/registry_entry.json` to the registry.

## 4. What the next agent should do

1. **Stop spending compute on the plain forward abstraction.** It is provably no stronger than
   the backward test at every width computed, and the reason (one strongly connected core
   reached by every long orbit) suggests it never will be.
2. Assignment 3 (enrich the state) is the only forward route left; the test of any enrichment is
   whether the enriched core is still one SCC containing 196's enriched state. Reuse
   `layer.c`/`peel.c` (they take any successor function; replace `forward`).
3. Width 10 on the Mac: run `layer 10` (≈64 GB, see §3) to settle all four-digit prefixes at
   width 10 exactly (no node cap) and compare with the batch's 7@k10 and "2,091 undetermined".
4. Diff the 7 width-9 exclusions above against the batch list and certify the missing one at
   width 9 (cycle-free; closure sizes and depths in §2).
5. Agent 7 (lead-one): 16 lead-one prefixes have no digit-word last predecessor in the core at
   k ≤ 5; only the overflow-type predecessors remain to be handled for them.
