# NinesCenter author evidence

Author: Agent #1 specialist `/root/research_status/cap4_existing_theorems`.
Accepted claim: `7fd992f8a842eb7e870cd047df0d1e995de77128`, proposal issue61 comment6228319054. Parent is sole Git writer and external issue relay. This directory and `proofs/Agent1PeriodicNinesCenter.lean` are this author's only writes during the claimed proof task.

## Frozen result

Canonical source SHA256: `7d6d27081c480345e796c6b8e950c08a5ce0d7207e4030d24e504db4abde695e`.
Git blob: `e6f1850b5e2e1f56491f88fbe92d587b9c739e77` (computed read-only).
Direct imports: Agent1PeriodicNines, Agent1PeriodicQuotient, Agent1PeriodicCenterWrap.

All public theorems are in `Agent1.Periodic`, with B,H bounded18 and `leftEntry B + rightEntry B H [9,9,9,9] = 1`. Set W9=[9,9,9,9], e=leftEntry B, g=rawGamma B H W9 and R=pair(fixedDigits H e ++ replicate g (9*e)). The exact endpoints are:

* `rawCenter_nines_mixed`: rawCenter B H W9 = W9 ++ R ++ W9.
* `quotientCenter_nines_mixed`: quotientCenter B H W9 = (stripPeriodCenter W9 R).1.
* `centerPeriods_nines_mixed`: centerPeriods B H W9 = (stripPeriodCenter W9 R).2 + 1.

Actual entries and actual whole-word overflow are retained. No symmetry, validity, positivity, catalog, cycle, or supplied safety premise is introduced. The residual is the literal maximal strip result; extra inner removals are permitted. No temporal descent, finite-center no-return, search result, or Lychrel witness is asserted.

The proof reuses the original raw zipper identity, constant-nine entry bounds and next-period formula, and existing `pair_three_parts`. The new generic strip-wrap successor is authored and audited separately by `numeric_bridge_review` in CenterWrap. Existing arithmetic and stripping definitions were not edited.

## Actual attempts

Every attempt contains an immutable source snapshot, driver snapshot, dependency source/object hashes, actual commands, complete diagnostics and result.

| Attempt | Actual result |
| --- | --- |
| attempt-001 | Compile failed in the two overflow-one finite cases because the already simplified pairing identity still needed an append reassociation. No accepted object/result claimed. |
| attempt-002 | Raw-identity checkpoint compile and full-origin audit PASS:9 theorem constants,1 required public endpoint, standard3 only, no definitions/runtime. This snapshot predates the final CenterWrap import and quotient projections. |
| attempt-003 | Full composition compile failed at direct `congrArg Prod.fst`: expected-type elaboration chose an unprojected right-hand pair. The literal strip identity and count projection themselves elaborated, but the module was not accepted. |
| attempt-004 | FINAL compile and full-origin audit PASS:12 theorem constants,3 required public endpoints, standard3 only,0 definitions,0 generated runtime,0 custom axioms. |

The erroring Lean snapshots print diagnostic `sorryAx` for failed declarations; those diagnostics are retained as failed evidence, never accepted as proofs. No sorry/admit/native_decide/custom axiom is present in the final source. The final origin audit rejects every non-theorem constant from the new module and rejects every axiom except propext, Classical.choice and Quot.sound. All three public endpoints also have explicit `#print axioms` in the canonical source.

## Verification conditions and provenance

Official Lean4.19.0, commit6caaee842e94; compiler SHA256 `92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.
Both final commands used `--trust=0 -j1 -DElab.async=false` with a4GiB address-space limit. Final compile: exit0,0.465736902s,447564KiB maximum RSS. Full-origin audit: exit0,1.217742412s,753064KiB cumulative child maximum RSS.

This is an author increment, **not** a fresh rebuild of the entire dependency closure. The driver verified16 dependency source/object pins:15 prior modules reused from the parent's completed fresh NineCycle build at `/workspace/p196-agent1-session-20261016/nine-cycle-parent-clean-001/agent1-periodic-nine-cycle/source`, plus the unchanged CenterWrap source/object from `wrap-author/attempt-002`. It checks sources against the frozen NinesCycle registry and the actual new CenterWrap import. The final static closure therefore has17 project modules including NinesCenter. Parent and independent reviewers own any subsequent fresh whole-closure run.

CenterWrap consumed source SHA256 `dd0cba7b9f1fd97eb733d8815e1059440040a464508a3a3a265bf11084383523`; its separately sealed receipt is in `../wrap-author/frozen-receipt.json`. Our earlier attempt003 consumed identical source from wrap attempt001; final attempt004 consumes final audited wrap attempt002.

Final object: `attempt-004/Agent1PeriodicNinesCenter.olean`, SHA256 `dab7ce682ed2ea9777ed1b3f736298871feafebbf2e01404adbc5848ad05b6a4`.
The driver and origin audit are retained as `run.py` and `CenterAudit.lean`, with exact copies inside successful audited attempts. Source-only proposal report is `/workspace/p196-agent1-session-20261016/nines-center-scope.md`, SHA256 `8581d82ca8dd14601060630a656b903e5d99dc29159d439d646ae0b99ca4ddf3`; parent handles its package inclusion.

No source edits are planned after this freeze. `manifest.json` inventories all retained evidence and separately identifies local object binaries; `frozen-receipt.json` binds the final source, object, actual attempt and manifest. No Git mutation or external communication was performed by this author.
