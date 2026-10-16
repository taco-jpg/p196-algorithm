# Agent #22 — M99-A02 guard-preservation counterexample

Status: **WIP / source-prepared, not LEAN-CHECKED in this execution environment**.

Manager #99 assigned Agent #22 to support M99-A02 with exact Lean guard-preservation interfaces and coordinate with Agent #12.

## Exact disposition

The proposed unconditional implication

`SevenGuards q L -> SevenGuards (iterated seven-step q) (returned width)`

is false. Agent #12's pinned WIP branch `research/agent-12/m99-a02-20261015` records the ordinary-decimal witness:

- pair word: `(4,4,0,1,3,16,3,1,0,4,4)`
- seed: `44013800000`
- first seven controls: `[0,0,0,0,0,0,1]`
- returned middle: `(3,5,9,15,15,9,5,3)`
- next controls: `[0,0,1,0,0,1]`
- next guard fails at checked control `t=5`.

The first eight ordinary iterates recorded by the source are non-palindromic.

## Independent check

The exact arithmetic construction was independently replayed during this execution. It reproduces the returned middle, first control word, second control word, seed, and first eight iterates from the pinned Agent #12 checker.

This is a counterexample to guard recurrence only. It is **not** a P196 proof, and it does not establish an infinite palindrome-avoiding orbit.

## Lean artifact

`GuardPreservationCounterexample.lean` contains an exact concrete proposition over the repository's `SevenStepOrbit` and ordinary decimal semantics. It deliberately avoids `sorry`, `admit`, `sorryAx`, new mathematical axioms, and `native_decide`.

The intended acceptance sequence remains: compile against Lean 4.19.0, inspect `#print axioms`, perform a clean rebuild, and obtain independent semantic review.

Source base for the assigned work: Agent #12 branch tip `c97df1ba98386537edd25044a541a59fe61dcc55`.
Research main pin: `afbb3282be77f63711aca4fb165814104a365806`.

No claim of LEAN-CHECKED or INDEPENDENTLY_REVIEWED is made until those checks actually run.
