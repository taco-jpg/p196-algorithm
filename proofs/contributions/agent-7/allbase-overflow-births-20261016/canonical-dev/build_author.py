from pathlib import Path
import subprocess, hashlib, json, os, sys, time, re
root=Path(__file__).resolve().parents[1]
label=sys.argv[1] if len(sys.argv)>1 else "attempt-001"
out=root/"canonical-dev"/label
if out.exists():
    raise SystemExit("Refusing to overwrite retained attempt: "+str(out))
src=out/"source";logs=out/"logs"
src.mkdir(parents=True);logs.mkdir()
lean=Path("/workspace/scratch/aaafdd394dd6/agent7-runtime/lean-4.19.0-linux/bin/lean")
pins=json.loads((root/"dependencies/SOURCE_PINS.json").read_text())["dependencies"]
order=["SignedDigitUniqueness","BaseReflection","ResetNormalization","PhysicalWidth","SeamSafety","ReverseAdd","BaseBirths","ActualBaseBirths","AdjacentBirths","OverflowDigits","ActualOverflowBirths","OverflowEndpoints","CanonicalOverflowBirths"]
known={x["module"]:x["sha256"] for x in pins}
known.update({
"AdjacentBirths":"6585cab8fbb64f64115f76c59a6a061598b3d03c563797642e2de70f38ae9c59",
"OverflowDigits":"37926723ba9d0d95b567f27607a810ea40d4fc622d60571d79228a5d33f33f8f",
"ActualOverflowBirths":"4c43069bfad9c9dc2f4af1a61c9e9438d26648a5cfe3e6958e001058e0d19b8d",
"OverflowEndpoints":"58a2656f3f38a891635f694b822a8fd41bdbea1d4f411a4ae3fa34a92dfdbe58"})
records=[]
for module in order:
    origin=root/("dependencies/"+module+".lean" if module in {x["module"] for x in pins} else module+".lean")
    data=origin.read_bytes();sha=hashlib.sha256(data).hexdigest()
    if module in known and sha!=known[module]:
        raise SystemExit("Frozen source changed: "+module)
    (src/(module+".lean")).write_bytes(data)
    records.append({"module":module,"origin":str(origin.relative_to(root)),"sha256":sha,"bytes":len(data)})
env=dict(os.environ);env["LEAN_PATH"]=str(src)
report={"author":"Agent #7 /root","status":"RUNNING","toolchain":subprocess.check_output([str(lean),"--version"],text=True).strip(),"lean_sha256":hashlib.sha256(lean.read_bytes()).hexdigest(),"flags":["--trust=0","-j1","-DElab.async=false"],"fresh_project_objects":True,"sources":records,"commands":[],"scope":"13-module canonical all-base overflow author build; final independent module-origin audit is separate"}
def save():
    (out/"verification.json").write_text(json.dumps(report,indent=2)+"\n")
save()
for module in order:
    command=[str(lean),"--trust=0","-j1","-DElab.async=false","-o",module+".olean",module+".lean"]
    started=time.monotonic()
    r=subprocess.run(command,cwd=src,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    log=logs/(module+".log");log.write_text(r.stdout)
    report["commands"].append({"module":module,"command":command,"cwd":str(src),"exit_code":r.returncode,"seconds":round(time.monotonic()-started,3),"log":str(log.relative_to(out)),"log_sha256":hashlib.sha256(log.read_bytes()).hexdigest()})
    print(module+": "+str(r.returncode),flush=True)
    if r.returncode:
        report["status"]="FAILED";save();raise SystemExit(r.returncode)
    save()
axioms={}
for log in logs.glob("*.log"):
    text=log.read_text()
    for name,body in re.findall(r"'([^']+)' depends on axioms:\s*\[(.*?)\]",text,re.S):
        axioms[name]=[s.strip() for s in body.split(",") if s.strip()]
    for name in re.findall(r"'([^']+)' does not depend on any axioms",text):
        axioms[name]=[]
allowed={"propext","Classical.choice","Quot.sound"}
bad={name:xs for name,xs in axioms.items() if not set(xs)<=allowed}
target="P196.Agent7.AllBaseOverflow.canonical_reverse_add_overflow_theorem"
if target not in axioms or bad:
    report["status"]="AUDIT_FAILED";report["unexpected_axioms"]=bad;save()
    raise SystemExit("Missing canonical audit or unexpected axiom")
report["status"]="LEAN-CHECKED";report["literal_public_axiom_reports"]=len(axioms)
report["canonical_axioms"]=axioms[target]
report["axiom_union"]=sorted(set().union(*(set(x) for x in axioms.values())))
report["axiom_reports"]=axioms
save()
print(json.dumps({"status":report["status"],"modules":len(order),"literal_public_audits":len(axioms),"canonical_sha256":records[-1]["sha256"],"report_sha256":hashlib.sha256((out/"verification.json").read_bytes()).hexdigest()}),flush=True)
