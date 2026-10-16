# Outer period-block stripping author evidence

Frozen source: `proofs/Agent1PeriodicOuterStrip.lean`.
SHA256 `734a8d8f639e5eac254e76de6eb8d9a41e377c6e87e0574be4478a3669cfb85c`.
Git blob `9e35c06bf3dd393f33dfd2af965a1ea2d4305bc7`.

This module implements exactly the outer loop in original `transition(s)`, line51 of `periodic_word_quotient.py` (blob `c7b87ad87287a7fafb6849c2e6cf9c4cd4ebe72a`). At period length4 it removes a final four-symbol copy, retains the prefix in its original order, and increments the absorbed count. The public definition handles arbitrary nonempty finite blocks; empty block is explicitly returned unchanged with count zero.

The theorem `stripPeriodSuffixAux_spec` proves reconstruction AND no remaining complete suffix for every fuel at least input length. Each successful removal shortens the list by the positive block length. The public definition supplies input length as fuel; maximality is consequently proved rather than inferred from an arbitrary fuel cutoff.

Public endpoints:

- `stripPeriodSuffixAux_spec w fuel B hw hFuel`: reconstruction and maximality under `w ≠ []` and `B.length ≤ fuel`.
- `stripPeriodSuffix_spec w B hw`: `B = result.1 ++ pow w result.2`.
- `stripPeriodSuffix_maximal w B hw`: no `D` with `result.1 = D ++ w`.
- `stripPeriodSuffix_empty_block B`: stripping `[]` returns `(B,0)`.
- `stripPeriodSuffix_length w B hw`: exact input length = remainder length + count * block length.
- `stripPeriodSuffix_bounded w B bound hw hB`: every retained coefficient obeys the original bound.

No symmetry, positive coefficient, parity, or decimal normalization hypothesis is needed by these finite-list statements. There is no safety, full output validity, cycle, numeric-realization, or infinite-orbit conclusion. Parent owns the quotient composition; the center algorithm is in a separate module and is outside this author's evidence.

Verification performed:

1. `dependencies.json` pins all eleven imported source modules by path, module import name, SHA256, and original blob. Their exact bytes were staged in a new isolated directory, `/workspace/p196-agent1-session-20261016/periodic-strip-outer-author-build`. Every source was compiled with Lean4.19.0, `--trust=0 -j1 -DElab.async=false`; all exited0. Full commands and times are in `baseline-results.json`, complete output in `baseline-*.log`.
2. `compiler.json` pins the actual executable path, SHA256, version, and source baseline95a17. No preexisting project olean files were copied.
3. `attempt-001/` preserves the first source snapshot and failed compile. Its rejected partial declarations produced `sorryAx` diagnostics after tactic errors; it is not accepted evidence. The errors concerned simplification of list lengths, rewriting the suffix also inside an index, and reducing a pair projection before rewriting. The final source contains no placeholder.
4. `attempt-002/` preserves the frozen accepted source, exact command, elapsed time, exit0, and all six literal axiom prints. Each uses only `propext` and/or `Quot.sound`.
5. `audit-001/OuterAudit.lean` imports the accepted olean and selects declarations by actual module origin. All13 theorem constants and all19 safe constants (including generated auxiliary declarations) passed the same allowed-axiom check. Nine unsafe compiler implementation declarations were recorded separately; none is accepted as a theorem dependency. The transitive axiom union is exactly `propext`, `Quot.sound`; there is no custom safe axiom. Audit command/log/result are retained.
6. A final accepted-source scan rejected placeholders, native evaluation, `Lean.ofReduceBool`, and source axiom declarations. `frozen-receipt.json` records every result and pin.

The eleven dependencies were not rebuilt redundantly after the frozen source passed. Parent will run a separate fresh combined closure/registry and independent review with the center and quotient modules. This record claims only the executed author checks above.

To reproduce from an empty build directory, copy the exact sources in `dependencies.json` under their recorded `<module>.lean` names, checking every SHA256, and run each recorded compiler command in dependency order with `LEAN_PATH` set to that directory. Copy the frozen OuterStrip source and run its command from `attempt-002/result.json`; then copy `audit-001/OuterAudit.lean` and run its command from `audit-001/result.json`. `run-attempt.py` is the actual incremental snapshot/checking driver used for both attempts; it deliberately records attempts in fresh directories and refuses to overwrite them.
