# Agent X17: nonlinear double-defect charge cancellation in decimal reverse-and-add

**Label: COMPUTED.** The arithmetic carry-interface lemma below is a PAPER PROOF component; the concrete 20,000-step result is finite only. **No infinite base-10 Lychrel number or closed certificate is claimed.**

## A constructive two-defect effect

Let `P_n` be the `n`-digit base-10 palindrome with least-significant-first digit `a_i = u[min(i,n-1-i) mod 8]`, where `u=88283583`. For odd `n` and a set of offsets `E`, set

`Q_{n,E} = P_n + sum_{k in E} 10^(floor(n/2)-k)`.

All the digits modified in the stated tests are less than 9. For `n=10001`, the **single** defects `E={7}` and `E={8}` each transmit a differential carry through an enormous uniform-9 pair-sum channel at step 107. By step 108, only **60** most-significant-side digits still agree with the palindrome baseline (and by step 109 the low-side common exterior is also 60 digits). In striking contrast, the **combined** seed `E={7,8}` has identical incoming carry bits across the corresponding common channel, and retains **4,971** common high-side digits at step 108, and **4,969** common low-side digits at step 109. These claims concern genuine decimal integer reverse-and-add, not a hypothetical pairword update.

At `t=107`, the first pair column beyond all the differing pair coefficients has the following exact carry-interface values (LSD-first, 0-based columns):

| seed offsets | first common column | carry baseline/perturb | following common-9 run | high matched digits at t=108 |
|---|---:|---|---:|---:|
| `{7}` | 5075 | `0/1` | 4912 | 60 |
| `{8}` | 5075 | `0/1` | 4912 | 60 |
| `{7,8}` | 5079 | `0/0` | 4908 | 4971 |

The **nonlinear superposition** is the new mechanism: *two individually destructive digit defects together suppress the long-range carry avalanche*. An exact Python bigint test repeats the gate calculations for `n=2001,6001,10001`, including the control `{1},{2},{1,2}` (18 cases total). This establishes positive arithmetic controls at these three lengths only; it is not a theorem that all lengths or all two-defect pairs work.

## Independent full-orbit control

For `n=10001, E={7,8}`, the ordinary decimal digit-column engine and an **independently implemented GMP arbitrary-precision reverse-and-add engine** both construct the seed and compare the **entire canonical decimal word of both baseline and perturbed numbers at every state `t=0..20000`** (20,001 full-string comparisons for each trajectory). The two orbits have equal length throughout, no perturbed state is palindromic, and at each state at least **2,154 digits at each exterior end** are identical. For `t>=1` an asymmetric digit pair occurs within that shared exterior, making nonpalindromicity explicit; at `t=0` the perturbation is visibly asymmetric. The final length at step 20,000 is **18,316** digits, and the matched exterior at that step is **2,154** digits. There are 211 synchronized checkpoint rows with length, hashes, and witness index; these checkpoint hashes are *additional* checks and are not substituted for full GMP/digit word equality.

The apparently similar control `E={1,2}` also cancels the initial t107 carry shock, but **does not** survive a comparably long shadow: its first missing external asymmetry witness is t458 and its first differing baseline/perturb digit lengths are t520. This shows plainly why one successful local charge cancellation does not imply an infinite certificate.

## Exact carry algebra and certificate direction

Let `s_i=d_i+d_{L-1-i}` be pair coefficients of a canonical length-`L` decimal number. Its next digits are `(s_i+c_i) mod 10`, with `c_0=0` and `c_{i+1}=floor((s_i+c_i)/10)`. The outgoing carry is independent of incoming bit `c_i` unless `s_i=9`; for `s_i=9`, `c_{i+1}=c_i`. Therefore a channel of 9s *transmits* any differential carry for arbitrary length, but a finite defect interface that produces **equal incoming bits** automatically prevents differential-carry propagation regardless of the channel's length. This is an exact local PAPER PROOF, not an empirical extrapolation. An infinite certificate would still need to prove recurring charge cancellation, retention of an asymmetry witness, and a closed transition law; none is established here.

## Reproduce and scope

From repository root: `bash calculation/new_structures/agent-X17/pair_gate_reproduce.sh`. Inputs include `pair_gate.py` and the 18-row `pair_gate.csv` for exact bigints, `shadow_pair.cpp` for digit-column replay, `independent_pair_gmp.cpp` for independent GMP arithmetic, and `pair78_checkpoints.csv` for 211 replay rows. The runner also confirms both destructive single-defect controls and the distinct `{1,2}` finite failure. Requirements: `python3`, `g++ -std=c++17`, `gmpxx`, `gmp`. Local regression PASS; no Lean or repo-wide `tools/verify.py --changed` claim because the full checkout and Lean toolchain were not available locally.