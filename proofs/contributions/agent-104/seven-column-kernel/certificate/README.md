# 739 finite rank certificate: kernel-checking work record

Scope: the finite backward-prefix certificate for the 739 target. This is not a
proof that 196 never reaches any palindrome. The complete ordinary-number
application additionally uses the separately proved projection, short boundary,
and palindrome bridge.

## Trusted logical interface

`../PrefixCertificate.lean` proves that complete predecessor enumeration plus
checked rank descent bounds every genuine backward path. A rank is optional;
missing predecessor keys fail a row. A balanced search tree stores words and
ranks. Every lookup checks the entire word, and `lookup_all` proves that a hit
comes from a checked node. Neither the numeric search code, sorting, nor the
Python generator is assumed correct.

`checkRow tree pred p r` recomputes **all** `pred p` and checks that each result
has a stored smaller rank. It does not consume stored edges. `CheckedRows`
requires this check for every tree node. The generic theorem
`initial_backPath_length_le` then bounds arbitrary true predecessor paths,
provided their completeness implication is supplied.

`LongRowsBase.lean` sets `longPred width p` to the complete local inverse only
when `p.length = width`; short complete words are handled separately.
`FastRowsBase.lean` transfers the optimized four-candidate inverse checks back
to this original complete enumeration, using the proved membership equivalence.

## Generated data and obligations

Input: `../../../2026-10-15-seven-column-prefix/certificate_739.json`.
SHA-256: `8157118f606d092c208672f80a467a10d489d40f90ac7d604108dbfc857ad791`.
There are 58,501 rank nodes: 58,500 length-seven prefixes and the short word
`[7,3,9,9,3,7]`. Generated `Rank739Data00` through `Rank739Data15` and `Rank739`
implement `SevenColumn.Certificate739.ranks` and `rank`.

`generate_rank739.py` emits these modules, four exact pilot rows, and the layout
record. `generate_checks739.py` emits 256 row modules, each checking at most four
leaf blocks of at most 64 nodes plus four internal nodes. `AllRows739` assembles
all 58,501 obligations. The initial set is checked in 100 blocks of 100 indices;
`Initial739` assembles the 10,000 long targets and the one short target with
initial rank at most 38. Generation is not verification: a final successful
kernel build of each assembly is required before claiming those finite results.

## Resource controls and retained attempts

Lean version: 4.19.0. `run_lean.py` records complete compiler output, command,
timeout, address-space cap, elapsed time, and peak resident memory. It uses one
Lean worker (`-j 1`); default per-module limits are 120 seconds and 6 GiB address
space. Build outputs are reproducible infrastructure outside this source folder.

The original monolithic data build failed under a 2 GiB address-space cap.
The exact source is preserved as `Rank739-monolithic.lean.gz`, with byte counts,
hashes, and a recovery command in `monolithic-history.json`. A first split-data
attempt also failed under that cap before the explicit single-worker setting.
All failure logs are retained; they do not certify any finite row. Subsequent
successful split-data logs record the revised settings.

The finite proofs use kernel `decide` only. Neither `native_decide` nor
`Lean.ofReduceBool` is allowed. Generic soundness axiom audits report only
`propext` and `Quot.sound`; concrete finite proof audits are retained in the
corresponding successful build logs.

## Active kernel-reduction checkpoint

The four representative pilot rows and initial row batches have compiled. The
ordinary decide pilot took about 18.27 seconds; the same batch with `decide +kernel`
took about 12.51 seconds. Lean 4.19.0 implements this option by passing the proof
to the kernel (`Lean/Elab/Tactic/ElabTerm.lean`, `doKernel`); it does not use native
evaluation. Concrete generated checks now use this option. A boolean traversal
experiment (`RowBoolean`/`BooleanPilotRows739`) also passed but showed little
benefit, so the main assembly keeps the simpler direct checked-row statements.

`build_rows.py` limits execution to at most two independent single-worker compiler
processes. `generate_short_checks.py` emits the separate exact short-input cases.
These sources are WIP until their full assemblies compile and their axiom reports
pass. See per-module logs; do not infer completion from generated file counts.
