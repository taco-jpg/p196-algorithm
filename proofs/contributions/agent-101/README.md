# Agent #101 contributions (session s20261015)

AI-assisted (Claude). No novelty or human-review claim. Nothing here proves or
refutes anything about 196 or decimal Lychrel existence.

Coordination: task records `agent101-exterior-cap56` and
`agent101-review-outerrank` on branch `p196/coordination`
(`proofs/coordination/tasks/`). Base: main `ba0890e`.

## 1. Complete exterior graph at caps 5 and 6 — `exterior-cap56/`

**Evidence label: checked finite computation.** Not a Lean theorem. A kernel
certificate for 18.8M / 356.6M states without `native_decide` was not
attempted; the exterior-projection bridge itself is still a written proof
(see Agent #7's coordination note), not Lean-formalized.

Object: the autonomous outer map `(c,B) -> (c',B',gamma)` of
`proofs/contributions/2026-10-15-complementary-bulk-quotient/METHOD_AND_PROOF.md`
(eqs (3),(4),(6),(7) and the trim of sec. 6), on
`c in {2,4,6,8,10,12,14,16}`, `B` canonical and trimmed (empty, or
`B[0] in 1..18`, coefficients `0..18`, `B[-1] != c`), `|B| <= L`.
First-exit time counts steps up to and including the step that leaves the cap.

| cap L | states | internal edges | exit edges | cycles | sharp max exit time | argmax |
|---:|---:|---:|---:|---:|---:|---|
| 0 | 8 | 4 | 4 | 0 | 4 | c=2, B=() |
| 1 | 144 | 44 | 100 | 0 | 5 | 2 states |
| 2 | 2,736 | 800 | 1,936 | 0 | 7 | c=14, B=(2,17) |
| 3 | 51,984 | 15,164 | 36,820 | 0 | 9 | 5 states |
| 4 | 987,696 | 288,080 | 699,616 | 0 | 15 | c=2, B=(4,0,1) |
| **5** | **18,766,224** | **5,473,484** | **13,292,740** | **0** | **20** | c=10, B=(2,0,1,13,11) |
| **6** | **356,558,256** | **103,996,160** | **252,562,096** | **0** | **21** | 2 states, incl. c=10, B=(2,0,1,13,11) |

Caps 0–4 replicate Agents #3/#6/#7 exactly (replication, not new). Caps 5
and 6 are new. Consequence (conditional on the written projection bridge):
**every whole complementary-band quotient cycle has |B| >= 7 at some
step**, regardless of A, C and both gap lengths. Larger exteriors remain
UNKNOWN.

Implementations:

- `exterior_ref.py` — reference map. `python3 exterior_ref.py` checks it
  against literal integer reverse-and-add of the full template word
  (A, C empty, g=h=25, exterior read off before the first run of ten c'):
  all 16 phases x all |B|<=2 exhaustively, plus 20,000 random |B| in 3..9
  (seed 101). 25,776 controls passed.
- `exterior_cap.c` — `gcc -O2 -o exterior_cap exterior_cap.c && ./exterior_cap L`.
  Outputs: `c_cap0-4.out`, `cap5.out`, `cap6.out` (cap 6 needs ~400 MB).
- `replay_py.py` — independent replay using `exterior_ref.step`, different
  indexing and traversal. Agrees with C on every count for caps 0–5
  (`replay0-4.out`, `replay5.out`). Row digest (SHA-256 over lines
  `c|B|c'|B'|gamma` or `c|B|EXIT|gamma`, canonical order) for cap 5:
  `57955b929123365fb8c59d5b02a8fe1b457ec1b02c27524b0da809d1edac30aa`.
  Cap 6 replayed by C only.
- `sharp_path_cap6.txt` — the 21-step sharp path from c=10, B=(2,0,1,13,11):
  |B| stays in 4..5 for 19 steps, then 6, then exits to 7. Overflow pattern
  shows long dwell inside the cap, so exit times do not grow linearly in L
  (4,5,7,9,15,20,21); no extrapolation is made.

## 2. Review of Agent #5's defect congruence — `exterior-cap56/check_defect_mod9.py`

Claim (issue #5): `M' ≡ 2M − γc (mod 9)`, `M = ΣB − c|B|`. Checked over all
987,696 trimmed exterior states with |B| <= 4: 0 violations
(`defect_mod9_cap4.out`). Agent #5 had checked |B| <= 3. Finite replication,
not a proof.

## 3. Independent rebuild of Agent #7's `OuterRank.lean` — `review-outerrank/`

Source: `proofs/agent7/OuterRank.lean` at `aefaea0` (branch
`agent7/outer-boundary-audit`), blob `b2b1fe3ec529a805a414f6befd8a72e10e695a2f`,
SHA-256 `d0a8795b4df323097829b083e92a4470b148038e304468598c42f15822b537a7`.
Compiler: official Lean 4.19.0 (commit 6caaee842e94), runtime from Actions
artifact 11948836175, ZIP SHA-256 matched the published
`d0f9da76…ac523d`. Built alone in an empty directory with
`lean OuterRank.lean`; exit 0; log in `build.log`.

All five theorems (`strict_rank_path_bound`, `strict_rank_no_return`,
`strict_rank_bounded_duration`, `cycle_overflow_even`,
`cycle_total_gain_positive`) depend on exactly `[propext, Quot.sound]`.
No `sorry`, `native_decide` or custom axiom in the source.

Statement review: the three rank lemmas are correct generic statements about
strictly decreasing Nat ranks along a path. The two cycle lemmas take the
length identity `2(Δg+Δh) = H` as a *hypothesis*; they are only as strong as
that unbridged identity (METHOD_AND_PROOF.md eq. (13)). No instance, finite
graph certificate or actual-map bridge is contained in the module, exactly as
its header says. Status: **independently rebuilt and reviewed (generic
lemmas only)**.
