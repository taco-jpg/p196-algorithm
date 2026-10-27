# Agent 115 — Central windows of five through eight coefficients

Task: `T1.central-window5-8-safety`, coordination issue #289.
Parent: [PR362](https://github.com/taco-jpg/p196-algorithm/pull/362),
commit `516160a2257c7b108b74e89ec3b6020f17865e0a`.

## Result 和 scope

**PAPER PROOF + COMPUTED:** neither the central 5/6-coefficient abstraction
nor the central 7/8-coefficient abstraction admits a nonempty universally safe
invariant for ordinary decimal reverse-add. Safety means that EVERY compatible
exterior completion has a nonpalindromic next output; closure quantifies over
EVERY compatible one-step transition. This extends the central 3/4 result in
PR362 和 the single-middle result in [REPORT216](REPORT_216.md), section4.

| Radius R | Odd/even window | States | Exact labelled edges | Initial safe states | Maximum escape rank |
|---:|---|---:|---:|---:|---:|
| 0, regression | 1/2 | 29 | 188 | 13 | 2 |
| 1, regression | 3/4 | 551 | 3,662 | 397 | 4 |
| 2, new | 5/6 | 10,469 | 69,578 | 8,959 | 7 |
| 3, new | 7/8 | 198,911 | 1,321,982 | 183,889 | 9 |

All four greatest universally closed safe subsets are empty. The radius2/3
closure computations were independently implemented. The arbitrary-radius
transition relation, state count, edge count, 和 safety count below are PAPER
PROOF; emptiness has **not** been established for arbitrary radius.

An abstract path may require different exterior completions at successive
steps. These ranks are **not bounds on an actual integer orbit**. No individual
infinite safe orbit, original neutral-band certificate, or decimal Lychrel
number is excluded. The new radius2/3 results are **not Lean theorems**.

## 1. Arbitrary-radius exact model — PAPER PROOF

For units-first ordinary digits d, set q_i=d_i+d_(L-1-i). A folded word q is
symmetric, has coefficients in 0..18, a positive outer coefficient, 和 an even
middle coefficient when L is odd. Conversely these conditions realize a
canonical positive integer: in each reflected pair choose the high digit
min(q_i,9) 和 the low digit q_i-min(q_i,9); halve an odd middle coefficient.

At radius R, retain a symmetric word w of length 2R+1 at odd width, or 2R+2
at even width. The independent half runs from the outside toward the center.
Write O(a_0,...,a_(R-1),r), with r even, 和 E(a_0,...,a_R). The domain is
all ordinary positive inputs of width at least 2R+1; the even minimum is 2R+2.
There is no upper bound on full width. Reverse-add does not decrease width.

There are 10*19^R odd states 和 19^(R+1) even states, totaling 29*19^R.
Normalize a displayed local word from incoming carry c in {0,1}, using
digit=(coefficient+carry)%10 和 carry=floor((coefficient+carry)/10).
Let D denote the resulting digits, indexed from zero. Every row below gives
the target independent half, for j=0,...,R.

| Source | Overflow g | Normalize | Target | Target half entry j |
|---|---:|---|---|---|
| Odd | 0 | w | Odd | D_j + D_(2R-j) |
| Odd | 1 | (z,w,z), z in 0..18 | Even | D_(j+1) + D_(2R+2-j) |
| Even | 0 | w | Even | D_j + D_(2R+1-j) |
| Even | 1 | w | Odd | D_(j+1) + D_(2R+1-j) |

The odd target middle is twice one digit, so parity is automatic. Necessity
follows because output reflection pairs indices summing to L-1 without
overflow 和 L with overflow. In the minimum odd-width case use virtual
z=c=0: the right virtual zero emits the actual appended carry. Minimum even
width uses c=0. Thus short sources create no omitted transition.

Every displayed choice is realizable. Put v=1+9g 和 u=10c, then use

```
(v,u,w,u,v)                    for odd g=0 or either even case;
(v,u,z,w,z,u,v)                for odd g=1.
```

The outer coefficient v forces the overall overflow; the lower u resets the
entering carry independently. These are valid symmetric folded words, hence
actual positive integers. No incompatible pair of independently guessed
carries is admitted. For odd overflow the mirrored z both affects the carry
entering w 和 supplies the new digit on its high side.

## 2. Closed-form graph counts — PAPER PROOF

For R>=1 the four labelled edge counts are

| Source/overflow | Edges |
|---|---:|
| Odd, g=0 | 20*19^R |
| Odd, g=1 | 2180*19^(R-1) |
| Even, g=0 | 38*19^R |
| Even, g=1 | 20*19^R |
| Total | 3662*19^(R-1) |

Here g is recoverable from source/target parity, so target deduplication
preserves the labelled count. To prove the formulas, compare normalization
from entering carries zero 和 one. Every digit difference is 0, +1, or -9;
the first digit always changes. A reflected pair containing a changed first
digit cannot cancel its change. Thus both no-overflow rows have two distinct
targets per source.

For even overflow the first digit is discarded. If a_0!=9, its outgoing
carry does not change, so there is one target. If a_0=9, the next digit
changes 和 its reflected partner cannot cancel that change: there are two.
This gives 19^(R+1)+19^R=20*19^R edges, also valid at R=0.

For this counting paragraph, D indexes normalization of w itself, without
the two neighboring z coefficients. Fix the effective carry h into w. For
each h=0,1, allowed
(z,c) make the emitted right digit range over all 0..9. If a_0!=9, the two
normalizations of w agree after the first digit, whose values differ by one.
The ten possible first target coefficients therefore form two overlapping
intervals with union size 11; every inner target coefficient agrees.
If a_0=9, the carry difference reaches the next digit, but the even-valued
middle stops it before the opposite outer digit. Hence the inner target
D_1+D_(2R) differs between h=0 和 h=1, giving two disjoint sets of ten targets.
The count is 10*19^(R-1)*(18*11+20)=2180*19^(R-1).
At R=0 the single odd coefficient is even, hence never 9: this row instead
has 110 edges, giving total 20+110+38+20=188.

## 3. Exact universal safety — PAPER PROOF

The existing complete next-palindrome criterion is

```
next is palindromic iff
    every q_i <= 9
    OR (q_0=11 and every q_i belongs to {0,11}).
```

Source: `DecimalDigits.step_palindrome_iff` in
[LychrelDigitSums.lean](../lean/P196/Foundations/LychrelDigitSums.lean), with
the carry proof restated in REPORT216 section2. Consequently a local window
is universally safe exactly when max(w)>=10 和 some entry lies outside {0,11}.
If the first condition fails, surround w by outer coefficient 1 to obtain
a palindrome-producing completion. If the second fails, use outer 11.

The unsafe-state count is

\[
U_R=15\,10^R+3\,2^R-2.
\]

Indeed all coefficients<=9 contribute 5*10^R odd 和 10^(R+1) even states;
all coefficients in {0,11} contribute 2^R odd 和 2^(R+1) even states.
The two all-zero windows were counted twice. Thus the safe count is
29*19^R-U_R. This explains 1,510/15,022 unsafe states at radii2/3.

## 4. Exact universal closure — COMPUTED

Let S_0 be the safe set 和 S_(k+1)={s in S_k: every successor lies in S_k}.
The independently reproduced cardinalities are:

| Round | Radius2 | Radius3 |
|---:|---:|---:|
| 0 | 8,959 | 183,889 |
| 1 | 6,197 | 146,428 |
| 2 | 2,627 | 86,937 |
| 3 | 512 | 28,951 |
| 4 | 50 | 3,791 |
| 5 | 7 | 299 |
| 6 | 1 | 43 |
| 7 | 0 | 5 |
| 8 | 0 | 1 |
| 9 | 0 | 0 |

Both programs compute shortest reverse reachability from all unsafe states.
The distance is the exact removal rank. Every positive-rank state has a
realizable successor of rank one less; the independent program additionally
checks the minimum-successor rank equation at every state. Any universally
closed safe predicate would have to contain these selected successors,
eventually contradicting rank zero. The unique last states are E(18,18,18)
at radius2 和 E(18,18,18,18) at radius3.

## 5. Two fixed escape policies fail — PAPER PROOF + COMPUTED

The finite results do not justify guessing a uniform-radius escape policy.
Two simple proposals already have safe-only cycles in the exact local graph:

```
Always g=1,c=0,z=0, radius2:
E(1,7,14) -> O(8,12,10) -> E(8,11,4) -> O(10,6,8) -> E(1,7,14).

Always g=0,c=0, radius3:
E(3,10,7,13) -> E(7,0,16,7) -> E(14,1,12,15) -> E(8,4,5,12)
 -> E(16,8,11,5) -> E(12,18,2,11) -> E(5,17,6,3)
 -> E(11,14,13,6) -> E(3,10,7,13).
```

Every listed state is safe. The fixed-policy script checks all twelve
transitions 和 ordinary-integer fixtures. These refute those two proposed
policies only: they are neither universally closed subsets under all controls
nor actual integer cycles. A state-dependent arbitrary-radius strategy remains
open; the 7/9 observed ranks do not imply a formula for larger radii.

## 6. Reproduction, guards, 和 repository gate

From the repository root:

```bash
python3 calculation/agent-115/central_window_radius.py --radius 0 1 2 3
python3 -O calculation/agent-115/central_window_radius_independent.py --radii 2 3
python3 calculation/agent-115/central_window_fixed_policies.py
python3 -O calculation/agent-115/central_window_fixed_policies.py
```

The primary `--json` option prints rank histograms, parity-resolved pruning,
maximum-rank states, 和 an abstract escape path with a separate integer
fixture for each edge. It does not write output dumps. The primary checks
every distinct edge; the independent implementation checks every raw control:

| Integer checks | Radius2 | Radius3 |
|---|---:|---:|
| Primary distinct-edge fixtures | 69,578 | 1,321,982 |
| Independent raw-control fixtures | 171,836 | 3,264,884 |
| All valid minimum-width profiles, each implementation | 9,918 | 188,442 |
| Unsafe palindrome completions, each implementation | 1,510 | 15,022 |

The final optimized primary radius3 run took 18.242 seconds / 32.484 MiB peak;
the independent optimized-Python run took 44.187 seconds / 30,128 KiB peak.
All checks use explicit exceptions, remaining active with `python -O`.
The independent CLI supports radii0..3 only. The primary defaults to a
1,100-second total budget, 6,144 MiB address-space limit, 300,000 states,
和 8,000,000 edges; incomplete runs return `UNDECIDED`, exit2. No cap was
reached in any reported complete census.

Nine targeted guard probes passed: astronomical radius with two state caps,
insufficient state/edge caps, zero/negative/overflowing caps, 和 nonfinite time.
A separate micro-time-budget probe returned UNDECIDED. Radius bounds are
checked before exponentiation or allocation; array index widths are guarded.
Normal/optimized fixed-policy controls pass all twelve edges. The final
optimized primary radius2/3 run reproduces every count above, exit0.

The actual `python3 tools/verify.py --changed` gate passed, exit0, on the
combined tree: 5,219 Lean files / 302 projects; 2 modules built 和 kernel-replayed;
8 endpoints audited; `ALL CHECKS PASSED (changed files only, against origin/main)`.
Wall time was 82.692 seconds, peak RSS 784,340 KiB, one Lean thread with the
pinned official Lean/checker4.19.0, 8 GiB address-space 和 20-minute limits.
The two selected modules 和 eight endpoints are unchanged from parent PR362.
No new Lean source is part of this result. That finite-model theorem concerns
radius1 only; its kernel verification does not prove radius2/3 emptiness.
