# Independent review: Agent116 exterior certificate obstruction

**INDEPENDENTLY-REVIEWED — PASS**, for remote source commit
`c0bca37913df5b52963c484ef20cbeb5b3838a32`.

This is the separate `agent116_claim_audit` agent's semantic review and actual
clean-source execution. The reviewer did not edit the proof-author modules and
did not invoke the author's checker. It is an independent AI review within the
same project session, not external human peer review. No merge or shared
accepted-build registration is performed by this review.

## Source identity

The execution snapshot matches all 137 corresponding Git blobs at local commit
`0bb18e90701b318168672e22ece8be6ae25de5b8`. The reviewer independently compared
both locally available Git trees: that commit and the remote source commit above
have the identical tree `22d91671e98a7c4283ee920470ec249a1c7c6c74`.
`execution/final/source_commit_check.json` and `remote_mapping.json` retain those
checks. All snapshotted source files remained unchanged at build completion.

The selected roots were `Agent116All` and `CanonicalityCounterexample`.
Their complete closure contains 128 new proof modules, eight existing dependency
modules, and one three-theorem review fixture. Each of the eight existing
dependencies was also checked byte-for-byte against baseline
`eec3d5f3646cab50abad6e610ea19626cd249070`. This includes the original
`LychrelDigitSums`, `PeriodObstructions`, `Compat`, and Agent109/Agent7 sources.

## Actual fresh execution

The independent runner `rebuild.py` created the previously nonexistent directory
`/workspace/scratch/b9ccc76d924e/review-build116/final`, snapshotted the full source
closure before compiling, set `LEAN_PATH` to that snapshot, and compiled with
two workers, each using `-j1 -DElab.async=false`. No existing project `.olean`
was imported. The toolchain's standard library objects were reused; this is not
a source rebuild of Lean or Std.

All **137 source compilations exited zero**, including the 57 valid-domain and
57 unrestricted finite-check batches, their coverage/assembly proofs, the
ordinary-integer endpoint, and the final aggregate. The separate compiled
environment audit also exited zero. In total the execution record contains
140 successful commands, including version and prefix queries.

The audit discovered and queried all **1,991 theorem constants** belonging to
the local closure, including private/generated constants and existing
dependencies. This is an audit inventory, not a count of new mathematical
results. Every actual `#print axioms` result is a subset of
`{propext, Classical.choice, Quot.sound}`. No `sorryAx`, `Lean.ofReduceBool`,
custom axiom or other unapproved proof dependency occurs. Executable source
tokens for admitted proofs, `native_decide`, `implemented_by` and `extern` were
also rejected by the runner's comment/string-aware source scan.

The full audit log SHA-256 is
`57eb26098a530251b34e0cf21f19fa929fd2aadf5cdeb993e2062b7909ec7cb0`.
Full commands, timings, exit codes, source hashes, individual compiler logs and
all axiom output are under `execution/final/`. Compiled objects and duplicate
source build directories are excluded as reproducible infrastructure.

The runtime was Lean 4.19.0, commit `6caaee842e94`, using the shared verified
release binary SHA-256
`92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.
The reviewer inspected the transparent wrapper and shim: they redirect only
the process's own `/proc/<PID>/exe` readlink to `/proc/self/exe` for this host.
Their fingerprints are recorded in the manifest. The reviewer did not download
a separate toolchain; independent execution and semantic review use the same
verified release installation as the authors.

## Mathematical disposition

The detailed statement review is in `SEMANTIC_REVIEW.md`. The accepted results
retain their exact scope:

| Endpoint | Reviewed conclusion |
|---|---|
| `outerNext_of_partial_trim` | Arbitrary partial certificate trims induce the original deterministic exterior transition after maximal suffix normalization. |
| `accepted_admissible_exceeds_two` | The existing canonical cap-two certificate obstruction, with explicit `Admissible0`. |
| `cap3_exit_witness` | Every valid even-phase exterior of length at most three exits cap three by time nine; its exterior sharpness is checked. |
| `cap3_all_exit_witness` | Every bounded even-phase exterior of length at most three, including zero-leading and untrimmed words, exits by time ten; its distinct sharpness is checked. |
| `accepted_exceeds_three` | Boolean certificate acceptance alone implies some listed state's maximally stripped exterior has length greater than three. No admissibility or positive-head premise remains. |
| `check_eq_false_of_normalized_cap_three`, `check_eq_false_of_raw_cap_three` | The original checker rejects every candidate confined to the respective cap-three domain, including empty candidates. |
| `lychrel_cap3_exit` | With the explicit actual-template, valid-exterior and band-length-at-least-18 hypotheses, the genuine ordinary orbit's specified exterior coordinate exceeds three within nine steps. |

The complete finite kernel proof discharges the escape premise of the
check-only theorem. The cyclic phase proof covers odd initial possibilities by
using the last link; period positivity and modular indices are explicit.
There is no supplied accepted certificate, infinite safe orbit, Lychrel witness,
or theorem about 196. The ordinary endpoint concerns the specified template
coordinate, not every alternative representation of the integer.

## Independent controls and prior checkpoint

The independent arithmetic controls passed 231,680 phase-append comparisons,
115,840 trim-invariance comparisons and 3,000 literal integer controls. The
complete unrestricted scan covers all 57,920 encoded inputs, finds no cycle,
and has maximum exit time ten with three maximizers. These are finite
experiments; the accepted all-domain implication relies on the kernel proof.
Full scripts, counts, paths and logs are retained alongside this review.

An initial clean replay of the nine-module cap-two/normalization closure and
385 theorem constants also passed; its exact evidence is retained separately
under `execution/initial/`. The review's rejected initial hand conjecture about
a zero-headed six-cycle, its explicit withdrawal and the corrected fixture are
documented in `SEMANTIC_REVIEW.md` and `development/`. That failed conjecture is
not used by any accepted proof or this review's conclusion.

Reproduce the final closure from this checkout:

```sh
python3 proofs/contributions/agent-116/review/rebuild.py \
  --build /absolute/new-empty-build-directory \
  --lean /absolute/lean-4.19.0/bin/lean --jobs 2 \
  Agent116All CanonicalityCounterexample
```
