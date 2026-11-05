# r11a: centres for the outer end of the p8 stack (rec0/rec1, m=20, p=8)

Studio dir `~/p196_run/r11a/`. Two agents worked here: the first wrote cen2.cpp, lemma2.py, stackcheck.py, bigint2.py,
ref2.py and queue.sh and ran most of the jobs. Its network connection dropped. The successor stopped queue.sh, took the
remaining jobs over in queue2.sh/queue3.sh (reordered, plus the stacked-table runs) and wrote this report. Nothing was rerun.
Labels: COMPUTED / PAPER PROOF / UNDECIDED.

Family: P(q,C) = B0 W0^q C rev(W0)^q rev(B0), where C is a legal palindromic coefficient centre (symbols 0..18; odd length has
an even midpoint). Test for period 80K: T^(80K)(P(q,C)) == P(q+K,C), comparing the whole pairword. Every centre is
enumerated in exact integer arithmetic, so there is **no pruning**. Every lane whose top carry leaves the clock g_t is
recomputed by the scalar reference routine. This makes the results exact without a pruning lemma.

## 0. Tool validation (COMPUTED)
- cen2 (SIMD) against the original centre.cpp, rec1 L12 q5: the RESULT and the full HIST are identical (`L12_rec1_cen2.log` vs `orig/L12_rec1_ctrl.log`).
- FORCEDEV build: every 7th lane is forced through the scalar path. rec1 L8 K2, rec1 L7 K3, rec0 L8 K2 give HISTs identical to the normal build (`runs/ctrl_fd_*`).
- Independent Python reference `ref2gen.py` (klib.pairword_step, any table): rec1 L6 q8 K2, rec0 L5 q11 K3, stk1 L6 q2 K1 and stk3 L5 q0 K1 all agree with cen2 on RESULT, maxprefix, argmax and HIST (`runs/ctrl_ref_*`).
- The stk0 table is byte-identical to rec1.tbl (B2 = B1[:11]).

## 1. rec1, |C| = 13..16, period 80, q >= 5 (COMPUTED + PAPER PROOF reduction)
The reduction comes from the earlier report (#476 R03A1 / p8_centre_exhaust): the return holds for some q >= 5 iff it holds at q = 5.

| L | centres | returns | clockdev | guardfail | max prefix / target length |
|---|---|---|---|---|---|
| 13 | 470,458,810 | 0 | 0 | 0 | 145 / 331 |
| 14 | 893,871,739 | 0 | 0 | 0 | 145 / 332 |
| 15 | 8,938,717,390 (9 shards) | 0 | 0 | 0 | 147 / 333 |
| 16 | 16,983,563,041 (18 shards) | 0 | 0 | 0 | 145 / 334 |

L13..16 total 27,286,610,980 centres, 0 returns. With the earlier L4..12 run: **rec1 has no fixed-centre exact 80-step return
for |C| = 4..16 at any q >= 5.** Every centre already fails inside the rooted B W^6 prefix (prefix <= 147 < 159).
Note: queue.sh never started rec1 L16 shard 18/18 ([16040031760, 16983563041)). It was found missing and run in queue3 (0 returns).
rec0 control: L4..14 at q5, 1,440,126,470 centres, 0 returns, max prefix 144. rec0 L15/L16 were **not** run, because rec0 is
outside the requested rec1 range.

## 2. Periods 160, 240
- Thresholds (lemma2.py part A, COMPUTED universal two-inlet shield, both inner carries, H = 80K):
  q0(160) = 8 and q0(240) = 11 for both rec0 and rec1. q0-1 fails at t = 146/218 (rec1) and t = 150/222 (rec0). All q in [q0, 29] pass.
  The W-insertion equivariance is per step (lemma.py (2): 640/640 kernel, PAPER PROOF block factorisation), so for every q >= q0,
  T^(80K)(P(q,C)) = P(q+K,C) iff the same holds at q0. This has the same status as the 80-step reduction.
- Exhaustion at the threshold (COMPUTED):

| rec | K | q0 | L | centres | returns | max prefix |
|---|---|---|---|---|---|---|
| rec1 | 2 | 8 | 4..14 | 1,440,126,470 | 0 | 200 |
| rec1 | 3 | 11 | 4..13 | 546,254,731 | 0 | 257 |
| rec0 | 2 | 8 | 4..12 | 75,795,921 | 0 | 200 |
| rec0 | 3 | 11 | 4..12 | 75,795,921 | 0 | 248 |

  clockdev, lenerr and guardfail are 0 in every run.
- Below the threshold, by direct exhaustion (no reduction needed), L4..10: K=2 for q = 0..7 and K=3 for q = 0..10, rec0 and
  rec1, 3,989,050 centres each, 0 returns. K=1 for q = 0..4, L4..12, rec0 and rec1, 0 returns.
  Consequence: **for K = 1, 2, 3 and every q >= 0, no fixed-centre return in rec0/rec1 with |C| <= 10.** For |C| <= 12
  this holds for K = 1 (rec0 and rec1) and for K = 2, 3 at q >= q0. rec1 also has |C| <= 16 (K=1, q >= 5), |C| <= 14 (K=2, q >= 8)
  and |C| <= 13 (K=3, q >= 11).

## 3. Stack S(s) W20^r C ..., S_t(s) = B2_t W48_t^s B1_t[11:] (HYBRID 7b, #481)
- PAPER PROOF reduction (lemma2.py part B for s = 0..8 and lemma2s.py for s = 9..16, finite symbolic kernel). The cap replacement
  J: B1 -> S(s) commutes with T (640/640). The W20 insertion under the stacked cap also commutes (640/640). The universal shield
  of S(s) W20^r has threshold r0 = 5 / 8 / 11 for H = 80 / 160 / 240, the same as rec1 and independent of s; r0-1 fails at
  t = 74 / 146 / 218. Hence for s <= 16 and r >= r0, the stack returns iff rec1 P(r0,C) returns. stackcheck.py (COMPUTED):
  600 random genuine 80-step runs (s in {0,1,2,3,5}, r = 4..6, |C| = 4..16) gave 0 J-equivariance failures.
  So the rec1 results in sections 1 and 2 carry over to the stack: none for |C| <= 16 (K=1), <= 14 (K=2), <= 13 (K=3).
- Small q, below the shield, direct exhaustion with cen2 on the stacked tables stk1..3 (COMPUTED). s = 1,2,3:
  K=1 for r = 0..5 at L4..12 (75,795,921 centres each), and K=2 for r = 0..8 at L4..10: **0 returns**.
  Together with the reduction: for s = 1..3 the stack has no return with |C| <= 12 (K=1) or <= 10 (K=2) at any r >= 0.
  The prefix histograms of stk1/stk3 equal those of rec1 at the same r (counts identical) with an offset of exactly
  |S|-39 = 48/144. This was checked at L9 for r = 0, 1, 2, 4, so J holds empirically even below the shield.
- Multi-period big-integer replays (bigint2.py, COMPUTED) used the max-prefix centres of rec1 L13..16 (K=1, 3 periods),
  L13/14 K=2 and L13 K=3 (2 periods). Pairwords matched klib at every step, no palindrome appeared, and nothing returned
  (prefixes per period shrink, e.g. 147 -> 129 -> 111).

## UNDECIDED
- |C| >= 17 (K=1), >= 15 (K=2), >= 14 (K=3).
- Period >= 320.
- Moving centres (C' != C).
- Stack s >= 17. The kernel was checked only for s <= 16. Larger s needs the #481 block identities (PAPER PROOF, not rechecked).
- Stack with s >= 4 at r < 5, and K=3 for the stack below r0.
- rec0 L15/16.
No exact return was found anywhere, so the requested multi-period replay of a return did not apply.

## Files
cen2.cpp, ref2.py, ref2gen.py, lemma2.py(+.log), lemma2s.py(+.log), stackcheck.py(+.log), mkstack.py, bigint2.py,
bigint_r11a*.log, aggregate.py(+.log), queue*.sh, queue.log, runs/ (one RESULT+HIST per job).
