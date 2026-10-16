"""Independent reachability and incomparability audit of a bounded snapshot."""
from collections import Counter, defaultdict
from pathlib import Path
import gzip
import hashlib
import json

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
SOURCE = ROOT/'main_existence_attempt/return_pass/language'
snapshot = HERE/'antichain_depth0.json.gz'
data = json.load(gzip.open(snapshot, 'rt'))
nfa_path = SOURCE/'safe_image2_nfa.json'
d0_path = SOURCE/'observation_depth0.json'
assert hashlib.sha256(nfa_path.read_bytes()).hexdigest() == data['nfa_sha256']
assert hashlib.sha256(d0_path.read_bytes()).hexdigest() == data['observer_sha256']
nfa = json.loads(nfa_path.read_text())
d0 = json.loads(d0_path.read_text())
trans = [dict(row) for row in nfa['transitions']]
rows = data['maximal_configurations']
assert len(rows) == data['active']
groups = defaultdict(list)
distinct = set()
largest = 0
for row in rows:
    p = row['pairs']
    assert not p or 1 <= p[0] <= 18
    assert all(type(q) is int and 0 <= q <= 18 for q in p)
    states = set(nfa['initial'])
    obs = 0
    for q in p:
        states = set.union(set(), *(set(trans[u].get(q, ())) for u in states))
        obs = d0['delta'][obs][q]
    assert sorted(states) == row['subset']
    assert obs == row['observer']
    key = obs, tuple(row['subset'])
    assert key not in distinct
    distinct.add(key)
    mask = sum(1 << u for u in states)
    groups[obs].append((mask, tuple(sorted(states))))
    largest = max(largest, len(states))
comparisons = 0
for group in groups.values():
    support = defaultdict(list)
    for i, (mask, states) in enumerate(group):
        for s in states:
            support[s].append(i)
    for i, (mask, states) in enumerate(group):
        if not states:
            assert len(group) == 1
            continue
        candidates = min((support[s] for s in states), key=len)
        for j in candidates:
            other, other_states = group[j]
            if len(other_states) <= len(states):
                continue
            comparisons += 1
            assert mask & other != mask
assert largest == data['largest_configuration']
result = dict(status='INDEPENDENT_REACHABLE_ANTICHAIN_SNAPSHOT_VERIFIED',
              verified_configurations=len(rows),
              observer_class_counts={str(q):len(v) for q,v in sorted(groups.items())},
              largest_configuration=largest, strict_superset_checks=comparisons,
              reachable_downward_closure_status='UNKNOWN',
              forward_language_closure_status='NOT_PROVED',
              snapshot_sha256=hashlib.sha256(snapshot.read_bytes()).hexdigest(),
              nfa_sha256=hashlib.sha256(nfa_path.read_bytes()).hexdigest())
(HERE/'antichain_depth0_audit.json').write_text(json.dumps(result, indent=2)+'\n')
print(json.dumps(result), flush=True)
