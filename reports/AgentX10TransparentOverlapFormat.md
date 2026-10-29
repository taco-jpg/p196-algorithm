# Agent X10: transparent decimal overlap in affine-exponent packet certificates

**Status: PAPER PROOF.** The finite-cycle soundness criterion is a paper proof; the explicit positive 13-edge decimal family is independently computed. No base-10 infinite certificate is claimed. This report is deliberately separate from the prior agent-X10 20,000-step separated four-sheet orbit.

## 1. Format: affine-exponent packets with bounded aggregate capacity

Fix a base `b>=2` and a Presburger-definable integer parameter domain `P`. A packet `k` consists of finitely many nonnegative base-`b` digits `d[k,j] in {0,..,b-1}` at exponents `e[k,j](p)=v[k]·p+c[k]+j`, for `p in P`, allowing distinct packets to have *equal absolute exponent*. Define the coefficient at position `h` as `A_p(h)=sum_{k,j:e[k,j](p)=h} d[k,j]`. An **overlap-capacity guard** asserts all exponents nonnegative, `0<=A_p(h)<b`, and a nonzero highest coefficient. Under this guard, `A_p(h)` is the exact ordinary digit of the integer `N_p=sum_h A_p(h)b^h`: no global carry occurs even if packets overlap. This extends the disjoint-position affine packet format.

**Arithmetic edge.** Let `H_p=max{h:A_p(h)>0}`. The ordinary reversal of the canonical digit numeral is `rev_b N_p=sum_{k,j}d[k,j]*b^(H_p-e[k,j](p))`. For each sheet/pair of mirrored sheets, add original and reflected coefficients with the ordinary carry recurrence locally inside that packet to get a target packet list. Since normalization preserves the *weighted integer value*, the sum of all normalized target packets equals `N_p+rev_b N_p` even when packets collide spatially. If the target overlap-capacity guard also holds, this sum is exactly its target canonical decimal word. Thus every such edge is arithmetically exact; it is not a heuristic based on finite sample lengths.

**Finite cycle criterion.** Given templates `T_0,...,T_{s-1}` and parameter update `Phi:P->P`, require for each state: a universal overlap-capacity guard; a universal unequal mirrored-digit witness; and for every edge the symbolic reversal/normalization rule and exact target-packet identity (with `T_s(p)=T_0(Phi(p))`). If `Phi(P) subset P`, induction on macrocycles proves every iterate is nonpalindromic. It is sufficient to check finitely many *affine exponent collision chambers*: all equality and ordering changes occur at affine hyperplanes; on any chamber, the active packet overlap sums and carry equations are finite and fixed. Quantifier elimination for integer linear arithmetic or a complete chamber enumeration can establish all parameter guards. This is a soundness implication, not a claim that the needed decimal return cycle exists. A Lean formalization could reuse the existing base-`b` digit normalization lemma and prove `rev(sum packets)=sum rev(packet)` under the capacity guard, then instantiate the same cycle induction as `lychrel_of_lcycle`; none was attempted or verified here.

## 2. Decimal crossing with two central sheets at fixed offset

Choose the explicit real decimal integer

`N0(q) = 88*10^(2q+4) + 78*10^q + 75` for all integers `q>=11`.

At time zero, its four least-significant-first packet rows are `P0=[5,7]`, `P1=[8,7]`, `P2=[]`, `P3=[8,8]`, at bases `0,q,q+4,2q+4`. Write `D=4`. The reflected partner of sheet `i` is `3-i` and the reversed local exponent is `top - exponent`, where `top` is the offset of the highest nonzero digit inside sheet 3. This reflection maps sheet bases `0 <-> 2q+D` and `q <-> q+D`. Normalize each resulting local row with the ordinary schoolbook base-10 carry recurrence, allowing each packet's local start/end offsets to change.

At each time `t`, the checker derives a *universal* lower bound `Q_t` ensuring: every sheet exponent nonnegative, sheets `(0,1)`, `(0,2)`, `(0,3)`, `(1,3)`, `(2,3)` strictly ordered with a gap, while sheets `(1,2)` may overlap. Each inequality has the form `a*q >= c` with integer `a>0`, so `Q_t` is the maximum of exact ceiling quotients. It then checks central sums over the finite *relative* coordinates of sheets 1 and 2 and asserts `max aggregate<=9`. These central sum checks do not depend on `q` once the external separation holds. The outer sheet pair has an exposed digit asymmetry at each state and cannot be palindromic while external separation holds.

For all `t=0..13`, the largest `Q_t` is **11**. Each source/target packet state has the canonical capacity bound, and the central overlaps start at `t=4`. Hence **for every q>=11**, the entire 13-edge formal packet chain equals the genuine ordinary decimal reverse-add chain, all its 14 states are nonpalindromic, and the packet boundaries are genuinely overlapping in states `t=4..13`. This is a universal `q` theorem by finite symbolic checks plus the exact arithmetic lemma, not mere interpolation of four samples.

## 3. Transparent collision trace and first boundary failure

The reproducible CSV trace is `calculation/new_structures/agent-X10/overlap_capacity_check.txt`. Key time slices:

| t | required q | overlapping nonzero digit sites | maximum central aggregate | sites requiring cross-packet carry |
| --- | ---: | ---: | ---: | ---: |
| 0 | 2 | 0 | 8 | 0 |
| 4 | 5 | 1 | 5 | 0 |
| 7 | 8 | 4 | 9 | 0 |
| 9 | 8 | 4 | 9 | 0 |
| 13 | 11 | 4 | 9 | 0 |
| **14** | **12** | **8** | **14** | **4** |

At state 14, four centre positions reach coefficient sum >=10. This is the first failure of the **transparent overlap capacity** format, not the first proven palindrome and not a discrepancy in the *integer equality* of unnormalized packet sums. One would need a cross-sheet carry-transfer gate to continue the same compact packet interpretation. This is a concrete redirect toward a regenerative centre, where cross-packet carry resets and packet separation gains compensate for incoming collisions.

## 4. Independent arithmetic checks

`overlap_capacity.cpp` includes the independently implemented `four_sheet_fast.cpp` per-packet engine. It verifies each universal affine gap bound, aggregation, nonpalindrome witness and packet transition. A separately implemented grade-school **whole-string decimal** reverse-and-add routine replays q=11,12,100,600 for 13 operations each and compares **every complete decimal string** at states t=0..13: 56 full-word identities, zero mismatches. Separately, `overlap_bigint.py` uses Python's arbitrary-precision native integers with `int(str(n)[::-1])` for an independent 56-state palindrome and arithmetic control, with SHA-256 orbit fingerprints. The deliberate failure control confirms t14 overcapacity (four sites, peak 14); it must not be misreported as an actual integer failure.

Reproduce with `bash calculation/new_structures/agent-X10/overlap_reproduce.sh` (C++17 g++ and Python 3, no extra packages). The script compares the symbolic trace byte-for-byte against the committed trace. No Lean files were modified; the repository-wide Lean verifier was not run due missing Lean toolchain/remote git checkout, so this result is not labeled LEAN-VERIFIED.

## 5. Scope and next constructive target

The format permits overlapping affine sheet supports whose sums fit inside a digit, and makes capacity a *finite-state local criterion*. The example demonstrates ten consecutive real decimal centre-overlap states, but fails the criterion at state 14. A truly infinite decimal certificate would require a finite family of carry-transfer gates or renewal macros that returns to a capacity-safe packet language with parameter update keeping every affine gap guard invariant. Neither such a cycle nor a base-10 Lychrel number is established here.
