# Exact non-nine period phase: author verification

Agent #1 specialist `/root/verification_plan`; task `agent1-periodic-phase-catalog-20261016`, accepted claim `6db01dafab1ec876d24c9964bc6086440ed21266`.

Frozen source: `proofs/Agent1PeriodicPhase.lean`.

- SHA-256: `705c139614ffd4f9f20a305f7c4bff20059da0c7fa127ca180ff8a88397a51ce`.
- Imports only `Agent1PeriodicGuard` and its unchanged ten-module transitive project dependency closure.
- No source edits after successful attempt 001.
- Parent remains sole Git writer. No external coordination message or Git mutation was performed by this specialist.

The new `phaseImage w g` uses the original `fixedDigits`, `terminalCarry`, and `zipperPeriod`. The main endpoint is:

```lean
theorem Agent1.Periodic.rawPeriod_eq_phaseImage (B H w : Agent8.Word)
    (hB : Agent8.Bounded B 18) (hH : Agent8.Bounded H 18)
    (hw : Agent8.Bounded w 18) (hlen : w.length = 4)
    (hne : w ≠ [9,9,9,9]) :
    Agent1.Periodic.rawPeriod B H w =
      Agent1.Periodic.phaseImage w (Agent1.Periodic.rawGamma B H w)
```

The clock is the actual original whole-word terminal carry. Both boundary entry carries disappear by applying the original `IncomingCarry.carryIn_eq_of_nonNine`, through the unchanged list/indexed bridge. Symmetry, exterior positivity, and integer realizability are unnecessary for this arithmetic identity. The all-nine exception is explicit and is handled in the separate specialist module. No phase graph search, finite-interface return, or safe infinite orbit is asserted.

Public declarations are `phaseImage`, `mem_nonNine_of_length_four`, `reverse_ne_nines`, `terminalCarry_eq_of_nonNine`, and `rawPeriod_eq_phaseImage` in namespace `Agent1.Periodic`.

## Executed checks

`attempt-001/run.json` records the first and only source compilation, exit 0 in 0.250 seconds:

```
/workspace/p196-tools/lean-4.19.0-linux/bin/lean --trust=0 -j1 -DElab.async=false -o Agent1PeriodicPhase.olean Agent1PeriodicPhase.lean
```

Working directory is this evidence directory's `attempt-001`. `LEAN_PATH` contains that directory followed by:

`/workspace/p196-agent1-session-20261016/periodic-zero-escape-parent-clean-001/agent1-periodic-zero-escape/source`

The source and object hashes of the exact ten imported dependency modules, original flattened paths, parent PASS receipt hash, and original source commit `6145e2aa53861bdf6c7a820dd8ee78da9abc014f` are retained in `attempt-001/dependencies.json`. These objects were reused from the parent's fresh 26-module build. This run is **an author increment, not a new independent clean rebuild**.

The produced `Agent1PeriodicPhase.olean` SHA-256 is `b589178df51c92967831984856fc169ee38f235b90482e729a85ee7ba9c8987c`. Its hash is retained in receipts; the generated object is not a source artifact required for publication.

`audit-002/run.json` records the successful complete module-origin audit, exit 0 in 1.508 seconds, again with `--trust=0 -j1 -DElab.async=false`. It uses the same explicit dependency path and executes `PhaseAudit.lean` from `audit-002`.

- Literal type and `#print axioms` checks cover all four public theorems and the public definition.
- The module-origin scan checks **all seven theorem constants**, including generated proof declarations, and the one safe definition.
- Axiom union is exactly `[Classical.choice, Quot.sound, propext]`; every theorem and safe definition has only permitted logical dependencies.
- `phaseImage` and `mem_nonNine_of_length_four` are axiom-free; `reverse_ne_nines` uses only `propext`; the carry wrapper and main endpoint use the permitted three standard axioms.
- No new axiom, admitted proof, or compiler-trusted theorem enters the accepted chain. Source scanning also rejects `sorry`, `admit`, `sorryAx`, `native_decide`, and explicit axiom declarations.

The first audit attempt failed because its helper rejected Lean's generated executable definitions `phaseImage._cstage1` and `phaseImage._cstage2`. This was an audit-helper classification error, not a theorem or source compilation failure. Its exact helper source, log, driver, and exit record remain under `audit-001`. The corrected audit names only these two compiler implementation definitions as such, continues to reject other non-safe definitions, and checks the logical dependencies of every theorem and the actual safe `phaseImage` definition. Both compiler definitions are reported in the successful receipt and are not theorem evidence.

The exact compiler SHA-256 is `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023` (official Lean 4.19.0).

The parent owns catalog assembly and publication. A separate reviewer owns the full fresh combined closure build and semantic review; no result from that future run is claimed here.
