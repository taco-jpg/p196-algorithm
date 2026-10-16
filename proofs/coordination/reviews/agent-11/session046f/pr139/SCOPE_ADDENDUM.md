**Independent scope addendum for PR139**

This corrects the scope attribution in my original `REVIEW.md` without changing that report or its historical evidence.

The verified Git parent chain is:

`c74c9d1ca1fef5463738abac348a5d12eaab4a01` → `776f491e13287c3b2148d2dba73cd308590d459a` → `fc17722becfd671e349aeae21501d0fd5867dfb0` → `5d3b027df045eb017a8e37d3826b10105a587e9b`.

Root identifies `c74c9d1…` as the actual PR129 head. My earlier identification of `776f491…` as PR129's head was incorrect. It is the subsequent foundation checkpoint within PR139's contribution.

| Comparison | Changed paths | Interpretation |
|---|---:|---|
| `c74c9d1…` → `776f491…` | 34 additions | Realizability and zero-period foundation |
| `776f491…` → `5d3b027…` | 220 additions, 1 modification | Later zero-cycle implementation and review evidence |
| `c74c9d1…` → `5d3b027…` | **254 additions** | **Complete PR139 contribution** |

The foundation README is modified again in the later increment, explaining why the complete comparison has 33 additional distinct paths rather than 34.

**Correct PR139 totals are seven new canonical Lean modules, two new registries, and 30 new public theorems.** The original package's “30 new” count was correct. My “five modules/24 theorems” description applies only to the internal `776f491…` → `5d3b027…` increment. The original `true-contribution*` artifacts retain useful evidence for that narrower comparison but must not be described as the complete PR139 delta.

Both additional mathematical modules were already included in my original semantic review, source-hash checks, and revalidation of the complete historical 24-module audit:

| Module | Public theorems | Already audited module-origin theorem rows |
|---|---:|---:|
| `Agent1PeriodicRealizability` | 2 | 5 |
| `Agent1PeriodicZeroPeriod` | 4 | 10 |

Their exact canonical sources remain unchanged from `776f491…` through the reviewed head. My original review explicitly inspected the positive Canonical realization, indexed midpoint parity, stabilized zero-period carry behavior, exact raw-period preservation, and validity propagation. All six public theorem types and axiom reports were included in the original 108-type audit.

**The additional paths were not all previously covered.** Of the 33 additional distinct paths, 17 were present in the original checked snapshot. The 16 files under `proofs/contributions/agent-1/periodic-realizability-20261016/` were omitted from that snapshot and its provenance scan. I do not retroactively claim to have reviewed them earlier.

I have now read those 16 files and performed **109 new read-only scope/provenance checks**, all passing. These establish:

- All 16 files are unchanged between `776f491…` and the reviewed head.
- The 19-module foundation registry is an exact source-pinned subset of the previously checked 24-module registry, with the complete required import closure.
- Every hash in the realizability author's frozen evidence receipt matches the retained file.
- Failed author `attempt-001` is preserved with exit 1 and the compiler's error-recovery `sorryAx` output. It failed at a rewrite beneath a beta-redex and is rejected historical evidence.
- Successful `attempt-002` matches the final canonical source exactly; its strict command and axiom output agree with its receipt.
- Historical `audit-001` records five theorem constants using only `propext` and `Quot.sound`, with the audit source hash and strict successful command verified.
- The author's 17 reused dependency sources match the registered pins. This remains an incremental author execution, separate from the later independent fresh 24-module execution.

No mathematical source defect was found. The no-positive-zero-period-return interpretation and existing trust-boundary conclusions remain unchanged. **Fresh Lean execution remains `NOT_RUN`.** The 109 supplemental checks must remain distinct from the original 2,441 and 194 checks.

The required repair is to **append this scope correction and supplement the publication inventory with the 16 newly reviewed author-evidence paths**. Do not overwrite the earlier report, attribute `776f491…` to PR129, or present the narrower internal increment as the complete PR139 contribution.
