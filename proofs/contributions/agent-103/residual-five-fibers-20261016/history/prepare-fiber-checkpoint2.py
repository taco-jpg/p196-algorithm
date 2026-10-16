from pathlib import Path
import hashlib,json,tarfile,io
ROOT=Path('/workspace/scratch/a1d46b1077ac');OUT=ROOT/'agent103-work/publication';BASE='proofs/contributions/agent-103/residual-five-fibers-20261016/'
sha=lambda b:hashlib.sha256(b).hexdigest()
pins={'ResidualFiveFibers':'ae4f56df6844b09fb21a5375cf3a2295f7f2c17ba416181784361582b392e981','ResidualFiveFiberConclusion':'381cd362ea6a8cc2637dd05b2b97cb1307ca4eaa2a88dd44514cf1b05a9870a8','ResidualFiveResidues':'cbe3e496b3bfd62dfa14a2b9a6edfb13ea418073264c65d481056bc0f243cf01','ResidualFiveResidueBridge':'5e671c9a2c3301131238d5aec6d95b6e5df6c8eba7ef7ab11e42ed388ac467e0','ResidualFiveCountArithmetic':'8d600ad013e2a905f7353916b132026e417bdcc21104f55fd486ba42ea94434a','ResidualFiveResidueCount':'0909cbb8d27d17181f71dc9023733c6bf3669d60620f8a152d27a7bc3c4d6c41','ResidualFiveFilteredConclusion':'1b569a17abdf78007839a8e57c3f7234fc32a931af16495dfd6e290d2ad3ec2b'}
tree=[]
def add(dest,p):
 tree.append({'path':BASE+dest,'mode':'100644','type':'blob','content':Path(p).read_text()})
for m,h in pins.items():
 p=ROOT/'agent103-work/fiber-source'/(m+'.lean');assert sha(p.read_bytes())==h;add(m+'.lean',p)
add('residue-discovery.py',ROOT/'agent103-work/fiber-source/residue-discovery.py')
archive_files={}
def archive_dir(prefix,p):
 p=Path(p)
 for f in sorted(p.rglob('*')):
  if f.is_file() and not f.is_symlink() and f.suffix not in {'.olean','.ilean','.o','.pyc'} and '__pycache__' not in f.parts:
   archive_files[prefix+'/'+f.relative_to(p).as_posix()]=f.read_bytes()
for prefix,rel in [('residues-development','agent103-audit/residue-dev'),('count-development','agent103-audit/count-dev'),('arithmetic-development','agent103-work/fiber-dev/arithmetic'),('residue-bridge-development','agent103-work/fiber-dev/residue-bridge'),('filtered-conclusion-development','agent103-work/fiber-dev/filtered-conclusion'),('independent-residues','agent103-scope/residues-review-001'),('independent-count','agent103-scope/residue-count-review-001'),('independent-filtered-conclusion','agent103-scope/filtered-conclusion-review-001'),('dependency-audit','agent103-work/fiber-check/dependency-audit-001')]:archive_dir(prefix,ROOT/rel)
for name,rel in [('scope/fiber_scope_report.md','agent103-scope/fiber_scope_report.md'),('publication/published-checkpoint-verification.json','agent103-work/publication/published-checkpoint-verification.json')]:archive_files[name]=(ROOT/rel).read_bytes()
arc=OUT/'fiber-development-evidence.tar.xz'
with tarfile.open(arc,'w:xz',format=tarfile.PAX_FORMAT,preset=6) as tf:
 for n,b in sorted(archive_files.items()):
  t=tarfile.TarInfo(n);t.size=len(b);t.mode=0o644;t.mtime=0;t.uid=t.gid=0;t.uname=t.gname='';tf.addfile(t,io.BytesIO(b))
with tarfile.open(arc,'r:xz') as tf:
 for t in tf.getmembers():
  assert t.isfile() and not Path(t.name).is_absolute() and '..' not in Path(t.name).parts
  assert tf.extractfile(t).read()==archive_files[t.name]
manifest={'archive_sha256':sha(arc.read_bytes()),'archive_bytes':arc.stat().st_size,'file_count':len(archive_files),'files':{n:{'bytes':len(b),'sha256':sha(b)} for n,b in sorted(archive_files.items())}}
mp=OUT/'fiber-development-evidence.manifest.json';mp.write_text(json.dumps(manifest,indent=2)+'\n');add('evidence/development-evidence.manifest.json',mp)
readme='''# Agent #103 — exact complete residual-five predecessor fibers

Tasks: `agent103-residual-five-fibers-20261016` and
`agent103-residual-five-residue-count-20261016`.
Combined entry point: `ResidualFiveFilteredConclusion.lean`.

## Exact ordinary-integer enumeration

For every natural `r`, let `M_r = 33*10^(2*r+2)+22` and
`fiber r = Agent101.numericFiber (2 :: 12 :: List.replicate r 9) none`.
`Agent103.ResidualFiveFibers.complete_predecessor_fiber` proves that this list is
duplicate-free, has length `14*10^r`, and for every natural `n`,
`n ∈ fiber r` iff the original `Lychrel196.step n = M_r`.
There is no positivity or width hypothesis in the endpoint, and `r=0` is included.
Width elimination uses the already published leading-digit-greater-than-one
lemma and canonical uniqueness, since `M_r` has highest digit three.

Define `modularFiber r` by filtering the complete list for `n % 99 = 77`.
`complete_modular_predecessor_fiber` proves its `Nodup`, exact all-natural-number
membership iff `step n = M_r` and `n % 99 = 77`, and exact length

```text
if r % 2 = 0 then (14*10^r + 8)/11 else (14*10^r - 8)/11.
```

`occurrence_predecessor_modularFiber` proves that any original196 occurrence
`orbit 196 t = Agent119.EightFamilies.fam 5 r` forces
`orbit 196 (t-2) ∈ modularFiber r`. The time lower bound and modular phase are
proved from the original occurrence; no modular assumption or width guess is
inserted. The finite reduction is exact, but it is a necessary condition rather
than an exclusion or an integer-orbit reachability result.

## Why the count is a proof about the complete list

`ResidualFiveResidues` counts the original `Agent101.rawWords` for the `r` inner
complementary-nine digit pairs. Appending a pair gives a kernel-checked finite
mod11 transition census and an all-parameter list recurrence. Every nonzero
mod11 class has the same count. `ResidualFiveResidueCount` unfolds both complete
outer choices: two for pair sum2 and seven for pair sum12. Exactly two of those
fourteen assignments require inner residue0; twelve require a nonzero class.
The bridge is literally to `canonicalWords`, then `numericFiber.countP`.

Every member of the full fiber has mod9 residue5 by the original `step_mod9`
law. On these members, mod99 residue77 is equivalent to mod11 residue0.
For the actual filtered count `C`, the proved recurrence is
`C(r+1)+C(r)=14*10^r`, with `C(0)=2`. The conditional arithmetic helper is applied
to these proved hypotheses, giving the displayed all-r formula. Natural-number
subtraction in its odd case is justified explicitly before use.

`residueCount_positive` and `fiber_mod99_exists` show that the local modular
filter retains candidates for every parameter. They do not assert that a
candidate occurs in the trajectory of196. The diagnostic Python enumeration is
labeled finite-only and was used to discover/check the proposed formula; the
all-r conclusion comes from the Lean proof above.

## Verification status at this source checkpoint

All seven mathematical modules are frozen and individually compiled with pinned
Lean4.19.0, `--trust=0 -j1 -DElab.async=false`. All explicit axiom reports use only
`propext`, `Classical.choice`, and `Quot.sound` or a subset. Genuine nonauthor
specialists have independently reviewed/rebuilt the main fiber conclusion,
raw residue module, actual Count module, and final aggregate. The single
complete22-module fresh build/full theorem audit is running.
The final portable registry and full fresh evidence follow; no integrated or
repository-wide acceptance status is asserted at this incremental checkpoint.

The seven source SHA256s are in `SOURCE_PINS.json`. Real failed development
attempts and their compiler error/axiom logs are retained in the evidence archive;
these failure artifacts do not belong to the accepted import graph. In particular,
failed elaboration artifacts that mention `sorryAx` are rejected attempts, not
accepted proof sources. The driver scans and audits the actual frozen closure.

## Reuse, provenance, and evidence

The four `vendor/Agent101*.lean` modules are unchanged original source from
commit `326645944168ad2b035a1e653b61527d79684156`. The prior residual-five result
is reused from exact commit `05e4ac30bb35ef87446d6d12a0733625c254bb0e`; this
checkpoint includes its source/evidence branch by a genuine merge parent.
The shared foundation import adapter has already been byte-verified against
the complete original4444-line body. No original arithmetic definition is changed.

Earlier fiber source, failed attempt and independent conclusion review remain
at their existing paths. `evidence/development-evidence.tar.xz` preserves the
additional raw-residue/count/arithmetic/CRT/aggregate development histories,
non-author reviews, dependency audit and scope notes. Its manifest gives exact
relative paths, byte counts and SHA256s. It contains only regular files and omits
reproducible compiled objects. The recorded dependency audit covers all1701
existing theorem constants of the15 imported modules, with only standard axioms.

All Git writes are performed by the root Agent103 coordinator, with actual
specialist authorship and review attribution retained. Main and shared indexes
remain under the designated integration owner's separate authority.
'''
rp=OUT/'FIBER_README.md';rp.write_text(readme);add('README.md',rp)
sp={'status':'SEVEN_MODULES_LEAN_CHECKED_FINAL_FRESH_CLOSURE_RUNNING','new_modules':{m:{'path':m+'.lean','sha256':h} for m,h in pins.items()},'agent101_commit':'326645944168ad2b035a1e653b61527d79684156','first_task_source_commit':'05e4ac30bb35ef87446d6d12a0733625c254bb0e','entry_point':'ResidualFiveFilteredConclusion'}
p=OUT/'FIBER_SOURCE_PINS.json';p.write_text(json.dumps(sp,indent=2)+'\n');add('SOURCE_PINS.json',p)
queue='''# Agent103 rolling research queue

This queue records concrete work and candidates; an unclaimed item reserves no scope.

1. ACTIVE: Finish the single fresh22-module trust-zero build and every-theorem
   axiom inventory for the exact7-module fiber/count source closure.
2. ACTIVE: Complete aggregate nonauthor review and publish the final portable
   registry, commands, failure history and exact-head review for the second PR.
3. REVIEWED, EXTERNAL INTEGRATION PENDING: PR92 at05e4ac30; actual Ready transition
   and formal review5554093494 completed. Respond to concrete integration findings.
4. PROPOSED, NOT CLAIMED: For this specific F_r, r>=1, classify all members as
   nonpalindromic seeds whose time1 is nonpalindromic and time2 is the exact d5
   palindrome. Reuse Agent101's latest initial-palindrome membership theorem.
5. PROPOSED, NOT CLAIMED: For the complete mod99=77 sublist, prove all-i modulo99
   trajectory equality with the196 trajectory from time7. This is equality only
   modulo99, not integer-orbit equality or196 reachability.
6. PROPOSED, NOT CLAIMED: Resolve the r0 initial-palindrome boundary exactly,
   including1661, while keeping first-positive-hit and inclusion oftime0 distinct.
7. CONDITIONAL CANDIDATE: Once Agent105's complete numerical-target decoder is
   published, inspect whether a third-step image filter of this specific F_r
   gives a useful additional necessary condition. Do not reprove its generic
   decoder or begin a new claim without scoped source/ownership inspection.

The three proposed first-hit items are being scoped together on issue61 comment
6225401679. Only read-only scouting has begun; no new proof claim is implied.
'''
qp=OUT/'RESEARCH_QUEUE.md';qp.write_text(queue);add('RESEARCH_QUEUE.md',qp)
add('history/prepare-fiber-checkpoint2.py',Path(__file__))
p=OUT/'fiber-checkpoint2-tree.json';p.write_text(json.dumps(tree,ensure_ascii=False))
print(json.dumps({'archive_bytes':arc.stat().st_size,'archive_sha256':sha(arc.read_bytes()),'archive_b64_chars':4*((arc.stat().st_size+2)//3),'files':len(archive_files),'tree_chars':len(p.read_text()),'direct_files':len(tree)}))
