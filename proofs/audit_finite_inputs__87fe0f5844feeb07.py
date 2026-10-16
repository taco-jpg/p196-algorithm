"""Audit finite necessary constraints using ordinary decimal reverse-add.

Fresh QF_LRA replay remains a solver result, not a separate proof checker.
"""
from pathlib import Path
import json,sys,time
sys.path.insert(0,str(Path(__file__).resolve().parent))
from search import m,r,z3,make_solver,expression
HERE=Path(__file__).resolve().parent

def realize(word):
    pairs,center=word
    high=[max(1 if i==0 else 0,q-9) for i,q in enumerate(pairs)]
    low=[q-d for q,d in zip(pairs,high)]
    digits=high+([] if center is None else [center//2])+low[::-1]
    return int(''.join(map(str,digits)))

def pair_word(n):
    digits=tuple(map(int,str(n)))
    return r.fold(tuple(a+b for a,b in zip(digits,digits[::-1])))

def advance(n):return n+int(str(n)[::-1])

def main():
    began=time.monotonic();report={}
    negatives=json.loads((HERE/'short_word_negative_paths.json').read_text())
    for entry in negatives:
        word=tuple(entry['word'][0]),entry['word'][1]
        n=realize(word);assert pair_word(n)==word
        for _ in range(entry['bad_output_after']+1):n=advance(n)
        assert str(n)==str(n)[::-1]
    report['ordinary_decimal_bad_future_checks']=len(negatives)
    replay=[]
    for seed in (196,18887):
        file=HERE/f'seed{seed}_boundNone_offsetNone.json'
        d=json.loads(file.read_text());word=tuple(d['seed'][0]),d['seed'][1]
        assert word==pair_word(seed)
        solver,w,b,_,_=make_solver(word,None,None,d['orbit_samples'])
        for raw in d['closure_words']:
            q=tuple(raw[0]),raw[1];n=realize(q)
            assert pair_word(n)==q
            nxt=pair_word(advance(n));assert nxt==r.qstep(q)
            solver.add(z3.Or(expression(w,b,q)<=0,expression(w,b,nxt)>=1))
        solver.set(timeout=20000);status=solver.check()
        assert status==z3.unsat
        replay.append(dict(seed=seed,ordinary_decimal_closure_checks=len(d['closure_words']),
                           fresh_solver_status=str(status),independent_proof_certificate=False))
    report['fixed_seed_replays']=replay
    report['seconds']=time.monotonic()-began
    report['positive_certificate_found']=False
    (HERE/'finite_input_audit.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
