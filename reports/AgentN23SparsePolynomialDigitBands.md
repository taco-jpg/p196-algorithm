# Agent N23: sparse-polynomial affine-band digit certificates

**Scope: COMPUTED finite certificate identities + PAPER algebraic soundness mechanism; NOT Lean verified, NOT a decimal Lychrel proof.** The known base-9 cycle is a positive control, not a novel base-9 existence claim.

## Format and soundness

Write each number as a least-significant-first digit word whose pieces are finite literals U and repeated motifs V^(a q+c), where a,c are nonnegative integers, q>=q0, and the final digit is nonzero. All motif lengths and slopes are fixed, but different bands may have different slopes. Let b be the arithmetic base. Put Z=b^q. For a motif V of m digits at offset s q+t, its exact value is

    b^t Z^s val_b(V) * (b^(m c) Z^(m a) - 1)/(b^m - 1).

Literal pieces also contribute monomials in Z. Hence the entire integer value N(q) is a sparse polynomial over Q in Z, irrespective of carries, band lengths, or the number of bands. Its digit reversal R(N(q)) is another such expression: reverse the order of pieces and reverse the digits within each piece. For b=10^k, reverse the k *decimal* digits in every radix-b block as well, i.e. rho_k(d)=reverse_k_digits(d), provided the high block always has k significant decimal digits. This is crucial: ordinary base-100 digit reversal is not decimal reversal.

For a phase transition T_i(q) -> T_j(q+delta), compute and compare all rational coefficients of

    N_i(Z) + R_decimal(N_i)(Z) - N_j(b^delta Z).

Zero coefficients prove equality for EVERY q>=q0, not merely for a finite sample. The checker normalizes fractions exactly. For palindrome avoidance, compute nonzero rational polynomial N_i(Z)-R(N_i)(Z), multiply by common denominators, divide out the least power Z^v, obtaining an integer polynomial with nonzero constant C. Any positive integer root must divide C (integer-root theorem). Checking only integer q>=q0 with b^q<=|C| decides palindrome avoidance for ALL q>=q0. If each closed edge holds, each phase is nonpalindromic, all high blocks are valid, and the final phase maps to the first with q gain >=0, induction yields a never-palindromic orbit. This is a mathematically sound format; the present checks are Python exact-arithmetic computations, NOT kernel-verified.

## Positive control in base 9

The existing base-9 lattice source B0 of length 61, motif [1,1,15,15], and original symmetric-pair split yield genuine digit words. The deterministic generator runs ordinary base-9 reverse-add independently for q=2..6, mines twenty digit-phase templates, each U ++ (V^2q) ++ W, and returns to phase one with q+1. The separate sparse-polynomial checker proves all twenty digit identities and nonpalindromes for EVERY q>=2. The C++ digit-list implementation, independent of Python and using only carries, confirms 20,000 successive steps and exact digit-word matching at every step: initial 141 digits, final **8141 digits**, q=1002. This is a new computational presentation of the known base-9 example, not a new base-9 mathematical discovery.

## Decimal cross-radix mechanism

With two-digit groups (b=100), let the initial real decimal number be N_0(q)=12 (99)^(q+2) 34 for q>=0. Group-digit words are LSB-first.

    [34] [99]^(q+2) [12]
      -> [55,98] [99]^(q+1) [56]
      -> [20,98] [99]^q [89,12,1].

Both arrows are verified by exact polynomial coefficients with internal two-digit reversal, for ALL q>=0. Independent decimal big integers check q=0..1000; 3000 randomized block-reversal identities agree with ordinary decimal reversal. The last word has high group 1, whose decimal representation uses only one digit. Its leading decimal digit is 1, trailing digit 0, so it is not palindromic, but the next step would require shifted two-digit block alignment. This is a CONSTRUCTIVE two-step mechanism and a precise next format extension: carry a block-alignment phase h mod k and reblock the reversed word accordingly, rather than treating base 10 and base 100 as ordinary reversal-conjugate.

## Reproduction and limitations

Run from repository root:

    bash calculation/new_structures/agent-N23/reproduce.sh

All checker/source/independent arithmetic control files are in calculation/new_structures/agent-N23/. The deterministic generated base-9 JSON and C++ text signatures are SHA-256 1b643c058c5ae26d1a1851a69f513988f9b5e27727be0e8b5a6e7f45a5c243d7 and 57b40746c09f824a7e1c1a44bf2cf7eee035417b71ffad6d52ece04925bef3b3. No wider-centre exclusion, dead-family census, base-10 infinite certificate, or Lean claim is made. Full repository verify.py --changed is unavailable without a working GitHub shell checkout; standalone checks passed.
