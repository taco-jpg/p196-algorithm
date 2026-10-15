# Independent clean rebuild: frozen preflight checkpoint

**Full rebuild status at this checkpoint: IN_PROGRESS.** This checkpoint is not a full-chain PASS and does not yet independently accept the numerical 739 endpoints. The ongoing rebuild is owned and executed by the new independent clean reviewer, not by the parent agent.

Exact published source commit: `957efa326b4b980391046598a0143cb7a7060242`.

Independent preflight **PASS**: all 383 local source modules match that commit byte for byte; the runner also matches the committed source. The source closure has 3,596,106 bytes and 3,464 explicit theorem declarations (counts are audit metadata). All sources were copied and hashed by the runner before source compilation began. No prebuilt local theorem objects are reused.

The official Lean 4.19.0 archive SHA256 is `6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe`. Its 1,476 selected compiler/shared-library/standard-object members exactly match the installation. The binary SHA256 is `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`; the release commit is `6caaee842e94`. This uses the previously recorded official release archive; no new independent download is claimed. The documented wrapper only preloads the inspected current-process `/proc/<pid>/exe` to `/proc/self/exe` compatibility shim. Its source, binary pins, dynamic symbols, and readlink disassembly are recorded. No inherited LD_PRELOAD or LD_LIBRARY_PATH override was present.

The accepted-source scan found no custom axiom, sorry/admit, unsafe metaprogram, native evaluator shortcut, or kernel-check bypass. Inspection of the official axiom collector confirms it traverses the checked kernel environment and includes every axiomInfo regardless of the unsafe flag. Consequently compiler-generated unsafe implementation declarations are acceptable only when none occurs transitively in any accepted theorem. That full theorem dependency gate remains pending until the run finishes.

The exact invocation is in `invocation.json`. It selects `Conclusion739` and `TerminalObstruction`, sets `--jobs 2 --require-committed`, and uses a completely new outside-repository directory: `/workspace/scratch/7649db1e242c/build104-independent-final/rebuild`. Each compiler uses `-j1 -DElab.async=false`; no memory cap is imposed. Math and runner sources remain frozen during this rebuild.

Only frozen preflight evidence is included here; live compilation logs have not been copied. Full substantive logs, final axiom audit, source/object/compiler pins, exit status, and independent post-build verification will be retained separately in the parent `review-final-clean` directory after completion. Duplicate source copies and compiled objects remain in scratch; exact committed originals and source hashes preserve reproducibility.
