# Agent X10: a programmable 88-step collision clock in a nested decimal carry hierarchy

**Status: COMPUTED**, with an exact paper justification for the local affine-packet arithmetic. This is an explicit **finite-horizon** mechanism only. It does not construct an infinite decimal Lychrel certificate. The novelty over the previous X10 single fusion is a genuine second, later nonlinear carry event whose time can be selected by one independent spatial parameter `R` and aligned to 88-step multiples.

## 1. Explicit two-parameter family and symmetric six-sheet geometry

In ordinary decimal, for integers `q,R` in the domains checked below, begin with

`N_0(q,R)=88*10^(2q+2R+4)+78*10^(q+R)+37*10^q+75`.

Store all digit coefficient words least-significant first. The six symbolic packet bases are

`0, q, q+R, q+R+4, q+2R+4, 2q+2R+4`.

They pair under reflection about the top numeral exponent because each mirror pair of bases sums to `B=2q+2R+4`. Initially, the nonempty packet rows are `P0=[5,7]`, `P1=[7,3]`, `P2=[8,7]`, and `P5=[8,8]`; the other rows are empty. For every state with a canonical aggregate, local packet `P_i` updates via a base-10 digit carry normalization of the sum of itself and the reverse of packet `P_(5-i)` about the high packet's local leading exponent `h`. The four exteriors are held apart by the variable gaps; central packets P2/P3 are deliberately allowed to overlap while their aggregate decimal coefficients stay below 10, precisely as proved in `reports/AgentX10TransparentOverlapFormat.md`.

At t=13, normalize the sum of P2 (base q+R) and P3 (base q+R+4) into ONE canonical centre packet C anchored at q+R. The six-sheet representation becomes the symmetric five-sheet arrangement

`0, q, q+R, q+2R+4, B`.

The five-packet local update uses the same exterior reflection pairs and, for C alone, the reflected local centre index `4+h`. The central fusion repairs the exact cross-centre carry that would make the separate-sheet aggregate exceed 9 at state14.

## 2. Second collision clock and exact timing law

Before it meets the side packets, the five-packet symbolic recurrence is **independent of both q and R**. The two inner side packets P_left at q and P_right at q+2R+4 are paired reflections, while C is anchored at q+R. At a time t their first physical overlap is characterized by either

`end(P_left,t) >= R + start(C_t)`

or

`R + end(C_t) >= 2R+4 + start(P_right,t)`.

Therefore set

`F_t = max( end(P_left,t)-start(C_t), end(C_t)-4-start(P_right,t) )`;

then the **first second-fusion time** for a chosen R is exactly

`t_2(R)=min{t>=13 : F_t >= R}`, provided no earlier unrelated packet collision occurs. This is a finite local frontier clock, not interpolation between whole-orbit samples. Every F_t is obtained from a recurrence that does not contain q or R. The checker verifies the relative packet contact independently of the full decimal replay and confirms all other packet ordering guards.

With d=4, the finite clock scan through t=500 gives the exact choices:

| R | first second fusion t_2 | clock alignment |
| ---: | ---: | --- |
| 56 | **88** | 1 x 88 |
| 60 | 94 | unsynchronized control |
| 110 | **176** | 2 x 88 |
| 165 | **264** | 3 x 88 |

The full table `R=10..150` (selected rows) and demand at t88/t176/t264 is committed as `clocked_fusion_scan.csv`, produced by `clocked_fusion_scan.cpp`. This is a **programmable collision delay**, not a periodic orbit and not a claim that these 88-step phases regenerate a missing digit band.

At time t_2, the three inner five-sheet packets may physically overlap. But their **source packets at the previous time were disjoint**, so the local step's integer sum is still exactly the true next integer. Fuse all three inner contributions into ONE canonical centre anchored at q by digitwise carry normalization with offsets 0,R,2R+4. The resulting three-packet geometry has bases

`0, q, 2q+2R+4`,

and its central self-reflection uses the local index `2R+4+h`. This is a *second exact nonlinear carry transfer*. Thus the entire trajectory moves across canonical grammars 6 → 5 → 3 without any erroneous global carry assumptions.

## 3. Universal integer-gap bounds, exact digits and palindrome avoidance

For each stage the checker forms every nonnegative-exponent and *non-overlapping exterior* inequality. Every inequality has affine form `a*q >= c` for integer a>=0, with the fixed-spacing a=0 cases checked directly; the six-sheet central P2/P3 pair is the only initially permitted overlap and undergoes the digit-sum <=9 capacity test. Every other pair must be strictly separated. At the fusion times, the newly aggregated central packet is normalized before checking capacity and exterior separation. These constraints produce exact integer ceiling bounds for all q at every state. Their maximum over t=0..20,000 gives:

| R | second fusion at | universal q minimum to t20000 | initial decimal length | length at t20000 |
| ---: | ---: | ---: | ---: | ---: |
| **56** | **88** | **11,964** | 24,046 | 32,300 |
| **110** | **176** | **12,040** | 24,306 | 32,560 |
| **165** | **264** | **11,971** | 24,278 | 32,532 |

At *every* phase of the symbolic program the low and high exterior packets have an unequal exposed mirrored digit, protected by the stated separation guard. Hence no guarded state can be a palindrome. Combining all exact symbolic transitions with the universal q guards yields, for each listed R and **every q above its threshold**, 20,001 certified nonpalindromic states. This universal parameter statement is finite: no claim is made for t>20000 at any fixed q.

For independent tests, `hierarchical_fusion_replay.cpp` builds the **entire ordinary decimal numeral** directly from the four initial nonzero contributions and advances it using a separate ordinary schoolbook reversal-plus-add, never using the symbolic recurrence to calculate the actual next integer. At **every state** it independently assembles the predicted full numeral from the current six/five/three packet tableau, verifies every digit, and checks that the actual entire numeral is not palindromic. All three boundary-q replays finished 20,000 operations with `matched=20001` and `nonpal=20001`. Rolling FNV64 digests of all decimal digits across all states are:

- R56 q11964: `11746619098009243994`;
- R110 q12040: `5249565364949052768`;
- R165 q11971: `10506554422228640177`.

Thus there are 60,003 explicitly replayed nonpalindromic decimal states, plus the universal exact packet/shield statement for these three infinite *parameter* families up to a finite horizon. The stored compact checkpoint traces (not 60,003 giant numerals) can be reproduced by `bash calculation/new_structures/agent-X10/reproduce_clocked.sh`, requiring g++ and standard tools. This script tests each clocked case, its universal shield, all whole-digit arithmetic, and the clock scan. No Lean files were touched. The repository-wide Lean verifier was unavailable locally; this is not a Lean-verification claim.

## 4. The specific missing infinite condition

In the three-packet stage the central packet grows in length and eventually consumes the exterior gap for each fixed q; the computed minimum q at t20,000 remains around 12,000. Aligning the **fusion event** with 88-step clock phases is not the same as returning the digit template to a prior state. An actual decimal Lychrel certificate would require a parameter-retaining or parameter-growing *macrocycle* (possibly recursive layers of carry gates) with a formal invariant-domain condition on all phase transitions and a nonpalindrome witness at every phase. This result supplies exact programmable nonlinear carry gates and independently checked data but does **not** produce that macrocycle, nor any proof about the orbit of 196.
