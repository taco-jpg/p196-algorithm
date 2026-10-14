# Arithmetic audit of the direct 936 exterior

No finite exterior and no width-independent obstruction were obtained.
This audit concerns only the proposed 24-phase N,O exterior for

    Q_m = P (936)^m W (639)^m reverse(P),
    W = (9,3,8,10,4,10,8,3,9),
    G^24(Q_m) = Q_(m+2).

Here words are low-to-high pair sums, p=|P|, and the outer coefficient
alternates 8,17. The verified center and periodic bulk identities remain
conditional on a finite exterior. The following necessary conditions
are exact for any finite p; none was inferred from a bounded search.

## A necessary exterior checksum modulo 11

Write P(x)=sum_i P_i x^i. Direct evaluation gives

    (936)(-1)=12,             W(-1)=12,
    Q_m(-1)=2P(-1)+12(-1)^p.

The last expression is independent of m. Indeed the two periodic bands
contribute 12(-1)^p(1-(-1)^m), while the center contributes
12(-1)^(p+m). Their m-dependent terms cancel.

At an addition whose input has an even number of decimal digits,
reverse(n)=-n mod11, so the output is divisible by 11. Subsequent
reverse-and-add updates preserve divisibility by 11, since reversing
an L-digit word changes its residue by the factor (-1)^(L-1).
The prescribed 24-step clock contains such an even-length input.

The normalized integer belonging to Q_m is exactly Q_m(10). The return
equation would therefore imply that Q_(m+2)(10) is divisible by 11.
Consequently every proposed exterior must satisfy

    P(-1)+6(-1)^p = 0 mod11.                         (1)

This condition is compatible with finite words and is not an obstruction.
For example P=(8,12,9,0) satisfies (1); it is only an example satisfying
the checksum, not a certified exterior or return family.

## Modulo 99 adds no independent obstruction here

For every decimal integer with L digits,

    reverse(n) = 10^(L-1) n mod99.

Thus an odd-length addition multiplies the residue by 2, and an
even-length addition by 11. In a 24-step alternating N,O block there
are twelve inputs of each parity. The resulting multiplier is

    2^12 * 11^12 = 22^12 = 55 mod99.

The core (936)^m W (639)^m has residue 1 mod99 for every m: its digit
sum is 36m+64=1 mod9, and its alternating sum is 12=1 mod11.
Since the complete word has odd length, its reflected P contributes
the same residue as P. Therefore

    Q_m(10) = 2P(10)+10^p mod99,

also independent of m. The return requires 55Q_m(10)=Q_m(10) mod99,
equivalent to 11 dividing Q_m(10). This is exactly (1); the mod9 part
already passes because the digit-sum increment is 36.

This also identifies a limit of the simplest higher-modulus strategy.
Any modulus coprime to 10 for which reversal of every L-digit word acts
as one scalar multiplier on its numerical residue must divide 99.
Comparing two adjacent digit positions forces 10^2=1 modulo that
modulus; conversely this condition suffices. Thus a stronger modular
argument needs extra digit or carry information. This statement does
not exclude higher-modulus arguments that retain such information.

## Exact rational tail-sum condition

Suppose a finite exterior exists, with phase words P_t of a common
width p and the prescribed bulk phase B_t to their right. Normalize
from the interior toward the outside, and let H_t be the resulting
p-digit word on P_t. Its digits lie in 0,...,9. Let D_t be the resulting
three-digit periodic tail, in the same outside-to-inside order.

The high-end digit stream of the next integer is H_t D_t^infinity
at an N step, and 1 H_t D_t^infinity at an O step. Interpreted as a
formal decimal stream, its rational value is respectively

    H_t(10) - 10^p D_t(10)/999,
    1+10H_t(10) - 10^(p+1) D_t(10)/999.

The sum of these 24 rational values must be zero. To justify this
without treating an infinite word as a witness: for every finite K,
the trailing K-digit update adds the reversed leading K-digit stream
modulo 10^K. Its 24-step periodicity makes their sum zero modulo 10^K.
All the stream values have denominator 999, coprime to 10. Their sum
is consequently a rational whose numerator is divisible by every
10^K, so that numerator is zero.

For the exact 936 bulk trace, independent periodic carry normalization
gives

    sum_(t even) D_t(10) = 5994,
    sum_(t odd)  D_t(10) = 5994.

Hence every proposed finite exterior must satisfy the exact integer
identity

    sum_(t even) H_t(10) + 10 sum_(t odd) H_t(10) + 12
       = 66 * 10^p.                                  (2)

The bulk contribution is integral and (2) is compatible with the digit
bounds. It supplies a global constraint on all phase prefixes, but this
audit did not turn it into a contradiction or construct words satisfying
the complete carry equations. It therefore does not close the exterior
gap.

## Verification and scope

`exterior936_audit.py` independently generates the exact 24 bulk phases
using periodic carry resets, verifies their return, and computes the
tail sums in (2). Direct finite polynomial evaluations supplement the
algebraic derivation of (1) and the mod99 formula. No new boundary search
was run. Results are in `exterior936_audit.json`.

No temporal-period-preservation assumption was used: a spatial successor
can introduce new temporal periods, as the existing graph calculations
already demonstrate. A finite 936 exterior remains neither constructed
nor ruled out by this audit.
