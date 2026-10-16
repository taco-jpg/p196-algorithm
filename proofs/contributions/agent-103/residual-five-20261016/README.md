# Agent #103 — residual digit-five necessary conditions

Task: `agent103-residual-five-20261016`. Entry point: `ResidualFiveConclusion.lean`.

## Result and mathematical scope

`Agent103.ResidualFive.occurrence_necessary_conditions` proves that an occurrence
`Lychrel196.orbit 196 t = 55*(10^(2*r+2)+1)` forces all of the following:

- `105 <= t`, `1 <= r`, and `t % 6 = 3`;
- canonical widths `2*r+4` at both preceding times;
- zero terminal carry on both final additions;
- exact intermediate integer `33*10^(2*r+2)+22`;
- complete earlier pair-sum word `[2,12] ++ replicate (2*r) 9 ++ [12,2]`;
- internal carry one exactly at columns `2` through `2*r+3`.

The unfolded endpoint writes the original integer family explicitly. It assumes
no first-positive-hit condition and no unverified certificate. These are necessary
conditions for an occurrence, not an exclusion of the residual family.

`Agent103.ResidualFiveWitness.residual_five_witness` proves that the positive seed
`71647625487907287180977453773517` first reaches a palindrome at time six,
namely `55*(10^32+1)`. Its entire modulo-99 trajectory at time `i` agrees with the
196 trajectory at time `3+i`. Thus that shifted modular trajectory alone is
insufficient to exclude this target. This seed is not asserted to lie on the
integer orbit of 196.

`ResidualFiveShape.lean` formalizes the written inverse structure in section 4 of
the preserved `p196_all_palindromes_and_eight_families.md`. Its local shape theorem
also includes `r=0`. The 196 occurrence theorem itself excludes `r=0` using the
original early-orbit result. Uniqueness refers to the pair-sum word and the
intermediate integer; individual source integers need not be unique.

## Verification

All four frozen modules passed an independent semantic review and rebuild.
The complete eleven-module dependency closure was then rebuilt into a new empty
project-object directory with pinned Lean 4.19.0, commit `6caaee842e94`, using
`--trust=0 -j1 -DElab.async=false`. Every build command exited zero.
The final audit individually queried `#print axioms` for all 1,532 theorem
constants of those modules: 1,380 dependency constants and 152 new-module constants.
All reported dependencies are among `propext`, `Classical.choice`, and `Quot.sound`.
This is a scoped closure verification, not a repository-wide build claim.

There are 63 source theorem declarations in the four new modules, including
private lemmas. A separate independent compilation produced 161 new-module
constants; the nine-count difference consists entirely of generated `_proof_N`
helpers. Source hashes and every non-generated theorem name agree. Both genuine
logs and the exact comparison are retained; theorem counts are not novelty counts.

Actual cross-author reviewers were the real `scope_scan` and `source_audit`
specialists in this Agent #103 session; `runtime` authored no mathematical source
and performed the full fresh closure build/audit. The GitHub publishing identity
is shared. This is not represented as approval by another GitHub account.

## Reproduction and preserved evidence

See [REPRODUCE.md](REPRODUCE.md) for both the portable historical-source replay
and the current-tree project registry. `check.py` and `SOURCES.json` pin original
commit/path/Git-blob/SHA256 identities. `BUILD_REGISTRY.json` consumes byte-identical
current-tree files and exact vendored dependencies without requiring historical
commits. The unchanged project verifier passed its `--check-only` gate on that
published layout. The stronger trust-zero full build is recorded separately.

Readable summaries are under `evidence/clean-summary.json` and
`evidence/publication-layout-check.json`. Complete clean-build sources, commands,
logs, per-theorem axiom records, the source-count comparison, registry staging,
and runtime recovery history are in `evidence/complete-replay-evidence.tar.xz`.
Its file-by-file inventory is `evidence/complete-replay-evidence.manifest.json`.
Earlier individual reviews and real failed attempts remain at their original
`evidence/` and `attempts/` paths and in commit history. Compiled objects and the
reproducible Lean toolchain are omitted from the archive; their measured hashes
remain in the verification reports.

Agent #119's eight-family theorem explicitly excludes `d=5` and is reused unchanged.
Agent #423's temporal module is also unchanged. The sole import adapter replaces
`Lychrel196Research.lean` with `import LychrelDigitSums`: the entire original
4,444-line foundation body was verified byte-identical inside the continuation
foundation before compilation. No arithmetic definition has been changed.

The status of 196 remains open in this contribution. Main integration is owned
separately and is not performed by this branch.
