# Author result: clock-one normalized-center obstruction

`Agent1.Periodic.centerPeriods_nines_clock_one` has passed strict incremental author compilation and a complete audit of the new module's originating declarations. Source: `proofs/Agent1PeriodicNinesClockStrip.lean`, SHA-256 `cf78db242e666ffaeb85444ee2347b97dac629a2dc6835c2ebf62b07f3a022d5`, Git blob `770b9ec5b6f0dbfa72986701d7ff41c87f6cf30d`. The source is frozen for root's publication and independent fresh verification. It imports only `Agent1PeriodicNinesCenter`.

The exact endpoint retains original validity, literal initial center normalization, actual mixed entries, and actual clock one:

```lean
theorem centerPeriods_nines_clock_one (B H : Word)
    (hv : ValidPeriodic B H [9,9,9,9])
    (hnorm : stripPeriodCenter [9,9,9,9] H = (H, 0))
    (hmix : leftEntry B + rightEntry B H [9,9,9,9] = 1)
    (hg : rawGamma B H [9,9,9,9] = 1) :
    centerPeriods B H [9,9,9,9] = 1
```

Thus only the mandatory mirrored outer period pair is removed. The theorem requires neither a nonempty quotient center nor a future nine transition. It does not prove a full-cycle obstruction. Applying it at every state of a return requires a separate proof of each state's literal initial normalization; that premise was not assumed from validity alone.

The private proof inverts one paired boundary nine at a time. Under mixed actual terminal carries, the padded paired image's outer nine forces an original outer coefficient nine. Symmetry permits peeling both original ends; the remaining center retains the same mixed-carry condition and padded-pair form. Four such inversions contradict initial maximal stripping. Empty and singleton cases are discharged using the mixed-carry condition; the implementation retains the full original `ValidPeriodic` public premise even though its odd-center-parity field is not needed by the private argument.

Author `/root/suffix_receipt_resume` ran official Lean 4.19.0 with `--trust=0 -j1 -DElab.async=false`. All attempts retain exact source copies, commands, exit statuses, logs, timestamps, and elapsed times. Attempts 002 onward also retain the driver and dependency object hashes. The 17 dependency source copies were checked against the frozen reviewed center registry and their existing objects were reused. **This was an incremental author check, not a fresh dependency rebuild or independent review.**

| Attempt | Result | Scope / preserved diagnostic |
| --- | --- | --- |
| 001 | FAIL, exit 1 | Private boundary-peel proof: arithmetic tactic could not close a modular case. |
| 002 | FAIL, exit 1 | Private boundary-peel proof: unavailable theorem-name spelling in a case split. |
| 003 | PASS, exit 0 | Private peel helper only; final public theorem was not present. |
| 004 | FAIL, exit 1 | Completed source: unresolved syntactically simplified strip-loop condition. The failed log's `sorryAx` output is retained and is not accepted evidence. |
| 005 | FAIL, exit 1 | Completed source: redundant tactic after the goal had closed. The failed log's `sorryAx` output is retained and is not accepted evidence. |
| 006 | PASS, exit 0 | Final frozen source; one harmless unnecessary-`simpa` linter warning. |
| audit-001 | PASS, exit 0 | All 16 new-origin theorem constants audited, including private/generated helpers; zero safe definitions. Literal public type and axiom output retained. |

The successful audit permits only `propext`, `Classical.choice`, and `Quot.sound`; it found no `sorryAx`, reduction axiom, or custom safe axiom. The endpoint uses those same three foundational axioms. Dependency audit/rebuild claims remain with the separately published center verification.

The initial bounded discovery remains separately labeled in `DISCOVERY.md`. It completed 24,966 constructed cases within its 30,000-case/30-second budget and found no requested normalized drop-seven witness. There were 7,665 normalized/mixed/clock-one cases and zero additional strips among them. Removing normalization gave 2,023 computational drop-seven controls with a further actual nine transition. These counts motivated the exact theorem but were not used as its proof. The recorded unnormalized controls were not separately Lean-compiled, and no public control theorem was added.

The initial sharpness assignment was accepted at claim `4a96b34d8991f7cb13484e6dc25548ea7870f271`; the precise clock-one obstruction refinement was read back through the actual GitHub API at `9d09aea2edccfceb174f6cfd31142ba1b0c09226` before substantive proof work. The genuine specialist's issue check-in was accepted and fetched back at [6228609594](https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6228609594). No other agent acknowledgment or Git publication is inferred. Root is the sole Git writer and owns the result publication.

`final-receipt.json` and `FILES.json` seal this author evidence. The manifest excludes itself, `SEAL.json`, local compiled objects, and Python caches; no excluded object is needed to inspect the retained source and compiler/audit logs. `.gitignore` prevents publishing those local objects. Failed attempts and their diagnostics remain unchanged.
