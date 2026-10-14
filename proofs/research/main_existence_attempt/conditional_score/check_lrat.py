"""Small independent checker for positive-hint LRAT/RUP certificates.

Deletions are deliberately ignored: retaining a proved clause is sound.
Negative RAT hints are rejected rather than trusted or silently skipped.
"""
from pathlib import Path
import json,hashlib,time,sys

def main():
    t=__import__('time').monotonic();base=Path(__file__).parent
    name=sys.argv[1] if len(sys.argv)>1 else 'any'
    source=base/(name+'.cnf');proof=base/(name+'.lrat');clauses={};n=None;m=None
    for line in source.read_text().splitlines():
        if not line or line.startswith('c'):continue
        if line.startswith('p'):
            _,_,nn,mm=line.split();n=int(nn);m=int(mm);continue
        row=list(map(int,line.split()));assert row[-1]==0
        assert all(1<=abs(x)<=n for x in row[:-1]);clauses[len(clauses)+1]=tuple(row[:-1])
    assert len(clauses)==m
    added=deleted=hints_used=0;proved_empty=False
    for lineno,line in enumerate(proof.read_text().splitlines(),1):
        toks=line.split()
        if not toks or toks[0]=='c':continue
        if toks[1]=='d':
            assert toks[-1]=='0';deleted+=len(toks)-3;continue
        row=list(map(int,toks));idx=row[0];sep=row.index(0,1)
        candidate=tuple(row[1:sep]);hints=row[sep+1:-1]
        assert row[-1]==0 and idx not in clauses
        assert all(h>0 for h in hints),('RAT hint unsupported',lineno)
        assignment={};conflict=False
        for lit in candidate:
            val=lit<0
            if abs(lit) in assignment and assignment[abs(lit)]!=val:conflict=True;break
            assignment[abs(lit)]=val
        if not conflict:
            for hint in hints:
                assert hint in clauses,(lineno,hint)
                hints_used+=1;unassigned=[];satisfied=False
                for lit in clauses[hint]:
                    val=assignment.get(abs(lit))
                    if val is None:unassigned.append(lit)
                    elif val==(lit>0):satisfied=True;break
                assert not satisfied,(lineno,hint,'satisfied hint')
                assert len(unassigned)<=1,(lineno,hint,'non-unit hint',unassigned)
                if not unassigned:conflict=True;break
                lit=unassigned[0];assignment[abs(lit)]=lit>0
        assert conflict,('failed RUP',lineno,idx)
        clauses[idx]=candidate;added+=1
        if not candidate:proved_empty=True
    assert proved_empty
    out=dict(verified=True,cnf_variables=n,cnf_clauses=m,checked_additions=added,ignored_deletions=deleted,checked_hints=hints_used,empty_clause_proved=True,seconds=time.monotonic()-t,cnf_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),lrat_sha256=hashlib.sha256(proof.read_bytes()).hexdigest(),scope='conditional XOR parity over 1123 carry-history tiles',infinite_existence_proved=False)
    (base/(name+'_lrat_check.json')).write_text(json.dumps(out,indent=2));print(json.dumps(out,indent=2))

if __name__=='__main__':main()
