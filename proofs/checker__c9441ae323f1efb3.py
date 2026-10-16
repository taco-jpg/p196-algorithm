"""Exact all-length conditional-closure checker for integer carry-tile scores.

F(q)=offset+sum(history tile weights). Search for F(q)>=1,F(Gq)<=0.
Connected nonnegative integral source/sink flows are exactly finite accepted
walks, by the directed Euler-trail criterion. Necessary connectivity cuts
exclude detached cycles without any bound on edge multiplicity.
"""
from pathlib import Path
from collections import deque
from functools import lru_cache
from itertools import product
import sys,time,json
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
import persist_spacetime_weighted as m
import creative_regular_invariant as r
import z3
from bisimulation import quotient,lift

def reconstruct(edges,source,sink,multiplicity,weights,offset,start,result,context,max_witness):
    size=sum(multiplicity)
    if size>max_witness:
        result.update(status='UNKNOWN',reason='SAT walk exceeds reconstruction limit',trail_length=size)
        return result
    outgoing=[[] for _ in range(max(source,sink,max(max(e[0],e[1]) for e in edges))+1)]
    for j,e in enumerate(edges):outgoing[e[0]].append(j)
    remaining=multiplicity[:]
    adjacency=[[j for j in row if remaining[j]] for row in outgoing]
    stack=[(source,None)];reverse=[]
    while stack:
        u=stack[-1][0]
        while adjacency[u] and not remaining[adjacency[u][-1]]:adjacency[u].pop()
        if adjacency[u]:
            j=adjacency[u][-1];remaining[j]-=1;stack.append((edges[j][1],j))
        else:
            _,j=stack.pop()
            if j is not None:reverse.append(j)
    trail=reverse[::-1]
    assert len(trail)==size and not any(remaining)
    actual=lift(trail,edges,context)
    current=context['original_source'];pairs=[];center=None;ended=False
    for u,v,ic,oc,kind,label in actual:
        assert u==current and not ended;current=v
        if kind=='pair':pairs.append(label)
        if kind=='terminal':center=label;ended=True
    assert ended and current==context['original_sink']
    word=(tuple(pairs),center);assert r.valid(word)
    nxt=r.qstep(word);a=score(weights,offset,word);b=score(weights,offset,nxt)
    assert a>=1 and b<=0
    assert sum(multiplicity[j]*e[2] for j,e in enumerate(edges))==a
    assert sum(multiplicity[j]*e[3] for j,e in enumerate(edges))==b
    result.update(word=word,next_word=nxt,input_score=a,output_score=b,
                  trail_length=size,seconds=time.monotonic()-start)
    return result

def score(weights,offset,word):
    return offset+sum(weights[j] for j in m.history_path(word))

@lru_cache(maxsize=1)
def topology():
    g0=m.trim(m.closure_graph('0'));g1=m.trim(m.closure_graph('1'))
    states,initial,edges0,terms0=g0
    assert states==g1[0] and initial==g1[1]
    edges=[];terminals=[]
    for (u,v,nxt),(uu,vv,diff) in zip(edges0,g1[2]):
        assert (u,v)==(uu,vv)
        prev=m.add(nxt,{k:-a for k,a in diff.items()})
        assert len(prev)==1 and list(prev.values())==[1]
        k=next(iter(prev));assert k<len(m.FE)
        edges.append((u,v,k,nxt,'pair',m.FE[k][1]))
    for (u,nxt),(uu,diff) in zip(terms0,g1[3]):
        assert u==uu
        prev=m.add(nxt,{k:-a for k,a in diff.items()})
        assert len(prev)==1 and list(prev.values())==[1]
        k=next(iter(prev));assert k>=len(m.FE)
        terminals.append((u,k,nxt,m.TS[k-len(m.FE)][1]))
    return states,initial,edges,terminals

def check(weights,offset=0,seconds=30,max_witness=100000,save_smt=None,front_end=True):
    start=time.monotonic()
    assert len(weights)==m.NW and all(type(x)is int for x in weights)
    assert type(offset)is int
    # Concrete witnesses are useful; failure of this bounded front end has
    #no logical status. Only the unbounded formula may return UNSAT.
    for length in range(2 if front_end else 0):
        for pairs0 in product(range(19),repeat=length):
            if pairs0 and not pairs0[0]:continue
            for center0 in [None]+list(range(0,19,2)):
                word0=(pairs0,center0)
                if not r.valid(word0):continue
                a0=score(weights,offset,word0)
                if a0<1:continue
                next0=r.qstep(word0);b0=score(weights,offset,next0)
                if b0<=0:
                    return dict(status='SAT',method='independently evaluated concrete word',
                                word=word0,next_word=next0,input_score=a0,output_score=b0,
                                seconds=time.monotonic()-start)
    states,initial,pairs,terminals=topology()
    source=len(states);sink=source+1;n=sink+1
    edges=[(source,x,offset,offset,'start',None) for x in initial]
    edges += [(u,v,weights[k],sum(weights[j]*a for j,a in nxt.items()),kind,label)
              for u,v,k,nxt,kind,label in pairs]
    edges += [(u,sink,weights[k],sum(weights[j]*a for j,a in nxt.items()),'terminal',center)
              for u,k,nxt,center in terminals]
    # Equal endpoints and two scores may use one representative tile path.
    unique={}
    for e in edges:unique.setdefault(e[:4],e)
    edges=list(unique.values())
    original_states=n;original_edges=len(edges)
    n,source,sink,edges,context=quotient(n,source,sink,edges)
    from flow_front import discover
    try:
        found=discover(edges,n,source,sink,seconds=min(5,max(.01,seconds/3)))
    except (ArithmeticError,ValueError,TypeError):
        # Large exact coefficients may exceed the numerical front end's
        #representation. The exact unbounded checker still applies.
        found=None
    if found is not None:
        result=dict(status='SAT',method='exactly rechecked bounded MILP witness',
                    states=n,edges=len(edges),original_states=original_states,
                    original_edges=original_edges,bisimulation_rounds=context['rounds'])
        return reconstruct(edges,source,sink,found,weights,offset,start,result,context,max_witness)
    s=z3.SolverFor('QF_LIA')
    count=[z3.Int('flow_%d'%j) for j in range(len(edges))]
    incoming=[[] for _ in range(n)];outgoing=[[] for _ in range(n)]
    for j,(u,v,*_) in enumerate(edges):
        outgoing[u].append(j);incoming[v].append(j);s.add(count[j]>=0)
    for v in range(n):
        s.add(z3.Sum([count[j] for j in outgoing[v]])-
              z3.Sum([count[j] for j in incoming[v]])==
              (1 if v==source else -1 if v==sink else 0))
    s.add(z3.Sum([count[j]*e[2] for j,e in enumerate(edges) if e[2]])>=1)
    s.add(z3.Sum([count[j]*e[3] for j,e in enumerate(edges) if e[3]])<=0)
    if save_smt:Path(save_smt).write_text(s.to_smt2())
    cuts=set()
    while True:
        remaining=seconds-(time.monotonic()-start)
        if remaining<=0:
            return dict(status='UNKNOWN',reason='time budget',connectivity_cuts=len(cuts),seconds=time.monotonic()-start)
        s.set(timeout=max(1,int(remaining*1000)))
        status=s.check()
        result=dict(status=str(status).upper(),states=n,edges=len(edges),
                    original_states=original_states,original_edges=original_edges,
                    bisimulation_rounds=context['rounds'],connectivity_cuts=len(cuts),seconds=time.monotonic()-start)
        if status==z3.unknown:result['reason']=s.reason_unknown();return result
        if status==z3.unsat:
            if save_smt:Path(save_smt).write_text(s.to_smt2())
            return result
        model=s.model();multiplicity=[model.eval(x).as_long() for x in count]
        undirected=[set() for _ in range(n)];used=set()
        for amount,(u,v,*_) in zip(multiplicity,edges):
            if amount:undirected[u].add(v);undirected[v].add(u);used.update((u,v))
        components=[]
        while used:
            component={next(iter(used))};todo=list(component)
            while todo:
                for v in undirected[todo.pop()]:
                    if v not in component:component.add(v);todo.append(v)
            used.difference_update(component);components.append(component)
        disconnected=[part for part in components if source not in part]
        if not disconnected:break
        for part in disconnected:
            key=frozenset(part);assert key not in cuts;cuts.add(key)
            activity=[count[j]>0 for j,(u,v,*_) in enumerate(edges) if u in part or v in part]
            crossing=[count[j]>0 for j,(u,v,*_) in enumerate(edges) if (u in part)!=(v in part)]
            s.add(z3.Implies(z3.Or(activity),z3.Or(crossing)))
        if save_smt:Path(save_smt).write_text(s.to_smt2())
    return reconstruct(edges,source,sink,multiplicity,weights,offset,start,result,context,max_witness)

if __name__=='__main__':
    tests=[('constant zero',[0]*m.NW,0,'UNSAT'),
           ('constant positive',[0]*m.NW,1,'UNSAT'),
           ('one minus pair count',[-1]*len(m.FE)+[0]*len(m.TS),1,'SAT')]
    for label,w,b,expected in tests:
        result=check(w,b,45,front_end=False);print(json.dumps(dict(test=label,**result)),flush=True)
        assert result['status']==expected
