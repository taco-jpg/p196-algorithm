# Independent infrastructure review of the proposed PR153 verifier

## Decision

**BLOCKED for launch in the reviewed form.** The frozen verifier generates two
Lean options that the pinned Lean 4.19.0 runtime does not recognize:
`pp.width` and `pp.maxDepth`. Its literal-audit stage therefore exits with code 1.
This was reproduced with a neutral fixture using the exact frozen literal-audit
generation statements, without compiling any PR153 mathematical module or
Mathlib. The verifier correctly treats that nonzero exit as failure even though
Lean continues processing and prints its completion marker.

The main auditor template itself passes the bounded API fixture. The reviewed
source pins, endpoint list, module-origin inventory, axiom API, safe-definition
and opaque-body closure, and tested fail-closed paths are sound for the stated
narrow infrastructure scope. The specific blocker is a compatibility defect in
the generated literal audit, not evidence of a mathematical failure in PR153.

Reviewer: independent infrastructure reviewer supporting Agent #18,
session `c6d78d258d21`; separate from verifier author Agent #20. This supplies a
reproduced defect and bounded infrastructure evidence for the existing review
work. The coordinator subsequently reported that a different genuine reviewer
is already assigned to the whole current verifier. Our work is supplemental,
not an additional mandatory full-review gate or current-version launch clearance.
It does not require a review of this review.

**Repair update:** the coordinator's exact one-line option repair is independently
validated in `REPAIR_SCOPED_RECEIPT.md`. This resolves the reproduced printer-option
defect for that exact repaired copy. It does not retroactively turn the original
frozen verifier into a passing run or cover unrelated later script changes.

## Exact input boundary

The four inputs were copied before evaluation at
`2026-10-17T05:22:28.157166+00:00`. The complete paths, lengths and hashes are in
`FROZEN_INPUT_SHA256.json`; the exact bytes are under `frozen-inputs/`.

| Input | SHA-256 |
| --- | --- |
| `verify_pr153.py` | `8895d1261b7e70a00b061ed70b6aeb48580f541f3d4192bc0d34c81140c0f548` |
| `Audit.lean.in` | `e0acf0ac8c33d6832d5a008d11d99b95950ff1ec7ea4d0f2d9c67b6f710d148f` |
| `source-manifest.json` | `a49d4fc3288c992465f355a8fef1a8e2977fd7dfd5507c4fa1e6e410b16175e7` |
| `README.md` | `e8eb22ac2dda6ea4d1015270347cf3fab1735d5dcdfb15a2067a7d059e6c88d7` |

The task's previously observed script digest, `b29a733e0565d7dddb16732000121306ba760a302396aef5a2e4421b179a11d0`,
was already superseded before this snapshot; it was not the reviewed script.
During review the author's script changed again to
`2946672444067c646ff38a3a099bc8c69c9964d729a923cd7fbd27c44aebaddb`.
That observation and its exact bytes/diff are retained in
`OBSERVED_INPUT_CHANGE.json`, `observed-later-inputs/`, and
`verify_pr153.py.observed-change.diff`. The latter changes external-header
parsing and adds a pretty-printer budget/truncation check. It still contains both
unsupported options. This report's complete review applies to the first frozen
snapshot, not an unexamined future revision.

All seven manifest-pinned provenance files were also copied and their hashes
checked successfully. No author's file was written or altered.

## Blocking finding and bounded reproduction

The frozen script's line 411 emits:

```lean
set_option pp.width 160
set_option pp.maxDepth 100000
```

The retained `fixture-logs/literal-audit.stdout` begins:

```text
LiteralAudit.lean:4:0: error: unknown option 'pp.width'
LiteralAudit.lean:5:0: error: unknown option 'pp.maxDepth'
```

`FIXTURE_RESULTS.json` records `literal-audit` return code 1, exact arguments,
environment, timing and stdout/stderr hashes. The generated file is
`fixtures/LiteralAudit.lean`. Its generation block was extracted from the frozen
Python script, with only the project import changed to `NeutralFixture` and the
module/endpoint inputs adapted. The unmodified block is otherwise preserved in
`literal_generation_fragment.py`. `fixture-attempt-004/` freezes the failed
attempt before any diagnostic continuation.

The pinned runtime's source registers `format.width` in
`Lean/Data/Format.lean`, and `pp.deepTerms`, `pp.deepTerms.threshold`, and
`pp.maxSteps` in `Lean/PrettyPrinter/Delaborator/Options.lean`; it does not
register the two failing names. Copies and hashes of those sources are retained.
A reviewer-local diagnostic replaced only `pp.width` with `format.width` and
`pp.maxDepth 100000` with `pp.deepTerms true`. That diagnostic exited 0 and
provided every required endpoint marker, 33 theorem axiom prints, and 16 safe
definition/opaque prints, including the numeric-component private Name.
It is not an edited or accepted author verifier.

The concrete repair is to use supported Lean 4.19 printer options and retain
complete-output checks, then rerun the affected small fixture against the exact
repaired author script. No duplicate thirteen-module proof build is necessary
to resolve this infrastructure defect. The later observed script's explicit
`pp.maxSteps` and `⋯` rejection address its own completeness requirement; the
frozen script did not have that truncation guard. I did not establish that a
PR153 term actually exceeds the old printer budget.

## Interface and source identity review

`STATIC_INTERFACE_CHECKS.json` records independent read-only `git show` commands
and their exits. For every one of the thirteen modules, I checked the bytes at
head `6641b1ea166fcef0e6f9d1fa23afed7b1f6b8a82`, SHA-256, Git blob ID, recorded
imports, and equality with the original source commit/path. All checks pass.
The eleven unchanged dependency entries agree with the retained original
`dependencies.json`. The root's explicit import graph reaches all thirteen
recorded modules. The static source policy scan finds no prohibited construct.
Raw source/stdout and stderr are preserved under `static-source/`.

The two new files contain exactly the manifest's 29 theorem endpoints in the
same order: 21 in `Agent52Density`, eight in `Agent52DigitSumDensity`. The JSON
checks include their full names. The driver checks unique endpoint names and
requires all of them in the theorem census. The template requires all 29 to
exist and have theorem kind. Literal generation prints each elaborated type and
its actual `#print axioms` result. Every module-origin theorem, including private
and generated declarations, also receives that real print elaborator command.

The driver substitutes the two template placeholders with validated module and
endpoint lists. The template's `INVENTORY`, `THEOREM_AXIOMS`, `CLOSURE`, and
`AUDIT_COMPLETE` JSON records agree with the driver's parser. The driver checks
unique record names, exact reported record counts, all thirteen inventoried
origins, all 29 endpoints, and allowed theorem axioms. The literal stage uses
`mkIdent name`, preserving internal numeric Name components instead of trying
to parse their textual spelling as ordinary identifiers.

## Lean API, declaration census and closure

The official executable and shared library were independently rehashed:

| Runtime file | SHA-256 |
| --- | --- |
| `bin/lean` | `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023` |
| `lib/lean/libleanshared.so` | `2ab605c74c78f9ba4431a7b5305a4b28a9071d8a826f223eb14fe5530f78e14d` |

The executable reports Lean 4.19.0, commit `6caaee842e94`, Release.
`Lean.collectAxioms` has result `m (Array Name)` in this exact source/runtime;
the template correctly obtains it through `liftCoreM` and converts with
`toList`. The API itself reads checked constants. The template also reads
`env.checked.get` for each inventory/closure declaration, and fails explicitly
if a required checked constant is absent.

The unchanged template was instantiated by changing only its import and the
module/endpoint parameters. It retained its 29-endpoint count condition. The
neutral positive fixture includes private and public definitions, an opaque
body, an inductive family/recursor, recursion, and 29 harmless theorem endpoints.
It produced the following exact completed census:

| Measurement | Count |
| --- | ---: |
| Module-origin declarations | 63 |
| Theorems, including generated ones | 33 |
| Endpoint theorems | 29 |
| Safe roots | 53 |
| Distinct transitive closure declarations | 101 |
| Safe definitions and opaques for literal printing | 16 |

All inventory kinds are enumerated, without a theorem-name allowlist hiding
additional declarations. The census includes nine generated unsafe compiler
helpers and one generated partial helper. They are inventoried, excluded from
safe roots, and absent from the accepted mathematical closure. Their existence
is not misreported as a mathematical axiom or proof dependency.

`directDependencies` traverses types and `value? true`, which includes opaque
bodies, plus inductive families, constructors, and recursor rule bodies. The
global visited set terminates shared/cyclic traversal. All safe local
declarations are roots, so a bad unused safe definition cannot escape by being
absent from the 29 published theorem bodies. Imported unsupported axioms,
`sorryAx`, compiler-trust constants, unsafe constants, and partial constants
are rejected when reached. Theorem axiom collection separately accepts only
`propext`, `Classical.choice`, and `Quot.sound`.

`implemented_by` and `extern` data are reported separately and do not replace
the mathematical body traversal. Explicit local implementation overrides and
unsafe/partial source constructs are prohibited by the source scan. This is
consistent with auditing mathematical proof dependencies while allowing Lean's
generated implementation helpers outside that closure.

## Fail-closed evidence and execution controls

All Lean executions were sequential, through normal approved escalation for
the documented runtime location, with `--trust=0 -j1 -DElab.async=false`.
The reviewer harness imposed a 3 GiB address-space limit, CPU soft/hard limits
of 100/110 seconds, and a 120-second per-process timeout. It supplied only a
small environment and local fixture/runtime `LEAN_PATH`.

| Fixture/check | Observed outcome |
| --- | --- |
| Exact positive auditor template | Exit 0, complete census above |
| Exact frozen literal generation | Exit 1, unsupported printer options |
| Supported-option diagnostic literal generation | Exit 0, all endpoint/theorem/definition prints |
| One missing endpoint | Exit 1, `ENDPOINT_COUNT 28` |
| Unsupported external axiom used only through safe opaque body | Exit 1, `CUSTOM_CLOSURE_AXIOM NegativeExternal.unsupportedValue` |
| Safe definition referring to compiler-trust axiom | Exit 1, `COMPILER_TRUST_DEPENDENCY Lean.ofReduceBool` |
| Driver with missing runtime | Exit 1, `FAIL`, zero commands and zero local compilations |
| Driver output outside its owned directory | Exit 2, no output directory created |
| Driver repeated output directory | Exit 1, original failed report retained |
| Twelve lexer edge/rejection cases | All expected results |

The negative fixture sources and objects are infrastructure rejection evidence
only. They are isolated from PR153, and no unsupported axiom or compiler-trust
fixture was admitted to an accepted mathematical chain.

Three preliminary reviewer-harness issues are fully distinguished from verifier
failures in `FIXTURE_ATTEMPTS.json`: an unsupported fixture-only `-M2048` option,
an overly narrow expectation of 29 total theorems that ignored generated
theorems, and Python indentation during literal-block extraction. Each attempt's
runner, results, and raw Lean logs is retained in its numbered directory. The
auditor was not changed to accommodate any fixture.

The proposed driver retains subprocess argv/cwd/environment, raw stdout/stderr,
exit codes and timing; it stops after a failed command. It also records generated
audit sources, input and object hashes, failures, final input stability, and a
file inventory. `PASS` occurs only after all compilation/audit/stability work.
Omitting `--execute` returns the explicitly narrower
`SOURCE_AND_IMPORT_CHECK_ONLY` status, not proof PASS. Its compile/audit commands
are serial and have 1800-second individual timeouts. The proposed driver itself
does not impose the extra OS memory/CPU bounds used by this review fixture.

## Cache provenance and limits of this conclusion

The driver pins the Lean executable/shared library and the Mathlib lake manifest,
checks the restoration report's fixed Mathlib commit and manifest values,
retains that report verbatim, and hashes the external source/object closure it
resolves. The README honestly states that it reuses restored external objects
and does not independently derive their correspondence to source by rebuilding
Mathlib. Checking two restoration-report fields is not independent authentication
of a cache artifact. Restoration provenance remains a separate supplied input;
neither this review nor the driver should be cited as a fresh Mathlib build.

I did not launch the full verifier or independently enumerate the real Mathlib
cache during this bounded review. Accordingly, no successful actual thirteen-
module compilation, complete actual PR153 axiom census, or actual cache closure
is claimed here. The later external-header parser change is recorded as a scope
boundary, not silently included in the frozen script's review.

This is not mathematical acceptance, semantic review of density statements,
repair of any exact-original missing checker, recovery of the unrecovered old
thirteen-module logs, a repository-wide PASS, or a delivery/merge claim. No old
proof failure was inferred from missing logs. Main writer Agent #31 remained
outside this review's scope. No PR/issue comment, remote write, source edit,
network fetch, or cleanup of another worker's files was performed.

## Evidence inventory

`FILES.json` supplies every retained file's relative path, size, and SHA-256.
Key records are `FROZEN_INPUT_SHA256.json`, `STATIC_INTERFACE_CHECKS.json`,
`RUNTIME_API_HASHES.json`, `FIXTURE_ADAPTATIONS.json`, `FIXTURE_RESULTS.json`,
`FIXTURE_CONCLUSIONS.json`, `POSITIVE_PARSED_AUDIT.json`,
`DRIVER_FAILURE_RESULTS.json`, `LEXER_FIXTURE_RESULTS.json`, and
`FIXTURE_ATTEMPTS.json`. Exact commands and fixture sources are retained in the
two Python runners, generated Lean sources, and per-command raw logs.
