"""Exact all-length closure for bounded spatial carry-tile contexts.

context=1 is the archived allowed-tile language. context>=2 retains adjacent
tile correlations and an explicit beginning-of-word sentinel. A graph cap is
UNKNOWN, never a rejected grammar. A safe fixed point is only a candidate
until the underlying arithmetic transducer receives an independent audit.
"""
from collections import deque, defaultdict
from pathlib import Path
import sys, json, time, argparse
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'research'))
from persist_spacetime_weighted import OUT, TERMS, history_path, advance, terminal_bad

TERM_OUT=defaultdict(list)
for (x,c),(extra,oc,k) in TERMS.items():
    TERM_OUT[x].append((c,extra,oc,k))


def move(ctx,k):
    return (ctx+(k,))[1:] if ctx else ()


def features(path,order):
    ctx=(-1,)*(order-1);result=set()
    for k in path:
        result.add(ctx+(k,));ctx=move(ctx,k)
    return result


def safety(allowed,order,cap):
    ctx=(-1,)*(order-1)
    seen={(x,ctx,(True,True,False)) for x in (0,1)};todo=deque(seen)
    while todo:
        x,ca,flags=todo.popleft()
        for c,extra,oc,k in TERM_OUT[x]:
            if ca+(k,) not in allowed:continue
            ff=flags if extra is None else advance(flags,extra)
            if terminal_bad(ff,oc):return False,len(seen)
        for q,o,y,k in OUT[x]:
            if ca+(k,) not in allowed:continue
            ff=advance(flags,o)
            if not (ff[0] or ff[1]):continue
            st=(y,move(ca,k),ff)
            if st not in seen:
                if len(seen)>=cap:return None,len(seen)
                seen.add(st);todo.append(st)
    return True,len(seen)


def image_features(allowed,order,cap):
    ctx=(-1,)*(order-1)
    states=[(x,y,ctx,ctx) for x in (0,1) for y in (0,1)]
    ids={s:i for i,s in enumerate(states)}
    incoming=defaultdict(list);edges=[];terminal=[]
    for x,y,ca,cb in states:
        u=ids[x,y,ca,cb]
        for c,extra,oc,a in TERM_OUT[x]:
            if ca+(a,) not in allowed:continue
            if extra is None:
                if (y,oc) in TERMS:
                    b=TERMS[y,oc][2]
                    terminal.append((u,(cb+(b,),)))
            else:
                for q2,o2,yy,b in OUT[y]:
                    if q2==extra and (yy,oc) in TERMS:
                        bb=TERMS[yy,oc][2]
                        terminal.append((u,(cb+(b,),move(cb,b)+(bb,))))
        for q,o,xx,a in OUT[x]:
            if ca+(a,) not in allowed:continue
            for q2,o2,yy,b in OUT[y]:
                if q2!=o:continue
                st=(xx,yy,move(ca,a),move(cb,b))
                if st not in ids:
                    if len(states)>=cap:return None,len(states)
                    ids[st]=len(states);states.append(st)
                v=ids[st];f=cb+(b,)
                edges.append((u,v,f));incoming[v].append(u)
    live={u for u,fs in terminal};todo=deque(live)
    while todo:
        for u in incoming[todo.popleft()]:
            if u not in live:live.add(u);todo.append(u)
    result={f for u,v,f in edges if v in live}
    for u,fs in terminal:result.update(fs)
    return result,len(states)


def closure(word,order=2,cap=1000000,seconds=300):
    allowed=features(history_path(word),order)
    sizes=[];max_graph=0;start=time.monotonic()
    while time.monotonic()-start<seconds:
        sizes.append(len(allowed))
        safe,nst=safety(allowed,order,cap);max_graph=max(max_graph,nst)
        if safe is False:
            return dict(status='unsafe_template',word=word,context=order,sizes=sizes,max_graph=max_graph)
        if safe is None:
            return dict(status='unknown',reason='safety graph cap',word=word,context=order,sizes=sizes)
        fs,nst=image_features(allowed,order,cap);max_graph=max(max_graph,nst)
        if fs is None:
            return dict(status='unknown',reason='closure graph cap',word=word,context=order,sizes=sizes,max_graph=max_graph)
        new=allowed|fs
        if new==allowed:
            return dict(status='candidate',word=word,context=order,sizes=sizes,max_graph=max_graph,
                        allowed_features=sorted(allowed))
        allowed=new
    return dict(status='unknown',reason='wall-clock budget',word=word,context=order,sizes=sizes,max_graph=max_graph)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--context',type=int,default=2)
    p.add_argument('--seed',type=int,default=196);p.add_argument('--seconds',type=float,default=300)
    p.add_argument('--cap',type=int,default=1000000);args=p.parse_args()
    s=str(args.seed);q=[int(a)+int(b) for a,b in zip(s,s[::-1])]
    w=(tuple(q[:len(q)//2]),q[len(q)//2] if len(q)%2 else None)
    st=time.monotonic();out=closure(w,args.context,args.cap,args.seconds);out['seconds']=time.monotonic()-st
    path=Path(__file__).with_name(f'context_{args.context}_seed_{args.seed}.json')
    path.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='allowed_features'},indent=2),flush=True)
