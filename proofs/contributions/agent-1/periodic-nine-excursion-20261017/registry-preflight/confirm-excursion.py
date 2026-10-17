#!/usr/bin/env python3
"""Check frozen excursion author evidence and join both author confirmations."""
from pathlib import Path
import hashlib,json,re
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
BASE=HERE.parent/'excursion-author'
RUN=BASE/'attempt-001'
EXPECTED='b923e5acf482fdaf7ce28e11ed6aae6f7a8f439107fde433a65809dbc9874919'
COMPILER='92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_bytes())
assert sha((BASE/'author-receipt.json').read_bytes())=='3da6e03b7305a2d2c588624caa7120e6ab258aa5e3db6774842850f5edca8808'
assert sha((BASE/'FILES.json').read_bytes())=='5f451215cf8397c4992e917057cfca8100db6072a8dbd601974ec536f3d7c375'
manifest=load(BASE/'FILES.json');assert len(manifest)==12
for path,entry in manifest.items():
    raw=(BASE/path).read_bytes();assert len(raw)==entry['bytes'] and sha(raw)==entry['sha256'],path
frozen=load(BASE/'frozen-receipt.json')
assert frozen['source_sha256']==EXPECTED and frozen['manifest_sha256']==sha((BASE/'FILES.json').read_bytes())
source=ROOT/'proofs/Agent1PeriodicNinesExcursion.lean'
assert sha(source.read_bytes())==EXPECTED and source.read_bytes()==(RUN/source.name).read_bytes()
result=load(RUN/'result.json')
assert result['status']=='PASS' and result['source_sha256']==EXPECTED and result['compiler_sha256']==COMPILER
assert result['dependency_count']==28 and not result['fresh_closure']
commands=load(RUN/'commands.json');assert commands==result['commands']
assert [c['name'] for c in commands]==['compile','audit']
for c in commands:
    assert c['exit_code']==0 and c['argv'][1:4]==['--trust=0','-j1','-DElab.async=false']
    assert sha((RUN/(c['name']+'.log')).read_bytes())==c['log_sha256']
dependencies=load(RUN/'dependencies.json');assert not dependencies['fresh_closure'] and len(dependencies['modules'])==28
for module,entry in dependencies['modules'].items():
    source_bytes=Path(entry['source_path']).read_bytes()
    assert sha(source_bytes)==entry['source_sha256'] and source_bytes==Path(entry['build_source']).read_bytes(),module
    assert sha(Path(entry['object']).read_bytes())==entry['object_sha256'] and entry['reused'],module
audit=(RUN/'audit.log').read_text()
rows=re.findall(r'^AUDIT_THEOREM (\S+)\s*:\s*\[([^\]]*)\]',audit,re.M)
assert len(rows)==15 and len({n for n,_ in rows})==15
assert 'MODULE_AUDIT theorem_constants=15 safe_defs=0 runtime=0 custom_axioms=0' in audit
allowed={'propext','Classical.choice','Quot.sound'};union=set()
for _,axs in rows:
    names={n.strip() for n in axs.split(',') if n.strip()};assert names<=allowed;union|=names
public=['Agent1.Periodic.quotient_return_nines_center_excursion','Agent1.Periodic.quotient_path_nines_small_centers_no_return']
for name in public:
    assert name in {n for n,_ in rows} and "'"+name+"' depends on axioms:" in audit
receipts=[BASE/'author-receipt.json',BASE/'frozen-receipt.json',BASE/'FILES.json',RUN/'result.json',RUN/'commands.json',RUN/'compile.log',RUN/'audit.log',RUN/'dependencies.json']
confirmation={'author':'Agent #1 root','explicit_freeze_confirmation_received':True,'source_sha256':EXPECTED,'compile_status':'PASS','new_module_audit_status':'PASS','strict_attempt':'attempt-001','theorem_constants':15,'safe_definitions':0,'runtime_entries':0,'actual_axiom_union':sorted(union),'public_endpoints':public,'dependency_objects_reused':28,'fresh_full_closure':False,'author_manifest_entries_checked':12,'dependency_sources_and_objects_rechecked':28,'lean_execution_performed_by_preflight':False,'receipts':[{'path':str(p.relative_to(ROOT)),'sha256':sha(p.read_bytes())} for p in receipts]}
out=HERE/'excursion-confirmation.json';assert not out.exists();out.write_text(json.dumps(confirmation,indent=2)+'\n')
ledger_path=HERE/'ledger-confirmation.json';assert sha(ledger_path.read_bytes())=='0bf7235c5ef7d98f8afb60cfce62827412cb29f36c6dee0c303b046d41a211cb';ledger=load(ledger_path)
assert sha((ROOT/'proofs/Agent1PeriodicNinesLedger.lean').read_bytes())==ledger['source_sha256']
for receipt in ledger['receipts']:assert sha((ROOT/receipt['path']).read_bytes())==receipt['sha256']
combined={'author_confirmation_received':True,'qualification':'Both authors explicitly froze these exact sources after their first strict compile/full-new-origin audit PASS. Author source snapshots, command/log receipts, sealed package manifests and root reused dependency objects were checked without executing Lean. These are incremental author checks; fresh parent and independent review remain pending.','modules':{'Agent1PeriodicNinesLedger':ledger,'Agent1PeriodicNinesExcursion':confirmation}}
target=HERE/'author-confirmation.json';assert not target.exists();target.write_text(json.dumps(combined,indent=2)+'\n')
print(json.dumps({'status':'BOTH_AUTHOR_EVIDENCE_PASS','author_confirmation_sha256':sha(target.read_bytes()),'source_sha256':EXPECTED},indent=2))
