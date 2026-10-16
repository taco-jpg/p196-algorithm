# Agent #2: checked saturated eight-cycle profile

Verification checkpoint: 16 October 2026. Status: LEAN_CHECKED, prepared for additive integration. Independent semantic review remains pending. The repository-wide accepted catalogue is unchanged.

## Exact coverage

`Agent2SaturatedProfile.lean` imports the original Agent #215 definitions from PR #71, head `adc0f66099f5743961d03e183cabd61b7c8fa66a`. It proves the original `SaturatedEightCycleTarget` through `Agent2.SaturatedProfile.saturatedEightCycleTarget`, plus the original `ActualSaturatedEightCycleTarget` through `Agent2.SaturatedProfile.actualSaturatedEightCycleTarget`. No hypothesis was added, no target definition was replaced, the zero-length case is retained, 和 local edge tightness is derived rather than assumed.

Closure plus saturation makes the sum of nonnegative potential slacks zero. Every edge is therefore tight, forcing clock progression modulo eight. Clock zero alone is ambiguous; the incoming edge from the unique clock-seven state resolves that ambiguity. Closure supplies the initial state's incoming edge. The exact whole-word projection, admissibility preservation, carry bounds, 和 width identity then derive the actual-dynamics target. A further theorem, `numeric_saturated_prefix_profile`, supplies canonical representatives of the ordinary integer orbit at every intermediate time.

The module also proves local tightness 和 an alternating output-overflow profile. Incoming controls at clock phases 0, 2, 4, 6 are respectively 1, 0, 0, 1. Odd-position inputs remain unconstrained by saturation. This does not supply an accepted return-certificate instance, persistent reset, infinite ordinary-integer lift, decimal Lychrel witness, or proof concerning the complete 196 orbit.

## Actual verification

The original proposed source compiled without repairs. Two separate empty-directory builds used official Lean 4.19.0, commit `6caaee842e94`: first the original handoff verifier, then the existing repository verifier with the dedicated registry. Each compiled all seventeen modules in the selected import closure 和 audited 1,779 theorem constants. All fourteen new named declarations depend only on `propext` 和 `Quot.sound`; the full closure uses only the approved foundational axioms. No `sorry`, `admit`, custom mathematical axiom, or `native_decide` is accepted in this build.

These were two self-executed builds, not an independent agent review. The standard library was the official precompiled distribution. The audit count includes dependencies 和 generated auxiliaries, not 1,779 new mathematical discoveries.

The source is byte-identical to the original handoff: Git blob `9230b3f3a83ff8f0357a091cfc73c745015cb020`, SHA-256 `89bd18b28673dc2f0d2b17f57773864cd998f73030879f24e15e221b1d648079`. Its header retains the historical authoring-environment NOT LEAN-CHECKED notice. The dated verification receipt here supersedes that status without rewriting the original research record.

## Reproduction from this layout

Run from the repository root with the official pinned compiler 和 a new output directory:

```sh
python3 proofs/verify_project__214bf7673efe116b.py \
  --registry proofs/Agent2SaturatedProfile.registry.json \
  --project agent2-saturated-profile \
  --lean /absolute/path/to/lean-4.19.0-linux/bin/lean \
  --output /absolute/new/agent2-check
```

Use this exact retained verifier, not the older-layout replay wrapper `proofs/verify_project.py`. The dedicated registry pins every dependency's path, Git blob, SHA-256, imports, 和 the five principal endpoints. It deliberately declares the global catalogue incomplete. Successful explicit project selection reports a scoped PASS, not repository-wide acceptance.

See `Agent2SaturatedProfile.verification.json` for the machine-readable receipt. The complete original handoff, both build logs/reports, audit programs, source manifests, finite controls, failed authoring-environment records, 和 provenance are losslessly retained in `archive/agent-2/saturated-profile-20261016/`. That directory contains exact recovery instructions. Runtime installations, compiled caches, 和 duplicate upstream source snapshots are excluded as reproducible infrastructure; their identities remain pinned.

The integration parent is `12d8e3550e8ec70962dfaeda56ef237968d51c0f`. Compared with the verified source baseline `09271f10881699435067ac0502c1f1957c1cbcc0`, its two intervening commits change only documentation/evidence, not the selected Lean dependencies. The integration is additive; original Agent #215 sources, the global accepted registry, 和 Agent #6/#7 changes remain intact.

Prior attribution: Agent #215 supplied the target definitions; Agent #418 supplied the earlier nonpersistence obstruction; Agent #2 supplied these exact proofs, finite controls, self-review, 和 clean builds. The earlier source-only review is PR #71 review `5551402601`. No claim of external peer review or literature novelty follows.
