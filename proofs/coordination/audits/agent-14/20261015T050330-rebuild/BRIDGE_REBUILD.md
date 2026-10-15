# Agent #14 — complete bridge rebuild and independent statement review

Executed checkpoint: 2026-10-15T05:36:01Z through 2026-10-15T05:37:59Z.
Exact selected source snapshot: `eb893f01c3d9f6e46007178326d7b19f92529d3e`.

## Strongest verification change

The complete actual-integer high-return bound, Agent #105's exact carry and two-output safety criteria, and Agent #109's ordinary-integer template transports now have a fresh Agent #14 rebuild. All 17 source modules compiled from an initially empty project directory, followed by all 483 explicit public theorem/lemma transitive axiom queries. Every compiler and audit command exited zero. The axiom sets contain only `propext`, `Classical.choice`, and/or `Quot.sound`; no `sorryAx`, custom mathematical axiom, `Lean.ofReduceBool`, or compiler-trusted reduction shortcut appeared.

This discharges the fresh-execution limitation recorded in this audit's earlier checkpoints. It also supplies the previously missing separate source review and fresh rebuild of the Agent #105 carry/safety-criterion package. Owner acknowledgment and shared-build acceptance are separate coordination events; this audit does not merge or alter the proof sources.

## Precisely established results

**Actual high-return bound.** For every positive ordinary integer n, starting time s, and natural R, if the actual decimal orbit is in the high region at every s+2j with j≤R, then R≤3. The high region means canonical mirrored digit-pair coefficients all lie in 9..18, with the exterior coefficient at least ten. Endpoint: `Agent105.ActualHighReturn.numeric_high_returns_after_le_three`. Its changing-width, small-width, second-overflow, canonical representation, actual-control, and concrete finite-rank obligations are discharged in the rebuilt chain. It does not prohibit later reentry after departure and is not a palindrome theorem.

**Exact return criterion.** `Agent105.ReturnCriterion.numeric_high_return_iff` characterizes an actual two-step high return using the actual second carry word, exterior coefficient, and permitted next-column coefficients. The carry entries are determined by arithmetic, not freely selectable controls. The explicit canonical representation is data describing the given integer, not an assumed witness to infinite safety.

**Exact two-output safety criterion.** Under the high-region hypothesis, `Agent105.ReturnSafety.numeric_two_outputs_safe_iff_large_adjacent` states that BOTH the first and second positive outputs are nonpalindromes exactly when some adjacent source pair coefficients sum to at least 28. No return premise is required. The starting integer's palindromicity and outputs after time two are outside this theorem. This is a local test, not an all-time invariant.

**Ordinary-integer template obstructions.** `Agent109.Compat.pairWord_orbit` identifies the Agent #8 word iteration with the accepted `Lychrel196.orbit` for actual integers. `Agent109.Endpoints.no_two_step_actual_template_return` excludes the specified two-step return for a positive integer with positive initial/final outer gaps. `no_repeatable_six_step_actual_template_return` excludes the specified six-step return with both gaps nondecreasing in the SIX phases named by `Agent8.SixPhase`. The separate Agent #8 word theorem covers all eight periodic even phases, but the rebuilt ordinary-integer endpoint has not yet exported that stronger phase range. No closed safe family or integer Lychrel witness is constructed.

`Agent109.Compat.isLychrel_iff` is an exact equivalence with an ALL-TIME word-safety condition. It does not discharge that condition for any particular seed.

## Semantic review performed

Agent #14 read the five Agent #105 actual-bound sources and all three carry/safety sources, inspecting the quantifiers, actual-width reflection, neutral-exterior overflow argument, small-width cases, actual prefix-control bounds, and representation transfer. The endpoint proofs use the existing checked rank certificate rather than assuming graph soundness. The safety source proves the first-output implication separately and uses the actual second-output palindrome criterion; the source does not silently assume safety at time zero.

The Agent #109 compatibility source and ordinary-integer endpoints were checked against the actual canonical arithmetic definitions and the Agent #8 word-level statements. In particular, the compatibility equalities are proved, not asserted because copied function bodies appear similar. This is an independent AI source/statement review, not external mathematical peer review or an independent rederivation of every historical supporting result.

## Rebuild provenance

Agent #14's read-only source-export workflow at audit commit `b5f95cb742f55e0027f77b599c665674a1345f98` explicitly checked out `eb893f01c3d9f6e46007178326d7b19f92529d3e`. Run 38687410777 succeeded; artifact 11950383236 contained 194 selected files. Every recorded SHA-256 and Git blob identity matched after extraction.

ZIP SHA-256: `0180cdb0adc3d6dc667f4106ae68c289d6c8f01983cf7301f1a72ea971b4b8b2`.
Inner source-archive SHA-256: `1c5c8712c0838961ec5c6007d43beb6a6cff3a0b38ac7773b1215cae95087731`.
Compiler SHA-256: `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.
Compiler version: `Lean (version 4.19.0, x86_64-unknown-linux-gnu, commit 6caaee842e94, Release)`.

The independent orchestration script made new source copies, set `LEAN_PATH` to the initially empty project build directory, invoked each module with `lean -j1 -o MODULE.olean MODULE.lean`, checked source hashes before/after compilation, and recorded source/object/log fingerprints and exit statuses. No project compiled object was reused. The reviewed declaration enumerator and multiline axiom parser were REUSED from Agent #105's checker, SHA-256 `8eac7767609da6cd48a4410f67519659fa3a17e8c710194d3f4696aa62edce22`; this is not a claim of an independently implemented census/parser.

## Complete 483-query finite inventory

LychrelDigitSums 291; HighCarryReduction 13; HighReturnRank 5; NeutralExterior 4; HighReturnPrefix 10; SmallWidth 4; NumericHigh 7; ActualHighReturn 9; LocalHigh 3; ReturnCriterion 5; ReturnSafety 6; PeriodObstructions 24; ActualWordBridge 26; AllPhaseRefinement 5; TemplateStep 52; Compat 16; IntegerEndpoints 3.

The full audit stdout is 42,029 bytes, SHA-256 `c851b0842929beb9ca1520dc19dc70e7848086f696515fe38a997ef1b234657a`. The retained driver includes exact endpoint type queries after every listed transitive axiom query. Counts include reused foundation results, not 483 new mathematical discoveries.

## Other checks completed after the preceding checkpoint

The interrupted Agent #5 ExteriorClock attempt was rerun successfully from the independently built dependencies; Agent #2 ExteriorCharge also compiled successfully. Their 30 and 31 printed transitive queries use only permitted logical axioms. The interrupted attempt is preserved and is not counted as a successful run.

The unchanged seven-column `verify_certificates.py` at source snapshot `f49d2fa2319d34e3f97fc94e49523c3ed3e056f4` was executed independently: exit 0, 11.277 seconds. All five complete certificates replayed. Prefixes 217, 218, 620, 739, and 777 have predecessor-depth bounds 23, 34, 12, 39, and 25 respectively. Output SHA-256: `d079164465262f290f001c59e5024a807d85eca705f1577f724a5b60a1697b09`. This is an executed Python certificate replay plus review of its written all-length coverage argument, not a new Lean certification of the concrete 739 instance.

Across this audit's successful selected builds, 24 UNIQUE Lean source modules were compiled and 629 DISTINCT fully qualified theorem names received transitive axiom inspection. This is a finite audit inventory. It is neither a repository-wide formalization percentage nor a measure of proximity to proving P196.

## Remaining central obligation

None of these results supplies a fixed finite positive seed with a proved infinite palindrome-free orbit. Actual arithmetic bridges, finite safe families, and finite-model exclusions now have stronger verification, but an all-time construction or a proof specific to 196 remains separate. Completing that obligation is not equivalent to adding more finite checks or declaration counts.
