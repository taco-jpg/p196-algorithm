# Agent X10: three-stage nested affine packet carry gates synchronized to 88-step phases

**Status: COMPUTED.** Exact local arithmetic and finite affine-parameter guards, with independently replayed entire ordinary decimal integers. The construction is finite horizon, not an infinite Lychrel certificate. This result **composes** the prior six→five→three fusion clock with one further external symmetric packet layer, obtaining a genuine third nonlinear carry-transfer gate after the earlier central collision.

## 1. Eight symmetric packets with three nested gaps

For integer parameters `q,R,S` define the genuine base-10 numeral

`N_0(q,R,S) = 88*10^(2q+2S+2R+4) + 78*10^(q+S+R) + 37*10^(q+S) + 37*10^q + 75`.

Its eight packet bases are

`0, q, q+S, q+S+R, q+S+R+4, q+S+2R+4, q+2S+2R+4, 2q+2S+2R+4`.

Every reflected pair sums to the same highest base `B=2q+2S+2R+4`, so the local reflection partner is always the packet with reverse index, and the local reflection index is the current high packet's highest local exponent. Initially the nonempty digit packets are, least significant first, `[5,7]` at base 0, `[7,3]` at base q, `[7,3]` at base q+S, `[8,7]` at base q+S+R, and `[8,8]` at base B. Other packets begin empty. Separate packet carrying is exact while the *full digit aggregate* remains below 10 per position; the innermost pair alone is allowed temporary transparent overlaps under this capacity guard at times t4..12. This is established by exact finite local coefficient checks, not sample interpolation.

Three explicitly defined, **canonical** packet fusions occur:

1. **t=13, 8→7:** normalize the inner two packets at bases `q+S+R` and `q+S+R+4` into a single packet anchored at `q+S+R`, carrying across their overlap.
2. **t=t2(R), 7→5:** normalize the centre and its adjacent mirror pair at bases `q+S`, `q+S+R`, `q+S+2R+4` into a packet anchored at `q+S` once their separation guard first reaches contact. Since the *previous* integer source state was correctly digitized, the raw sum of the new overlapping packets still has the exact true integer value; merging with ordinary carries produces its canonical word.
3. **t=t3(S;R), 5→3:** normalize the new centre and its remaining adjacent mirror pair at bases `q`, `q+S`, `q+2S+2R+4` into a single packet anchored at `q` once their supports first contact. Again, a canonical merged packet carries across both sides; the exterior `[low,high]` packets remain separated by the q shield.

Between fusions, mirrored *distinct* packet pairs are updated by the same local `newpacket` digit normalization as in earlier X10 results. For an odd number of packets, the central self-reversing packet's local reflection index is `h+4` (seven-sheet), `h+2R+4` (five-sheet), or `h+2S+2R+4` (three-sheet), where `h` is the current top packet's local leading exponent. This is a direct consequence of reflecting an absolute exponent about the entire numeral's top exponent and subtracting the centre's affine base. The correctness argument is value preservation by per-packet normalization plus a capacity guard on source and target. The source just before a fusion is separated, and the fusion normalizes its newly overlapping image *before another reversal*; hence no lost cross-packet carries.

## 2. Two independent local collision clocks

The five/seven packet **local recurrences** do not depend on the large outer gap q or the next unused buffer S. After the first centre fusion, the second event is triggered by the first time the local demand exceeds R:

`F_t=max(end(P_left)-start(C), end(C)-4-start(P_right))`;

`t2(R)=min{t>=13 : F_t>=R}`.

The prior exact `clocked_fusion_scan.cpp` gives `F_88=56`, so choosing **R=56** schedules the second fusion at t88. All prior noncentral same-slope buffer gaps are checked before that event, so this is an actual first physical contact, not an arbitrary symbolic rewrite.

After that merger, the remaining outer-middle pair begins at bases q and q+2S+2R+4 around a centre anchored at q+S. The next demand, now using the five-sheet source packets, is

`G_t=max(end(P_left)-start(C), end(C)-(2R+4)-start(P_right))`;

`t3(S;R)=min{t>=t2(R) : G_t>=S}`.

For fixed R=56, **G_t depends on neither q nor S before this third fusion**. The independent finite scanner `third_clock_scan.cpp` shows exact choices:

| R | S | first fusion | second fusion | third fusion |
| ---: | ---: | ---: | ---: | ---: |
| 56 | **109** | 13 | **88** | **176** |
| 56 | **161** | 13 | **88** | **264** |

Local scan markers: `G_176=109`, `G_264=161`; S108 triggers at t175 and S110 at t178. This verifies precise phase selection, not a statement that the full orbit is periodic or that centres renew indefinitely.

## 3. Exact finite polyhedral shielding and nonpalindrome witness

All sheet bases are of form `a_i*q + b_i(R,S)` with slopes a_i in `{0,1,2}`. At every state the symbolic checker proves that the low/outer packet and the relevant inner packets stay physically separated: for each pair ordered from low to high, either its spacing has zero slope in q and its **actual** fixed R,S guard is checked, or it yields an exact lower bound on q through a positive-slope linear inequality. Nonnegative exponents are checked similarly. The only allowed physical overlap before t13 is the innermost central pair with aggregate digit capacity <=9; subsequent contact events are resolved by canonical fusion before any further reversal. These are finite integer computations on packet supports, not Monte Carlo or q interpolation.

The full protected-region bounds for two phase-aligned cases, exactly enumerated through t20,000, are:

| (R,S) | universal minimum q | physical length at t0 | length at t20000 | fusion times |
| --- | ---: | ---: | ---: | --- |
| (56,109) | **12,014** | 24,364 | 32,618 | 13,88,176 |
| (56,161) | **11,977** | 24,394 | 32,648 | 13,88,264 |

Both families have an unequal *exposed outer pair* of decimal digits at every symbolic state. Since those high/low packets are disjoint from the centre for every q above the exact bound, this proves nonpalindromicity for each of the 20,001 states in **every** parameter member of these two finite-horizon families. The theorem is restricted to t≤20,000; it does not infer nonpalindromicity after the q shield is eventually consumed.

## 4. Independent complete-integer decimal replay

`nested_three_fusion_replay.cpp` begins from the entire explicit decimal numeral and advances it by an independent schoolbook whole-word reverse-and-add routine, without consulting the symbolic packet oracle for the next actual integer. At every step, it separately assembles the predicted **complete decimal word** by aggregating the current eight/seven/five/three packets, checks every digit equality, checks the true complete numeral for palindrome, and checks the q guard and outer-digit witness. Controls:

- `(q,R,S)=(12014,56,109)`: 20,001/20,001 full-word matches and nonpalindromes; 24,364→32,618 digits; FNV64 across every digit of every word `2370273337756707104`.
- `(12015,56,109)`: 20,001/20,001 matches/nonpalindromes; 24,366→32,620; FNV64 `2468584939443058680`.
- `(11977,56,161)`: 20,001/20,001 matches/nonpalindromes; 24,394→32,648; FNV64 `1307506684224705553`.
- `(600,56,109)`: 1,001/1,001 matches/nonpalindromes through t1,000; exact bound q=600 and FNV64 `4870332162165790597`.

No palindrome was observed, and all real whole-number digits matched exact symbolic words in 61,004 states across these four controls. Every t0..20000 step of the first three controls is independently checked, not just the sparse checkpoint rows. Source, compact deterministic traces, paper derivation and reproducer: `calculation/new_structures/agent-X10/`, `results/AgentX10ThreeLevelFusionClock20000.md`, and `bash calculation/new_structures/agent-X10/reproduce_nested3.sh`. No Lean files were changed and the repository-wide Lean checker could not be run here; do not label this LEAN-VERIFIED.

## 5. Where a true infinite proof would have to improve

This is a *finite descending packet-stack*: two explicitly programmed nested buffer gaps are consumed during collision, causing 8→7→5→3. No new packet layers are spontaneously created by the displayed orbit. The q shielding requirement continues to grow over time. Synchronizing a finite number of carry transfers to multiples of 88 does not establish an invariant macro-return. To obtain an infinite base-10 Lychrel certificate one would need a **stack-replenishing or self-replicating packet rule** with finite verification of a return relation and guaranteed nonpalindrome witness for all macrocycles. This work provides exact clocked gates but not that missing recurrence; it proves nothing about decimal seed 196.
