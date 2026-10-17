#!/usr/bin/env python3
"""Check all three frozen author packages without running Lean."""
from pathlib import Path
import hashlib,json,re,subprocess
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]
CONTRIBUTION=HERE.parent
COMPILER='92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
ALLOWED={'propext','Classical.choice','Quot.sound'}
sha=lambda b:hashlib.sha256(b).hexdigest()
load=lambda p:json.loads(p.read_bytes())
MODULES={
 'Agent1PeriodicCenterNormalPath':{'source_sha256':'fbf8ff955a238d4f3257073e9a936391df7203ad822e4cd5da2c427803ad59b4','author':'Agent #1 specialist center_parent_receipt','base':CONTRIBUTION/'normal-author','attempt':'attempt-001','theorems':5,'deps':15,'public':['Agent1.Periodic.stripPeriodCenter_of_maximal','Agent1.Periodic.quotient_path_return_centers_normal']},
 'Agent1PeriodicNinesSharpExcursion':{'source_sha256':'80a00dd7519b1184b1e9cf808f0bbdf5b18cab61ddc855709a5a82233908e596','author':'Agent #1 root','base':CONTRIBUTION/'sharp-author','attempt':'attempt-002','theorems':9,'deps':31,'public':['Agent1.Periodic.quotient_return_nines_center_drop_eight','Agent1.Periodic.quotient_path_nines_centers_le_eight_no_return']}
}
def verify_manifest(base,manifest_name,expected):
 raw=(base/manifest_name).read_bytes();assert sha(raw)==expected
 entries=json.loads(raw)
 for name,e in entries.items():
  assert not Path(name).is_absolute() and '..' not in Path(name).parts
  data=(base/name).read_bytes();assert len(data)==e['bytes'] and sha(data)==e['sha256'],name
 return entries

def audit_check(module,text,count,public):
 rows=re.findall(r'^AUDIT_THEOREM (?:'+re.escape(module)+r'\s+)?(\S+)\s*:\s*\[([^\]]*)\]',text,re.M)
 assert len(rows)==count and len({n for n,_ in rows})==count,(module,len(rows))
 union=set()
 for _,axs in rows:
  names={n.strip() for n in axs.split(',') if n.strip()};assert names<=ALLOWED;union|=names
 assert not re.findall(r'^(?:AUDIT_SAFE_DEFINITION|AUDIT_SAFE_OPAQUE|NONSAFE_DEFINITION|GENERATED_RUNTIME|UNSAFE_OPAQUE|UNSAFE_IMPLEMENTATION_AXIOM) ',text,re.M),module
 for name in public:
  assert name in {n for n,_ in rows} and "'"+name+"' depends on axioms:" in text,name
 return sorted(union)

def pins(paths):return [{'path':str(p.relative_to(ROOT)),'sha256':sha(p.read_bytes())} for p in paths]
confirmed={}
for module,spec in MODULES.items():
 base=spec['base'];run=base/spec['attempt'];source=ROOT/'proofs'/(module+'.lean')
 assert sha(source.read_bytes())==spec['source_sha256'] and source.read_bytes()==(run/source.name).read_bytes(),module
 frozen=load(base/'frozen-receipt.json');assert frozen['source_sha256']==spec['source_sha256']
 entries=verify_manifest(base,'FILES.json',frozen['manifest_sha256'])
 author=load(base/'author-receipt.json');assert author['source_sha256']==spec['source_sha256'] and author['compiler_sha256']==COMPILER
 expected_receipt=frozen.get('author_receipt_sha256',frozen.get('receipt_sha256'))
 assert sha((base/'author-receipt.json').read_bytes())==expected_receipt
 result=load(run/'result.json');assert result['status']=='PASS' and result['source_sha256']==spec['source_sha256'] and result['dependency_count']==spec['deps']
 assert not result.get('fresh_closure',result.get('fresh_full_closure'))
 commands=load(run/'commands.json')
 assert [c.get('label',c.get('name')) for c in commands]==['compile','audit']
 for c in commands:
  label=c.get('label',c.get('name'));assert c['exit_code']==0 and c['argv'][1:4]==['--trust=0','-j1','-DElab.async=false']
  assert sha((run/(label+'.log')).read_bytes())==c['log_sha256']
 union=audit_check(module,(run/'audit.log').read_text(),spec['theorems'],spec['public'])
 failed=[]
 if module=='Agent1PeriodicNinesSharpExcursion':
  first=load(base/'attempt-001/result.json');assert first['status']!='PASS';failed=['attempt-001']
 confirmed[module]={'author':spec['author'],'explicit_freeze_confirmation_received':True,'source_sha256':spec['source_sha256'],'compile_status':'PASS','new_module_audit_status':'PASS','strict_attempt':spec['attempt'],'theorem_constants':spec['theorems'],'safe_definitions':0,'runtime_entries':0,'actual_axiom_union':union,'public_endpoints':spec['public'],'dependency_objects_reused':spec['deps'],'fresh_full_closure':False,'author_manifest_entries_checked':len(entries),'failed_attempts_preserved':failed,'receipts':pins([base/'author-receipt.json',base/'frozen-receipt.json',base/'FILES.json',run/'result.json',run/'commands.json',run/'compile.log',run/'audit.log',run/'dependencies.json'])}
# ClockStrip preserves original author paths, all failed attempts and discovery.
module='Agent1PeriodicNinesClockStrip';clock_path='proofs/contributions/agent-1/periodic-nine-excursion-20261017/sharpness'
base=ROOT/clock_path;original=Path('/workspace/p196-agent1-nine-excursion-20261017')/clock_path
seal=load(base/'SEAL.json');assert seal['source_sha256']=='cf78db242e666ffaeb85444ee2347b97dac629a2dc6835c2ebf62b07f3a022d5'
assert seal['manifest_sha256']=='e28aa82e7a8fe30b2a7b7b80cf4c91fb23864c6618afda8f74c65f073b80a9a3'
entries=verify_manifest(base,'FILES.json',seal['manifest_sha256']);assert len(entries)==seal['manifest_file_count']
transfer_commit='28282029c5f88ebeb3e8043ff52fcf851dc7e060'
for name in list(entries)+['FILES.json','SEAL.json']:
 data=(base/name).read_bytes();assert data==(original/name).read_bytes(),name
 assert data==subprocess.check_output(['git','show',transfer_commit+':'+clock_path+'/'+name],cwd=ROOT),name
receipt=load(base/'final-receipt.json');assert sha((base/'final-receipt.json').read_bytes())==seal['final_receipt_sha256']
assert receipt['refined_claim']=='9d09aea2edccfceb174f6cfd31142ba1b0c09226' and receipt['author']=='/root/suffix_receipt_resume'
assert receipt['compiler_sha256']==COMPILER and receipt['successful_final_attempt']=='attempt-006'
source=ROOT/'proofs'/(module+'.lean');assert sha(source.read_bytes())==seal['source_sha256']
assert source.read_bytes()==(base/'attempt-006'/source.name).read_bytes()==subprocess.check_output(['git','show',transfer_commit+':proofs/'+source.name],cwd=ROOT)
for attempt in receipt['author_attempts']:
 run=base/('attempt-'+str(attempt['attempt']).zfill(3));command=load(run/'command.json')
 assert command['exit_code']==attempt['exit_code'] and command['source_sha256']==attempt['source_sha256']
 assert sha((run/'compile.log').read_bytes())==attempt['log_sha256']
 assert sha((run/source.name).read_bytes())==attempt['source_sha256']
for record in [load(base/'attempt-006/command.json'),load(base/'audit-001/result.json')]:
 assert record['exit_code']==0 and record['source_sha256']==seal['source_sha256'] and record['argv'][1:4]==['--trust=0','-j1','-DElab.async=false']
assert sha((base/'audit-001/audit.log').read_bytes())==receipt['audit']['log_sha256']
public=['Agent1.Periodic.centerPeriods_nines_clock_one'];union=audit_check(module,(base/'audit-001/audit.log').read_text(),16,public)
confirmed[module]={'author':'Agent #1 specialist suffix_receipt_resume','explicit_freeze_confirmation_received':True,'source_sha256':seal['source_sha256'],'compile_status':'PASS','new_module_audit_status':'PASS','strict_attempt':'attempt-006','theorem_constants':16,'safe_definitions':0,'runtime_entries':0,'actual_axiom_union':union,'public_endpoints':public,'dependency_objects_reused':17,'fresh_full_closure':False,'author_manifest_entries_checked':len(entries),'source_claim':receipt['refined_claim'],'transfer_commit':transfer_commit,'all_original_author_bytes_preserved':True,'failed_attempts_preserved':[x['attempt'] for x in receipt['author_attempts'] if x['exit_code']!=0],'intermediate_helper_only_pass_preserved':'attempt-003','receipts':pins([base/'final-receipt.json',base/'SEAL.json',base/'FILES.json',base/'attempt-006/command.json',base/'attempt-006/compile.log',base/'attempt-006/dependencies.json',base/'audit-001/result.json',base/'audit-001/audit.log',CONTRIBUTION/'source-transfer.json'])}
out=HERE/'author-confirmation.json';assert not out.exists()
out.write_text(json.dumps({'author_confirmation_received':True,'qualification':'All three exact source freezes explicitly confirmed. Source snapshots, strict successful command/log receipts and all sealed author manifest members verified. ClockStrip original authored attempts and paths remain byte-identical to the original workspace and transfer checkpoint; historical pending-publication text is not rewritten. This checker executes no Lean. Fresh combined review remains separate.','modules':confirmed},indent=2)+'\n')
print(json.dumps({'status':'ALL_AUTHOR_EVIDENCE_PASS','author_confirmation_sha256':sha(out.read_bytes()),'module_count':len(confirmed)},indent=2))
