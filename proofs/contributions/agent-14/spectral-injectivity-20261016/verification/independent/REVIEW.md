# Independent build and axiom review

**Result: `INDEPENDENT_BUILD_AND_AXIOM_PASS`.**

Reviewer: genuine Agent #14 `/root/runtime`, separate from the authors of the
three mathematical modules. This review covers source identity, fresh Lean
execution, public signatures and axiom dependencies. The separate semantic
review is retained by `/root/spectral_semantics`.

## Exact source binding

The target published checkpoint is
`1418f5c176582435d6aa824da72513117da2832b`. The parent verified that publication
against its remote file bytes. This specialist checked the following exact
local source hashes, which bind this execution to those mathematical files.
This specialist did not check out or independently fetch that commit. The
execution correctly records the unchanged local checkout HEAD
`5ff4f607535587d572fbc9e95ba9501d1fbe5fc5`.

| Module | SHA-256 |
|---|---|
| `LychrelDigitSums` | `ca5f46523b7cff02c00918b6466a97963087b499fb5f184232b8b3d806dc0b57` |
| `Agent14SpectralWeights` | `d691d02f3170db988ac9c5529402f5c09cf83425c7188d78cd0f2a6a8f4568c8` |
| `Agent14SpectralInjectivity` | `082347eccad303f235a835c65be2dc20062d4457646082575cd192d06601d0c9` |
| `Agent14SpectralDecimal` | `c3bc01e978d9bd3e90fc8c6b7a185432f02db94184eaec324bbb3f762fb978a2` |

The registry SHA-256 is
`e20ae868441cf27fec279a0659d443e4cefeffbb3d23e6bb79cbfe9d90ea0073`.
Every source also matched its registered Git blob identity. Sources and the
registry were checked again after the completed audit.

The original runners' `source_tree_clean` fields check tracked changes using
`--untracked-files=no`. They do not certify that newly added source files were
already committed locally. Exact selected-source identity is established by
the explicit hashes above and the retained source snapshots.

## Execution and independent checks

The official toolchain is Lean 4.19.0, release commit `6caaee842e94`. Its
executable SHA-256 is
`92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.
The reused complete runtime was independently compared with all 4,617
nondirectory members of the official release archive during this session.
That archive's SHA-256 is
`6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe`.
No toolchain patch or host readlink adapter was used. Supported execution
escalation was required because the ordinary hosted sandbox could not locate
the application and later could not create a mount marker on the full disk.

Two distinct executions were completed:

| Execution | Result | Actual compiler flags | Coverage |
|---|---|---|---|
| Unchanged canonical verifier | `PASS` | `-j1 -DElab.async=false` | Four fresh modules, 15 endpoints, all 1,077 theorem constants |
| Independent rebuild and audits | `INDEPENDENT_BUILD_AND_AXIOM_PASS` | `--trust=0 -j1 -DElab.async=false` | Four fresh modules, all 1,237 safe constants, 50 explicit public signatures and literal axiom reports |

The canonical verifier is the unchanged
`proofs/verify_project__214bf7673efe116b.py`, SHA-256
`c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a`.
Its literal `Agent #1` report field belongs to the historical verifier; the
current executor is identified separately as Agent #14/runtime. The canonical
execution did not use `--trust=0`.

Canonical sources, logs and manifests were verified before removing its
reproducible objects. The independent build then began with zero local project
objects and compiled all four sources again with the strict flags. It reused
no author project objects. `LychrelDigitSums` took 69.118373 seconds in the
canonical run and 66.246179 seconds in the strict run. The strict Decimal
module took 0.467366 seconds. Every mathematical compilation exited zero.

## Complete safe-constant and public-declaration audit

The independent Lean audit enumerated every imported declaration whose module
origin belongs to the four-source closure. It rejected safe custom axioms and
any transitive axiom outside the permitted set, auditing safe definitions and
other safe kernel declarations as well as theorems.

| Module | Theorem constants | Safe definitions | Other safe constants |
|---|---:|---:|---:|
| `LychrelDigitSums` | 986 | 131 | 14 |
| `Agent14SpectralWeights` | 36 | 10 | 0 |
| `Agent14SpectralInjectivity` | 51 | 5 | 0 |
| `Agent14SpectralDecimal` | 4 | 0 | 0 |
| **Total** | **1,077** | **146** | **14** |

The 14 other safe constants consist of four inductives, six constructors and
four recursors. There are no safe opaque constants in this closure. Counts
include generated auxiliaries and are not counts of distinct mathematical
claims.

The complete safe axiom union is exactly:

```text
Classical.choice
Quot.sound
propext
```

The audit separately inventoried 794 unsafe and 20 partial implementation
constants. Their names and kinds are retained in
`audit-continuation-001/implementation-inventory.json`. These implementation
declarations do not enlarge the permitted axiom set; no disallowed axiom
occurred in any audited safe declaration's transitive dependencies.

All 50 explicit public source declarations of the three new modules were
checked with `#check @name` and literal `#print axioms name`: 42 theorems and
eight definitions. Their module origins were checked against the source
declaration list. Their literal axiom reports agree individually with the
exhaustive safe-constant audit. The registry's 15 named endpoints are included.
Full signatures, including explicit arguments and universes, are retained in
`audit-continuation-001/public-types-and-axioms.log`.

The accepted scope is the literal recurrence weights, their domination,
fixed-width injectivity for symmetric natural coefficient words bounded by 18,
and the registered original decimal column-sum corollaries and finite controls.
The registry retains its explicit exclusions and `repository_wide_pass: false`.

## Preserved parser failure and completed continuation

All four strict compilations and the Lean safe-constant audit in `run-001`
exited zero. Lean pretty-printed the final three-element axiom list over three
lines. The original Python parser expected a single line and ended with:

```text
ValueError: Safe audit output is absent or incomplete
```

The original `FAIL` report, complete logs, sources and manifests remain
unchanged in `run-001`. Its exact runner, SHA-256
`faf1fd95d9ecbaab46afde729e0e2532569b26c235442eadd1e4ee1fc888aba0`, is preserved
as `development/rebuild-initial.py`. The repaired `rebuild.py` accepts wrapped
axiom arrays and checks all reported counts and the complete axiom union.
No mathematical source or generated Lean safe-audit program was changed.

`complete_audit.py` verified every original evidence hash, every frozen source,
the original strict compiler commands, compiler identity and current object
hashes. It parsed the already completed Lean audit and executed the remaining
public type and axiom checks with `--trust=0`. It then verified that sources,
objects and runtime remained unchanged. Its successful result is retained in
`audit-continuation-001/verification.json`. This is a continuation of the same
fresh independent build, not an additional fresh rebuild or a relabeling of
the original failed parser result.

## Reproduction and retained evidence

The corrected `rebuild.py` performs the complete process in a new output
directory. From the repository root, supply the official Lean executable and
a new evidence directory:

```sh
python3 -B proofs/contributions/agent-14/spectral-injectivity-20261016/verification/independent/rebuild.py \
  --repository "$PWD" \
  --lean "$AGENT14_LEAN_BIN" \
  --output "$AGENT14_EVIDENCE" \
  --decimal-sha256 c3bc01e978d9bd3e90fc8c6b7a185432f02db94184eaec324bbb3f762fb978a2 \
  --canonical
```

The archive prepared by `package_evidence.py` retains the earlier runtime and
six-module baseline evidence, the canonical spectral replay, the strict
source build, both parser versions, the completed continuation, generated audit
sources, substantive logs and this review. It excludes reproducible objects
and caches and the external official runtime distribution. Every retained file
is checked by SHA-256 and byte count after streaming extraction from the archive.
No source publication, PR review submission or Git mutation was performed by
this specialist.
