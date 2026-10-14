# Structural boundary derivations

These results concern the exact alternating N,O exterior transfer graph.
They construct no finite decimal Lychrel witness and make no claim about
196, other clocks, or decimal Lychrel existence in general.

The reverse-language computation in `../reverse/` now supplies a route to
an exact obstruction, rather than a larger forward search. The local and
ranking checks below were independently implemented in
`structural_checks.py`. The complete all-width conclusion also requires
the independently checked exact-preimage and graph-closure obligations
for that reverse certificate.

## A short forbidden temporal factor

Write a cut letter as `(a,b,c,z)`, using the archived N/O pair convention.
Immediately after the mandatory first exterior column 8/17, its letter is

    r = (0,1,1,7).

Thus every temporal slot of the exterior root is r.

The reverse agent's edge-labeled graphs G_0,...,G_8 describe exact cyclic
temporal languages at successive inverse spatial depths. Their observed
graph equality is G_8=G_5. Once the exact-preimage property and equality
are checked, the union of G_0,...,G_7 contains every finite-distance
predecessor of every specified bulk target, for every temporal period.

A particularly small exclusion certificate is available inside each
graph: delete all edges whose label is not r. The remaining directed
graph has no path of three edges. The independently checked data are:

| Graph | Vertices | Edges | r-labeled edges | Longest r path |
| --- | ---: | ---: | ---: | ---: |
| G_0 | 12 | 12 | 0 | 0 |
| G_1 | 22 | 40 | 0 | 0 |
| G_2 | 60 | 178 | 0 | 0 |
| G_3 | 136 | 484 | 3 | 1 |
| G_4 | 342 | 1,322 | 11 | 2 |
| G_5 | 456 | 1,802 | 21 | 2 |
| G_6 | 456 | 1,802 | 21 | 2 |
| G_7 | 456 | 1,802 | 21 | 2 |

For each graph, `root_factor_rank_certificate.json` gives a sparse vertex
rank rho in {0,1,2}. Every r-labeled edge u->v satisfies rho(u)<rho(v).
These inequalities directly forbid a path labeled rrr. They also forbid
an r-labeled closed walk of any positive length: repeat the closed walk
until it has at least three edges. A temporal period of one or two pairs
is therefore not an exceptional case.

Consequently the forced root word r^n cannot belong to the closed reverse
language for any n>0. This gives a human-readable temporal factor
obstruction once the finite reverse-language closure is certified.
It does not assume that temporal periods are preserved by spatial edges.

The rank file records SHA-256 hashes of the exact graph files it checks.
`structural_checks.py` also checks the parsed equality G_8=G_5, but does
not by itself prove that every graph is the full preimage of its prior
graph. That separate obligation belongs to the reverse-language checker.

### Fixed-width boundaries without an assumed temporal return

There is a further finite-state consequence after the all-period
obstruction is established. Fix a prefix width k, the prescribed 8/17
outer branch, and one of the specified bulk traces. Suppose that arbitrary
phase prefixes P_t of this width satisfy the exact boundary and seam
equations forever, without assuming any temporal period for P_t.

The state `(t mod 24, P_t)` has at most 24*19^k possibilities. The bulk
trace supplies the inward high carry, and the exterior supplies initial
low carry zero, so the exact update of P_t is deterministic. An infinite
valid trajectory must repeat one of these states. Its intervening segment
is then an exact periodic exterior of period divisible by 24. The
all-period exclusion contradicts this. Equivalently, sampling every 24
steps gives a repeat within 19^k+1 samples if the boundary remains valid.

Thus allowing a nonperiodic schedule of prefixes cannot maintain this
same fixed-width, alternating-clock exterior indefinitely. This argument
uses finite-state eventual periodicity at one fixed spatial width. It
does not claim that spatial successor columns preserve temporal periods.
It does not exclude boundaries whose necessary width grows without bound,
or changes to the bulk or overflow schedule.

## Closed-form inverse fibers

Let the new cut's letter be `(alpha,beta,delta,zeta)`. An inverse option
records `(Q,a,b,c,e,R)`. The archived inverse enumeration has at most two
options at every letter. The reason is elementary:

1. The O coefficient R and its outward high carry e are unique.

   - If 0<=zeta<=8, then R=zeta+10*beta, e=beta, and b is either bit.
   - If zeta is -1 or 9, then R=9, e=(9-zeta)/10, and b=beta.

2. The ordinary N inverse is

       a = (R-delta) mod 2,
       Q = 10*alpha + (R-delta-a)/2,
       c = alpha.

   Retain this option exactly when 0<=Q<=18. The two cases that fail
   are precisely the empty new letters `(0,0,1,0)` and `(1,1,0,8)`.

3. There is one extra N inverse precisely when R=9 and alpha!=delta:

       Q=9, a=alpha, c=delta.

This describes all options. Direct forward digit normalization checks the
formula for all 88 new letters: 78 fibers have two options, eight have
one, and two are empty.

In particular, the old N high carry c equals the new N low carry alpha
except at the neutral Q=R=9 alternative. At a bulk target the first
inverse column has no such O=9 ambiguity, so its coefficient column is
fixed even though some incoming O carries remain free. This explains why
raw inverse states can acquire longer temporal periods without changing
the first inverse coefficient column. It does not imply period
preservation at later columns.

## An exact compatible charge modulo nine

There is also a useful algebraic identity. For a letter x=(a,b,c,z), put

    F(x)=11a+10b-110c+10z.

For every valid local transfer from old x to new x', with N coefficients
Q and Q_next at successive temporal pairs, ordinary carry arithmetic gives

    10 Q_next - 22 Q
      = F(x) - 10 F(x') + 99 (z' - 11 c').

The standalone checker verifies this exact integer identity on all 1,640
admissible local tiles. For a cyclic temporal word of 12 pairs, multiply
the j-th equation by 7^j and add modulo nine. Since 7^-1=4 modulo nine,
the temporal Q terms cancel. Thus every spatial edge preserves

    I(a,b,c,z) = sum_j 7^j(2a_j+b_j-2c_j+z_j) mod 9.

The same derivation works for a temporal pair count divisible by three.
The exterior root and all twelve bulk targets have I=0. Therefore this
charge is compatible with the proposed boundary and is not the separating
invariant. It must not be described as an impossibility proof.

## A compression that is too coarse

The 39,194-orbit finite certificate contains 262 distinct adjacent pairs
of temporal cut letters. Retaining only these pairs discards essential
correlations. `pair_language.py` computes exact two-inverse-column SCC
composition for this pair-language abstraction, over arbitrary temporal
periods. Its first closure step adds 808 pairs and already admits the
uniform root pair (r,r). The abstraction eventually closes at 4,168 pairs.

This failure is a limitation of that pair-language abstraction, not a
counterexample to the exact reverse-language certificate. In particular,
no finite exterior was obtained from the abstract root pair. The exact
sofic construction preserves the hidden temporal correlations that the
pair abstraction loses.
