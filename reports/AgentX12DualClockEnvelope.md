# X12 finite two-counter collision/guard envelope (COMPUTED)

## Construction and measurement

For exact base-10 low-first pairwords, use B0 (length 39), W0 (length 20), and U of length40 with all 1s except U[13]=7,U[20]=7,U[30]=6 from the X12 centre-pulse result. C(r)=[8,0,0]++U++1^r++[16]++1^r++reverse(U)++[0,0,8]. The genuine seed integers realize P(q,r)=B0++W0^q++C(r)++reverse(W0)^q++reverse(B0). Compare the full pairwords for r and r+1, requiring the longer to equal the shorter after symmetric deletion of exactly one coefficient on each side. Normalize the coefficients by their actual base-ten carries, with a separate overflow bit at every step.

Two distinct first-failure clocks emerge in the selected finite experiments. Let E(q) be the first time either orbit's initial 39-coordinate rooted p8 exterior differs from its established phase row; let L(q,r) be the first time the two whole pairwords cease to differ by precisely one symmetric inserted coefficient. With q varying and r=12000, all 12 listed tested q have E(q)=88q+276, while their whole-word insertion, and the alternating overflow clock, survive at least to E(q)+2.

With r varying, select q_min(r)=max(1,floor((L(r)-276)/88)+1) from the **proposed** collision staircase L(5k+s)=6k+[13,15,16,16,17][s-1], 1<=s<=5. In all 12 listed r values, q_min's actual full pairword insertion first fails at exactly L(r), the 39-site B exterior and alternating overflow persist through the failure time, and q_min-1 (when >=1) first loses the B exterior at E(q_min-1) <= L(r). Thus the displayed threshold is exact for THESE cases, not for all integers q,r. There is no claim that the two counter clocks are the only possible failure events.

The two clocks describe a nontrivial protected transport regime. In the interval where the outer W reservoir is intact, the extra uniform central coefficient follows a six-phase doubling clock 2,4,8,16,14,10, with a first wall collision that grows by six steps per five additional central positions. The 88-step outer lattice depletion competes with this six-step centre clock. At r=20000 the inner collision is t24011, and 270 W blocks protect the outer rooted B interface through that time, whereas 269 W blocks fail at t23948. The earlier independent 20,000-step q300,r20000 two-orbit integer replay is a protected point well inside this computed two-counter region; it is not an infinite extension.

## Exact samples

Outer q, with r=12000 and first-B deviation E:
`(1,364),(2,452),(3,540),(4,628),(5,716),(7,892),(10,1156),(16,1684),(20,2036),(30,2916),(50,4676),(65,5996)`. Pairword splice and alternating overflows are valid through E+2, so these are genuine isolated exterior-boundary departures, not the centre collision.

Protected inner triples (r,q_min,L):
`(100,1,131),(250,1,311),(500,4,611),(850,9,1031),(1000,11,1211),(1500,18,1811),(2000,25,2411),(3000,38,3611),(5000,66,6011),(10000,134,12011),(15000,202,18011),(20000,270,24011)`. At q_min-1 for q_min>1 the first B failure occurs at E(q_min-1), stored exactly in `envelope_observations.json`. All tests simulate through the asserted collision, not merely a horizon where both templates are still equal.

A completely separate Python built-in-integer reverse-and-add calculation checks both genuine decimal numbers at every state for (q,r,L)=(1,100,131),(4,500,611),(9,850,1031), 3552 integer-state comparisons in total, using literal decimal reversal and checking that the splice survives before L and fails at L. It tests zero palindrome encounters. The C++ symbolic program additionally checks that every overflow retains the prescribed 1010 clock until the protected collision, and compares all 39 exterior coefficients on both orbits at each step.

## Implication for certificate construction

A candidate two-timescale macro-certificate needs a **renewal edge** that compensates both monotone resource clocks, rather than an indefinitely large initial pair of reservoirs. The observed frontier has a nearly linear protective ratio q/r of about 3/220 in large listed cases: one additional W block gives 88 outer clock steps, and five central 1s give six inner clock steps. The exact finite threshold is q_min(r) on the stated samples only. Neither the linear formulas nor an invariant renewal map has been established for all q,r. A finite 264-step affine-counter Presburger guard, with exact internal carries and a compensating q increase, is a plausible next checker target. This is a concrete construction direction, not a negative no-go result.

## Reproduction and limits

From repository root: `g++ -O3 -std=c++17 calculation/new_structures/agent-X12/envelope.cpp -o /tmp/x12_env && /tmp/x12_env --full && python3 calculation/new_structures/agent-X12/envelope_bigint.py`. The short C++ default mode checks selected controls. Exact compact data: `calculation/new_structures/agent-X12/envelope_observations.json`.

No all-parameter proof, infinite palindrome-free decimal certificate, or Lean verification is claimed. No file imported by other agents is modified; local GitHub checkout and repository-wide `tools/verify.py --changed` were unavailable.
