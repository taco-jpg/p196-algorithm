# Complete base-146 neutral-band reverse-and-add certificate

**COMPUTED (base 146 only).** This supplies a new instance of the existing sound Agent120 neutral-band cycle format, not a new generic theorem and not a Lean kernel-verified instance. Every source, data file and control runner needed to reproduce the result is included in this same commit under `calculation/neutral_band/agent10_base146/`.

## Exact template and cycle

All coefficient words are least-significant first. With `b=146` and neutral coefficient `145`, use `T(B,C,h)=B ++ [145]^h ++ C ++ [145]^h ++ reverse(B)` where `B` is nonempty and `C` palindromic. The explicit first exterior `B0` has 80 coefficients and initial centre `C0=[182,45,102,102,45,182]` with `h0=12`. Every exterior coefficient lies in `[0,290]`; `B0[0]!=0`. Exact 4-edge JSON is `cert_b146.json`. The independent `generate.py` reconstructs the exterior with a canonical-root 2-time position automaton and regenerates identical JSON byte-for-byte, with no SMT or other untracked prerequisite.

| phase | centre | e1 | e2 | overflow gamma | trim u | trim v |
|---|---|---:|---:|---:|---:|---:|
| 0 | `[182,45,102,102,45,182]` | 0 | 1 | 0 | 1 | 0 |
| 1 | `[72,91,204,204,91,72]` | 1 | 0 | 1 | 0 | 0 |
| 2 | `[218,163,150,118,150,163,218]` | 0 | 1 | 0 | 1 | 1 |
| 3 | `[36,9,238,9,36]` | 1 | 0 | 1 | 0 | 0 |

All four steps satisfy the original exact `norm` carry equations, with e1!=e2, correct overflow, and the specified 145-only suffix of `nextB` and two 145-only prefixes/suffixes of `nextC`. The fourth returns `B4=B0`, `C4=C0` identically. `sum(u+v-gamma)=3-2=+1`, so the neutral band grows by exactly one every cycle from initial positive gap 12. The original repository's general Lean `lychrel_of_cycle` pumping theorem is applicable after its checker accepts this exact finite data, but no Lean file or kernel endpoint is claimed or pushed here.

## Ordinary-integer independent replay

Starting with the complete symmetric pair coefficient word `T(B0,C0,12)`, construct canonical least-significant-first digit pairs `lo=P_i-min(P_i,145)` and `hi=min(P_i,145)`, placing `lo,hi` at mirrored positions (and half the pair coefficient at the centre, if odd length). The leading digit is nonzero. The independent Python checker recalculates `norm`, all edge trims and closes the cycle, then performs 1,000 actual arbitrary-precision integer reverse-add steps, checking the *full* pairword equals the time-specific pumped template and that the integer is nonpalindromic at **every** step. Output: `PASS: plain Python big-integer reverse+add and full pairword+nonpal 1000 steps`, final digit length 689 and band width 262.

The C++17 `replay.cpp` independently constructs the digits and performs 20,000 ordinary digit-list reverse-add additions with carry, without calling Python, the generator or the finite-state engine. It checks the complete pair word and lack of palindrome at each step. Exact output: `PASS: 20000 independent ordinary digit-list base146 reverse-add steps; all full pair words match cycle and none is palindromic; final digits=10190 gap=5012`.

## Reproduction, external controls and scope

From the repository root, with only Python 3, a C++17 compiler and standard Unix shell utilities:

```bash
bash calculation/neutral_band/agent10_base146/reproduce.sh
```

This single script: (1) regenerates the certificate and requires `cmp` byte identity with the committed JSON; (2) runs the independent Python 1000-step bigint checker; (3) compiles the standalone C++ and checks all 20000 full digit-list steps; (4) compiles the repository's unchanged `bauto3.cpp`, runs mandatory positive control base9 `g=1100011000` with period-4 SCC depth61, and base13 `g=1010010000` with SCC singleton depths55/75. Control cap is 3,000,000 states. No code is sandbox-only. The wrapper uses a temporary directory and removes it on completion.

Individual commands include `python3 calculation/neutral_band/agent10_base146/generate.py --output /tmp/agent10_b146.json`, `cmp /tmp/agent10_b146.json calculation/neutral_band/agent10_base146/cert_b146.json`, `python3 calculation/neutral_band/agent10_base146/check.py calculation/neutral_band/agent10_base146/cert_b146.json 1000`, and `c++ -O3 -std=c++17 calculation/neutral_band/agent10_base146/replay.cpp -o /tmp/replay146 && nice -n 10 /tmp/replay146 calculation/neutral_band/agent10_base146/cert_b146.json 20000`.

Scope: finite certificate in **base 146, period 4** only. The result does not imply a base-10 certificate, a proof about 196, or a parameterized infinite family. Local git HTTPS/Lean 4.19.0 and `python3 tools/verify.py --changed` were unavailable; the non-Lean result was published via the connected GitHub Git Data API without claiming repository-wide or Lean verification.
