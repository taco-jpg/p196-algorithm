"""Fresh ZeroExterior compilation against the root-rebuilt decimal dependency."""
from pathlib import Path
import hashlib,json,os,re,shutil,subprocess,time
HERE=Path(__file__).resolve().parent
PASS=HERE.parent
PROJECT=PASS.parents[1]
SOURCE=PASS/'lean/zero_exterior/ZeroExterior.lean'
CORE=PROJECT/'continuation/LychrelDigitSums.lean'
BUILD=HERE/'zero_exterior_build'
BUILD.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
prior=json.loads((HERE/'lean_rebuild.json').read_text())
assert prior['status']=='PASS'
assert sha(CORE)==prior['source_sha256']['continuation/LychrelDigitSums.lean']
assert sha(CORE)==sha(HERE/'lean_build/LychrelDigitSums.lean')
for name in ['LychrelDigitSums.olean','LychrelDigitSums.lean']:
    shutil.copyfile(HERE/'lean_build'/name,BUILD/name)
frozen=sha(SOURCE)
shutil.copyfile(SOURCE,BUILD/SOURCE.name)
names=['ZeroExterior.'+x for x in re.findall(r'^(?:theorem|def)\s+(\w+)',SOURCE.read_text(),re.M)]
audit=HERE/'ZeroExteriorAxioms.lean'
audit.write_text('import ZeroExterior\n'+''.join('#print axioms '+n+'\n' for n in names))
shutil.copyfile(audit,BUILD/audit.name)
compiler='/workspace/scratch/fe6abe1df721/lean-runtime/lean'
env=dict(os.environ,LEAN_PATH=str(BUILD))
logs=[]; rows=[]; axioms={}
for p in [SOURCE,audit]:
    (BUILD/(p.stem+'.olean')).unlink(missing_ok=True)
    start=time.monotonic()
    r=subprocess.run([compiler,'-o',p.stem+'.olean',p.name],cwd=BUILD,env=env,text=True,capture_output=True)
    row={'source':p.name,'exit_code':r.returncode,'seconds':time.monotonic()-start}
    rows.append(row); output=r.stdout+r.stderr
    logs.extend([json.dumps(row),output])
    (HERE/'zero_exterior_recheck.log').write_text('\n'.join(logs))
    assert r.returncode==0,output
    for m in re.finditer(r"'([^']+)' (?:depends on axioms:\s*\[([^\]]*)\]|does not depend on any axioms)",output,re.S):
        a=set(x.strip() for x in (m[2] or '').split(',') if x.strip())
        assert a<={'propext','Classical.choice','Quot.sound'}
        axioms[m[1]]=sorted(a)
assert set(axioms)==set(names)
assert sha(SOURCE)==frozen
result={'status':'PASS','source_sha256':frozen,'dependency_sha256':sha(CORE),'root_rebuilt_dependency_receipt':'lean_rebuild.json','compilations':rows,'declaration_axioms':axioms,'all_time_numeric_bridge_reviewed':True,'main_existence_proved':False}
(HERE/'zero_exterior_review.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':'PASS','declarations':len(names),'source_sha256':frozen}),flush=True)
