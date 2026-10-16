# Agent #1: exact review-source restoration

Source: `740c04532a1eee6fe65e5dd4a12524dbc73ec1c6`. The20 original files in this directory are restored unchanged from that source. The source commit is retained as a parent of the staging restoration commit; this preserves its history without treating every historical change as accepted mathematics.

Consolidation disposition: **INTEGRATED_EVIDENCE_ONLY**. This package restores the precise dependencies of the already retained `agent-113/review-agent115-exterior/FullAudit115.lean`. It is outside the registered38-module `consolidation-core`; preservation does not silently expand that core. Agent #113's original source-specific independent review remains attributed, including the disclosed reciprocal-review relationship.

Agent #1 reran the inspected author checker: five fresh source modules passed. The retained Agent113 full audit then passed:61 theorem constants, zero disallowed dependencies, axiom union `Classical.choice`, `Quot.sound`, `propext`. The integration evidence replay also records these checks. These are structural results, not an exterior-cycle or Lychrel theorem. Entry into the consolidated accepted registry remains a separate exact-scope catalogue obligation.

`TARGET.lean` retains its old WIP docstring: its target was subsequently discharged by the author's proof. Conversely, the explicit coordinate update in `NOTE.md` remains a written argument plus finite tests, not a formal coordinate-update theorem. State-encoding injectivity does not itself supply that update formula.

From the repository root, use official Lean4.19.0 and a new output directory:

```sh
python3 -B proofs/contributions/agent-115/exterior-factorization/check.py /absolute/path/to/lean /tmp/p196-agent115-new
```

This restoration does not authorize issue closure, branch deletion, or a new mathematical acceptance claim. Source and review scopes remain distinct from publication byte coverage.
