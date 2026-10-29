# Agent X17: defect-charge selection controls a 4,920-column carry gate

**Label: COMPUTED** for the stated decimal instances and full 20,000-step tests; local carry propagation equation has a PAPER PROOF. **No infinite Lychrel certificate is claimed.**

## The seed family and charge gate

For the 10,001-digit decimal palindrome `P` whose least-significant-first digits are `88283583[min(i,10000-i) mod 8]`, compare the two one-cell perturbed seeds `Q_k=P+10^(5000-k)` with `k=1` and `k=3`. Both are nonpalindromic and differ from the same palindrome in only one off-centre digit. This is **not** a repdigit-zero wall; the common surrounding digits are nonzero and the local carry rules depend on a temporal lattice.

At `t=107`, the pair coefficient word for the palindrome baseline has an extraordinary all-9 corridor extending almost to its most-significant end. What matters is the **incoming carry charge**, not just the existence of this corridor. A one-column pair-sum `q=9` sends `c -> floor((9+c)/10)=c`, so different incoming carry bits persist across thousands of such columns, but equal bits pass harmlessly.

Exact Python bigint data for the first `t=107` upper-side column where the **two pair coefficient words become equal forever toward the high end**:

| perturb | first common column (LSD index) | baseline/perturb carry entering | common 9-run | matched high digits at t=108 | matched low digits at t=109 |
| --- | ---: | --- | ---: | ---: | ---: |
| `k=1` | 5,067 | `0/1` | 4,920 | 60 | 60 |
| `k=3` | 5,071 | `0/0` | 4,916 | 4,978 | 4,977 |

For `k=3`, shifting the seed's perturbation by **two cells** changes a finite carry boundary condition from unequal to equal. It prevents a normally catastrophic, width-spanning discrepancy across the same large neutral-9 channel, without removing the channel. The 15-offset exhaustive *specified* scan `k=1..15` and exact `t=107..109` data are in `charge_gate.csv`. This is a concrete constructive **charge-selection** mechanism, not an inference from appearance or a general all-offset theorem.

## Long-run positive control

For `k=3`, the baseline and perturbed orbits remain equal-length at all 20,001 states `t=0..20000`; each pair of decimal strings agrees in at least **2,151 digits at both ends**, so their exterior pair-sum words are identical there. The baseline supplies a nonpalindromic exterior witness for all `t>=1`, and `Q_3` is nonpalindromic at `t=0`. **Every complete word**, not merely hash/checkpoints, was compared by an independent GMP ordinary-bigint reverse-and-add engine and a separate decimal digit-column engine for 20,000 steps. Final length is **18,316 digits** and final common exterior width is 2,151. For comparison, the same motif with `k=1` loses the exterior witness at step 427 and the baseline/perturbation have different lengths at step 452. No claims about either orbit after the positive horizon.

## Exact scope / soundness

The finite arithmetic identity is universal: for base `b` and coefficient `q in [0,2b-2]`, `floor((q+c)/b)` is independent of input carry `c in {0,1}` except at `q=b-1`, when it equals `c`. Thus **carry equality on entry to an identical coefficient band is a sufficient firewall**, even when that band consists entirely of neutral coefficients and has unbounded length. A potential infinite construction could enforce a finite *carry-charge cancellation* at every recurrent defect-band interface, instead of requiring the band to absorb carries. This current experiment verifies the cancellation only at one specific gate time; global inductive recurrence remains UNDECIDED.

Reproduce exactly with `bash calculation/new_structures/agent-X17/charge_gate_reproduce.sh`. This runs `charge_gate.py` (Python bigint, all 15 offsets), checks stored 15-row data, and independently compares the full 20,001-state orbit for `k=3` using `independent_offset_gmp.cpp` and the previously committed `shadow.cpp`. Requirements: C++17, GMP, Python3. No Lean or repository-wide verifier claim because the full checkout/toolchain was unavailable locally.