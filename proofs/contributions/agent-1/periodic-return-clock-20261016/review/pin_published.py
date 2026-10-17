#!/usr/bin/env python3
"""Independently verify published ReturnClock bytes and its actual minimal closure."""
import argparse, ast, hashlib, json, re, subprocess
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('--source-root',type=Path,required=True)
p.add_argument('--commit',required=True)
a=p.parse_args()
root=a.source_root.resolve()
review=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def git(*args): return subprocess.check_output(['git',*args],cwd=root)
commit=git('rev-parse',a.commit+'^{commit}').decode().strip()
registry_path='proofs/Agent1PeriodicReturnClock.registry.json'
regbytes=(root/registry_path).read_bytes()
assert regbytes==git('show',commit+':'+registry_path),'Registry differs from published commit'
reg=json.loads(regbytes)
project=reg['projects']['agent1-periodic-return-clock']
assert project['roots']==['Agent1PeriodicReturnClock']
modules=project['modules']
# Use the already controlled lexical masker without running the replay module.
tree=ast.parse((review/'replay.py').read_text())
masknode=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='lean_code_tokens')
namespace={}
exec(compile(ast.Module(body=[masknode],type_ignores=[]),'scanner','exec'),namespace)
mask=namespace['lean_code_tokens']
actual={}
entries={}
for name,entry in modules.items():
    data=(root/entry['path']).read_bytes()
    assert data==git('show',commit+':'+entry['path']),name+' differs from published commit'
    assert sha(data)==entry['sha256'],name+' SHA mismatch'
    blob=subprocess.check_output(['git','hash-object','--stdin'],input=data,cwd=root).decode().strip()
    assert blob==entry['git_blob'],name+' blob mismatch'
    code=mask(data.decode())
    imports=[]
    for match in re.finditer(r'^\s*import\s+([^\n]+)',code,re.M): imports.extend(match.group(1).split())
    assert imports==entry['imports'],(name,imports,entry['imports'])
    actual[name]=imports
    entries[name]=dict(module=name,path=entry['path'],sha256=sha(data),git_blob=blob,imports=imports)
seen=set(); active=set(); ordered=[]
def visit(name):
    if name in ('Init','Std','Lean') or name.startswith(('Init.','Std.','Lean.')): return
    assert name in modules,'Unregistered dependency '+name
    assert name not in active,'Import cycle at '+name
    if name in seen: return
    active.add(name)
    for dep in actual[name]: visit(dep)
    active.remove(name);seen.add(name);ordered.append(entries[name])
for name in project['roots']: visit(name)
assert seen==set(modules),('Not exact closure',set(modules)-seen)
new_code=mask((root/'proofs/Agent1PeriodicReturnClock.lean').read_text())
exports=['Agent1.Periodic.'+name for name in re.findall(r'^theorem\s+(\w+)',new_code,re.M)]
claimed=[name for claim in reg['claims'] if claim['project']=='agent1-periodic-return-clock' for name in claim['endpoints']]
assert exports==claimed,(exports,claimed)
identity={'status':'PUBLISHED_SOURCE_PIN_PASS','source_commit':commit,'registry_path':registry_path,'registry_sha256':sha(regbytes),'roots':project['roots'],'source_paths_match_published_commit':True,'actual_import_closure_exact':True,'module_count':len(ordered),'new_module_exports':exports,'sources':ordered,'lean_execution_performed':False,'reviewer':'Agent #1 specialist symbolic_scope','independence':'Reviewer authored none of Agent1PeriodicReturnClock; some already frozen dependency modules have prior reviewer authorship.'}
out=review/'final-source-identity.json'
assert not out.exists(),'Preserve earlier identity; use a separate review attempt for changed sources'
out.write_text(json.dumps(identity,indent=2)+'\n')
print(json.dumps({k:v for k,v in identity.items() if k!='sources'},indent=2))
