# U43: exact decimal template trace simulator

**Scope: COMPUTED cross-checking tool plus a direct arithmetic soundness argument. This is not a decimal Lychrel certificate.**

The tool checks concrete members of the rooted phase-0 p12/m9 template family

    H(q,k) = B0 ++ W0^q ++ J ++ U^k
    P(q,k) = H(q,k) ++ C ++ reverse(H(q,k))

B0 and W0 come from calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt. J is any finite coefficient word, including empty; C is any palindromic coefficient word, including empty; U is one of the 30 cyclic charge-zero complement-nine words. Coefficients are least-significant first and lie in 0..18. If C has odd length, its midpoint coefficient must be even so P is realizable as a decimal pair-coefficient word.

## What it checks

simulator.cpp is a fast, independent C++ digit-vector engine. For requested q,k it realizes a canonical integer from P(q,k) and emits every state from time 0 through steps. Each trace row includes the full decimal digit string, the full pair-coefficient word, palindrome status, the next overflow bit, whether that bit matches the rooted p12 clock, and whether an epoch checkpoint equals P(q,k+r*gain).

For example, steps=240, epoch=120, gain=5 compares the full pairword at steps 0, 120, and 240 against P(q,k), P(q,k+5), and P(q,k+10). A checkpoint match is reported, never assumed. The simulator also reports palindrome states; finite trace output alone does not imply an all-time guard.

crosscheck.py independently computes the same orbit with Python unbounded integers. It compares every state exactly: decimal digits, every pair coefficient, palindrome flag, overflow bit, clock match, and checkpoint comparison. It does not use hashes as a substitute for equality. crosscheck_r30.py additionally compares the 120-step control fixture with the existing R30 parametric verifier.

## Soundness argument for each concrete transition

Let the current canonical decimal digits be d0,...,d(n-1), least-significant first, and let p_i = d_i + d_(n-1-i). Then

    N + reverse(N) = sum_i p_i * 10^i.

Consequently, the exact ordinary decimal addition is schoolbook normalization of the pair coefficients: with carry c0=0, compute s_i=p_i+c_i, output digit e_i=s_i mod 10, and set c_(i+1)=floor(s_i/10). Append the final carry if it is nonzero. Since 0<=p_i<=18, each carry is 0 or 1 and the output is precisely N+reverse(N). The next pairword is exactly e_i+e_(n'-1-i), which the C++ engine emits and the Python bigint oracle independently checks.

The initial realization splits each symmetric coefficient p_i into two decimal digits in 0..9; an odd-length centre is split in half only when its coefficient is even. Thus the constructed source is a canonical positive integer with the requested pairword. At each epoch checkpoint, the tool compares the full observed pairword to a freshly expanded target template. The proof above establishes transition semantics for each concrete state; it does not prove that any template returns, that a clock persists for all parameters, or that an orbit stays non-palindromic forever.

## Build and run

From the repository root:

    g++ -O3 -std=c++17 -Wall -Wextra -Werror calculation/new_structures/U43/simulator.cpp -o /tmp/u43-simulator

    python3 calculation/new_structures/U43/crosscheck.py --simulator /tmp/u43-simulator --lattice calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt --J 5 --U 9,14,4 --C 10 --widths 20:20,40:40,80:80,160:160 --steps 240 --epoch 120 --gain 5

For a reproducible multi-fixture test, including an even centre, an odd centre, a rotated U, and empty J,C:

    bash calculation/new_structures/U43/test_controls.sh

pairword_code uses 0123456789ABCDEFGHI: digits 0 through 9 represent coefficients 0 through 9, and A through I represent 10 through 18. This is an exact lossless encoding, not a digest.

## Scope and limitations

- Decimal base 10 only; rooted phase-0 B0,W0 from the named lattice file.
- Concrete q,k parameters and finite traces; no universal symbolic quantification over q,k.
- Supports all 30 cyclic U rotations, arbitrary finite J, and empty or nonempty palindromic C.
- The output is an independent ALERT-checking aid. Do not label a finite replay as an all-time certificate; an ALERT still requires the exact all-width seam-return proof and a non-palindrome guard.
