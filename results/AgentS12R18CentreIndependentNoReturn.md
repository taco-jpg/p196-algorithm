# AgentS12R18CentreIndependentNoReturn
**COMPUTED:** For the fixed phase-4 rooted p12/m9 seam J24, U=(18,0,9), the all-width R18 mismatch already established by S08/verify.py is independent of the centre's content and length.
The carry-reset lemma applies at every phase because U_t and reverse(U_t) contain a coefficient other than 9; hence the successor pairword on B4 W4^q J24 is centre-independent.
For all independent q,k≥512 and every finite canonical palindromic C, including even-length C, the 120-step image mismatches the fixed k+5 target at index 9q+35 (actual 9, expected 5); the 240-step mismatch is at 9q+12 (actual 6, expected 5).
Reproducible controls: r18_center_independence.cpp (compiled digit-array) and r18_center_independence.py (independent native bigint), 64 cases across all 16 q,k pairs in {20,40,80,160} and four even centres, 240 steps each.
**Redirect:** changing C cannot repair this fixed R18 seam; alter J/U or permit a phase-moving seam.
**Scope:** this excludes only the fixed R18 J24/U family, not decimal Lychrel existence.