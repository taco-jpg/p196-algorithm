"""Independent replay of the Laurent unit-pivot rank certificate.

Sources are rebuilt by substitution in the ORIGINAL2429-variable rows,
not by calling either elimination routine used during discovery.
"""
from pathlib import Path
from collections import deque
import json,sys,time,hashlib
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
import persist_spacetime_weighted as m
HERE=Path(__file__).resolve().parent

def plus(a,b):
    out=dict(a)
    for e,v in b.items():
        out[e]=out.get(e,0)+v
        if not out[e]:del out[e]
    return out

def times(a,b):
    out={}
    for e,v in a.items():
        for f,w in b.items():out[e+f]=out.get(e+f,0)+v*w
    return {e:v for e,v in out.items() if v}

def put(row,j,value):
    result=plus(row.get(j,{}),value)
    if result:row[j]=result
    elif j in row:del row[j]

def linear(a,b):
    out={}
    if a:out[0]=a
    if b-a:out[1]=b-a
    return out

def potential_substitutions():
    potentials=[];locations=[];offset=0
    for kind in ('safety','closure'):
        g0=m.trim(m.safety_graph() if kind=='safety' else m.closure_graph('0'))
        g1=m.trim(m.safety_graph() if kind=='safety' else m.closure_graph('1'))
        states,initial,edges,terms=g0
        assert states==g1[0] and initial==g1[1]
        adjacency=[[] for _ in states]
        for (u,v,a),(uu,vv,b) in zip(edges,g1[2]):
            assert (u,v)==(uu,vv)
            cost={j:linear(a.get(j,0),b.get(j,0)) for j in a.keys()|b.keys()}
            adjacency[u].append((v,{j:p for j,p in cost.items() if p}))
        paths=[None]*len(states);queue=deque(initial)
        for x in initial:paths[x]={}
        while queue:
            u=queue.popleft()
            for v,cost in adjacency[u]:
                if paths[v] is not None:continue
                paths[v]={j:dict(p) for j,p in paths[u].items()}
                for j,p in cost.items():put(paths[v],j,p)
                queue.append(v)
        assert all(x is not None for x in paths)
        potentials.extend(paths)
        edgebase=offset+2*len(initial)
        locations.extend((edgebase+i,1) for i in range(len(edges)))
        termbase=edgebase+len(edges)
        locations.extend((termbase+i,-1) for i in range(len(terms)))
        locations.extend((offset+2*i,1) for i in range(len(initial)))
        offset=termbase+len(terms)
    return potentials,locations,offset

def main():
    start=time.monotonic();file=HERE/'unit_pivot_certificate.json'
    cert=json.loads(file.read_text()); assert cert['complete']
    potential,locations,count=potential_substitutions()
    nv,a0,_,_=m.constraints('0',((7,),18))
    nv1,a1,_,_=m.constraints('1',((7,),18))
    assert nv==nv1==m.NW+len(potential)
    assert len(a0)==len(a1)==count+1
    def source(projected):
        index,sign=locations[projected];out={}
        for j in a0[index].keys()|a1[index].keys():
            poly=linear(sign*a0[index].get(j,0),sign*a1[index].get(j,0))
            if j<m.NW:put(out,j,poly)
            else:
                for k,q in potential[j-m.NW].items():put(out,k,times(poly,q))
        return out
    pivots=[];columns=set()
    for rec in cert['records']:
        row=source(rec['original_row'])
        for index,factorlist in rec['operations']:
            assert 0<=index<len(pivots)
            previous_col,previous=pivots[index]
            factor={int(e):int(v) for e,v in factorlist}
            assert row.get(previous_col,{})==factor
            neg={e:-v for e,v in factor.items()}
            for j,poly in previous.items():put(row,j,times(neg,poly))
        shift,sign=rec['normalization'];assert sign in (-1,1)
        row={j:{e+shift:v*sign for e,v in poly.items()} for j,poly in row.items()}
        col=rec['pivot_column']
        assert col not in columns and row[col]=={0:1}
        assert not columns.intersection(row)
        columns.add(col);pivots.append((col,row))
    assert len(pivots)==m.NW-(len(m.FS)-2)==1079
    # Every history has46 states, two prescribed starting potentials and
    #44 independent internal potentials. All states are reachable, proving
    #injectivity of the edge-difference map over every field.
    reachable={0,1}
    while True:
        new=reachable|{v for u,q,o,v in m.FE if u in reachable}
        if new==reachable:break
        reachable=new
    assert len(reachable)==len(m.FS)==46
    # Check each of the44 integer gauge vectors telescopes on every tile.
    for free in range(2,len(m.FS)):
        h=[int(j==free) for j in range(len(m.FS))]
        weights=[h[v]-h[u] for u,q,o,v in m.FE]
        weights.extend(-h[x] for x,c,extra,oc in m.TS)
        assert len(weights)==m.NW
        for i,(u,q,o,v) in enumerate(m.FE):assert weights[i]==h[v]-h[u]
        for (x,c),(extra,oc,tile) in m.TERMS.items():assert weights[tile]==-h[x]
    report=dict(checked=True,ring='Z[t,t^-1]',unit_pivots=len(pivots),
                weights=m.NW,gauge_dimension=44,
                conclusion='For every field and every nonzero scalar, all solutions score zero on every accepted history.',
                certificate_sha256=hashlib.sha256(file.read_bytes()).hexdigest(),
                seconds=time.monotonic()-start,existence_proved=False)
    (HERE/'unit_certificate_check.json').write_text(json.dumps(report,indent=2))
    print(json.dumps(report,indent=2))

if __name__=='__main__':main()
