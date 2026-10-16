# Four mixed bands with independently variable gaps

No persistent safe language or decimal Lychrel witness is constructed.
This followup derives an exact positive-certificate architecture with two
independent gap parameters, then completely excludes its smallest specified
initial interface family. It does not change the frozen four-state DFA proof.

## Exact canonical family

Let B and A be finite coefficient blocks and C a nonempty symmetric block.
All coefficients lie in 0,...,18. B may be empty, but otherwise its first
coefficient is positive and its last is not 9. A is nonempty with neither
end 9. C has neither end 9 and has even center when its length is odd.
For integers g,h>=2 define the whole symmetric word

`Q(B,A,C;g,h) = B 9^g A 9^h C 9^h reverse(A) 9^g reverse(B)`.

This is canonical. In particular, empty B gives outside coefficient 9,
and zeros at the outside of A or C are allowed.

Normalize B,A,C,reverse(A),reverse(B) consecutively, carrying the outgoing
bit of each block into the next. Denote their original-width digit blocks
by `D_B,D_A,D_C,D_RA,D_RB`, the four intermediate carries by
`e0,e1,e2,e3`, and the actual final carry by gamma. The omitted 9-runs do
not change a carry, so these are precisely the whole-word carries for
every g,h. Both mirrored pairs of bands are mixed exactly when

`e0+e3=1` and `e1+e2=1`.

Put `z_i=9(1-e_i)`. Under these two equalities, the actual output digits are

`D_B,z0^g,D_A,z1^h,D_C,z2^h,D_RA,z3^g,D_RB,[gamma if gamma=1]`.

This gives an exact all-parameter transition. For gamma=0, set

`Braw=D_B+reverse(D_RB)`,

`Araw=D_A+reverse(D_RA)`,

`Craw=D_C+reverse(D_C)`.

Here each plus is coefficientwise. For gamma=1, set

`Braw=(D_B appended z0)+(1 prepended reverse(D_RB))`,

`Araw=(D_A appended z1)+(z3 prepended reverse(D_RA))`,

`Craw=pair(D_C appended z2)`,

where `pair(D)=D+reverse(D)`. Directly pairing the displayed ordinary digit
word yields, in both cases,

`G(Q(B,A,C;g,h))=Q(Braw,Araw,Craw;g-gamma,h-gamma)`.

The gamma=1 formula absorbs the first following neutral digit into each
finite block and shifts the reflected block by one digit. Each remaining
neutral position pairs complementary z values and is exactly 9. The clock
is computed from the entire canonical word; no local carry controls are free.

## Boundary absorption and the vector return condition

If Araw or Craw consists entirely of 9s, adjacent bands merge. The current
four-band mechanism then terminates. Otherwise strip uB trailing 9s from
Braw, vA leading and uA trailing 9s from Araw, and vC outer pairs of 9s
from Craw. Write the remaining blocks as B',A',C'. They are again canonical
interfaces, with B' possibly empty. Define

`delta_g=uB+vA-gamma`, `delta_h=uA+vC-gamma`.

Then the exact all-gap identity is

`G(Q(B,A,C;g,h))=Q(B',A',C';g+delta_g,h+delta_h)`.

A surviving edge additionally requires the two mixed equalities for the
new actual block carries. This is stronger than retaining just one active
seam; an exit is a failure of the tracked four-band mechanism, not a proof
of ordinary palindromicity.

If b,a,c are the block widths, the complete width identity is

`2b'+2a'+c'+2delta_g+2delta_h=2b+2a+c+gamma`.

Consider a nonempty cycle of finite interfaces. Summing gives

`2*(total_delta_g+total_delta_h)=total_gamma`.

Its right side must be positive. If every gamma were zero, no state could
have empty B: empty B and the outer mixed condition force gamma=1.
With nonempty B and no overflow, the positive outside coefficient at least
doubles at each step. It cannot return to its initial value. Thus a cycle
has strictly positive total gap gain.

To obtain a genuine infinite safe family, the cycle must have **nonnegative
gain in each coordinate**, not merely positive total gain. Choose g and h
large enough that every within-cycle prefix keeps both gaps at least two.
Each complete traversal then increases or preserves both gaps, so the exact
identities repeat forever. Every source has an active mixed 9-band and
therefore has a nonpalindromic next ordinary output. Its starting realization
also cannot be a palindrome because its folded word contains the odd pair
coefficient 9. A qualifying cycle would consequently supply a concrete
decimal Lychrel witness. No such cycle was found here.

This architecture is broader than a finite cycle of the two-band quotient:
the middle block of its outer pair of bands contains another variable gap
h. It can grow even while all three new finite interfaces repeat. It is
not equivalent to merely adding more DFA states to the previous SAT search.

## Exact finite failure and all retained bounds

The searched initial family has `B=(b), A=(a), C=(c)`, with b positive,
all three interface endpoints different from 9, c even, and both mixed
conditions true. There are exactly 765 such states. Every state was followed
until mixedness was lost or bands merged. Configured caps were 100,000 graph
states, 1,000 path steps, and total interface width 256. **No cap was reached.**

The complete reachable graph has 1,389 states, with 708 surviving edges,
564 mixed-condition-loss terminals, 45 outer/inner-band merges, and 72
central-band merges. No cycle occurs. Of the 765 seeds, 613 lose a mixed
condition, 60 undergo outer/inner merge, and 92 undergo central merge.
The strict DAG rank is at most 19, and each individual interface reaches
width at most 9. Initial g,h>=10 suffice to keep both tracked gaps at least
two through the corresponding terminating trajectories. Thus every member
of this stated all-gap family leaves this four-band mechanism within
19 actual updates.

`four_band_controls.json.gz` preserves the complete graph and every seed
path. `verify_four_band.py` imports no discovery code, reconstructs the
initial family and each graph transition using ordinary integer arithmetic,
checks all graph targets and complete reachability, and assigns strict DAG
ranks. It checks every state at gaps (2,2),(3,5),(6,3),(64,65): 5,556 ordinary
integer transitions. The four-band longest-path witness includes a concrete
ordinary seed and every tracked output. The written block identity proves
the all-gap claim; finite controls audit its implementation.

Arbitrary larger interfaces, other numbers of bands, and mechanisms that
change bulk coefficients remain unrestricted. A mixed-band-loss or merge
terminal can still be safe or later generate new 9s. No general safe-language
emptiness theorem or decimal termination theorem follows from this graph.

Reproduce from this directory:

```sh
python3 -B four_band.py
python3 -B verify_four_band.py
```
