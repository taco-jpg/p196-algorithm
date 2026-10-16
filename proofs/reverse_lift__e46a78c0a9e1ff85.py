"""Targeted temporal-period lift: (0000111)^4 and its period-three tails.

Searches spatial predecessors of all40 exact returning tails. A C4 temporal
rotation quotient is sound because the outer boundary is7-periodic and the
complete target set is invariant. Caps/time limits remain UNKNOWN.
"""
from pathlib import Path
from collections import deque
import json,time,argparse
from columns import bulk_state,initial,check_edge,successors
HERE=Path(__file__).resolve().parent


def rotate(state,k):
    a,b,z=state
    return (a[7*k:]+a[:7*k],b[4*k:]+b[:4*k],z[3*k:]+z[:3*k])


def canonical(state):return min(rotate(state,k)for k in range(4))


def predecessors(new,clock,limit=1000000):
    na,nb,nz=new;p=len(clock);j=k=0;opts=[]
    for t,h in enumerate(clock):
        choices=[]
        for q in range(19):
            for a in (0,1):
                if (q+a)//10!=na[t]:continue
                lo=(q+a)%10
                if h:
                    for incoming in (0,1):
                        high=(q+incoming)//10
                        if q-10*high==nz[k]:
                            item=(q,a,None,high,lo)
                            if item not in choices:choices.append(item)
                else:
                    high=(q+nb[j])//10
                    r=lo+(q+nb[j])%10
                    choices.append((q,a,high,None,r))
        opts.append(choices)
        if h:k+=1
        else:j+=1
    out={};truncated=False;generated=0
    def compatible(t,x,y):
        if clock[t]:
            z=y[0]-x[4]-x[3]
            if 0<=z+x[3]<=9 and -1<=z<=9:return z
            return None
        return 0 if x[4]==y[0] else None
    def visit(path,zs):
        nonlocal truncated,generated
        if truncated:return
        t=len(path)
        if t==p:
            z=compatible(p-1,path[-1],path[0])
            if z is None:return
            old=(tuple(x[1]for x in path),tuple(x[2]for x,h in zip(path,clock)if not h),
                 tuple(zs+([z]if clock[-1]else[])))
            col=tuple(x[0]for x in path)
            out.setdefault(old,col);generated+=1
            if len(out)>=limit:truncated=True
            return
        for x in opts[t]:
            if not path:visit([x],[])
            else:
                z=compatible(t-1,path[-1],x)
                if z is not None:visit(path+[x],zs+([z]if clock[t-1]else[]))
            if truncated:break
    if all(opts):visit([],[])
    return out,truncated,[len(x)for x in opts]


def run(seconds=30,cap=100000,edgecap=100000,viable=False,new_only=False):
    data=json.loads((HERE/'clock28_0_bulk.json').read_text())
    clock=data['clock'];outer=(1,2,4,9,18,9,10)*4
    motifs=data['motifs']
    if new_only:
        old=json.loads((HERE/'clock14_bulk.json').read_text())[0]['returning_period3']
        motifs=[B for B in motifs if B not in old]
    targets={bulk_state(B,clock)for B in motifs}
    assert all(rotate(s,k)in targets for s in targets for k in range(4))
    target_orbits={canonical(s)for s in targets};root=canonical(initial(outer,clock))
    retained=set(target_orbits);todo=deque(target_orbits)
    began=time.monotonic();done=edges=rawedges=0;dead=0;alive_cache={s:True for s in retained};status='UNKNOWN';reason='time limit'
    while todo and time.monotonic()-began<seconds:
        state=todo.popleft()
        if state==root:status='ROOT_REACHED_RECONSTRUCTION_REQUIRED';reason=None;break
        prev,truncated,_=predecessors(state,clock,edgecap)
        if truncated:reason='per-state predecessor cap';break
        done+=1;rawedges+=len(prev)
        for old,col in prev.items():check_edge(old,state,col,clock)
        orbitprev={canonical(old)for old in prev};edges+=len(orbitprev)
        for old in orbitprev:
            if old in retained:continue
            if viable and old!=root:
                if old not in alive_cache:
                    witness,_,_=predecessors(old,clock,1)
                    alive_cache[old]=bool(witness)
                    if not witness:dead+=1
                if not alive_cache[old]:continue
            retained.add(old);todo.append(old)
        if len(retained)>=cap:reason='state cap';break
        if done%100==0:print(json.dumps(dict(expanded=done,states=len(retained),rawedges=rawedges,dead_pruned=dead,seconds=time.monotonic()-began)),flush=True)
    if not todo and status=='UNKNOWN':status='COMPLETE_TARGET_PREDECESSOR_CLOSURE_ROOT_ABSENT';reason=None
    result=dict(status=status,reason=reason,clock=clock,outer=outer,targets=len(targets),target_orbits=len(target_orbits),
                expanded=done,states=len(retained),edges=edges,rawedges=rawedges,seconds=time.monotonic()-began,
                queue=len(todo),viability_filter=viable,new_tails_only=new_only,dead_pruned=dead,
                finite_exterior_supplied=False,decimal_existence_proved=False)
    stem='reverse28_0_viable'if viable else'reverse28_0'
    if new_only:stem+='_new'
    if status.startswith('COMPLETE'):
        (HERE/f'{stem}_closed.json').write_text(json.dumps(list(retained),separators=(',',':'))+'\n')
    (HERE/f'{stem}.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seconds',type=float,default=30)
    p.add_argument('--cap',type=int,default=100000);p.add_argument('--edgecap',type=int,default=100000)
    p.add_argument('--viable',action='store_true')
    p.add_argument('--new-only',action='store_true')
    a=p.parse_args();run(a.seconds,a.cap,a.edgecap,a.viable,a.new_only)
