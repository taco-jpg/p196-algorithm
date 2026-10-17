from pathlib import Path,PurePosixPath
import json,hashlib,tarfile,shutil,io,gzip
BASE=Path('/dev/shm/p196-agent15-43cf6e114472')
PKG=BASE/'support-repo/proofs/contributions/agent-15/spectral-carry-support-43cf6e114472'
def sha(b):return hashlib.sha256(b).hexdigest()
def writej(p,v):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,indent=2,ensure_ascii=False)+'\n')
copies=[]
def cp(src,dest):
 dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dest)
 assert src.read_bytes()==dest.read_bytes()
 copies.append({'source':str(src),'published_path':str(dest.relative_to(PKG)),'bytes':dest.stat().st_size,'sha256':sha(dest.read_bytes())})
ad=PKG/'development/author';out=PKG/'evidence/author'
archive=ad/'delivery/author-evidence.tar.gz';manifest=json.loads((ad/'delivery/author-evidence.manifest.json').read_text())
assert sha(archive.read_bytes())==manifest['archive']['sha256']=='d98b44f9c8a8c8faa5d9401fb6767e1587e51a22ea23d795f1a12364803e8dcd'
with tarfile.open(archive,'r:gz') as tf:
 members=tf.getmembers();assert len(members)==manifest['archive']['member_count']
 manifest_members={x['archive_member']:x for x in manifest['members']}
 for m in members:
  p=PurePosixPath(m.name);assert m.isfile() and not p.is_absolute() and '..' not in p.parts
  rec=manifest_members[m.name];data=tf.extractfile(m).read()
  assert len(data)==rec['bytes'] and sha(data)==rec['sha256'],m.name
for n in ['author-evidence.tar.gz','author-evidence.manifest.json','DELIVERY_REPORT.md']:
 cp(ad/'delivery'/n,out/n)
for src,dest in [
 ('AUTHOR_REPORT.md','AUTHOR_REPORT.md'),('PREPARATION.md','PREPARATION.md'),
 ('checker/CHECKER_REPORT.md','CHECKER_REPORT.md'),
 ('checker/canonical-run-0001/verification.json','verification.json'),
 ('checker/canonical-run-0001/public-and-critical-axioms.json','public-and-critical-axioms.json'),
 ('checker/canonical-run-0001/source-pins.json','source-pins.json'),
 ('checker/canonical-run-0001/import-closure.json','import-closure.json'),
 ('checker/canonical-run-0001/exports.json','exports.json'),
 ('checker/canonical-run-0001/logs/PublicAudit.stdout','PublicAudit.stdout'),
 ('checker/canonical-run-0001/logs/PublicAudit.stderr','PublicAudit.stderr')]:
 cp(ad/src,out/dest)
sd=BASE/'support-semantic-review';so=PKG/'evidence/semantic';so.mkdir(parents=True,exist_ok=True)
files=[p for p in sorted(sd.rglob('*')) if p.is_file()]
members=[]
archive=so/'semantic-review-5d02e88f.tar.gz'
with archive.open('wb') as raw:
 with gzip.GzipFile(filename='',mode='wb',fileobj=raw,mtime=0) as gz:
  with tarfile.open(fileobj=gz,mode='w',format=tarfile.PAX_FORMAT) as tf:
   for f in files:
    assert not f.is_symlink()
    rel=f.relative_to(sd);data=f.read_bytes();name='support-semantic-review/'+str(rel)
    ti=tarfile.TarInfo(name);ti.size=len(data);ti.mode=0o644;ti.mtime=0
    tf.addfile(ti,io.BytesIO(data));members.append({'path':name,'bytes':len(data),'sha256':sha(data)})
with tarfile.open(archive,'r:gz') as tf:
 actual=tf.getmembers();assert len(actual)==len(members)
 for m,r in zip(actual,members):
  data=tf.extractfile(m).read();assert m.name==r['path'] and len(data)==r['bytes'] and sha(data)==r['sha256']
writej(so/'semantic-archive-manifest.json',{'source_commit':'5d02e88f13f59f6fcd09cf75d8c7f188c6645727','archive':{'path':archive.name,'bytes':archive.stat().st_size,'sha256':sha(archive.read_bytes()),'members':len(members)},'files':members,'all_originals_retained':True,'all_archive_members_rehashed':True})
for n in ['FINAL_SEMANTIC_REVIEW.md','FORMAL_COMMENT.md','REVIEW_MANIFEST.json','CONTRACT_REVIEW_001.md','SOURCE_REVIEW_001.md']:
 cp(sd/n,so/n)
nextscout=BASE/'next-claim-scout'
for n in ['NEXT_CLAIM_SCOUT.md','evidence.json']:
 cp(nextscout/n,PKG/'research'/n)
cp(Path(__file__),PKG/'development/root/package-support-initial-evidence.py')
writej(PKG/'evidence/initial-copy-manifest.json',{'scope':'Author and semantic frozen evidence, plus preclaim source scout; runtime review packaged separately.','copies':copies})
print(json.dumps({'author_archive_bytes':(out/'author-evidence.tar.gz').stat().st_size,'semantic_archive_bytes':archive.stat().st_size,'semantic_archive_sha256':sha(archive.read_bytes()),'semantic_archive_members':len(members),'readable_copies':len(copies)}))
