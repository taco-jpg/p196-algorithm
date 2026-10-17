# Independent canonical verification: 620 certificate

## Result

**PASS_CANONICAL_SELECTED_620_CLOSURE.** Agent 104's `runtime_scout` performed
one complete fresh canonical build of the frozen 620 certificate. The unchanged
canonical checker completed **523 source modules and one final ProjectAudit**;
all **524 commands exited 0**. The exhaustive module-origin audit checked
**3,047 theorem declarations**, including compiler-generated theorem helpers.
The theorem axiom union is exactly
`[Classical.choice, Quot.sound, propext]`.

The original canonical report and its project both say `PASS`. The outer
execution report additionally confirms that the source snapshots, input files,
compiler libraries, and all 1,471 official standard-library `.olean` files were
unchanged at completion. No second full build or additional root `--trust=0`
check was performed.

## Frozen mathematical sources and endpoints

The 510 concrete sources and generation manifest were checked against the
actually published commit
[`dc2123ae4a4513acfe75e0a6cd21c3b6a044bec4`](https://github.com/taco-jpg/p196-algorithm/commit/dc2123ae4a4513acfe75e0a6cd21c3b6a044bec4),
tree `8836aacee2ce47903df4f5edce7bd5b8ca275dab`. Their manifest SHA256 is
`d2b92c7139f59fe1cb8268addd0d10073780275f06b109bc3cf72933f9170c03`.
The remaining 13 generic sources were fetched again from their pinned Git
objects at `ae8bbdfd2a18e8910eebc25fd2a81661c01abc16`. Every one of the 523
source records has a real source commit, Git blob, SHA256, and exact imports.
No source record has a null commit.

The root is
[`proofs/Agent104Prefix620.lean`](https://github.com/taco-jpg/p196-algorithm/blob/dc2123ae4a4513acfe75e0a6cd21c3b6a044bec4/proofs/Agent104Prefix620.lean),
SHA256 `9c4af5ff576c4184c1beb7fded6e1c0a33a815bfb1130793029815e66ab3e653`.
The canonical registry checks these three endpoints:

| Endpoint | Meaning | Axioms |
| --- | --- | --- |
| `Agent104.Prefix620.palindromeStarts620_iff` | The target predicate is exactly a decimal palindrome whose canonical numeral has at least three digits and starts with 6, 2, 0. | none |
| `Agent104.Prefix620.ancestry_bound12` | For every positive natural seed `A`, target `P`, and iteration count `t`, reaching such a target implies `t ≤ 12`. | `Classical.choice`, `Quot.sound`, `propext` |
| `Agent104.Prefix620.no_196_620_palindrome` | No iterate of the ordinary reverse-and-add orbit from 196 is a palindrome starting with 620. | `Classical.choice`, `Quot.sound`, `propext` |

The last two root statements have no certificate hypotheses. The result is
scoped to this target family and this registry. The separately verified
depth-12 witness is outside this execution's 523-module registry and must be
cited separately when establishing optimality.

## Exact execution method

The build directory
`/tmp/agent104-prefix620-canonical-independent-v1` did not exist at startup.
The original-layout replay and the canonical checker each created their own
new source/build directories. All 523 selected modules were compiled from
their exact source bytes. No author `.olean` was reused.

The official compiler was Lean 4.19.0, release commit `6caaee842e94`. The
unchanged canonical checker used its original commands:

```text
lean -j1 -DElab.async=false -o Module.olean Module.lean
lean -j1 -DElab.async=false ProjectAudit.lean
```

The original compiler default trust level is `max`; these commands did not
include `--trust=0`. Imported project artifacts were protected by rebuilding
every selected source in dependency order in the empty build. The standard
library was separately compared byte-for-byte with the official archive,
SHA256 `6fe3ce97a58f44e2b3567d455b994eacec5bfe9ae7774f2a573444480ba813fe`,
and its 1,471 module digests were checked before and after this build.
The original wrapper, replay helper, and verification backend were unmodified:

| Component | SHA256 |
| --- | --- |
| Repository wrapper | `e314b0656470773e81d14d04bbb548f914cd9e9808c89fdb07166d8ca58ef55b` |
| Original-layout replay helper | `744180f651360c1df34d1fad465dc009a304abbafab5277ddfb163a738430c70` |
| Canonical verification backend | `c047ff1ff1fe12b2c2094ca5f36af871b1c6faf89db593a102f9c2f7d48cc98a` |

Only one Lean process was used by this verification. Canonical wall time was
**1,504.317765 seconds**; the outer run, including preparation and final
integrity checks, took **1,510.532073 seconds**. Module compilation consumed
1,381.857806 seconds and the final audit consumed 117.845311 seconds.

## Complete theorem and axiom statistics

There were 456 modules containing audited theorem declarations and 67 modules
without theorem declarations. All 523 modules were compiled. The theorem
counts by exact axiom set are:

| Exact theorem axiom set | Theorem declarations |
| --- | ---: |
| none | 1,577 |
| `Classical.choice` | 15 |
| `Classical.choice`, `Quot.sound`, `propext` | 105 |
| `Quot.sound`, `propext` | 922 |
| `propext` | 428 |
| **Total** | **3,047** |

The checker found zero safe custom axioms. It recorded **70 unsafe
implementation axioms**, with their complete names and origin modules in the
raw report and `THEOREM_AUDIT_STATISTICS.json`. None occurs in the audited
theorem axiom union. That statistics file also gives every selected module's
theorem count and the three individual endpoint axiom sets.

## Retained evidence and metadata interpretation

`canonical/` retains 527 original evidence files byte-for-byte: the original
report and output inventory, all 524 compiler/audit logs, and the generated
`ProjectAudit.lean`. `CANONICAL_RETAINED_FILES.json` records their digests and
their original execution paths. The reproducible `.olean` outputs remain in
the temporary build and are excluded from the publication list.

`source-snapshot.json` and `SOURCE_SNAPSHOT_LINKAGE.json` link every original
canonical source snapshot to its pinned Git source, including a direct source
URL and a match to the canonical source inventory. The mathematical sources
already exist in the frozen published commit. `REGISTRY.json` contains the
complete 523-module project and its three claims; `SOURCE_MAP_ADDITIONS.json`
contains the 514 layout-map additions needed for the selected new/versioned
sources. The broader repository source map was not edited by this run.

The raw canonical report's literal `agent: Agent #1` identifies the upstream
checker implementation. The actual executor is recorded by the outer report
as Agent 104, specialist `runtime_scout`. Its `source_commit` is the replay
baseline `2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5`, and
`source_tree_clean` is `false` for the materialized replay workspace. Those
original fields were retained unchanged. The actual published mathematical
sources are fixed by the outer `published_source` record and every source
entry, as described above. `repository_wide_pass` is `false`; this is a
successful selected-project check rather than a completed repository census.

Key immutable evidence digests:

| Evidence | SHA256 |
| --- | --- |
| `build.json` | `f044307147ccd1541aea7b0a537ca05347bf0100f5aafa50433332a7809a5a36` |
| `canonical/verification.json` | `52992057d5f3051a6db6413ed724375e06f903ef8ea78a145ef23693f2edba30` |
| `REGISTRY.json` | `509310b61aefbef5f4330eb0e8bbbc1f4d71a1728edaeeb5f147d48eb6a603a3` |
| `source-snapshot.json` | `09e0c610ba247e3e16995cd4ed4c4eddc815735a43a5c2e04cbae56834c75035` |
| `ProjectAudit.log` | `8c59855ddc50189307e0da9d08d9b9f917ae30ec7bbf0c7e15db11f8c30b5ca6` |
| `ProjectAudit.lean` | `08db920c5f80724b9bc0b85f9f3fa2c474ac607f0b841b9803dff6672a1c53d5` |

`PUBLISH_INDEPENDENT_VERIFICATION.txt` gives the exact repository-relative
publication payload, including the execution helper and the standard-library
origin manifest required to replay the supplied entry point.
