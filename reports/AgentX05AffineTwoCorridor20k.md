# Agent X05: two independently sized decimal carry corridors, 20,000 steps

**Status: COMPUTED.** Extends `AgentX05AffineTwoCorridor` from 2,000 to 20,000 decimal reverse-and-add steps, with an **independent complete GMP ordinary-integer replay** through all 20,000 steps. The exact symbolic result is uniform for **every pair of independently chosen integers `A>=20000`, `B>=20000`**, with no coupling such as `A=B`.

## Explicit candidate and scope

Take the symmetric pair-coefficient word, least significant first:

`P_0(A,B) = 9^(A+1) ++ [18,18] ++ 9^B ++ [0,0] ++ 9^B ++ [18,18] ++ 9^(A+1)`,

and `N_0(A,B) = val_10(P_0(A,B))`, an ordinary decimal integer. Symbolic coefficients (0..18) are **not decimal digits**. For `T(P) = pairs(digits_10(val_10(P)))`, the new C++ affine-RLE engine computes the exact `T^t(P_0(A,B))`, with every digit normalization, leading-zero trim and reversed-end alignment justified by affine inequalities valid throughout the entire independent two-parameter orthant. For every `t=0..19999`, `digits_10(val_10(T^t(P_0(A,B))))` has at least one unequal mirrored pair. By induction for the **stated finite horizon**, no palindrome is encountered at any of those times for any permitted A,B. Step 20,000 itself is constructed as a complete pairword, but nonpalindromicity at time 20,000 is not asserted by the 20,000 predecessor checks.

The engine aborts if (i) a symbolic run could be nonpositive, (ii) a length comparison depends on A or B, or (iii) a palindrome arises. It does not truncate runs or rely on a sample grid. The generic affine-RLE soundness argument and proposed infinite-cycle criterion are in `reports/AgentX05AffineTwoCorridor.md`. This extension is **not** a discovered finite cycle, infinite Lychrel number, result about 196, or Lean-verified theorem.

## Independent ordinary-arithmetic check

A standalone GMP-backed ordinary decimal integer is initialized from the actual canonical decimal digits of `N_0(20000,20017)`. On each of 20,000 steps, the code converts it to a full decimal digit string, rejects if this string equals its reverse, compares it byte-for-byte to the expanded and independently carry-normalized affine-RLE pairword, then performs `n <- n + reverse_decimal(n)` using GMP. Every comparison passed. Checkpointed segments are 3,000,3,000,3,000,3,000,3,000,3,000,2,000 steps, linked by full decimal GMP state and complete symbolic RLE; every resumed segment rechecks the initial state. The complete decimal integer has **88,291 digits after step 20,000**, with SHA-256 digest `9891c73bc276927b598a629c0f9ae458e3def1bfc5ee24f80dad7ad8edc733e0` on its most-significant-first decimal representation.

At `t=20000`, there are **51,821** RLE terms and the symmetric pair-coefficient word has **88,256** entries for A=B=20000. It still contains **four distinct, independently parametrized 0-runs**: two with length `A-12048`, and two with length `B-12070`; at the minimum allowed parameters, their lengths are respectively 7,952 and 7,930. The surviving pumped corridors have **changed from coefficient 9 to absorbing coefficient 0**; they are not neutral all along. The junction regions have developed thousands of finite coefficients. This demonstrates a two-counter *moving interface* format rather than a static short centre. The remaining long corridors have negative length drift, so the next construction should investigate **regenerative zero-to-neutral boundary gates or a domain reset**, not merely lengthening the initial neutral 9 band.

## Reproduction and limitations

Run `bash calculation/new_structures/agent-X05/replay20k.sh` from repository root (requires C++17, GMP headers, GMP and GMPXX libraries, and Python3). It compiles `affine_rle_fast.cpp`, separately checks the entire 20,000-step all-parameter symbolic run, repeats the GMP 20,000-step decimal orbit with full pairword comparisons and validates every checkpoint's SHA-256 against `evidence20k.json`. All compressed evidence, checkpoint metadata, orbit-length milestones, and long-corridor lengths are in `calculation/new_structures/agent-X05/evidence20k.json`. The 500-KB checkpoint intermediates are intentionally **not** committed. Independently, the earlier Python `affine_rle.py` matches the C++ engine's first 2,000-step final length and RLE size, and `independent.py` reproduces the first 1,200 big-integer steps for a smaller initial family.

**Finite-horizon only.** No argument presently rules out a palindrome after step 20,000. A finite coefficient run shrinking by roughly 0.60 positions per step cannot by itself serve as an absorbing infinite-time proof. The next mathematical task is a *true regenerative transition*, or a closed affine-RLE phase graph with verified counter nondecrease, not a claim that the observed finite orbit already repeats.
