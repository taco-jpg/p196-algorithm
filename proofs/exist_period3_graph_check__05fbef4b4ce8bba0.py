"""Independent literal-integer cross-check for the period-three family graph."""
import json,itertools,time

def bulk(state):
    r=state//190;a=2*((state%190)//19);b=state%19
    return tuple(a if 2*i%3==(r-1)%3 else b for i in range(3))

def actual(prefix,state,m):
    Q=bulk(state);r=state//190;M=3*m+r
    q=prefix+(Q*(m+1))[:M]+prefix[::-1]
    ds=[0]*len(q)
    for i in range(len(q)//2):
        ds[-1-i]=min(9,q[i]);ds[i]=q[i]-ds[-1-i]
    if len(q)%2:
        assert q[len(q)//2]%2==0
        ds[len(q)//2]=q[len(q)//2]//2
    n=int(''.join(map(str,ds[::-1])))
    s=str(n+int(str(n)[::-1]))
    if s==s[::-1]:return 'unsafe',None
    v=tuple(map(int,s[::-1]));out=tuple(x+y for x,y in zip(v,v[::-1]));k=len(prefix)
    h=len(out)-len(q);assert h in (0,1)
    newQ=out[k+6:k+9]
    if any(out[i]!=newQ[(i-k)%3] for i in range(k,len(out)-k)):
        return 'core_mismatch',None
    return 'valid',(out[:k],newQ,(r+h)%3,h)

def check(k):
    counts={'unsafe':0,'core_mismatch':0,'valid':0,'overflow':0};start=time.monotonic()
    for first in range(1,19):
      for tail in itertools.product(range(19),repeat=k-1):
        P=(first,)+tail
        for state in range(570):
            a=actual(P,state,4);b=actual(P,state,5)
            assert a==b,(P,state,a,b)
            counts[a[0]]+=1
            if a[0]=='valid':counts['overflow']+=a[1][-1]
            if k==1:
                assert a==actual(P,state,7)==actual(P,state,8)
    report=json.load(open('exist_period3_graph_results.json'))
    cpp=next(x for x in report['widths'] if x['boundary_width']==k)
    assert counts['unsafe']==cpp['unsafe_states']
    assert counts['core_mismatch']==cpp['core_mismatches']
    assert counts['valid']==cpp['valid_edges']
    assert counts['overflow']==cpp['overflow_edges']
    return dict(boundary_width=k,**counts,seconds=time.monotonic()-start,independent_literal_integer_check='passed')
if __name__=='__main__':
    records=[]
    for k in (1,2):
        records.append(check(k));print(records[-1],flush=True)
    json.dump(records,open('exist_period3_graph_check_results.json','w'),indent=2)
