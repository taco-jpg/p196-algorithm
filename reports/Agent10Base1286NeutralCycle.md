# Agent10Base1286NeutralCycle: complete base-1286 neutral-band certificate

**COMPUTED, base 1286 only.** This is a new finite instance of the repository's existing sound neutral-band reverse-and-add certificate format `Agent120.Neutral.cycleOK`. No new generic theorem or Lean-kernel certificate is claimed.

## Source-level exact data and four-edge cycle

The committed `calculation/neutral_band/agent10_base1286/cert_b1286.json` records all complete outer `B` and palindromic centre `C` coefficient arrays (least-significant first) at all four temporal phases, plus each successor, carry, overflow and neutral trim. The initial `B0` has 1204 coefficients; initial centre is `C0=[1607,1044,742,548,548,742,1044,1607]`; start with neutral band width `h0=12` and pair coefficient `b-1=1285`. All coefficients lie in `[0,2570]`, and the leading-digit boundary has `B0[0]!=0`.

For each time phase, use the symmetric pairword template `T(B,C,h)=B ++ [1285]^h ++ C ++ [1285]^h ++ reverse(B)`. The existing `norm` equations define `DB,e1`, `DC,e2`, `DR,gamma`; a raw `nextB` word is trimmed by `u` final neutral coefficients and a raw `nextC` word by `v` neutral coefficients at each end.

| phase | B length | C length | e1 | e2 | gamma | u | v |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 | 1204 | 8 | 0 | 1 | 0 | 1 | 0 |
| 1 | 1203 | 8 | 1 | 0 | 1 | 0 | 0 |
| 2 | 1204 | 9 | 0 | 1 | 0 | 1 | 1 |
| 3 | 1203 | 7 | 1 | 0 | 1 | 0 | 0 |

The fourth edge returns to the exact initial `B,C` pair; `sum(u+v-gamma)=3-2=1` guarantees a positive neutral band that increases every four-step cycle. The committed `generate.py` deterministically reconstructs the canonical-root exterior through a finite exact two-time position automaton and then generates all four source-normalized edges from this centre, asserting closure and trimming. This generator uses no solver or uncommitted cache.

## Independent integer and digit-list replay

The separate `check.py` imports neither the generator nor the exterior automaton. It checks the full JSON with independent source-level digit-normalization arithmetic and exact mirrored neutral trims. It then constructs an ordinary base-1286 integer from the full pair coefficients, performs Python arbitrary-precision reverse-and-add, and checks the **entire** pumped pairword template and absence of a palindrome at every step. Run `python3 calculation/neutral_band/agent10_base1286/check.py calculation/neutral_band/agent10_base1286/cert_b1286.json 1000`: **PASS**, final digit length 2939, neutral gap 262.

The C++17 `replay.cpp` does not invoke Python, `generate.py` or `check.py`; it builds the ordinary base-1286 digits separately and executes digit-list reverse-and-add with explicit carries. On **20,000** steps, the complete pairwords match the four-phase pumped template and the digit lists are never palindromic. Direct command: `c++ -O3 -std=c++17 calculation/neutral_band/agent10_base1286/replay.cpp -o /tmp/agent10_b1286 && nice -n 10 /tmp/agent10_b1286 calculation/neutral_band/agent10_base1286/cert_b1286.json 20000`. Output: **PASS**, final digit length **12440**, gap **5012**.

## Full self-contained reproduction

```bash
bash calculation/neutral_band/agent10_base1286/reproduce.sh
```

The runner regenerates the JSON from source into a temporary directory and demands byte identity with the committed 133KB data file; runs the independent Python bigint checker; compiles the independent C++ and executes its 20,000 steps; compiles existing repository `calculation/decimal_frontier/lattice_formats/code/bauto3.cpp` and checks mandatory b9 `g=1100011000` period-4/depth61 and b13 `g=1010010000` singleton depths55/75 at a 3,000,000-state cap. All source code, explicit data, checkers, controls, commands and this report are included in a **single commit**.

This certificate is in base 1286 only. It is not a claim of an infinite parametric family, any decimal Lychrel number, a fact about 196, or Lean verification. The container has no functional HTTPS GitHub DNS checkout, so `python3 tools/verify.py --changed` could not run; the non-Lean result can be pushed via GitHub's available write API without overstating repository-wide verification.
