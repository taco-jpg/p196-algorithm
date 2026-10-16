#!/usr/bin/env python3
"""Read-only independent verification of the retained constructed paths."""
import gzip
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def decimal(n):
    out = []
    while n:
        n, d = divmod(n, 10)
        out.append(d)
    return out or [0]


def true_step(n):
    rev = 0
    for d in decimal(n):
        rev = 10*rev+d
    return n+rev


def pal(n):
    ds = decimal(n)
    return ds == ds[::-1]


def bad(n):
    ds = decimal(n)
    q = [x+y for x,y in zip(ds,ds[::-1])]
    return max(q) <= 9 or (q[0] == 11 and set(q) <= {0,11})


def main():
    report = json.loads((HERE/'verification.json').read_text())
    compressed = (HERE/'paths.json.gz').read_bytes()
    raw = gzip.decompress(compressed)
    for data, key in [(compressed,'compressed'),(raw,'original')]:
        assert len(data) == report['raw_paths'][key+'_bytes']
        assert hashlib.sha256(data).hexdigest() == report['raw_paths'][key+'_sha256']
    assert hashlib.sha256((HERE/'check_congruence_paths.py').read_bytes()).hexdigest() == report['checker_sha256']
    records = json.loads(raw)
    cases = [(0,0),(1,1),(1,5),(2,0)]
    cases += [(r,ell) for r in [*range(2,65),128,256] for ell in (r,2*r+3)]
    assert [(r['R'],r['ell']) for r in records] == cases
    assert report['cases'] == [list(c) for c in cases]
    states = edges = violations = protected = 0
    for rec in records:
        R,ell = rec['R'],rec['ell']
        k = 7*R//4+1
        start = 2*(10**k-1)
        if R == 0:
            expected, a = [18,99],0
        else:
            a = 5 if R == 1 else k+2
            expected = [start,11*(10**k-1)]
            if R == 1:
                expected.append(10989)
            for j in range(ell+1):
                e = a+j
                expected.append(10**e+990*a+(989 if e%2==0 else 89))
            E = a+ell+1
            terminal = 10**E+(692 if E%2==0 else 782)
            expected.extend([terminal,true_step(terminal)])
        values = [int(n) for n in rec['states_decimal']]
        assert values == expected and rec['chain_label_a'] == a
        hit = 1 if R == 0 else ell+(5 if R == 1 else 4)
        assert rec['first_positive_palindrome_time'] == hit == len(values)-1
        assert not any(pal(n) for n in values[:-1]) and pal(values[-1])
        assert values[1] == true_step(values[0])
        assert values[-1] == true_step(values[-2])
        assert all(n%99 == 0 for n in values[1:])
        failed = []
        for t,n in enumerate(values):
            assert len(decimal(n)) >= len(decimal(start))+t//5
        for t,(n,out) in enumerate(zip(values,values[1:])):
            dn,do = decimal(n),decimal(out)
            assert n < out < 11*n
            assert len(dn) <= len(do) <= len(dn)+1
            assert out%9 == 2*n%9
            assert out%11 == (0 if len(dn)%2==0 else 2*n%11)
            assert pal(out) == bad(n) == pal(true_step(n))
            if bad(n):
                assert out == true_step(n)
            if sum(do) < 2*sum(dn)-9*len(dn):
                failed.append(t)
        assert failed == rec['digit_sum_lower_bound_failure_edges']
        if R >= 3:
            assert 1 in failed
        assert rec['safe_through_requested_R'] == (hit>R)
        if ell >= R or R == 0:
            assert hit > R
            protected += 1
        states += len(values)
        edges += len(values)-1
        violations += len(failed)
    assert (len(records),states,edges,violations,protected) == (134,8259,8125,128,133)
    assert report['status'] == 'PASS'
    assert report['state_count']==states and report['edge_count']==edges
    assert report['case_count']==len(records)
    assert report['digit_sum_lower_bound_failure_edge_count']==violations
    assert report['cases_required_safe_through_R']==protected
    result = {'result':'PASS','paths':len(records),'states':states,'edges':edges,
              'carry_budget_failures':violations,'protected_cases':protected,
              'method':'Independent arithmetic radix division and literal integer reversal; full exact catalog and retained-byte hashes checked without running or importing the producer.',
              'scope':'Constructed finite paths only, with genuine first and terminal edges. No global countermap or actual-orbit substitution.',
              'files':{n:hashlib.sha256((HERE/n).read_bytes()).hexdigest() for n in
                       ['CONGRUENCE_PATHS.md','check_congruence_paths.py','paths.json.gz','verification.json']}}
    (HERE/'independent_audit.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
