# T12: rooted decimal local-cut and insertion theorem

**Label: PAPER PROOF**, with finite two-carry arithmetic checks; not an existence proof.

Fix published rooted B34, W9, any U among the thirty rotations of (9,a,18-a) for even a=0..18, any fixed finite junction J, and any palindromic coefficient centre C with an even midpoint if odd length. Define H=B0 W0^q J U^k and P(q,k)=H C reverse(H), all coefficients LSD-first. For **all independent q>=14,k>=100**, 120 genuine decimal reverse-and-add steps have clock (1000)^30, with a W9 insertion after two W copies and a U3 insertion after 55 U copies commuting at every step. Consequently, for each fixed J,C,U, genuine Return(q,k): P_120(q,k)=P(q,k+5) holds for every such q,k **if and only if** it holds at the single literal width (q,k)=(14,100). Every intermediate phase has an odd coefficient in the rooted B row, so any successful return gives an all-time nonpalindromic orbit.

The exact conservative reset-cone losses are 91 columns from W toward its root, 150..152 at the U junction side and 120..122 at the U centre side. These are **not** claimed to be minimal physically attainable radii. The cut positions are cW=52 and cU=34+9q+|J|+165. The theorem does not bound J,C, discover a returning interface, or prove decimal Lychrel existence. See NOTES.md for the proof and cut.py for reproducible exact calculations.


**Sharp carry-port refinement (T12MinimalCarryCone):** the phase-locked 120-step local-causality radii are exactly 91 on the W side, 152 on the U junction side and 122 on the U centre side, minimal for arbitrary carry-inlet differences. For fixed J the seam window is at most 243+|J| pair coefficients. This is not a claim of minimal physically reachable defect radii.
