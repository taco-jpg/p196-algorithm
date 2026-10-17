#!/usr/bin/env python3
"""Agent #118: exact finite seven-column precursor/rank experiment, prefixes 5523/5524.

Finite computation, NOT a Lean certificate or a theorem about all decimal integers.
No third-party dependencies. The inverse enumeration here is an independently written
column-wise solver for the (unrestricted inner carry) relation used by Agent104/117.

Run: python3 -B verify_shared.py 5523 5524
Sanity baseline: python3 -B verify_shared.py 2641 --no-small-crosscheck
"""
from __future__ import annotations
from collections import Counter, defaultdict, deque
from itertools import product
from hashlib import sha256
import json, sys, time

K = 7


def full_forward(s):
    """Normalize the *complete* symmetric pair-sum word and mirror digits."""
    carry, d = 0, []
    for v in s:
        u = v + carry
        d.append(u % 10)
        carry = u // 10
    if carry:
        d.append(carry)
    return tuple(d[i] + d[-1-i] for i in range(len(d)))


def prefix_forward(s):
    """Two exact output k-prefix possibilities indexed by inner carry e=0/1."""
    k = len(s)
    carry, low = 0, []
    for v in s:
        u = v + carry
        low.append(u % 10)
        carry = u // 10
    ans = set()
    for e in (0, 1):
        carry = e
        high = [0] * k
        for i in range(k-1, -1, -1):
            u = s[i] + carry
            high[i] = u % 10
            carry = u // 10
        if carry:
            ans.add((1+low[0],) + tuple(low[i] + high[i-1] for i in range(1,k)))
        else:
            ans.add(tuple(low[i] + high[i] for i in range(k)))
    return ans


def sources_short(k):
    """Every positive symmetric pair word of width <k, with even odd center."""
    for n in range(1,k):
        if n == 1:
            for mid in range(2,19,2):
                yield (mid,)
            continue
        half = n // 2
        for lead in range(1, 19):
            for rest in product(range(19), repeat=half-1):
                left = (lead,) + rest
                if n % 2 == 0:
                    yield left + left[::-1]
                else:
                    for mid in range(0, 19, 2):
                        yield left + (mid,) + left[::-1]


def initial_words(prefix,k):
    head = tuple(int(c) for c in prefix)
    assert 3 <= len(head) <= k and 1 <= head[0] <= 9 and all(0 <= c <= 9 for c in head)
    long = {head + t for t in product(range(10), repeat=k-len(head))}
    short = set()
    for n in range(len(head),k):
        for half in product(range(10),repeat=(n+1)//2):
            pal = half + half[:n//2][::-1]
            if pal[:len(head)] == head and (n%2 == 0 or pal[n//2]%2 == 0):
                short.add(pal)
    return long, short


class Predecessors:
    """Complete inverse via 4 carry-state digit arithmetic; no candidate heuristics."""
    def __init__(self,k):
        self.k=k
        self.ng={}
        for v in range(19):
            for x in (0,1):
                for yin in (0,1):
                    self.ng[v,x,yin]=tuple(
                        (s,(s+x)//10,(s+yin)//10) for s in range(19)
                        if ((s+x)%10+(s+yin)%10)==v)
        self.cache={}

    def get(self,p):
        if any(v < 0 or v > 18 for v in p):
            return frozenset()
        if p in self.cache:
            return self.cache[p]
        k=self.k
        ng={((),0,0)}
        for i,v in enumerate(p):
            new=set()
            for word,x,needed in ng:
                for yin in (0,1):
                    for s,xout,yout in self.ng[v,x,yin]:
                        if i == 0 and s == 0:
                            continue
                        if yout != needed:
                            continue
                        new.add((word+(s,),xout,yin))
            ng=new
        preds={w for w,_,_ in ng}
        # Carry out of outermost high scan = 1, so normalized width grows.
        if 1 <= p[0] <= 10:
            for xout in (0,1):
                s0=p[0]-1+10*xout
                if not 1 <= s0 <= 18:
                    continue
                g={((s0,),xout,yin) for yin in (0,1) if (s0+yin)//10==1}
                for i in range(1,k):
                    new=set()
                    for word,x,y_prev in g:
                        hi_prev=(word[-1]+y_prev)%10
                        low=p[i]-hi_prev
                        if not 0 <= low <= 9:
                            continue
                        for xout in (0,1):
                            s=low+10*xout-x
                            if not 0 <= s <= 18:
                                continue
                            for yin in (0,1):
                                if (s+yin)//10==y_prev:
                                    new.add((word+(s,),xout,yin))
                    g=new
                preds.update(w for w,_,_ in g)
        out=frozenset(preds)
        self.cache[p]=out
        return out


def small_crosscheck():
    """Complete independent *forward* enumeration for k=3/4, then invert selected outputs."""
    t=time.monotonic()
    out={}
    for k in (3,4):
        inverse=Predecessors(k)
        index=defaultdict(set)
        for lead in range(1,19):
            for rest in product(range(19),repeat=k-1):
                s=(lead,)+rest
                for p in prefix_forward(s):
                    index[p].add(s)
        keys=sorted(index)
        test=keys if k==3 else keys[::max(1,len(keys)//120)]
        for p in test:
            got=set(inverse.get(p))
            assert got==index[p], ("inverse-incomplete-or-unsound",k,p,len(got),len(index[p]), list(got ^ index[p])[:3])
        for p in [(19,)*k, (0,)*k, (18,)*k, (5,)*k]:
            assert set(inverse.get(p)) == index.get(p,set()), ("negative-target",k,p)
        out[str(k)]={"source_rows":18*(19**(k-1)),"distinct_outputs":len(keys),"inverses_compared":len(test)+4}
    out["runtime_seconds"]=round(time.monotonic()-t,3)
    return out


def certify(prefixes, cap=700_000):
    t0=time.monotonic()
    init={}
    for p in prefixes:
        long,short=initial_words(p,K)
        init[p]={"long":long,"short":short,"all":long|short}
    roots=set().union(*(v["all"] for v in init.values()))
    pred=Predecessors(K)
    short_inverse=defaultdict(set)
    all_short=list(sources_short(K))
    assert len(all_short)==10467,("short-source-count",len(all_short))
    for s in all_short:
        short_inverse[full_forward(s)].add(s)
    # Exhaustive directed ancestor closure of all selected initial targets.
    visited=set(roots)
    todo=list(roots)
    edges={}
    succ=defaultdict(list)
    checked_long=checked_short=0
    while todo:
        p=todo.pop()
        q=set(short_inverse.get(p,()))
        if len(p)==K:
            q.update(pred.get(p))
        edges[p]=q
        for s in q:
            if len(s)==K:
                assert p in prefix_forward(s),("invalid-long-edge",s,p)
                checked_long+=1
            else:
                assert full_forward(s)==p,("invalid-short-edge",s,p)
                checked_short+=1
            succ[s].append(p)
            if s not in visited:
                visited.add(s)
                todo.append(s)
                if len(visited)>cap:
                    raise RuntimeError("CAP, incomplete finite search: %s"%len(visited))
    degrees={p:len(edges[p]) for p in visited}
    queue=deque(p for p in visited if degrees[p]==0)
    rank={p:0 for p in queue}
    while queue:
        q=queue.popleft()
        for p in succ[q]:
            degrees[p]-=1
            if degrees[p]==0:
                rank[p]=1+max(rank[s] for s in edges[p])
                queue.append(p)
    if len(rank)!=len(visited):
        return {"status":"UNRANKED","ranked":len(rank),"visited":len(visited)}
    assert all(rank[p]==(1+max(rank[s] for s in qs) if qs else 0) for p,qs in edges.items())
    assert all(rank[s]<rank[p] for p,qs in edges.items() for s in qs)
    # Separate full closures, using the joint graph as a read-only independent check.
    individually={}
    for p,v in init.items():
        closure=set(v["all"])
        todo=list(closure)
        while todo:
            w=todo.pop()
            for s in edges[w]:
                if s not in closure:
                    closure.add(s)
                    todo.append(s)
        individually[p]=closure
    shared_overlap=set.intersection(*individually.values()) if len(individually)>1 else set()
    h=sha256()
    for p in sorted(visited):
        h.update(",".join(map(str,p)).encode("ascii"))
        h.update(b":")
        h.update(str(rank[p]).encode("ascii"))
        h.update(b"\n")
    summary={"task":"agent118-k7-double-prefix-5523-5524-20261016",
      "status":"ACYCLIC","evidence":"CHECKED FINITE COMPUTATION; NOT LEAN-CHECKED",
      "k":K,"prefixes":list(prefixes),"initial_union":len(roots),
      "short_sources_exhaustively_enumerated":len(all_short),
      "closure_total":len(visited),"closure_long":sum(len(x)==K for x in visited),
      "closure_short":sum(len(x)<K for x in visited),
      "all_edges":checked_long+checked_short,"long_edges":checked_long,"short_edges":checked_short,
      "rank_max_entire_graph":max(rank.values()),
      "rank_distribution":dict(sorted(Counter(rank.values()).items())),
      "shared_overlap_nodes":len(shared_overlap),
      "ranked_rows_sha256":h.hexdigest(),
      "by_prefix":{p:{"initial_long":len(v["long"]),"initial_short":len(v["short"]),
       "closure_nodes":len(individually[p]),"initial_max_rank":max(rank[x] for x in v["all"]),
       "method_bound":1+max(rank[x] for x in v["all"])} for p,v in init.items()},
      "runtime_seconds":round(time.monotonic()-t0,3)}
    return summary


def main():
    prefixes=tuple(x for x in sys.argv[1:] if not x.startswith("--")) or ("5523","5524")
    start=time.monotonic()
    if "--no-small-crosscheck" not in sys.argv:
        print("SMALL_EXACT_CROSSCHECK",json.dumps(small_crosscheck(),sort_keys=True),flush=True)
    result=certify(prefixes)
    print(json.dumps(result,indent=2,sort_keys=True),flush=True)
    print("TOTAL_RUNTIME_S",round(time.monotonic()-start,3))
    if result["status"]!="ACYCLIC": sys.exit(1)

if __name__=="__main__": main()
