#!/usr/bin/env python3
"""Read-only validation of retained PR172 author/preflight payload; never runs Lean."""
from pathlib import Path
import hashlib, json, re, sys

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'source'
PREFIX = Path('proofs/contributions/agent-1/periodic-nine-cycle-20261017')
BASE = SOURCE / PREFIX
OUT = Path(__file__).resolve().parent
H = 'b8c17a5204ae56ad1fc99d8f9932ca9f57b6ac80'
NEW = ['Agent1PeriodicNinesPath', 'Agent1PeriodicNinesCycle']
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}
COMPILER = '92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
checks, warnings, manifests, attempts, input_hashes = [], [], [], [], {}

def sha(raw): return hashlib.sha256(raw).hexdigest()
def blob(raw): return hashlib.sha1(b'blob ' + str(len(raw)).encode() + b'\0' + raw).hexdigest()
def read(p):
    raw=p.read_bytes()
    input_hashes[str(p.relative_to(ROOT))]={'bytes':len(raw),'sha256':sha(raw),'git_blob':blob(raw)}
    return raw
def obj(p): return json.loads(read(p))
def check(label, ok, detail=None):
    checks.append({'check':label,'passed':bool(ok),'detail':detail})
    if not ok: raise AssertionError(label + ': ' + str(detail))
def entries(label, base, records):
    count=0
    for e in records:
        p=base / e['path']; raw=read(p)
        check(label+': '+e['path']+' SHA256',sha(raw)==e['sha256'])
        if 'bytes' in e: check(label+': '+e['path']+' size',len(raw)==e['bytes'])
        count+=1
    manifests.append({'manifest':label,'checked_entries':count})
    return count

source_manifest=obj(ROOT/'SOURCE_MANIFEST.json')
check('source manifest head',source_manifest['source_head']==H)
indexed={e['path']:e for e in source_manifest['files']}
selected=[]
for p in sorted(BASE.rglob('*')):
    if not p.is_file(): continue
    parts=p.relative_to(BASE).parts
    if parts[0] in {'numeric-author','path-author','registry-preflight','scope'} or parts==('README.md',) or parts==('QUEUE.md',):
        selected.append(p)
for p in selected:
    raw=read(p); rel=str(p.relative_to(SOURCE)); e=indexed[rel]
    check('materialized scope identity '+rel,sha(raw)==e['sha256'] and blob(raw)==e['git_blob'] and len(raw)==e['bytes'])

numeric=obj(BASE/'numeric-author/frozen-receipt.json')
entries('numeric-author/frozen-receipt.json files_sha256',BASE/'numeric-author',
        [{'path':p,'sha256':v} for p,v in numeric['files_sha256'].items()])
path_manifest=obj(BASE/'path-author/manifest.json')
entries('path-author/manifest.json files',BASE/'path-author',path_manifest['files'])
entries('path-author/manifest.json runtime_objects',BASE/'path-author',path_manifest['runtime_objects'])
entries('registry-preflight/FILES.json',BASE/'registry-preflight',obj(BASE/'registry-preflight/FILES.json'))

registry=obj(SOURCE/'proofs/Agent1PeriodicNinesCycle.registry.json')
project=registry['projects']['agent1-periodic-nine-cycle']; modules=project['modules']
check('one scoped project and one root',len(registry['projects'])==1 and project['roots']==['Agent1PeriodicNinesCycle'])
check('34 registered source modules',len(modules)==34)
check('only flat proofs Lean sources in registered closure',all(v['path'].startswith('proofs/') and v['path'].count('/')==1 and v['path'].endswith('.lean') for v in modules.values()))
check('global registry explicitly excluded',registry['accepted_global_registry_modified'] is False)
check('only two canonical new proof files',sorted(p for p in indexed if p.endswith('.lean') and p.count('/')==1)==['proofs/Agent1PeriodicNinesCycle.lean','proofs/Agent1PeriodicNinesPath.lean'])
check('no accepted build or workflow mutation in incoming manifest',not any(p=='proofs/ACCEPTED_BUILD.json' or p.startswith('.github/') for p in indexed))
seen=set(); order=[]
def visit(n):
    if n in {'Std','Init','Lean'}: return
    check('import module registered '+n,n in modules)
    if n in seen: return
    seen.add(n)
    for dep in modules[n]['imports']: visit(dep)
    order.append(n)
visit(project['roots'][0])
check('all registered modules reachable',seen==set(modules))
endpoints=registry['claims'][0]['endpoints']
check('five endpoint names',len(endpoints)==len(set(endpoints))==5)
check('no archive module registered',all('/contributions/' not in v['path'] for v in modules.values()))
for n in NEW:
    raw=read(SOURCE/modules[n]['path'])
    check('new module byte identity '+n,sha(raw)==modules[n]['sha256'] and blob(raw)==modules[n]['git_blob'])
    check('new module imports match registry '+n,re.findall(r'^import\s+(\S+)',raw.decode(),re.M)==modules[n]['imports'])
actual_public=[]
for n in NEW:
    actual_public += ['Agent1.Periodic.'+x for x in re.findall(r'^theorem\s+(\w+)',read(SOURCE/modules[n]['path']).decode(),re.M)]
check('endpoints equal five public source theorems',actual_public==endpoints)

for lane, module, final_attempt, count in [('numeric-author','Agent1PeriodicNinesCycle','attempt-003',7),('path-author','Agent1PeriodicNinesPath','attempt-002',16)]:
    runner=read(BASE/lane/'run.py')
    for a in sorted((BASE/lane).glob('attempt-*')):
        result=obj(a/'result.json'); commands=obj(a/'commands.json'); deps=obj(a/'dependencies.json')
        source=read(a/(module+'.lean')); log=read(a/'compile.log').decode()
        expected=1 if lane=='path-author' and a.name=='attempt-001' else 0
        check('attempt source pin '+str(a.relative_to(BASE)),sha(source)==result['source_sha256'])
        check('attempt compile exit '+str(a.relative_to(BASE)),commands[0]['name']=='compile' and commands[0]['exit_code']==expected and result['exit_code']==expected)
        check('author honest increment '+str(a.relative_to(BASE)),result['dependency_objects_reused'] is True and result['fresh_full_closure'] is False)
        check('author dependency count '+str(a.relative_to(BASE)),result['dependency_count']==len(deps))
        check('runner preserved '+str(a.relative_to(BASE)),read(a/'run.py')==runner)
        check('compiler version retained '+str(a.relative_to(BASE)),'version 4.19.0' in read(a/'lean-version.txt').decode() and '6caaee842e94' in (a/'lean-version.txt').read_text())
        for cmd in commands:
            check('strict argv '+str(a.relative_to(BASE))+'/'+cmd['name'],all(f in cmd['command'] for f in ['--trust=0','-j1','-DElab.async=false']) and cmd['compiler_sha256']==COMPILER)
        for dep in deps:
            check('dependency source pin '+str(a.relative_to(BASE))+'/'+dep['module'],dep['module'] in modules and dep['source_sha256']==modules[dep['module']]['sha256'])
            check('dependency object hash format '+str(a.relative_to(BASE))+'/'+dep['module'],bool(re.fullmatch('[0-9a-f]{64}',dep['object_sha256'])))
        if expected:
            check('failed author evidence retained truthfully','error: omega could not prove' in log and 'sorryAx' in log and not (a/'audit.log').exists())
        else: check('successful compile excludes error/sorryAx','sorryAx' not in log and 'error:' not in log)
        if a.name==final_attempt:
            check('final author snapshot equals canonical '+module,source==read(SOURCE/'proofs'/(module+'.lean')))
            check('final author includes successful audit '+module,[c['name'] for c in commands]==['compile','audit'] and all(c['exit_code']==0 for c in commands))
            audit=read(a/'audit.log').decode()
            rows=re.findall(r'AUDIT_THEOREM\s+(\S+)\s*:\s*\[([^\]]*)\]',audit,re.S)
            check('author origin theorem count '+module,len(rows)==count and len(set(n for n,_ in rows))==count)
            for name,axs in rows:
                axset={x.strip() for x in axs.split(',') if x.strip()}
                check('author theorem permitted axioms '+name,axset <= ALLOWED)
            check('author summary matches count '+module,f'MODULE_AUDIT theorems={count}' in audit)
        attempts.append({'lane':lane,'attempt':a.name,'source_sha256':sha(source),'exit_code':result['exit_code'],'commands':len(commands),'dependency_count':len(deps),'fresh_full_closure':False})

objpath=BASE/'path-author/attempt-002/Agent1PeriodicNinesPath.olean'
objsha=sha(read(objpath))
numericdeps=obj(BASE/'numeric-author/attempt-003/dependencies.json')
cross=next(d for d in numericdeps if d['module']=='Agent1PeriodicNinesPath')
check('published path object matches numeric author dependency',cross['object_sha256']==objsha)
check('numeric manifest embedded attempts match actual result files',all(numeric['all_attempts'][a.name]==obj(a/'result.json') for a in sorted((BASE/'numeric-author').glob('attempt-*'))))
check('numeric receipt commands match final command record',numeric['commands']==obj(BASE/'numeric-author/attempt-003/commands.json'))
check('numeric receipt embedded origin summary',numeric['origin_audit']==obj(BASE/'numeric-author/origin-summary.json'))
check('numeric receipt embedded dependency provenance',numeric['dependency_provenance']==obj(BASE/'numeric-author/dependency-provenance.json'))
check('numeric excluded object absent from publication manifest',not any(p.startswith(str(PREFIX/'numeric-author')) and p.endswith('.olean') for p in indexed))
warnings.append({'boundary':'Historical numeric object and external reused dependency objects are deliberately not published; their recorded hashes are not claimed to have been rehashed in this review. Published Path object was rehashed and cross-bound.'})

confirm=obj(BASE/'registry-preflight/author-confirmation.json')
check('author-confirmation script pin',confirm['script_sha256']==sha(read(BASE/'registry-preflight/confirm-authors.py')))
check('confirmation does not claim fresh execution',confirm['lean_execution_performed_by_this_script'] is False and confirm['fresh_combined_verification']=='PENDING')
for n,rec in confirm['modules'].items():
    entries('author-confirmation/'+n,SOURCE,rec['receipts'])
    check('author confirmation source binding '+n,rec['source_sha256']==modules[n]['sha256'] and rec['source_git_blob']==modules[n]['git_blob'])
check('author confirmation total',confirm['total_origin_theorems']==23 and confirm['total_safe_definitions']==0 and confirm['total_generated_runtime_implementations']==0)
claimraw=read(BASE/'registry-preflight/claim.json'); claimread=obj(BASE/'registry-preflight/claim-read.json')
check('historical claim exact local identity',sha(claimraw)==claimread['sha256'] and blob(claimraw)==claimread['git_blob'])
for run,n in [('run-000',32),('run-001',34),('run-002',34)]:
    p=BASE/'registry-preflight'/run; report=obj(p/'report.json'); runmods=obj(p/'modules.json')
    check('preflight source script identity '+run,read(p/'prepare.py')==read(BASE/'registry-preflight/prepare.py') and report['script_sha256']==sha(read(p/'prepare.py')))
    check('preflight module count '+run,len(runmods)==report['module_count']==n)
    check('preflight inherited source pins '+run,all(rec==modules[name] for name,rec in runmods.items()))
    check('preflight claim pin '+run,report['claim_sha256']==sha(claimraw) and report['claim_git_blob']==blob(claimraw))
    check('preflight honest no compiler execution '+run,report['lean_execution_performed'] is False and report['source_scan_hits']==[] and report['source_snapshots_stable_during_run'] is True)
    check('preflight matching duplicate source pins '+run,len(report['duplicate_prior_pin_matches'])==17 and all(d['identical'] for d in report['duplicate_prior_pin_matches']))
    if n==34:
        runreg=obj(p/'registry.json')
        check('preflight registry file pin '+run,sha(read(p/'registry.json'))==report['registry_sha256'])
        check('preflight registry modules '+run,runreg['projects']['agent1-periodic-nine-cycle']['modules']==modules)
        for name in NEW: check('preflight snapshot '+run+'/'+name,read(p/(name+'.lean'))==read(SOURCE/'proofs'/(name+'.lean')))
check('final preflight registry equals canonical',read(BASE/'registry-preflight/run-002/registry.json')==read(SOURCE/'proofs/Agent1PeriodicNinesCycle.registry.json'))
check('final confirmation duplicated without alteration',read(BASE/'registry-preflight/run-002/author-confirmation.json')==read(BASE/'registry-preflight/author-confirmation.json'))
check('same historical numeric scout duplicated without alteration',read(BASE/'scope/periodic-nines-return-scope.md')==read(BASE/'numeric-author/SOURCE-SCOUT.md'))
check('historical pending explicitly disclosed','historical pending text' in read(BASE/'README.md').decode())
check('queue explicitly candidates not claims','These are candidates, not ownership claims.' in read(BASE/'QUEUE.md').decode())

result={'status':'PASS_SCOPED_ARCHIVE_PAYLOAD','source_head':H,'scope_file_count':len(selected),'scope_bytes':sum(p.stat().st_size for p in selected),'checks_passed':len(checks),'manifest_checks':manifests,'attempts':attempts,'registry':{'module_count':34,'inherited_count':32,'new_modules':NEW,'endpoints':endpoints,'sha256':sha(read(SOURCE/'proofs/Agent1PeriodicNinesCycle.registry.json'))},'published_runtime_object':{'path':str(objpath.relative_to(SOURCE)),'sha256':objsha,'bytes':objpath.stat().st_size,'numeric_dependency_match':True},'warnings':warnings,'lean_execution':'NOT_RUN','historical_scripts_executed':False,'inputs':input_hashes,'checks':checks}
(OUT/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in {'inputs','checks'}},indent=2))
