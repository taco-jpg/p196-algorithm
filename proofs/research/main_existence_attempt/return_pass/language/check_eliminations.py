"""Independent all-length replay of residual-kernel exclusion certificates.

Imports neither the discovery code nor a carry transducer. All implication
edges are checked by ordinary integer reversal/addition. Complete coverage
uses just the saved DFA transition table and canonical-prefix reachability.

One rejected class may switch to a DIFFERENT word in that same class. Thus
these are language-family exclusions, not numeric termination claims.
"""
from collections import deque
from pathlib import Path
import argparse
import hashlib
import json

HERE = Path(__file__).resolve().parent
CENTERS = (None,) + tuple(range(0, 19, 2))


def class_of(delta, pairs, center):
    state = 0
    for symbol in pairs:
        state = delta[state][symbol]
    terminal = 0 if center is None else center // 2 + 1
    return 11 * state + terminal


def integer_of(pairs, center):
    assert all(isinstance(q, int) and 0 <= q <= 18 for q in pairs)
    assert center in CENTERS
    if pairs:
        assert pairs[0] > 0
    else:
        assert center is not None and center > 0
    # Build a decimal string from high end to low end, independently of the
    # discovery program's polynomial accumulation. The outer high digit >0.
    high = ''.join(str(min(q, 9)) for q in pairs)
    middle = '' if center is None else str(center // 2)
    low = ''.join(str(max(0, q - 9)) for q in reversed(pairs))
    return int(high + middle + low)


def fold_integer(n):
    digits = [int(x) for x in str(n)]
    k = len(digits) // 2
    pairs = [digits[i] + digits[-1-i] for i in range(k)]
    return pairs, 2 * digits[k] if len(digits) % 2 else None


def reachable_classes(delta):
    # Empty prefix is permitted only with a positive even center.
    classes = {j for j in range(2, 11)}
    seen = {delta[0][q] for q in range(1, 19)}
    todo = deque(seen)
    while todo:
        state = todo.popleft()
        classes.update(range(11 * state, 11 * state + 11))
        for target in delta[state]:
            if target not in seen:
                seen.add(target)
                todo.append(target)
    return classes


def check(depth, extended=False, prefix=''):
    mpath = HERE / ('observation_%sdepth%d.json' % (prefix,depth))
    kpath = HERE / ('kernel_%sdepth%d%s.json' % (prefix,depth,'_extended' if extended else ''))
    machine = json.loads(mpath.read_text())
    result = json.loads(kpath.read_text())
    assert result['status'] == 'EMPTY_KERNEL'
    delta = machine['delta']
    assert delta and all(len(row) == 19 for row in delta)
    assert all(type(t) is int and 0 <= t < len(delta) for row in delta for t in row)
    all_classes = reachable_classes(delta)
    eliminated = set()
    rank = {}
    witness = {}
    longest = 0
    max_integer_digits = 0
    bad_count = 0
    for row in result['eliminated']:
        source, target = row['source'], row['target']
        pairs, center = row['word']
        assert source in all_classes and source not in eliminated
        assert class_of(delta, pairs, center) == source
        number = integer_of(pairs, center)
        out = number + int(str(number)[::-1])
        outpairs, outcenter = fold_integer(out)
        assert fold_integer(number) == (pairs, center)
        if target is None:
            assert str(out) == str(out)[::-1]
            assert row['rank'] == 0
            bad_count += 1
        else:
            assert target in eliminated
            assert class_of(delta, outpairs, outcenter) == target
            assert row['rank'] == rank[target] + 1
        rank[source] = row['rank']
        witness[source] = row
        eliminated.add(source)
        longest = max(longest, len(pairs))
        max_integer_digits = max(max_integer_digits, len(str(number)))
    assert eliminated == all_classes
    assert len(eliminated) == result['classes']
    assert bad_count == result['initial_bad_classes']
    # Illustrative obstruction chain for the class containing 196. Each row
    # certifies a language implication, not a step of 196's ordinary orbit.
    seedclass = class_of(delta, [7], 18)
    chain = []
    node = seedclass
    while True:
        row = witness[node]
        pairs, center = row['word']
        number = integer_of(pairs, center)
        out = number + int(str(number)[::-1])
        chain.append(dict(class_id=node,rank=row['rank'],witness_number=str(number),
                          output_number=str(out),pair_word=[pairs,center],target=row['target']))
        if row['target'] is None:
            break
        node = row['target']
    report = dict(depth=depth,status='INDEPENDENT_EXCLUSION_VERIFIED',
                  states=len(delta),covered_classes=len(eliminated),
                  numeric_edges=len(eliminated)-bad_count,palindrome_roots=bad_count,
                  max_rank=max(rank.values()),longest_pair_prefix=longest,
                  max_integer_digits=max_integer_digits,seed196_class=seedclass,
                  seed196_language_obstruction=chain,
                  machine_sha256=hashlib.sha256(mpath.read_bytes()).hexdigest(),
                  certificate_sha256=hashlib.sha256(kpath.read_bytes()).hexdigest())
    if prefix:
        report['observer_refinement']=prefix.rstrip('_')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-depth',type=int,default=3)
    parser.add_argument('--extended',action='store_true',help='Use extended certificate at the maximum depth.')
    parser.add_argument('--image1',action='store_true')
    parser.add_argument('--prefix',default='')
    args = parser.parse_args()
    reports = []
    for depth in range(args.max_depth+1):
        r = check(depth,args.extended and depth==args.max_depth,args.prefix or ('image1_' if args.image1 else ''))
        reports.append(r)
        print(json.dumps({k:v for k,v in r.items() if k!='seed196_language_obstruction'}),flush=True)
    label=args.prefix.rstrip('_') or ('image1' if args.image1 else '')
    filename='independent_replay%s%s.json'%(('_'+label) if label else '', '_extended' if args.extended else '')
    (HERE/filename).write_text(json.dumps(reports,indent=2)+'\n')
