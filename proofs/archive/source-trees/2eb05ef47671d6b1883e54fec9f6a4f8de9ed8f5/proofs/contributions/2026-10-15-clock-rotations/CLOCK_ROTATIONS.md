# The scalar clock bound applies at every starting phase

Let an admissible decimal pair word have width L and evolve by ordinary
reverse-and-add. Put a=(4,8,16,7,15,6,13). Suppose its outside coefficient
at times t=0,...,7R is a[(s+t) mod 7], for any starting phase s.
Then R <= 98. For L>=2 the more precise bound is

    R <= 94 + max(0, ceil((14-L)/3)).

For L>=14 it is R<=94. For L=1 no complete period occurs.
These are conservative bounds, not sharpness claims. Leaving this clock
does not imply a palindrome. This statement concerns the entire prescribed
scalar sequence, not isolated visits to outside coefficient 4.

## Proof from the retained certificate

The component-specific certificate in
`../2026-10-14-component-specific-bound/component_certificates.json.gz`
has root job 0 for the scalar hierarchy. Its seven start-phase path-vertex
bounds are all 659. Its root graph is one strongly connected component
containing all seven phase vertices. The previously reviewed actual-path
lifting argument and component-specific induction do not assume phase zero:
they bound an actual path starting in any root vertex by that vertex's
component rank. Thus at physical width at least 14 every matching clock
path has at most 658 edges, and 7R<=658 gives R<=94.

This uses the full existing induced-graph, projection and weighted-rank
certificate and its independent audit. The small checker here only checks
the stated corollary data; it does not replace that earlier audit or claim
a new kernel formalization of the numerical hierarchy.

For every transition of the prescribed scalar sequence the actual overflow
is forced by the outside coefficient. For outside coefficients less than 9
it is zero; for coefficients at least 10 it is one. None of these seven
coefficients is 9. Hence the overflow sequence by phase is
(0,0,1,0,1,0,1). Every seven consecutive phases, including a cyclic rotation,
increase width by exactly three. If L>=2, after
k=max(0,ceil((14-L)/3)) complete periods the width is at least 14.
If R<k the result is immediate; otherwise apply the 94-period bound to
the remaining R-k periods, whose start phase is still s. Since k<=4,
the uniform bound is 98.

For L=1 admissibility requires an even coefficient, so the only possible
starting clock values are 4,8,16,6. The literal one-column trajectories are:

* (4) -> (8) -> (16) -> (7,7) -> (14,14), failing the clock at time 4.
* (8) -> (16) -> (7,7) -> (14,14), failing at time 3.
* (16) -> (7,7) -> (14,14), failing at time 2.
* (6) -> (12), failing at time 1 (the prescribed next value is 13).

Thus none completes a period. Odd clock values cannot be a width-one
admissible pair word.

The same result applies at any time offset of an ordinary positive integer
orbit: use its actual pair word and width at that time. Admissibility is
preserved by the established normalization bridge. A fixed cyclic shift of
this clock therefore cannot become a perpetual eventual clock, even after
an arbitrary initial transient. This excludes only these seven rotations;
it does not exclude different clocks, changing clocks, or nonperiodic
outside-coefficient sequences.
