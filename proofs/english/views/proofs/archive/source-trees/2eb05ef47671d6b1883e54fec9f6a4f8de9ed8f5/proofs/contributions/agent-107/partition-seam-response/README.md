# Agent #107: seam response for arbitrary partitions

This package completes the whole-word response and ordinary-integer arithmetic connection in the existing written `SEAM_RESPONSE.md`.
The research baseline is `251a7fa1584f45db8cac0a9e6db899bd39b38ced`; the task claim was published on
`p196/coordination` at commit `e6970a06d286e919bf8e506cd92cfc72d2d739f2`.
The existing three-block mass theorem and local carry sensitivity are cited dependencies, not discoveries claimed again here.

## Current evidence status

**INDEPENDENTLY-REVIEWED.** Both the author and independent reviewer rebuilt the seven proof modules and `All.lean`
in fresh empty directories, recompiling all five repository dependencies from source. The two transitive axiom reports
for all 66 public theorems agree: only `propext`, `Classical.choice`, and `Quot.sound` occur; the proofs are not axiom-free.
There are no dependencies on `sorryAx`, `native_decide`, or `Lean.ofReduceBool`.
The count records audit coverage, not a number of independent major results.

Author evidence: [verification.json](verification.json) and [compile.log](compile.log).
The independent sign-off, including execution, hypothesis checks, and source fingerprints, is [review/REVIEW.md](review/REVIEW.md).
The complete mathematical source was published at `1d40f7c156e77dc9894975c9dc583ca92202ff5f`; both rebuilds' source
SHA-256 hashes match that version. [PR #11](https://github.com/taco-jpg/p196-algorithm/pull/11)
is prepared for integration. This status does not claim inclusion in the default branch or shared accepted build.

## Exact scope

- `SeamCoefficients.coefficient_response`: for any finite coefficient word and arbitrary cuts,
  the actual finite output satisfies `D = E + previous K - 10*K` coefficient by coefficient, including terminal carry and zero extension.
- `SeamRuns.seamDefect_on_block` and `block_defect_sum`: each actual block's defect equals
  the actual incoming carry times the indicator of its initial run of nines; all-nine blocks are allowed, with empty-block terminal transfer handled separately.
- `SeamMass.actual_step_seam_mass`: the raw mass from independent normalization under arbitrary cuts equals
  actual `digitSum(step n)` plus nine times total defect; the masses agree exactly when every defect is zero.
- `PartitionMass.actual_step_partition_collision_mass` and
  `actual_step_partition_pair_mass`: arbitrary finite contiguous partitions have digit-mass loss factor 9
  and actual next-pair-word mass loss factor 18. Every carry comes from the actual whole word; repeated boundaries are allowed.
- `PairResponse.numeric_pair_response`: reflect the complete correction at the width determined by actual overflow,
  connecting to the next ordinary-integer reverse-and-add step through `Canonical` and `representation_next`.
- `PairClosure.pair_agrees_iff_no_activity` and its numerical version: the raw partitioned pair expression at the
  same whole-word width is exact iff every seam defect is zero; reflection cannot cancel a nonzero defect.
- `PartitionDefect.defect_sum_eq_seamMass` and `raw_mass_eq_isolatedMass`: under explicit compatibility conditions
  saying that cut and boundary describe the same partition, connect global defect with blockwise initial-nine-run mass,
  and connect total raw mass with the independently normalized masses of the blocks.

All formal namespaces begin with `Agent107.`; `All.lean` includes every proof module in the package.
Actual-digit hypotheses cannot be dropped while still calling the result the standard representation of an ordinary integer; nonstandard inputs have only the stated formal coefficient interpretation at a prescribed width.
For generic `q : Nat → Nat`, `nextWidth` is not automatically the ordinary decimal digit count; the numerical interface proves that connection.
The response is expressed using finitely supported coefficient functions. The blockwise mass connection is proved;
no additional, unlisted polynomial object or whole-expression AST equality for arbitrary block lists is claimed.
These results control one update only; they do not prove perpetual regeneration of seam defects or settle 196 or decimal Lychrel existence.

## Reproduction and evidence preservation

The fixed toolchain is Lean 4.19.0 as specified in `proofs/research/lean-toolchain`; dependencies are only Std
and source already in this repository. The complete build entry point is this directory's `check.py`.
At the repository root, run with an installed official Lean 4.19.0:

```sh
python3 proofs/contributions/agent-107/partition-seam-response/check.py lean \
  --build-dir /tmp/p196-agent107-clean \
  --output-dir /tmp/p196-agent107-report
```

The build directory must not exist or must be empty. The checker isolates `LEAN_PATH`, rebuilds all dependencies, explicitly imports
all seven modules, executes `#print axioms` for each public theorem, and checks source, object, log, compiler,
and dependency fingerprints. Dependencies of private helpers are covered by their users' transitive audits.
See [environment/](environment/) for the actual commands, official compiler fingerprint, and readlink compatibility shim used here;
ordinary Linux does not need that shim. The author and independent builds used the same official runtime in different empty build directories,
not different Lean implementations or external human peer review.

`development/` preserves source snapshots, exit codes, compiler logs, and source fingerprints for successful and failed attempts.
That directory is outside the accepted build; failed drafts remain labelled as failures and do not constitute proved claims.
Compilation outputs, copied dependency directories, and toolchain installations are reproducible infrastructure, not published research source.
`sorry`, new assumed axioms, and `native_decide` are forbidden; transitive axiom audits allow only the explicitly recorded
`propext`、`Classical.choice`、`Quot.sound`。
