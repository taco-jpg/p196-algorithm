"""Exact spatial-column reachability for a 24-step alternating exterior.

This eliminates guessed high carries using the N/O pair equations.  A graph
state records twelve pairs of low carries, the N high carry, and the preceding
O coefficient minus ten times its high carry.  Bounds yield UNKNOWN only.
"""
from pathlib import Path
from collections import deque
import sys,time,json,argparse
ROOT=Path(__file__).resolve().parents[2];sys.path.insert(0,str(ROOT/'research'))
from astra_substitution_gluing import trace
from astra_substitution_enumerate import transition


def successors(state):
    aa,bb,cc,zz=state;out={}
    def walk(j,Q,Q0,an,ao,bn,zs,qs,rs):
        if j==12:
            if Q==Q0:out.setdefault((tuple(an),tuple(ao),tuple(bn),tuple(zs)),tuple(v for p in zip(qs,rs)for v in p))
            return
        a,b,c,z=aa[j],bb[j],cc[j],zz[j]
        for nc in (0,1):
            if (Q+nc)//10!=c:continue
            R=(Q+a)%10+Q+nc-10*c
            if not 0<=R<=18:continue
            for oc in (0,1):
                if R<9 and oc!=0 or R>9 and oc!=1:continue
                if z==-1 and oc!=1 or z==9 and oc!=0:continue
                nxt=(R+b)%10+z+oc
                if not 0<=nxt<=18:continue
                walk(j+1,nxt,Q0,an+[(Q+a)//10],ao+[(R+b)//10],bn+[nc],zs+[R-10*oc],qs+[Q],rs+[R])
    for q in range(19):walk(0,q,q,[],[],[],[],[],[])
    return out


def bulk_state(B):
    bt=trace(tuple(B))
    return (tuple(bt[t]['A'][0]for t in range(0,24,2)),tuple(bt[t]['A'][0]for t in range(1,24,2)),
            tuple(bt[t]['R'][0]for t in range(0,24,2)),tuple(bt[t]['q'][-1]-10*bt[t]['R'][-1]for t in range(1,24,2)))


def initial():return ((0,)*12,(1,)*12,(1,)*12,(7,)*12)


def search(seconds=120,cap=200000):
    begin=time.monotonic();deadline=begin+seconds
    base=(5,2,5);targets={bulk_state(base[r:]+base[:r]):base[r:]+base[:r]for r in range(3)}
    root=initial();parent={root:None};todo=deque([(root,1)]);done=0;edges=0;last_depth=0
    here=Path(__file__).resolve().parent;status='unknown';reason='time budget';candidate=None
    while todo and time.monotonic()<deadline:
        state,depth=todo.popleft()
        if depth!=last_depth:
            last_depth=depth;print(json.dumps(dict(depth=depth,retained_states=len(parent),expanded=done,queue=len(todo),seconds=time.monotonic()-begin)),flush=True)
        if state in targets:
            B=targets[state];columns=[];cur=state
            while parent[cur] is not None:
                prev,row=parent[cur];columns.append(row);cur=prev
            columns.reverse();columns=[tuple(8 if t%2==0 else 17 for t in range(24))]+columns
            rows=[tuple(col[t]for col in columns)for t in range(24)];bt=trace(B)
            for t in range(24):assert transition('exterior',rows[t],bt,t)==rows[(t+1)%24]
            candidate=dict(bulk=B,width=len(columns),rows=rows,integer_column_replay=True)
            status='positive_exterior_component';reason=None;break
        out=successors(state);done+=1;edges+=len(out)
        for new,row in out.items():
            if new not in parent:
                if len(parent)>=cap:
                    reason='state cap';break
                parent[new]=(state,row);todo.append((new,depth+1))
        if reason=='state cap':break
    else:
        if not todo:status='closed_reachable_graph_no_exterior';reason=None
    result=dict(status=status,reason=reason,seconds=time.monotonic()-begin,state_cap=cap,retained_states=len(parent),expanded_states=done,edges=edges,last_depth=last_depth,candidate=candidate,finite_seed_proved=False)
    if status=='closed_reachable_graph_no_exterior':
        (here/'exterior_columns_closed_states.json').write_text(json.dumps(list(parent),separators=(',',':'))+'\n')
    (here/'exterior_columns_result.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--seconds',type=float,default=120);p.add_argument('--cap',type=int,default=200000);args=p.parse_args()
    search(args.seconds,args.cap)
