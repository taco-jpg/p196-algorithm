"""Agent452 independent trim and finite-domain graph coverage audit.
The exact PR63 raw arithmetic is reused; trim decomposition, domain enumeration,
and sparse directed-cycle checking are independent implementations.
"""
import sys,json,time,hashlib,importlib.util
from pathlib import Path
from itertools import product
P=Path(__file__).parent
sp=importlib.util.spec_from_file_location('original',P/'original/review_all_trims.py')
o=importlib.util.module_from_spec(sp);sp.loader.exec_module(o)
key=lambda s:(s[0],tuple(s[1]),tuple(s[2]),tuple(s[3]))

def independent_variants(s):
    c,B,A,C=o.raw_parts(s);d=18-c
    bs=[tuple(B[:len(B)-j]) for j in range(len(B)+1) if all(x==c for x in B[len(B)-j:])]
    aa=[]
    for j1 in range(len(A)+1):
        if not all(x==c for x in A[:j1]):continue
        for j2 in range(len(A)-j1+1):
            if all(x==d for x in A[len(A)-j2:]):aa.append(tuple(A[j1:len(A)-j2]))
    cc=[tuple(C[k:len(C)-k]) for k in range(len(C)//2+1) if all(x==d for x in C[:k]+C[len(C)-k:])]
    return {(c,b,a,cc0) for b,a,cc0 in product(bs,aa,cc)}

def words(vals,maxlen):
    return [w for n in range(maxlen+1) for w in product(vals,repeat=n)]

def domain(phases,vals,mb,ma,mc,sym):
    B=words(vals,mb);A=words(vals,ma);C=[]
    if not sym:C=words(vals,mc)
    else:
        for n in range(mc+1):
            for h in product(vals,repeat=n//2):
                if n%2==0:C.append(h+h[::-1])
                else:
                    for m in range(0,19,2):C.append(h+(m,)+h[::-1])
    return {(c,b,a,m) for c,b,a,m in product(phases,B,A,C)}

def audit(name,args,expected):
    t=time.monotonic();U=domain(*args);E={};omissions=0;extra=0
    for u in U:
        s=(u[0],list(u[1]),list(u[2]),list(u[3]))
        full=independent_variants(s)&U
        old=set(map(key,o.all_trim_variants(s)))&U
        omissions+=len(full-old);extra+=len(old-full)
        if full:E[u]=full
    color={}
    def dfs(u):
        color[u]=1
        for v in E.get(u,()):
            if color.get(v)==1:return True
            if color.get(v,0)==0 and dfs(v):return True
        color[u]=2
        return False
    cycle=any(color.get(u,0)==0 and dfs(u) for u in E)
    result=[len(U),sum(len(vs) for vs in E.values()),max(map(len,E.values()),default=0),cycle]
    assert result==expected,(name,result,expected)
    canonical=[(u,v) for u in sorted(E) for v in sorted(E[u])]
    digest=hashlib.sha256(json.dumps(canonical,separators=(',',':')).encode()).hexdigest()
    record={'name':name,'args':args,'result':result,'expected':expected,'original_internal_edges_omitted':omissions,'original_internal_edges_extra':extra,'internal_edge_sha256':digest,'seconds':time.monotonic()-t,'independent_trim_checker_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'raw_arithmetic_scope':'Reused exact PR63 raw_parts, not an independent integer bridge or Lean proof','source_head':'ae3d8c1cc18f8293c941fa47d5f1a6989b59a858','exit_status':0}
    (P/(name+'.json')).write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record),flush=True)

v=list((0,1,8,9,10,17,18))
configs={
 'pr63_all16':(([1,2,3,4,5,6,7,8,10,11,12,13,14,15,16,17],list(range(19)),1,1,1,False),[128000,360,1,False]),
 'pr63_six':(([2,4,8,16,14,10],v,2,2,2,True),[350892,9023,4,False]),
 'pr63_two':(([6,12],v,2,2,2,True),[116964,352,1,False]),
 'pr64':(([6,12],v,2,2,3,True),[571824,1232,1,False]),
 'pr66':(([6,12],v,2,2,4,True),[890226,1584,1,False]),
 'pr67':(([6,12],v,3,2,2,True),[820800,1376,1,False]),
 'pr68':(([6,12],v,2,3,2,True),[820800,2112,1,False]),
}
if __name__=='__main__':
    for name in sys.argv[1:]:audit(name,*configs[name])
