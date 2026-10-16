# Agent 9: exact complementary-bulk exterior erasure

The mathematical report is [ERASURE_THEOREM.md](ERASURE_THEOREM.md). This directory contains a verified local contribution, not a proof of P196 or an all-width exclusion of complementary-bulk cycles.

`ExteriorErasure.lean` proves the exact all-length overflow suffix rule, the trimmed no-overflow rule, their length consequences, and full binary collapse. The 28 supporting declarations have a complete standard-axiom audit; see `verification.json` and `ExteriorErasure.compiler.log`. The actual whole-word connection is the pinned written quotient theorem identified in the report, rather than an assumed claim that the entire bridge has been formalized here.

Reproduction with Lean 4.19.0 and Python 3.10+:

```sh
python verify.py --lean /path/to/lean-4.19.0/bin/lean
python audit_quotient.py
python audit_erasure.py
```

The first finite test replays 267,520 literal integer instances. The second checks 2,085,136 canonical exteriors through length four, 65,520 full-collapse binary words through length twelve, and 10,000 seeded random literal full-quotient instances. These counts are test evidence, not additional all-length theorems.

The isolated GitHub workflow is `.github/workflows/agent9-exterior-erasure.yml`; source-pinned accepted run 38683728944 was rebuilt independently in the local checker. AI-assisted research, with no claim of literature novelty or independent human verification. Coordination: issue #7. Agent 9's independent scalar-instance replay is a separate task in issue #13.
