#!/usr/bin/env python3
"""Preserved strict author increments; dependency objects are reused after hash checks."""
from pathlib import Path
import hashlib, json, os, resource, shutil, subprocess, sys, time

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
LEAN = Path('/workspace/p196-tools/lean-4.19.0-linux/bin/lean')
MODULE = 'Agent1PeriodicEighteenLabel'
BASES = [Path('/workspace/p196-agent1-session-20261016/periodic-return-parent-clean-001/agent1-periodic-return-core/source')]

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def dump(p, x): p.write_text(json.dumps(x, indent=2)+'\n')
def limits(): resource.setrlimit(resource.RLIMIT_AS, (4*1024**3, 4*1024**3))

attempt = HERE / sys.argv[1]
attempt.mkdir(exist_ok=False)
shutil.copyfile(__file__, attempt/'run.py')
source = REPO/'proofs'/(MODULE+'.lean')
shutil.copyfile(source, attempt/source.name)
paths = [Path(p).resolve() for p in sys.argv[2:]] + BASES
records = {}
for filename in ['Agent1PeriodicReturnCore.registry.json']:
    registry = json.loads((REPO/'proofs'/filename).read_text())
    for project in registry['projects'].values():
        for name, rec in project['modules'].items():
            if name in records:
                assert records[name]['sha256']==rec['sha256'], name
                assert records[name]['imports']==rec['imports'], name
            records[name]=rec

imports = [line.split()[1] for line in source.read_text().splitlines() if line.startswith('import ')]
for name in imports:
    if name not in records:
        p=REPO/'proofs'/(name+'.lean')
        records[name]={'path':str(p.relative_to(REPO)), 'sha256':sha(p),
            'imports':[line.split()[1] for line in p.read_text().splitlines() if line.startswith('import ')]}
needed=set()
def visit(name):
    if name in needed or name=='Std' or name.startswith('Lean.'): return
    for dep in records[name]['imports']: visit(dep)
    needed.add(name)
for name in imports: visit(name)
deps=[]
for name in sorted(needed):
    rec=records[name]; original=REPO/rec['path']
    assert sha(original)==rec['sha256'], name
    directory=next(p for p in paths if (p/(name+'.olean')).is_file())
    src=directory/(name+'.lean'); obj=directory/(name+'.olean')
    assert sha(src)==rec['sha256'], (name, str(src))
    deps.append({'module':name,'original':str(original),'source':str(src),
        'source_sha256':sha(src),'object':str(obj),'object_sha256':sha(obj)})
dump(attempt/'dependencies.json',deps)
env=os.environ.copy();env['LEAN_PATH']=':'.join(map(str,[attempt,*paths]))
version=subprocess.check_output([str(LEAN),'--version'],text=True)
assert 'version 4.19.0' in version and '6caaee842e94' in version
(attempt/'lean-version.txt').write_text(version)
commands=[]
def run(label,args):
    start=time.monotonic()
    with (attempt/(label+'.log')).open('w') as log:
        result=subprocess.run(args,cwd=attempt,env=env,stdout=log,stderr=subprocess.STDOUT,
            timeout=600,preexec_fn=limits)
    commands.append({'name':label,'command':args,'cwd':str(attempt),'LEAN_PATH':env['LEAN_PATH'],
        'compiler_sha256':sha(LEAN),'address_space_limit_bytes':4*1024**3,
        'exit_code':result.returncode,'elapsed_seconds':time.monotonic()-start,
        'max_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss})
    dump(attempt/'commands.json',commands)
    print((attempt/(label+'.log')).read_text(),end='',flush=True)
    return result.returncode
flags=[str(LEAN),'--trust=0','-j1','-DElab.async=false','-DmaxHeartbeats=16000000']
code=run('compile',flags+['-o',MODULE+'.olean',MODULE+'.lean'])
if code==0:
    shutil.copyfile(HERE/'LabelAudit.lean',attempt/'LabelAudit.lean')
    code=run('audit',flags+['LabelAudit.lean'])
dump(attempt/'result.json',{'exit_code':code,'source_sha256':sha(attempt/(MODULE+'.lean')),
    'dependency_count':len(deps),'dependency_objects_reused':True,'fresh_full_closure':False})
sys.exit(code)
