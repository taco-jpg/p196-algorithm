# Agent W06: exact two-state regular carry-erasure automaton

**PAPER PROOF** for the all-length synchronization language below; **COMPUTED** for 37,280 exhaustive bounded checks, independent Python BIGINT controls, and an inherited 20,000-step ordinary-decimal replay. NOT an infinite Lychrel certificate, complete enumeration of every possible eraser, or Lean verification.

## Positive extension of the eight-site carry-erasure family

Use the same base-10 least-significant-first coefficient blocks B and W of p8/m20 rec0, defined in calculation/new_structures/agent-W06/toggle_family.py and in reports/AgentW06RegularCarryErase.md. W has length 20. Now permit the following **sixteen** coefficient toggles, each by exactly +9 or -9:

| W cell j | baseline | alternate |
|---:|---:|---:|
| 0 | 17 | 8 |
| 1 | 3 | 12 |
| 2 | 1 | 10 |
| 3 | 13 | 4 |
| 4 | 17 | 8 |
| 5 | 11 | 2 |
| 6 | 14 | 5 |
| 7 | 3 | 12 |
| 8 | 18 | 9 |
| 9 | 1 | 10 |
| 10 | 2 | 11 |
| 12 | 7 | 16 |
| 13 | 3 | 12 |
| 14 | 14 | 5 |
| 15 | 12 | 3 |
| 19 | 13 | 4 |

Inside each W block select any subset of these sites without two *adjacent* indices. Across adjacent W blocks, also prohibit choosing site 19 in the previous block AND site 0 in the next. This is a strictly larger alphabet than the previous independent eight-toggle family and requires just **one boundary state bit**, namely whether the preceding cell was toggled.

For any M>=1, legal masks a[0]..a[M-1], and even centre C in {0,2,...,18}, put

    H = B ++ W[a[0]] ++ ... ++ W[a[M-1]]
    P = H ++ [C] ++ reverse(H).

Digit-split this pairword using (min(9,p),p-min(9,p)) on mirrored coefficients, with centre digit C/2, to obtain a canonical decimal seed N(P). Its length is exactly 2(39+20M)+1. Distinct mask words give distinct canonical integers.

## Exact transfer matrix and growth (PAPER PROOF)

The 2-state automaton records the previous block's site-19 bit, starting at 0. A transition accepts the next 16-bit mask precisely if there is no adjacent selected site within its block and it does not select site 0 when the previous state is 1. Its new state is the current site-19 bit. The matrix of numbers of accepted masks, indexed by old state 0/1 in rows and new state 0/1 in columns, is **exactly**

    T = [[1864,1864],
         [1152,1152]].

Proof of counts: when site 0 is unselected, selectable sites 1..10 form a path of length 10 with 144 independent sets, sites 12..15 form a path of length four with eight independent sets, and site 19 is freely selected or not. For each fixed output state (site 19), there are 144*8=1152 masks. When site 0 is selected, site 1 is excluded and selectable sites 2..10 form a length-nine path with 89 independent sets. Together with sites 12..15 there are 89*8=712 additional choices per fixed output state, but only if previous state=0. Therefore T00=T01=1152+712=1864, T10=T11=1152.

The initial vector of output-state counts is [1864,1864], summing to 3728 legal first-block masks. Multiplication by T maintains equality of the state counts and multiplies their sum by 3016. Hence, for **every integer M>=1**, the exact number of distinct accepted mask sequences is

    A(M) = 3728 * 3016^(M-1).

This counting result is a finite-state transfer-matrix proof, not a sample census.

## All-length soundness: common pairword after one step, common integer after two

At each toggled coefficient x in the low half, let y=n-1-x be its mirror, where n is the initial odd coefficient length. An individual +/-9 toggle in the specified table changes the base-10 normalization carry for one cell and merges it after one successor cell; the precise baseline carry is fixed by the unmodified W and absorbing B. Each successor coefficient is different from 9 in the accepted unmodified context, including the even central C after site 19 at the innermost W block. The no-adjacent rule ensures no second toggle modifies that successor; its interblock version protects the only cross-block adjacency. Thus selected toggles have **disjoint two-cell carry domains**, regardless of M.

Precisely, for a +9 toggle at x and y, the complete normalized-digit difference is -1 at x and y, +1 at x+1 and y+1, and zero at all other indices; reverse these signs for a -9 toggle. The unchanged B suffix ensures an overflow digit 1, giving both normalized decimal outputs length n+1. In a length-(n+1) output, reflection is i -> n-i, so x pairs with y+1, and x+1 pairs with y. Each of the four-impulse differences cancels in its symmetric coefficient. Their domains are disjoint for accepted masks, so these cancellations add for every allowed mask.

Therefore the **entire first-step pairword** is independent of all M mask choices, and one further ordinary reverse-add, which is determined by that full pairword, produces the **identical integer N2**. This is a PAPER PROOF for arbitrary M, not a finite-run guess. For t=0 the initial B coefficient 17 is odd; for t=1 the common rec0 temporal-root coefficient at index 1 is 13, also odd. Since palindrome digits have all even symmetric pair coefficients, all accepted seeds avoid palindromes at t0 and t1.

## Computed finite-time consequence

For **M=320, C=18**, the exact family contains

    A(320) = 3728 * 3016^319

distinct canonical **12,879-digit** integers, approximately 2^3699.0004 seeds. Every one joins the common baseline orbit after two reverse-add additions. The previously published independent actual-GMP and actual-digit-array 20,000-step replay of that exact baseline in results/AgentW06RegularCarryErase.md proves *computationally* that all 20,001 tested states are nonpalindromic, all carry-overflow bits match 10101010, and the full decimal final length is 22,879. The complete MSD-first FNV64 final fingerprint is **3bba2a5955eee568**. The digit-array checker also checked the entire 39-cell temporal B root plus the following 256 W coefficients for every state. Thus every A(320) seed survives this finite horizon. This does not imply any seed is a Lychrel number.

## Reproducibility and independent controls

Run directly from the repo root:

    python3 calculation/new_structures/agent-W06/regular16_automaton.py

This implementation exhausts **all 3728** structurally allowed one-block masks at each even centre value 0..18 (37,280 exact tests). It checks the entire predicted four-impulse difference, next-pairword equality, output length, exact two-state count matrix, and selected larger random words: 40 deterministic trials each at M=2,3,5,10,100,320,1000 (280 independent multiblock tests). Of those, 35 pairs are *also* replayed using ordinary Python big integers constructed independently from decimal seed digits, comparing literal second-step values and verifying both first states are nonpalindromic. One deliberately invalid adjacent j7/j8 mutation fails the first-step pairword equality. Exact compact expected metrics are in calculation/new_structures/agent-W06/regular16_observations.json. Independent 20k ordinary-integer controls remain in toggle_schoolbook.cpp and toggle_gmp.cpp, as shipped by the previous W06 result.

The accepted regular language is **sufficient, not complete**; certain adjacent-site combinations can erase too, but they are not covered by this noninteracting two-state proof. In particular, the construction gives a large preimage family, **not** a regenerative outward-propagating interface. A finite certificate for an infinite nonpalindromic decimal orbit remains open.
