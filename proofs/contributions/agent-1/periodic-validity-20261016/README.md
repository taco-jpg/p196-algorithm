# Exact period-four validity — Agent #1

Status: **LEAN-CHECKED source; independent and parent fresh17module verification running.** All three roots compile under Lean4.19.0 --trust=0 with literal public axiom audits containing only propext, Classical.choice and Quot.sound. Frozen source hashes and exact dependency closure are in proofs/Agent1PeriodicValidity.registry.json. Author increments reuse pinned prior independently verified objects explicitly; fresh combined acceptance remains pending.

raw_valid proves the exact raw tuple satisfies unchanged ValidPeriodic whenever the input does. strip_valid preserves all seven fields under maximal complete-block removal, including empty remainders. quotient_valid and valid_quotient_transition combine the executable quotient with exact original validity and a positive resulting exponent. This certifies the original Python valid(target) assertion without a safety premise. The resulting exponent is guaranteed >=1, not >=3, so the result alone does not justify another guard application, safety, a cycle or an infinite integer orbit.

The original Agent8.canonical_step is reused for positivity. Parity is a small literal indexed interface to the known paired-word middle-even fact, attributed to Agent112.pair_mirr; no new normalization or realizability definitions are introduced. The outside head remains exterior++period, not exterior alone. All failed attempts remain outside the registry roots and finite controls remain diagnostics.

```sh
python3 -B proofs/verify_project__214bf7673efe116b.py --registry proofs/Agent1PeriodicValidity.registry.json --project agent1-periodic-validity --lean /path/to/lean-4.19.0/bin/lean --output /tmp/periodic-validity-fresh
```

Dependency PR111 sourcebf4ff749. Claimace62473; parentAgent1 soleGitwriter and finalValidityauthor, symbolic_scopeParityauthor, verification_planPositivityauthor, research_status independentreviewer. No main slot; historical later-interface owner preserved.
