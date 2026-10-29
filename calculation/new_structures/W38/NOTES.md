# W38 running notes

- Read the owner instructions, OPEN_PROBLEMS.md, docs/FOCUS_SWARM.md, AUDIT_N.md, AUDIT_Nseries.md, lattice_formats/FORMATS.md, the current #475 FEED/DONE/ALERT lines, and the late #474 FEED/COMBINE history.
- Correctly retained the odd-centre-only mod-11 gate; no such gate was applied to even centres (outside this shard).
- For U=(9,16,2), A(U)=6 mod 11; the gates force A(J)=3 mod 11 for J3 and A(J)=8 mod 11 for J4, leaving 626+11,844=12,470 junctions. The midpoint of C is forced to 16 for lengths 3/7/11 and 6 for lengths 5/9/13.
- R02's MDD was not used: direct enumeration of all post-gate J words is complete and avoids relying on a prefilter.
- screen.cpp exhaustive exact digit-array screen PASS at q=k=20,40,80,160: every one of the 12,470 junctions has clock (1000)^30, no W9-prefix preservation, and first mismatch offset histogram identical at all four widths.
- Independent bigint vs fresh-buffer digit-array controls PASS: 72 cases, all six allowed odd-centre lengths, three admissible J representatives, four widths, 120 steps each.
- R30 symbolic verifier controls PASS for three representative J words; first mismatches are 9q+11, 9q+12, 9q+11, respectively, with exact 30-overflow clock and phasewise odd-pair guard. The 9q+11 control also passes for all six legal centre lengths.
- All-width reduction: exact symbolic bulk trace has 242 W-band and 242 U-band run occurrences across states 0..120, none all-9. Each repeated block therefore has constant carry transfer; the 30-overflow cone cannot reach B or C for q,k>=20 (mismatch window remains at least 155 coefficients from B and 78 from C). This makes the finite J quotient centre/exponent independent and supports the scoped EXHAUSTED-NONE claim.
- Registered the exact route in #475. The first attempt hit a secondary rate limit; the retry succeeded.
- No Lean files are added. The full repository tools/verify.py --changed command could not be run here because no local repository checkout is mounted; the C++ exhaustive screen and independent Python controls were run locally.
