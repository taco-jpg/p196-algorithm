# Independent semantic and fresh-build review

Reviewer: Agent #1 specialist `symbolic_scope`. The reviewer authored none of the three new modules. Some frozen dependencies have prior reviewer authorship; this boundary is explicit.

Status: independent review PASS at published commit `6f169320a7a750ea7978093c4cd05140d5d6cc73`. The three reviewed source hashes were unchanged at final publication and after the fresh build. All 30 source modules plus the full origin audit compiled from source with official Lean 4.19.0 and explicit `--trust=0`; no precompiled project objects were reused. No semantic finding or reviewer compile failure occurred. This review does not claim that a qualifying cycle exists.

## Exact hypotheses and quantifiers

`quotient_path_repeat` requires a positive length and literal equality of all three endpoint words B, H, and w. Each repeated successor uses its corresponding endpoint equality at the wrap. It copies the original boundedness and length-four premises at the residue, rather than inferring a full transition from a projected edge. The input sequences outside indices 0 through N are immaterial. The repeated-path conclusion admits horizon zero. `quotient_path_repeat_valid` correctly needs no closure premise for its separate pointwise validity statement; it inherits validity at each residue of the original path.

`quotientPathExponent_accounting` uses a guard at every used source before converting the literal natural subtraction into signed accounting. `quotientCycleExponent` adds a natural gain G after each completed traversal to the original finite schedule beginning at 2*N+3. For positive N every residue is strictly below N. The inherited lower bound supplies at least three copies at every residue, and the natural epoch gain cannot reduce that guard. Both wrap and nonwrap recurrence branches use this guard before commuting subtraction with the added gain. The endpoint condition for the arithmetic helper is explicit. The final schedule obtains it from the existing full-return clock theorem and the guarded signed identity; it does not assume that an arbitrary signed trajectory is a natural trajectory.

`quotient_cycle_actual_orbit` constructs one schedule k, then chooses one positive n and one initial digit function d using the original realizer before introducing the arbitrary time t. For every later t, the supplied-seed finite transport is applied to these same k, n, and d. It does not invoke the finite existential theorem separately at each horizon. The complete original canonical width and every in-range column sum are retained in the conclusion. Later digit witnesses may depend on t, as is appropriate for representations of the different orbit integers.

`quotient_cycle_safe_positive_seed` assumes Boolean safety at every residue i<N. The path gives a length-four period at each residue, so the period is nonempty, and the global guard gives a positive exponent. The original safety bridge classifies the next output of the represented integer. The theorem therefore chooses m=step n. The original `Lychrel196.IsLychrel` includes time zero, and `Lychrel196.orbit_from_step` identifies orbit(step n,t) with orbit(n,t+1); this makes the safety timing correct, including t=0. Positivity of m follows from positivity of the original ordinary orbit at time one.

## Scope boundary

The package is conditional on a supplied positive full quotient cycle, original initial validity, and (for palindrome avoidance) explicit safety at every cycle state. It constructs neither such a cycle nor safe states, and proves no claim for a particular decimal seed or 196. It does not turn an arbitrary projected graph walk into an actual quotient path. It does not strengthen the earlier finite-horizon theorem by a quantifier swap. The written METHOD already states the conditional cycle criterion; this package supplies its local repetition and guarded-exponent adapter.

## Directly inspected source interfaces

The review read the three new modules completely, plus `Agent1PeriodicGuardedPath`, `Agent1PeriodicReturnClock`, `Agent1PeriodicSafetyNumeric`, and the original definitions `Lychrel196.step`, `Lychrel196.orbit`, `Lychrel196.IsLychrel`, and `Lychrel196.orbit_from_step` in `Lychrel196Research__c696e0ea3db39d92`. The complementary reviewer independently checked the Numeric interpretation; that review is separately attributed under `complementary-review/` and is not substituted for this reviewer’s compilation.

## Observed source hashes

- `Agent1PeriodicCyclePath.lean`: `196f04ef0d9ca89e0eb6151905c0f3abf217eefcf8469c32269e0954423384a9`
- `Agent1PeriodicCycleGuard.lean`: `357d626233997cd7b1d9b2606c63f196814854abd29f7e72a1a51254c9aa2041`
- `Agent1PeriodicCycleNumeric.lean`: `4cbf4ee50c819e71ee09d108ab62fd703af1287507b969988a09e61b3fe2c527`

## Execution and audit

The exact registry SHA is `239a98f425775ffa41298e1776e7618aed4793f064115f8571f4a29bc0dabac7`. The reviewer independently read back the published remote branch at the pinned commit and checked every registered source byte and Git blob against that commit. Literal imports give exactly the 30 registered modules. All 31 commands (30 modules and ReviewAudit) returned zero in the first reviewer attempt. Original raw sources, commands, compiler hash, resource limits, output logs, and all inventories are retained in `clean-001/`.

The origin audit checked all 1,506 theorem constants and 243 safe definitions in the closure. The theorem axiom union is exactly `propext`, `Classical.choice`, and `Quot.sound`; safe definitions use only `propext`. The three new modules contribute 31 theorem constants and two safe definitions. Their ten public theorem declarations and two public definitions have complete checked types and axiom output; the larger count includes private/generated proof constants. The audit also type-checked all 124 top-level public Agent1 theorem declarations in the closure.

The separate compiler inventory records 976 generated non-safe runtime definitions: 945 compilation-stage helpers and 31 unsafe-recursion implementation helpers whose safe bases were all audited. It also records 13 compiler implementation axioms inherited from `LychrelDigitSums`, zero unsafe opaques, and no unclassified runtime definition. None of these implementation entries appears in the checked theorem/safe-definition axiom dependencies. They are not erased from the inventory or described as additional accepted proof axioms.

The parent's separate canonical run also passed all 30 modules and its ProjectAudit. Its 63 original manifest files are copied byte-for-byte under `../verification/parent-clean-001/`; a separate package manifest adds identity metadata and the exact checker snapshot. Its original report says `source_tree_clean=true` under the checker’s tracked-file status rule, and its Lean commands contain no explicit trust override. Those historical fields are unchanged and are distinct from this reviewer’s explicit trust-zero commands. This is a review of the pinned closure, not a repository-wide acceptance claim.
