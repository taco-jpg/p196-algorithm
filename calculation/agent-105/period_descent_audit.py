#!/usr/bin/env python3
"""Independent checks of the base-6 failure of exterior driver-period descent.

The graph oracle enumerates complete coefficient columns as Cartesian products,
then checks all temporal equations simultaneously.  It does not import the
primary transition function.  Integer word evaluation and the original mirror
independently replay the four-step witness.  Static backward certificates give
an additional finite proof of the missing two-step return.
"""
import argparse
from collections import Counter, deque
from functools import lru_cache
import importlib.util
from itertools import product
import json
from pathlib import Path
import resource


BASE = 6
BLOCKS = ((4,7,7,8,3), (9,3,4,5,8), (4,7,7,10,2,2), (9,3,4,9))
ROOT = (0,0,0,1,1)
TARGET = (0,1,1,0,5)
BACKWARD12 = {
    (0,0,0,1,2): (),
    (0,0,0,1,3): (),
    (0,0,1,0,3): (),
    (0,1,0,0,2): ((0,0,0,1,2), (0,1,0,1,1)),
    (0,1,0,1,1): ((0,0,0,1,3), (0,1,0,1,2)),
    (0,1,0,1,2): ((1,0,0,1,2), (1,1,0,1,1)),
    (0,1,1,0,5): ((0,1,0,0,2), (0,1,1,0,5)),
    (1,0,0,1,2): ((1,0,1,0,5), (1,1,1,0,4)),
    (1,0,1,0,5): ((0,0,1,0,3),),
    (1,1,0,1,1): (),
    (1,1,1,0,4): ((1,1,1,1,5),),
    (1,1,1,1,5): ((1,1,1,1,5),),
}
T,A,B,C,D,E = (TARGET, (0,1,0,0,2), (0,1,0,1,1),
               (0,1,0,1,2), (1,0,0,1,2), (1,0,1,0,5))
BACKWARD6 = {
    T: ((T,(5,5)), (A,(2,5))),
    A: ((B,(4,8)),), B: ((C,(3,6)),), C: ((D,(3,7)),),
    D: ((E,(6,1)),), E: (),
}


def require(condition, message):
    if not condition:
        raise ArithmeticError(message)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    require(spec is not None and spec.loader is not None, 'cannot load requested module')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def period(sequence):
    n = len(sequence)
    require(n > 0, 'empty period input')
    return next(p for p in range(1,n+1) if n%p == 0
                and all(sequence[t] == sequence[t%p] for t in range(n)))


def integer_step(base, block):
    """Normalize via integer evaluation and fixed-width digit extraction."""
    width = len(block)
    number = sum(x*base**i for i,x in enumerate(block))
    reverse_number = sum(x*base**i for i,x in enumerate(reversed(block)))
    e, low_value = divmod(number, base**width)
    g, reverse_value = divmod(reverse_number+1-e, base**width)
    require(e in (0,1) and g in (0,1), 'normalization carry is not a bit')
    low, rev = [], []
    for _ in range(width):
        low_value, digit = divmod(low_value, base)
        low.append(digit)
        reverse_value, digit = divmod(reverse_value, base)
        rev.append(digit)
    right = rev[::-1]
    if g:
        low.append((base-1)*(1-e))
        right.insert(0,1)
    raw = tuple(x+y for x,y in zip(low,right))
    end = len(raw)
    while end and raw[end-1] == base-1:
        end -= 1
    return raw[:end], e, g, len(raw)-end, raw


def inflate(state):
    return (state[:2], state[2:4], (0,state[4]))


def flatten(state):
    low, high, previous = state
    return (*low,*high,previous[1])


@lru_cache(None)
def cartesian_edges(base, word, state, first=False):
    """Independent whole-column enumeration, not phase-by-phase propagation."""
    p = len(word)
    low, high, previous = state
    edges = []
    choices = range(1 if first else 0, 2*base-1)
    for column in product(choices, repeat=p):
        digits = tuple((column[t]+low[t])%base for t in range(p))
        next_low = tuple((column[t]+low[t])//base for t in range(p))
        incoming = []
        for t in range(p):
            next_coefficient = column[(t+1)%p]
            allowed = tuple(k for k in (0,1)
                            if (column[t]+k)//base == high[t]
                            and next_coefficient == digits[t]+(
                                previous[t] if word[t] else (column[t]+k)%base))
            if not allowed:
                break
            incoming.append(allowed)
        else:
            for inward in product(*incoming):
                next_previous = tuple((column[t]+inward[t])%base if word[t] else 0
                                      for t in range(p))
                edges.append(((next_low,inward,next_previous),column))
    return tuple(edges)


def terminal(base, word, state):
    low, high, previous = state
    return all(l+h == 1 for l,h in zip(low,high)) and all(
        not word[t] or previous[t] == (base-1)*low[t] for t in range(len(word)))


def graph(base, bits):
    word = tuple(map(int,bits))
    initial = (True, ((0,)*len(word),word,word))
    depths, edges, parent = {initial:0}, {}, {initial:None}
    queue = deque([initial])
    while queue:
        vertex = queue.popleft()
        first, state = vertex
        row = []
        for target,column in cartesian_edges(base,word,state,first):
            key = (False,target)
            row.append((key,column))
            if key not in depths:
                depths[key] = depths[vertex]+1
                parent[key] = (vertex,column)
                queue.append(key)
        edges[vertex] = tuple(row)
    accepted = {}
    witnesses = []
    for vertex,depth in depths.items():
        if not terminal(base,word,vertex[1]):
            continue
        eword = ''.join(map(str,vertex[1][0]))
        accepted[eword] = min(depth,accepted.get(eword,depth))
        columns = []
        current = vertex
        while parent[current] is not None:
            previous,column = parent[current]
            columns.append(column)
            current = previous
        columns.reverse()
        blocks = []
        for t in range(len(word)):
            block = tuple(column[t] for column in columns)
            end = len(block)
            while end and block[end-1] == base-1:
                end -= 1
            blocks.append(block[:end])
        for t,block in enumerate(blocks):
            target,e,g,_,_ = integer_step(base,block)
            require(target == blocks[(t+1)%len(word)] and e == int(eword[t])
                    and g == word[t], 'Cartesian graph witness failed integer replay')
        witnesses.append({'e':eword,'width':depth,'B_period':period(blocks),
                          'driver_period':period(tuple(zip(map(int,eword),word)))})
    return depths, edges, accepted, witnesses


def finite_certificates():
    universe = tuple(product(range(2),range(2),range(2),range(2),range(6)))
    predecessors = {state:[] for state in universe}
    count = 0
    invariant_checks = 0
    for source in universe:
        for successor,column in cartesian_edges(6,(0,1),inflate(source)):
            target = flatten(successor)
            predecessors[target].append((source,column))
            count += 1
            reverse0 = (column[0]+target[2])%6
            require(6*(target[0]+target[1]) == source[0]+source[1]+reverse0+source[4],
                    'carry-sum identity failed')
            if source[0]+source[1] == 1:
                require(target[0]+target[1] == 1, 'complementary-carry invariant failed')
                invariant_checks += 1
    require(len(universe) == count == 96, 'full generic universe census changed')
    for target,expected in BACKWARD12.items():
        observed = {source for source,_ in predecessors[target]}
        require(observed == set(expected), '12-state full predecessor row differs')
        require(observed <= BACKWARD12.keys(), '12-state set not predecessor closed')
    require(TARGET in BACKWARD12 and ROOT not in BACKWARD12,
            '12-state separator does not separate root from target')
    for target,expected in BACKWARD6.items():
        observed = Counter((source,column) for source,column in predecessors[target]
                           if source[0]+source[1] == 1)
        require(observed == Counter(expected), 'six-state labelled inverse row differs')
        require(all(source in BACKWARD6 for source,_ in observed), 'six-state set is not closed')
    first = {flatten(s) for s,_ in cartesian_edges(6,(0,1),inflate(ROOT),True)}
    expected_first = {(0,1,1,0,3),(0,1,1,1,4),(0,1,0,0,4),(0,1,0,1,5)}
    require(first == expected_first, 'positive first-column list differs')
    require(first.isdisjoint(BACKWARD6) and all(s[0]+s[1] == 1 for s in first),
            'first columns fail six-state separation')
    return {'generic_states':96,'generic_labelled_edges':count,
            'complementary_carry_edges':invariant_checks,'backward_closed_states':12,
            'invariant_backward_closed_states':6,'positive_first_successors':4,
            'excluded_terminal':TARGET,'status':'PASS'}


def witness_audit(mirror):
    empty_target,empty_e,empty_g,empty_u,empty_raw = integer_step(6,())
    require((empty_target,empty_e,empty_g,empty_u,empty_raw) == ((6,),0,1,0,(6,)),
            'empty exterior integer update failed')
    require(mirror.hyp(6,[],[10]) and mirror.e1(6,[]) == 0
            and mirror.gam(6,[],[10]) == 1 and mirror.nextB(6,[],[10]) == [6],
            'empty exterior original-mirror control failed')
    records = []
    for t,block in enumerate(BLOCKS):
        target,e,g,u,raw = integer_step(6,block)
        require(target == BLOCKS[(t+1)%4] and e == g == t%2,
                'explicit four-block witness does not close with stated labels')
        require(u == (0,0,2,0)[t], 'wrong canonical trim')
        center = [0] if e else [10]
        require(mirror.hyp(6,list(block),center), 'synthetic one-edge fixture violates Hyp')
        require(mirror.e1(6,list(block)) == e and mirror.gam(6,list(block),center) == g,
                'original mirror driver mismatch')
        require(tuple(mirror.nextB(6,list(block),center)) == raw, 'original mirror raw edge mismatch')
        records.append({'B':block,'B2':target,'e':e,'g':g,'u':u,'raw':raw})
    require(period(BLOCKS) == 4, 'explicit B period is not four')
    require(period(tuple((row['e'],row['g']) for row in records)) == 2, 'joint driver period is not two')
    padded = tuple(block+(5,)*(6-len(block)) for block in BLOCKS)
    for t,block in enumerate(padded):
        _,e,g,_,raw = integer_step(6,block)
        require(raw == padded[(t+1)%4]+(5,)*g and e == g == t%2,
                'natural common-width trim check failed')
    differing = [j for j in range(6) if any(padded[t][j] != padded[(t+2)%4][j] for t in range(4))]
    require(differing == [3,4,5], 'genuine period-difference flag incorrect')
    # A doubled two-step witness must not be mistaken for primitive period four.
    repeated = ((1,0),(2,),(1,0),(2,))
    for t,block in enumerate(repeated):
        target,e,g,_,_ = integer_step(2,block)
        require(target == repeated[(t+1)%4] and e == g == t%2, 'binary repeat control failed')
    repeated_padded = tuple(block+(1,)*(2-len(block)) for block in repeated)
    require(period(repeated) == 2 and not any(repeated_padded[t] != repeated_padded[(t+2)%4]
                                            for t in range(4)), 'false primitive-period flag')
    for width in range(1,7):
        _,e,g,_,raw = integer_step(6,(5,)*width)
        require((e,g,raw) == (0,1,(6,)+(5,)*width), 'empty-word padding control failed')
    return {'B_least_period':4,'joint_driver_least_period':2,'canonical_trims':[0,0,2,0],
            'common_width':6,'padded_trims':[0,1,0,1],'differing_columns':differing,
            'false_primitive_period_control':'PASS','mirror_edges':4,
            'empty_exterior_control':'PASS',
            'scope':'synthetic centers are separate one-edge fixtures, not a C-cycle'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mirror',type=Path,
                        default=Path(__file__).resolve().parents[1]/'neutral_band_search.py')
    parser.add_argument('--primary',type=Path,
                        default=Path(__file__).with_name('period_descent.py'))
    args = parser.parse_args()
    current,hard = resource.getrlimit(resource.RLIMIT_AS)
    maximum = 1024**3 if current == resource.RLIM_INFINITY else min(current,1024**3)
    resource.setrlimit(resource.RLIMIT_AS,(maximum,hard))
    mirror = load_module('period_descent_audit_mirror',args.mirror)
    certificate = finite_certificates()
    witness = witness_audit(mirror)
    # The primary module is used only for result comparison after oracle setup.
    primary = load_module('period_descent_primary_comparison',args.primary)
    summaries = []
    for base,bits in ((2,'01'),(2,'0101'),(3,'01'),(4,'01'),(5,'01'),(6,'01'),(6,'0101')):
        depths,edges,accepted,witnesses = graph(base,bits)
        other_depths,other_accepted,other_count = primary.generic_graph(base,bits)
        count = sum(map(len,edges.values()))
        require(depths == other_depths and accepted == other_accepted and count == other_count,
                'independent Cartesian graph differs from primary temporal propagation')
        if (base,bits) == (6,'01'):
            require((len(depths),count,max(depths.values()),accepted) == (24,24,7,{'10':5}),
                    'complete two-period census differs')
            vertices,primary_edges,primary_depths = primary.graph()
            translated = {(first,flatten(state)):depth for (first,state),depth in depths.items()}
            require(translated == dict(zip(vertices,primary_depths)), 'explicit state table differs')
            observed = Counter(((first,flatten(state)),(other_first,flatten(other_state)),column)
                               for (first,state),row in edges.items()
                               for ((other_first,other_state),column) in row)
            expected = Counter((vertices[i],vertices[j],(x0,x1))
                               for i,row in enumerate(primary_edges) for j,x0,x1 in row)
            require(observed == expected, 'explicit labelled transition table differs')
        if (base,bits) == (6,'0101'):
            require((len(depths),count,max(depths.values()),accepted) ==
                    (65,68,8,{'1010':5,'0101':6}), 'complete four-period census differs')
        summaries.append({'base':base,'g':bits,'states':len(depths),'transitions':count,
                          'max_shortest_depth':max(depths.values()),'accepted_e':accepted,
                          'accepted_witness_periods':witnesses,'complete':True})
    print(json.dumps({'status':'PASS','witness':witness,'inverse_certificates':certificate,
                      'exact_graph_comparisons':summaries,
                      'peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss},sort_keys=True))


if __name__ == '__main__':
    main()
