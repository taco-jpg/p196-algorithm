# X27: an exact parity-regeneration rule for even-base reverse-and-add

**Status: PAPER PROOF**, all finite arithmetic controls **COMPUTED**. Not a proof of an infinite decimal Lychrel orbit.

## Theorem (fully quantified)

Fix any even integer base `b>=2`. Let `N>0` be a canonical base-`b` integer of length `n>=2` with digits `d_i in {0,...,b-1}` least-significant first and `d_(n-1)!=0`. Define the palindromic pair-coefficient word `P_i=d_i+d_(n-1-i)` for `0<=i<n`. Suppose **all** `P_i` are even. Let `m=ceil(n/2)` and `j = min { 0<=i<m : P_i>=b }`, if this set is nonempty. Write `M=N+rev_b(N)` and let `P'` denote the pairword of the canonical digits of `M`.

1. If there is no such `j`, then `M` **is a palindrome**, with the base-`b` digit word exactly `P`.
2. If `j=0`, then `P'_0` is odd.
3. If `j>0`, then `P'_(j-1)` is odd.

In particular, **two consecutive states with all-even pairwords cannot occur in any palindrome-free reverse-and-add orbit in an even base.** This is a positive one-step *parity regeneration* mechanism: a large even pair coefficient generates an odd pair witness, moving one position outward when the first such coefficient is not at the edge.

## Proof

Normalize the formal sum `sum_i P_i*b^i` with one-digit carries `c_0=0`, `c_(i+1)=floor((P_i+c_i)/b)`, `e_i=P_i+c_i-b*c_(i+1)`. Since `P_i<=2b-2` and `c_i in {0,1}`, and since both `b` and every `P_i` are even, no coefficient equals `b-1`. Therefore **for every** index `i` and either incoming carry, `c_(i+1)=H_i`, where `H_i=1` if `P_i>=b`, else `0`. This resets the carry at every column.

If no `H_i=1` occurs in the first `m` positions, reflection `P_i=P_(n-1-i)` forces **all** `H_i=0`. Thus every carry is zero and `e_i=P_i`, and because `P` is palindromic, so is the output digit word. Since `P_0=d_0+d_(n-1)>=1`, its leading digit is nonzero; the canonical digit length is `n`, as claimed.

If `j=0`, then `H_0=1` and the final overflow `c_n=H_(n-1)=H_0=1`. Hence `M` has length `n+1`; its lowest digit is `e_0=P_0-b`, which is even, while the new highest digit is 1. Their sum `P'_0=e_0+1` is odd.

If `j>0`, then `H_0=0`, so `c_n=0` and output length stays `n`. Let `i=j-1`. The exact formula for the pairword of the next output is `P'_i = e_i+e_(n-1-i)`; reducing modulo 2, the two copies of the palindromic source coefficient cancel, as do the multiples of the even base, giving `P'_i = c_i+c_(n-1-i) (mod 2)`. Because `j` is the first high coefficient, `c_i=0`: if `j=1`, this is `c_0=0`; otherwise `c_i=H_(j-2)=0`. The opposite carry is `c_(n-j)=H_(n-j-1)=H_j=1` by source-word reflection. The chosen `i=j-1` is strictly less than `floor(n/2)` for every `j<m`, so it is a legal off-centre pair. Consequently `P'_i` is odd, proving (3).

The dichotomy is exhaustive. If a state with all-even pairword is itself nonpalindromic and its successor is also nonpalindromic, case (1) cannot happen; cases (2)-(3) force a parity witness in the successor. The predecessor's own nonpalindromicity must be proved separately. In particular, an all-even pairword containing a high coefficient does **not** by itself imply the input is nonpalindromic (e.g. decimal `77`), and a valid certificate checker must not silently assume that.

## New regenerative template-format theorem (conditional soundness)

Call a concrete digit template *A-labelled* if every realization has at least one odd pair coefficient. Call a concrete digit template *B-labelled* if every realization (i) has a specified mismatch of mirrored **digits** (so is nonpalindromic), (ii) has every pair coefficient even, and (iii) contains at least one high pair coefficient `P_j>=b`. A finite phase-indexed set of templates, with parameter domains (e.g. arbitrary long bands) closed under their exact reverse-add digit rewrite, is *regenerative* when each phase is A or B, and all B successors fall into A (automatically by the theorem; an edge checker still verifies the resulting template identity). A finite closed regenerative graph supplies a nonpalindromic orbit for every admitted seed, by ordinary induction. This replaces a permanently live parity witness with two types of safe witnesses and a forced one-step recharge at all B phases. It is **more expressive than requiring all phase pairwords to have an odd coefficient**, because B phases can be admitted without misclassifying them as palindromes.

A full decimal closed graph is **not** provided here, so this is a new **soundness format and arithmetic regeneration lemma**, not a claimed decimal certificate. The next positive search should try two-step A→B→A renormalization on the known p8/m20 and p12/m9 decimal exteriors with an *explicit anti-palindrome digit witness* in B phases, rather than enforcing parity across every centre phase.

## Numerical controls, with exact scopes

Run `python3 calculation/new_structures/agent-X27/regenerate.py`. It examines every integer from base `b` through `b^5-1` (all canonical 2..5-digit integers) for `b=2,4,6,8,10`, classifying the cases by whether the source pairword has any odd coefficient, or has no high coefficient and a palindromic successor, or has a high coefficient and exactly the predicted next odd position. Counts:

| base | odd input pairword | all-even, no high, next palindrome | all-even, high, regenerated odd | total |
|---:|---:|---:|---:|---:|
| 2 | 21 | 0 | 9 | 30 |
| 4 | 750 | 30 | 240 | 1,020 |
| 6 | 5,775 | 240 | 1,755 | 7,770 |
| 8 | 24,444 | 1,020 | 7,296 | 32,760 |
| 10 | 74,745 | 3,120 | 22,125 | 99,990 |

It additionally tests 16,000 seeded random canonical 2..199-digit inputs, in bases 2,4,6,8,10,12,16,32; no counterexample. These enumerations are controls, not the proof.

Run `c++ -O3 -std=c++17 calculation/new_structures/agent-X27/outage196.cpp -o /tmp/x27outage && /tmp/x27outage 100000`. This standalone literal-digit decimal engine lists the **three** all-even-pairword phases of actual seed 196 in the first 100,000 steps: `(t,n,j,odd-index-next)=(8,7,0,0), (13,9,3,2), (19,11,1,0)`; each successor is nonpalindromic with the advertised new odd coefficient. There are no other all-even phases in the scanned 100,001 states. This is numerical observation, not a proof of 196's infinite trajectory.

## Lean 4.19 proof sketch (not compiled, not LEAN-VERIFIED)

With the existing `Lychrel`/`norm` word definition and a lemma `base_even : b % 2 = 0`, prove `even_pair_carry_reset` by case-splitting `P_i < b`/`P_i >= b` and bounding `P_i` in `[0,2*b-2]`. Then prove `carry_eq_high` for each index by unfolding `norm`. Split the least-high position `j` into none/zero/successor, use pairword reflection to show `H_(n-j-1)=H_j`, and invoke the length formula `n' = n + c_n`. For `j>0`, apply `Nat.ModEq` modulo 2 to `e_i+e_(n-1-i)` and simplify both multiples of even `b` plus doubled `P_i`. Finally derive the A/B regenerative graph theorem by induction on time, reusing the existing template step-soundness endpoints. There is no Lean file in this commit and no implicit kernel verification claim.
