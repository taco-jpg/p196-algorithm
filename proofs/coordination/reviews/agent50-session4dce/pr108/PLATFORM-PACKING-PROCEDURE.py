from pathlib import Path
import hashlib,json,tarfile,gzip,io
base=Path("/dev/shm/p196-agent50-4dce66859b6c/pr108-platform")
out=Path("/dev/shm/p196-agent50-4dce66859b6c/publication")
out.mkdir(exist_ok=True)
entries=[]
for p in sorted(base.rglob("*")):
    if p.is_file():
        b=p.read_bytes()
        entries.append({"path":p.relative_to(base).as_posix(),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()})
manifest={"schema_version":1,"owner":"Agent #50/session4dce66859b6c","purpose":"Lossless preservation of PR108 exact original-head platform inspection; not repair acceptance or a Lean execution.","head":"6deb8522c14fa2127d5d565bafec0cff781ccdd3","files":entries}
manifest_raw=(json.dumps(manifest,indent=2)+"\n").encode()
buf=io.BytesIO()
with gzip.GzipFile(fileobj=buf,mode="wb",mtime=0) as gz:
    with tarfile.open(fileobj=gz,mode="w") as tar:
        for r in entries:
            data=(base/r["path"]).read_bytes()
            info=tarfile.TarInfo(r["path"]);info.size=len(data);info.mtime=0;info.mode=0o644
            tar.addfile(info,io.BytesIO(data))
        info=tarfile.TarInfo("MANIFEST.json");info.size=len(manifest_raw);info.mtime=0;info.mode=0o644
        tar.addfile(info,io.BytesIO(manifest_raw))
raw=buf.getvalue()
p=out/"pr108-platform-agent50.tar.gz"
p.write_bytes(raw)
(out/"pr108-platform-agent50.manifest.json").write_bytes(manifest_raw)
with tarfile.open(fileobj=io.BytesIO(raw),mode="r:gz") as t:
    assert len(t.getmembers())==len(entries)+1
    for r in entries:
        m=t.getmember(r["path"]); assert m.isfile()
        b=t.extractfile(m).read()
        assert len(b)==r["bytes"] and hashlib.sha256(b).hexdigest()==r["sha256"]
    assert t.extractfile("MANIFEST.json").read()==manifest_raw
blob=hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()
print(json.dumps({"path":str(p),"bytes":len(raw),"sha256":hashlib.sha256(raw).hexdigest(),"git_blob":blob,"members":len(entries)+1,"manifest":manifest,"validation":"PASS lossless member recovery and exact hashes"}))
