#!/usr/bin/env python3
"""Source-only inherited preflight and author-frozen sharp-excursion registry."""
from pathlib import Path
import argparse,hashlib,json,re,shutil,subprocess,time
ROOT=Path(__file__).resolve().parents[5]
HERE=Path(__file__).resolve().parent
BASELINE="ee58c494d1021aa27ff71ef75653b962cf6a2006"
CLAIM="215f7c42462db4bccc2eb19917d0ea60f694d929"
PROJECT="agent1-periodic-nine-clock-strip"
TARGET="Agent1PeriodicNinesSharpExcursion"
NEW=["Agent1PeriodicCenterNormalPath","Agent1PeriodicNinesClockStrip",TARGET]
PRIORS=["Agent1PeriodicNinesExcursion.registry.json"]
OLD_ROOTS=["Agent1PeriodicNinesExcursion"]
TOKENS=["sorry","admit","sorryAx","native_decide","axiom","implemented_by","extern","unsafe","ofReduceBool","trustCompiler"]
def sha(b):return hashlib.sha256(b).hexdigest()
def blob(b):return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def save(p,v):p.write_text(json.dumps(v,indent=2)+"\n")
def git_bytes(commit,path):return subprocess.check_output(["git","show",commit+":"+path],cwd=ROOT)
def code_only(source):
    """Mask nested Lean comments and strings while retaining line positions."""
    out = list(source)
    i = depth = 0
    string = False
    while i < len(source):
        if depth:
            if source.startswith('/-', i):
                out[i:i+2] = '  '; depth += 1; i += 2
            elif source.startswith('-/', i):
                out[i:i+2] = '  '; depth -= 1; i += 2
            else:
                if source[i] != '\n': out[i] = ' '
                i += 1
        elif string:
            if source[i] == '\\':
                out[i] = ' '; i += 1
                if i < len(source): out[i] = ' '; i += 1
            else:
                if source[i] == '"': string = False
                if source[i] != '\n': out[i] = ' '
                i += 1
        elif source.startswith('/-', i):
            out[i:i+2] = '  '; depth = 1; i += 2
        elif source.startswith('--', i):
            while i < len(source) and source[i] != '\n':
                out[i] = ' '; i += 1
        elif source[i] == '"':
            out[i] = ' '; string = True; i += 1
        else:
            i += 1
    assert not depth and not string, 'Unterminated comment/string'
    return ''.join(out)

p=argparse.ArgumentParser();p.add_argument("run");m=p.add_mutually_exclusive_group(required=True);m.add_argument("--inherited-only",action="store_true");m.add_argument("--freeze",action="store_true");a=p.parse_args()
run=HERE/a.run;assert run.parent==HERE and run.name.startswith("run-");run.mkdir(exist_ok=False);shutil.copy2(__file__,run/"prepare.py");(run/"sources").mkdir()
started=time.time();prior={};origins=[];duplicates=[]
for filename in PRIORS:
 path="proofs/"+filename;raw=(ROOT/path).read_bytes();assert raw==git_bytes(BASELINE,path),path
 origins.append({"path":path,"sha256":sha(raw),"git_blob":blob(raw),"baseline_commit":BASELINE})
 for project in json.loads(raw)["projects"].values():
  for name,entry in project["modules"].items():
   pin={k:entry[k] for k in ("path","sha256","git_blob","imports")}
   if name in prior:assert prior[name]==pin,(name,path);duplicates.append({"module":name,"registry":path,"identical":True})
   else:prior[name]=pin
claimraw=(HERE/"claim.json").read_bytes();assert claimraw==git_bytes(CLAIM,"proofs/coordination/tasks/agent1-periodic-nine-clock-strip-20261017.json");claim=json.loads(claimraw)
assert claim["status"]=="CLAIMED"
for name in NEW:assert "proofs/"+name+".lean" in claim["intended_source_files"]
assert "proofs/"+TARGET+".registry.json" in claim["intended_source_files"]
modules={};order=[];active=set();hits=[];captures={}
def visit(name):
 if name in ("Std","Lean","Init") or name.startswith(("Std.","Lean.","Init.")) or name in modules:return
 assert name not in active,("Import cycle",name)
 active.add(name)
 path="proofs/"+name+".lean" if name in NEW else prior[name]["path"]
 raw=(ROOT/path).read_bytes();code=code_only(raw.decode())
 imports=[n for m in re.finditer(r"^\s*import\s+([^\n]+)",code,re.M) for n in m[1].split()]
 entry={"path":path,"sha256":sha(raw),"git_blob":blob(raw),"imports":imports}
 if name not in NEW:
  assert entry==prior[name],("Prior pin mismatch",name)
  assert raw==git_bytes(BASELINE,path),("Baseline mismatch",name)
 for token in TOKENS:
  for match in re.finditer(r"\b"+token+r"\b",code):hits.append({"module":name,"token":token,"line":code[:match.start()].count("\n")+1})
 for dep in imports:visit(dep)
 active.remove(name);modules[name]=entry;order.append(name);captures[path]=raw
 (run/"sources"/(name+".lean")).write_bytes(raw)
for name in (OLD_ROOTS if a.inherited_only else [TARGET]):visit(name)
assert not hits,hits
public=[]
if a.freeze:
 assert set(NEW).issubset(modules)
 for name in NEW:
  code=code_only(captures[modules[name]["path"]].decode())
  assert re.findall(r"^namespace\s+([^\n]+)",code,re.M)==["Agent1.Periodic"],name
  ds=re.findall(r"^\s*(?:@\[[^\]]*\]\s*)*(?:noncomputable\s+)?(theorem|def|abbrev|structure|inductive)\s+(\w+)",code,re.M)
  assert ds,("No public declarations",name)
  public.extend({"module":name,"kind":kind,"name":"Agent1.Periodic."+identifier} for kind,identifier in ds)
 confirmationraw=(HERE/"author-confirmation.json").read_bytes();confirmation=json.loads(confirmationraw)
 assert confirmation["author_confirmation_received"] is True
 assert set(confirmation["modules"])==set(NEW)
 for name,info in confirmation["modules"].items():
  assert info["source_sha256"]==modules[name]["sha256"],name
  assert info["compile_status"]==info["new_module_audit_status"]=="PASS",name
  assert info["receipts"],name
  for receipt in info["receipts"]:assert sha((ROOT/receipt["path"]).read_bytes())==receipt["sha256"],receipt["path"]
 (run/"author-confirmation.json").write_bytes(confirmationraw)
 scope=("The original maximal center-strip algorithm retracts every center with no whole mirrored period wrapper. On a positive original QuotientPath with returned center and period, every center through the endpoint is literally normalized, without initial normalization, original validity or exterior-return assumptions. For original ValidPeriodic nine input with literal initial center normalization, actual mixed entries and actual rawGamma=1, centerPeriods=1; ClockStrip retains its prior-claim authorship and evidence. Combined with the existing exact ledger, a supplied positive original-valid full B/H/w nine return has nonempty centers and a used transition dropping center length by at least eight, excluding a source-center cap of eight. No free carry/clock model, hidden initial-normalization premise on the full-return theorem, actual cycle construction, unrestricted nonreturn, infinite ordinary orbit or196 conclusion.")
 registry={"schema_version":1,"catalogue_complete":False,"catalogue_blockers":[f"Scoped {len(modules)}-module contribution registry, not a repository-wide catalogue.","All three new registered modules completed strict author compilation and full new-module audits; fresh parent and independent combined checks remain pending at registry freeze."],"toolchain":{"version":"4.19.0","commit":"6caaee842e94","allowed_axioms":["propext","Classical.choice","Quot.sound"]},"projects":{PROJECT:{"scope":scope,"roots":[TARGET],"modules":modules}},"claims":[{"id":"A1-PERIODIC-NINE-SHARP-EXCURSION","project":PROJECT,"endpoints":[d["name"] for d in public]}],"source_baseline":BASELINE,"source_pin_origins":origins,"accepted_global_registry_modified":False,"verification_status":"FROZEN_AUTHOR_CHECKED_FRESH_REVIEW_PENDING","metadata_validation":{"exact_actual_import_dfs":True,"module_count":len(modules),"new_module_count":len(NEW),"new_public_declaration_count":len(public),"new_public_theorem_count":len([d for d in public if d["kind"]=="theorem"]),"matching_duplicate_prior_pins":len(duplicates),"source_tokens_checked":TOKENS,"source_token_hits":hits,"lean_execution_performed_by_this_preflight":False,"claim_commit":CLAIM,"claim_git_blob":blob(claimraw),"claim_sha256":sha(claimraw)},"author_verification":{"new_modules_compile":"PASS","new_module_origin_audits":"PASS","fresh_combined_verification":"PENDING","evidence_path":str((HERE/"author-confirmation.json").relative_to(ROOT)),"evidence_sha256":sha(confirmationraw),"qualification":"Actual author confirmations and receipt hashes checked; this preflight never executes Lean."}}
 save(run/"registry.json",registry);target=ROOT/("proofs/"+TARGET+".registry.json");assert not target.exists(),"Preserve earlier registry; changed freeze requires explicit new checkpoint";shutil.copy2(run/"registry.json",target)
report={"status":"SOURCE_PREFLIGHT_PASS_AUTHOR_FROZEN" if a.freeze else "INHERITED_SOURCE_PREFLIGHT_PASS","baseline_commit":BASELINE,"claim_commit":CLAIM,"roots":[TARGET] if a.freeze else OLD_ROOTS,"module_count":len(modules),"new_module_count":len(NEW) if a.freeze else 0,"exact_actual_import_order":order,"prior_registry_origins":origins,"identical_duplicate_pins":duplicates,"new_public_declarations":public,"source_scan_tokens":TOKENS,"source_scan_hits":hits,"lean_execution_performed":False,"reviewer":"Agent #1 specialist control_review, registry only","independence":"No mathematical source authoring or final independent-review role in this task.","started_at_epoch":started,"finished_at_epoch":time.time()}
if a.freeze:report["registry_sha256"]=sha(target.read_bytes())
assert all((ROOT/path).read_bytes()==raw for path,raw in captures.items()),"Sources changed during source-only preflight"
save(run/"modules.json",modules);save(run/"report.json",report)
print(json.dumps({k:v for k,v in report.items() if k not in ("prior_registry_origins","identical_duplicate_pins")},indent=2))
