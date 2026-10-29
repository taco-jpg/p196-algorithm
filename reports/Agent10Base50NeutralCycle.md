# Agent10Base50NeutralCycle: complete base-50 neutral-band certificate

**COMPUTED, base 50 only.** This new certificate uses the repository's existing sound `Agent120.Neutral.cycleOK` template and is independent of the base-146 result. No Lean code is changed and no new kernel-checked theorem is claimed.

## Explicit finite data

The exact certificate is `calculation/neutral_band/agent10_base50/cert_b50.json`. Coefficients are least-significant first. For base `b=50`, neutral pair coefficient `b-1=49` and gap `h`, the symmetric template is

`T(B,C,h) = B ++ [49]^h ++ C ++ [49]^h ++ reverse(B)`.

The initial outer exterior `B0` has 36 coefficients with nonzero first coefficient; the initial palindromic centre is `C0=[62,15,22,32,32,22,15,62]`, and `h0=12`. Each pair coefficient belongs to `[0,98]`. The deterministic generator `generate.py` finds `B0` from the exact canonical-root period-two position automaton, then computes all four transitions using independent integer normalization, requiring the fourth return to `(B0,C0)`. No SAT or additional data file is needed.

| phase | B length | C length | e1 | e2 | gamma | u | v |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 36 | 8 | 0 | 1 | 0 | 1 | 0 |
| 1 | 35 | 8 | 1 | 0 | 1 | 0 | 0 |
| 2 | 36 | 9 | 0 | 1 | 0 | 1 | 1 |
| 3 | 35 | 7 | 1 | 0 | 1 | 0 | 0 |

Every step obeys the original `norm` equations for `DB,DC,DR`, `nextB` and `nextC`; the trailing `u` and reflected `v` trims each consist entirely of coefficient 49, and `B4=B0,C4=C0`. The net neutral-band gain is `sum(u+v-gamma)=3-2=1` per four steps, keeping the gap positive forever from the initial value 12.

## Independent ordinary-integer checks

The independent `check.py` neither imports the generator nor calls an SMT solver. It reads the JSON and recomputes the complete carry, edge and trimming equations, then constructs an actual ordinary base-50 integer with the specified symmetric pair-word template. It executes reverse-and-add using Python arbitrary-precision integers and verifies the **entire** pair word against the expected pumped phase template and nonpalindromicity at every step. Command `python3 calculation/neutral_band/agent10_base50/check.py calculation/neutral_band/agent10_base50/cert_b50.json 2000` passed, with final digit length 1103 and gap 512; the single reproduction runner uses a 1000-step Python control.

The separate `replay.cpp` implements base-50 ordinary digit-list reverse-and-add with integer carries. It does not import Python, the generator or `check.py`; it independently reconstructs the starting digits from the symmetric pair coefficients and verifies every digit sum in the full pairword, plus no palindrome, for 20,000 consecutive steps. Command `c++ -std=c++17 -O3 calculation/neutral_band/agent10_base50/replay.cpp -o /tmp/agent10_b50 && nice -n 10 /tmp/agent10_b50 calculation/neutral_band/agent10_base50/cert_b50.json 20000` passed, producing final digit length **10104** and gap **5012**.

## One-command reproduction including mandatory controls

```bash
bash calculation/neutral_band/agent10_base50/reproduce.sh
```

This runner regenerates the exact JSON into a temporary location and checks byte-for-byte identity with `cmp`; executes the independent Python bigint and C++ 20,000-step digit-list replays; builds the repository's `calculation/decimal_frontier/lattice_formats/code/bauto3.cpp` without changes and asserts known exact SCC positive controls: base 9 `g=1100011000`, spatial period 4 depth 61; base 13 `g=1010010000`, fixed SCC depths 55 and 75, each at a 3,000,000-state cap. All code, small data (under 5MB), independent checker and exact commands are in **one commit**.

**Scope and verification.** This is a complete base-50 finite computational neutral-band certificate under the existing sound certificate format, not a proof in Lean's kernel and not a parametric infinite family. It proves nothing about decimal 196. Local GitHub HTTPS checkout and the required `python3 tools/verify.py --changed` cannot be run in the present container, so publication by the GitHub Git Data API does not imply repository-wide verification. The two standalone arithmetic controls were run locally.
