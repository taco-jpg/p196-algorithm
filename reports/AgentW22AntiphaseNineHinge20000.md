# Agent W22: antipodal six-clock carry hinge

**COMPUTED:** explicit decimal 20,000-step pairword and nonpalindrome replay. **PAPER PROOF:** the local carry-hinge identity below. **UNDECIDED:** infinite centre/resource renewal. NOT a decimal Lychrel certificate; not Lean-verified.

## Seed and phase clocks

Pair coefficients are always 0..18 (19/20 can only be intermediate unnormalized sums). All words are least-significant-first coefficients. Define A=(8,16,14,10,2,4), B=(10,2,4,8,16,14)=A rotated by 3. Initial symmetric pairword:
P0 = 8^14000 ++ 9^8000 ++ 10^16000 ++ 9^8000 ++ 8^14000.
To realize it as a true 60,000-digit positive integer, each mirrored coefficient p is split into low=min(p,9) and high=p-low, except p0=8 uses low=0, high=8, so the leading digit is nonzero. The subsequent pairword depends only on P0, regardless of this valid split.

## Exact local mechanism (PAPER PROOF)

For a long homogeneous pairword segment x != 9, where x is one of the six bulk coefficients, the first cell forces the carry k(x)=1 if x>=10, else 0. Every later normalized digit in this bulk is x-9k(x), so the interior next pair coefficient equals 2(x-9k(x)). These are exactly the six-clock transitions:
8 -> 16 -> 14 -> 10 -> 2 -> 4 -> 8.
For every phase t, k(A_t)+k(B_t)=1. A run of coefficient 9 transmits its entering carry unmodified. Two mirror-related normalized interior 9 cells are 9-9k(A_t) and 9-9k(B_t); their sum is exactly 9. The identity holds with overflow 0 or 1 as long as both partners stay in their respective homogeneous interiors. Both antipodal clocks progress synchronously; **this only proves the interior identity, not preservation of finite seam boundaries**.
The same-phase controls A=B=8 and A=B=16 immediately turn the 9 corridor into 18 or 0, respectively. Six one-step antipodal checks and 48 full pairword transitions pass in unit.py.

## Full ordinary-integer replay

hinge_fast.cpp independently computes schoolbook digit-list reverse-and-add AND a carry-normalized full pairword. Every one of the 20,001 integer states is compared against the complete pairword; each state is nonpalindromic and has first-half runs in the exact order A,9,B with minimum widths 654,1198,1344. The odd coefficient 9 itself excludes palindromicity because a palindrome has even paired digit sums.

hinge_gmp_fast.cpp independently accumulates GMP mpz_class integer additions using reversed decimal operands, checks against a second independently coded schoolbook digit stream at steps 1..4 and every 100 steps including step 20000, and yields byte-for-byte the same final integer as the first checker. This is a 20,000-step GMP accumulator; the reversed operand is built from the concurrent digit stream rather than GMP-to-string on every step, and full numerical agreement is explicitly checked at 100-step intervals. This distinction is intentional.

Initial digits 60,000; final digits 68,296; exactly 8,296 overflows. SHA-256 of the newline-free final decimal integer: 8e111023c78fad5fa2606faf67db5203e2d578964b1ba29b5046f93fa52ccafc.

| time | length | cumulative overflow | A half-run | 9 half-run | B half-run | each seam defect |
|---:|---:|---:|---:|---:|---:|---:|
| 0 | 60000 | 0 | 14000 | 8000 | 8000 | 0 |
| 1000 | 60408 | 408 | 13340 | 7664 | 7672 | 496 |
| 5000 | 62063 | 2063 | 10651 | 6297 | 6333 | 2518 |
| 10000 | 64120 | 4120 | 7309 | 4596 | 4665 | 5037 |
| 15000 | 66203 | 6203 | 3971 | 2913 | 3007 | 7536 |
| 20000 | 68296 | 8296 | 654 | 1198 | 1344 | 10057 |

Both seam-defect gaps widen continuously in the macroscopic sense; the protected A/9/B resources all shrink. An earlier (A,L,C)=(4500,5000,7000) test lost its macroscopic 9 run by t=15000. This explicitly redirects construction to an emitter that renews the opposite-phase carry states and neutral 9 supply, rather than claiming a stationary bounded kink. No indefinite orbit follows from the 20k computation.

## Reproduce

Run from repository root: sh calculation/new_structures/agent-W22/reproduce.sh. Requires Python3, g++ C++17, GMP. This runs six antiphase controls, two same-phase destruction controls, 48 transitions, independently executes the complete 20,000-step schoolbook/pairword and GMP/digit-vector replays, checks byte-for-byte final integer agreement, and prints SHA-256 and shape minima.
