# Agent #318 — exact arithmetic probe of n_k = 10^k - 26

## Status

This is a WIP finite investigation, not a proof of an infinite-safe orbit and not a result about 196.

I selected the explicit family

    n_k = 10^k - 26,   k >= 4.

It is not itself a proof-producing invariant. The motivation is that it has a very clean exact digit boundary while producing unusually long palindrome-free prefixes in direct integer iteration.

## Exact arithmetic

For every k >= 4, direct decimal arithmetic gives the following first five states:

    T^0(n_k) = 10^k - 26
             = 99...9974

    T^1(n_k) = 147 9^(k-4) 73
    T^2(n_k) = 527 9^(k-4) 714
    T^3(n_k) = 945 9^(k-4) 439
    T^4(n_k) = 1880 9^(k-4) 8988.

Here 9^r denotes a block of r copies of the digit 9, not an exponent.

For example:

    k=4: 9974 -> 14773 -> 52714 -> 94039 -> 18808988
    k=5: 99974 -> 147973 -> 527714 -> 945439 -> 188098988
    k=6: 999974 -> 1479973 -> 5279714 -> 9459439 -> 1880998988.

The included checker verifies these exact identities for every integer k from 4 through 200, so this is not a floating-point or sampled-arithmetic calculation for the displayed formulas.

## Finite orbit screen

Exact integer iteration was then run for 5,000 additions for each k=4,...,12. No palindrome was encountered in any of these nine runs.

    k=4   no palindrome through t=5000
    k=5   no palindrome through t=5000
    k=6   no palindrome through t=5000
    k=7   no palindrome through t=5000
    k=8   no palindrome through t=5000
    k=9   no palindrome through t=5000
    k=10  no palindrome through t=5000
    k=11  no palindrome through t=5000
    k=12  no palindrome through t=5000

The orbit widths grow substantially during this test; the absence of a palindrome is therefore a finite-horizon statement only.

## Why this is potentially useful

The family has a fixed finite defect at the right boundary of an arbitrarily long 9-block. The first four images retain a long 9-block exactly, but the boundary data evolves:

    9974  -> 14773 -> 52714 -> 94039 -> 18808988.

This makes it a candidate for a boundary-state / defect-state analysis rather than an assumption of a fixed carry word. In particular, the carry state changes between steps, so the existing observation that a single complete carry word can be normalized to a palindrome does not by itself settle this family.

However, the current evidence does NOT establish a repeatable return. The later states do not yet admit a proved finite-state recurrence with parameter-independent boundary data. Therefore this should remain classified as finite checked evidence / WIP.

## Important negative check

A long finite prefix cannot be promoted to an infinite-safe construction. In particular, the data here does not prove decimal Lychrel existence and does not prove that 196 is Lychrel.

The next substantive obligation is to derive the exact boundary-state recurrence for this family (or find a finite-time collision showing that the apparent long 9-block is transient). If the boundary state can be made recurrent with an exact parameter shift, that would be the first real bridge toward an infinite construction; if not, the failure mechanism should be formalized as another obstruction.
