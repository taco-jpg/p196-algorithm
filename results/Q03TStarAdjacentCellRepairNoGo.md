# Q03TStarAdjacentCellRepairNoGo

**Label: PAPER PROOF.** For every deep U3 first-contact gate in the rooted p12/m9 T* family, changing only the contact coefficient j and its mirror plus the immediately adjacent coefficient j+1 and its mirror cannot make the successor pairwords agree through j+1.
- For g=0, the residual equation is 2ε+s−10u=0, impossible by parity because s=±1 and u∈{−1,0,1}.
- For g=1, the exact threshold split gives residual y−10 or y−19 when s=+1, and y+1 or y−8 when s=−1; none vanishes for y∈[0,18]. The q=0/18 port restrictions only remove cases.
- **COMPUTED controls:** exhaustively tested all 19 adjacent replacements for each of 3,600 U3/phase gates: 68,400 genuine canonical-integer edits; bigint and schoolbook digit-array reverse-add agree.
- Reproduce: python3 calculation/new_structures/Q03/tstar_u3_first_contact.py; full proof: reports/Q03TStarU3FirstContact.md.
**REDIRECT:** exclude adjacent two-cell repair patches; any viable return needs a non-adjacent correction or a wider moving interface/carry state.
**Scope:** local all-width no-go for support {j,j+1} and its reflection only; not a full T* obstruction or a decimal Lychrel certificate.
