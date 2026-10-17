import pathlib,json,hashlib,subprocess,re
root=pathlib.Path(__file__).resolve().parents[5]
base=root/'proofs/contributions/agent-1/zero-width-loop-20261016/registry-preflight'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
modules={};origins=[];duplicates=[]
for name in ['Agent1PeriodicWidthLift','Agent1PeriodicReturnCore']:
 p=root/'proofs'/(name+'.registry.json');d=json.loads(p.read_text());origins.append({'path':str(p.relative_to(root)),'sha256':sha(p)})
 for project in d['projects'].values():
  for m,v in project['modules'].items():
   if m in modules:
    assert modules[m]==v,m
    duplicates.append(m)
   else:modules[m]=v
name='Agent1PeriodicZeroWidthLoop';p=root/'proofs'/(name+'.lean')
source=p.read_text();imports=re.findall(r'^import (\S+)',source,re.M)
modules[name]={'path':str(p.relative_to(root)),'sha256':sha(p),'git_blob':subprocess.check_output(['git','hash-object',str(p)],text=True,cwd=root).strip(),'imports':imports}
order=[];seen=set()
def visit(m):
 if m in ['Std','Init'] or m in seen:return
 assert m in modules,m
 seen.add(m)
 for dep in modules[m]['imports']:visit(dep)
 order.append(m)
visit(name)
assert len(order)==37,len(order)
for m in order:
 v=modules[m];p=root/v['path'];assert sha(p)==v['sha256'],m
 assert subprocess.check_output(['git','hash-object',str(p)],text=True,cwd=root).strip()==v['git_blob'],m
 assert re.findall(r'^import (\S+)',p.read_text(),re.M)==v['imports'],m
exports=re.findall(r'^#print axioms (\S+)',source,re.M);assert len(exports)==11
key='agent1-periodic-zero-width-loop'
out={'schema_version':1,'catalogue_complete':False,'catalogue_blockers':['Scoped 37-module contribution registry; not a repository-wide accepted catalogue.','Author source checks are recorded separately; parent and independent fresh closure verification pending.'],'toolchain':{'version':'4.19.0','commit':'6caaee842e94','allowed_axioms':['propext','Classical.choice','Quot.sound']},'projects':{key:{'scope':'An explicit sixteen-edge labelled closed walk with eight clocks in the necessary width projection starts at the projection of an original-valid canonically realizable zero-period template. Every positive exact full quotient path from that initial tuple fails to return. No claim that an actual orbit follows the selected abstract walk, no nonpalindromicity or all-time safety, and no196 conclusion.','roots':[name],'modules':{m:modules[m] for m in order}}},'claims':[{'id':'A1-ZERO-WIDTH-LOOP-NOT-SUFFICIENT','project':key,'endpoints':exports}],'source_baseline':'946c69edf3d2e6a87f5516db1fd0091eae29e663','source_pin_origins':origins,'accepted_global_registry_modified':False,'verification_status':'SOURCE_PINS_VALIDATED; fresh closure pending'}
p=root/'proofs/Agent1PeriodicZeroWidthLoop.registry.json';p.write_text(json.dumps(out,indent=2)+'\n')
report={'status':'PASS_SOURCE_PIN_AND_IMPORT_VALIDATION','modules':len(order),'new_public_endpoints':exports,'duplicate_module_records_identical':duplicates,'registry_sha256':sha(p),'roots':[name],'excluded_modules':[m for m in modules if m not in seen],'new_lean_execution':False}
(base/'result.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
