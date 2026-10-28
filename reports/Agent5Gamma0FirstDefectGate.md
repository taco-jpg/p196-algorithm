# The universal no-overflow first-defect carry gate

**PAPER PROOF.** This is a first-mismatch *necessary condition*, not a
criterion for periodic centres or a proof that base-10 Lychrel numbers
exist. Its corollary rules out one-step erasure of **arbitrarily wide**
centre-side perturbations of the published decimal p12/m9 lattice at
three specified no-overflow temporal phases, provided the first defect is
safely inside the lattice bulk. It says nothing about time periods,
general initial exteriors, the other nine phases, or the orbit of 196.

## Universal theorem (no lattice assumptions)

Let P and R be two **palindromic** pair-coefficient words of the same
length n, with all entries in [0,18]. Carry-normalize each in base 10,
with incoming carry zero; assume both have final carry **zero**, so
both digit outputs O and V have length n. Assume their complete next
pair words agree:

    O[i] + O[n-1-i] = V[i] + V[n-1-i]   (0 <= i < n).

Let j>=1 be the first differing coefficient in the lower half, and
require `j < (n-1)/2` so its reflected site `j'=n-1-j` is distinct and
not the central site. Put q=P[j], q'=R[j], delta=q'-q != 0.
Let `c_i`, `d_i` be the carry *into* position i for P and R, and
`k_i=d_i-c_i` (each k is in {-1,0,1}). Grade-school normalization gives

    V[i]-O[i] = R[i]-P[i] + k_i - 10 k_(i+1).

Since all lower coefficients before j coincide, `k_j=0`; symmetry also
makes all upper coefficients after j' coincide. Next-pair equality at
`i=j-1` gives `V[j'+1]=O[j'+1]`, because its other partner `j-1` is
unchanged. Applying the normalization equation at this unchanged
coefficient gives `k_(j'+1)=10 k_(j'+2)`. As both are in {-1,0,1},

    k_(j'+1)=k_(j'+2)=0.

At i=j, both the lower and upper coefficient differences equal delta.
The two normalized digit differences are `delta-10 k_(j+1)` and
`delta+k_(j')`, so pair agreement gives

    2 delta + k_(j') - 10 k_(j+1) = 0.

Parity forces `k_(j')=0`, then `delta=5 k_(j+1)`. Thus a nonzero first
defect must change the lower outgoing carry by +1 or -1, **but not** the
upper outgoing carry; both incoming carries at these two sites are
unchanged by the comparison.

Write `cL=c_j` and `cU=c_j'` for the original incoming carry bits. Because
`q,q'` are in 0..18, a complete elementary check of
`floor((q+c)/10)` gives exactly four possibilities:

| original q | replacement q' | cL | cU |
|---:|---:|---:|---:|
| 4 | 9 | 1 | 0 |
| 9 | 4 | 1 | 0 |
| 9 | 14 | 0 | 1 |
| 14 | 9 | 0 | 1 |

These conditions are **necessary only**; even a matching first cell may
fail further inside. The four-case enumeration is exhaustively checked
by the included 19x19x2x2 arithmetic control.

## Application to all widths of the decimal period-12 lattice

Read the repository's `calculation/decimal_frontier/lattice_kinks/data/lat_p12m9.txt`
(base 10, p=12, m=9, exterior width 34, overflow word
`100010001000`). Let P be the symmetric pair word built from the
published phase-t exterior B_t followed by the phase-t period-9 row W_t
through the lower half, and then mirrored; if n is odd, make its centre
coefficient even without changing other entries. These are realizable
as ordinary canonical decimal seeds because the outer pair coefficient
is positive. For each `t in {3,7,11}` the outer coefficient is less
than 9, so the normalization has **no final overflow for any length**.

Let R be any distinct symmetric pair word of that same length, also
with no final overflow and identical coefficient exterior up to its
first differing lower-half position j. Suppose that j is a genuine
periodic bulk location, at least one full spatial period away from the
exterior and from the middle (for example `j>=34+18` and
`j<=ceil(n/2)-12`). There is no restriction on how many later
coefficients R changes. The universal theorem applies to the first
mismatch j.

For the pure-lattice baseline P, the entering lower carry is the
published periodic value `cL=C_t[r]`, `r=(j-34) mod 9`. The entering
upper carry `cU` at j' is determined from the row in reverse order.
Since every temporal row W_t has a non-9 symbol in each spatial period
(in fact the maximum consecutive 9-run is 1), any centre correction
loses carry influence before j' when the stated margin holds. Thus

    cU = [ W_t[r+1] >= 10 ]  if W_t[r+1] != 9,
         [ W_t[r+2] >= 10 ]  otherwise,     (indices mod 9).

The finite 9-residue check of (q,cL,cU) against the four-case gate
has **zero matches** at t=3,7,11. Hence no such R can have the same next
pair word as the pure-lattice P, at *any* band length. This is a proved
one-step non-erasure obstruction for arbitrarily wide modifications;
it is NOT a period-12 no-centre theorem, since successors need not
match a pure lattice, and other phases remain available.

For context, the other six no-overflow phases do have potential first
sites: t=1,5,9 permit a 4->9 or 9->4 at two residues each; t=2,6,10
permit 9->14 at two residues each. These are only local necessary
gates, not positive collision witnesses or certificates.

## Independently checked controls

`gamma0_gate.py` checks every q,q',cL,cU case; recomputes the 12-phase
lattice carry and row data at n=400,401,418,419; checks that t=3,7,11
have no gate at any of nine residues; and independently replays three
small **real** no-overflow pairword collisions at lengths 7,8,9, using
ordinary schoolbook decimal digit addition rather than the pair-word
normalizer. They demonstrate that the gate restriction is sharp enough
to admit valid cases, though it is not sufficient.

Run from the repository root:

    python3 calculation/decimal_frontier/lattice_kinks/code/gamma0_gate.py

The all-width result is the carry argument plus the exact nine-residue
row check, not an inference from finite n simulations.