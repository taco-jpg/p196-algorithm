# Checked original-Local transition coverage

`PrefixMachine.lean` is author LEAN-CHECKED at SHA-256
`4cb78f4a7b620049e15421ae8d859bfa6b28650280047a1f06fb761474c955a5`.
The actual Lean 4.19.0 `--trust=0` attempt 003 completed with exit zero
and all 27 explicit axiom reports. Only `propext` and `Quot.sound` occur.

The partial transition accepts Boolean inputs `false -> 5`, `true -> 14`
and an original carry triple. `machineStep_eq_some_iff` gives both
directions of correspondence with three unchanged original `Local`
relations. In particular, every original transition is represented;
the proof does not use only a sound subgraph as an upper bound.

The original Agent9 finite table and label uniqueness supply the carry
and label coverage. Checked first- and second-layer readouts exclude
coefficient nine before each needed uniqueness application. The initial
14 transition and empty-state absorption are separately proved. Prefix
execution satisfies the usual empty, cons, and concatenation identities.

Attempts 001, 002, and 003 are retained under `development/machine/`.
The second attempt failed while synthesizing finite decisions for
proposition-valued option matches. The final finite statements use
equality guards and total readouts; their mathematical transition scope
is unchanged. No compiler-trusted evaluation shortcut is used.

The concrete rejecting-word certificate, original-path induction and
actual-prefix count wrapper are still WIP at this checkpoint. The
generic binary block theorem remains conditional on its stated rejection
premise. No completed-center or mixed-clock conclusion is asserted.
