# Rules for contributors (people and agents)

The repository has one branch, `main`, and it must always pass `python3 tools/verify.py`.

1. **One branch.** Do not create branches or pull requests on this repository. Work in your own clone or fork;
   when a change is finished and `python3 tools/verify.py` passes, give the owner one patch (or one fork commit).
   The owner reviews it, re-runs `verify.py`, and pushes it to `main`.
2. **Every Lean file is part of a registered result.** A new result is a new directory `lean/P196/<ResultName>/`
   plus one entry in `lean/registry.json` with: `scope` (one paragraph, including what is *not* claimed),
   `roots`, `modules`, `endpoints` (the theorems a reader should trust). `verify.py` rejects unregistered files.
3. **No duplicates.** Import existing modules instead of copying them; `verify.py` rejects byte-identical files.
   Before proving something, search `RESULTS.md` and `lean/registry.json` for an existing statement.
4. **No escape hatches.** No `sorry`, `admit`, custom `axiom` or `native_decide`. Allowed axioms: `propext`,
   `Classical.choice`, `Quot.sound`.
5. **Commit results, not process.** No logs, review transcripts, evidence bundles, base64 archives, probe files or
   failed attempts in the repository. Keep those locally.
6. **Update `RESULTS.md`** with the new result in the right topic section.
7. **Computation** goes in `calculation/`: release zips named `lychrel196_v<N>[_<suffix>].zip`, math packages
   `math_v<N>.zip`, and the single engine page `196-Engine-Fixed.html`.

Toolchain: Lean 4.19.0 (pinned in `lean/lean-toolchain`), no Mathlib.
