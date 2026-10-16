# Merged-candidate clean verification: frozen preflight checkpoint

**Full merged rebuild status at this checkpoint: IN_PROGRESS.** This is a preflight PASS, not an accepted merged full-chain result. The earlier contribution-only independent PASS remains frozen separately.

Published candidate commit: `4bdd59bdc8f3e8f0556c3decb0898e6c6f271b29`. Candidate tree: `0185512ec6de577246450e83d703f11d84687ce4`.

All 383 accepted Lean sources and the checker match the published candidate bytes. The source hashes are also identical to the earlier independently checked contribution, but no local compiled object is reused. The candidate is undergoing a separate fresh source-only build in `/workspace/scratch/7649db1e242c/build104-integrated/rebuild`, selecting `Conclusion739` and `TerminalObstruction` with `--jobs 2 --require-committed`. Each compiler runs with `-j1 -DElab.async=false`. No memory cap is imposed.

Official Lean 4.19.0 release commit `6caaee842e94` is pinned. Archive SHA256: `6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe`; compiler binary SHA256: `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`. All 1,476 selected compiler/shared-library/standard-object archive members were compared anew with the installation. The prior official archive is reused, independently hashed; no fresh network download is claimed.

The transparent current-process `/proc/<pid>/exe` compatibility shim is source/binary pinned and its exported symbols, readlink disassembly, and read-only data are retained. No inherited preload/library override is present. The official axiom collector source is independently matched to the archive and explicitly traverses every transitive `axiomInfo`, including unsafe entries. Compiler-generated unsafe implementation declarations are acceptable only if none occurs in any accepted theorem's dependencies. The final exhaustive gate will allow only `propext`, `Classical.choice`, and `Quot.sound`.

The mathematical scope remains the unrestricted-width 39-step ancestry bound for palindromes beginning 739 and all-time exclusion of that restricted family from the ordinary 196 orbit. It does not settle P196.

This directory contains frozen preflight controls, invocation, pins, provenance, and toolchain inspection only. No live compiler log is copied here. Final complete logs, exit status, theorem inventory, post-build pin validation, and source recovery instructions will be added in the parent `integration-verified` directory after actual completion. Duplicate sources, local compiled objects, and runtime infrastructure remain outside the repository.
