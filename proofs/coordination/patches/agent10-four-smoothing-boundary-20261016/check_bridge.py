"""Fresh exact-source dependency closure and transitive axiom audit.
Source pins are those read from the repository's accepted registry at
87d3b831f8093d0ae0d840c48a898613ef2fb515. No foundation adapter is needed here:
this closure imports the original Lychrel196Research once, and never imports
its duplicate embedding LychrelDigitSums. Original source bytes are unchanged.
"""
import hashlib,json,os,pathlib,re,subprocess,sys,tempfile
PINS={
'Lychrel196Research':('c6c1f5441c54a36f2d82b3ef78dff1ccdbc5a506','f8950d138fa4231b536059e2334d36b6496de3d25a806f4cf3925941aa05144c'),
'PrefixCarryBound':('925f1954f5ab5857f602f679764d149eb67416b7','a13fa77fd7862885a1f87e8329b094a0806a3f8277267db789e3a138cb43c486'),
'ActualCarryObservability':('8bfe81cb2e9e928609df8265d5d9a3605eaeed1e','465c8f05f46aa3d9e44c9ce5136de74fb402d1aa2494e5b89644fab84d1db3c9'),
'DifferenceObservability':('d0727d391ee901ddaa782c218f493a23b8aadff3','60e724414ebd2bcbe590b0d61976147ef280eedfab6ff057d7cbdb7aeb0505d7')}
ALLOWED={'propext','Classical.choice','Quot.sound'}

def main():
    lean=pathlib.Path(sys.argv[1]).resolve(); source_dir=pathlib.Path(sys.argv[2]).resolve()
    report=pathlib.Path(sys.argv[3]).resolve();report.mkdir(parents=True,exist_ok=True)
    version=subprocess.run([str(lean),'--version'],capture_output=True,text=True,check=True).stdout.strip()
    if 'version 4.19.0' not in version or '6caaee842e94' not in version: raise SystemExit('Wrong Lean: '+version)
    sources={}
    for name,(blob,digest) in PINS.items():
        data=subprocess.run(['git','cat-file','blob',blob],capture_output=True,check=True).stdout
        if hashlib.sha256(data).hexdigest()!=digest: raise SystemExit('Source mismatch: '+name)
        sources[name]=data
    new=['Agent10SmoothingBoundary','Agent10SmoothingBridge']
    for name in new:
        data=(source_dir/(name+'.lean')).read_bytes()
        if re.search(rb'\b(sorry|admit|native_decide|sorryAx|ofReduceBool)\b',data) or re.search(rb'^\s*axiom\s',data,re.M): raise SystemExit('Rejected shortcut: '+name)
        sources[name]=data
    result={'lean':version,'source_commit':subprocess.run(['git','rev-parse','HEAD'],capture_output=True,text=True,check=True).stdout.strip(),'source_pins':{n:hashlib.sha256(d).hexdigest() for n,d in sources.items()},'historical_git_blobs':{n:v[0] for n,v in PINS.items()},'verification_level':'WIP','attempts':[]}
    (report/'source-pins.json').write_text(json.dumps(result,indent=2)+'\n')
    for attempt in (1,2):
        with tempfile.TemporaryDirectory(prefix='agent10-bridge-clean-') as tmp:
            root=pathlib.Path(tmp);env=dict(os.environ);env['LEAN_PATH']=tmp
            env.pop('LD_PRELOAD',None)
            for name,data in sources.items(): (root/(name+'.lean')).write_bytes(data)
            for name in sources:
                cmd=[str(lean),'-j1','-DElab.async=false','--root='+tmp,'-o',str(root/(name+'.olean')),str(root/(name+'.lean'))]
                try:
                    run=subprocess.run(cmd,cwd=root,env=env,capture_output=True,text=True,timeout=240)
                    log=run.stdout+run.stderr;code=run.returncode
                except subprocess.TimeoutExpired as exc:
                    log=(exc.stdout or b'').decode(errors='replace')+(exc.stderr or b'').decode(errors='replace')+'\nTIMEOUT: 240 seconds\n';code=124
                (report/f'{attempt}-{name}.log').write_text(log)
                axioms=sorted({a.strip() for group in re.findall(r'depends on axioms:\s*\[([^\]]*)\]',log) for a in group.split(',') if a.strip()})
                expected=len(re.findall(rb'^#print axioms ',sources[name],re.M))
                observed=log.count('depends on axioms:')+log.count('does not depend on any axioms')
                passed=code==0 and observed==expected and not (set(axioms)-ALLOWED)
                row={'attempt':attempt,'module':name,'command':cmd,'exit_code':code,'expected_audits':expected,'observed_audits':observed,'axioms':axioms,'passed':passed}
                result['attempts'].append(row)
                (report/'bridge-verification.json').write_text(json.dumps(result,indent=2)+'\n')
                print('BEGIN_MODULE_LOG',attempt,name,flush=True);print(log,flush=True)
                print('END_MODULE_LOG',attempt,name,flush=True);print(json.dumps(row),flush=True)
                if not passed:raise SystemExit(1)
    result['verification_level']='LEAN-CHECKED'
    (report/'bridge-verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print('BEGIN_VERIFICATION_JSON');print(json.dumps(result,indent=2));print('END_VERIFICATION_JSON')
if __name__=='__main__':main()
