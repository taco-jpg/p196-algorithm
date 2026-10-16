"""Human-auditable grammar obstructions as finite exact word derivations.
Every closure step is ordinary decimal arithmetic on folded pair sums.
"""
from exist_tile_horn import *
from creative_regular_invariant import qstep,bad,unfold,fold

def word_of(path,center):return (tuple(FE[k][1] for k in path),center)

def safety_word(allowed):
    aa=set(allowed);st,initial,edges,terms=trim(safety_graph());adj=defaultdict(list);end=defaultdict(list)
    for u,v,cost in edges:
        k=next(iter(cost))
        if k in aa:adj[u].append((v,k))
    for u,cost in terms:
        k=next(iter(cost))
        if k in aa:end[u].append(k)
    paths={u:[] for u in initial};todo=deque(initial)
    while todo:
        u=todo.popleft()
        if end[u]:
            k=end[u][0];x,c,extra,oc=TS[k-len(FE)];w=word_of(paths[u],c)
            assert set(history_path(w))<=aa and bad(qstep(w));return w
        for v,k in adj[u]:
            if v not in paths:paths[v]=paths[u]+[k];todo.append(v)
    return None

def closure_word(allowed):
    aa=set(allowed);states,edges,terms=composed_tiles();adj=defaultdict(list);end=defaultdict(list)
    for u,v,a,b in edges:
        if a in aa:adj[u].append((v,a,b))
    for u,a,extra,b in terms:
        if a in aa:end[u].append((a,extra,b))
    paths={(u,False):[] for u in range(4)};todo=deque(paths)
    while todo:
        u,broken=todo.popleft();path=paths[u,broken]
        for a,extra,b in end[u]:
            if broken or b not in aa or extra is not None and extra not in aa:
                x,c,e,oc=TS[a-len(FE)];w=word_of(path,c);out=qstep(w)
                assert set(history_path(w))<=aa and not set(history_path(out))<=aa
                return w,out
        for v,a,b in adj[u]:
            ns=(v,broken or b not in aa)
            if ns not in paths:paths[ns]=path+[a];todo.append(ns)
    return None

def derive(seed):
    allowed=set(history_path(seed));steps=[]
    while True:
        unsafe=safety_word(allowed)
        if unsafe is not None:return dict(seed=seed,steps=steps,unsafe=unsafe,unsafe_image=qstep(unsafe),final_tiles=sorted(allowed),status='obstruction',decimal_existence_proved=False)
        ce=closure_word(allowed)
        if ce is None:return dict(seed=seed,steps=steps,status='certificate',allowed_tiles=sorted(allowed),independent_check=path_and_check(allowed),decimal_existence_proved=True)
        w,out=ce;new=sorted(set(history_path(out))-allowed);assert new;steps.append(dict(input=w,image=out,new_tiles=new));allowed.update(new)
        if len(steps)>NW:raise AssertionError('strict tile growth exceeded universe')

def verify(c):
    def word(w):return tuple(w[0]),w[1]
    allowed=set(history_path(word(c['seed'])))
    for s in c['steps']:
        a,b=word(s['input']),word(s['image']);assert set(history_path(a))<=allowed;assert qstep(a)==b;new=set(history_path(b))-allowed;assert new==set(s['new_tiles']);allowed.update(new)
    assert c['status']=='obstruction';w=word(c['unsafe']);assert set(history_path(w))<=allowed;assert qstep(w)==word(c['unsafe_image']);assert bad(qstep(w));assert sorted(allowed)==c['final_tiles'];return True

if __name__=='__main__':
    for name,seed in [('196',((7,),18)),('18887',((8,16),16))]:
        c=derive(seed);assert verify(c);json.dump(c,open(f'exist_tile_derivation_{name}.json','w'),indent=2);print(name,c['status'],len(c['steps']),len(c['final_tiles']),c['unsafe'],flush=True)
