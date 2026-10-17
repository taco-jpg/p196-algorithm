# CycleGuard author receipt

Accepted claim: `b4dc82e6d8d521b4295236f171b8d9e1a1d690cd`.
Author: Agent1 specialist `cap4_existing_theorems`.
Root remains sole Git writer and owns the combined numeric adapter.

Frozen source: `proofs/Agent1PeriodicCycleGuard.lean`.
SHA-256:
`357d626233997cd7b1d9b2606c63f196814854abd29f7e72a1a51254c9aa2041`.
Direct imports are exactly `Agent1PeriodicGuardedPath` and
`Agent1PeriodicReturnClock`. The final exact source and compiled object are
retained in `attempt-003/`; no source changes are planned after that attempt.

## Checked interfaces

All public declarations are in namespace `Agent1.Periodic`.

- `quotientPathExponent_accounting B H w k0 N hguard` identifies the natural
  finite exponent with `k0 + quotientDeltaSum` over Int. The guard is required
  at every used source before any natural subtraction is linearized.
- `quotientCycleExponent B H w N G t` is the safe, axiom-free definition
  `quotientPathExponent B H w (2*N+3) (t%N) + (t/N)*G`.
- `quotientCycleExponent_guarded B H w N G hN t` proves its guard at every
  time for positive N and any natural G. It reuses the existing finite budget
  bound and never assumes that every individual signed shift is nonnegative.
- `quotientCycleExponent_step B H w N G hN hend t` proves the literal natural
  exponent recurrence at the remainder state, given the finite endpoint
  equality `finiteK N = 2*N+3+G`. Both the interior and wrap cases are checked.
- `quotient_return_guarded_schedule B H w N hp hv hN hreturn` gives exactly
  one function `k : Nat → Nat` with `k 0 = 2*N+3`, every guard `3≤k t`, and
  the literal recurrence using `B(t%N), H(t%N), w(t%N)` for every natural t.

The final theorem obtains the natural gain from the unchanged
`quotient_return_clock_gain`, combines its signed delta identity with guarded
finite accounting, and uses the concrete schedule. No quotient cycle is
constructed. There is no safety conclusion, arbitrary graph-path lift,
independent seed choice at successive horizons, or 196 claim. CyclePath is
not imported; its separately authored remainder-state interface is intended
for the parent CycleNumeric adapter.

## Retained execution evidence

All author compilation and audit commands use pinned Lean 4.19.0 commit
`6caaee842e94`, `--trust=0 -j1 -DElab.async=false`, with a 4 GiB address-space
limit. Exact commands, executable hash, source snapshots, dependency pins,
logs, timings and return codes are retained per attempt.

| Attempt | Actual result |
| --- | --- |
| `attempt-001` | Source compilation failed because `conv_lhs` is unavailable in this original dependency closure. Its failed elaboration and downstream error output are retained. No accepted theorem or audit result is claimed for this snapshot. |
| `attempt-002` | Source compilation passed after replacing that tactic with direct `congrArg`. Full-origin audit stopped at the compiler-generated unsafe runtime declaration `quotientCycleExponent._cstage1`; the mathematical source already matched the final frozen bytes. |
| `runtime-inventory-001` | Inventory command failed because command slicing accidentally included `-o` without its output filename. Exact command and Lean usage output retained. |
| `runtime-inventory-002` | Corrected read-only environment inventory passed and identified the safe definition plus precisely its `_cstage1` and `_cstage2` compiled implementations. |
| `attempt-003` | Unchanged final mathematical source compiled and full module-origin audit passed. The audit checks all 21 theorem constants, the sole safe definition, all four required public theorems, and inventories exactly the two named compiler runtime implementations. |

The final audit axiom union is exactly `propext`, `Classical.choice`, and
`Quot.sound`; the safe schedule definition and its equation theorem are
axiom-free. The only inventoried runtime names are:

```text
Agent1.Periodic.quotientCycleExponent._cstage1
Agent1.Periodic.quotientCycleExponent._cstage2
```

The audit rejects custom axioms, unexpected constant kinds, any other unsafe
definition, and unexpected safe definitions. It independently audits the safe
base definition; runtime entries are not treated as mathematical axioms.
Every public source declaration has a retained `#print axioms` report.

Attempt 003 compile: exit 0, 0.767 seconds, 469320 KiB maximum RSS.
Attempt 003 audit: exit 0, 1.569 seconds, 756176 KiB maximum RSS.
These timings are rounded; `commands.json` retains exact measurements.

Twenty-five dependency objects were reused after source-hash matching to
the frozen GuardedPath and ReturnClock registries. Their source/object hashes
and actual parent-clean build paths are retained in `dependencies.json`.
This is an **author increment**, not a fresh full-closure rebuild or an
independent acceptance result. Root and the independent reviewer own those
subsequent checks.

`manifest.json` inventories publication evidence other than itself and binary
runtime objects. `runtime-objects.json` inventories those objects separately.
Every failure and partial result remains intact. No Git writes or external
issue messages were performed by this author.
