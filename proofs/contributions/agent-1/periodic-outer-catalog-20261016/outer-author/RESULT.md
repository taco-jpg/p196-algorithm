# Actual quotient outside-head bridge: author verification

Agent #1 specialist `/root/verification_plan`; accepted claim `db88a5c78fd5f67ac134031d8486c26df9201799`, original scope proposal issue #61 comment `6226182566`.

Frozen source: `proofs/Agent1PeriodicOuter.lean`.

- SHA-256: `b30b54bce57542a649208c29900d511e9cc4b64429fb4a48f8da2a387d040678`.
- Direct import: `Agent1PeriodicSafetyAlphabet`, with its unchanged eighteen-module project dependency closure.
- Source remained unchanged after its first successful compilation.
- No Git mutation, issue write, original arithmetic reproof, or graph search was performed by this specialist. Root owns publication and catalog assembly; another specialist owns the finite outer choices.

## Exact public interfaces

All declarations are in `Agent1.Periodic`:

```lean
def outside (B w : Agent8.Word) : Nat := (B ++ w).headD 0

theorem outside_bounds (B H w : Agent8.Word) (hv : ValidPeriodic B H w) :
    0 < outside B w ∧ outside B w ≤ 18

theorem quotient_outside_step (B H w : Agent8.Word) (hv : ValidPeriodic B H w) :
    let e := Agent8.lastInput (periodicWord B H w 3)
    e ≤ 1 ∧ rawGamma B H w = Agent8.overflow (outside B w) e ∧
      outside (quotientOuter B H w) (rawPeriod B H w) =
        Agent8.nextExterior (outside B w) e
```

The carry is the actual carry entering the final column of the exponent-three whole word. The actual clock is unchanged. The appended period supplies the physical head if the stored exterior is empty, including after complete stripping.

The proof directly uses `Agent8.canonical_step`, `terminalCarry_eq_actual_overflow`, `periodicWord_head`, `stripPeriodSuffix_outside`, and the existing raw-block length identity. The private helpers establish only nonemptiness and equality of heads under literal prefix extraction/stripping. No freely chosen bit or clock is introduced, and no interface return, safety, or infinite orbit is asserted.

## Executed compilation and audit

`attempt-001/run.json` records exit 0 in 0.240 seconds for:

```
/workspace/p196-tools/lean-4.19.0-linux/bin/lean --trust=0 -j1 -DElab.async=false -o Agent1PeriodicOuter.olean Agent1PeriodicOuter.lean
```

Working directory: this evidence directory's `attempt-001`.

The explicit `LEAN_PATH` contains, in order:

1. That `attempt-001` directory.
2. `/workspace/p196-agent1-session-20261016/periodic-phase-parent-clean-001/agent1-periodic-phase-catalog/source`.
3. `/workspace/p196-agent1-session-20261016/periodic-safety-review-clean-001`.

Seventeen unchanged validity dependency objects were reused from the parent's fresh phase build at source commit `e2ce8e1cd121b78ce839c120d0d475990f561b8f`; the reviewed exact `Agent1PeriodicSafetyAlphabet` object was reused from the safety review build. The shared seventeen source pins were checked identical in both source snapshots and the current checkout. All eighteen selected source/object hashes and both PASS receipt hashes are retained in `attempt-001/dependencies.json`.

This is **an author increment using prior objects, not an independent fresh rebuild**. The produced object has SHA-256 `e4ad6584db009d263d69cb4bafeadcd9d5a3123773d87017ae20ae36c6d2fe19`; it is retained locally and hashed in receipts but is not a publication source artifact.

`audit-001/run.json` records exit 0 in 1.580 seconds for `OuterAudit.lean`, with `--trust=0 -j1 -DElab.async=false`, its own explicit working directory, and the same dependency path.

- Three literal type/`#print axioms` pairs cover the two public theorems and `outside` definition.
- The full module-origin scan checks all **ten** new theorem constants, including private/generated proofs, and the one safe definition.
- The complete theorem axiom union is `[Classical.choice, Quot.sound, propext]`.
- `outside` is axiom-free; `outside_bounds` uses only `propext` and `Quot.sound`; `quotient_outside_step` uses the permitted standard three axioms.
- Lean's two generated executable implementation definitions `outside._cstage1` and `outside._cstage2` are separately inventoried. They are not proof evidence; every theorem's logical dependencies were checked independently of this classification.
- The audit rejects custom axioms, unexpected new declaration types, unrecognized non-safe definitions, and disallowed theorem/safe-definition axioms. The source scanner also rejects admitted proofs, `native_decide`, and explicit axiom declarations.

Both initial attempts passed. There were no failed source compilations or failed audit attempts in this module's development. Exact sources, drivers, commands, logs, exit codes and hashes are preserved rather than inferred from source inspection.

Official Lean 4.19.0 executable SHA-256: `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.

The parent and independent reviewer own the later combined clean build, complete product certificate review, and publication. No outcome of that later verification is claimed here.
