"""Independent exact checks; no search implementation or stochastic model imports."""
from collections import Counter
from itertools import product
from pathlib import Path
import json

def step(n): return n+int(str(n)[::-1])
def pal(n): return str(n)==str(n)[::-1]
def carry(n):
    d=list(map(int,str(n)[::-1]));q=[a+b for a,b in zip(d,reversed(d))];c=[0]
    for x in q:c.append((x+c[-1])//10)
    return c

def closed_count(L):
    if L==1:return 4
    m=L//2
    return (5 if L%2 else 1)*45*55**(m-1)+8*9**(m-1)

counts=[]
for L in range(1,7):
    actual=sum(pal(step(n)) for n in range(10**(L-1),10**L))
    assert actual==closed_count(L)
    counts.append({'width':L,'input_count':9*10**(L-1),'one_step_palindromes':actual})

families=[]
for m in range(1,5):
    marginals=[Counter() for _ in range(2*m)];checked=0
    for first in range(1,10):
        for inner in product(range(10),repeat=m-1):
            half=(first,)+inner
            digits=half+tuple(9-d for d in half[::-1])
            n=int(''.join(map(str,digits)))
            assert not pal(n)
            assert step(n)==10**(2*m)-1
            for j,d in enumerate(digits):marginals[j][d]+=1
            checked+=1
    assert checked==9*10**(m-1)
    for j,ct in enumerate(marginals):
        allowed=range(1,10) if j==0 else range(9) if j==2*m-1 else range(10)
        assert set(ct)==set(allowed)
        assert len(set(ct.values()))==1
    families.append({'width':2*m,'all_inputs_nonpalindromic':True,'inputs_checked':checked,'common_palindromic_image':str(10**(2*m)-1),'input_max_nontrivial_fourier_modulus':'1/9','output_max_nontrivial_fourier_modulus':'1'})

atoms=[22421411,33532522]
records=[]
for n in atoms:
    c=carry(n);L=len(str(n));ind=[int(c[k]==c[L-1-k]) for k in (1,3)]
    records.append({'n':n,'Tn':step(n),'palindromic_output':pal(step(n)),'carries':c,'I1_I3':ind})
assert records[0]['I1_I3']==[1,1] and records[1]['I1_I3']==[0,0]
assert all(r['carries'][-1]==0 for r in records)
assert all(int(b)-int(a)==1 for a,b in zip(str(atoms[0]),str(atoms[1])))
out={'status':'PASS','one_step_counts':counts,'sum9_families':families,'correlated_indicator_atoms':records,'P_I1':'1/2','P_I3':'1/2','P_I3_given_I1':'1','decimal_lychrel_existence_proved':False,'scope':'Finite exact controls for separately written all-length marginal counterexamples. No claim of W2 for the deterministic 196 orbit.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
