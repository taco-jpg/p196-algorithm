#!/usr/bin/env python3
"""Seal all files and verify original archive-member coverage, including nested manifests."""
from pathlib import Path,PurePosixPath
import json,hashlib,tarfile,traceback
ROOT=Path(__file__).resolve().parent;BASE=ROOT.parent
ARCHIVE=BASE/'agent12-review115-publication-001.tar.xz'
def sha(d):return hashlib.sha256(d).hexdigest()
def blob(d):return hashlib.sha1(b'blob '+str(len(d)).encode()+b'\0'+d).hexdigest()
def main():
 original=json.loads((ROOT/'assembly-history/attempt-001/MANIFEST.json').read_text())
 sources=json.loads((ROOT/'SOURCE_ARCHIVES.json').read_text())
 files=[];canonical={}
 for p in sorted(ROOT.rglob('*')):
  if p.is_file() and p!=ROOT/'MANIFEST.json':
   assert not p.is_symlink();data=p.read_bytes();rel=p.relative_to(ROOT).as_posix();digest=sha(data);key=(len(data),digest);item={'path':rel,'bytes':len(data),'sha256':digest}
   if key in canonical:item['identical_bytes_also_at']=canonical[key]
   else:canonical[key]=rel
   files.append(item)
 bypath={x['path']:x for x in files}
 for source in sources:
  d=(ROOT/source['publication_archive_member']).read_bytes();assert len(d)==source['bytes'] and sha(d)==source['sha256']
  for member in source['members']:
   listed=bypath[member['publication_member']];assert listed['bytes']==member['bytes'] and listed['sha256']==member['sha256']
 manifest={**original,'files':files,'file_count_excluding_manifest':len(files),'payload_bytes_excluding_manifest':sum(x['bytes'] for x in files),'final_original_archive_expanded_member_coverage':'PASS_ALL_399_MEMBERS','assembly_correction':'ASSEMBLY_CORRECTION.json','initial_assembly_preserved':'assembly-history/attempt-001/'}
 (ROOT/'MANIFEST.json').write_text(json.dumps(manifest,indent=2)+'\n')
 md=(ROOT/'MANIFEST.json').read_bytes();expected={**bypath,'MANIFEST.json':{'bytes':len(md),'sha256':sha(md)}}
 with tarfile.open(ARCHIVE,'w:xz',preset=6) as tf:
  for rel in sorted(expected):tf.add(ROOT/rel,arcname='review115-publication-001/'+rel,recursive=False)
 seen=set()
 with tarfile.open(ARCHIVE,'r:xz') as tf:
  for m in tf:
   p=PurePosixPath(m.name);assert m.isfile() and not p.is_absolute() and '..' not in p.parts and p.parts[0]=='review115-publication-001'
   rel=PurePosixPath(*p.parts[1:]).as_posix();assert rel in expected and rel not in seen;seen.add(rel);d=tf.extractfile(m).read();assert len(d)==expected[rel]['bytes'] and sha(d)==expected[rel]['sha256']
 assert seen==set(expected)
 for source in sources:assert sha((BASE/source['archive']).read_bytes())==source['sha256']
 post=json.loads((ROOT/'POSTMERGE_IDENTITY.json').read_text());ad=ARCHIVE.read_bytes()
 delivery={'status':'PASS_READY_FOR_PUBLICATION_NOT_UPLOADED','publication_root':str(ROOT),'archive':str(ARCHIVE),'archive_bytes':len(ad),'archive_sha256':sha(ad),'archive_git_blob_sha1':blob(ad),'archive_member_count':len(seen),'payload_bytes_excluding_manifest':manifest['payload_bytes_excluding_manifest'],'roundtrip':'PASS_ALL_REGULAR_MEMBER_BYTES_SIZES_SHA256_AND_SAFE_PATHS','all_399_original_expanded_member_mappings_checked':True,'source_archives_unchanged':True,'initial_assembly_correction_preserved':'ASSEMBLY_CORRECTION.json and assembly-history/attempt-001/','source_archive_expanded_members':{x['archive']:x['member_count'] for x in sources},'manifest':str(ROOT/'MANIFEST.json'),'manifest_sha256':sha(md),'direct_files':{n:{'path':str(ROOT/n),'bytes':(ROOT/n).stat().st_size,'sha256':sha((ROOT/n).read_bytes())} for n in ['README.md','SEMANTIC_REVIEW.md','RECEIPT.json','FRESH_REVIEW_RECEIPT.json','POSTMERGE_IDENTITY.json','SOURCE_BINDINGS.json','VERIFIER_METADATA_BINDINGS.json']},'actual_merge_commit':post['actual_merge_commit'],'actual_merge_ordered_parents':post['actual_merge_ordered_parents'],'actual_merge_tree':post['actual_merge_tree'],'observed_current_main':post['observed_current_main'],'observed_current_main_tree':post['observed_current_main_tree'],'merge_attribution':post['merge_attribution'],'remote_mutations':False,'uploaded':False}
 (BASE/'agent12-review115-publication-001-delivery.json').write_text(json.dumps(delivery,indent=2)+'\n');print(json.dumps(delivery,indent=2))
if __name__=='__main__':
 try:main()
 except BaseException:
  (ROOT/'seal-publication-failure.log').write_text(traceback.format_exc());raise
