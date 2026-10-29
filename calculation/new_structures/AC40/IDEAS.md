# AC40 idea log

- The strict-per-phase W9 MDD is inadequate for endpoint-only T* searches: rejected paths can damage and subsequently heal W9. Did not use it.
- Fixed 1- or 2-site junction obstructions and odd-centre mod-11 gates are insufficient for this six-site cell, especially because even C must be included. Did not use either to prune.
- Local negative diagnostic for the phase-7 W9 cut suggests site 137 is a useful necessary witness; replace the diagnostic by an unpruned full first-symbol-slice scan, with independent decimal big-integer controls.
- If the scan excludes this slice, the remaining phase-7 problem is J[0]=1..18, the other 29 U rotations, and arbitrary palindromic C; a finite exclusion does not itself repair the T* epoch-map defect.