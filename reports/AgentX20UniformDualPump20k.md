# X20: independent two-cut pumping through 20,000 real decimal steps

**Result label: COMPUTED** for the exhaustively checked finite horizon; **PAPER PROOF** for the elementary localized absorbing-carry pumping lemma. This is a uniform finite-horizon result, **not** an infinite Lychrel certificate and not Lean-verified.

## The exact family

Let `B,W,V` be the period-20/period-48 decimal coefficient arrays in `calculation/new_structures/agent-X20/two_counter.cpp`. All coefficient words below are least significant first and coefficient entries may be as large as 18. Define

`H(m,n) = B ++ W^m ++ [9] ++ V^n`,
`P0(m,n) = H(m,n) ++ [9] ++ reverse(H(m,n))`,
`N0(m,n) = val_10(P0(m,n))`.

The theorem covers **every** integer pair `(m,n)` in the union of two northeast quadrants:

- `m >= 427` and `n >= 509`;
- `m >= 509` and `n >= 427`.

Let the two real baseline pairword trajectories be `P_t^A=P_t(427,509)` and `P_t^B=P_t(509,427)`, including t=0 as the initial palindrome-symmetric coefficient word and t>=1 as the actual pairword of the preceding ordinary decimal integer. Both baseline decimal integers were independently replayed for 20,000 additions using decimal digit-array arithmetic and a **different** base-10^9 limb implementation, with complete numerical equality at every step and no palindrome (`results/AgentX20IndependentDualCounter.md`).

At each t define `I_W,t` as insertion of one period-20 bulk word `W_t` at zero-based low-half coefficient position `x_W=39+600=639`, and simultaneous insertion of the reflected reversed word at the symmetric high-half cut. Define `I_V,t` similarly for the period-48 word `V_t` at `x_V=39+20m0+1+15168`, where m0 is the baseline's first counter. The low-half index of the V cut shifts by +20 for each prior W insertion, as dictated by ordinary concatenation. Both cuts are chosen at integer multiples of their respective periods deep inside two exact periodic regions, leaving at least two complete periods on either side. The insertion operations are well-defined on whole palindrome-symmetric coefficient words; they commute when their shifted cut coordinates are interpreted consistently.

For all `0<=t<=20000`, `r,s>=0`, the asserted exact full-word identity is

`P_t(m0+r,n0+s) = I_W,t^r I_V,t^s (P_t(m0,n0))`.

This statement is **finite in time but unbounded in both independent parameters**. The low exterior stays unchanged under either insertion, so the nonpalindromicity witness persists in all two-parameter instances.

## Sound one-step pump lemma (PAPER PROOF)

For a palindrome-symmetric pair-coefficient word P, let D=norm(P) be its genuine base-b digits with the usual carry array c and final overflow gamma. Suppose around one mirrored pair of cuts there are complete copies of a spatial-period-m word U in the source coefficient word, and both cut carries satisfy `f_U(c_low)=c_low`, `f_reverse(U)(c_high)=c_high`, where f is the carry-output map for the entire block. Suppose the updated paired output near the cut is again a period-m word U' and a one-copy insertion has been verified to give `F(I_U(P))=I_U'(F(P))` with the same overflow. Here F(P) is `pair(norm(P))`, with `gamma` included when choosing the reflected partner.

Then **any number** of insertions of U at that exact phase have the same property. For each additional copy, the carry to its right equals its incoming fixed point, so no digit outside the inserted block changes; the high mirror satisfies the corresponding reversed-block fixed point. The added normalized digits are the same period-m words for every copy; the only new coefficient letters are the same local pair sums with the same gamma shift. After insertion, the original two-sided periodic neighborhood still exists with the same phase, and the hypotheses remain true. Induction on copies proves `F(I_U^r(P))=I_U'^r(F(P))`. For two spatially disjoint insertion sites, do the same separately: the outer insertion shifts the inner cut by an integer period but neither destroys the other's fixed carry or periodic surroundings, so the insertions commute and the two exponent updates are **independent**. This is a local proof, not extrapolation from large sampled r,s.

The calculation makes every premise explicit and fail-closed, including a full-word check for each one-copy commutation. The theorem makes no claim when a cut is in a neutral or non-stationary carry band, when guard windows fail, or when the one-copy identity is false.

## Finite arithmetic tests and no-palindrome induction

`pump_guard20k.cpp` replays genuine decimal arithmetic from the baseline seed. For **each t=0..20,000** (20,001 successive one-step tests per baseline), it checks:

1. P is symmetric; actual coefficient normalization matches the decimal digits and their overflow, using the baseline tested engine.
2. The two low insertion neighborhoods agree with their exact current W_t and V_t words for two full periods in both directions. Symmetry supplies the mirrored high-side pattern.
3. The carried low-cut and high-cut states are fixed by their respective forward/reversed periodic words, independently for W and V.
4. The complete exact identities `F(I_W(P_t))=I_W'(F(P_t))`, `F(I_V(P_t))=I_V'(F(P_t))`, and `F(I_W I_V(P_t))=I_W' I_V'(F(P_t))` hold. This is **three whole-word comparisons** at every step, rather than only eight phases or a handful of widths.
5. One odd coefficient occurs within the first eight positions of every relevant P_(t+1). Such an odd coefficient cannot arise as the sum of two equal opposing decimal digits, so the corresponding N_t is not a palindrome. Insertions occur far beyond the first 39 positions and preserve this witness.

Both baselines pass 20,001 x 3 = 60,003 full-word comparisons each, total **120,006** tested identities. For resource-limited executions, the same code accepts a `start` parameter to skip only the expensive insertion comparisons for earlier t, while still replaying all intermediate base arithmetic and validating all carry and periodic guards. Running `[0,10000)` and `[10000,20001)` checks every intended edge without gaps. Both baseline parameter pairs pass the complete split run, with the two tested intervals covering all 20,001 transitions without gaps.

For each baseline, the independently verified 20k final decimal length and least-significant-first FNV-1a 64-bit hash are:

| (m0,n0) | digits at t=20k | FNV64 |
|---|---:|---|
| (427,509) | 76,026 | `fd9b296c175cbcce` |
| (509,427) | 71,434 | `29d9fb65743a3d46` |

Independent Python built-in arbitrary-precision `int` checks (64 ordinary additions, zero palindromes) additionally passed `(428,509)`, `(427,510)`, `(428,510)`, `(510,427)`, `(509,428)`; this code uses the separate `spotcheck.py` from the first result. These are controls, **not** the proof of all parameter counts.

## Reproduction

```sh
# From repository root
g++ -O3 -std=c++17 calculation/new_structures/agent-X20/pump_guard20k.cpp -o /tmp/x20pump
/tmp/x20pump 427 509 10000 0
/tmp/x20pump 427 509 20001 10000
/tmp/x20pump 509 427 10000 0
/tmp/x20pump 509 427 20001 10000
# Independent baseline integer replays (both must pass):
g++ -O3 -std=c++17 calculation/new_structures/agent-X20/asymmetric20k.cpp -o /tmp/x20_big
/tmp/x20_big 427 509 20000
/tmp/x20_big 509 427 20000
```

No Lean/kernel verification or global `tools/verify.py --changed` is asserted (full git checkout unavailable in this execution environment). The result does not establish an infinite decimal Lychrel orbit, a closed template cycle, or anything specifically about 196. The next target is to make the **base trajectories themselves** renormalize, replacing the 20k finite time horizon with a finite macrocycle of the guarded-centre dynamics.
