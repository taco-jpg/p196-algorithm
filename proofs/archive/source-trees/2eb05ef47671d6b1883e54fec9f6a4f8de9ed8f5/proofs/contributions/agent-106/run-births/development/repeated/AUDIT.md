# RepeatedBirths development and proof audit

Frozen accepted source: `../../RepeatedBirths.lean`.
Namespace: `RunBirths.RepeatedBirths`.
It imports only the existing `LychrelDigitSums` foundation.

## Construction

For `m > 0`, repeat the symmetric length-ten source block
`[1,9,1,10,9,9,10,1,9,1]` exactly `m` times, with coefficients outside the
physical width set to zero. The actual incoming carry equals one precisely
at physical indices whose remainder modulo ten lies in `[4,7]`.
The carry at every block boundary and at total width `10*m` is zero.
The actual normalized digit block is `[1,9,1,0,0,0,1,2,9,1]`.
Consequently the actual next-column block is
`[2,18,3,1,0,0,1,3,18,2]`.

The proof establishes the column equation first and identifies its proposed
carry with the existing recursively defined `DecimalDigits.carry` by
induction. No guessed carry or target update is assumed. The source is
admissible for every positive `m`; the exact source symmetry follows from
the actual mirror remainder `9 - i % 10`. The numeric realization theorem
connects the family to canonical positive integers and their actual
`Lychrel196.step` successors.

## Run claim and scope

At each block index `j < m`, the positions `10*j+4, 10*j+5` form a maximal
length-two zero run. Their immediate neighbors at offsets 3 and 6 both
have coefficient 1. The positions `10*j+1` and `10*j+8` each form a maximal
singleton 18 run; their immediate neighbors have coefficients 2 and 3.
All these neighbors lie inside the actual physical word. Every source
position avoids both 0 and 18, so all the displayed runs are new births.

The main theorem `arbitrarily_many_separate_birth_runs` quantifies every
`B : Nat` and gives an admissible actual no-overflow step with two explicitly
injective enumerations: `Fin (B+1)` indexes distinct maximal zero pairs and
`Fin (2*(B+1))` indexes distinct maximal 18 singletons. Each enumerated run
carries explicit physical bounds and nonextreme neighbors. Thus the result
concerns arbitrarily many separate new runs, rather than merely many
columns in a fixed number of long runs.

The accepted file does not define or prove list `runCount` equalities.
Its exact residue classification and isolated-run/injection certificates
supply the stronger positional information needed for the requested
unboundedness. It makes no temporal repeated-regeneration, infinite-orbit,
or 196-nontermination assertion.

## Attempts and checks

- `attempt01.lean/.log`: the first 13 foundational theorems all passed.
- `attempt02.lean/.log`: first run extension; retained failures concerned
  simplification of numeric conditions, boundary-index normal forms, and
  the unavailable Mathlib-style name `Function.Injective` in Std.
- `attempt03.lean/.log`: two remaining boundary/lambda normalization errors.
- `attempt04.lean/.log`: all 23 exported theorems passed, and every printed
  transitive axiom set is contained in the standard three-axiom allowance.

No failed source is part of the accepted module. Error-recovery `sorryAx`
entries in the failed compilation logs are not present in the accepted
fourth attempt or in its final check. No source uses `sorry`, `admit`,
`native_decide`, or any new axiom.

`finalcheck.py` repeats the full accepted-source check with Lean 4.19.0,
`-j1 -DElab.async=false`, and the root's compiled unmodified foundation.
It requires successful compiler exit, all 23 theorem names in the axiom
inventory, permitted axiom sets, and absence of compiler errors. Exact
source/compiler/preload hashes, command, exit code, and elapsed time are
recorded in `finalcheck.json`; all compiler output is in `finalcheck.log`.
The root's final empty-directory rebuild supplies the additional independent
dependency reconstruction and review gate.
