import sys, collections, itertools, json
sys.path.insert(0,'research')
from astra_counting_nooverflow_depth import layers,sccs

def graph(depth,y,cap=200000):
    root=tuple((0,0) for _ in range(depth))
    first=frozenset(ns for ns,labs in layers(root,y+9) if all(labs))
    states=[first]; ix={first:0}; trans=[];todo=collections.deque([first])
    while todo:
        st=todo.popleft();row=[]
        for s in (y,y+9):
            nxt=frozenset(ns for path in st for ns,_ in layers(path,s))
            if nxt not in ix:
                if len(states)>=cap:return {'capped':cap}
                ix[nxt]=len(states);states.append(nxt);todo.append(nxt)
            row.append(ix[nxt])
        trans.append(row)
    accept=[any(all(a==b for a,b in path) for path in st) for st in states]
    components=sccs(trans)
    closed=[c for c in components if any(accept[v] for v in c) and all(w in c for v in c for w in trans[v])]
    return dict(states=len(states),nondeterministic=sum(len(s)>1 for s in states),components=[len(c) for c in components],closed=[dict(size=len(c),accept=sum(accept[v] for v in c)) for c in closed])

out=[]
for d,y in itertools.product(range(1,5),range(1,10)):
    r=dict(depth=d,y=y,**graph(d,y));print(r,flush=True);out.append(r)
open('main_existence_attempt/decimal_counting_return_alphabets.json','w').write(json.dumps(out,indent=2))
