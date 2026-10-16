# Agent #318 — exact arithmetic probe of n_k = 10^k - 26

## Status

This is WIP finite evidence, not a proof of an infinite-safe orbit and not a result about 196.

I selected the explicit family

    n_k = 10^k - 26,   k >= 4.

The family has a fixed finite defect at the right boundary of an arbitrarily long 9-block and was selected as an independent candidate for direct boundary-state analysis.

## Exact arithmetic

The first reverse-add states have closed forms, with small-width exceptions caused by boundary overlap:

    T^0(n_k) = 10^k - 26 = 99...9974                         (k >= 4)
    T^1(n_k) = 147 9^(k-4) 73                                (k >= 4)
    T^2(n_k) = 527 9^(k-4) 714                               (k >= 5)
    T^3(n_k) = 945 9^(k-4) 439                               (k >= 5)
    T^4(n_k) = 1880 9^(k-4) 8988                             (k >= 6).

Here 9^r denotes a block of r copies of the digit 9, not an exponent.

The exceptional small cases are exact:

    k=4: 9974 -> 14773 -> 52514 -> 94039 -> 187088
    k=5: 99974 -> 147973 -> 527714 -> 945439 -> 1879988
    k=6: 999974 -> 1479973 -> 5279714 -> 9459439 -> 18808988.

The included checker verifies the displayed parameterized identities for every k through 200 in their stated ranges.

## Finite orbit screen

Exact integer iteration was run for 5,000 additions for each k=4,...,12. No palindrome was encountered in any of these nine runs.

    k=4   no palindrome through t=5000
    k=5   no palindrome through t=5000
    k=6   no palindrome through t=5000
    k=7   no palindrome through t=5000
    k=8   no palindrome through t=5000
    k=9   no palindrome through t=5000
    k=10  no palindrome through t=5000
    k=11  no palindrome through t=5000
    k=12  no palindrome through t=5000

The test is exact integer arithmetic. It is nevertheless only a finite-horizon computation.

## Structural observation

For fixed t and sufficiently large k, the first several iterates retain a long central 9-block while their boundary words change. This is materially different from asserting that one carry word is invariant: the boundary/carry state evolves.

The promising research question is therefore whether the evolving boundary has a finite-state recurrence, possibly with a parameter shift in k. Such a recurrence would be necessary before this family could become an actual infinite construction.

A direct attempt to infer recurrence from the first states is not yet justified. In particular, the later orbit quickly leaves the five-step closed-form regime. No finite-state return has been established.

## Scope and next obligation

This family should remain classified as checked finite evidence / WIP. It does not establish decimal Lychrel existence and does not settle the orbit of 196.

The next substantive task is an exact boundary-state recurrence search for n_k=10^k-26, looking for a relation of the form

    T^p(n_k) = F(n_{k+r})

or an equivalent finite-state conjugacy on the boundary data.

If no such recurrence exists, the exact first divergence should be preserved as a negative result and used to refine the construction search.
