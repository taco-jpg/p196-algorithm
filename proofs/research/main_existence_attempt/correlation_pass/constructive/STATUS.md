# Context-sensitive seam normalization: an exact first step, no recursive closure

No decimal Lychrel number, proof for 196, or all-time safe recursive family
was obtained. This pass replaces the failed independent concatenation at
an active collision by an exact **endpoint-overlap identity with neutral-run
corrections**. It applies to any finite number of arbitrary motifs, not just
periodic words or the earlier three-island reservoir family.

The new identity does not iterate as an independent motif substitution.
A three-column output gives the first obstruction in the smallest eligible
one-column even alphabet. More generally, a fixed overlap decomposition
containing a duplicated positive component cannot evolve independently at
every step for five consecutive updates. Genuinely coupled seam states,
changing overlaps, and identities only at selected return times remain
outside that exclusion.

## 1. Definitions and exact domain

Words are ordered from low to high decimal position. A canonical pair word
is a nonempty symmetric word over 0,...,18 with positive outer coefficient
and even middle coefficient if its length is odd. Every such word has an
ordinary positive decimal realization.

Write `N_c(A)` for the retained-length digit word obtained by normalizing
the coefficients of A with incoming carry c in {0,1}. Write G(A) for the
pair word of its ordinary reverse-and-add successor; G includes the possible
new leading digit before taking mirrored sums.

Let A_1,...,A_m be canonical pair words in a reflection-symmetric list:

    A_j = A_(m+1-j).

Inside each A_j, let r_j be the length of its initial 9-run. Require that
the first coefficient after that run is greater than 9. The all-9 word is
excluded. Symmetry means that the last non-9 coefficient is the same high
coefficient. Therefore each A_j has final carry 1 for **both** incoming
carry choices. Internal coefficients and motif lengths are otherwise free.

Put a_j=|A_j|, s_1=0, s_j=sum_(i<j) a_i, and L=sum_j a_j. For a word U of
length L+1 let

    rev_L U(x) = x^L U(1/x),

where words are identified with their coefficient polynomials.

For any list of words, endpoint overlap means concatenation with one shared
endpoint at each join, adding the two endpoint coefficients. It does not
normalize, clip, or discard an excessive coefficient. Thus

    (a,b,c) overlap (d,e) = (a,b,c+d,e).

In particular, because |G(A_j)|=a_j+1, their overlap polynomial is

    R(x) = sum_j x^(s_j) G(A_j)(x),

of length L+1. R need not itself be a canonical pair word.

## 2. The exact all-motif collision identity

Define S_r(x)=1+x+...+x^(r-1) for r>=1 and S_0=0. Then

    H(x) = (x-10) sum_(j=2,...,m) x^(s_j) S_(r_j)(x).

For every finite list in the stated domain, exactly

    G(A_1 ... A_m) = R + H + rev_L H.                 (1)

There are no unspecified outside carries or extra end columns in (1).
The left endpoint is entered by carry zero. Every subsequent motif is
entered by carry one, and the whole word finishes with the single leading
digit one. The reflection in (1) uses the full actual output width L+1.

In particular, when every motif begins above 9, all r_j are zero and

    G(A_1 ... A_m) = G(A_1) overlap ... overlap G(A_m). (2)

Here R is automatically canonical. Its shared endpoints are sums of
numbers in 1,...,9, so no coefficient exceeds 18. This is an exact way to
account for a simultaneous collision of any number of motifs without the
spurious digit growth of independent concatenation.

### Proof including the neutral-run correction

Put D_j=N_0(A_j). Switching its incoming carry from zero to one changes only
the initial neutral run and the following high coefficient:

    N_1(A_j) - N_0(A_j) = -9 S_(r_j) + x^(r_j).

For r_j=0 this difference is simply 1 at the first digit. Both carry paths
have merged immediately after the first non-9 coefficient, and both leave
the motif with carry one. Consequently

    N_1(A_j) - N_0(A_j) - 1 = (x-10) S_(r_j).       (3)

The standalone successor digit polynomial for A_j is E_j=D_j+x^(a_j).
Adding shifted E_j creates a proposed digit polynomial

    E = sum_j x^(s_j) E_j.

At each internal seam, the preceding motif contributes a 1 at the first
column of the next motif. Formula (3) gives exactly the correction needed
to normalize that added 1. Thus the actual whole successor digit polynomial
is E+H. It has one leading digit 1 at position L; no internal carry has
been counted as an additional output column.

The symmetry of the motif list implies

    E + rev_L E = sum_j x^(s_j) (E_j + rev_(a_j) E_j) = R.

Pairing the actual digits E+H with their global reflection proves (1).
This argument allows corrections to meet or overlap; polynomial addition
accounts for every such column.

Evaluating (1) at x=1 also gives the exact seam mass loss

    mass(G(A_1...A_m))
      = sum_j mass(G(A_j)) - 18 sum_(j=2,...,m) r_j.  (4)

The corresponding ordinary digit-sum loss relative to the independent
component outputs is 9 times the sum of these neutral-run lengths. Formula
(4) does not assert a monotonic digit sum along the actual whole orbit.

## 3. A parameterized obstruction to bounded-radius seam repair

For every r>=1, take the valid finite motif

    A_r = 9^r · 10 · 10 · 9^r.

Its length is a=2r+2, and its two incoming-carry transfer values are both 1.
Its isolated update is

    G(A_r) = 10 · 9^(r-1) · 0 · 2 · 0 · 9^(r-1) · 10.

Formula (1) gives the exact full boundary identity

    G(A_r A_r) =
      10 · 9^(r-1) · 0 · 2 · 1 · 0^(2r-1)
         · 1 · 2 · 0 · 9^(r-1) · 10.                (5)

Relative to the endpoint overlap of two isolated G(A_r), the correction is

| Position relative to the seam a | Coefficient correction |
|---|---:|
| 0 | -20 |
| +/-j, 1<=j<r | -9 |
| +/-r | +1 |
| All other positions | 0 |

In particular, the correction has a nonzero coefficient exactly r columns
away from the seam. For every fixed repair radius K, choose r>K. No rule
that changes only the K columns on each side of this seam can turn the
independent overlap into the correct output. This is an all-parameter
obstruction, not an observation from long simulated trajectories.

The two carry-transfer bits do not reveal this radius: every A_r has the
same constant-one carry transfer. Keeping r makes the first update exact,
but there is no claim that the sequence of these radii closes under G.
This excludes bounded spatial support for the repair, not parameterized
run descriptions, finite-state transducers that scan an arbitrary run, or
context-sensitive grammars.

## 4. The overlap substitution does not close at the next step

The simplest canonical one-column atoms in the high-reset domain are
10,12,14,16,18. For A=(14), two copies have the exact first update

    G(14,14) = (5,10,5) = (5,5) overlap (5,5).

But the next actual update and independently updated components disagree:

    G(5,10,5)                     = (11,0,11),
    G(5,5) overlap G(5,5)         = (10,20,10).       (6)

The target has an inadmissible coefficient 20. This is a coefficient error
despite equal lengths; endpoint overlap repairs the previous length error
but does not make the dynamics a homomorphism. The concrete nonpalindromic
canonical seed is 95, with ordinary trajectory

    95 -> 154 -> 605 -> 1111.

Thus this proposed elementary recursion actually reaches a palindrome.
Among the eligible one-column even atoms, 14 is the smallest that fails
on this second update: the internal seams for atoms 10 and 12 still have
no carry on that step. This is not a claim of minimality among all possible
motifs or all finite seeds.

More generally, let a in {14,15,16,17}, p=a-9, and m>=2. The input a^m is
canonical whenever m is even or a is even. Its first update is

    G(a^m) = p · (2p)^(m-1) · p.

For m=2,

    G^2(a^2) = (2p+1, 4p-20, 2p+1).

For every m>=3,

    G^2(a^m) =
      (2p+1, 4p-19) · (4p-18)^(m-3) · (4p-19, 2p+1). (7)

These formulas follow by normalizing the first low endpoint with carry
zero, passing carry one through every internal coefficient 2p, and resetting
it at the final endpoint p<=8. In contrast, the independent overlap target
contains internal coefficient 4p>=20. Formula (7) is a whole parameterized
collision obstruction, not a bounded orbit search.

## 5. A general five-step obstruction to independent fixed overlaps

Consider any proposed representation by finitely many independently
evolving, positive canonical pair words B_j(t)=G^t(B_j(0)). Suppose the
representation joins adjacent words with fixed overlap depths d_j, so its
literal width at every time is

    W_t = sum_j |B_j(t)| - sum_j d_j.                (8)

Endpoint overlap is d_j=1. The same argument includes fixed zero or larger
overlaps, provided the representation is defined and its stated width is
indeed (8). No cancellation or trimming of outer columns is permitted.

If h_j(t) is the component's overflow flag, (8) implies

    W_(t+1)-W_t = sum_j h_j(t).

An actual ordinary reverse-and-add step increases width by at most one.
Therefore exact stepwise independent evolution requires

    sum_j h_j(t) <= 1                              (9)

at every update. In a reflection-symmetric decomposition containing two
copies of a positive component, those copies overflow simultaneously.
Their first overflow contradicts (9). Every positive component must
eventually overflow, so such a fixed independent decomposition cannot be
an all-time invariant.

The existing unconditional theorem

    width(T^5(n)) >= width(n)+1

sharpens this to failure within five updates from any putative exact
splice state. It is the r=5 instance of
`DecimalFiniteAncestry.numeric_width_five_floor`, already checked in
`../../ancestry_direct_pass/lean/FiniteAncestry.lean`. Every canonical
component has an ordinary realization, so the theorem applies to each
component orbit. This branch does not add a new Lean formalization of the
splice argument.

The bound is an obstruction to **stepwise independent evolution with fixed
overlaps**. It does not exclude variable-depth overlaps, a substitution
that changes the component list, genuine coupled seam evolution, or a
variable-time return identity that allows intermediate words to leave
the representation.

## 6. Verification and what remains open

Run from the project root:

    python -B main_existence_attempt/correlation_pass/constructive/seam_overlap.py

The checker uses literal integer reversal and addition independently of
the carry-based prediction on 7,296 arbitrary motif-list cases. These
include unequal motif lengths, several simultaneous seams, all nine high
reset values, neutral prefixes, internal arbitrary coefficients, and both
central parities. Each case also checks every individual motif against
literal arithmetic and checks the exact mass formula (4).

There are 67 literal controls for (5), including r=1000, and 384 controls
for (7), covering all canonical parities in the stated range. Those controls
audit the implementation; the arbitrary-length proofs are the symbolic
carry calculations above. The script also records the first failure of
the independent overlap rule for all five one-column even atoms. Measured
from the first splice state, failure occurs at updates 4,2,1,1,1 for atoms
10,12,14,16,18 respectively. None survives five updates.

The promising part retained here is the exact coupled seam normalization:
the first return can be written without extra digits, and the precise
neutral context and its mass cost are visible. The missing constructive
step is a parameterized or recursive rule for the **updated** motifs and
seams, together with a nonpalindromicity invariant. Neither the collision
identity, the unbounded repair radius, nor the fixed-overlap obstruction
supplies that rule or proves decimal Lychrel existence.
