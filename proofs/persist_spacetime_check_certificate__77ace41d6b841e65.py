"""No optimizer and no floating point: check a supplied rational dual exactly."""
from fractions import Fraction
from collections import defaultdict
from persist_spacetime_weighted import constraints
import hashlib,json,sys

def check(path):
    record=json.load(open(path));seed=record['seed']
    if not isinstance(seed,dict):seed=(tuple(seed[0]),seed[1])
    nv,rows,rhs,meta=constraints(record['lambda_'],seed)
    dual={int(i):Fraction(v) for i,v in record['dual'].items()}
    assert dual and all(0<=i<len(rows)-1 and y<=0 for i,y in dual.items())
    assert all(b==0 for b in rhs[:-1])
    coefficients=defaultdict(Fraction)
    for i,y in dual.items():
        for j,a in rows[i].items():coefficients[j]+=y*a
    assert all(coefficients[j]==rows[-1].get(j,0) for j in range(nv))
    encoded=json.dumps([sorted(r.items()) for r in rows],separators=(',',':')).encode()
    return dict(file=path,lambda_=record['lambda_'],seed=seed,
                inequalities=len(rows)-1,variables=nv,dual_nonzero=len(dual),
                matrix_sha256=hashlib.sha256(encoded).hexdigest(),
                exact_rational_check='passed',
                conclusion='The specified all-length additive carry-memory score cannot be positive on this seed.',
                decimal_lychrel_existence='unresolved')

if __name__=='__main__':
    paths=sys.argv[1:] or ['persist_spacetime_dual_1.json']
    results=[check(p) for p in paths]
    print(json.dumps(results,indent=2))
    json.dump(results,open('persist_spacetime_certificate_check_results.json','w'),indent=2)
