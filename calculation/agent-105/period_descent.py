#!/usr/bin/env python3
"""Base-6 counterexample to exterior descent to the full driver period.

A primitive four-step canonical B cycle has (e,g)=(01,01) repeated twice.
An independently enumerable 24-state graph excludes EVERY finite two-step
B return with (e,g)=(01,01), including arbitrary neutral trims via padding.
This concerns exterior B dynamics only; it supplies no compatible C cycle.
"""
from collections import deque
from itertools import product
from pathlib import Path
import argparse
import importlib.util
import json

BASE = 6
BLOCKS = ((4,7,7,8,3), (9,3,4,5,8), (4,7,7,10,2,2), (9,3,4,9))
TRIMS = (0,0,2,0)
# (L_0,L_1,H_0,H_1,Y_1), ordered by the exact BFS below.
STATES = (
 (0,0,0,1,1), (0,1,0,0,4), (0,1,0,1,5), (0,1,1,0,3),
 (0,1,1,1,4), (1,0,0,0,4), (1,0,0,1,5), (1,0,1,0,3),
 (1,0,1,1,4), (1,0,0,0,5), (1,0,1,0,4), (1,0,1,1,5),
 (1,0,0,0,3), (1,0,0,1,4), (1,0,1,0,2), (1,0,1,1,3),
 (1,0,0,1,0), (0,1,1,0,4), (0,1,1,1,5), (1,0,0,0,2),
 (1,0,0,1,3), (1,0,1,0,1), (1,0,1,1,2), (0,1,1,1,0),
)
# Each entry (target_state_id, x_0, x_1) is one entire spatial column.
EDGES = (
 ((1,5,10),(2,5,10),(3,4,9),(4,4,9)), (), (),
 ((5,8,4),(6,8,4),(7,7,3),(8,7,3)), (), (), (),
 ((9,8,5),(10,7,4),(11,7,4)), (), (),
 ((12,7,3),(13,7,3),(14,6,2),(15,6,2)), (), (), (), (),
 ((16,8,5),), ((16,5,5),(17,4,10),(18,4,10)),
 ((19,7,2),(20,7,2),(21,6,1),(22,6,1)), ((23,5,5),),
 (), (), (), (), (),
)


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def integer_step(base, block):
    """Full B step using integer evaluation, fixed-width digits, maximal trim."""
    require(isinstance(base, int) and base >= 2, 'invalid base')
    require(all(type(a) is int and 0 <= a <= 2*base-2 for a in block),
            'invalid coefficient')
    require(not block or block[0] != 0, 'zero exterior head')
    n = len(block)
    value = lambda w: sum(a*base**i for i,a in enumerate(w))
    low_number = value(block)
    e = low_number // base**n
    high_number = value(block[::-1]) + 1-e
    g = high_number // base**n
    require(e in (0,1) and g in (0,1), 'non-bit endpoint carry')
    low = [(low_number//base**i)%base for i in range(n)]
    high = [(high_number//base**i)%base for i in range(n)][::-1]
    if g:
        low.append((base-1)*(1-e)); high.insert(0,1)
    raw = tuple(a+c for a,c in zip(low,high))
    target = raw
    while target and target[-1] == base-1:
        target = target[:-1]
    return target, len(raw)-len(target), e, g, raw


def outgoing(state, first):
    """All p=2, g=01 columns, enumerating BOTH inward carry bits first."""
    l0,l1,h0,h1,y = state
    for a0,a1 in product((0,1), repeat=2):
        for x0 in range(1 if first else 0, 11):
            if (x0+a0)//6 != h0:
                continue
            x1 = (x0+l0)%6 + (x0+a0)%6
            if first and x1 == 0:
                continue
            if (x1+a1)//6 != h1:
                continue
            if (x1+l1)%6 + y != x0:
                continue
            successor = ((x0+l0)//6, (x1+l1)//6,
                         a0, a1, (x1+a1)%6)
            yield successor, x0, x1


def graph():
    initial = (True, (0,0,0,1,1))
    vertices = [initial]
    ids = {initial:0}
    depths = [0]
    edges = []
    queue = deque([0])
    while queue:
        i = queue.popleft()
        first, state = vertices[i]
        row = []
        for target,x0,x1 in outgoing(state,first):
            key = (False,target)
            if key not in ids:
                ids[key] = len(vertices)
                vertices.append(key)
                depths.append(depths[i]+1)
                queue.append(ids[key])
            row.append((ids[key],x0,x1))
        edges.append(tuple(row))
    return tuple(vertices), tuple(edges), tuple(depths)


def generic_graph(base, word):
    """Independent-form full-column control, used here only for periods 2 and 4."""
    require(base >= 2 and word and set(word) <= {'0','1'}, 'invalid graph input')
    g = tuple(map(int,word)); p = len(g)
    initial = (True, ((0,)*p,g,g))
    depths = {initial:0}; queue = deque([initial]); emitted = 0
    accepts = {}
    choices = tuple(product((0,1),repeat=p))
    while queue:
        first,state = queue.popleft(); low,high,previous = state
        depth = depths[(first,state)]
        if all(low[t]+high[t] == 1 for t in range(p)) and all(
                not g[t] or previous[t] == (base-1)*low[t] for t in range(p)):
            accepts.setdefault(''.join(map(str,low)),depth)
        for inward in choices:
            for seed in range(1 if first else 0,2*base-1):
                x = seed; column = []
                for t in range(p):
                    if first and x == 0:
                        break
                    if (x+inward[t])//base != high[t]:
                        break
                    column.append(x)
                    partner = previous[t] if g[t] else (x+inward[t])%base
                    x = (x+low[t])%base+partner
                else:
                    if x != seed:
                        continue
                    emitted += 1
                    target = (tuple((column[t]+low[t])//base for t in range(p)),
                              inward,
                              tuple((column[t]+inward[t])%base if g[t] else 0
                                    for t in range(p)))
                    key = (False,target)
                    if key not in depths:
                        depths[key] = depth+1; queue.append(key)
    return depths,accepts,emitted


def accepted(state):
    l0,l1,h0,h1,y = state
    return l0+h0 == l1+h1 == 1 and y == 5*l1


def verify_graph():
    vertices,edges,depths = graph()
    require(tuple(s for _,s in vertices) == STATES, 'static state table mismatch')
    require(edges == EDGES, 'static transition table mismatch')
    require(vertices[0][0] and not any(f for f,_ in vertices[1:]),
            'restricted root was confused with an ordinary state')
    accepts = [(i,''.join(map(str,s[:2])))
               for i,(_,s) in enumerate(vertices) if accepted(s)]
    require(accepts == [(16,'10')], 'unexpected complete accepted e set')
    require((0,1,1,0,5) not in STATES, 'forbidden e01 endpoint is reachable')
    return dict(states=len(vertices), transitions=sum(map(len,edges)),
                max_shortest_depth=max(depths), accepted_e=['10'],
                excluded_e='01', complete=True)


def verify_witness(mirror):
    records=[]
    for t,block in enumerate(BLOCKS):
        target,u,e,g,raw = integer_step(BASE,block)
        require(target == BLOCKS[(t+1)%4], 'four-step witness does not close')
        require(u == TRIMS[t] and e == g == t%2, 'wrong trim or joint label')
        require(block[-1] != 5, 'witness block is not canonical')
        # An independent one-edge center fixture forces the required carry flip.
        center = [0] if e else [10]
        require(mirror.hyp(BASE,list(block),center), 'mirror Hyp failed')
        require(mirror.e1(BASE,list(block)) == e, 'mirror e failed')
        require(mirror.gam(BASE,list(block),center) == g, 'mirror g failed')
        require(tuple(mirror.nextB(BASE,list(block),center)) == raw,
                'mirror full raw B edge differs')
        records.append(dict(B=list(block),B2=list(target),u=u,e=e,g=g,raw=list(raw)))
    require(len(set(BLOCKS)) == 4, 'witness is not primitive period four')
    # Common-width witness: append neutral 5s up to width six, with allowed trims u=g.
    padded = tuple(b+(5,)*(6-len(b)) for b in BLOCKS)
    for t,block in enumerate(padded):
        _,_,e,g,raw = integer_step(BASE,block)
        require(raw == padded[(t+1)%4]+(5,)*g, 'common padding identity failed')
        require(e == g == t%2, 'padding changed labels')
    # Include the empty exterior, which pads to an all-neutral nonempty word.
    for width in range(1,7):
        _,_,e,g,raw = integer_step(BASE,(5,)*width)
        require((e,g,raw) == (0,1,(6,)+(5,)*width), 'empty-block padding control failed')
    # Reachable e10 is a positive two-period control for the negative graph.
    positive = ((4,7,7,6,8),(9,3,4,2))
    for t,block in enumerate(positive):
        target,_,e,g,_ = integer_step(BASE,block)
        require(target == positive[1-t] and e == 1-t and g == t,
                'positive two-period control failed')
    return records


def table():
    print('| ID | (L0,L1,H0,H1,Y1) | Complete outgoing list: column -> ID |')
    print('|---:|---|---|')
    for i,(state,row) in enumerate(zip(STATES,EDGES)):
        entries = '; '.join(f'({x0},{x1}) -> {j}' for j,x0,x1 in row) or 'none'
        print(f'| {i} | {state} | {entries} |')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mirror',type=Path,
                        default=Path(__file__).resolve().parents[1]/'neutral_band_search.py')
    parser.add_argument('--table',action='store_true')
    args=parser.parse_args()
    spec=importlib.util.spec_from_file_location('descent_mirror',args.mirror)
    require(spec is not None and spec.loader is not None, 'cannot load mirror')
    mirror=importlib.util.module_from_spec(spec);spec.loader.exec_module(mirror)
    result=verify_graph()
    records=verify_witness(mirror)
    controls=[]
    for word,expected in (('01',{'10':5}),('0101',{'1010':5,'0101':6})):
        depths,accepts,emitted=generic_graph(6,word)
        require(accepts == expected, 'generic complete accepted set differs')
        if word == '01':
            flat = {(first, (low[0],low[1],high[0],high[1],previous[1]))
                    for first,(low,high,previous) in depths}
            require(flat == {(i == 0,state) for i,state in enumerate(STATES)},
                    'generic and explicit p2 graph state sets differ')
            require(emitted == 24, 'generic p2 transition count differs')
        else:
            require((len(depths),emitted,max(depths.values())) == (65,68,8),
                    'generic p4 graph counts differ')
        controls.append(dict(g=word,states=len(depths),transitions=emitted,
                             max_shortest_depth=max(depths.values()),
                             accepted_e=accepts,complete=True))
    print(json.dumps(dict(status='PASS' ,base=BASE,driver_e='01',driver_g='01',
                          primitive_B_period=4,witness_edges=records,
                          two_period_graph=result,complete_graph_controls=controls,
                          scope='exterior only; no compatible C cycle claimed'),
                     separators=(',',':')))
    if args.table:
        table()

if __name__=='__main__':
    main()
