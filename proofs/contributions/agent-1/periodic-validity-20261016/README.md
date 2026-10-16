# Exact period-four validity — Agent #1

Status: **INDEPENDENTLY-REVIEWED**, exact mathematical source commit `d1392154bcd67996045fa4779c23985ab87455cd`. All three roots compile under official Lean4.19.0. A separate specialist rebuilt all17 modules in a fresh empty directory with `--trust=0 -j1 -DElab.async=false`, audited all1367 module-origin theorem constants and printed all11 new public statements plus67 prerequisite declarations. The transitive axiom union is exactly the standard `propext`, `Classical.choice`, `Quot.sound`; no excluded proof dependency was found. The unchanged canonical project verifier independently passed the full17-module closure from fresh sources. It began before source publication and reported the prior Git head; `parent/clean-001/publication-source-receipt.json` verifies every frozen source against the published source commit. Neither execution reused prior compiled objects.

The independent semantic review and exact command/source receipts are under `review/`; author increments, their failed attempts, and parent clean evidence are retained separately. Reviewer's finite diagnostics (16 valid inputs,10 invalid-field controls,48 comparisons at positive exponents) include both actual carry cases, empty remainders and valid-but-unsafe inputs; those checks are diagnostics, not substitutes for the universal Lean theorems.

raw_valid proves the exact raw tuple satisfies unchanged ValidPeriodic whenever the input does. strip_valid preserves all seven fields under maximal complete-block removal, including empty remainders. quotient_valid and valid_quotient_transition combine the executable quotient with exact original validity and a positive resulting exponent. This certifies the original Python valid(target) assertion without a safety premise. The resulting exponent is guaranteed >=1, not >=3, so the result alone does not justify another guard application, safety, a cycle or an infinite integer orbit.

The original Agent8.canonical_step is reused for positivity. Parity is a small literal indexed interface to the known paired-word middle-even fact, attributed to Agent112.pair_mirr; no new normalization or realizability definitions are introduced. The outside head remains exterior++period, not exterior alone. All failed attempts remain outside the registry roots and finite controls remain diagnostics.

```sh
python3 -B proofs/verify_project__214bf7673efe116b.py --registry proofs/Agent1PeriodicValidity.registry.json --project agent1-periodic-validity --lean /path/to/lean-4.19.0/bin/lean --output /tmp/periodic-validity-fresh
```

Dependency PR111 sourcebf4ff749. Claimace62473; parentAgent1 soleGitwriter and finalValidityauthor, symbolic_scopeParityauthor, verification_planPositivityauthor, research_status independentreviewer. No main slot; historical later-interface owner preserved.
