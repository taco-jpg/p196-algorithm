"""Fresh Lean compilation and transitive axiom audit; no cached objects reused."""
import hashlib,json,pathlib,re,subprocess,sys,tempfile
lean=pathlib.Path(sys.argv[1]).resolve()
source=pathlib.Path(sys.argv[2]).resolve()
report=pathlib.Path(sys.argv[3]).resolve();report.mkdir(parents=True,exist_ok=True)
text=source.read_text()
if re.search(r'\b(sorry|admit|native_decide|sorryAx|ofReduceBool)\b',text) or re.search(r'^\s*axiom\s',text,re.M):
    raise SystemExit('Rejected proof shortcut in source')
version=subprocess.run([str(lean),'--version'],text=True,capture_output=True,check=True).stdout.strip()
if 'version 4.19.0' not in version: raise SystemExit('Wrong Lean version: '+version)
result={'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'lean':version,'verification_level':'WIP','attempts':[]}
for attempt in (1,2):
    with tempfile.TemporaryDirectory(prefix='agent10-clean-') as tmp:
        root=pathlib.Path(tmp);target=root/source.name;target.write_bytes(source.read_bytes())
        cmd=[str(lean),'--root='+tmp,'-o',str(root/(source.stem+'.olean')),str(target)]
        run=subprocess.run(cmd,text=True,capture_output=True,timeout=240)
        log=run.stdout+run.stderr;(report/f'lean-{attempt}.log').write_text(log)
        audit_count=log.count('depends on axioms:')+log.count('does not depend on any axioms')
        axiom_lists=re.findall(r'depends on axioms:\s*\[([^\]]*)\]',log)
        axioms=sorted({a.strip() for group in axiom_lists for a in group.split(',') if a.strip()})
        forbidden=[a for a in axioms if a not in {'propext','Classical.choice','Quot.sound'}]
        passed=run.returncode==0 and audit_count==11 and not forbidden
        result['attempts'].append({'command':cmd,'exit_code':run.returncode,'audit_count':audit_count,'axioms':axioms,'unexpected_axioms':forbidden,'passed':passed})
        (report/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
        print(log,flush=True);print(json.dumps(result['attempts'][-1]),flush=True)
        if not passed: raise SystemExit(1)
result['verification_level']='LEAN-CHECKED'
(report/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
