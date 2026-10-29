# Agent Q03 formal target (migrated to current T*)

## Ultimate target
Find fixed finite J, fixed realizable palindromic coefficient centre C, and one charge-zero U3 motif U=(9,a,18-a), with even a, such that for every independent q>=14,k>=100, the canonical rooted decimal family

P(q,k)=B ++ W^q ++ J ++ U^k ++ C ++ reverse(U)^k ++ reverse(J) ++ reverse(W)^q ++ reverse(B)

has an exact 120 ordinary reverse-and-add step return P(q,k) -> P(q,k+5), with every intermediate state nonpalindromic and every phase's complete two-ended carry/overflow state restored. The published T12 paired-insertion theorem reduces this fixed-J,C,U return claim to the finite instance (q,k)=(14,100); full physical seam equality and phase guards still have to be checked.

## Q03 proved sublemma
For any deep U3-bulk contact site in any of the 30 U3 motifs over all 120 rooted p12/m9 phases, if a one-cell mirrored source perturbation preserves the next pairword prefix through the first changed coefficient and has the same overflow, the only possible gate is:
- g=0: the unique 9 -> 4 with carries (1,0), or 9 -> 14 with carries (0,1);
- g=1: the even coefficient immediately before the unique 9, x -> x+9 for x<=8 with carries (1,1), or x -> x-9 for x>=10 with carries (0,0).
The exact all-width statement and independent physical controls are in reports/Q03TStarU3FirstContact.md and calculation/new_structures/Q03/tstar_u3_first_contact.py. The successor does not erase the gate: g=0 emits a reflected ±1 pair one column inward; g=1 emits a reflected two-column (∓10,±1) packet, with every other coefficient unchanged.

## Remaining missing implication
The local gate must be embedded in a physically reachable finite seam/carry state that returns after 120 ordinary steps while keeping q fixed and gaining five U3 copies. First-contact equality is not full-interface equality and does not by itself imply a decimal Lychrel number.

Adjacent-cell constraint: the first-contact gate's successor packet cannot be absorbed by changing only the immediately next coefficient and its mirror. A return must use a non-adjacent correction or a wider moving interface/carry state.
