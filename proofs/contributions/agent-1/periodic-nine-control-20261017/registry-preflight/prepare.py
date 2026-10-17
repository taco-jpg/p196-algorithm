#!/usr/bin/env python3
"""Immutable finite-control source preflight; never executes Lean."""
from pathlib import Path
import argparse,hashlib,json,re,shutil,subprocess,time
ROOT=Path(__file__).resolve().parents[5]
HERE=Path(__file__).resolve().parent
BASELINE="b8c17a5204ae56ad1fc99d8f9932ca9f57b6ac80"
CLAIM="d3eb5690eeb7d8b1daf002f44435a6a89470b581"
TARGET="Agent1PeriodicNinesExtraStrip"
PROJECT="agent1-periodic-nine-control"
EXPECTED="e50a7e04b272f8b0d78d380b1ec1e2df80fc4b1647719dd31bdac02109a8107e"
TOKENS=["sorry","admit","sorryAx","native_decide","axiom","implemented_by","extern","unsafe","ofReduceBool","trustCompiler"]
def sha(b): return hashlib.sha256(b).hexdigest()
def blob(b): return hashlib.sha1(b"blob "+str(len(b)).encode()+b"\0"+b).hexdigest()
def save(p,v): p.write_text(json.dumps(v,indent=2)+"\n")
def git_bytes(commit,path): return subprocess.check_output(["git","show",commit+":"+path],cwd=ROOT)
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

p=argparse.ArgumentParser();p.add_argument("run");a=p.parse_args()
run=HERE/a.run
assert run.parent==HERE and run.name.startswith("run-")
run.mkdir(exist_ok=False);shutil.copy2(__file__,run/"prepare.py");(run/"sources").mkdir()
claimraw=(HERE/"claim.json").read_bytes();assert claimraw==git_bytes(CLAIM,"proofs/coordination/tasks/agent1-periodic-nine-control-20261017.json")
claim=json.loads(claimraw)
assert claim["status"]=="CLAIMED"
assert "proofs/"+TARGET+".lean" in claim["intended_source_files"]
assert "proofs/"+TARGET+".registry.json" in claim["intended_source_files"]
prior_path="proofs/Agent1PeriodicQuotient.registry.json";priorraw=(ROOT/prior_path).read_bytes();assert priorraw==git_bytes(BASELINE,prior_path)
prior=json.loads(priorraw)["projects"]["agent1-periodic-quotient"]["modules"]
modules={};order=[];active=set();hits=[];captures={}
def visit(name):
 if name in ("Std","Init","Lean") or name in modules:return
 assert name not in active
 active.add(name)
 path="proofs/"+TARGET+".lean" if name==TARGET else prior[name]["path"]
 raw=(ROOT/path).read_bytes();code=code_only(raw.decode())
 imports=[n for m in re.finditer(r"^\s*import\s+([^\n]+)",code,re.M) for n in m[1].split()]
 entry={"path":path,"sha256":sha(raw),"git_blob":blob(raw),"imports":imports}
 if name!=TARGET:
  assert entry==prior[name],name
  assert raw==git_bytes(BASELINE,path),name
 else:assert sha(raw)==EXPECTED
 for token in TOKENS:
  for m in re.finditer(r"\b"+token+r"\b",code):hits.append({"module":name,"token":token,"line":code[:m.start()].count("\n")+1})
 for dep in imports:visit(dep)
 active.remove(name);modules[name]=entry;order.append(name);captures[path]=raw
 (run/"sources"/(name+".lean")).write_bytes(raw)
visit(TARGET)
assert len(modules)==15 and not hits,(len(modules),hits)
code=code_only(captures["proofs/"+TARGET+".lean"].decode())
assert re.findall(r"^namespace\s+([^\n]+)",code,re.M)==["Agent1.Periodic"]
public=re.findall(r"^\s*(?:@\[[^\]]*\]\s*)*(theorem|def|abbrev|structure)\s+(\w+)",code,re.M)
assert public==[("theorem","nines_extra_strip_control")],public
exports=["Agent1.Periodic."+name for kind,name in public]
author=ROOT/"proofs/contributions/agent-1/periodic-nine-control-20261017/author/attempt-001"
result=json.loads((author/"result.json").read_text())
assert result["status"]=="PASS" and result["source_sha256"]==EXPECTED and result["dependency_count"]==14 and result["fresh_closure"] is False
assert result["compiler_sha256"]=="92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023"
for c in result["commands"]:
 assert c["exit_code"]==0 and c["argv"][1:4]==["--trust=0","-j1","-DElab.async=false"]
 assert sha((author/(c["name"]+".log")).read_bytes())==c["log_sha256"]
receipt={"author_confirmation_received":True,"confirmation":"Root message: frozen first attempt001 PASS, no further source changes.","source_sha256":EXPECTED,"result_path":str((author/"result.json").relative_to(ROOT)),"result_sha256":sha((author/"result.json").read_bytes()),"fresh_closure":False,"author_reused_pinned_dependencies":14}
save(HERE/"author-confirmation.json",receipt);save(run/"author-confirmation.json",receipt)
origin={"path":prior_path,"sha256":sha(priorraw),"git_blob":blob(priorraw),"baseline_commit":BASELINE}
scope="One explicit finite control B=[1], H=[9,9,9,14,18,18,14,9,9,9], w=[9,9,9,9]: original ValidPeriodic; initial literal strip=(H,0); actual entry sum1; actual raw period unchanged; exactly two mirrored period pairs stripped; residual [18,18]; quotient outer [3]; next actual raw period also nine. Refutes only a blanket one-step centerPeriods<=1 bound on this original-valid initially normalized input domain with nonempty residual. No safe successor, cycle, infinite continuation, temporal descent or 196 conclusion."
registry={"schema_version":1,"catalogue_complete":False,"catalogue_blockers":["Scoped 15-module contribution registry, not a repository-wide catalogue.","Strict author compile/origin audit passed; fresh independent and parent verification pending at freeze."],"toolchain":{"version":"4.19.0","commit":"6caaee842e94","allowed_axioms":["propext","Classical.choice","Quot.sound"]},"projects":{PROJECT:{"scope":scope,"roots":[TARGET],"modules":modules}},"claims":[{"id":"A1-PERIODIC-NINE-EXTRA-STRIP-CONTROL","project":PROJECT,"endpoints":exports}],"source_baseline":BASELINE,"source_pin_origins":[origin],"accepted_global_registry_modified":False,"verification_status":"FROZEN_AUTHOR_CHECKED_FRESH_REVIEW_PENDING","metadata_validation":{"exact_actual_import_dfs":True,"module_count":15,"new_module_count":1,"new_public_declaration_count":1,"new_public_theorem_count":1,"source_tokens_checked":TOKENS,"source_token_hits":hits,"lean_execution_performed_by_this_preflight":False,"claim_commit":CLAIM,"claim_git_blob":blob(claimraw),"claim_sha256":sha(claimraw)},"author_verification":receipt}
save(run/"modules.json",modules);save(run/"registry.json",registry)
registry_path=ROOT/("proofs/"+TARGET+".registry.json");assert not registry_path.exists();shutil.copy2(run/"registry.json",registry_path)
assert all((ROOT/path).read_bytes()==raw for path,raw in captures.items())
report={"status":"SOURCE_PREFLIGHT_PASS_AUTHOR_FROZEN","baseline_commit":BASELINE,"claim_commit":CLAIM,"module_count":len(modules),"inherited_module_count":14,"new_module_count":1,"exact_dfs_order":order,"new_public_theorems":exports,"source_scan_hits":hits,"registry_sha256":sha(registry_path.read_bytes()),"source_sha256":EXPECTED,"lean_execution_performed":False,"independence":"control_review authors scoped registry/review metadata, none of the mathematical source."}
save(run/"report.json",report)
print(json.dumps(report,indent=2))
