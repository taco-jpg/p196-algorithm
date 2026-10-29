# AC10 failed paths and corrections
- One-step root/J mismatch at index 139/140 is independent of C for these U, but it only excludes the chosen J=[5] and must NOT be mistaken for a center-side exclusion.
- A sparse code prototype indexed the baseline successor one layer late; independent dense replay found a disagreement at t=1. Fixed the reference source/successor separation before running exhaustive cells.
- A strict-intermediate W9 MDD would be faster but is unsound for endpoint healing; deliberately excluded.
- |C|>=11 space grows to 24,760,990, 47,045,881, 470,458,810, 893,871,739 per U. Only 50,000 each are sampled; do not advertise these lengths as exhaustive.
- No repeating seam/center map or all-time decimal repair was found; focus next on carry-aware SCC/product rather than additional finite-horizon seeds.
