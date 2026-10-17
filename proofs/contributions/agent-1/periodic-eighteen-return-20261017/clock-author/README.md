# Actual indexed carry and raw quotient clock

Author: Agent 1 specialist `/root/research_status`. This is author verification,
not independent review. The parent is sole Git writer. Accepted parent task:
`fcb20cb967483a96aa46261642d748fd32d4f5d6`.

`Agent1PeriodicEighteenClock.lean` supplies three public theorems:

- `periodicWord_carry_eq_rawGamma`: for bounded B, H, and w and **every k>0**,
  the original `DecimalDigits.carry` of the complete indexed periodic word is
  exactly the existing `rawGamma B H w` read at exponent three.
- `quotient_path_actual_carry_step`: the existing `quotientClockSum` satisfies
  the literal indexed-carry recurrence at each positive-exponent source of a
  supplied finite quotient path.
- `quotient_path_actual_carry_sum`: any natural cumulative sequence starting
  at zero and satisfying that recurrence agrees with `quotientClockSum` for
  every t≤N, including N=0.

The first proof composes unchanged `scan_carry_stable`,
`terminalCarry_eq_carryIn`, and `carryIn_zero_eq_carry`. No carry arithmetic or
length law is reproved. Its hypotheses are weaker than full original validity:
neither a period length, center symmetry/parity, positive exterior, nor a safety
premise is necessary for this carry identity. The positive exponent remains
explicit; it is not claimed for k=0. The path adapters require guards only at
used sources i<N and impose no endpoint guard or natural-exponent recurrence.
They identify the sum of carries of the displayed words; the separate guarded
path theorem supplies actual successive-word evolution when needed.

The existing raw-clock API is `rawGamma`, not a declaration named
`rawPhaseStep`. No abstract clock bit is supplied as an assumption, and no
phase catalog is imported. Empty B/H and arbitrary bounded w are included in
the first endpoint. The existing `QuotientPath` supplies source bounds and the
period length in the finite adapters. This module has no RunAncestry import,
new sum definition, generic maximal-run theorem, return-existence conclusion,
or claim about 196.

## Actual verification

`attempt-001` is the only attempt. Compilation and the complete originating
module audit both exited 0 under official Lean 4.19.0, explicit `--trust=0`,
`-j1`, `-DElab.async=false`, default stack, 4 GiB address-space cap and a
600-second command timeout. All commands, source snapshots and original output
are retained. There were no failed attempts.

The audit inspects all imported constants whose originating module is
`Agent1PeriodicEighteenClock`; all six are theorem constants, including generated
proof helpers. It checks the presence and literal types of all three public
endpoints. All dependencies are within `propext`, `Classical.choice`, and
`Quot.sound`. There are zero new safe definitions, unsafe/compiler definitions,
opaque constants, or custom axioms; the audit rejects any non-theorem constant
originating in this module.

This is an **incremental author check**. Fifteen unchanged dependency objects
were reused from the parent's completed fresh CycleAdapter build at
`/workspace/p196-agent1-session-20261016/cycle-adapter-parent-clean-001/agent1-periodic-cycle-adapter/source`.
Each current dependency source and its prior build source were matched against
the existing registry SHA256. Both the source and object were copied into an
isolated attempt build; object hashes were checked after copying. The full
fifteen source snapshots and source/object pins are retained. No fresh full
closure or independent verification is claimed here.

## Replay and evidence

Run `python3 proofs/contributions/agent-1/periodic-eighteen-return-20261017/clock-author/run.py attempt-NEW`
from the contribution worktree. The driver refuses an existing attempt or build
directory. Its preserved default paths refer to the original environment;
additional verified object directories may be passed as positional arguments.
Every dependency source must match the pinned CycleNumeric registry before
reuse. The complete parent package's later fresh verification is the portable
source-only reproduction route.

`attempt-001/run.py` is the exact executed driver. `ClockAudit.lean` and the
attempt snapshot are byte-identical. `source-and-result.json` binds the current
source to the actual compilation and audit. `FILES.json` covers all retained
evidence except itself. Compiled objects remain outside the contribution.
