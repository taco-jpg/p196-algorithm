# W04: exact twelve-step base-10 transfer of carry-resource between two independent bands

**PAPER PROOF** (unbounded independent band lengths for a *finite 12-step recurrence* and full twelve-edge carry-pumping soundness). **PAPER PROOF conditional on fully checked finite trace** (a 20,000-step nonpalindrome family). **COMPUTED** (two independent, 20,000-step ordinary integer implementations and all controls). **UNDECIDED** for indefinite avoidance: no infinite decimal Lychrel certificate, no Lean claim.

## Explicit positive source and two exact images

Let `m,n>=10` be completely independent. Define the folded even palindromic pairword in least-significant-first coefficient order as

    H0(m,n) = [11,9,8,17] ++ 8^m ++ [9,16,7,8,8] ++ 16^n ++ [8].

The full pairword is `H0++reverse(H0)`. It is realized by a **genuine positive decimal integer** with each high-side decimal digit `min(9,p)` and its reflected low-side decimal digit `p-min(9,p)`; the most significant decimal digit is 9 and all coefficients are in 0..18. The fixed odd coefficients ensure nonpalindromicity. All arithmetic from here uses actual `N -> N+reverse_digits(N)`.

Two entirely *literal* universal equalities, verified by an exact twelve-edge carry certificate, are:

    H6(m,n) = [15,6,17] ++ 8^(m+1) ++ [14,12,4,10,8,8] ++ 16^n ++ [8]

    H12(m,n) = [8,16,14,13,10,7] ++ 8^m ++ [11,8,1,8] ++ 16^(n+1) ++ [12,8].

Thus the **first** six-step block grows the first repeated 8-band by one and leaves the second 16-band unchanged; the **second** six-step block gives back the first-band credit and adds **one** 16-band cell. Both literal bulk runs are nonshrinking over the full twelve-step block: `(m,n)->(m,n+1)`. The centre/interfacial words in the two displays differ and cannot be silently identified as the same state; we are NOT asserting a repeatable positive-drift 12-step cycle. This resource transfer is distinct from the first W04 rebound (`AgentW04PositiveRebound`, which had +1,+1 at t6 but (-3,-2) at t12), and does not just rename an initial 8 or 16 that was already part of an adjacent repeated run.

The twelve overflow bits are **`100010101001`** and the pairword parities at t=0..12 are `0,1,1,1,1,0,0,1,1,0,0,0,1`. Every one of the thirteen source/target phases is an explicit cylinder

    H_t(m,n) = L_t ++ x_t^(m+a_t) ++ J_t ++ y_t^(n+b_t) ++ R_t,

where `x_t=(8,16,14,10,2,4)[t mod 6]`, `y_t=(16,14,10,2,4,8)[t mod 6]`, and all the complete `L_t,J_t,R_t,a_t,b_t` objects (including both central parities and every overflow flag) are in `length12_witness.json`. The constant prefix/junction/suffix includes an odd pair coefficient in every phase, independently of the values of m,n. `length12_pdr.py` recomputes and asserts all those concrete words using ordinary column carries; they are not merely pattern matches in a finite orbit.

## Finite two-port carry certificate and soundness for every m,n>=10

A two-ended folded-normalization carry transducer has the finite complete state `(a,z,h)`, where `a` is the low incoming carry, `z` is the high outgoing carry, and `h` is the previously normalized high decimal digit. For each paired source column p, guess high incoming carry r and impose

    z=floor((p+r)/10),
    a'=floor((p+a)/10), z'=r, h'=(p+r)%10.

It emits low digit `(p+a)%10` plus either current high digit `h'` without overflow or the previously processed high digit `h` in overflow mode (and the new leading overflow digit 1 for the first column). At the centre, the low/high carries must meet and satisfy the exact odd/even terminal constraint. This is a direct, exact reformulation of ordinary decimal normalization. For each of the twelve actual transitions, `length12_pdr.py` checks the whole accepting path at m=n=10 and its exact target; in *each* of the two aligned repeated bands it finds one column whose full three-component state is unchanged before/after the column. The 24 independently pumpable self-loops, including their source and target letter and complete state tuple, are encoded as immutable evidence in `length12_witness.json`; all are recomputed and compared by the checker. A mutated carry state is rejected.

Inserting q>=0 extra copies of the first self-loop and r>=0 of the second gives the precise source and target cylinder with **m=10+q, n=10+r**. Each inserted loop preserves the entire finite carry state, so the boundary and central equations stay valid, the loops remain disjoint, and the exact accepted path persists under two **independent** elongations. Decimal normalization is deterministic and its physical output is exactly the accepted target. Consequently every one of the twelve edges holds for ALL independent m,n>=10, with no synchronizing equality. Induction gives the two displayed identities for t6 and t12. An additional independent Python arbitrary-precision decimal big-integer oracle reproduces all 13 phase pairwords and no palindromes for 99 chosen independent positive seeds (including strongly off-diagonal widths).

This is a genuine finite universal **positive resource-transfer tile**, not a 12-step return in a finite graph of identical interfaces. The finite-state proof method is the same sound two-port-loop calculus as our first two-counter rectangular report, but the pairword source, target, step count and **nonnegative counter update** are new. The earlier N19 six-phase diagonal ray reduced its band widths; this transfers a unit of slack to the other resource over two six-step blocks.

## Exact failure to become infinite

The interface at t12 is `[8,16,14,13,10,7] / [11,8,1,8] / [12,8]`, not the original `[11,9,8,17] / [9,16,7,8,8] / [8]`. The 12-step positive drift cannot be repeated by fiat. Direct ordinary pairword replay at m=n=100 reports bulk run pairs at checkpoints:

| step | first 8-band | second 16-band |
|---:|---:|---:|
| 0 | 100 | 100 |
| 6 | 101 | 100 |
| 12 | 100 | 101 |
| 18 | 96 | 98 |
| 24 | 91 | 95 |

The transformation after 12 steps is transient: by step 18 both run widths are strictly below their initial lengths. This finite observation does not exclude some entirely different interface from restoring the source, and it does **not** imply anything about a palindrome after step 20000. The next constructive synthesis task is a graph of separately pumpable interfaces whose affine **cycle** (not a single edge) has a nonnegative two-counter drift and permanently odd fixed coefficient.

## A further 20,000-step rectangular consequence

The one actual diagonal reference at m=n=15000 is advanced by `length12_20k.cpp` using ordinary decimal digit arrays and **actual decimal addition** for 20,000 transitions, checking at each edge two disjoint state-self-loops within the aligned uniform bulk runs. It also checks a nonzero odd pair coefficient in every state and no palindromes. Minimum overlapping pumpable lengths over 20,000 edges: **1739 and 1816**, minimum number of odd pair coefficients: **2**. These are fully recorded as fail-closed machine checks rather than assumed bounded-difference propagation.

Extending the two disjoint loops by arbitrary q,r>=0 independently at **every** reference edge proves by induction that for all independent m,n>=15000 the complete folded pairwords through t=20000 equal the actual diagonal reference word extended in the two distinguished runs. All inserted letters in every phase are even, so the fixed odd pairword witness is unaffected, giving a **finite-horizon PAPER PROOF conditioned on that complete COMPUTED trace** that every corresponding ordinary integer is nonpalindromic for all 20001 states. This is **not** an unbounded-time induction; both physical bands later erode, and no time beyond 20000 is claimed.

The off-diagonal seed `(m,n)=(15000,16000)` is independently replayed through all 20000 transitions by two entirely different ordinary-number arithmetic kernels:

- `length12_20k.cpp`: full decimal byte digits plus schoolbook one-digit carry, with pairword checks used only *after* genuine integer arithmetic.
- `length12_limbs.cpp`: independent base-10^9 arbitrary-precision integer limbs with 64-bit carry, decimal string reverse, and parse back to 9-digit limbs. Does not call the decimal digit engine or transition on pairwords.

They agree on ALL 20001 length-and-band trace records as a running digest, and five complete-number FNV64 fingerprints:

| t | decimal digits | first band | second band | full-number FNV64 |
|---:|---:|---:|---:|---|
| 0 | 62,020 | 15,000 | 16,000 | `da1854851042db96` |
| 5,000 | 64,083 | 11,685 | 12,739 | `fffb1f159d616fae` |
| 10,000 | 66,129 | 8,408 | 9,469 | `544e86e10224c287` |
| 15,000 | 68,223 | 5,055 | 6,137 | `295d5ea734db6b9b` |
| 20,000 | 70,313 | 1,739 | 2,816 | `8707e338ab7d46e2` |

Final metadata trace digest: **`d05d7af6a51858bc`**. Separate diagonal all-edge witness: m=n=15000, final 68,313 decimal digits, full FNV64 `a98c6cfb2d9cb132`, minimum pumpable overlaps 1739/1816. Fingerprints and controls are in `length12_checkpoints.json`. The runner compares both independent engines against all exact checkpoints and refuses a deliberately corrupted expected fingerprint.

### Exact reproduction

    bash calculation/new_structures/agent-W04/run_length12.sh

Requires standard Python 3 and a C++17 compiler, no external libraries or internet access. It regenerates/validates every exact transducer loop and phase, runs 99 independent big-int small controls, checks 12 exact universal parameterized steps, replays diagonal and off-diagonal ordinary decimal integer trajectories for 20000 steps, checks the independent 9-digit-limb kernel, five physical full-number fingerprints and a negative corrupted-checkpoint control. Successful exit prints `AGENT_W04_LENGTH12_ALL_CHECKS_PASSED`. Full sources, small witness/checkpoint JSON and independent oracles are in the same result commit, entirely under `calculation/new_structures/agent-W04/`. Repository-wide `verify.py --changed` and Lean were not available to run from this sandbox; no such check is asserted.