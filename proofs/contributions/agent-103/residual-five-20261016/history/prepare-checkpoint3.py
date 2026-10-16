from pathlib import Path
import hashlib,json,tarfile,io
ROOT=Path('/workspace/scratch/a1d46b1077ac')
PUB=ROOT/'agent103-work/publication'
BASE='proofs/contributions/agent-103/residual-five-20261016/'
sha=lambda b:hashlib.sha256(b).hexdigest()
README='''# Agent #103 — residual digit-five necessary conditions

Task: `agent103-residual-five-20261016`. Entry point: `ResidualFiveConclusion.lean`.

## Result and mathematical scope

`Agent103.ResidualFive.occurrence_necessary_conditions` proves that an occurrence
`Lychrel196.orbit 196 t = 55*(10^(2*r+2)+1)` forces all of the following:

- `105 <= t`, `1 <= r`, and `t % 6 = 3`;
- canonical widths `2*r+4` at both preceding times;
- zero terminal carry on both final additions;
- exact intermediate integer `33*10^(2*r+2)+22`;
- complete earlier pair-sum word `[2,12] ++ replicate (2*r) 9 ++ [12,2]`;
- internal carry one exactly at columns `2` through `2*r+3`.

The unfolded endpoint writes the original integer family explicitly. It assumes
no first-positive-hit condition and no unverified certificate. These are necessary
conditions for an occurrence, not an exclusion of the residual family.

`Agent103.ResidualFiveWitness.residual_five_witness` proves that the positive seed
`71647625487907287180977453773517` first reaches a palindrome at time six,
namely `55*(10^32+1)`. Its entire modulo-99 trajectory at time `i` agrees with the
196 trajectory at time `3+i`. Thus that shifted modular trajectory alone is
insufficient to exclude this target. This seed is not asserted to lie on the
integer orbit of 196.

`ResidualFiveShape.lean` formalizes the written inverse structure in section 4 of
the preserved `p196_all_palindromes_and_eight_families.md`. Its local shape theorem
also includes `r=0`. The 196 occurrence theorem itself excludes `r=0` using the
original early-orbit result. Uniqueness refers to the pair-sum word and the
intermediate integer; individual source integers need not be unique.

## Verification

All four frozen modules passed an independent semantic review and rebuild.
The complete eleven-module dependency closure was then rebuilt into a new empty
project-object directory with pinned Lean 4.19.0, commit `6caaee842e94`, using
`--trust=0 -j1 -DElab.async=false`. Every build command exited zero.
The final audit individually queried `#print axioms` for all 1,532 theorem
constants of those modules: 1,380 dependency constants and 152 new-module constants.
All reported dependencies are among `propext`, `Classical.choice`, and `Quot.sound`.
This is a scoped closure verification, not a repository-wide build claim.

There are 63 source theorem declarations in the four new modules, including
private lemmas. A separate independent compilation produced 161 new-module
constants; the nine-count difference consists entirely of generated `_proof_N`
helpers. Source hashes and every non-generated theorem name agree. Both genuine
logs and the exact comparison are retained; theorem counts are not novelty counts.

Actual cross-author reviewers were the real `scope_scan` and `source_audit`
specialists in this Agent #103 session; `runtime` authored no mathematical source
and performed the full fresh closure build/audit. The GitHub publishing identity
is shared. This is not represented as approval by another GitHub account.

## Reproduction and preserved evidence

See [REPRODUCE.md](REPRODUCE.md) for both the portable historical-source replay
and the current-tree project registry. `check.py` and `SOURCES.json` pin original
commit/path/Git-blob/SHA256 identities. `BUILD_REGISTRY.json` consumes byte-identical
current-tree files and exact vendored dependencies without requiring historical
commits. The unchanged project verifier passed its `--check-only` gate on that
published layout. The stronger trust-zero full build is recorded separately.

Readable summaries are under `evidence/clean-summary.json` and
`evidence/publication-layout-check.json`. Complete clean-build sources, commands,
logs, per-theorem axiom records, the source-count comparison, registry staging,
and runtime recovery history are in `evidence/complete-replay-evidence.tar.xz`.
Its file-by-file inventory is `evidence/complete-replay-evidence.manifest.json`.
Earlier individual reviews and real failed attempts remain at their original
`evidence/` and `attempts/` paths and in commit history. Compiled objects and the
reproducible Lean toolchain are omitted from the archive; their measured hashes
remain in the verification reports.

Agent #119's eight-family theorem explicitly excludes `d=5` and is reused unchanged.
Agent #423's temporal module is also unchanged. The sole import adapter replaces
`Lychrel196Research.lean` with `import LychrelDigitSums`: the entire original
4,444-line foundation body was verified byte-identical inside the continuation
foundation before compilation. No arithmetic definition has been changed.

The status of 196 remains open in this contribution. Main integration is owned
separately and is not performed by this branch.
'''
(PUB/'README.md').write_text(README)
REPRO='''# Reproduce the Agent #103 residual-five contribution

## Exact historical-source replay with full trust-zero audit

Use the official Linux Lean 4.19.0 release (compiler commit `6caaee842e94`).
The measured compiler SHA256 in this execution was
`92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023`.
The following commands assume a checkout of this contribution and a Lean path
chosen by the caller. `--evidence` must name a directory that does not yet exist.

```sh
git fetch origin 913441a936a437e5f4b82d03d7e7fae32da877af
git fetch origin 6fae6e659e5c08c59666588c71a4ed06760de85e
python3 proofs/contributions/agent-103/residual-five-20261016/check.py \
  --repo . --lean /absolute/path/to/lean-4.19.0-linux/bin/lean \
  --evidence /absolute/path/to/new-evidence-directory
```

The driver reads dependencies from immutable Git objects, verifies Git blob and
SHA256 identities, checks the one exact foundation import forwarder, scans the
compiled source, computes the dependency order, and creates an empty project
snapshot. It builds all eleven modules with `--trust=0 -j1 -DElab.async=false`.
It inventories every theorem constant by its module of origin, executes a literal
`#print axioms` for each, and rejects missing reports or nonstandard axioms.
No prebuilt project `.olean` is accepted. The driver itself does not download
source, invoke an external solver, or modify Lean.

The original successful run used the working manifest with source files under
`source/`; the publication manifest only normalizes those four paths to the
package root and adds current-tree recovery documentation. Source bytes, dependency
pins, compiler arguments, and driver bytes are identical. That specific difference
is checked in `evidence/publication-layout-check.json`; original manifests and full
commands remain inside the evidence archive.

## Current-tree registry without historical Git objects

```sh
python3 proofs/verify_project__214bf7673efe116b.py \
  --registry proofs/contributions/agent-103/residual-five-20261016/BUILD_REGISTRY.json \
  --project agent103-residual-five --check-only \
  --lean /absolute/path/to/lean-4.19.0-linux/bin/lean \
  --output /absolute/path/to/new-registry-evidence-directory
```

The source identities and staged check-only result are retained in
`evidence/registry-source-evidence.json` and the staged verification report.
Remove `--check-only` for a full project-verifier replay. Its standard invocation does not add
`--trust=0`; use the portable driver above to reproduce the recorded stricter run.
No shared accepted-build index is edited by this contribution. The registry lists
`ResidualFiveConclusion` as its root and includes all eleven module sources.

## Inspect evidence without running code

`evidence/complete-replay-evidence.manifest.json` gives a SHA256 and byte count for
every archived regular file. The archive contains relative paths only, no symbolic
links, executables, compiled project objects, or toolchain binaries. Extract into
a new empty directory and compare the files against that manifest. The original
clean `verification.json` and `FILES.json` contain detailed commands, source/object
hashes, individual theorem records, and the complete axiom union. Full ordinary
compiler stdout is retained, including genuine failures in development histories.

The separate generated-helper comparison explains why independent compilation
instances may inventory 161 versus 152 new-module theorem constants while all 63
source declarations and all non-generated names stay identical. Either number is
an execution fact about that particular compiled environment, not a mathematical
claim about 161 or 152 distinct results.
'''
(PUB/'REPRODUCE.md').write_text(REPRO)
files={}
def add_file(arc,p):
 p=Path(p)
 if p.suffix in {'.olean','.ilean','.o','.pyc'}:return
 b=p.read_bytes();files[arc]=b

def add_dir(prefix,p):
 p=Path(p)
 for f in sorted(p.rglob('*')):
  if f.is_file() and not f.is_symlink() and '__pycache__' not in f.parts:add_file(prefix+'/'+f.relative_to(p).as_posix(),f)
add_dir('clean',ROOT/'agent103-work/verification-clean-001')
add_dir('registry-check-only',ROOT/'agent103-work/registry-check-only-001')
for n in ['SOURCES.json','SOURCES.publish.json','theorem-count-comparison.json','publication-layout-check.json','registry-source-evidence.json']:
 add_file('publication/'+n,ROOT/'agent103-work'/n)
for n in ['README.md','Smoke.lean','verify_runtime.py','prepare_temporal_baseline.py','run_temporal_baseline.py','prepare_agent119_baseline.py','run_agent119_baseline.py','audit_agent103_baseline.py','build_exact_modules.py','registry-stage-preparation.json']:
 add_file('runtime-history/'+n,ROOT/'agent103-runtime'/n)
add_dir('runtime-history/logs',ROOT/'agent103-runtime/logs')
add_dir('runtime-history/controls',ROOT/'agent103-runtime/controls')
add_file('scope-history/scope_report.md',ROOT/'agent103-scope/scope_report.md')
add_file('independent-first-task-evidence-review.json',ROOT/'agent103-work/fiber-check/first-task-evidence-review.json')
manifest={p:{'bytes':len(b),'sha256':sha(b)} for p,b in sorted(files.items())}
archive=PUB/'complete-replay-evidence.tar.xz'
with tarfile.open(archive,'w:xz',format=tarfile.PAX_FORMAT,preset=6) as tf:
 for name,b in sorted(files.items()):
  t=tarfile.TarInfo(name);t.size=len(b);t.mode=0o644;t.mtime=0;t.uid=t.gid=0;t.uname=t.gname=''
  tf.addfile(t,io.BytesIO(b))
with tarfile.open(archive,'r:xz') as tf:
 members=tf.getmembers();assert len(members)==len(files)
 for t in members:
  assert t.isfile() and not Path(t.name).is_absolute() and '..' not in Path(t.name).parts
  assert tf.extractfile(t).read()==files[t.name]
(PUB/'complete-replay-evidence.manifest.json').write_text(json.dumps({'archive_sha256':sha(archive.read_bytes()),'archive_bytes':archive.stat().st_size,'file_count':len(files),'files':manifest},indent=2)+'\n')
full=json.loads((ROOT/'agent103-work/verification-clean-001/verification.json').read_text())
summary={k:v for k,v in full.items() if k not in {'theorems'}}
summary['full_evidence']='complete-replay-evidence.tar.xz:clean/verification.json'
summary['source_theorem_declarations']=63
summary['independent_compilation_count_note']='161 versus 152 new-module constants differs only by 9 generated _proof_N helpers. See complete archive publication/theorem-count-comparison.json.'
(PUB/'clean-summary.json').write_text(json.dumps(summary,indent=2)+'\n')
direct={'README.md':PUB/'README.md','REPRODUCE.md':PUB/'REPRODUCE.md','check.py':ROOT/'agent103-work/check.py','SOURCES.json':ROOT/'agent103-work/SOURCES.publish.json','BUILD_REGISTRY.json':ROOT/'agent103-work/BUILD_REGISTRY.json','evidence/clean-summary.json':PUB/'clean-summary.json','evidence/publication-layout-check.json':ROOT/'agent103-work/publication-layout-check.json','evidence/registry-source-evidence.json':ROOT/'agent103-work/registry-source-evidence.json','evidence/complete-replay-evidence.manifest.json':PUB/'complete-replay-evidence.manifest.json','history/prepare-checkpoint3.py':Path(__file__)}
tree=[{'path':BASE+p,'mode':'100644','type':'blob','content':f.read_text()} for p,f in direct.items()]
(PUB/'checkpoint3-tree.json').write_text(json.dumps(tree,ensure_ascii=False))
print(json.dumps({'archive_bytes':archive.stat().st_size,'archive_sha256':sha(archive.read_bytes()),'files':len(files),'tree_chars':len((PUB/'checkpoint3-tree.json').read_text()),'direct_files':len(tree)}))
