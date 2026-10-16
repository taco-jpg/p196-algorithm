# Path author verification

This directory retains the author's execution evidence for
`proofs/Agent107TransducerPath.lean`. Its ten exported theorems compile under
Lean 4.19.0 with `--trust=0 -j1 -DElab.async=false`. Every printed transitive
axiom report is exactly `propext, Quot.sound`; no excluded evaluation axiom
or unfinished proof occurs in the successful reports.

`manifest.json` pins the checked source, frozen definitions and logs. The
first failed attempt and its complete error log are preserved, outside the
accepted module. Build 02 completes the mathematical endpoints. Build 03
adds the remaining theorem audit commands without changing proofs. Both
successful compilations exited zero.

The author imports the separately compiled frozen definitions from
`agent107-build` and the independently built foundation from
`agent107-runtime/baseline`. This is an actual author compile, not a claim of
an independent clean dependency rebuild. The coordinator's fresh package
rebuild and separate interpretation review remain required.

## Scope

`actual_accepts` supplies a complete path for each original `Admissible`
word. `accepting_carries` reuses `even_folded_trace_sound` and
`odd_folded_trace_sound`; it does not replace those foundational proofs.
`accepting_state_eq_actual` then forces all five literal state fields on
indices at most `L / 2`. `exists_unique_finitePath` uses the actual
`List.ofFn` finite prefix; it deliberately does not assert equality of
arbitrary function tails. The center positivity test includes `L=1`.

`BoundaryChecks.lean` contains six compile-time controls: zero-width
rejection, two single-column carry cases, even-width overflow, an odd-width
overflow with delayed digit zero, and equality of finite traces despite
different unused tails. Its build exited zero. These controls are not
substitutes for the universal theorems and are not additional research
claims.

## Reproduction

From the repository root, after compiling the frozen dependencies:

```sh
LEAN_PATH=/workspace/scratch/94808c4aecb2/agent107-build:/workspace/scratch/94808c4aecb2/agent107-runtime/baseline \
  /workspace/scratch/94808c4aecb2/agent107-runtime/lean-4.19.0-linux/bin/lean \
  --trust=0 -j1 -DElab.async=false \
  -o /workspace/scratch/94808c4aecb2/agent107-path-build/Agent107TransducerPath.olean \
  proofs/Agent107TransducerPath.lean
```

For the controls, prepend `agent107-path-build` to `LEAN_PATH` and compile
`proofs/contributions/agent-107/folded-transducer-20261016/path-development/BoundaryChecks.lean`
with the same flags.
