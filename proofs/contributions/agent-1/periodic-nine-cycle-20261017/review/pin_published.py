#!/usr/bin/env python3
"""Independently verify published NinesCycle bytes and its actual minimal closure."""
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
registry_path='proofs/Agent1PeriodicNinesCycle.registry.json'
regbytes=(root/registry_path).read_bytes()
assert regbytes==git('show',commit+':'+registry_path),'Registry differs from published commit'
reg=json.loads(regbytes)
project=reg['projects']['agent1-periodic-nine-cycle']
assert project['roots']==['Agent1PeriodicNinesCycle']
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
new_modules=['Agent1PeriodicNinesPath','Agent1PeriodicNinesCycle']
public_declarations=[]
for module in new_modules:
    new_code=mask((root/modules[module]['path']).read_text())
    public_declarations.extend((module,kind,name) for kind,name in re.findall(r'^(?:noncomputable\s+)?(theorem|def|abbrev|structure|inductive)\s+(\w+)',new_code,re.M))
exports=['Agent1.Periodic.'+name for module,kind,name in public_declarations]
theorems=['Agent1.Periodic.'+name for module,kind,name in public_declarations if kind=='theorem']
definitions=['Agent1.Periodic.'+name for module,kind,name in public_declarations if kind!='theorem']
claimed=[name for claim in reg['claims'] if claim['project']=='agent1-periodic-nine-cycle' for name in claim['endpoints']]
assert len(exports)==len(set(exports)) and len(claimed)==len(set(claimed))
assert set(exports)==set(claimed),(exports,claimed)
identity={'status':'PUBLISHED_SOURCE_PIN_PASS','source_commit':commit,'registry_path':registry_path,'registry_sha256':sha(regbytes),'roots':project['roots'],'source_paths_match_published_commit':True,'actual_import_closure_exact':True,'module_count':len(ordered),'new_modules':new_modules,'new_module_exports':exports,'new_module_theorems':theorems,'new_module_definitions':definitions,'sources':ordered,'lean_execution_performed':False,'reviewer':'Agent #1 specialist symbolic_scope','independence':'Reviewer authored none of the two new nine-cycle modules; some already frozen dependency modules have prior reviewer authorship.'}
out=review/'final-source-identity.json'
assert not out.exists(),'Preserve earlier identity; use a separate review attempt for changed sources'
out.write_text(json.dumps(identity,indent=2)+'\n')
print(json.dumps({k:v for k,v in identity.items() if k!='sources'},indent=2))
