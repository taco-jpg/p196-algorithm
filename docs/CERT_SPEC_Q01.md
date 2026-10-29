# Q01 certificate specification: temporal clock vs spatial growth

**PAPER PROOF**, conditional necessary conditions; **not** an existence proof or a decimal certificate. Independent whole-integer controls: `python3 calculation/new_structures/Q01/cert_spec_check.py`. Scope: fixed, *literally returning* rooted exterior, periodic band, fixed finite centre, and genuine ordinary reverse-and-add edges, uniform over every sufficiently large band count. A phase-twisted/moving-junction/multiband format must be analysed separately.

## 1. Formal parameters and theorem

Write `P_t(q) = B_t ++ W_t^q ++ C_t ++ reverse(W_t)^q ++ reverse(B_t)` for a symmetric **pair-coefficient** word, least significant coefficient first, with `|W_t|=m>0`. The finite blocks `B_t,C_t` are independent of `q`; `C_t` is palindromic. Every `P_t(q)` must be realized as the mirrored digit-sum word of a *canonical positive base-10 integer*. Assume a **sound edge sequence for every q>=q0**: the ordinary reverse-and-add orbit's pairwords follow the templates at every ordinary step, and at some fixed `k>0`, `P_k(q)=P_0(q+g)` for the **same literal** `B_0,W_0,C_0`. Suppose also the complete exterior/clock state has primitive temporal period `p` (returning the state entails returning `t mod p`), and the actual overflow indicators `gamma_t in {0,1}` have sum `S>0` over a full `p`-period.

**Necessary phase-growth theorem.** If the return repeats indefinitely without crossing an invalid source-length guard, then

`k=p*r`, `Gamma=sum_{t<k} gamma_t=r*S=2*m*g`, `g>=1`.

In particular, with `h=gcd(S,2m)`, the complete set of **arithmetically admissible** positive pairs is

`(k,g)=(a*p*2*m/h, a*S/h)` for integers `a>=1`.

A return after `k` steps shifts the **temporal** phase by `k mod p` and the full-band **spatial** phase by `Gamma/2 mod m`; literal closure requires both to vanish. They are distinct modular conditions, not an assertion that the *spatial displacement* is divisible by the *temporal clock period*.

For the **merged lattice** `P_t(l)=B_t ++ prefix(W_t^infinity,l) ++ reverse(B_t)`, with `l=m*q+rho` and identical initial/terminal `rho`, replace `2m` throughout by `m`: `Gamma=m*g`, `(k,g)=(a*p*m/gcd(S,m), a*S/gcd(S,m))`. The merged theorem presupposes every phase's band symmetry and canonical realisability. These formulas are *necessary*, not sufficient; they do not solve the carry/centre repair.

**Proof.** Each positive reverse-and-add step increases the integer, and its digit length gains exactly its genuine overflow bit (0 or 1). Every pairword has the length of the represented canonical integer. The initial/return pairword lengths differ by exactly `2mg` in the paired format (respectively `mg` in the merged format). Thus `Gamma=2mg` (respectively `mg`). The primitive exterior phase condition forces `p|k`, yielding `Gamma=(k/p)S`. Solving the integer equation `rS=2mg` by gcd gives the displayed positive solutions. For a indefinitely closed family, `g<0` would eventually cross its minimum legal source length. If `g=0`, the same complete pairword at each macro return would force equal *next* integers, because `N_{t+1}=value_{10}(P_t)`, contradicting strict growth. Hence `g>=1`. The merged case is identical by length accounting. QED.

**Warning on an attractive false strengthening.** “Total exterior shift must be a multiple of the clock period `p`” is **false** if shift means digit positions or band cells. The **Lean-verified base-9** merged lattice returns in `k=p=10` with spatial shift `Gamma=4` (not divisible by 10). The **base-50** four-edge paired neutral band returns with `Gamma=2` and a one-cell band gain, neither a multiple of `p=4`. Require `p|k` and the applicable `m|Gamma` / `2m|Gamma` instead.

## 2. Additional all-width coefficient-mass filter (base 10)

For the fixed literal paired template above, let `A=sum(W_0)`, `E=sum(B_0)`, `H=sum(C_0)`, all taken modulo 9. The same exact return for **every q>=q0** implies the two independent congruences

`2*(2^k-1)*A == 0 (mod 9)`  and
`2*g*A == (2^k-1)*(2*E+H) (mod 9)`.

**Proof.** The pairword `P_t` represents `N_t+reverse(N_t)=N_{t+1}`, so `value_{10}(P_{q+g}) == 2^k value_{10}(P_q) (mod 9)`, since any reverse-and-add step doubles its value modulo 9. The coefficient sum of `P_q` is `2E+2qA+H`. Comparing two consecutive admissible `q` isolates the coefficient of `q` and gives the first congruence; its constant part gives the second. This uses real orbit equality and a single fixed finite centre; it is not an assumed carry clock. QED.

For the published p12/m9 row, `A=60==6 (mod 9)`. The length-only minimum would be `k=72, g=1`, but `2^72==1 (mod 9)` makes the fixed-centre charge demand `2*g*60==0 (mod9)`, i.e. `3|g`. Therefore **the first length+mass-admissible fixed-centre return has `k=216, g=3`**, not 72 or 144. This is the already published all-width obstruction `AgentY18P12CentreCharge216`; it is **attributed**, not claimed new. Changing centre charge can bypass the fixed-centre version but then the centre state has not returned.

## 3. Arithmetic filter table (not realizability evidence)

| Route | Template | (p,S,m) | Length-only minimal (k,g) | Extra fixed-cap condition |
|---|---|---|---|---|
| Lean base 9 | merged | (10,4,4) | (10,1), shift 4 | actual certified |
| Computed base 50 | mirrored neutral, m=1 | (4,2,1) | (4,1), shift 2 | actual complete four-edge cycle |
| Decimal p8/m20 | mirrored | (8,4,20) | (80,1), then (160,2), ... | no periodic centre known |
| Decimal p8/m48 | mirrored | (8,4,48) | (192,1), then (384,2), ... | no periodic centre known |
| Decimal p12/m9 | mirrored | (12,3,9) | (72,1), (144,2), (216,3), ... | fixed-centre charge excludes 72 and 144; 216 first admissible |
| Decimal p8/m20 | merged lattice | (8,4,20) | (40,1) | no rooted self-mirror centre-free cycle |
| Decimal p8/m48 | merged lattice | (8,4,48) | (96,1) | no rooted self-mirror centre-free cycle |
| Decimal p12/m9 | merged lattice | (12,3,9) | (36,1) | no rooted self-mirror centre-free cycle |

Every positive multiple of the table's length-only primitive `(k,g)` passes **only** the length/clock equations, not physical boundary carries, exact literal cap return, a palindrome witness, or reachability. Temporal period can be smaller for a phase-symmetric state: use the **primitive period of the *entire* returning clock state**, not merely a displayed overflow word.

## 4. Reproducible controls, relation to existing work, remaining gap

The Python driver reads the canonical Lean base-9 certificate and base-50 JSON, constructs **actual canonical integers realizing the entire symmetric pairword**, and independently performs ordinary unbounded integer reverse-and-add; it checks every complete pairword and nonpalindrome on 20 (base 9) and 12 (base 50) steps at q=20,40,80,160. It also checks the genuine rooted decimal p8/m20 rec0, p8/m48 rec2 and p12/m9 **exterior and overflow clocks** over one primitive period at all four widths. These latter controls are **not certificates**, and no finite-time survival claim is offered as progress.

Prior art: `reports/REPORT_205.md` and `reports/REPORT_215.md` already prove several run-length growth/charge constraints for uniform six-cycle bands; `reports/REPORT_LATTICE_BAND.md` supplies merged-lattice soundness; `results/AgentY18P12CentreCharge216.md` already establishes the 216-step charge obstruction. The present specification makes explicit the **full temporal/spatial Diophantine gate** and a uniform-over-q coefficient-mass gate for arbitrary fixed periodic words; it does not supplant those proofs.

**Exact unresolved lemma:** exhibit a canonical base-10 seed and a physically carry-sound, palindrome-free full phase cycle satisfying the gates above for every admitted band length, with a nondepleting centre/interface return and `g>0`. No such decimal witness is established here.
