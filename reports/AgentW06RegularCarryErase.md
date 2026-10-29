# Agent W06: a regular carry-erasure language with 256^M decimal seeds

Status: **PAPER PROOF** for the universal synchronization; **COMPUTED** for precisely the finite 20,000-step decimal orbits below. Neither is an infinite Lychrel certificate, a regenerative lattice interface, or Lean verification.

## Explicit decimal family

All symmetric pairword coefficients are low-digit-first, P[i]=d[i]+d[n-1-i], in 0..18. From the existing p8/m20 rec0 exterior:

B = [17,5,0,1,13,4,14,12,9,8,15,16,17,13,17,9,1,4,4,11,8,16,0,9,14,11,9,11,6,13,18,9,4,7,17,15,9,7,13]

W = [17,3,1,13,17,11,14,3,18,1,2,0,7,3,14,12,15,9,7,13]

For every 8-bit mask a, define W[a] by independently toggling the following eight cells:

| site j | original | alternate |
|---:|---:|---:|
| 1 | 3 | 12 |
| 3 | 13 | 4 |
| 5 | 11 | 2 |
| 7 | 3 | 12 |
| 9 | 1 | 10 |
| 12 | 7 | 16 |
| 14 | 14 | 5 |
| 19 | 13 | 4 |

For every M>=1, masks a[0]..a[M-1], and even C in {0,2,...,18}, let

    H = B ++ W[a[0]] ++ ... ++ W[a[M-1]]
    P = H ++ [C] ++ reverse(H).

Realize P as a canonical decimal integer by splitting its symmetric coefficient p into digits (min(9,p), p-min(9,p)) and using centre digit C/2. The integer is well defined with exactly 2(39+20M)+1 digits, because the leading and trailing coefficients B[0]=17 yield nonzero end digits. Distinct masks give distinct pairwords and integers, hence exactly 256^M distinct seeds per M,C.

## Theorem: all masks completely synchronize (PAPER PROOF)

For fixed M and C, the **complete pairword after one actual reverse-add step is identical** for all 256^M seeds. Their **complete integers after two reverse-add steps are identical**. This holds for every M without a size bound.

Let P0 use the unmodified W in every block; Pa use arbitrary masks. Let n be the odd common coefficient length, x=39+20r+j a toggled lower-half site, and y=n-1-x its reflected mate. The coefficient changes at x and y by the same delta, either +9 or -9. By the explicit list, the original coefficient and its alternate are one in {1,...,8} and one in {10,...,17}; each changed cell flips its outgoing carry by exactly one for either possible incoming carry. Every successor coefficient along the low-to-high normalization scan is different from 9, so the changed carry merges after exactly one more cell. At the closest-to-centre site j=19, the successor is the centre C, which is even and thus different from 9. At all mirrored sites the next coefficient is W[j-1], also different from 9.

Selected sites are at least two positions apart even across the 20-cell period boundary. Consequently the carry disturbances never overlap. By direct two-cell base-10 arithmetic, each coefficient change of +9 adds digit differences -1 at x and y and +1 at x+1 and y+1, with the signs reversed for a -9 change. Thus, for every combination of mask bits, the normalized decimal digit words of the first iterates differ by precisely the **sum of these disjoint four-position impulse patterns**, and nowhere else. Both ordinary decimal outputs have length n+1 because the unchanged suffix reverse(B) exits with carry 1.

The mirror partner in a length-(n+1) result is index n-i. In particular, x is paired with y+1 and x+1 is paired with y. The two digit differences cancel in each mirrored pair, for each toggle separately. Thus the full symmetric pairwords of the first iterates are equal, including every central and boundary cell. Reverse-add of an integer depends only on its mirrored pairword, therefore the second iterates are literally equal. No empirical recurrence assumption enters this proof.

At t=0 each seed is nonpalindromic because B[0]=17 is odd. At t=1 all seeds have the same pairword, whose coefficient at index 1 is 13 (the rec0 temporal phase-1 root), also odd. Since a palindrome has all pair coefficients even, these two states are nonpalindromic independently of the later common orbit.

## A computed 20,000-step family with 2^2560 members

Choose M=320 and centre C=18. Then there are 2^2560 different **12,879-digit** seeds, all of whose actual reverse-add orbits are identical starting at step 2. The baseline seed was independently replayed for 20,000 true decimal additions by (a) a C++ digit-vector schoolbook implementation and (b) GMP mpz_class with literal canonical decimal-string reversal. Each independently finds zero palindromes at all 20,001 states t=0..20000 and zero violations of the alternating length increment 10101010. The schoolbook version separately checks the full temporal 39-coefficient root plus 256 period-20 lattice coefficients at every one of those 20,001 steps, zero mismatches. The GMP version independently realizes one deterministic nonzero 8M-bit mask (bit j of block r is toggled iff (17r+13j) mod 3 = 0), verifies that its N0 and N1 differ from the baseline, and that N2 agrees exactly.

Both ordinary-number replays agree on the full-string MSD-first ASCII FNV-1a 64-bit fingerprints, offset 1469598103934665603 and multiplier 1099511628211:

| t | canonical decimal digits | full-digit FNV64 |
|---:|---:|---|
| 0 | 12879 | efda6892a65f9ae8 |
| 1 | 12880 | 9fb829784146db11 |
| 2 | 12880 | 6d81c163a078f36d |
| 20000 | 22879 | 3bba2a5955eee568 |

The all-M paper proof plus the first-two-step parity guards then imply **every one** of those 2^2560 seeds has no palindrome for t=0..20000, not that any avoids palindromes forever.

## Exact reproduction

From repository root, run the following commands, independently:

    python3 calculation/new_structures/agent-W06/toggle_family.py
    g++ -O3 -std=c++17 calculation/new_structures/agent-W06/toggle_schoolbook.cpp -o /tmp/w06tbook
    /tmp/w06tbook 320 20000
    g++ -O3 -std=c++17 calculation/new_structures/agent-W06/toggle_gmp.cpp -lgmpxx -lgmp -o /tmp/w06tgmp
    /tmp/w06tgmp 320 20000

The Python checker exhausts all 256 one-block masks times the ten even central coefficients (2,560 distinct cases); then checks 500 seeded arbitrary multi-block masks (M up to 500), including **90** separate paired ordinary Python-bigint replay controls. It directly verifies each predicted digit impulse, the complete next-pairword equality and the actual second integer identity. An intentionally invalid adjacent toggle pair (sites 7 and 8, where site 8 is *not* among the eight permitted sites) fails the first-pairword equality, providing a mutation negative control. All compact fingerprints and the explicit toggle table are in calculation/new_structures/agent-W06/toggle_observations.json.

## Still open

The lattice wall still moves **inward** (about ten spatial cells per 44 steps). The regular family is a useful exact many-to-one carry-erasure quotient, but an infinite certificate still needs an unbounded or regenerative pumpable centre/interface closed under the full decimal dynamics and equipped with a nonpalindrome guard. The current proof does not supply such a closed macroedge, so a decimal Lychrel number remains unproved.
