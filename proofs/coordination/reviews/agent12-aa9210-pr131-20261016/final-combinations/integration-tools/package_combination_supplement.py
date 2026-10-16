import argparse,hashlib,json
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument("--publication",required=True);p.add_argument("--combo",action="append",required=True);p.add_argument("--evidence-commit",required=True);p.add_argument("--output",required=True)
a=p.parse_args(); pub=Path(a.publication); m=json.loads((pub/"MANIFEST.json").read_text())
arc=(pub/m["archive"]).read_bytes()
assert hashlib.sha256(arc).hexdigest()==m["archive_sha256"]
index={}
for row in m["files"]: index.setdefault((row["bytes"],row["sha256"]),row["path"])
files={};records=[]
for root in map(Path,a.combo):
 for f in sorted(root.rglob("*")):
  if not f.is_file(): continue
  b=f.read_bytes(); rel=root.name+"/"+f.relative_to(root).as_posix(); sha=hashlib.sha256(b).hexdigest(); origin=index.get((len(b),sha))
  row={"path":rel,"bytes":len(b),"sha256":sha}
  if origin:
   row.update({"storage":"EXACT_DUPLICATE_IN_PUBLISHED_ARCHIVE","original_archive_member":origin})
  else:
   files[rel]=b.decode("utf-8");row["storage"]="DIRECT_APPEND_ONLY_FILE"
  records.append(row)
receipt={"schema_version":1,"status":"LOSSLESS_APPEND_ONLY_SUPPLEMENT","prior_evidence_commit":a.evidence_commit,"prior_archive":m["archive"],"prior_archive_sha256":m["archive_sha256"],"prior_archive_git_blob":hashlib.sha1(b"blob "+str(len(arc)).encode()+b"\0"+arc).hexdigest(),"files":records,"direct_files":len(files),"duplicate_files":sum(r["storage"]=="EXACT_DUPLICATE_IN_PUBLISHED_ARCHIVE" for r in records),"explanation":"Every new combination artifact is retained directly or is byte-identical (same size and SHA256) to a specifically named file in the already published, round-trip-verified archive. No substantive source, command, result or failure is discarded; this removes only exact duplication."}
files["LOSSLESS_REUSE.json"]=json.dumps(receipt,indent=2)+"\n"
out=Path(a.output);assert not out.exists();out.write_text(json.dumps({"files":files,"receipt":receipt},ensure_ascii=False))
print(json.dumps({"output":str(out),"direct_files":receipt["direct_files"],"duplicate_files":receipt["duplicate_files"],"bytes":out.stat().st_size}))
