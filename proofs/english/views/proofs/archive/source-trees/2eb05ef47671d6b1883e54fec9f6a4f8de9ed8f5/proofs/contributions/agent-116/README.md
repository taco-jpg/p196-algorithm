# Agent #116 — exterior-boundary obstructions to cyclic certificates

Claim: agent116-certificate-exterior-obstruction. Main baseline: eec3d5f3646cab50abad6e610ea19626cd249070; claim published at b4c05cab6570b98cd1ee5f8023f43ecd7f18c349 with expected-head checking and a non-force update.

## Completed interfaces: checkpoint01

- CertificateRealization.lean: from Valid and existing Admissible0, construct ordinary-integer realizations of every certificate state and prove a nonempty exterior has positive first coefficient. This condition is not silently added to check.
- ExteriorNormalization.lean: outerNext_stripSuffix_eq proves arbitrary input phase-suffix removal does not change the normalized exterior update; outerNext_of_partial_trim connects certificate partial-trimming equality to the deterministic normalized update. Assumptions are only actual Phase and Bounded.

Both modules and the complete local dependencies rebuilt in a fresh directory: seven modules,360 compiled theorem constants, all actually queried with #print axioms and passing with only propext,Classical.choice,Quot.sound. See verification/checkpoint-01/verification.json. Counts measure audit coverage, not independent results. Checkpoint status: **LEAN-CHECKED**; independent semantic review is recorded separately.

## Complete endpoints: checkpoint02

Agent116All.lean is the contribution's complete build root, importing every concrete finite check and final theorem. Endpoints below compiled and passed transitive axiom audits; independent fresh rebuild/semantic review now also passed:137 modules,140 successful commands,1,991 compiled theorem constants, union only propext,Classical.choice,Quot.sound. Review pins remote source c0bca37913df5b52963c484ef20cbeb5b3838a32; see [REVIEW.json](review/REVIEW.json) and full logs. Final default-branch publication status is separately recorded on shared coordination.

| Lean endpoint | Exact conclusion |
|---|---|
| Agent116.CertificateExterior.accepted_exceeds_three | For arbitrary cert, original check cert=true alone gives i<cert.P whose state has exterior length>3 after maximal phase-suffix removal. No extra realizability, positive-head, period-cap, or inner-block-length hypothesis. |
| check_eq_false_of_normalized_cap_three / check_eq_false_of_raw_cap_three | Every candidate whose normalized exterior, or more strongly raw exterior, always has length≤3 is rejected by the original checker, including empty certificates. |
| P196.Agent116.Cap3.cap3_exit_witness | For eight even phases, a valid exterior of length≤3 exits that cap within nine steps. With both ordinary-decimal template bands at least18, Agent116.ActualCap3.lychrel_cap3_exit connects this to actual Lychrel196.orbit. |
| P196.Agent116.Cap3.cap3_all_exit_witness | No positive-head or normalized-input requirement: every exterior of length≤3 and coefficients≤18 exits within ten steps. |
| cap3_sharp_first_exit / cap3_all_sharp_first_exit | Witnesses(8,[11,9]) and(6,[0]) first exit at steps9/10 respectively. The second is in the relaxed domain, without a claimed ordinary positive-integer realization. |

The main advance completes arbitrary certificate partial trimming → deterministic normalized exterior periodic orbit → finite-graph exit. A kernel proof over the entire relaxed domain removes the intermediate cap2 version's Admissible0 assumption. This restricts this certificate format, not every possible infinitely safe mechanism.

Finite checks use two sets of57 kernel batches; Lean decoding completeness and aggregate batch theorems prove coverage. Independent Python scans support discovery/cross-checking, not axioms. All successful/failed sources and logs and exact generator-reproduction records remain.

No valid cyclic-certificate instance, infinitely safe orbit, or proof of the196 conjecture is supplied.

## Reproduction

Run at repository root with Lean4.19.0, release commit6caaee842e94:

```sh
python3 proofs/contributions/agent-116/check.py /absolute/path/to/lean \
  --evidence /tmp/agent116-fresh \
  --module Agent116All --jobs 2
```

The evidence directory must not exist. The script copies/hashes the whole import closure, rebuilds fresh local objects, enumerates every local theorem in the compiled environment, and executes transitive axiom audits individually. Adapted from Agent104's existing build script; this pass fixed parsing of declaration names ending in apostrophes, preserving the first failed audit in development/runner/baseline-01/.

This host uses the existing public readlink shim to locate unchanged official Lean; distribution/binary hashes match prior repository records. Original research, failed attempts, and full substantive logs remain; regenerable build products, copied dependencies, and toolchain installations are not committed.
