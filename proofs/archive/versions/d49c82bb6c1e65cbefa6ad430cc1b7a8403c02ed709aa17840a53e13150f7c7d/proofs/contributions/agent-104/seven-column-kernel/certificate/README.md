# 739 finite rank certificate: kernel-checking work record

Scope: the finite backward-prefix certificate for the 739 target. This is not a
proof that 196 never reaches any palindrome. The complete ordinary-number
application additionally uses the separately proved projection, short boundary,
and palindrome bridge.

Current status: all four concrete assemblies (`AllRows739`, `Initial739`,
`Short739`, `Conclusion739`) passed their first Lean compilation at source
`957efa326b4b980391046598a0143cb7a7060242`. The final ordinary-number ancestry
and orbit-exclusion theorems have no remaining finite-certificate hypotheses.
Their transitive axioms are exactly `propext`, `Classical.choice`, and
`Quot.sound`. An independent fresh rebuild of the full dependency chain is
running; the earlier WIP and resource-failure records below are historical.

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
all 58,501 obligations. The initial set is checked in 10 blocks of 1,000 indices;
`Initial739` assembles the 10,000 long targets and the one short target with
initial rank at most 38. Generation is not verification: the successful kernel
assembly logs, rather than generated source counts, establish completion of
this first build.

## Resource controls and retained attempts

Lean version: 4.19.0. `run_lean.py` records complete compiler output, command,
timeout, address-space cap, elapsed time, and peak resident memory. It uses one
Lean worker (`-j 1`); default per-module limits were initially 120 seconds and 6 GiB address
space. Build outputs are reproducible infrastructure outside this source folder.

The original monolithic data build failed under a 2 GiB address-space cap.
The exact source is preserved as `Rank739-monolithic.lean.gz`, with byte counts,
hashes, and a recovery command in `monolithic-history.json`. A first split-data
attempt also failed under that cap before the explicit single-worker setting.
All failure logs are retained; they do not certify any finite row. Subsequent
successful split-data logs record the revised settings.

The finite proofs use kernel `decide` only. Neither `native_decide` nor
`Lean.ofReduceBool` is allowed. Generic soundness axiom audits are contained in
`propext`, `Classical.choice`, and `Quot.sound`; concrete finite proof audits are retained in the
corresponding successful build logs.

## Earlier kernel-reduction checkpoint

The four representative pilot rows and initial row batches have compiled. The
ordinary decide pilot took about 18.27 seconds; the same batch with `decide +kernel`
took about 12.51 seconds. Lean 4.19.0 implements this option by passing the proof
to the kernel (`Lean/Elab/Tactic/ElabTerm.lean`, `doKernel`); it does not use native
evaluation. Concrete generated checks now use this option. A boolean traversal
experiment (`RowBoolean`/`BooleanPilotRows739`) also passed but showed little
benefit, so the main assembly keeps the simpler direct checked-row statements.

`build_rows.py` limits execution to at most two independent single-worker compiler
processes. `generate_short_checks.py` emits the separate exact short-input cases.
At that earlier checkpoint the full assemblies were WIP. Their successful
first assembly logs are now retained as `AllRows739-aggregate01.log`,
`Initial739-kernel01.log`, `Short739-kernel01.log`, and
`Conclusion739-aggregate01.log`. The independent fresh build remains a separate
verification gate.

## Memory refinement

Dense unsplit row blocks 57, 58, 85 and 97 exhausted their process or host memory
budget. Their sources and logs are retained. `split_row_batches.py` replaces only
their proof decomposition: the original `checked_leaf` statements remain identical,
but their components are established in modules of at most 14 concrete row checks.
The wrapper assembles those checked lemmas against the same original tree.

The runner now defaults to a 3.5 GiB address-space cap and shares two file-lock
slots across row, short-boundary and initial-family workers. This avoids accidental
extra concurrent compiler processes when multiple build queues are active.
