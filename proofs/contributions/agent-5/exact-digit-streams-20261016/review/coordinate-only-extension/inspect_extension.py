#!/usr/bin/env python3
"""Pin the coordinate-only extension and exercise its new selector boundary.

This script invokes no compiler and does not alter the frozen core review.
The finite controls supplement exact-statement review; they are not a proof.
"""

from pathlib import Path
from itertools import product
import json
import re
import sys

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
REVIEW = HERE.parent
REPO = REVIEW.parents[4]
sys.path.insert(0, str(REVIEW))
from semantic_inventory import code_only, digest, git_blob


def normalize(word, carry):
    digits = []
    for x in word:
        digit = (x + carry) % 10
        carry = (x + carry) // 10
        digits.append(digit)
    return digits, carry


def high_value(word):
    value = 0
    for x in word:
        value = 10 * value + x
    return value


def strip(c, word):
    while word and word[-1] == c:
        word.pop()
    return word


def outer_next(c, word):
    k = int(c >= 10)
    t = c - 9 * k
    low, e = normalize(word, 0)
    right, g = normalize(word[::-1], k)
    u = max(0, c + e - 10 * k)
    opposite = right[::-1] + [t] if g == 0 else [1] + right[::-1]
    return (2 * t, strip(2 * t, [x + y for x, y in zip(low + [u], opposite)]))


def coordinate_successor(c, word, count, use_quotient=False):
    length = len(word)
    low_value = sum(x * 10**i for i, x in enumerate(word))
    a = 9 * low_value - c * 10**length
    r = 9 * high_value(word) + c
    base = 9 * 10**length
    g = r // base if use_quotient else int(base <= r)
    denominator = base * 10**g
    low, high = [], []
    for _ in range(count):
        d = (-a) % 10
        assert (a - 9 * d) % 10 == 0
        a = (a - 9 * d) // 10
        low.append(d)
        d, r = divmod(10 * r, denominator)
        high.append(d)
    phase = 2 * (c - 9 * int(c >= 10))
    return (phase, strip(phase, [x + y for x, y in zip(low, high)]))


def main():
    registry_data = (HERE / 'registry.json').read_bytes()
    registry = json.loads(registry_data)
    project = registry['projects']['agent5-exact-digit-streams']
    core = json.loads((REVIEW / 'semantic-source-inventory.json').read_text())
    records = {}
    new_theorems = []
    for module, expected in project['modules'].items():
        data = (REPO / expected['path']).read_bytes()
        assert digest(data) == expected['sha256']
        assert git_blob(data) == expected['git_blob']
        code = code_only(data.decode())
        forbidden = re.findall(r'\b(?:sorry|admit|native_decide|sorryAx|axiom|ofReduceBool|skipKernelTC|unsafe)\b', code)
        assert not forbidden, (module, forbidden)
        imports = [part for line in re.findall(r'^\s*import\s+([^\n]+)', code, re.M) for part in line.split()]
        assert imports == expected['imports']
        record = {**expected, 'forbidden_source_tokens': []}
        if module in core['modules']:
            assert data == (REVIEW / 'strict-replay-01/source' / (module + '.lean')).read_bytes()
            assert expected['sha256'] == core['modules'][module]['sha256']
            record['same_bytes_as_frozen_independent_core_review'] = True
        else:
            namespace = 'Agent6.ExteriorCoordinates.' if module == 'CoordinateThreshold' else 'Agent5.ExactDigitStreams.'
            found = list(re.finditer(r'^(def|theorem)\s+(\w+)', code, re.M))
            declarations = []
            for index, match in enumerate(found):
                end = found[index + 1].start() if index + 1 < len(found) else len(code)
                declaration = code[match.start():end].strip()
                declaration = re.sub(r'\nend\s+[\w.]+\s*$', '', declaration).strip()
                kind, name = match.group(1), namespace + match.group(2)
                if kind == 'theorem':
                    body = re.search(r':=\s+by\b', declaration)
                    assert body is not None
                    contract = declaration[:body.start()].strip()
                    if module == 'CoordinateOnlyStreams':
                        new_theorems.append(name)
                else:
                    contract = declaration
                declarations.append({'kind': kind, 'name': name, 'contract': contract, 'contract_sha256': digest(contract.encode())})
            record['declarations'] = declarations
            record['written_public_theorem_count'] = sum(d['kind'] == 'theorem' for d in declarations)
            record['written_definition_count'] = sum(d['kind'] == 'def' for d in declarations)
        records[module] = record
    endpoints = [e for c in registry['claims'] for e in c['endpoints']]
    core_endpoints = [d['name'] for m in core['modules'].values() for d in m.get('declarations', []) if d['kind'] == 'theorem']
    assert len(endpoints) == 30 and len(new_theorems) == 5
    assert set(endpoints) == set(core_endpoints + new_theorems)
    assert records['CoordinateThreshold']['written_public_theorem_count'] == 16
    immutable = []
    for line in (REVIEW / 'REVIEW_MANIFEST.sha256').read_text().splitlines():
        expected, path = line.split('  ', 1)
        assert digest((REVIEW / path).read_bytes()) == expected, path
        immutable.append(path)
    inventory = {
        'status': 'PASS_INDEPENDENT_EXTENSION_SEMANTIC_REVIEW',
        'reviewer': 'Agent #5 /root/semantic_review',
        'authored_any_reviewed_theorem': False,
        'registry_sha256': digest(registry_data),
        'modules': records,
        'new_agent5_exports': new_theorems,
        'total_agent5_exports': 30,
        'agent6_written_public_theorems_reviewed': 16,
        'agent6_definitions_reviewed': 3,
        'core_manifest_sha256': digest((REVIEW / 'REVIEW_MANIFEST.sha256').read_bytes()),
        'frozen_core_review_files_verified_unchanged': immutable,
        'blocking_semantic_defects': [],
        'proved_extension_scope': 'Coordinate-only reconstruction of the unchanged abstract exterior successor using phase, length, zValue and rhoNum at every cutoff >= B.length + 1, with nonneutralPhase c and all coefficients <= 18.',
        'unproved_scope': ['Global real/adic bijection', 'New coordinate update theorem', 'Exterior cycle or safe infinite orbit', 'All-time finite integer realization', 'Palindrome avoidance', '196 or Lychrel conclusions'],
    }
    (HERE / 'semantic-source-inventory.json').write_text(json.dumps(inventory, indent=2) + '\n')

    allowed_phases = [c for c in range(18) if c != 9]
    counts = {'arbitrary_coefficient_quotient_and_zero_criterion': 0,
              'bounded_eight_phase_selector_states': 0,
              'coordinate_endpoint_prefixes': 0,
              'empty_word_phase_characterization': 0}
    for length in range(4):
        for word in product([0, 1, 9, 10, 18, 19, 20, 99], repeat=length):
            for c in allowed_phases:
                g = normalize(word[::-1], int(c >= 10))[1]
                r, denominator = 9 * high_value(word) + c, 9 * 10**length
                assert g == r // denominator
                assert (g == 0) == (r < denominator)
                counts['arbitrary_coefficient_quotient_and_zero_criterion'] += 1
    for length in range(4):
        for word in product(range(19), repeat=length):
            for c in [2, 4, 6, 8, 10, 12, 14, 16]:
                g = normalize(word[::-1], int(c >= 10))[1]
                r, denominator = 9 * high_value(word) + c, 9 * 10**length
                selector = int(denominator <= r)
                assert g == selector == r // denominator
                assert 0 < r < 2 * denominator
                assert 0 < r < denominator * 10**selector
                counts['bounded_eight_phase_selector_states'] += 1
                if length <= 2:
                    for tail in [0, 1, 4]:
                        cut = length + 1 + tail
                        actual = outer_next(c, list(word))
                        assert coordinate_successor(c, word, cut) == actual
                        assert coordinate_successor(c, word, cut, use_quotient=True) == actual
                        counts['coordinate_endpoint_prefixes'] += 1
    for c in range(100):
        g = normalize([], int(c >= 10))[1]
        assert (g == c // 9) == (c <= 17 and c != 9)
        counts['empty_word_phase_characterization'] += 1
    assert normalize([10], 0)[1] == 1  # Agent6's equality boundary c=0, B=[10].
    assert 9 * high_value([10]) == 9 * 10
    assert outer_next(12, []) == coordinate_successor(12, [], 1) == (6, [3])
    excluded = {}
    for c in [9, 18]:
        g = normalize([], int(c >= 10))[1]
        excluded[str(c)] = {'actual_empty_carry': g, 'rho_quotient': c // 9}
        assert g != c // 9
    c, word = 2, [20]
    r, denominator = 9 * high_value(word) + c, 90
    unbounded = {'state': {'c': c, 'B': word}, 'actual_carry': normalize(word[::-1], 0)[1],
                 'threshold_selector': int(denominator <= r), 'rho_quotient': r // denominator,
                 'actual_successor': outer_next(c, word), 'invalid_threshold_successor': coordinate_successor(c, word, 2),
                 'invalid_quotient_successor': coordinate_successor(c, word, 2, use_quotient=True)}
    assert unbounded['actual_carry'] == 2 and unbounded['threshold_selector'] == 1
    assert unbounded['actual_successor'] != unbounded['invalid_threshold_successor']
    assert unbounded['actual_successor'] != unbounded['invalid_quotient_successor']
    controls = {'status': 'PASS_EXTENSION_BOUNDARY_CONTROLS',
                'proof_status': 'Finite exact-integer controls only; no compiler invoked by this script.',
                'counts': counts,
                'empty_phase_12': {'rho_numerator': 12, 'base_denominator': 9, 'selector': 1, 'scaled_denominator': 90, 'adic_numerator': -12, 'successor': [6, [3]]},
                'equality_threshold': {'c': 0, 'B': [10], 'rho_numerator': 90, 'base_denominator': 90, 'actual_carry': 1, 'belongs_to_agent6_phase_domain': True, 'belongs_to_agent5_phase_domain': False},
                'excluded_phase_controls': excluded,
                'coefficient_bound_control': unbounded}
    (HERE / 'boundary-controls.json').write_text(json.dumps(controls, indent=2) + '\n')
    print(json.dumps({'semantic_status': inventory['status'], 'new_agent5_exports': len(new_theorems), 'immutable_core_files': len(immutable), 'controls': counts}))


if __name__ == '__main__':
    main()
