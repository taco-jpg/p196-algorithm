# Constant-eighteen quotient return: source and ownership check

2026-10-17. Reviewer: `/root/research_status`, a same-session specialist.
Read-only source/coordination inspection; no proof, Lean execution, experiment,
Git mutation, claim, or external message was performed for this scout.

**Finding:** the proposed period-four one-run boundary application is distinct
from the inspected Agent 7 population-renewal claim. No exact existing theorem
or competing claim for the endpoint below was found in the checked records and
sources. This is a bounded ownership finding, not proof of the endpoint, owner
acknowledgment, or release of Agent 7's active scope.

```lean
theorem quotient_path_eighteen_no_return
    (B H w : Nat → Agent8.Word) (N : Nat)
    (hp : QuotientPath B H w N)
    (hv : ValidPeriodic (B 0) (H 0) (w 0))
    (hw : w 0 = [18,18,18,18]) (hN : 0 < N) :
    ¬ (B N = B 0 ∧ H N = H 0 ∧ w N = w 0)
```

The proposed statement comes from cap4_existing_theorems' separate source
scout, `periodic-next-obligation-scout.md`. It has no safety hypothesis and
excludes a complete tuple return, rather than a phase self-edge. Its boundary
geometry and finite tracking estimates remain proof obligations.

## Current ownership and publication

Initial and final live coordination reads agree at
`1004f1f804eac1eaec8cb01fc433fe2c5032fcd0`. Agent 7's task
`proofs/coordination/tasks/agent7-run-population-renewal-20261016.json` is
**CLAIMED**, exact blob `caf4e64b9730b3deb85ed4e831a225747e8516b3`.
It is unchanged from the prior complete 237-record snapshot at
`42364746152af5d540e31051eafdd24cb6aa4c5a`. The intervening deltas through
`e123eb836f9a2f1158280a507e6b831463e3ff3b` were inspected in the checker scout;
the only further changed task is Agent 1's independent PR165 verification.

Agent 7 owns, for arbitrary original `Admissible L q` and `c = 0 ∨ c = 18`:

- Partitioning **every** successor maximal run into a wholly born run or the
  exact nonempty descendant of a unique old maximal run.
- Unique founder-run/state-time coverage for every later maximal run.
- Birth-free whole-population extinction after `4*R+1` and eventual
  birth/occurrence equivalences, with ordinary-integer interpretation.

The task explicitly excludes **“No reproof or new ownership of existing
no-merging, one-run lifetime, numerical representation or restart facts.”**
The published README is narrower still about its positive ownership:
**“This contribution owns only the population coverage and its stated
temporal consequences.”**

The actual branch `research/agent-7/run-renewal-20261016T2225Z` remains at
`638a9957c3a9549dd6aa59da75a9ad8dc61cce36`. Its complete, untruncated tree has
the scope package and unchanged dependency snapshots, but none of the five
planned new theorem files (`MaximalIntervals`, `RunOrigins`, `RunFounders`,
`RunRenewal`, `RunRenewalInteger`). The task's null published-source field is
therefore stale relative to its **scope** checkpoint, not evidence of a
published new theorem. The branch absence is not abandonment or release.

The original [Agent 7 scope notice](https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6225764887)
expressly credits existing exact surviving intervals/maximality/no merging
and one-run extinction. Parent's specialized application notice is
[6227856515](https://github.com/taco-jpg/p196-algorithm/issues/61#issuecomment-6227856515).
The final issue read ends at that notice. No Agent 7 reply to it was observed;
silence has not been treated as consent.

## Exact existing statements, not a new population premise

`RunAncestry__5f2702512ad8719e.lean` is identical on the inspected Agent 7
branch and current main `74a1c3922eb7af438fe40b23d2105ad07556e3f5`:
blob `cdabce887a7f2ca952447f01bd99a2fe30855b81`,
SHA256 `6c8041050576a142949376818a2e37997031ce40b99a7908a763396ee702a9eb`.

- `MaximalRun` (line 31) means a nonempty physical interval `[a,b)`, all
  coefficients equal to c, with unequal neighbors unless at a word end.
- `descendant` (line 39) is `(a or a+1, b or b-1)` when the **actual** terminal
  carry is zero, and exactly `(a+1,b)` when it is nonzero.
- `descendant_step` (line 178) assumes original admissibility, an extreme
  symbol, and one old maximal run. Besides exact survival on its old interval,
  it proves that every nonempty descendant is maximal in the **whole** next
  word. Containment and loss of at least the overflow bit are already proved.
  This whole-word maximality is the existing fact preventing a newly born
  neighboring band from silently extending the tracked run.

The final original `AncestryExtinction__567be2f804ec7f4c.lean` is likewise
identical on the branch/main: blob `aa32de68b258f36361f56c102852f39bc21b29c5`,
SHA256 `4563ec3dffa0a69d3df3b3312eb783f835f76cacdd2261f9c88ed0b9f06d3c7e`.
`track`, `track_invariant`, `survival_bound`, `extinct_uniform`, and
`orbit_ancestry_extinct` follow **one selected initial ancestry**. They do not
identify a later run merely because it has the same symbol or location, do
not supply whole-population coverage, and do not prove the proposed quotient
return exclusion.

The retained earlier file `AncestryExtinction__91bf7e70e989cdfe.lean` has
SHA256 `d0099b058b94f5edc083b9f6e3f38495ee6405f9d9feadeb75d88c39bc33a768`.
The later version appends `central_run_step`; their preceding bytes agree.
That one-step central-run statement still is not the proposed full return
obstruction. The minimal proposed route needs only `RunAncestry`, not either
extinction version; historical verification of the earlier version must not
be relabeled as verification of the appended theorem.

## Safe ownership boundary for a narrow claim

The new application may own static geometry for the displayed
`periodicWord B H [18,18,18,18] k`, existence of one maximal run covering its
left repeated band, and a recursion tracking that selected run through the
already guarded finite quotient path. The proposed left endpoint
`B.length - (B.reverse.takeWhile (· == 18)).length` depends on B, including its
terminal eighteen suffix. Reusing unchanged `descendant_step`, the existing
list/index successor bridges, original admissibility, and actual-clock gain
to compare that boundary after a supplied return is distinct from generic
population renewal.

Keep a general all-words maximal-interval constructor, predecessor/birth
partition, unique predecessor/founder theorem, and temporal coverage out of
this claim. Agent 7 has specifically assigned `MaximalIntervals` and
`RunOrigins`; broadening a convenient local helper into those APIs would
require renewed coordination. Existence scoped to this explicit periodic
band does not need that broad theorem. No new generic extinction or
no-merging result should be claimed.

The proof still must establish rather than assume: survival of the chosen
descendant across every intermediate step; its maximality and in-range
indices; equality of original terminal carry with the actual raw clock;
and the endpoint identification under the literal full tuple return. Empty
B/H, B ending in eighteens, and H joining both bands cannot be excluded.
These are semantic obligations recorded here, not newly proved claims.

Other adjacent lanes remain intact: historical affirmative
`periodic_interface_followup` search/lift; Agent 418 compatibility; Agent 8
potential refinements; and the generic supplied-cycle checker proposal.
This task supplies no accepting cycle, no population absence theorem, no
safe infinite witness, and no conclusion about 196.

## Evidence and limits

`periodic-eighteen-return-scout/` retains exact API task/ref/tree/comment
receipts, seven decoded source/scope files, source pins, and main/branch
identity receipts. Every downloaded source was checked against its Git blob
hash and SHA256. The prior all-task comparison is retained separately under
`periodic-cycle-checker-scout/`; this report does not claim a new read of all
remote branch source trees. No mathematical source was changed or executed.
Parent remains sole Git writer and ordinary issue-chat relay.
