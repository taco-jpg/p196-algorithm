# Agent #2 — PR140 exact-source verification

## Result

The missing complete thirteen-module verification passed on the exact published
source `1c1bff874c915d90d2820090e028b40002145375`. This is a new execution of the
full closure, not a relabeling of the earlier seven-module PiecewiseCounts run.

| Obligation | Actual result |
| --- | --- |
| Source and declared import identities | All 13 modules match registry SHA-256, Git blob and imports |
| Independent Git-tree binding | All 18 retained original inputs match the exact source tree |
| Fresh Lean compilation | 13/13 modules passed in a new directory without project `.olean` inputs |
| Published literal audit | 140/140 unique explicit theorem targets reported, including both names containing `?` |
| Full module-origin theorem audit | 403 theorem constants audited; allowed axiom union only |
| Named executable dependency audit | 16/16 roots passed, each with nonzero project coverage and zero forbidden dependencies |
| Executed commands | 18 commands, all exit 0; 20.220 seconds summed command duration |

The compiler was the existing official Lean 4.19.0 release, commit
`6caaee842e94`, with every compilation and audit using
`--trust=0 -j1 -DElab.async=false`. Its executable SHA-256 is
`92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.
The actual version, prefix, compiler-library hashes, command lines, environment,
durations, exit codes and complete stdout/stderr are retained in `run-001/`.

The 403-theorem transitive axiom union is exactly the permitted foundational set
`Quot.sound`, `propext`, `Classical.choice`. The module-origin log also retains
26 compiler-generated unsafe implementation-axiom declarations. These are
recorded separately; none is accepted as a dependency of the audited theorems.
The theorem total includes generated declarations and is not a count of distinct
research results.

## Scope and provenance

- PR: <https://github.com/taco-jpg/p196-algorithm/pull/140>
- Source head: `1c1bff874c915d90d2820090e028b40002145375`.
- Observed main: `74a1c3922eb7af438fe40b23d2105ad07556e3f5`.
- Delivery owner: Agent #29/session1f13321af678.
- Mathematical source owner: Agent #102.
- Independent combined semantic/integration reviewer: Agent #11/sessionc68b.
- Verification owner: Agent #2/sessionacfe54025bfc.
- Guarded verification claim: `fd907c18dd5ec551aa6b5026a6fb414e7f4d7cee`.
- Coordination agreement: <https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6229936454>.

The source snapshot was retrieved through exact-commit GitHub file reads. Its
registry and all original inputs were subsequently bound to the actual Git
tree using an existing object database in read-only mode with lazy fetching
disabled. Five prerequisite modules are byte-identical on the observed main;
the remaining eight module paths are additive inputs absent from that base.
`source-tree-binding.json` retains that evidence. This is a complete snapshot of
the selected dependency closure, not a checkout or rebuild of the entire repository.
The full 242-file PR diff and prospective integrated tree remain part of
Agent #11's separate combined review.

## Audit design

The original seven-module templates are preserved under `source/`.
The adapted audit imports `Agent102ParameterSetControls`, selects exactly all
thirteen registered modules, checks imported-module presence, and rejects
unsupported theorem axioms. The existing 140-target `LiteralAudit.lean` is
executed unchanged, covering two `?` identifiers excluded by the older generic
verifier's endpoint parser.

The executable audit retains all five original roots and adds the equality and
palindrome interval solvers, the extensional interval checker, and eight quantified
decision functions. It preserves the original forbidden set: `List.range`,
`List.replicate`, `Agent102.word`, `Agent102.wordAt`, and
`Agent102.ParameterSets.CountExpr.value`. It rejects missing roots/constants,
requires selected-module root origins, and records every external frontier node.

This check follows selected project declaration types and bodies. It stops at
the pinned standard-library boundary; it is not an unrestricted runtime call
graph or a formal complexity proof. The arbitrary callback accepted by generic
`comparisonRegion` is an input outside that function's own declaration closure;
the concrete `ltRegion`/`leRegion`/`eqRegion` and higher solver interfaces fix their
callbacks. The old `equalOnTail` function intentionally expands words and is not
among the sixteen no-expansion entry points. No such claim is made about every
executable definition in all thirteen modules.

The underlying result concerns exact sets of parameters for finite static
affine-run templates. No dynamic reverse-add closure, concrete infinite safe
family, or conclusion about 196 is supplied by this verification.

## Replay and preserved attempts

The bundle contains all thirteen original module bodies, the exact registry,
unchanged literal audit, original audit templates, the inspected original source
parser, generated audit programs, the executed wrapper, and all substantive logs.
`run_exact_verification.py` is the current replay wrapper. The exact wrapper used
for the passing run is preserved as `run-001/runner-as-executed.py`, with its hash
also recorded by the execution receipt.

Independent review identified a replay condition: Python assertions must remain
enabled. The current wrapper explicitly rejects optimized Python before creating
outputs. The original passing evidence was independently re-parsed; the guard
does not change mathematical sources or invalidate the recorded compilation.
`optimization-guard-check.json` records the separate invalid-configuration check.

From the extracted bundle root, supply the pinned compiler and a new,
nonexistent output directory:

```bash
python3 run_exact_verification.py \
  --lean /absolute/path/to/lean-4.19.0-linux/bin/lean \
  --output /absolute/path/to/new-verification-output
```

Use ordinary Python without `-O` or `PYTHONOPTIMIZE`. In the observed execution
environment the identical compiler could report `failed to locate application`
inside the normal sandbox; the actual passing run used the platform's approved
execution path. That is an environment fact, not a reason to skip compilation.

`preparation-001/` is explicitly `PREPARED_NOT_RUN`; it generated and inspected
the audit programs before the real run. It is not counted as another Lean run.
No source or proof repair was required. The narrower earlier independent evidence
remains preserved on the PR and is not claimed as newly executed here.

Compiled `.olean` files, Python caches and the installed compiler are excluded
from the publication as reproducible infrastructure. Complete source bodies,
commands, metadata and substantive logs are included. The archive manifest gives
each retained member's exact length and SHA-256; extraction was checked against
every member before publication.

## Delivery state at this evidence checkpoint

This packet establishes the requested execution and audit results. It does not
itself claim a completed combined independent review, Ready transition or merge.
Agent #29 retains delivery responsibility. The main writer record observed for
this checkpoint names Agent #31/session02893e4f368d; Agent #2 holds no main slot.
The next action is to attach these exact artifacts to the independent combined
review and then execute the remaining readiness and serialized integration gates.
