# Agent 3 — T3.p12.theory: all-base odd-center invariants

**PAPER PROOF.** Not Lean-verified. Separate finite arithmetic audit is labeled COMPUTED. This is a theory deliverable under #289 Manager's agent-3 scope split, not an all-k impossibility theorem.

## Source and semantics

For any integer base `b>=2`, write the symmetric nonempty coefficient center as `C=[c_0,...,c_{m-1}]`, with `0<=c_i<=2(b-1)` and `c_i=c_{m-1-i}`. Under the `Agent120.Neutral` mirror, assume the entering center carry `e∈{0,1}` has outgoing carry `1-e`. Normalize to the ordinary digits `d=norm(b,C,e).digits`. The raw next center is

* no overflow (`g=0`): `N=d + reverse(d)` (elementwise);
* overflow (`g=1`): `N=(d ++ [(b-1)e]) + ([(b-1)e] ++ reverse(d))`.

A legal trim removes `v>=0` symmetric outer copies of coefficient `b-1`, retaining a nonempty symmetric `C'`. Every genuine neutral-band center edge is a case of this local rule. Define `A(W)=sum_i(-1)^i W[i]` (index 0 least significant) and `J(W)=A(W)-(b-1)` for odd-length W.

## Theorem 1 (PAPER PROOF, arbitrary base and width)

**If a closed neutral-band cycle includes at least one overflow, every odd-length center in that cycle satisfies**

`A(C) ≡ b-1 (mod b+1)` and `C[(m-1)/2]` is even.

**Proof.** Let `h_i` denote carries in the normalization of C: `h_0=e`, `h_m=1-e`, and `d_i=c_i+h_i-b*h_{i+1}`. As `-b≡1 mod(b+1)`, alternating summation cancels every interior carry:

`A(d)≡ A(C)+e+(-1)^(m-1)(1-e) (mod b+1)`.

If m is even, `A(C)=0` by symmetry, so `A(d)≡2e-1`. For `g=1`, the raw next center is odd-length and

`A(N)=2(A(d)+(b-1)e)≡2((b+1)e-1)≡-2≡b-1 (mod b+1)`.

If m is odd, `A(d)≡A(C)+1`. For `g=0`, the raw next center is odd-length and `A(N)=2A(d)`, giving

`J(N)=A(N)-(b-1) ≡ 2J(C) (mod b+1)`.

For every odd symmetric raw N with v outer `(b-1)` pairs removed, the exact integer identity is

`J(C')=(-1)^v J(N)`.

Thus an even→odd overflow sets `J(C')≡0`; odd→odd nonoverflow preserves `J≡0`. Overflows flip center-length parity, while no-overflow steps preserve it. A closed cycle containing any overflow must contain an even→odd overflow, and every odd center on the cycle lies downstream of one without crossing an odd→even overflow. Hence `J(C)≡0` throughout the odd phases.

The odd-length raw image, whether obtained from even m with g=1 or odd m with g=0, has its unique central coefficient equal to `2*d[floor(m/2)]` (using the appropriate existing central index). Symmetric outer trimming leaves it unchanged, so every odd output center has even central coefficient. All cycle states have predecessors. QED.

## Corollaries for every base (including decimal)

**Corollary 1:** No cycle with an overflow ever has a center of length 1, in **any** base. Indeed if `C=[c]`, the invariant forces `c≡b-1 mod(b+1)` and `0≤c≤2b-2`, hence `c=b-1` uniquely. But a single `(b-1)` coefficient transmits the entering carry unchanged, `norm(b,[b-1],e).exit=e`, contradicting the required outgoing carry `1-e`. For even b there is also an immediate contradiction with central evenness.

**Corollary 2:** For **any** b, if a cycle has center `C=[a,c,a]` at an overflow, it cannot trim exactly one `(b-1)` pair to obtain a center of length 2. Such a trim requires the raw leading coefficient `(a+e) mod b + (b-1)e` to equal b-1. With `0≤a≤2b-2` and the required outgoing carry `1-e`, this forces `a=b-1`. Then `A(C)=2(b-1)-c≡b-1 mod(b+1)` forces `c≡b-1 mod(b+1)`, hence `c=b-1`. But `C=[b-1,b-1,b-1]` preserves the normalization carry, contradicting its required exit `1-e`. (For even b, central parity provides a second contradiction.) QED.

**Corollary 3:** For **any** base, an overflow-containing closed center cycle cannot have every center length ≤3. A length-1 state is excluded; a 2→odd overflow must land at length 3 (rather than 1), and an odd→even overflow from length 3 must land at length 2 if length is bounded by 3, contradicting Corollary 2. Consequently every such certificate visits a center of length ≥4.

All these are independent of period, carry stream, trim schedule, or center width *outside the explicitly excluded small-width corollary*.

## Application to base-10 period 12

For `g=100010001000`, exactly 3 overflows occur per 12 steps. The previously established length identity `|C'|=|C|+g-2v` implies every closed center repetition count k must be even, since `3k=2Σv`. This is a pre-existing parity obstruction and **not new** here.

Theorems above apply to all three documented p12 phase rotations and to any k (including even k≥4). They provide a safe width-free filter, not a proof that such cycles are impossible at arbitrary width. In particular they do not exclude centers with max length ≥11.

The independent bounded-center graph I ran in Python (`agent3_alt11_allk.py`, DFS and Kahn) excludes cycles when every center has length≤9 (1,575,612 invariant-filtered states / 915,425 edges). This is a useful cross-check, but Agent 6 has since supplied the **stronger**, unfiltered all-k computation through center width 10, in [review patch #296](https://github.com/taco-jpg/p196-algorithm/issues/296). Do not attribute a new width record to this paper.

## COMPUTED arithmetic audit

Independent script `agent3_mod11_check.py` enumerates every symmetric C of lengths 1–4 and every `e,g∈{0,1}` in bases 2,4,8,10,11,17,26, including all legal nonempty symmetric trims. It checks the two one-step congruence implications and the central-even identity. All 20,512 local edges checked pass (7 exact base-by-base counts below). These finite checks are **not** the proof of the arbitrary-width result.

```
base=2 checked_edges=56 odd_outputs=28 PASS
base=4 checked_edges=256 odd_outputs=128 PASS
base=8 checked_edges=1040 odd_outputs=520 PASS
base=10 checked_edges=1624 odd_outputs=812 PASS
base=11 checked_edges=1960 odd_outputs=980 PASS
base=17 checked_edges=4672 odd_outputs=2336 PASS
base=26 checked_edges=10904 odd_outputs=5452 PASS
```

Sum: 20,512 local edges. No decimal cycle was found or certified; no Lean compilation or `verify.py` is claimed. AGENTS.md's main-only/PR conflict remains on hold by the Manager; this report and self-contained checker are a review-only proposal, not a merge or PR.