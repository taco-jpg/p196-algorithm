from pathlib import Path
import subprocess,os,json,hashlib,re
root=Path(__file__).resolve().parent
source=root/'source'
tool='/workspace/scratch/aaafdd394dd6/agent7-runtime/lean-4.19.0-linux/bin/lean'
command=[tool,'--trust=0','-j1','-DElab.async=false','-o',str(source/'AllExportsAudit.olean'),str(source/'AllExportsAudit.lean')]
result=subprocess.run(command,cwd=source,env=dict(os.environ,LEAN_PATH=str(source)),text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
(root/'AllExportsAudit.log').write_text(result.stdout)
allowed={'propext','Classical.choice','Quot.sound'}
observed=set()
for group in re.findall(r'depends on axioms: \[([^\]]*)\]',result.stdout):
    observed.update(x.strip() for x in group.split(',') if x.strip())
exports=json.loads((root/'exported-theorems.json').read_text())
reported=len(re.findall(r"^'P196\.Agent7\.OddFibers\.[^']+' (?:depends on axioms:|does not depend on any axioms)",result.stdout,re.MULTILINE))
passed=result.returncode==0 and observed<=allowed and reported==exports['total']
record={'command':command,'cwd':str(source),'exit_code':result.returncode,'export_count':exports['total'],'reported_count':reported,'axiom_union':sorted(observed),'unexpected_axioms':sorted(observed-allowed),'all_passed':passed,'log_sha256':hashlib.sha256(result.stdout.encode()).hexdigest()}
(root/'axiom-audit.json').write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(record,indent=2))
raise SystemExit(0 if passed else 1)
