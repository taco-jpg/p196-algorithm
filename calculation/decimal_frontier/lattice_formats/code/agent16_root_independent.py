#!/usr/bin/env python3
"""Independent brute-force canonical-root graph and SCC checker.
Checks exact whole graphs for every rotation of g=101100 and bases 4,5,6,
using all 2^6 time-carry assignments instead of the C++ time-path DFS.
"""
import argparse, itertools, json, subprocess
from collections import deque

G='101100'

def rotate(s,k):return s[k:]+s[:k]

def edge_candidates(base,g,state,first):
    L,H,Y=state
    p=len(g)
    ts=[i for i,x in enumerate(g) if x=='1']
    yy=dict(zip(ts,Y))
    for x0 in range(int(first),2*base-1):
        for cs in itertools.product((0,1),repeat=p):
            x=x0;xs=[]
            for t,bit in enumerate(g):
                if not 0<=x<=2*base-2 or (x+cs[t])//base!=H[t]:break
                xs.append(x)
                x=(x+L[t])%base + (yy[t] if bit=='1' else (x+cs[t])%base)
            else:
                if x!=x0:continue
                z=(tuple((xs[t]+L[t])//base for t in range(p)),
                   tuple(cs),tuple((xs[t]+cs[t])%base for t in ts))
                yield z,(xs,cs)

def independent_graph(base,g):
    root=(tuple(0 for _ in g),tuple(int(z) for z in g),tuple(1 for z in g if z=='1'))
    depth={root:0};q=deque([root]);adj={}
    while q:
        s=q.popleft()
        edges={z for z,_ in edge_candidates(base,g,s,s==root)}
        adj[s]=edges
        for z in edges:
            if z not in depth:depth[z]=depth[s]+1;q.append(z)
    return adj,depth

def components(adj):
    order=[];seen=set()
    for r in adj:
        if r in seen:continue
        todo=[(r,False)]
        while todo:
            v,done=todo.pop()
            if done:order.append(v);continue
            if v in seen:continue
            seen.add(v);todo.append((v,True))
            todo.extend((w,False) for w in adj[v] if w not in seen)
    rev={v:set() for v in adj}
    for v,es in adj.items():
        for w in es:rev[w].add(v)
    comp=[];seen=set()
    for r in reversed(order):
        if r in seen:continue
        todo=[r];seen.add(r);block=set()
        while todo:
            v=todo.pop();block.add(v)
            for w in rev[v]:
                if w not in seen:seen.add(w);todo.append(w)
        comp.append(block)
    return [a for a in comp if len(a)>1 or any(v in adj[v] for v in a)]

def parse_cpp(base,g,binary):
    proc=subprocess.run([binary,str(base),g,'--dump'],check=True,capture_output=True,text=True)
    lines=proc.stdout.splitlines();ids={};scc=[];raw=[]
    for row in lines[1:]:
        if row.startswith('SCC '):scc.append(row);continue
        if not row.startswith('V '):continue
        head,arrow=row.split(' ->');_,idx,ls,hs,ys=head.split()
        state=(tuple(map(int,ls)),tuple(map(int,hs)),tuple(map(int,ys.split(','))))
        ids[int(idx)]=state
        raw.append((int(idx),[int(v) for v in arrow.split()]))
    adj={ids[i]:{ids[v] for v in targets} for i,targets in raw}
    return adj,lines[0],scc

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--binary',required=True)
    ap.add_argument('--witness',required=True)
    opts=ap.parse_args()
    summaries=[]
    for k in range(6):
        g=rotate(G,k)
        for b in (4,5,6):
            graph,depth=independent_graph(b,g)
            cgraph,line,scc=parse_cpp(b,g,opts.binary)
            assert graph==cgraph,(b,k,'graph mismatch',len(graph),len(cgraph))
            E=sum(map(len,graph.values()))
            cyc=components(graph)
            depths=sorted(min(depth[v] for v in component) for component in cyc)
            expect=(957,1012,[9,13,14,18]) if b==4 else (5,4,[])
            assert (len(graph),E,depths)==expect,(b,k,len(graph),E,depths)
            summaries.append(dict(base=b,rotation=k,word=g,states=len(graph),edges=E,
                                  cycles=len(cyc),scc_min_depths=depths))
            print('PASS',b,k,g,len(graph),E,depths,flush=True)
    for b in range(2,101):
        for k in range(6):
            g=rotate(G,k)
            root=(tuple(0 for _ in g),tuple(int(z) for z in g),tuple(1 for z in g if z=='1'))
            paths=sum(1 for _ in edge_candidates(b,g,root,True))
            assert paths==(4 if b in (4,5,6) else 0),(b,k,paths)
    print('PASS all six cyclic phases, canonical-root first-coordinate paths, bases 2..100')
    data=json.load(open(opts.witness))
    assert data['base']==4 and data['g']==G
    graph,depth=independent_graph(4,G)
    assert len(data['self_loop_states'])==4
    for item in data['self_loop_states']:
        state=(tuple(map(int,item['L'])),tuple(map(int,item['H'])),tuple(item['Y']))
        assert state in graph and state in graph[state]
        assert depth[state]==item['distance']
        witnesses=list(edge_candidates(4,G,state,False))
        assert len([1 for child,(xs,cs) in witnesses if child==state])==item['witness_count']==1
        assert any(list(xs)==item['x_t'] and list(cs)==item['c_t'] and child==state
                   for child,(xs,cs) in witnesses)
    print('PASS four compact base-4 self-loop witnesses; full successor states checked')
    print('PASS all 18 complete graphs, independent brute-force vs C++ DFS')
    print(json.dumps(summaries,separators=(',',':')))

if __name__=='__main__':main()
