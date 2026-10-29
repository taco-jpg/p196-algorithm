# U43 target statement

## Exact object

Use the canonical phase-0 root B0,W0 in calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt, and define, least-significant coefficient first,

    H(q,k) = B0 ++ W0^q ++ J ++ U^k
    P(q,k;J,U,C) = H(q,k) ++ C ++ reverse(H(q,k))

J is any finite coefficient word, C is a finite palindromic coefficient word with even midpoint coefficient when its length is odd, and U is one of the 30 cyclic rotations of (9,a,18-a) for even a in 0..18. The exponents q,k are concrete positive integers for simulator runs.

## Lemma this route supplies

For every valid concrete pairword and every finite time t, the digit-vector transition emitted by simulator.cpp is exactly the ordinary decimal reverse-and-add transition N → N + reverse(N), including the full next pairword, digit length, overflow bit, and palindrome status; crosscheck.py checks those values state-by-state against Python unbounded integers. At epoch checkpoints it exactly tests, rather than assumes, whether the observed pairword equals P(q,k+r*gain;J,U,C).

This is the finite-step semantic correctness lemma needed to trust a future candidate-checking trace. It is not the missing all-width recurrence P(q,k) → P(q,k+5), and it proves no all-time non-palindrome claim by itself.
