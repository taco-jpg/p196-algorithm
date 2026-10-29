# N25: symmetric zero-sector splicing and a 20,000-step decimal family

Label: COMPUTED.

Let `R(n)=n+rev10(n)` and let concatenation be denoted by juxtaposition. For integers `u,v>=40001`, define the decimal integer

`N(u,v) = 1789 0^u 3141 0^v 5926 0^u 5358`.

**Result (finite-time only).** Each `N(u,v)` has a nonpalindromic decimal representation at all times `t=0,...,20000`. At every time, the digit word has *three* reflection-paired protected zero sectors. The two exterior sectors have width at least `u-2t+G_t`, and the central sector at least `v-2t+G_t`, where `G_t` is the number of length-increasing steps before time `t`. Consequently its pair-sum word contains three zero sectors, with nonzero dynamics confined to the intervening arithmetic joints. This is a *two-parameter infinite family of finite-horizon nonpalindromic orbits*, NOT a number proved Lychrel, NOT an infinite-time decimal certificate.

## Local carry firewall lemma (paper proof)

Use least-significant-digit-first coordinates. Suppose an `n`-digit canonical decimal number has all zero digits on interval `I=[a,b]` and its reflection `I*=[n-1-b,n-1-a]` (central self-mirror intervals allowed). Define its pair-sum word `P_i=d_i+d_{n-1-i}`, and its normalized result digits `e_i=(P_i+c_i) mod 10`, `c_{i+1}=floor((P_i+c_i)/10)`, `c_0=0`. Since `P_i=0` on both intervals, **every carry entering either zero sector is killed by its first digit**: for all `i>a`, `e_i=0` within `I`, and likewise for `I*`. Set `gamma=c_n`, the overflow bit. The new digit length is `n+gamma`. Pairing the new digits around this updated centre, the intervals

`I'=[a+1,b-1+gamma]` and `I'*=[(n+gamma)-1-(b-1+gamma),(n+gamma)-1-(a+1)]`

are again all zero. (Intersect the normalized zero interval `[a+1,b]` with the reflection of the normalized mirror interval `[n-b,n-1-a]` about `n+gamma-1`; the intersection is exactly the displayed `I'`.) No digit/carry inside an interior zero sector can cross it. If an interval has initial length `g`, it retains at least `g-2t+G_t` zero positions after `t` steps, with low-coordinate left endpoint `a+t`, provided the right endpoint stays >= the left endpoint. The statement does not depend on exterior arithmetic or on the other intervals.

## Two-parameter splicing lemma (paper proof)

Start with four 4-digit packets separated by reflection-symmetric zero sectors `U 0^u V 0^v W 0^u X`. The packets `U,V,W,X` need not themselves be symmetric. Inflate the reflected exterior gaps by the same arbitrary `h>=0`, and the central gap by an independent arbitrary `k>=0`. At any time before the protected intervals become empty, **inflating commutes with reverse-and-add** after the insertion coordinates are updated by `+t` at the lower-position end, and by the current overflow `G_t` at the higher-position end. The carry entering any sector is absorbed at its first zero, so inserting zeros strictly inside the protected portion changes no carry arriving at any later nonzero packet. Reflection-paired insertions preserve pair alignment, and `gamma` is unchanged. Thus induction gives identical packet sequences, identical overflows and identical palindrome status for both gap settings until the first protected gap closes. The same argument applies independently to any finite collection of mirror-paired vacuum sectors. A palindrome cannot be created or destroyed by inserting reflection-paired zeros inside such sectors, since all inserted digits equal their mirrored partners and every exterior mirrored pair is unchanged.

For this result, the base trajectory uses `u=v=40001`, so the crude guard `40001-2t >= 1` lasts through `t=20000` regardless of the overflow history. Its nonpalindromicity then lifts to **all** `u,v>=40001` by the splicing lemma, with independent inflation of `u` and `v`.

## Independent numerical evidence

- Canonical seed: 120,019 digits; ordinary-digit recurrence and *independent base-10^9 multi-limb integer arithmetic* agree on every full-number FNV-1a 64-bit trace row for `t=0,...,20000` (20,001 comparisons, also final full decimal bytes compared). Both separately checked three protected sectors and nonpalindromicity at every step.
- At `t=20000`: `G_t=8227`, 128,246 digits, at least 8,228 guaranteed zero digits per sector. Final SHA-256: `59464c5366b9800d8b557cd0434b3ad245d10e5b72d842b7f35aa463669e1fba`.
- Independent Python built-in big integers: 1,000-step ordinary integer splicing comparison for `u=2101,v=2107` against `u'=2114,v'=2128`, plus 100 seeded random packet/gap/inflation cases at 11 times each; all overflow, full digit-word, and palindrome statuses matched after removing the extra protected zeros.
- Arithmetic positive controls: `R(196)=887`, `R(89)=187`, `R(1001)=2002`.

Reproduction from repository root:

`python3 calculation/new_structures/agent-N25/run.py --steps 20000 --gap 40001`

`python3 calculation/new_structures/agent-N25/splice.py`

Both tests use only Python 3 and `g++ -std=c++17`, with no external packages; 20,000-step runs generate temporary trace/final files and compare both arithmetic engines byte-for-byte, and output concise checkpoints. Checkpoint data in `checkpoints.json`. No GitHub network access or Lean is required for reproduction.

## What fails and what to try next

The vacuum guard **contracts** by `2-gamma` positions per step. This finite-horizon family does not imply a decimal Lychrel number; it says nothing about times after the gap closes. **Search redirection:** seek a *regenerating firewall* whose carry-carrying joint deposits at least `2q-sum(gamma)` fresh symmetry-paired zeros into each active sector over a `q`-step macrocycle, or a joint-to-joint transfer automaton that moves/replenishes protected sectors rather than consuming a finite initial buffer. Such a replenishment contract plus a nonpalindromicity boundary invariant would make the splicing format potentially infinite-time sound.
