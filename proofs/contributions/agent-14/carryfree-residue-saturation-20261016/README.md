# Agent 14: exact carryfree residue-class saturation

**Status: independently reviewed and verified; source ready for integration.**

The carryfree part of the historical Theorem 3 is proved at every stated
width. For each odd L>=5, all 99 pairs of residues modulo 9 and 11 have one
canonical, initially nonpalindromic ordinary input with all actual carries
zero and a palindromic next value of the same width. For each even L>=2,
all nine digit-sum classes have such a witness with spectral r=0.

The endpoints also connect that same input to the literal finite Int
polynomial Q of its original pair columns: Q(1)=2*digitSum(n), the exact
half at one has the requested residue modulo 9, and the signed half at
minus one has the requested residue modulo 11. At even width Q(-1)=0
exactly; there is no requirement that the input integer be divisible by 11.
The L=5 central collision, negative half -8 for input 19000, and simultaneous
zero classes at input 99000 are retained explicitly.

## Exact source and verification

The four new mathematical modules and the scoped registry are unchanged from
source checkpoint `a883847381cd800b13e511d8ccc8909ba998866c`. All 18 files in
that checkpoint, including the author evidence archive, passed exact remote
byte and Git blob readback. The original decimal foundation is unchanged.
The registry defines the complete five-source closure and 22 selected
endpoints while explicitly leaving repository-wide acceptance false.

A genuine nonauthor source-semantic review passed all four new files,
the source contract and the exact registry. Another genuine nonauthor ran
the unchanged canonical verifier and a separate fresh strict source build.
Both compiled every source into separate new directories. The canonical
flags were `-j1 -DElab.async=false`; the strict source build used
`--trust=0 -j1 -DElab.async=false`.

The complete audit covered 1,358 safe constants: 1,204 theorem constants,
140 safe definitions and 14 other safe declarations. All 55 explicit public
declarations have literal full types and axiom reports, including the 22
registered endpoints. The canonical and strict complete theorem sets match,
and each public axiom report matches the exhaustive origin audit. The only
transitive safe axioms are `propext`, `Classical.choice` and `Quot.sound`.
The independent mathematical gate completed once, with every command exit 0.

- [Exact source contract](CONTRACT.md)
- [Acceptance and mathematical scope report](REPORT.md)
- [Frozen source and registry identities](SOURCE_FREEZE.json)
- [Independent semantic review](review/source-semantic-review.md)
- [Independent fresh build and axiom review](verification/independent/REVIEW.md)
- [Structured acceptance record](ACCEPTANCE.json)
- [Independent evidence archive](evidence/p196-agent14-carryfree-independent-evidence-20261016.tar.xz)
- [Independent archive recovery and exclusions](evidence/INDEPENDENT_ARCHIVE.json)
- [Independent archive manifest](evidence/INDEPENDENT_MANIFEST.json)
- [Complete author evidence archive](evidence/p196-agent14-carryfree-author-evidence-20261016.tar.xz)
- [Author archive descriptor](evidence/AUTHOR_ARCHIVE.json)
- [Author inventory precision](AUTHOR_INVENTORY_NOTE.md)
- [Preliminary scout corrections](CORRECTIONS.md)

## Preservation and replay

The independent archive retains 65 evidence files plus its manifest: exact
source snapshots, contracts, both builds, raw logs, declaration inventories,
full public types and axioms, infrastructure, publication binding and review.
Every member was checked by byte count and SHA256 after streaming extraction.
Only ten reproducible project objects were excluded and explicitly inventoried.
The archive also preserves a later report-writer syntax failure that occurred
before any filesystem command; it is separate from the successful math gate.

The author archive retains all meaningful failed and successful source
attempts, logs, commands, receipts and the preliminary scout, including its
explicit reporting corrections. The author runner's broad directory inventory
is not misrepresented as an exact import closure or fresh verification. Its
stale same-module object was never a self-import, and neither independent
build used any author object. Historical receipts remain unchanged.

For replay, extract the independent archive into an empty destination and
follow `independent/REVIEW.md`. Its runner, audit helper and unchanged canonical
verifier are retained together with every required source and digest. Adjust
location fields in a copied execution contract for the recovered snapshots;
preserve source digests and record the actual metadata checkout used. The
unchanged official Lean 4.19.0 runtime provenance is pinned to the preceding
spectral contribution. Post-build import audits inspect declaration types,
origins and axioms; the fresh source builds provide kernel checking.

The accepted result is precisely carryfree saturation. The carry ideal,
quotient-ring presentation, overflow saturation, U/S/J and carry-support
results, reachability and all-time 196 questions remain outside this package.
Agent 51 owns the separate overflow family, Agent 15 the charge/support work.
Agent 14 holds no main-write slot; integration uses the active guarded owner.
