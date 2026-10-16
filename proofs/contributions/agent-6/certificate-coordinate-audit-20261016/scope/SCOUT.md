# Agent 6: next-scope source census

Updated 2026-10-16 21:40:58 UTC. This report records read-only source analysis. No new theorem source or Lean build was started for these targets.

## Recommended next claim

Use the original accepted-certificate projection to transport the newly published signed-beta cycle law to the certificate's exact listed rows. Parent has selected the new worktree `agent6-checker` at `a075b2719c4ff1cb972b68b1d9240d8eaa8d463f`. The proposed author file is `proofs/contributions/agent-6/certificate-coordinate-audit-20261016/CertificateCoordinates.lean`; parent owns `CertificateFilter.lean`. Proof work waits for the guarded claim.

Put

```lean
q i := Agent116.CertificateExterior.stateOuter (cert.st i)
delta i := Agent6.ExteriorCoordinates.highContribution (q i).c (q i).B
```

The smallest useful endpoint is

```lean
check cert = true →
  Agent110.Accounting.sumPrefix delta cert.P = 0 ∧
  (∃ i, i < cert.P ∧ 0 < delta i) ∧
  (∃ j, j < cert.P ∧ delta j < 0)
```

These are necessary conditions on the unchanged full checker. A Boolean filter can check these finite rows and reject a candidate that violates them; satisfying the filter does not establish checker acceptance.

The statement needs only `check cert = true`. `check_sound` supplies `0 < cert.P` and `LocalOK` on every row. `LocalOK` supplies `Phase c := 1 ≤ c ∧ c ≤ 17 ∧ c ≠ 9`, hence positive initial phase. The all-positive-phase nonzero theorem already suffices for both signs. No admissibility, positive head, width cap, even phase, or separately assumed `validOuter` premise is necessary. Empty exterior words remain included.

## Exact existing interfaces

- `Agent116.CertificateExterior.stateOuter s = ⟨s.c, stripSuffix s.c s.B⟩`.
- `local_outer_step` takes only one original `LocalOK` and concludes `outerNext (stateOuter s) = stateOuter s'`.
- `certificate_outer_orbit cert hv n` concludes `P196.Agent7.Finite.outerIterate n (stateOuter (cert.st 0)) = stateOuter (cert.st (n % cert.P))` for every `n`.
- `Agent109.Outer.outerIterate_eq` already relates the original tail-recursive iterator to a forward-recursive `outerIter`. Agent 6's new iterator has the same forward recurrence; only that small iterator compatibility and finite row-sum transport remain.
- `CoordinateCycle` already exports `closed_orbit_contributionSum_eq_zero`, `closed_orbit_both_signs_of_pos`, and `closed_orbit_weighted_balance`. Their source is blob `6b7ab7b9801109f3a5af7e8237f59db84601686a` at the published Agent 6 checkpoint.

The projection's exact source is `proofs/CertificateExterior__94efd9fc73b36162.lean`, blob `76e86aea561288b8a47f1b5999c2578e50d597c4`; its original module path is `proofs/contributions/agent-116/certificate-exterior/CertificateExterior.lean`. The unchanged checker is `proofs/ReturnCertificate__b037c18e81a43bb5.lean`, blob `95196cfe2da9b224412a9c31910163cf5784f996`. The existing `sumPrefix` helper is `proofs/CertificateAccounting__ad0d1bd9b0242036.lean`, blob `79bf1fdfebabcf95dee96698be9aab3747c2599a`.

Use normalized rows explicitly. No new highContribution trimming-invariance theorem is needed. Optional weighted row balance can transport the already proved identity using each normalized row's `overflowBit`. Identifying that count with the original checker's `totalGam` would need an additional carry-under-trim bridge; the present scope does not assume it.

## Complete source closure

The three import roots are `CertificateExterior`, `CertificateAccounting`, and `CoordinateCycle`. Their union contains exactly **17 project modules**, with **Std** as the only external module:

```text
TemplateStep, ReturnCertificate, OuterFinite, OuterBounds, OuterBridge,
CertificateRealization, ExteriorNormalization, CertificateExterior,
CertificateAccounting, TARGET, ExteriorFactorizationProof,
ExteriorObservationInjective, ExteriorUpdateLaw, CoordinateDynamics,
CoordinateThreshold, CoordinateSign, CoordinateCycle
```

`checker-import-closure.json` contains topological order, original and flattened paths, exact source commit, Git blob, SHA-256, and imports for every module. `checker-imports/` contains unchanged source copies. All 17 copies were byte-checked against those pins; runtime independently repeated that check. This staging is not a compilation result. Any new build must use pinned Lean 4.19.0 with `--trust=0 -j1 -DElab.async=false` and preserve its failed attempts.

## Ownership and existing work

The complete earlier census is pinned at coordination `d04c1b38434036bc69071332ea319b1887ae1401`: 89 task names and 67 live branches. Subsequent exact task reads add the Agent115/110 claims below. Root must guard the actual claim against the latest coordination head.

| Area | Exact evidence | Consequence for this claim |
|---|---|---|
| Agent116 original projection and cap3 obstruction | Final preserved task blob `1ccf11c8ba693c4be90c7f65a5d0edb57926991a`, status INTEGRATED; integration task `a7fa14397fe0ced7f92648666e93749637336d1d`, role explicitly released. No Agent116 task or branch in the complete pinned census. | Reuse unchanged projection. The old work contains no signed-beta row audit. |
| Agent412 charge telescope | Task `f69fd17e234a567cd7015974ed6e4d3432c8b920`; source `bde07a39b020752219965ce3b859242eea3845db`. | Owns original-checker phase 6/12 scaled-charge residue, not signed-beta cancellation. |
| Agent412 interface/gain residues | Task `e6031f6538b4be30df438184a3e0531ac13f03a1`; source `097be33b22fb728966c87790363c28824d3fb274`. | Owns mod-3 interface and band-gain congruences. |
| Agent412 period 12 | Task `b80df190f66444f1f17aeea918fb740e6ff22a2d`; source `4b99a05d42c56c5b7c1bc011fd335cb1e190b486`. | Owns checked P ≠ 12 and divisibility consequences. No new period result here. |
| Agent115 rho cycle, newly claimed | Task `769c16bb70b4ea4b3a31c876f6e0f21e938b1b6a`. | **Exclude rational rho recurrence, its period telescope, forced overflow, and proposed width/count strengthening from our queue and claim.** |
| Agent110 two-step return, newly claimed | Task `486eb1460dab5cca752d312c623e2488c5d34ed4`. | Exclude phase-6 two-step exact nonreturn or counterexample. |
| Agent5 literal coordinate streams | Task `482a64321742bcb9f289b04ac5b55cae86d50e3d`. | No literal low/high digit-stream proof or stream recombination. |

The surviving Agent115 branch `fba03a902e0f6b198cbf8f42efa8d11f8f2ba7a6` has 1,361 Lean file entries, representing 1,269 distinct blobs. All those blobs were read through exact mapped sources or the seven branch-only source snapshots and byte-verified. None contains the new identifiers `betaNum`, `highContribution`, `contributionSum`, `weightedPhase`, or `weightedReverse`. Its `FactAudit.lean` checks factorization, observation injectivity, and the already formal `rawSucc_values` / `successor_observation`. This identifier census is not an automatic theorem-equivalence proof. Actual Agent412 source was also read; its observables are charge/tau/rho modulo three, not the signed beta increment. Raw task and source snapshots accompany this report.

## Rolling queue

All deferred rows require a fresh ownership check and explicit narrow claim. This is a queue of interfaces to develop, not a claim that the open global cycle problem has been resolved.

| Rank | Concrete remaining obligation | First action and boundary |
|---|---|---|
| 1 | Accepted checker implies exact normalized-row signed-beta cancellation and both signs; parent adds a necessary Boolean filter. | Transport the existing certificate orbit into `CoordinateCycle`; no new projection or trim invariance. |
| 2 | Original checker `gam (cert.st i)` equals the rho threshold bit of its raw row B. | Combine `normalize7_eq` with the existing `CoordinateThreshold` endpoints under the checker's existing phase/bounds. No rho recurrence or Agent412 charge proof. |
| 3 | Expose exact rho-selected carry and suffix-trim count in `actual_step_outer`. | Preserve original hypotheses; retain its explicit witness `G = g + gamma + j` and `|B'| + j = |B| + 1`. Source blob `06ed5a8660e83b2dde192a10c822c9317a79483b`. |
| 4 | Exact finite ordinary-template gap accounting: `H_n = H_0 + O_n - 2n` and `G_n + |B_n| = G_0 + |B_0| + O_n - n` in Int. | First expose rank 3's one-step equality, then telescope only across an actually supplied finite guarded trajectory. Do not overlap Agent14's cut-window transport or invent an infinite schedule. |
| 5 | Canonical exact return iff phase return, zero signed-beta sum, and cross-multiplied rho equality. | Package existing `observation_injective` (blob `80d175e4c28ba171e67eaf7e0f9961235e0ec7e7`) with the new beta telescope and explicit valid endpoints. Low priority; no new injectivity, rho recurrence, period exclusion, or two-step theorem. |

Full hypotheses, source blobs, exclusions, and first actions are also stored in `queue.json`. Existing saturated profiles, phase periods, repeated blocks, native charge correspondence, generic boundedness, and owned stream/cycle targets are excluded.
