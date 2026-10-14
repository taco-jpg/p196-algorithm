"""Independent integer-arithmetic control of the exact uniform-core graph."""
from itertools import product
from pathlib import Path
import json

BULK = (16,14,10,2,4,8)

def integer_step(prefix, phase, middle):
    q = prefix + (BULK[phase],)*middle + prefix[::-1]
    length = len(q)
    digits = [0]*length
    for i in range(length//2):
        digits[i] = q[i]//2
        digits[-1-i] = q[i]-digits[i]
    if length%2:
        assert q[length//2]%2 == 0
        digits[length//2] = q[length//2]//2
    n = int(''.join(map(str,digits[::-1])))
    assert len(str(n)) == length
    out = n + int(str(n)[::-1])
    actual = tuple(map(int,str(out)[::-1]))
    r = tuple(a+b for a,b in zip(actual,actual[::-1]))
    k = len(prefix)
    overflow = len(r)-length
    assert overflow in (0,1)
    if r[k:len(r)-k] != (BULK[(phase+1)%6],)*(middle+overflow):
        return None
    return ((phase+1)%6, r[:k], overflow)

def main():
    cpp = json.loads(Path('exist_count_uniform_graph_results.json').read_text())
    reports = []
    for k in range(1,4):
        edges = {}
        unsafe = core_fail = overflow_edges = 0
        for phase,b in enumerate(BULK):
            for tail in product(range(19),repeat=k-1):
                for a in range(1,19):
                    prefix=(a,)+tail
                    if b<=9 and all(x<=9 for x in prefix):
                        unsafe+=1
                        continue
                    samples=[integer_step(prefix,phase,m) for m in (3,4,7,8)]
                    assert all(z==samples[0] for z in samples)
                    z=samples[0]
                    if z is None:
                        core_fail+=1
                        continue
                    phase2,prefix2,h=z
                    edges[(phase,prefix)]=(phase2,prefix2)
                    overflow_edges+=h
        done=set()
        cycles=0
        for start in edges:
            if start in done:
                continue
            seen=set()
            current=start
            while current in edges and current not in seen and current not in done:
                seen.add(current)
                current=edges[current]
            cycles+=int(current in seen)
            done.update(seen)
        row={'boundary_width':k,'states':6*18*19**(k-1),'unsafe_states':unsafe,
             'core_mismatches':core_fail,'valid_edges':len(edges),
             'overflow_edges':overflow_edges,'cycles':cycles,
             'middle_controls':[3,4,7,8]}
        expected=cpp['widths'][k-1]
        for key in ('states','unsafe_states','core_mismatches','valid_edges','overflow_edges','cycles'):
            assert row[key]==expected[key], (key,row,expected)
        reports.append(row)
        print(json.dumps(row),flush=True)
    Path('exist_count_uniform_independent_results.json').write_text(json.dumps(reports,indent=2)+'\n')

if __name__=='__main__':
    main()
