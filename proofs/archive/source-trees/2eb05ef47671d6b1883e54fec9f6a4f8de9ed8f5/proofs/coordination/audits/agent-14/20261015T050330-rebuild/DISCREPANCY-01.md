# Agent #14 discrepancy A14-D01

Urgency: **REPORTING_OR_METADATA_ERROR**.
State: CONFIRMED_AT_PIN; correction requested, acknowledgment not yet observed.
Audited current-main source pin: `eb893f01c3d9f6e46007178326d7b19f92529d3e`.

## Exact discrepancy

`proofs/README.md`, lines 26–35, still presents safe three-return sharpness as UNKNOWN and describes the actual-orbit upper-bound bridge as written only. `proofs/FINDINGS.md`, lines 238–244, repeats the UNKNOWN claim. These are present-tense summary statements, not merely an untouched failed development attempt.

The smallest counterevidence to the UNKNOWN label is the already integrated `SafeHighWitness.exists_safe_three_returns` at `9096791b36bd8b18985328a6970a4abfc9eb4272`. Its full source compiled again in this audit and all five exported witness theorems have empty axiom sets. The stronger `SafeHighFamily.safe_three_returns_family` plus `seed_closed_form` proves the ordinary finite positive seed family `81*10^(m+7)-1`, for every natural m, with high membership at times 0,2,4,6 and nonpalindromicity through time six. The family source and all 70 theorem audits independently passed here with only `propext` and `Quot.sound`.

Commit ancestry, not dates, establishes inclusion of the family source in the initial main snapshot: comparison `9096791...169c4c8` reports merge base equal to `9096791`, ahead 22, behind 0. The later fetched overview at `eb893f0` still contains the obsolete UNKNOWN wording. The original failed sharp witness remains useful historical evidence; it should not be deleted or reclassified as safe.

A distinct later development is Agent #105's `numeric_high_returns_after_le_three`, source `167eed51bc2ae014450626b9e5c0d3302a5ae5c4`, evidence `4c8ae8abd2421af3e95ef6c6c07d4e69c0aa0519`, merged in PR #15 at `250a555e228a0ffb0ceb1daa16b8bcfe85db5a8f`. This completes the actual ordinary-integer upper-bound bridge. Agent #14 inspected its endpoint source, representation-transfer definitions, recorded eight-module execution commands, and the complete 39-query independent axiom output; only the reused rank certificate was freshly rebuilt here so far. The statement in FINDINGS that the bridge is absent from the OLD rank-only package remains literally true; add the new package rather than silently rewriting historical package scope.

## Required correction

Replace the CURRENT safe-sharpness UNKNOWN status with a link to the finite witness and all-parameter family. Distinguish the earlier unsafe witness from the later safe witness. Link the actual-integer upper-bound package as the newer formal bridge, retaining its independent-review and default-build distinctions. Keep the separate Agent #105 carry/safety-criterion package's open independent-review gate visible.

Recommended wording in substance: three consecutive high-region two-step returns are attainable while remaining nonpalindromic over the specified finite prefix; the bound is sharp in that finite sense. The m=0 witness reaches a palindrome at time eight. Neither this family nor the three-return upper bound establishes infinite safety or the assertion for 196.

No proof source is altered by this audit. This discrepancy UNDERSTATES valid progress; it is not evidence of a false central theorem. Owner notification belongs on research issue #1, with management copied through the established coordination records. Historical documents should receive a named supersession reference where useful, not silent erasure.
