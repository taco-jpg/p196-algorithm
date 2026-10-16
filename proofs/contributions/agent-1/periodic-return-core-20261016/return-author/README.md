# Return-core author verification

Frozen source: `proofs/Agent1PeriodicReturnCore.lean`.

* SHA256: `271fbd1e8c5487e515420ccd145391c039f8dccab3b8f134cf31ff9b8dd7255f`
* Git blob: `66a9dea4465cc9599ac3556704a1d5eda5e3536a`
* Strict final compilation: `attempt-003`, PASS in 0.45s, sampled peak 450436 KiB RSS.
* New-module origin audit: `audit-001`, PASS in 1.76s, sampled peak 974312 KiB RSS.
* Official Lean 4.19.0 uses `--trust=0 -j1 -DElab.async=false`; the compiler executable hash is in `compiler.json`.

All three public theorems print exactly the standard axiom set `propext`, `Classical.choice`, `Quot.sound`. The origin audit includes nine theorem declarations and the safe `returnCore` definition. Nine ordinary compiler-generated runtime implementations are separately inventoried; no unsafe theorem, unexpected unsafe declaration, or custom axiom is accepted. The final code-token scan, excluding comments, finds no prohibited proof construct.

## Exact result and limits

`quotient_return_component_constant` applies the existing `CondensationBound.component_interval` with weight one and N+1 vertices. It makes every projected component label equal along a complete-tuple return, including both endpoints; N=0 is permitted for this first statement.

`quotient_return_core` additionally assumes N>0. The first actual quotient edge excludes every internal-edge label except 8,129,130,131. The original valid zero-path no-return theorem removes 131. The conclusion is one label in 8,129,130 shared by every projected node i<=N, and each node belongs to the literal filtered `returnCore` list.

`quotient_return_initial_outside` specializes to initial period `[14,14,4,4]` and concludes that the physical outside `(B 0 ++ w 0).headD 0` is 9 or 10. It needs no separate catalog-membership assumption: complete original validity and the checked initial rows establish it. Empty B remains supported.

The return hypothesis equates B, H, and w, not merely their projection or widths. No safety, exponent guard, ordinary numeric-trajectory interpretation, return existence, or surviving-component acyclicity is claimed. No IntervalBound is supplied or inferred; the component-interval theorem does not need it.

## Dependencies and attempts

The exact import closure contains 38 modules including the new root. 36 prior dependency objects are explicitly reused with source/object hashes in `reused-dependencies.json`. The existing CondensationBound source is copied byte-for-byte from its preserved flattened source and freshly checked in `condensation-dependency-001`; its SHA is `04bb2ec87115a532ca91d5d0d453c0062f6c46f030c1fe072ee649db000a0ef8`. The new root is checked incrementally. This is not a fresh combined closure build.

Every attempted source and full log is retained:

* `attempt-001`, FAIL: the arithmetic tactic did not reduce the constant weight lambda, a closed-decision tactic was used in an open context, and list membership simplification left an empty-list disjunct. Lean's error recovery printed `sorryAx`; this failed artifact is excluded from the accepted chain.
* `attempt-002`, FAIL: weight positivity was fixed, but explicit disjunction cases still exposed the unreduced empty-list membership. This failed artifact is excluded.
* `attempt-003`, PASS: standard `List.not_mem_nil`/`or_false` simplification closes those cases; the theorem statements and mathematical argument are unchanged.
* `audit-001`, PASS: all originating logical declarations of the exact final source, plus a separate inventory of generated runtime implementations.

`stage-dependencies.py` stages only the actual import closure from explicitly supplied successful object directories and rejects conflicting source bytes. `run-attempt.py <unused-attempt-name>` preserves and checks the current source; append `audit` for the current audit source. Its one-core runner enforces a 1500 MiB physical-RSS watchdog. The parent owns fresh combined checking, independent review and publication. No Git or issue writes were performed by this author.
