# Agent W18: a 100,000-step base-10 1089-class uniform shield
**Label: COMPUTED** (ordinary decimal arithmetic, no Lean or infinite-orbit claim).

The true decimal seeds are `N0(Q)=5(99)^Q4`, every integer Q>=20702. All full base-10 states t=0..100000 have *exact* digit form `U_t++9^L_t(Q)++V_t` (least significant first), `|U_t|=|V_t|`, `U_t != reverse(V_t)`, and `L_t(Q)>=2`. This is the existing N23 exact two-wall nine-band transition rule applied to a new initial pairword class `[9]++[18]^(2Q)++[9]` (not their original initial end pair-sum 5). It proves a symmetric central coefficient-18 pairword band and nonpalindromicity at every claimed step.

The rule's exterior updates are independent of Q so long as L>=2. The exact computed exterior orbit has 58,598 paired nine-boundary trims and 41,402 overflows; therefore total band loss is `2*100000 - 41402 - 2*58598 = 41402`. The minimum baseline Q=20702 starts with 41,404 central 9s and reaches exactly 2 at the end; the minimum was first achieved at t99999. Hence for all Q>=20702, `L_t(Q)=L_t(20702)+2(Q-20702)`, proving every member safe through 100000 steps under the sound local carry lemma. The seed starts with 41,406 decimal digits and ends with 82,808 digits.

An **independently programmed full-width ordinary decimal digit-vector oracle** performs each complete reverse-add operation column by column (without the symbolic wall rule), checks every one of the 100001 actual integers for a palindrome, measures the central 9 band, and hashes the entire resulting numeral. Checkpoints for Q20702:

| t | digits | central 9 band | checksum mod 1000000007 |
|---:|---:|---:|---:|
| 1000 | 41831 | 40979 | unavailable |
| 5000 | 43504 | 39306 | 495327694 |
| 10000 | 45566 | 37244 | 418761382 |
| 20000 | 49680 | 33130 | 535191435 |
| 50000 | 62097 | 20713 | 509705119 |
| 100000 | 82808 | 2 | 132839273 |

Q20701 first violates the transducer's required `L>=2` guard at t99995. Loss of this invariant is **not** a palindrome or a proof that the true decimal orbit stops; no infinite-time certificate is claimed. Relative to N23's uniform 100k seed threshold Q30037, this uses about 31.1% fewer repeated 99 blocks, an independently replayed constructive improvement, not a duplicated census.

Reproduce with `bash calculation/new_structures/agent-W18/reproduce_100k.sh`. Sources and compact threshold ledger are under `calculation/new_structures/agent-W18/`; inherited `wall.cpp` is in the immediately previous W18 commit. The local HTTPS GitHub checkout is unavailable so full `python3 tools/verify.py --changed` was not executed; no Lean files are added. The hard missing ingredient remains an infinite-time replenishing centre or a closed renormalization cycle.
