#!/usr/bin/env python3
"""Validate historical inventory plus direct published blob identities, without extraction."""
from pathlib import Path,PurePosixPath
import hashlib,json,tarfile,io
r=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
blob=lambda b:hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
m=json.loads((r/"ownership-manifest.json").read_text());raw=(r/"source-scope-inventory.tar.gz").read_bytes()
assert len(raw)==m["archive_bytes"] and sha(raw)==m["archive_sha256"] and blob(raw)=="555dd32a4df6b73de7f4f4d3c1a2a7081c175950"
expected={x["archive_path"]:x for x in m["source_files"]};seen={}
with tarfile.open(fileobj=io.BytesIO(raw)) as t:
 for mem in t:
  assert mem.isfile() and mem.name in expected and mem.name not in seen
  p=PurePosixPath(mem.name);assert not p.is_absolute() and ".." not in p.parts
  b=t.extractfile(mem).read();rec=expected[mem.name]
  assert sha(b)==rec["sha256"] and len(b)==rec["bytes"]
  seen[mem.name]=sha(b)
assert set(seen)==set(expected) and len(seen)==18
published=json.loads((r/"remote-changed-blobs.json").read_text());assert len(published)==173
matches=[]
for name in ["final-independent.tar.gz","generic-verification.tar.gz","runtime-development.tar.gz"]:
 with tarfile.open(r/name) as t:
  for mem in t:
   if mem.name in published:
    b=t.extractfile(mem).read();assert blob(b)==published[mem.name]
    matches.append({"archive":name,"path":mem.name,"git_blob":blob(b)})
out={"result":"PASS","new_lean_executions":0,"historical_inventory":{"archive":"source-scope-inventory.tar.gz","bytes":len(raw),"sha256":sha(raw),"git_blob":blob(raw),"members":18,"member_hashes":seen,"classification":m["purpose"]},"published_changed_files":173,"archive_members_matching_direct_published_git_blobs":matches}
(r/"supplemental-integrity.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"result":"PASS","inventory_members":18,"inventory_bytes":len(raw),"inventory_sha256":sha(raw),"direct_published_member_matches":len(matches)},indent=2))
