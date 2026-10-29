# Z33 target: rooted p12/m9, clock phase 9

## Exact claim attempted

At the reference width `(q,k)=(14,100)), enumerate every junction word
`J in {0,...,18}^m` for `m in {3,4,5}`, paired with every one of the 30
charge-zero `U3` rotations `rot(9,a,18-a)` for even `a in [0,18]`.
Do not prune either parity of the palindromic centre `C`: the U3 carry-reset
cone makes the seam/port transition independent of C.

The tested transition is the exact rooted decimal reverse-and-add seam map
starting at clock phase 9. A valid edge must preserve the strict W9/root
prefix and reproduce the U3 port at each phase; the junction itself may change
during the epoch, so this is not merely a fixed-J test. The desired endpoint
would be a closed 120-step seam orbit, followed by a second epoch if any
one-epoch orbit survived.

## Scope boundary

This target covers fixed junction length 3, 4, or 5 throughout the phase walk.
It does not cover length-changing/growing seams, |J| >= 6, U4/mixed bands, or
other clock phases. A negative result here is not a proof that a decimal
Lychrel number exists.
