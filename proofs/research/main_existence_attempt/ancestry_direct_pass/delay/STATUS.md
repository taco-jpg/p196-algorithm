# Finite safe ancestry versus terminating delay

The all-depth claim is **not proved**. No parametric family with unbounded
finite first-hit times was obtained, and no primary proof of that assertion
was located in the focused source check. There is, however, an exact
structural equivalence and a concrete obstruction through depth 288.

## Indexing and the exact equivalence

Let T(n)=n+reverse(n), and define

    d+(n) = min { t>=1 : T^t(n) is a palindrome },

with infinity if the set is empty. This is the **least positive iterate**.
The initial n is allowed to be a palindrome, matching S_0=Canonical.

Let B be the canonical pair words whose next ordinary integer is a
palindrome. Let the safe image operator on sets be

    H(X) = { G(q) : q in X and q not in B },
    S_0 = Canonical,       S_(r+1)=H(S_r),
    K_r = S_r minus B.

Then for every finite r>=0,

    S_r intersects B
      iff there exists a positive integer n with d+(n)=r+1.       (1)

Indeed, membership gives a finite realizable ancestry
q_0,...,q_r, with q_j outside B for j<r and q_r in B. Realize q_0
as an ordinary positive integer. Its first r positive iterates are
nonpalindromic and its (r+1)-st is palindromic. Conversely, the pair
words of such an integer trajectory give precisely this ancestry.
The initial integer need not be nonpalindromic for this equivalence.

Finite values of d+ form an initial segment of the positive integers:
if d+(n)=D and 1<=k<=D, then

    d+(T^(D-k)(n)) = k.

Consequently the following are equivalent:

* Unbounded finite positive first-hit times exist.
* Every positive integer occurs as a finite positive first-hit time.
* S_r intersects B for every finite r.

Also, S_r intersect B is empty **if and only if every finite d+ is at
most r**. Thus the proposed all-depth obstruction requires an actual
unbounded-delay theorem; arbitrarily long trajectories of unknown fate
do not establish it.

If one instead requires a nonpalindromic initial seed, unboundedness is
equivalent: a palindromic start with d+(n)>=2 has nonpalindromic T(n)
with first-hit delay d+(n)-1. This possible one-step shift matters for
finite bounds. It is unnecessary for the concrete witness below,
whose seed and all proper trajectory prefixes are nonpalindromic.

## Closure of K_r has a corresponding exact test

The sets S_r are nested, since H is monotone and H(S_0) is a subset
of S_0. Moreover G(K_r)=S_(r+1), a subset of S_r. Therefore K_r
fails forward closure precisely when some element of G(K_r) belongs
to B. Equivalently,

    G(K_r) is not a subset of K_r
      iff S_(r+1) intersects B
      iff some n has d+(n)=r+2.                                 (2)

This is a statement about the whole language K_r itself. It does not
exclude proper safe invariant sublanguages inside K_r.

## A verified 289-step finite witness

Use the published ordinary decimal seed

    n_0 = 13968441660506503386020.

`check_delay.py` independently recomputes all 289 additions by Python
integer reversal and checks every result against schoolbook column
normalization of the pair sums. Every n_0,...,n_288 is nonpalindromic;
n_289 is a 142-digit palindrome. The canonical realization of q(n_0)
is also nonpalindromic and has the same first successor.

Put b=q(n_288). The **same** b belongs to S_r intersect B for every
0<=r<=288: its r-step safe ancestry starts at q(n_(288-r)). Thus no
filter S_r in that range eliminates all palindrome predecessors.

Put a=q(n_287). For every 0<=r<=287, a belongs to K_r, but
G(a)=b does not belong to K_r. Its r-step safe ancestry starts at
q(n_(287-r)). Thus K_r is not forward closed throughout that range.

The full ordinary orbit is saved in `delay_289_trajectory.json`, and
`check_delay.json` records the endpoint pair words and the ancestry
indices for every claimed depth. These are exact finite arithmetic
witnesses, not a proof of unbounded finite delay.

## What a finite successful ancestry cutoff would imply

Nonemptiness of S_r and K_r is not an additional obstacle. The existing
long-run lemma supplies a simple all-r witness. For M>=1 use

    Q_M = 9^2 · 18^M · 9^2,
    u_M = the ordinary decimal integer 9^(M+2)00.

Here powers in u_M mean repeated digits. A surviving 18 run loses at
most two inherited positions per update, and the presence of an 18
coefficient excludes both branches of B. Taking M=2r+1 therefore
keeps all first r+1 positive iterates nonpalindromic. This proves
arbitrarily long **safe finite segments**, not termination afterwards.

For completeness, the local survival estimate follows because a
nonoverflow update preserves every strict interior 18 column, while
an overflow preserves the M-1 positions combining two old 18 columns.
The predecessor characterization used throughout the project is:
all q coefficients <=9, or outer coefficient 11 with every coefficient
in {0,11}; neither branch contains 18.

In particular, if all finite positive first-hit times were bounded by
a known D, u_(2D+1) would be an explicit Lychrel number: it avoids
palindromes for D+1 steps and could never have a later finite first hit.
Likewise, a proved cutoff S_r intersect B empty, or a closed K_r, would
directly yield existence using these nonempty safe-ancestry sets.

This gives the exact dichotomy

    either finite terminating delays are unbounded,
    or a finite decimal Lychrel number exists.

It does not choose a side. In particular, arbitrary finite safe-ancestry
filters have not been proved incapable of success at every depth.

## Source check: the published extension method is not uniform

The 289-step seed and its displayed trajectory appear at the original
experimenter's calculation page:

* https://jasondoucette.com/pal/13968441660506503386020

Anton Stefanov's authored OEIS entry describes a finite inverse-search
construction extending 288-step examples to 289 steps. It explicitly
includes an unextendable 287-step branch; it does not state that every
delay can always be increased:

* https://oeis.org/A340397

Stefanov's original article explains the inverse search and reports that
the particular ancestor 105956506309091459564960 admits no extensions
of delay 290 or above under the exhaustive branch calculation described
there. That is a source-reported result about that inverse tree, not a
newly independently audited theorem here:

* https://habr.com/ru/articles/536104/

The shorter record-page description of an x-to-x+1 extension method
must therefore not be read as a universally iterable induction:

* https://jasondoucette.com/worldrecords.html

No full source text has been copied into this directory. The source
lookup establishes the provenance and limited scope of the construction;
the 289-step trajectory used for (1)--(2) is independently verified.

## Reproduction and remaining obligation

Run

    python -B check_delay.py

Besides the 289-step trajectory, the script checks the long-reservoir
implementation for r=0,...,32,64,128,289. These finite controls supplement
the arbitrary-length survival argument; they are not its proof.

To rule out every finite-depth ancestry cutoff, one still needs a family
of *terminating* trajectories whose finite positive delays tend to
infinity, or another proof of that same assertion. The current results
establish the exact logical reduction and the finite depths above only.
