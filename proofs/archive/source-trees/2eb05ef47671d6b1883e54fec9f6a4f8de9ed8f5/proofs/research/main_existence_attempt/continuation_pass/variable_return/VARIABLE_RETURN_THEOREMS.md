# Variable-time return reductions and the zero-exterior obstruction

Decimal Lychrel existence and the assertion for 196 remain unproved.
These are written carry arguments and exact arithmetic certificates.
The three-zero theorem is additionally formalized and freshly audited in
`../lean/zero_exterior/`; the other reductions here are not Lean theorems.
No novelty claim is made.

Words are low-to-high decimal pair sums. For a positive decimal integer n
of width L, let q_i=d_i+d_(L-1-i). Write G(q) for the pair word of
n+reverse(n). A canonical symmetric word has symbols in 0..18, positive
outer symbol, and an even middle symbol at odd width; it is always realized
by a finite positive integer. All statements below use actual terminal
overflow and actual decimal width.

## 1. Variable return times on an affine successor ray stabilize

Let Q_k be a canonical family with a fixed finite run-symbol list and
positive run lengths a_i*k+b_i, for all integers k>=0. Suppose the lengths
are unbounded and have total slope A=sum a_i>0. Fix a positive integer s.
Assume that for every sufficiently large k there is some positive return
time tau(k) such that

    G^tau(k)(Q_k) = Q_(k+s).

Then there is one fixed positive time t and one K such that

    G^t(Q_k) = Q_(k+s)       for every k>=K.

If the supplied return segments are safe at every positive ordinary
output, t can also be chosen safe for every k>=K. Thus allowing an
unbounded or irregular time label supplies no additional tail construction
for a one-parameter affine family with an additive parameter update.
The theorem does not cover multiplicative parameter maps, growing run
catalogues, or arbitrary unions of multivariate parameter regions.

### Uniform time bound

The repository's independently formalized outer-width potential is

    p:    1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18
    psi:  4 3 2 2 2 1 1 1 1  1  0  0  0  0  0  0  0  0.

For every actual step with outer pair coefficient p, next outer p', and
overflow h, it satisfies

    psi(p')+1 <= psi(p)+4h.

Summing through a segment of width gain Delta gives

    t <= 4 Delta+psi(p_initial)-psi(p_final) <= 4 Delta+4.    (1)

This is the strengthened bound in `../../../exist_count_notes.txt`, not
the earlier weaker `5 Delta+4` estimate. In Q_k -> Q_(k+s), the outer
symbol is unchanged and Delta=A*s. Consequently

    1 <= tau(k) <= 4*A*s.                                  (2)

For a finite collection of affine templates with the same slope and
fixed intercept differences, (1) likewise bounds the times on each edge.

### Why the finite cover contains a uniform tail, not just scattered k

For each fixed t, the t-step image G^t(Q_k) is, on some integer tail,
another fixed-symbol affine-run word. Here is the relevant specialization
of the previously proved multivariate run theorem; it is not assumed from
a fit to sample values. Through a positive constant input run the carry
is fixed after its first column, so normalization emits at most two digit
runs. An actual terminal carry adds one constant-length digit. Reversing
and overlaying those digit runs compares finitely many affine endpoints.
Every difference alpha*k+beta has a constant sign on a sufficiently long
tail, unless it is identically zero. Therefore every comparison has one
permanent outcome after finitely many k, and every retained run length
is positive there. Induction proves the claim for each fixed finite t.

Choose one common tail for the finitely many times in (2). Positive
canonical RLE has a unique run-symbol list and run lengths. Thus equality
with Q_(k+s) is either an identity throughout this tail, or holds for at
most one k: unequal symbol lists never agree; if symbol lists agree,
one nonzero affine run-length difference has at most one root. A finite
collection of these at-most-singleton sets cannot cover the entire tail.
At least one return time is therefore an identity throughout a tail.

Safety has the same eventual dichotomy. For each intermediate step the
normalized decimal digit word has an eventual positive RLE. Its equality
to its reversal either holds on the whole tail or at at most one k.
Discard those finitely many exceptional k. Every one of the finitely many
return times is now either safe everywhere on the tail or unsafe everywhere
on it. The original safe-cover hypothesis forces a time that is both an
identity and safe throughout the tail. This explicitly handles isolated
palindromic parameters; checking one parameter would not suffice.

For an update k -> a*k+b with a>1, Delta=A*((a-1)k+b) is unbounded,
and this finite-cover argument does not apply. This is the genuine
expanding/reset case investigated by the separate catalogue probe.

## 2. Three zero columns prohibit arbitrarily late returns

**Theorem.** If q_t is the actual pair word at time t in any positive
decimal reverse-and-add orbit and starts

    (p,0,0,0),       1<=p<=18,

then t<=4. More precisely, its entire history consists of nonoverflow
steps up to t at these four columns, and p=2^t*q_0[0].

In particular, no fixed p prefix `(p,0,0,0)` can return at any positive
time. No family of words with a single nonzero outer coefficient followed
by at least three zeros can support infinitely many returns, even if its
core, spacer, outer coefficient, and return times vary arbitrarily.
This includes multiplicatively growing zero-spacer reset templates.

### Column proof

For an input symmetric q, write a_i for the low incoming carry and c_i
for the high outgoing carry at column i. Then a_0=0 and

    a_(i+1)=floor((q_i+a_i)/10),
    c_i=floor((q_i+c_(i+1))/10).

The low and high digits are l_i=(q_i+a_i) mod 10 and
u_i=q_i+c_(i+1)-10c_i. The actual overflow is h=c_0. Pairing in the
actual output width gives

    h=0:  q'_i=l_i+u_i;
    h=1:  q'_0=l_0+1,  q'_i=l_i+u_(i-1) for i>=1.        (3)

These identities hold when the displayed windows overlap near the center;
they are identities of the same actual symmetric word, not an independence
assumption about two windows. A canonical word with the target prefix
has width at least five, so its predecessor has at least four columns and
all displayed columns exist. In particular, overlapping windows at the
minimum widths are included.

Suppose first h=1 and q'_1=q'_2=q'_3=0. Nonnegative digits in (3) give
l_1=u_0=0. From u_0=0 and c_0=1, q_0+c_1=10. There are two cases.

* q_0=10,c_1=0. Then a_1=1 and l_1=0 force q_1=9.
  The equation c_1=0 forces c_2=0. Thus u_1=9, contradicting q'_2=0.
* q_0=9,c_1=1. Then a_1=0 and l_1=0 force q_1 in {0,10};
  c_1=1 excludes 0, so q_1=10. Now a_2=1, and q'_2=0 forces
  q_2=9 and u_1=c_2=0. Hence c_3=0 and u_2=9,
  contradicting q'_3=0.

Overflow therefore cannot produce the target prefix.

Now suppose h=0 and q'_1=q'_2=q'_3=0. We have q_0<=9 and a_1=0.
From l_1=u_1=0, q_1 is 0 or 10, and c_2=0. If q_1=10,
then a_2=1, while q'_2=0 forces q_2=9,c_3=1 and hence c_2=1,
a contradiction. Thus q_1=0 and c_1=c_2=a_2=0. Next, l_2=0
gives q_2 in {0,10}; c_2=0 excludes 10. So q_2=0 and c_3=a_3=0.
Similarly q'_3=0 forces q_3=0. Finally q'_0=2q_0 because c_1=0.
Thus the predecessor starts `(p/2,0,0,0)` and this step has no overflow.

Apply this argument backwards t times. Positivity and p<=18 give
1<=q_0[0]=p/2^t, so 2^t<=18 and t<=4. No assertion about safety is
needed. The positive seed 10^4 reaches a pair word starting `(16,0,0,0)`
at time four, showing the time bound is sharp; its intervening palindromes
are deliberately continued.

The three-zero requirement matters. The canonical input
`(9,10,9,0,9,10,9)` has an overflowing successor beginning `(10,0,0)`.
Two zeros alone do not imply the no-overflow predecessor conclusion.

### Verification scope

`zero_exterior_check.py` independently realizes all 18*19^3 four-column
prefixes with both possible incoming carries as ordinary positive integers.
It executes decimal reversal and integer addition, checks the conclusions,
and preserves every outcome in a binary gzip stream. It also exhausts
every canonical input word of widths one through eight, checking the
minimum predecessor/successor widths four and five and all overlapping
windows in that range. The analytic column
proof above supplies arbitrary length and arbitrary time. The finite
controls audit the arithmetic implementation and include the sharp
time-four example and the two-zero overflow counterexample.

The independent formal stream subsequently verified the complete theorem,
its arbitrary-width ordinary-orbit bridge, backward no-overflow/doubling
history, fixed-outer nonreturn, and both sharp examples in Lean. See
`../lean/zero_exterior/STATUS.md` for its exact declarations and axiom audit.

## 3. What remains for an expanding construction

The zero-exterior theorem eliminates the first simple multiplicative
attempt. It does not apply to the generalized overlap exterior `(p,p,0)`:
the second outer coefficient can store carry information and permits
returns under varying clocks. The finite catalogue probe therefore tests
those actual overlap words with no prescribed overflow clock. Its exact
all-spacer additive-reset classification and its separately bounded
multiplicative-reset experiment are reported in `STATUS.md`.

A positive result still needs a finite realizable seed and a safe reset
map that stays inside a proved parameter domain after every iteration.
No such map is supplied here. A finite counterexample to a universal
template or a finite failed reset search is not an all-time result about
any decimal Lychrel candidate.
