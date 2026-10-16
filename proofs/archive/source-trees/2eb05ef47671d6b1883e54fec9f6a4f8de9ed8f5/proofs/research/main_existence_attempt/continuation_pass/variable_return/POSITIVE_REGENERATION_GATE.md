# A safe +4 neutral-band gate and its exact failed return

This is a finite positive construction, valid for every parameter value.
It is not an infinite invariant, and no decimal Lychrel existence result
or theorem about 196 is asserted.

Write W(B,H,g)=B 9^g H 9^g reverse(B), in low-to-high pair-sum order.
Put

    B=(1,9,12,3,14,14),    H=(4,4,15,10,15,4,4),
    C=(3,9,4,8),          J=(11,2,11).

For **every integer g>=0**, the actual no-overflow identity is

    G(W(B,H,g)) = W(C,J,g+4).                            (1)

Both the first and second ordinary reverse-and-add outputs are
nonpalindromic. At g=0, this creates two length-four neutral bands from an
input with no spacer between these interfaces. This primitive was found
inside the complete 4/14 interface graph; it is not a fitted trajectory.

## Exact carries, width, and safety

Normalize B from carry zero. Its digits and outgoing carry are

    (1,9,2,4,4,5),  1.

The first 9^g therefore emits 0^g and retains carry 1. Normalize H
from that carry, obtaining

    (5,4,5,1,6,5,4),  0.

The second band emits 9^g. Normalizing reverse(B) from carry zero gives

    (4,5,4,2,0,2),  0.

The final zero carry is the actual whole-word overflow bit. Thus the
decimal digit word is exactly the concatenation of these three digit
blocks with intervening 0^g and 9^g. This remains true at g=0. Pairing
with its reversal in the same actual width gives raw interface blocks

    Braw=(3,9,4,8,9,9),
    Hraw=(9,9,11,2,11,9,9).

Two terminal nines from Braw and two outer nines from Hraw join each
band. This proves (1), including its +4 parameter update.

The input width and output width are both 2g+19. All coefficients lie
in 0..18, both words are symmetric with positive outer coefficient,
and their middle coefficients are respectively 10 and 2. They are
therefore canonical and have finite positive decimal realizations.

The first output has outer pair coefficient 3, which is odd, so it
cannot itself be a palindrome. Its pair word has coefficient 11 and
outer coefficient 3. It is neither of the exact palindrome-predecessor
types (all coefficients <=9, or exclusively 0/11 with outer 11), so its
next ordinary output is also nonpalindromic. Alternatively, both states
have the intrinsic high-to-nine seam certified by the seam stream's
formal safety theorem. No future seam persistence is inferred.

## The originating family and all subsequent interfaces

The gate is reached after three overflowing steps from the smaller
interface family with B0=(18,18,4), H0=(14,0,0,14), and gap R>=3.
The table gives **the exact whole pair word at every listed time**:
B_t a_t^(R+d_t) H_t a_t^(R+d_t) reverse(B_t).

| t | B_t | H_t | a_t | d_t |
|---:|---|---|---:|---:|
| 0 | (18,18,4) | (14,0,0,14) | 9 | 0 |
| 1 | (9,18,13,14) | (4,5,0,5,4) | 9 | -1 |
| 2 | (10,8,13,9,4) | (14,9,5,5,9,14) | 9 | -2 |
| 3 | (1,9,12,3,14,14) | (4,4,15,10,15,4,4) | 9 | -3 |
| 4 | (3,9,4,8) | (11,2,11) | 9 | +1 |
| 5 | (6,18,8,17) | (2,6,2) | 9 | +1 |
| 6 | (13,16,18,14) | (5,12,5) | 9 | +1 |
| 7 | (4,11,16,14,4) | (15,8,8,15) | 9 | 0 |
| 8 | (9,3,14,9,10) | (10,17,17,10) | 9 | 0 |
| 9 | (18,7,9,0,2) | (2,16,16,2) | 0 | 0 |

The actual overflow clock for these nine transitions is
`1,1,1,0,0,0,1,0,0`. Every positive ordinary output through time nine
is nonpalindromic, uniformly for R>=3. At R=3 the gate occurs with g=0;
this minimum boundary is included by literal integer arithmetic and the
direct digit proof of (1).

At time eight both sides of each neutral band send carry 1, so mixedness
has been lost. On the next no-overflow step both digit contributions
inside each band are zero, giving the explicit 0^R reservoirs at time
nine. Thus the gate's mixed bands fail after five updates from the gate
and become zero after six; safety through this finite segment survives.

The four-step composite has increased the gap from R to R+1, but its
interfaces are C,J, not B0,H0. When the outer coefficient first returns
to 18 at time nine, the whole width equals that of the original family
at parameter R+2. Nevertheless the actual second coefficient is 7,
whereas the proposed returned family's second coefficient is 18:

    G^9(W(B0,H0,R)) != W(B0,H0,R+2)     for every R>=3.    (2)

The reserve symbols also differ, zero versus nine. Therefore neither
the shared outer coefficient nor the matching width supplies the missing
return. Reversing the known originating path cannot identify these
different actual words.

## Certification and remaining construction problem

`regeneration_gate.py` produces all ten affine run states at R=4+k for
every k>=0, the nine exact transitions, and explicit ordinary-integer
controls including R=3. `check_regeneration_gate.py` imports neither the
generator nor its run normalizer; it recomputes the carry polynomials
and verifies the identities after multiplying by x-1. It also replays
the complete finite boundary trajectories. These are written and
exact-arithmetic certificates, not new Lean declarations.

The isolated proof (1) supplies actual band regeneration and two-step
safety. The extended trace supplies a genuine earlier construction and
a concrete failed return. A long zero band retains a zero interior under
any fixed number of further updates; see the seam stream's
`../seam_persistence/followup_absorbing_core/ABSORBING_CORE.md` for the
precise finite-propagation theorem. Restoring an unbounded neutral
band after this loss therefore needs fronts to traverse a distance that
grows with R, or a different source of growing 9 bands. No such variable-
time reset, no matching later interfaces, and no closed parameter map
have been proved here.
