#!/usr/bin/env python3
"""Check the explicit frozen ledger author receipts; no Lean execution."""
from pathlib import Path
import hashlib,json,re
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
BASE=HERE.parent/'ledger-author'
RUN=BASE/'attempt-001'
EXPECTED='f3cbfad8fc013e88d5337f51e4f43d8d4e459460f677b065b336876b2069af4a'
COMPILER='92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_bytes())
assert sha((BASE/'author-receipt.json').read_bytes())=='39778bb063c70841dcac605766575019f3c4cefa828855f519d693b099512c4d'
assert sha((BASE/'FILES.json').read_bytes())=='3e11367cf241a2377ff6028016c3eaf4d512a3f8b3f1046168ac9a40be90801b'
assert sha((BASE/'frozen-receipt.json').read_bytes())=='ea64d0f8d7017bec2e8c73719df9ab46d87b13174b48fed460efa1895663fba4'
manifest=load(BASE/'FILES.json')
assert len(manifest)==48
for path,entry in manifest.items():
    raw=(BASE/path).read_bytes()
    assert len(raw)==entry['bytes'] and sha(raw)==entry['sha256'],path
source=ROOT/'proofs/Agent1PeriodicNinesLedger.lean'
assert sha(source.read_bytes())==EXPECTED
assert source.read_bytes()==(RUN/source.name).read_bytes()
result=load(RUN/'result.json')
assert result['status']=='PASS' and result['exit_code']==0 and result['source_sha256']==EXPECTED
assert result['dependency_count']==24 and result['dependency_objects_reused'] and not result['fresh_full_closure']
compiler=load(RUN/'compiler.json')
assert compiler['sha256']==COMPILER
commands=load(RUN/'commands.json')
assert [c['label'] for c in commands]==['compile','audit']
for c in commands:
    assert c['exit_code']==0 and c['argv'][1:4]==['--trust=0','-j1','-DElab.async=false']
    assert sha((RUN/(c['label']+'.log')).read_bytes())==c['log_sha256']
audit=(RUN/'audit.log').read_text()
theorems=re.findall(r'^AUDIT_THEOREM (\S+)\s*:\s*\[([^\]]*)\]',audit,re.M)
defs=re.findall(r'^AUDIT_SAFE_DEFINITION (\S+)\s*:\s*\[([^\]]*)\]',audit,re.M)
runtime=re.findall(r'^GENERATED_RUNTIME (\S+)',audit,re.M)
assert len(theorems)==11 and len(defs)==5 and len(runtime)==13
assert 'custom_axioms=0' in audit
allowed={'propext','Classical.choice','Quot.sound'}
union=set()
for _,axs in theorems+defs:
    names={n.strip() for n in axs.split(',') if n.strip()}
    assert names<=allowed
    union|=names
assert all(not axs.strip() for _,axs in defs)
public=['Agent1.Periodic.ninesExtraStrips','Agent1.Periodic.ninesExtraSum','Agent1.Periodic.quotientCenter_nines_length_balance','Agent1.Periodic.quotient_path_nines_center_balance']
assert set(public)<=set(n for n,_ in theorems+defs)
for name in public:
    assert "'"+name+"' depends on axioms:" in audit or "'"+name+"' does not depend on any axioms" in audit
receipts=[BASE/'author-receipt.json',BASE/'frozen-receipt.json',BASE/'FILES.json',RUN/'result.json',RUN/'commands.json',RUN/'compiler.json',RUN/'compile.log',RUN/'audit.log',RUN/'dependencies.json']
confirmation={'author':'Agent #1 specialist center_parent_receipt','explicit_freeze_confirmation_received':True,'source_sha256':EXPECTED,'compile_status':'PASS','new_module_audit_status':'PASS','strict_attempt':'attempt-001','theorem_constants':11,'safe_definitions':5,'runtime_entries':13,'actual_axiom_union':sorted(union),'safe_definition_axiom_union':[],'public_endpoints':public,'dependency_objects_reused':24,'fresh_full_closure':False,'author_manifest_entries_checked':48,'lean_execution_performed_by_preflight':False,'receipts':[{'path':str(p.relative_to(ROOT)),'sha256':sha(p.read_bytes())} for p in receipts]}
out=HERE/'ledger-confirmation.json'
assert not out.exists()
out.write_text(json.dumps(confirmation,indent=2)+'\n')
print(json.dumps({'status':'LEDGER_AUTHOR_EVIDENCE_PASS','confirmation_sha256':sha(out.read_bytes()),'source_sha256':EXPECTED},indent=2))
