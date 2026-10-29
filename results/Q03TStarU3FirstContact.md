# Q03TStarU3FirstContact

**Label: PAPER PROOF.** For the rooted decimal p12/m9 T* family, all 30 charge-zero U3 motifs and all 120 temporal phases have exactly one physically realizable one-cell first-contact gate at a deep U3 site.
- No overflow: the unique 9 must change to 4 or 14, with carry ports (1,0) or (0,1) respectively.
- Overflow: the unique gate is the even coefficient immediately before 9; x≤8 changes to x+9 with ports (1,1), while x≥10 changes to x−9 with ports (0,0).
- All other cells fail the universal Q03 ±5/±9 gate conditions; carry reset makes this necessary table valid at every width, independent of J,C away from the seam.
- Exact post-contact transport: gamma=0 emits a reflected ±1 pair; gamma=1 emits reflected (∓10, ±1) two-cell packets, with all other successor coefficients unchanged.
- COMPUTED controls: 3,600 phase/motif rows, 10,800 actual carry ports and 16,560 one-cell edit checks; bigint and independent schoolbook digit-array engines agree.
- Reproduce: python3 calculation/new_structures/Q03/tstar_u3_first_contact.py; derivation: reports/Q03TStarU3FirstContact.md.
**Scope:** local first-contact necessity only; no full 120-step seam return, no positive-growth certificate, and no base-10 Lychrel existence claim.
