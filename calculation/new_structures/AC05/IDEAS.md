# AC05 ideas and limitations

- Brute-force full decimal-digit replay is exact but too costly for large centres. A port-certified symmetric-window computation reduces cost; failure of a port equality triggers a full replay.
- Odd-centre mod-11 gates must never be imposed on even centres. No modular or strict-per-phase W9 pruning was used.
- Centre length 11..14 search remains partial. Its huge search space needs a sound symbolic pruner, not extrapolation from observed first mismatches.
- Fixed J=[5] and phase 0 are a restricted predicate. Other phases, growing/moving seams, and mixed U are not excluded.
- No moving-seam repair or all-time decimal certificate was found.
