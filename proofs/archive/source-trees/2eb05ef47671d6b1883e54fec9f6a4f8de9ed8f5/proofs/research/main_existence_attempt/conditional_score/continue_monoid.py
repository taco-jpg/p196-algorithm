"""One controlled 600-second discovery run on the unchanged monoid CNF.

No proof trace is produced during discovery. SAT is independently replayed
but remains candidate_pending_root_audit; UNSAT remains proof_pending.
"""
from pathlib import Path
import time,json,subprocess,hashlib
import monoid

def canonical_realization(word):
    ps,c=word;digits=[0]*(2*len(ps)+(c is not None))
    for i,q in enumerate(ps):
        hi=min(q,9);lo=q-hi
        digits[i]=hi;digits[-1-i]=lo
    if c is not None:digits[len(ps)]=c//2
    assert digits and digits[0]>0 and all(0<=d<=9 for d in digits)
    return int(''.join(map(str,digits)))

def numerical_audit(word):
    r=monoid.w.r
    word=tuple(word[0]),word[1]
    assert r.valid(word)
    n=canonical_realization(word)
    def q_of(n):
        ds=tuple(map(int,str(n)))
        return r.fold(tuple(x+y for x,y in zip(ds,ds[::-1])))
    def T(n):return n+int(str(n)[::-1])
    n1=T(n);n2=T(n1)
    assert q_of(n)==word
    assert q_of(n1)==r.qstep(word)
    assert q_of(n2)==r.qstep(r.qstep(word))
    assert str(n2)!=str(n2)[::-1]
    return dict(canonical_realization=str(n),first_reverse_add=str(n1),shifted_candidate=str(n2),checks_passed=True,root_audit_pending=True)

def main():
    base=Path(__file__).parent;path=base/'monoid.cnf';t=time.monotonic()
    previous=json.loads((base/'monoid_45s_result.json').read_text())
    sha=hashlib.sha256(path.read_bytes()).hexdigest()
    assert sha==previous['cnf_sha256']
    meta=json.loads((base/'monoid_encoding.json').read_text())
    cmd=[str(monoid.p.ROOT/'lean-runtime/lean-4.19.0-linux/bin/cadical'),'-t','600',str(path)]
    start=dict(status='running',budget_seconds=600,cnf_sha256=sha,proof_trace=False,cnf_variables=meta['meta']['cnf_variables'],cnf_clauses=meta['meta']['cnf_clauses'],infinite_existence_proved=False)
    (base/'monoid_600s_status.json').write_text(json.dumps(start,indent=2));print(json.dumps(start),flush=True)
    with (base/'monoid_600s.log').open('w') as log:
        process=subprocess.Popen(cmd,stdout=log,stderr=subprocess.STDOUT)
        (base/'monoid_600s_process.json').write_text(json.dumps(dict(pid=process.pid,started_unix=time.time(),command=cmd),indent=2))
        result=process.wait(timeout=630)
    discovery='sat' if result==10 else 'unsat' if result==20 else 'unknown'
    report=dict(start,discovery_status=discovery,status='candidate_pending_root_audit' if discovery=='sat' else 'unsat_proof_pending' if discovery=='unsat' else 'unknown',returncode=result,seconds=time.monotonic()-t)
    if discovery=='sat':
        lines=(base/'monoid_600s.log').read_text().splitlines()
        model={abs(x):x>0 for line in lines if line.startswith('v ') for x in map(int,line[2:].split()) if x}
        checked=0
        for line in path.read_text().splitlines():
            if not line or line[0] in 'cp':continue
            clause=list(map(int,line.split()));assert clause[-1]==0
            assert any(model[abs(x)]==(x>0) for x in clause[:-1]);checked+=1
        assert checked==meta['meta']['cnf_clauses']
        values=[[int(model[v]) for v in row] for row in meta['tile_variables']]
        report['tile_values']=values;report['exact_check']=monoid.check_and_witness(values)
        report['numerical_audit']=numerical_audit(report['exact_check']['word'])
        report['model_clause_replay']=checked
    (base/'monoid_600s_result.json').write_text(json.dumps(report,indent=2))
    (base/'monoid_600s_status.json').write_text(json.dumps({k:v for k,v in report.items() if k!='tile_values'},indent=2))
    print(json.dumps({k:v for k,v in report.items() if k!='tile_values'}),flush=True)

if __name__=='__main__':main()
