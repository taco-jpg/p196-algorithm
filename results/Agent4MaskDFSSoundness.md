# Agent4MaskDFSSoundness
**PAPER PROOF:** Conservative coefficient/carry bitmasks in the K1 solver
contain every exact valid centre trajectory after each finite step.
A fully exhausted zero-survivor width/H search therefore excludes
periodic centres of that width with any temporal period.
**COMPUTED controls:** 720 independent full-digit scalar-carry checks;
24 complete small-width enumerations and 6 prefix partition identities.
Base-26 control width 3 at H=30: survivor counts (4,2).
Run: python3 calculation/decimal_frontier/lattice_formats/agent4_mask_soundness/check.py
Same commit contains exact solver source, independent Python checker,
proof, three small inputs, and these reproduction/control commands.
**UNDECIDED:** Decimal neutral p11 width 13, p12 width 11, wider
centres and the base-10 Lychrel certificate.
