#!/usr/bin/env python3
"""Agent #17: read-only retained-evidence validation; never invoke Lean."""
from pathlib import Path, PurePosixPath
import collections, hashlib, io, json, re, subprocess, tarfile
ROOT=Path(__file__).resolve().parent
P="proofs/contributions/agent-101/protected-numeric-multiplicity-20261016/"
G="proofs/contributions/agent-101/nonpalindromic-fibers-20261016/"
C=P+"archives/final-independent-canonical/"
R=P+"reviews/"
ALLOWED={"propext","Classical.choice","Quot.sound"}
sha=lambda b:hashlib.sha256(b).hexdigest()
blob=lambda b:hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
out={"reviewer":"Agent #17 /root/pr114_evidence","pr":114,"head":"71c2ab3393e26d44b908fcbcc04d7527fac569f7","source_commit":"71691d50497edc83247b3571af276bb0ee438491","new_lean_executions":0,"archives":[]}
data={}
for name,mname,expected_blob in [
 ("final-independent.tar.gz","final-independent-manifest.json","d99f1971f633863e0b3f2864838abcf6eb5116d9"),
 ("generic-verification.tar.gz","generic-manifest.json","1af9f0df1a716e2b6876dcb88945f5cee2360087"),
 ("runtime-development.tar.gz","runtime-manifest.json","f3f780263ce71f94996c5091ec07d08d26a30359")]:
 raw=(ROOT/name).read_bytes(); mr=(ROOT/mname).read_bytes(); m=json.loads(mr)
 info=m["archive"] if isinstance(m["archive"],dict) else {"sha256":m["archive_sha256"],"bytes":m["archive_bytes"],"member_count":m["member_count"]}
 assert sha(raw)==info["sha256"] and len(raw)==info["bytes"] and blob(raw)==expected_blob
 expected={x["path"]:x for x in m["members"]};assert len(expected)==len(m["members"])
 d={}
 with tarfile.open(fileobj=io.BytesIO(raw),mode="r:gz") as tar:
  for member in tar:
   path=PurePosixPath(member.name)
   assert member.isfile() and not path.is_absolute() and path.as_posix()==member.name
   assert not any(x in (".","..") for x in path.parts) and member.name not in d and member.name in expected
   assert not member.name.endswith((".olean",".ilean"))
   b=tar.extractfile(member).read(); row=expected[member.name]
   assert len(b)==row["bytes"]==member.size and sha(b)==row["sha256"]
   d[member.name]=b
 assert set(d)==set(expected) and len(d)==info["member_count"]
 assert not set(data).intersection(d)
 data.update(d)
 out["archives"].append({"filename":name,"bytes":len(raw),"sha256":sha(raw),"git_blob":blob(raw),"manifest_sha256":sha(mr),"members":len(d),"member_bytes":sum(map(len,d.values())),"all_member_hashes_match":True,"no_compiler_objects":True})
d=data
registry=json.loads(d["proofs/Agent101ProtectedFamily.registry.json"])
mods=registry["projects"]["agent101-protected-family"]["modules"]
canonical=json.loads(d[R+"final-canonical-verification.json"]);project=canonical["projects"]["agent101-protected-family"]
assert canonical["source_commit"]==out["source_commit"]
assert sha(d["proofs/Agent101ProtectedFamily.registry.json"])==canonical["registry_sha256"]=="04aba56fc69ef566d32b0c1064a4db2298f095d88e98fcd9fefe7f5c70614307"
assert d[R+"final-canonical-verification.json"]==d[C+"verification.json"]
assert d[R+"final-registry.json"]==d["proofs/Agent101ProtectedFamily.registry.json"]
assert len(mods)==len(project["sources"])==len(project["build_order"])==26
source_rows=[]
for module,rec in mods.items():
 raw=d[rec["path"]]; compiled=d[C+"agent101-protected-family/source/"+module+".lean"]
 assert sha(raw)==rec["sha256"] and blob(raw)==rec["git_blob"]
 assert sha(compiled)==project["sources"][module]["build_sha256"]
 if not rec.get("adapter"):assert raw==compiled
 source_rows.append({"module":module,"path":rec["path"],"sha256":sha(raw),"git_blob":blob(raw),"build_sha256":sha(compiled)})
original=d[mods["Lychrel196Research"]["path"]].splitlines(keepends=True)
embedded=d[mods["LychrelDigitSums"]["path"]].splitlines(keepends=True)
assert original[0]==b"import Std\n" and len(original[1:])==4444 and original[1:]==embedded[10:4454]
out["sources"]={"count":26,"published_bytes":sum(len(d[x["path"]]) for x in mods.values()),"registry_sha256":canonical["registry_sha256"],"verifier_sha256":sha(d["proofs/verify_project__214bf7673efe116b.py"]),"all_published_and_build_hashes_match":True,"foundation_embedded_lines":4444,"modules":source_rows}
files_raw=d[C+"FILES.json"]
assert files_raw==d[R+"final-canonical-FILES.json"]
files=json.loads(files_raw)
for path,row in files.items():assert len(d[C+path])==row["bytes"] and sha(d[C+path])==row["sha256"]
assert len(files)==55
counts=collections.Counter(PurePosixPath(k).suffix for k in files)
assert counts=={".lean":27,".log":27,".json":1}
manifest=json.loads((ROOT/"final-independent-manifest.json").read_text())
assert len(manifest["excluded_files"])==26 and all(r["path"].endswith(".olean") for r in manifest["excluded_files"])
out["erratum"]={"canonical_FILES_bytes":len(files_raw),"canonical_FILES_sha256":sha(files_raw),"entries":55,"suffix_counts":dict(counts),"omitted_olean_in_archive_manifest":26,"copies_compared_now":["archived canonical FILES","archived review FILES"],"historical_four_copy_claim":"Two archived copies independently rechecked; original historical local output was not available to this reviewer."}
logs=[]
for cmd in project["commands"]:
 b=d[C+cmd["log"]]
 assert sha(b)==cmd["log_sha256"]
 assert b==d[R+"final-build-logs/"+cmd["label"]+".log"]
 assert cmd["exit_code"]==0 and "--trust=0" not in cmd["argv"]
 assert not re.search(r"\berror:|sorryAx|Lean.ofReduceBool",b.decode())
 logs.append({"label":cmd["label"],"bytes":len(b),"sha256":sha(b),"exit_code":cmd["exit_code"],"argv":cmd["argv"]})
assert len(logs)==27
project_log=d[R+"final-ProjectAudit-trust0.log"].decode()
rows=re.findall(r"^AUDIT_THEOREM (\S+) (\S+) : \[([^\]]*)\]$",project_log,re.M)
assert len(rows)==1783 and len({n for m,n,a in rows})==1783
axiom_union=set()
for mod,name,axs in rows:
 assert mod in mods
 a={s.strip() for s in axs.split(",") if s.strip()};assert a<=ALLOWED;axiom_union.update(a)
assert axiom_union==ALLOWED
unsafe=re.findall(r"^UNSAFE_IMPLEMENTATION_AXIOM (\S+) (\S+)$",project_log,re.M)
assert len(unsafe)==32 and sorted([list(x) for x in unsafe])==sorted(project["unsafe_implementation_axioms"])
assert re.findall(r"^FULL_MODULE_AUDIT theorems=(\d+) union=(.*)$",project_log,re.M)==[("1783","[Classical.choice, Quot.sound, propext]")]
assert d[R+"final-ProjectAudit-trust0.log"]==d[C+"agent101-protected-family/logs/ProjectAudit.log"]
exports=json.loads(d[R+"final-public-exports.json"])
public_log=d[R+"final-PublicAudit-trust0.log"].decode()
printed=re.findall(r"^'([^']+)' (?:depends on axioms: \[([^\]]*)\]|does not depend on any axioms)$",public_log,re.M)
safe=re.findall(r"^PUBLIC_SAFE (\S+)$",public_log,re.M)
assert len(exports)==len(printed)==len(safe)==94 and set(safe)=={x["name"] for x in exports}=={n for n,a in printed}
assert collections.Counter(x["kind"] for x in exports)=={"theorem":85,"def":9}
public_union=set()
for name,axs in printed:
 a={s.strip() for s in axs.split(",") if s.strip()};assert a<=ALLOWED;public_union.update(a)
assert public_union==ALLOWED and re.findall(r"^PUBLIC_COUNT (\d+)$",public_log,re.M)==["94"]
commands=json.loads(d[R+"final-audit-commands.json"])
for cmd in commands:
 name="final-"+cmd["label"]+".log"
 assert cmd["returncode"]==0 and "--trust=0" in cmd["command"] and sha(d[R+name])==cmd["log_sha256"]
 filename="final-ProjectAudit.lean" if cmd["label"]=="ProjectAudit-trust0" else "final-PublicAudit.lean"
 assert sha(d[R+filename])==cmd["audit_source_sha256"]
 assert not re.search(r"\berror:|CUSTOM_AXIOM|DISALLOWED_AXIOMS|sorryAx|Lean.ofReduceBool",d[R+name].decode())
out["canonical_build"]={"reused_not_rerun":True,"compiler":canonical["compiler"],"commands":logs,"builds":26,"initial_audits":1,"explicit_trust_zero_module_builds":False}
out["final_audits"]={"reused_not_rerun":True,"commands":commands,"theorems":1783,"module_theorem_counts":dict(collections.Counter(m for m,n,a in rows)),"axiom_union":sorted(axiom_union),"unsafe_implementation_axioms_separately_recorded":len(unsafe),"public_count":94,"public_kinds":{"theorem":85,"def":9},"public_module_counts":dict(collections.Counter(x["module"] for x in exports)),"public_axiom_union":sorted(public_union),"public_axiom_sets":dict(collections.Counter(",".join(sorted(s.strip() for s in a.split(",") if s.strip())) or "NONE" for n,a in printed)),"endpoint":next({"name":n,"axioms":a} for n,a in printed if n=="Agent101.Protected.protectedNonpalFamily_exact")}
GR=G+"reviews/independent-numeric-bridge-20261016/"
gv=json.loads(d[GR+"verification.json"]);ca=json.loads(d[GR+"compiled-audit-verification.json"])
for cmd in gv["commands"]:
 assert cmd["exit_code"]==0 and "--trust=0" in cmd["argv"]
 b=d[GR+"logs/"+cmd["module"]+".log"]
 assert not re.search(r"\berror:|sorryAx|Lean.ofReduceBool",b.decode())
assert len(gv["commands"])==9 and len(gv["sources"])==7
for rec in gv["sources"]:
 matches=[b for p,b in d.items() if p.startswith(GR) and p.endswith("/"+rec["module"]+".lean")]
 assert matches and all(sha(b)==rec["sha256"] for b in matches)
e=d[GR+"logs/ExportAudit.log"].decode()
printed_g=re.findall(r"'([^']+)' (?:depends on axioms|does not depend on any axioms)",e)
assert len(printed_g)==51 and set(printed_g)==set(gv["reviewed_module_exports"]+gv["boundary_review_theorems"])
cl=d[GR+"logs/CompiledAudit.log"].decode()
logical=re.findall(r"COMPILED_(THEOREM|DEFINITION|OPAQUE) (\S+) (\S+)",cl)
assert len(logical)==48 and collections.Counter(k for k,m,n in logical)=={"THEOREM":44,"DEFINITION":4}
for text in [e,cl]:
 ax={a.strip() for group in re.findall(r"axioms: \[([^\]]*)\]",text) for a in group.split(",") if a.strip()}
 assert ax<=ALLOWED
assert len(re.findall(r"UNSAFE_COMPILER_IMPLEMENTATION (\S+) (\S+)",cl))==14
assert ca["exit_code"]==0 and "--trust=0" in ca["command"]
failed=json.loads(d[GR+"attempts/compiled-audit-v01.json"])
assert failed["exit_code"]==1
out["generic_review"]={"reused_not_rerun":True,"fresh_modules":7,"commands":9,"public":32,"boundary":19,"compiled_logical":48,"compiled_theorems":44,"compiled_definitions":4,"unsafe_implementation_symbols":14,"failed_classifier_preserved":True,"independence":gv["independence"]}
runtime=json.loads((ROOT/"runtime-manifest.json").read_text())
for rec in runtime["accepted_source_pins"]:
 for path in rec["matching_archived_snapshots"]:assert sha(d[path])==rec["sha256"]
out["development_evidence"]={"members":102,"accepted_snapshots_match":True,"classification":runtime["publication_caveat"],"not_used_as_exact_published_final_build":True}
helper=subprocess.run(["python3",str(ROOT/"final-independent-verify.py")],text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
(ROOT/"helper-verify-only.log").write_text(helper.stdout)
assert helper.returncode==0
out["new_helper_run"]={"argv":["python3",str(ROOT/"final-independent-verify.py")],"exit_code":helper.returncode,"stdout":helper.stdout,"log_sha256":sha(helper.stdout.encode())}
out["result"]="PASS_RETAINED_EVIDENCE_INTEGRITY"
(ROOT/"evidence-validation.json").write_text(json.dumps(out,indent=2)+"\n")
print(json.dumps({"result":out["result"],"archives":out["archives"],"sources":26,"canonical_FILES":out["erratum"],"final_theorems":1783,"public_declarations":94,"generic_logical":48,"new_lean_executions":0},indent=2))
