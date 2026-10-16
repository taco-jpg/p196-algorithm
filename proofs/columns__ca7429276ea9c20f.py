"""Exact spatial transfer for an arbitrary fixed overflow clock.

At cut i, A is the low carry entering column i in every phase; B is the
high carry leaving column i in N phases; Z=q[i-1]-10*high[i-1] in O phases.
The delayed high digit is Z+high[i]. This eliminates unneeded high-carry
coordinates at overflow phases, while retaining their consistency bounds.
"""
from pathlib import Path
import json,time,argparse,sys
from collections import deque
HERE=Path(__file__).resolve().parent


def bulk_trace(B,clock):
    """Standard-library periodic carry normalization, with a non-nine reset."""
    q=tuple(B);out=[];n=len(q)
    for h in clock:
        assert any(v!=9 for v in q)
        A=[0]*n;R=[0]*n;c=0
        for _ in range(2):
            for i in range(n):A[i]=c;c=(q[i]+c)//10
        c=0
        for _ in range(2):
            for i in reversed(range(n)):c=(q[i]+c)//10;R[i]=c
        assert all(A[(i+1)%n]==(q[i]+A[i])//10 for i in range(n))
        assert all(R[i]==(q[i]+R[(i+1)%n])//10 for i in range(n))
        lo=[(q[i]+A[i])%10 for i in range(n)]
        hi=[(q[i]+R[(i+1)%n])%10 for i in range(n)]
        out.append(dict(q=q,A=A,R=R,lo=lo,hi=hi))
        q=tuple(lo[i]+hi[(i-h)%n]for i in range(n))
    assert q==tuple(B)
    return out


def initial(outer,clock):
    p=len(clock);aa=[];bb=[];zz=[]
    for t,h in enumerate(clock):
        q=outer[t];r=outer[(t+1)%p]
        aa.append(q//10)
        if h:
            assert r==q%10+1
            zz.append(q-10)
        else:
            c=r-2*q
            assert c in (0,1) and (q+c)//10==0
            bb.append(c)
    return tuple(aa),tuple(bb),tuple(zz)


def bulk_state(B,clock):
    bt=bulk_trace(B,clock)
    return (tuple(b['A'][0]for b in bt),
            tuple(b['R'][0]for b,h in zip(bt,clock)if not h),
            tuple(b['q'][-1]-10*b['R'][-1]for b,h in zip(bt,clock)if h))


def successors(state,clock):
    aa,bb,zz=state;p=len(clock);oldb={};oldz={}
    j=k=0
    for t,h in enumerate(clock):
        if h:oldz[t]=zz[k];k+=1
        else:oldb[t]=bb[j];j+=1
    out={}
    def visit(t,q,q0,an,bn,zn,qs):
        if t==p:
            if q==q0:out.setdefault((tuple(an),tuple(bn),tuple(zn)),tuple(qs))
            return
        a=aa[t];lo=(q+a)%10;na=(q+a)//10
        if clock[t]:
            z=oldz[t]
            for b in (0,1):
                if q<9 and b or q>9 and not b:continue
                if z==-1 and not b or z==9 and b:continue
                r=lo+z+b
                if 0<=r<=18:visit(t+1,r,q0,an+[na],bn,zn+[q-10*b],qs+[q])
        else:
            b=oldb[t]
            for c in (0,1):
                if (q+c)//10!=b:continue
                r=lo+(q+c)%10
                visit(t+1,r,q0,an+[na],bn+[c],zn,qs+[q])
    for q in range(19):visit(0,q,q,[],[],[],[])
    return out


def check_edge(old,new,column,clock):
    a,b,z=old;na,nb,nz=new;j=k=0;p=len(clock)
    for t,h in enumerate(clock):
        q=column[t];r=column[(t+1)%p]
        assert na[t]==(q+a[t])//10
        if h:
            high=(q-nz[k])//10
            assert high in (0,1) and q-10*high==nz[k]
            assert not(q<9 and high or q>9 and not high)
            assert not(z[k]==-1 and not high or z[k]==9 and high)
            assert r==(q+a[t])%10+z[k]+high
            k+=1
        else:
            assert (q+nb[j])//10==b[j]
            assert r==(q+a[t])%10+(q+nb[j])%10
            j+=1


def run(index=1,seconds=30,cap=200000,repeat=1):
    row=json.loads((HERE/'clock14_bulk.json').read_text())[index]
    clock=row['overflow']*repeat;outer=row['clock']*repeat
    # All old motifs are retained as targets. For lifted clocks additional
    # motifs may occur; absence of these targets alone is not an exclusion
    # of the omitted motifs. A completely acyclic closed graph is stronger.
    motifs=row['returning_period3']
    if index==0 and repeat==2 and (HERE/'clock28_0_bulk.json').exists():
        lifted=json.loads((HERE/'clock28_0_bulk.json').read_text())
        assert lifted['clock']==clock
        motifs=lifted['motifs']
    targets={bulk_state(B,clock):B for B in motifs}
    start=initial(outer,clock);parent={start:None};todo=deque([(start,1)])
    began=time.monotonic();done=edges=0;depth=0;answer=None;status='UNKNOWN'
    while todo and time.monotonic()-began<seconds:
        state,d=todo.popleft()
        if d!=depth:
            depth=d;print(json.dumps(dict(depth=depth,states=len(parent),expanded=done)),flush=True)
        if state in targets:
            columns=[];s=state
            while parent[s] is not None:
                prev,col=parent[s];columns.append(col);s=prev
            columns.reverse();columns=[tuple(outer)]+columns
            answer=dict(bulk=targets[state],rows=list(map(list,zip(*columns))),width=len(columns))
            status='FOUND_EXTERIOR_COMPONENT';break
        out=successors(state,clock);done+=1;edges+=len(out)
        for ns,col in out.items():
            check_edge(state,ns,col,clock)
            if ns not in parent:
                parent[ns]=(state,col);todo.append((ns,d+1))
        if len(parent)>=cap:break
    if not todo and answer is None:status='COMPLETE_NO_EXTERIOR_TO_TARGET_BULKS'
    reason=None if status!='UNKNOWN'else('state cap'if len(parent)>=cap else'time limit')
    result=dict(status=status,reason=reason,clock_index=index,temporal_repeat=repeat,clock=clock,outer=outer,
                seconds=time.monotonic()-began,states=len(parent),expanded=done,targets=len(targets),
                edges=edges,last_depth=depth,cap=cap,queue=len(todo),candidate=answer,
                finite_decimal_witness_supplied=False,decimal_existence_proved=False)
    stem=f'columns{14*repeat}_{index}'
    if status.startswith('COMPLETE'):
        (HERE/f'{stem}_closed.json').write_text(json.dumps(list(parent),separators=(',',':'))+'\n')
    (HERE/f'{stem}.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result),flush=True)
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--clock-index',type=int,default=1)
    p.add_argument('--seconds',type=float,default=30);p.add_argument('--cap',type=int,default=200000)
    p.add_argument('--repeat',type=int,default=1)
    a=p.parse_args();run(a.clock_index,a.seconds,a.cap,a.repeat)
