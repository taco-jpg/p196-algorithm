from pathlib import Path
import hashlib,json,re,subprocess
root=Path(__file__).resolve().parents[5];here=Path(__file__).resolve().parent
mods={};origins=[];dups=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
for name in ['Agent1PeriodicReturnCore','Agent1PeriodicReturnClock']:
 p=root/'proofs'/(name+'.registry.json');d=json.loads(p.read_text());origins.append({'path':str(p.relative_to(root)),'sha256':sha(p)})
 for project in d['projects'].values():
  for m,v in project['modules'].items():
   if m in mods:assert mods[m]==v,m;dups.append(m)
   else:mods[m]=v
exports=[]
for m in ['Agent1PeriodicInitialIncoming','Agent1PeriodicReturnUpper']:
 p=root/'proofs'/(m+'.lean');s=p.read_text();mods[m]={'path':str(p.relative_to(root)),'sha256':sha(p),'git_blob':subprocess.check_output(['git','hash-object',str(p)],text=True,cwd=root).strip(),'imports':re.findall(r'^import (\S+)',s,re.M)};exports.extend(re.findall(r'^#print axioms (\S+)',s,re.M))
order=[];seen=set()
def visit(m):
 if m in ['Std','Init'] or m in seen:return
 assert m in mods,m
 seen.add(m)
 for dep in mods[m]['imports']:visit(dep)
 order.append(m)
visit('Agent1PeriodicReturnUpper')
for m in order:
 v=mods[m];p=root/v['path'];assert sha(p)==v['sha256'];assert re.findall(r'^import (\S+)',p.read_text(),re.M)==v['imports']
 assert subprocess.check_output(['git','hash-object',str(p)],text=True,cwd=root).strip()==v['git_blob']
key='agent1-periodic-return-upper-gap'
out={'schema_version':1,'catalogue_complete':False,'catalogue_blockers':['Scoped contribution registry, not a repository-wide accepted catalogue.','Author verification recorded separately; parent and independent fresh closure verification pending.'],'toolchain':{'version':'4.19.0','commit':'6caaee842e94','allowed_axioms':['propext','Classical.choice','Quot.sound']},'projects':{key:{'scope':'Unchanged phase-catalog incoming initial-phase clock1, transported to the last literal quotient step; existing initial outside9/10 and original scalar lower-potential slack give N+2<=4C for positive complete initial-phase returns. The open actual quotient potential adapter reuses original local exterior bounds. No generic lower3/equality classifier, arbitrary-walk realization, safety, return existence or196 conclusion.','roots':['Agent1PeriodicReturnUpper'],'modules':{m:mods[m] for m in order}}},'claims':[{'id':'A1-INITIAL-PHASE-UPPER-CLOCK-GAP','project':key,'endpoints':exports}],'source_baseline':'84a65f296625e16851b4a369e27ffca43aaea40c','source_pin_origins':origins,'accepted_global_registry_modified':False,'verification_status':'SOURCE_PINS_VALIDATED; fresh closure pending'}
p=root/'proofs/Agent1PeriodicReturnUpper.registry.json';p.write_text(json.dumps(out,indent=2)+'\n')
r={'status':'PASS_SOURCE_PIN_IMPORT_CHECK','module_count':len(order),'new_public_endpoints':exports,'duplicate_records_identical':dups,'registry_sha256':sha(p),'new_lean_execution':False,'source_baseline':out['source_baseline']};(here/'result.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
