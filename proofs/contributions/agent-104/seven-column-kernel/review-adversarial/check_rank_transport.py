#!/usr/bin/env python3
"""Data-transport diagnostic only. Does not verify predecessor closure."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import re
import resource

resource.setrlimit(resource.RLIMIT_CPU, (20, 25))
resource.setrlimit(resource.RLIMIT_AS, (500 * 1024**2, 500 * 1024**2))
HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
DATA = HERE.parent/'certificate'
CERT = ROOT/'proofs/contributions/2026-10-15-seven-column-prefix/certificate_739.json'
definitions = {}
hashes = {}


def parse_expr(tokens, start=0):
    t = tokens[start]
    if t == '(':
        node, pos = parse_expr(tokens, start+1)
        assert tokens[pos] == ')'
        return node, pos+1
    if t == '.empty':
        return None, start+1
    if t != '.node':
        assert t in definitions, t
        return definitions[t], start+1
    key = int(tokens[start+1])
    assert tokens[start+2] == '['
    word = []; pos = start+3
    while tokens[pos] != ']':
        if tokens[pos] != ',':
            word.append(int(tokens[pos]))
        pos += 1
    rank = int(tokens[pos+1])
    left, pos = parse_expr(tokens, pos+2)
    right, pos = parse_expr(tokens, pos)
    return (key, tuple(word), rank, left, right), pos


for path in sorted(DATA.glob('Rank739Data[0-9][0-9].lean')):
    data = path.read_bytes()
    hashes[str(path.relative_to(ROOT))] = hashlib.sha256(data).hexdigest()
    for line in data.decode().splitlines():
        if not line.startswith('def '):
            continue
        name, expr = re.fullmatch(r'def (\w+) : RankTree := (.*)', line).groups()
        tokens = re.findall(r'\.node|\.empty|\w+|[(),\[\]]', expr)
        node, pos = parse_expr(tokens)
        assert pos == len(tokens)
        assert name not in definitions
        definitions[name] = node

root_path = DATA/'Rank739.lean'
root_data = root_path.read_bytes()
hashes[str(root_path.relative_to(ROOT))] = hashlib.sha256(root_data).hexdigest()
root_name = re.search(r'^def ranks : RankTree := (\w+)\s*$', root_data.decode(), re.M).group(1)
tree = definitions[root_name]
seen = Counter(); codes = {}; stack = [tree]
while stack:
    node = stack.pop()
    if node is None:
        continue
    key, word, rank, left, right = node
    code = 1
    for digit in word:
        code = 19*code+digit
    assert code == key
    seen[(word, rank)] += 1
    assert word not in codes
    codes[word] = key
    stack.extend((left, right))

cert = json.loads(CERT.read_text())
expected = Counter((tuple(row['word']), row['rank']) for row in cert['nodes'])
assert seen == expected
for word, rank in seen:
    node = tree
    key = codes[word]
    while node:
        pivot, stored_word, stored_rank, left, right = node
        if key < pivot:
            node = left
        elif pivot < key:
            node = right
        else:
            assert stored_word == word and stored_rank == rank
            break
    else:
        raise AssertionError(('unreachable lookup', word))

result = {'status': 'PASS_DATA_TRANSPORT_ONLY', 'root': root_name,
          'source_certificate_sha256': hashlib.sha256(CERT.read_bytes()).hexdigest(),
          'definitions': len(definitions), 'reachable_nodes': sum(seen.values()),
          'exact_multiset_equality_with_frozen_certificate': True,
          'every_stored_lookup_reaches_its_full_word_and_rank': True,
          'lean_source_sha256': hashes,
          'scope': 'No predecessor enumeration or kernel certificate acceptance performed by this script.'}
(HERE/'rank-transport-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k != 'lean_source_sha256'},indent=2))
