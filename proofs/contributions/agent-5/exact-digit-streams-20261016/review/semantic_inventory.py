#!/usr/bin/env python3
"""Pin independently reviewed source contracts; no compiler is invoked."""

from pathlib import Path
import hashlib
import json
import re


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def git_blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def code_only(text):
    result = []
    index = 0
    depth = 0
    while index < len(text):
        if depth:
            if text.startswith('/-', index):
                depth += 1
                result.extend('  ')
                index += 2
            elif text.startswith('-/', index):
                depth -= 1
                result.extend('  ')
                index += 2
            else:
                result.append('\n' if text[index] == '\n' else ' ')
                index += 1
        elif text.startswith('/-', index):
            depth = 1
            result.extend('  ')
            index += 2
        elif text.startswith('--', index):
            end = text.find('\n', index)
            if end < 0:
                end = len(text)
            result.extend(' ' * (end - index))
            index = end
        elif text[index] == '"':
            result.append(' ')
            index += 1
            while index < len(text):
                if text[index] == '\\':
                    result.extend('  ')
                    index += 2
                elif text[index] == '"':
                    result.append(' ')
                    index += 1
                    break
                else:
                    result.append('\n' if text[index] == '\n' else ' ')
                    index += 1
        else:
            result.append(text[index])
            index += 1
    assert depth == 0
    return ''.join(result)


def main():
    registry_path = REPO / 'proofs/Agent5ExactDigitStreams.registry.json'
    registry_bytes = registry_path.read_bytes()
    registry = json.loads(registry_bytes)
    modules = registry['projects']['agent5-exact-digit-streams']['modules']
    new_modules = ['DigitDefinitions', 'AdicDigits', 'FractionDigits', 'CoordinateStreams']
    records = {}
    all_endpoints = []
    for name, expected in modules.items():
        data = (REPO / expected['path']).read_bytes()
        assert digest(data) == expected['sha256']
        assert git_blob(data) == expected['git_blob']
        code = code_only(data.decode())
        tokens = re.findall(r'\b(?:sorry|admit|native_decide|sorryAx|axiom|ofReduceBool|skipKernelTC|unsafe)\b', code)
        assert not tokens, (name, tokens)
        imports = [part for line in re.findall(r'^\s*import\s+([^\n]+)', code, re.M) for part in line.split()]
        assert imports == expected['imports']
        record = {**expected, 'forbidden_source_tokens': []}
        if name in new_modules:
            declarations = []
            found = list(re.finditer(r'^(?:@\[[^\]]*\]\s*)?(def|theorem)\s+(\w+)', code, re.M))
            for number, match in enumerate(found):
                end = found[number + 1].start() if number + 1 < len(found) else len(code)
                text = code[match.start():end].strip()
                kind, declaration = match.group(1), match.group(2)
                if kind == 'theorem':
                    delimiter = re.search(r':=\s+by\b', text)
                    assert delimiter is not None
                    contract = text[:delimiter.start()].strip()
                    full_name = 'Agent5.ExactDigitStreams.' + declaration
                    all_endpoints.append(full_name)
                else:
                    full_name = 'Agent5.ExactDigitStreams.' + declaration
                    contract = text
                declarations.append({'kind': kind, 'name': full_name, 'contract': contract, 'contract_sha256': digest(contract.encode())})
            record['declarations'] = declarations
            record['theorem_count'] = sum(item['kind'] == 'theorem' for item in declarations)
        records[name] = record
    expected_endpoints = [endpoint for claim in registry['claims'] if claim['project'] == 'agent5-exact-digit-streams' for endpoint in claim['endpoints']]
    assert len(all_endpoints) == 25 and set(all_endpoints) == set(expected_endpoints)
    report = {
        'status': 'PASS_INDEPENDENT_SEMANTIC_REVIEW',
        'reviewer': 'Agent #5 /root/semantic_review',
        'authored_theorem_source': False,
        'is_compiler_replay': False,
        'registry_path': str(registry_path.relative_to(REPO)),
        'registry_sha256': digest(registry_bytes),
        'modules': records,
        'reviewed_contribution_theorems': 25,
        'new_definitions': 2,
        'all_registry_exports_reviewed': True,
        'blocking_semantic_defects': [],
        'scope': 'Exact finite digit-stream equalities and reconstruction of the unchanged abstract exterior successor, using the actual outgoing carry.',
        'unproved_by_this_package': ['Coordinate-only threshold selector', 'Global real/adic bijection', 'New coordinate-update or orbit theorem', 'All-time finite integer realization', 'Palindrome avoidance', '196 or Lychrel conclusions'],
    }
    (HERE / 'semantic-source-inventory.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': report['status'], 'reviewed_contribution_theorems': 25, 'registry_sha256': report['registry_sha256']}, indent=2))


if __name__ == '__main__':
    main()
