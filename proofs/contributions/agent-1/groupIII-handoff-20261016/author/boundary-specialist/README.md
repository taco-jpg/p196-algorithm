# Group III finite handoff boundary control

Claim: `507d0d3deb80563c7a4b228932bacd888af7e843`.

Canonical source: `attempt-002/Boundary.lean`. It compiles against the frozen reviewed `Agent1GroupIII` dependencies using Lean 4.19.0, explicit `LEAN_PATH`, and `--trust=0`. `attempt-002/command.sh` is the exact executed command script. Its compiler exit code is 0. The compiler log reports that all five exported theorems depend on no axioms.

The source proves component width 8 and exact finite columns `GroupIII.sixWord 1 16 8 5 9`, whole width 9, exact signed defect `[1,-20,1,0,0,0,1,-20,1]`, and failure of finite actual overlap at time four. The fixed initial parameters are r=1, p=1, u=10, v=6. This is a finite boundary control, not an all-r or recurrence result.

`attempt-001` preserves the first successful compilation using `omega` index splitting; its finite-index theorems depend only on the standard axioms `propext` and `Quot.sound`. `attempt-002` uses finite decidable quantifiers and removes these dependencies. There were no failed compiler attempts. Both source snapshots, exact commands, compiler logs, source/evidence hashes, version output, object files, and exit-status records are retained. `manifest.json` records the dependency and compiler hashes.

Only the assigned handoff-boundary directory was written. No repository sources, Git metadata, or external messages were changed by this specialist.
