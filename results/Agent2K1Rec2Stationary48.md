# Agent2K1Rec2Stationary48
**COMPUTED.** Decimal p=8, g=10101010, rec2 spatial m=48,
fixed first-defect x=107+j (or x+48q), j=0..47, all time phases.
The corrected exact necessary k-column graph has no cyclic state for
46 of 48 classes, so no permanently stationary off-lattice first defect
exists at ANY width in those classes (not a moving-front exclusion).
First vanishing k for j=0..23 (same for j+24):
2,2,24,4,6,2,4,3,3,4,CAPPED,4,2,2,8,4,2,5,7,2,2,3,4,3.
Unresolved j=10,34: k=14 has 25,140,401 candidates and 4,884,451
survivors in the two-sided core; k=15 has 92,804,569 candidates,
exceeding the declared 60,000,000 candidate cap. **UNDECIDED.**
Data/control: `agent2_rec2_data.py` checks all 384 bulk transitions and
carries. Reproduce using `agent2_rec2_stationary.cpp` with `lat2.txt`.
No unrestricted kink, decimal Lychrel certificate, or 196 claim.