"""Exact residual-observation automata and universal inductive kernels.

This is a positive certificate search, not a finite-orbit test. No solver is
used. A completed nonempty kernel would yield a regular safe closed language.
Empty kernels get independently replayable, concrete elimination proofs.

All output stays beside this file. Resource caps mean UNKNOWN, never UNSAT.
"""
from __future__ import annotations

from collections import deque
from pathlib import Path
import argparse
import hashlib
import json
import random
import time

HERE = Path(__file__).resolve().parent
CENTERS = (None,) + tuple(range(0, 19, 2))


def ci(c):
    return 0 if c is None else c // 2 + 1


def canonical(p, c):
    return (bool(p) and 1 <= p[0] <= 18 and all(0 <= x <= 18 for x in p)
            and (c is None or c in CENTERS)) or (not p and c in range(2, 19, 2))


def realize(p, c):
    assert canonical(p, c)
    ds = [max(0, q - 9) for q in p]
    if c is not None:
        ds.append(c // 2)
    ds.extend(min(9, q) for q in reversed(p))
    return sum(d * 10 ** i for i, d in enumerate(ds))


def numeric_word(n):
    ds = tuple(map(int, str(n)))
    q = tuple(a + b for a, b in zip(ds, reversed(ds)))
    return q[:len(q)//2], q[len(q)//2] if len(q) % 2 else None


def numeric_step_word(p, c):
    n = realize(p, c)
    return numeric_word(n + int(str(n)[::-1]))


def bad(p, c):
    return ((all(x <= 9 for x in p) and (c is None or c <= 9)) or
            (bool(p) and p[0] == 11 and all(x in (0, 11) for x in p)
             and (c is None or c == 0)))


def base_machine():
    """Terminal outputs are -1 for noncanonical input and 0/1 otherwise."""
    keys = [(True, True, False)]
    ids = {keys[0]: 0}
    d, f = [], []
    i = 0
    while i < len(keys):
        key = keys[i]
        if key is None:
            d.append([i] * 19)
            f.append([-1] * 11)
            i += 1
            continue
        low, exc, started = key
        row = []
        for q in range(19):
            nxt = None if not started and q == 0 else (
                low and q <= 9,
                exc and (q in (0, 11) if started else q == 11), True)
            if nxt not in ids:
                ids[nxt] = len(keys)
                keys.append(nxt)
            row.append(ids[nxt])
        d.append(row)
        f.append([-1 if not started and c in (None, 0) else int(
            (low and (c is None or c <= 9)) or
            (exc and started and c in (None, 0))) for c in CENTERS])
        i += 1
    return minimize((d, f))


def minimize(machine):
    """Moore minimization preserves all eleven terminal observation values."""
    d, f = machine
    classes = [0] * len(d)
    while True:
        sig_ids = {}
        nxt = []
        for i in range(len(d)):
            sig = (tuple(f[i]), tuple(classes[v] for v in d[i]))
            if sig not in sig_ids:
                sig_ids[sig] = len(sig_ids)
            nxt.append(sig_ids[sig])
        if nxt == classes:
            break
        classes = nxt
    reps = {}
    for i, a in enumerate(classes):
        reps.setdefault(a, i)
    # BFS reindexing makes initial state zero, and removes unreachable states.
    order = [classes[0]]
    ren = {order[0]: 0}
    outd, outf = [], []
    for a in order:
        i = reps[a]
        row = []
        for v in d[i]:
            b = classes[v]
            if b not in ren:
                ren[b] = len(order)
                order.append(b)
            row.append(ren[b])
        outd.append(row)
        outf.append(f[i])
    return outd, outf


def fst_edge(st, q):
    """Outside-in exact carry update; emit one new folded pair."""
    h, a, b, t, started = st
    if q == 0 and not started:
        return
    for bn in (0, 1):
        if (q + bn) // 10 != b:
            continue
        lo, hi = (q + a) % 10, (q + bn) % 10
        yield (h, (q + a) // 10, bn, hi if h else -1, True), lo + (t if h else hi)


def fst_term(st, c):
    """Return (extra pair or None, output center), or no valid terminal."""
    h, a, b, t, started = st
    if not started and c in (None, 0):
        return None
    if c is None:
        return (None, 2 * t if h else None) if a == b else None
    if (c + a) // 10 != b:
        return None
    return ((c + a) % 10 + t, None) if h else (None, 2 * ((c + a) % 10))


START_FST = ((0, 0, 0, -1, False), (1, 0, 1, 1, False))


def extend_observation(machine, cap=200000, deadline=float('inf')):
    """Record bad(q),bad(Gq),...,bad(G^(k+1)q) exactly for EVERY word.

    Subset states keep all backward-carry alternatives until the actual
    center resolves them. This is full-word correlation, not a suffix window.
    """
    d, f = machine
    bd, bf = base_machine()
    first = (0, tuple((st, 0) for st in START_FST))
    keys = [first]
    ids = {first: 0}
    nd, nf = [], []
    largest = 0
    for key in keys:
        if time.monotonic() > deadline:
            return None, dict(status='UNKNOWN_time_cap',raw_states=len(keys))
        bs, paths = key
        largest = max(largest, len(paths))
        row = []
        for q in range(19):
            targets = set()
            for st, s in paths:
                for ns, out in fst_edge(st, q):
                    targets.add((ns, d[s][out]))
            nxt = bd[bs][q], tuple(sorted(targets))
            if nxt not in ids:
                if len(keys) >= cap:
                    return None, dict(status='UNKNOWN_state_cap',raw_states=len(keys))
                ids[nxt] = len(keys)
                keys.append(nxt)
            row.append(ids[nxt])
        flags = []
        for c in CENTERS:
            b = bf[bs][ci(c)]
            if b < 0:
                flags.append(-1)
                continue
            vals = []
            for st, s in paths:
                term = fst_term(st, c)
                if term is None:
                    continue
                extra, oc = term
                target = s if extra is None else d[s][extra]
                vals.append(f[target][ci(oc)])
            # Exact functionality: one complete actual carry history.
            assert len(vals) == 1 and vals[0] >= 0, (key, c, vals)
            flags.append(b | (vals[0] << 1))
        nd.append(row)
        nf.append(flags)
    result = minimize((nd, nf))
    return result, dict(status='COMPLETE',raw_states=len(keys),
                        minimized_states=len(result[0]),max_carry_alternatives=largest)


def state_of(machine, p):
    d, f = machine
    s = 0
    for q in p:
        s = d[s][q]
    return s


def observation(machine, p, c):
    return machine[1][state_of(machine, p)][ci(c)]


def controls(machine, depth):
    rng = random.Random(41898 + depth)
    words = []
    for n in range(1, 20001):
        words.append(numeric_word(n))
    for _ in range(2000):
        p = (rng.randrange(1, 19),) + tuple(rng.randrange(19) for _ in range(rng.randrange(30)))
        words.append((p, rng.choice(CENTERS)))
    for p, c in words:
        assert canonical(p, c)
        w = p, c
        mask = 0
        for k in range(depth + 1):
            # Direct decimal palindromicity is independent of the B predicate.
            n = realize(*w)
            z = n + int(str(n)[::-1])
            bit = str(z) == str(z)[::-1]
            mask |= int(bit) << k
            w = numeric_word(z)
        assert observation(machine, p, c) == mask, (p,c,depth,mask)
    return len(words)


def kernel(machine, cap=2000000, deadline=float('inf')):
    """Greatest safe invariant with these fixed pair transitions.

    Terminal choices are unrestricted. A class is (pair-state,center). Edges
    include EVERY exact finite decimal transition, by finite FST product BFS.
    """
    d, f = machine
    states = [(0, 0, st) for st in START_FST]
    ids = {s: i for i, s in enumerate(states)}
    parents = [None, None]
    # Every edge records a product prefix and its final center, giving a word.
    edges = {}
    reps = {}
    for index, (si, so, st) in enumerate(states):
        if time.monotonic() > deadline:
            return dict(status='UNKNOWN_time_cap',product_states=len(states),class_edges=len(edges))
        for c in CENTERS:
            term = fst_term(st, c)
            if term is None:
                continue
            extra, oc = term
            target = so if extra is None else d[so][extra]
            source_class = si * 11 + ci(c)
            target_class = target * 11 + ci(oc)
            assert f[si][ci(c)] >= 0 and f[target][ci(oc)] >= 0
            edges.setdefault((source_class, target_class), (index, c))
            reps.setdefault(source_class, (index, c))
        for q in range(19):
            for ns, out in fst_edge(st, q):
                nxt = d[si][q], d[so][out], ns
                if nxt not in ids:
                    if len(states) >= cap:
                        return dict(status='UNKNOWN_state_cap',product_states=len(states),class_edges=len(edges))
                    ids[nxt] = len(states)
                    states.append(nxt)
                    parents.append((index, q))
    # This product is complete; every admissible word has exactly one terminal.
    nodes = set(reps)
    assert all(a in nodes and b in nodes for a,b in edges)
    incoming = {v: [] for v in nodes}
    for a, b in edges:
        incoming[b].append(a)
    bads = sorted(v for v in nodes if f[v//11][v%11] & 1)
    removed = set(bads)
    why = {v: None for v in bads}
    rank = {v: 0 for v in bads}
    order = list(bads)
    for b in order:
        for a in incoming[b]:
            if a not in removed:
                removed.add(a)
                why[a] = b
                rank[a] = rank[b] + 1
                order.append(a)
    live = sorted(nodes - removed)

    def prefix(index):
        p = []
        while parents[index] is not None:
            index, q = parents[index]
            p.append(q)
        return list(reversed(p))

    proof = []
    for a in order:
        b = why[a]
        index, c = reps[a] if b is None else edges[a,b]
        p = prefix(index)
        proof.append(dict(source=a,target=b,rank=rank[a],word=[p,c]))
    result = dict(status='POSITIVE_CANDIDATE' if live else 'EMPTY_KERNEL',
                  dfa_states=len(d),classes=len(nodes),class_edges=len(edges),
                  product_states=len(states),initial_bad_classes=len(bads),
                  elimination_depth=max(rank.values(),default=0),live_classes=live,
                  eliminated=proof)
    if live:
        a = live[0]
        index,c = reps[a]
        p = prefix(index)
        n = realize(p,c)
        result.update(seed=[p,c],representative=str(n),proposed_lychrel_witness=str(n+int(str(n)[::-1])))
    return result


def save_json(name, data):
    path = HERE / name
    path.write_text(json.dumps(data, separators=(',', ':')) + '\n')
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--max-depth',type=int,default=4)
    p.add_argument('--seconds',type=float,default=240)
    p.add_argument('--automaton-cap',type=int,default=200000)
    p.add_argument('--product-cap',type=int,default=2000000)
    args = p.parse_args()
    start = time.monotonic()
    deadline = start + args.seconds
    machine = base_machine()
    report = dict(status='RUNNING',approach='exact right-context observation kernel',runs=[])
    for depth in range(args.max_depth+1):
        if depth:
            machine, build = extend_observation(machine,args.automaton_cap,deadline)
            if machine is None:
                report['runs'].append(dict(depth=depth,build=build))
                break
        else:
            build = dict(status='COMPLETE',minimized_states=len(machine[0]))
        machine_hash = save_json('observation_depth%d.json'%depth,dict(depth=depth,delta=machine[0],finish=machine[1]))
        checks = controls(machine,depth)
        result = kernel(machine,args.product_cap,deadline)
        result_hash = save_json('kernel_depth%d.json'%depth,result)
        row = dict(depth=depth,build=build,arithmetic_controls=checks,
                   machine_sha256=machine_hash,kernel_sha256=result_hash,
                   **{k:v for k,v in result.items() if k not in ('eliminated','live_classes')})
        row['live_class_count']=len(result['live_classes']) if 'live_classes' in result else None
        report['runs'].append(row)
        print(json.dumps(row),flush=True)
        report['seconds']=time.monotonic()-start
        save_json('kernel_search_report.json',report)
        if result['status'].startswith('UNKNOWN') or result['status']=='POSITIVE_CANDIDATE':
            break
    report['status']='FINISHED_NO_POSITIVE_CERTIFICATE' if all(x.get('status')!='POSITIVE_CANDIDATE' for x in report['runs']) else 'POSITIVE_PENDING_INDEPENDENT_AUDIT'
    report['seconds']=time.monotonic()-start
    save_json('kernel_search_report.json',report)


if __name__=='__main__':
    main()
