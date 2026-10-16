"""Finite certificates excluding arbitrary time-dependent one-tile languages.

No clock periodicity is assumed. Every forced output tile is justified by an
explicit accepted input word and exact reverse-and-add arithmetic. Checking
the certificate needs no SAT solver and no induction over unbounded words.
"""
from exist_tile_derivation import *

def output_tiles(allowed):
    aa=set(allowed);states,edges,terms=composed_tiles();adj=defaultdict(list);rev=defaultdict(list);end=defaultdict(list)
    for u,v,a,b in edges:
        if a in aa:adj[u].append((v,a,b));rev[v].append((u,a,b))
    for u,a,extra,b in terms:
        if a in aa:end[u].append((a,extra,b))
    fw={i:[] for i in range(4)};todo=deque(fw)
    while todo:
        u=todo.popleft()
        for v,a,b in adj[u]:
            if v not in fw:fw[v]=fw[u]+[a];todo.append(v)
    bw={u:([end[u][0][0]],end[u][0]) for u in end};todo=deque(bw)
    while todo:
        v=todo.popleft()
        for u,a,b in rev[v]:
            if u not in bw:bw[u]=([a]+bw[v][0],bw[v][1]);todo.append(u)
    witnesses={}
    def add(path,outputs):
        terminal=path[-1];x,c,e,oc=TS[terminal-len(FE)];w=word_of(path[:-1],c);img=qstep(w);hp=set(history_path(img));assert set(path)<=aa
        for k in outputs:
            assert k in hp
            if k not in witnesses:witnesses[k]=(w,img)
    for u,v,a,b in edges:
        if u in fw and v in bw and a in aa and b not in witnesses:add(fw[u]+[a]+bw[v][0],[b])
    for u,a,extra,b in terms:
        if u in fw and a in aa:add(fw[u]+[a],[b] if extra is None else [extra,b])
    return witnesses

def derive(seed,limit=100):
    aa=set(history_path(seed));levels=[]
    for t in range(limit):
        w=safety_word(aa)
        if w is not None:return dict(seed=seed,levels=levels,unsafe_time=t,unsafe=w,unsafe_image=qstep(w),status='obstruction',arbitrary_time_dependent_tile_grammar_excluded=True,decimal_existence_proved=False)
        ws=output_tiles(aa);rows=[dict(tile=k,input=w,image=im) for k,(w,im) in sorted(ws.items())];levels.append(rows);aa=set(ws)
    return dict(seed=seed,levels=levels,status='incomplete',decimal_existence_proved=False)

def verify(c):
    def w(a):return tuple(a[0]),a[1]
    aa=set(history_path(w(c['seed'])))
    for rows in c['levels']:
        bb=set()
        for row in rows:
            inp,img=w(row['input']),w(row['image']);assert set(history_path(inp))<=aa;assert qstep(inp)==img;assert row['tile'] in history_path(img);bb.add(row['tile'])
        aa=bb
    assert set(history_path(w(c['unsafe'])))<=aa;assert qstep(w(c['unsafe']))==w(c['unsafe_image']);assert bad(w(c['unsafe_image']));assert c['unsafe_time']==len(c['levels']);return True

if __name__=='__main__':
    for name,seed in [('196',((7,),18)),('18887',((8,16),16))]:
        cc=derive(seed);assert cc['status']=='obstruction';assert verify(cc);json.dump(cc,open(f'exist_tile_timevarying_{name}.json','w'),indent=2);print(name,cc['unsafe_time'],[len(x) for x in cc['levels']],cc['unsafe'],flush=True)
