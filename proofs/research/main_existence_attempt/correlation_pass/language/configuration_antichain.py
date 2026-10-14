"""Exact downward reachable configurations, with bounded discovery.

The order is (observer state, NFA subset) <= (same observer state, superset).
NFA transitions are monotone, so maximal reachable subsets suffice to cover
every reachable configuration without complete powerset determinization.
Completion alone is not an inductive-language or Lychrel certificate.
"""
from pathlib import Path
import argparse
import gzip
import hashlib
import json
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = ROOT / 'main_existence_attempt/return_pass/language'


def bits(mask):
    while mask:
        low = mask & -mask
        yield low.bit_length() - 1
        mask ^= low


def run(depth, seconds, cap):
    begin = time.monotonic()
    nfa_file = SOURCE / 'safe_image2_nfa.json'
    observer_file = SOURCE / f'observation_depth{depth}.json'
    nfa = json.loads(nfa_file.read_text())
    observer = json.loads(observer_file.read_text())
    edges = [{q: sum(1 << x for x in vs) for q, vs in row}
             for row in nfa['transitions']]
    delta, finish = observer['delta'], observer['finish']
    invalid = {i for i, row in enumerate(finish) if all(x < 0 for x in row)}
    # Each live id is indexed at every NFA state and once at its least state.
    groups, containing, anchored, exact = {}, {}, {}, {}
    nodes = []  # (observer, subset mask, parent node, input pair)
    active = set()
    progress = []
    comparisons = 0

    def insert(o, mask, parent, q):
        nonlocal comparisons
        lookup = exact.setdefault(o, {})
        if mask in lookup:
            return None
        members = tuple(bits(mask))
        group = groups.setdefault(o, set())
        index = containing.setdefault(o, {})
        anchor = anchored.setdefault(o, {})
        if not members:
            if group:
                return None
            candidates = ()
        else:
            bucket = min((index.get(s, ()) for s in members), key=len)
            for i in tuple(bucket):
                if nodes[i][1].bit_count() <= len(members):
                    continue
                comparisons += 1
                if mask & ~nodes[i][1] == 0:
                    return None
            candidates = [i for s in members for i in anchor.get(s, ())]
            candidates.extend(anchor.get(-1, ()))
        removed = []
        for i in candidates:
            if nodes[i][1].bit_count() >= len(members):
                continue
            comparisons += 1
            if nodes[i][1] & ~mask == 0:
                removed.append(i)
        for i in removed:
            old = nodes[i][1]
            active.remove(i)
            group.remove(i)
            del lookup[old]
            old_members = tuple(bits(old))
            for s in old_members:
                index[s].remove(i)
            anchor[old_members[0] if old_members else -1].remove(i)
        i = len(nodes)
        nodes.append((o, mask, parent, q))
        active.add(i)
        group.add(i)
        lookup[mask] = i
        for s in members:
            index.setdefault(s, set()).add(i)
        anchor.setdefault(members[0] if members else -1, set()).add(i)
        return i

    insert(0, sum(1 << s for s in nfa['initial']), -1, -1)
    cursor = 0
    next_log = begin + 5
    status = 'COMPLETE_REACHABLE_DOWNWARD_CLOSURE'
    while cursor < len(nodes):
        if time.monotonic() - begin >= seconds:
            status = 'UNKNOWN_TIME_CAP'
            break
        if len(nodes) >= cap:
            status = 'UNKNOWN_INSERTION_CAP'
            break
        i = cursor
        cursor += 1
        if i not in active:
            continue
        o, mask, parent, incoming = nodes[i]
        members = tuple(bits(mask))
        for q in range(19):
            no = delta[o][q]
            if no in invalid:
                continue
            nm = 0
            for s in members:
                nm |= edges[s].get(q, 0)
            insert(no, nm, i, q)
        now = time.monotonic()
        if now >= next_log:
            row = dict(seconds=now-begin, inserted=len(nodes), processed=cursor,
                       active=len(active), comparisons=comparisons)
            progress.append(row)
            print(json.dumps(row), flush=True)
            next_log = now + 5

    def word(i):
        out = []
        while nodes[i][2] >= 0:
            o, mask, i, q = nodes[i]
            out.append(q)
        return list(reversed(out))

    maximal = [dict(observer=nodes[i][0], subset=list(bits(nodes[i][1])),
                    pairs=word(i), processed=i < cursor)
               for i in sorted(active)]
    summary = dict(status=status, depth=depth, seconds_cap=seconds,
                   insertion_cap=cap, seconds=time.monotonic()-begin,
                   inserted=len(nodes), processed=cursor, active=len(active),
                   comparisons=comparisons, largest_configuration=max(
                       (len(x['subset']) for x in maximal), default=0),
                   nfa_sha256=hashlib.sha256(nfa_file.read_bytes()).hexdigest(),
                   observer_sha256=hashlib.sha256(observer_file.read_bytes()).hexdigest(),
                   progress=progress, positive_invariant_found=False,
                   live_acceptance_count=None)
    output = HERE / f'antichain_depth{depth}.json.gz'
    with gzip.open(output, 'wt') as stream:
        json.dump(dict(summary, maximal_configurations=maximal), stream,
                  separators=(',', ':'))
    (HERE / f'antichain_depth{depth}_summary.json').write_text(
        json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary), flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--depth', type=int, default=0)
    parser.add_argument('--seconds', type=float, default=120)
    parser.add_argument('--cap', type=int, default=300000)
    args = parser.parse_args()
    run(args.depth, args.seconds, args.cap)
