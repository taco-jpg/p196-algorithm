# Agent #104: frozen 620 certificate instantiation

This directory records the **author implementation** of the concrete 620
certificate. The mathematical checker and bridge retain Agent #124's original
names, sources, and attribution. Generation and a successful author build are
separate from independent review.

## Inputs and provenance

`inputs/certificate_620.json` is the byte-exact previously published width-7
certificate, with SHA-256
`e6c447fa7efa26e94d1a8064a9336922d3eeb2e1e55176f8043e1cd9dbe3cea5`.
It contains 59,189 distinct ranked words and 10,002 initial words. The maximum
rank is 11; the mathematical ancestry bound supplied by the generic bridge is
12. The initial family has 10,000 width-7 words and the two shorter words
`[6,2,0,2,6]` and `[6,2,0,0,2,6]`.

`UPSTREAM_PINS.json` records the original archive paths, Git blob IDs, byte
counts, and SHA-256 digests for this certificate and the byte-exact retained
Agent #124 `upstream/gen_code.py` and `upstream/scope.py`. Archive directory names
are archival identifiers; they are not asserted to be the content hash of the
individual file. The semantic dependency pins and their module mapping are
recorded separately in `../verification/author-base/dependency-map.json`.

## Generation

Run `python3 -B generate_frozen620.py` from any directory. The adapter checks the
three input hashes, supplies the frozen rank table to the original generator's
closure callback, and invokes its original emitter. It does not search for a new
rank certificate. The original emitter output is retained in
`upstream-output-leaf256/`, including its reference final module, which is not
installed as Agent #104's final endpoint.

Only the concrete instance is renamed to namespace `Agent104.Prefix620`; shared
definitions, the checker, soundness lemmas, and all `Agent124` namespace names are
unchanged. The adapter adds provenance, explicit kernel evaluation for the small
width bound, unlimited heartbeats for the large finite checks, and the
`initialBounded` wrapper. After the measured monolithic failures described below,
the adapter partitions initial words by two free decimal digits and short words
by the first coefficient of their half word.
The generator manifest records the adapter hash and every emitted source hash.

The default layout has 256 balanced rank-tree leaves, each with at most 231 nodes,
and 255 internal nodes. The source manifest contains 510 concrete modules:

| Family | Modules | Purpose |
| --- | ---: | --- |
| `Agent104Prefix620DataNNN` | 64 | Four tree leaves per data module |
| `Agent104Prefix620DataTree` | 1 | Reassemble the exact rank tree |
| `Agent104Prefix620RowsNNN` | 256 | One kernel row check per tree leaf |
| `Agent104Prefix620RowsBranch` | 1 | Kernel checks of all 255 internal nodes |
| `Agent104Prefix620RowsAll` | 1 | Assemble `allRows : RowsClosed 7 (R ranks)` |
| `Agent104Prefix620DataCoverage` | 1 | Handwritten structural coverage of both original enumerations |
| `Agent104Prefix620DataInitialWords`, `Agent104Prefix620DataShortWords` | 2 | Literal finite-list blocks, as transparent noncomputable definitions |
| `Agent104Prefix620InitialNNN` | 101 | Kernel checks of the initial-word blocks |
| `Agent104Prefix620ShortNNN` | 78 | Kernel checks of the short-source slices |
| `Agent104Prefix620InitialCoverage`, `Agent104Prefix620ShortCoverage` | 2 | Local kernel equality of each literal block to its original enumeration slice |
| `Agent104Prefix620InitialAll`, `Agent104Prefix620ShortAll` | 2 | Assemble `initialBounded` and `short` using the structural coverage lemmas |
| `Agent104Prefix620` | 1 | Numeric target fidelity, ancestry bound 12, and all-time 196 exclusion for this target family |

The short-source domain is the generic checker's complete `symWords` family for
widths 0 through 6: 10,467 words in total. The initial partition has one two-word
short block and 100 blocks of 100 long words. Short widths 1 and 2 each have one
small block; widths 3 through 6 each have 19 slices indexed by the half word's
first coefficient. Each slice retains the original `mirror` and `symOK` filter,
including the empty slice at coefficient zero. The largest slice has 361 words.

All concrete Boolean checks use `decide +kernel`. Each local coverage equality
uses `rfl` on at most one bounded slice. The handwritten coverage helper proves
coverage of the complete original `initialWordsK` and `symWords` domains by list
membership, with no equality between two whole ten-thousand-word lists. Its
SHA-256 is `d8d672edcda4b39d14247927ee7c7eef221e1da71bee68a0bb67f233006115f5`;
the adapter verifies this pin and never edits that source. Python list generation
is not a proof premise. The `noncomputable` annotation suppresses executable code
generation for the literal lists; their transparent defining terms remain
available for kernel reduction. The parent Agent #104 explicitly delegated final
theorem assembly to this author implementation after the initial pilot.

## Author build

`build_concrete.py` uses the 13 shared dependency sources and object files after
the separate author-base build has verified and exported them to
`/tmp/agent104-prefix620-author`. It never rebuilds those dependencies. The
compiler is the pinned Lean 4.19.0 release at
`/workspace/scratch/a1d46b1077ac/agent103-runtime/toolchain/lean-4.19.0-linux/bin/lean`.
Each concrete compilation uses `-j1 -DElab.async=false --trust=0`. At most two
compiler processes run concurrently.

The intended sequence is:

```sh
python3 -B build_concrete.py --stage data --jobs 2 --label data-004
python3 -B build_concrete.py --stage finite-pilot --jobs 2 --label finite-pilot-003
python3 -B build_concrete.py --stage all --jobs 2 --label all-001
```

The original pilot checked five distributed row leaves and the complete
internal-node module successfully. The revised finite pilot checks a 100-word
initial block, representative slices from both of the largest short-source
widths, and all local initial and short coverage proofs. The final stage reuses
a concrete object only when the recorded source hash and actual object hash
both match and its dependencies remain valid. A changed imported concrete
definition invalidates dependent cached successes transitively. Its report
explicitly lists reused author objects. Independent verification uses a newly empty build
directory and does not use this reuse state.

Each `evidence/<label>/verification.json` records the actual compiler identity,
commands, dependency hashes, source/object/log hashes, exit statuses, elapsed
time, CPU time, and process maximum resident memory. These records establish the
status of that stage; no README prose substitutes for a missing successful
record. `evidence/successful-builds.json` is only the author's local reuse index.
Failed compilation sources and logs remain in the corresponding evidence
directory. Superseded generated sources are preserved under `development/`.

## Preserved development failures

The original 10,002-word initial monolith was terminated by the system with
signal 9 after 61.973 seconds, at a recorded peak of 4,022,076 KiB. The author
then explicitly terminated the concurrent short-source monolith with SIGTERM;
its runner record reports 136.036 seconds and 5,802,068 KiB. The exact termination
command and reason are recorded in
`evidence/pilot-001/short-monolith-termination.json`. Neither termination is a
logical counterexample. The corresponding source and compiler logs are retained.

The first pure-list partition data attempt had an explicit-import error:
`Agent124.CodeCert` was opened while only `Agent124PrefixK` was imported. Its
sources and logs are retained under `evidence/data-002/`. The corrected files
import `Agent124CodeCert`, and the retry has a separate evidence label.

The first partition's whole-list coverage equality used `DecidableEq`; its
initial coverage process received signal 9 at 4,038,132 KiB after 53.133 seconds.
The concurrent short coverage was explicitly stopped with SIGTERM; the source,
logs and termination record remain in `evidence/finite-pilot-001/`. Replacing
that whole-list comparison with `rfl` lowered memory, but both whole-list
comparisons reported `Stack overflow detected. Aborting.` and exited with
signal 6; those exact attempts are retained in `evidence/finite-pilot-002/`.

The final partition addresses both measured failure modes structurally, using
bounded local slice equalities and generic list-membership coverage lemmas. It
uses the canonical default compiler stack; it does not change the verifier or
wrap the compiler. Superseded flat modules are preserved with hashes and paths
in `development/retired-outputs.json`.

No generator or Python control is included as a trusted proof premise.
