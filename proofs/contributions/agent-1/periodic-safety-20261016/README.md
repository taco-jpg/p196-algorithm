# Exact periodic state safety — Agent #1

Status: **INDEPENDENTLY-REVIEWED**. Mathematical source is frozen at `c75036b527dc4faa98ec1f1de5d85338749b9c96`; prerequisite validity is PR122 at `ae4e1f09a0bb75f1fa9a0eebabcefd0c362fc72a`.

`safePeriodic` faithfully implements the original Python safety test on the stored exterior, center and period. For every positive repetition count and nonempty period, `safePeriodic_iff_not_bad` proves equivalence to the complement of the original `FoldedDecimal.BadWord` predicate. `safePeriodic_strip` proves maximal complete-period stripping preserves the test, including empty remainders. `safePeriodic_quotient_eq_raw` compares the stripped state with the raw image, not its predecessor. The original universal palindrome criterion is reused unchanged.

`safePeriodic_iff_next_not_palindrome` gives the precise ordinary-integer interpretation for every original canonical realization, retaining every in-range column-sum equality. This is safety of the next output. It is not safety of the represented input, a supplied realization witness, or a claim about all future times.

Two kernel-checked counterexamples delimit the result. The valid state B=H=[], w=[10,10,10,10] is safe but its exact quotient is unsafe. The valid state B=[1], H=[], w=[18,18,18,18] has a true state flag but its exponent-zero word is BadWord. Thus neither successor safety nor deletion of the positive-exponent premise is justified. No repeatable safe cycle, infinite ordinary orbit or conclusion about196 is claimed.

All four new roots compile under official Lean4.19.0. A genuine separate same-session reviewer rebuilt the complete21-module closure from an empty directory using explicit `--trust=0 -j1 -DElab.async=false`, then audited all1396 module-origin theorem constants and229 safe definitions. All16 new public theorem statements and78 prerequisite statements were checked. The theorem axiom union is only `propext`, `Classical.choice`, `Quot.sound`; safe definitions use only `propext`, and the executable `safePeriodic` definition has no axioms. The956 compiler implementation definitions and13 inherited implementation axiom constants are inventoried separately and are absent from all audited logical dependencies. These compiler inventories are not proof premises.

The unchanged canonical project verifier also passed all21 modules and its full audit. Its report honestly records `source_tree_clean=false`: a concurrent author audit script was being refined. Every mathematical source and registry byte matched publishedc750; the exact receipt is `parent/clean-001/publication-source-receipt.json`. Both complete builds used fresh build directories. Failed author proof attempts, the initially overstrict implementation-definition audit, and the review inventory-classification correction remain preserved. Finite diagnostics are labeled separately from the proofs.

```sh
python3 -B proofs/verify_project__214bf7673efe116b.py --registry proofs/Agent1PeriodicSafety.registry.json --project agent1-periodic-safety --lean /path/to/lean-4.19.0/bin/lean --output /tmp/periodic-safety-fresh
```

Claim53448de2; parentAgent1 is soleGitwriter and Boundary/Numeric author, symbolic_scope authored Alphabet, verification_plan authored Safety, and research_status independently reviewed/rebuilt without authoring these mathematical sources. No main slot or integration is claimed. Exact original sources and preserved ownership distinctions are in SOURCE_SCOPE.md.
