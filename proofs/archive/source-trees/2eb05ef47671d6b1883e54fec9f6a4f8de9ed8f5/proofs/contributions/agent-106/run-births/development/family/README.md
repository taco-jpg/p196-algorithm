# BirthFamily development record

Final source: `../../BirthFamily.lean` (namespace `RunBirths.BirthFamily`).

For every natural `g >= 2`, the full source word has width `g + 6` and is
`(1,10,8),18^g,(8,10,1)`. Its actual recursive decimal carry has no final
overflow. Its exact `FoldedDecimal.nextColumns` successor is
`(3,0,18,17),18^(g-2),(17,18,0,3)` at the same width.
Both words are proved `Admissible`; a self-reflected center lies in the
coefficient-18 region and is therefore even, including odd values of `g`.

Core API:

- `source_admissible`, `target_admissible`.
- `actual_carry`, `no_overflow`, `actual_width`, `actual_update`.
- `two_new_births`: source coefficients 8 at positions 2 and g+3 become 18.
- `residual_core`: positions [4,g+2) retain old coefficient 18.
- `barriers_and_singletons`: old endpoints 3 and g+2 become 17; positions
  1 and g+4 become 0, making both newly born 18s singleton maximal runs.
- `core_lengths`: old and residual lengths are g and g-2, with g-2+2=g.
- `exact_18_positions`: no additional source or successor 18 positions.
- `numeric_canonical_next`: any canonical decimal realization has the
  explicitly given normalized digits as its exact numeric successor.
- `numeric_two_steps_safe`: any realization and its first two successors
  are nonpalindromic.
- `family_realized`: every g>=2 has a positive finite decimal realization
  satisfying that canonical-next and finite-safety package.

The package asserts one exact step. It does not assert closure of the
family, repeated regeneration, an infinite orbit, or membership in the
orbit of 196.

Compilation records:

1. `attempt_001.lean/log`: initial full source; three range/if simplification
   goals were unfinished. The corresponding error-recovery `sorryAx` output
   is a failed development artifact, not an accepted proof.
2. `attempt_002.lean/log`: all goals compile; one unused parameter warning.
3. `attempt_003.lean/log`: final source compiles with exit code 0 and no
   warnings. All 27 exported theorem declarations plus the private helper
   have `#print axioms`; only `propext`, `Classical.choice`, and `Quot.sound`
   occur. No `sorryAx`, custom axioms, or native decision proof appears.

Command used (from repository root):

```sh
LD_PRELOAD=/workspace/scratch/50e90e07524e/runtime/readlink_self.so \
LEAN_PATH=/workspace/scratch/50e90e07524e/build106 \
/workspace/scratch/50e90e07524e/runtime/lean-4.19.0-linux/bin/lean \
-o /workspace/scratch/50e90e07524e/build106/BirthFamily.olean \
proofs/contributions/agent-106/run-births/BirthFamily.lean
```

The reused technique is the explicit column-balance equation followed by
induction proving the computed carry, as in the existing
`RegenerationGate.lean` / `RegenerationGateDynamics.lean`. The final module
imports only `LychrelDigitSums`.
