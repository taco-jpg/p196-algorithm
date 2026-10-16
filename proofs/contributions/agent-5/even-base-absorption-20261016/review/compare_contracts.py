#!/usr/bin/env python3
"""Independent source contract comparison; this is not a Lean build."""

from pathlib import Path
import hashlib
import json
import re


ROOT = Path(__file__).resolve().parent
ORIGINAL = ROOT.parent / 'agent5-recovery/original/agent5_assumption_discharge'
REPAIRED = ROOT / 'repaired-fixture/proofs/contributions/agent-5/even-base-absorption-20261016'
REPOSITORY = ROOT.parent / 'p196'
MODULES = ['InitialValidity', 'FiniteOverflow']
DEPENDENCIES = [
    'proofs/ExteriorClock__b2b9d37012d53747.lean',
    'proofs/GeneralCarryMass__ad1a2561147adc83.lean',
    'proofs/GeneralMomentAbsorption__d6c541c17a8aa76f.lean',
]


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def git_blob(data):
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def code_only(source):
    """Remove nested comments while retaining newlines and quoted strings."""
    result = []
    index = 0
    nesting = 0
    quoted = False
    while index < len(source):
        if nesting:
            if source.startswith('/-', index):
                nesting += 1
                result.extend('  ')
                index += 2
            elif source.startswith('-/', index):
                nesting -= 1
                result.extend('  ')
                index += 2
            else:
                result.append('\n' if source[index] == '\n' else ' ')
                index += 1
        elif quoted:
            result.append(source[index])
            if source[index] == '\\' and index + 1 < len(source):
                index += 1
                result.append(source[index])
            elif source[index] == '"':
                quoted = False
            index += 1
        elif source.startswith('/-', index):
            nesting = 1
            result.extend('  ')
            index += 2
        elif source.startswith('--', index):
            end = source.find('\n', index)
            if end < 0:
                end = len(source)
            result.extend(' ' * (end - index))
            index = end
        else:
            quoted = source[index] == '"'
            result.append(source[index])
            index += 1
    assert nesting == 0 and not quoted
    return ''.join(result)


def declarations(source):
    source = code_only(source)
    found = list(re.finditer(r'^(def|abbrev|structure|theorem)\s+([A-Za-z0-9_]+)', source, re.M))
    declarations = {}
    for number, match in enumerate(found):
        kind, name = match.group(1), match.group(2)
        end = found[number + 1].start() if number + 1 < len(found) else len(source)
        full = source[match.start():end].strip()
        contract = full[:full.index(':=')].strip() if kind == 'theorem' else full
        assert name not in declarations
        declarations[name] = {'kind': kind, 'contract': contract, 'full': full}
    return declarations


def source_record(path):
    data = path.read_bytes()
    forbidden = re.findall(r'\b(?:sorry|admit|native_decide|sorryAx|axiom|unsafe)\b', code_only(data.decode()))
    return {
        'path': str(path), 'sha256': sha256(data), 'git_blob_sha1': git_blob(data),
        'forbidden_source_tokens': sorted(set(forbidden)),
    }


receipt = {
    'review_kind': 'independent_source_contract_and_semantic_review',
    'is_lean_build': False,
    'repair_patch': source_record(ROOT.parent / 'agent11-agent5-repair.patch'),
    'dependencies': [source_record(REPOSITORY / path) for path in DEPENDENCIES],
    'modules': {},
}

for module in MODULES:
    original = ORIGINAL / (module + '.lean')
    repaired = REPAIRED / (module + '.lean')
    old = declarations(original.read_text())
    new = declarations(repaired.read_text())
    assert list(old) == list(new)
    records = []
    for name in old:
        assert old[name]['kind'] == new[name]['kind']
        assert old[name]['contract'] == new[name]['contract'], name
        records.append({
            'name': 'P196.Agent5.General.InitialValidity.' + name,
            'kind': old[name]['kind'],
            'contract_sha256': sha256(old[name]['contract'].encode()),
            'contract_unchanged': True,
            'proof_text_changed': old[name]['full'] != new[name]['full'],
        })
    receipt['modules'][module] = {
        'original': source_record(original), 'repaired': source_record(repaired),
        'theorem_count': sum(record['kind'] == 'theorem' for record in records),
        'non_theorem_declaration_count': sum(record['kind'] != 'theorem' for record in records),
        'all_contracts_and_definitions_unchanged': True,
        'declarations': records,
    }

receipt['total_theorems'] = sum(module['theorem_count'] for module in receipt['modules'].values())
receipt['total_non_theorem_declarations'] = sum(
    module['non_theorem_declaration_count'] for module in receipt['modules'].values()
)
receipt['changed_proof_declarations'] = [
    declaration['name']
    for module in receipt['modules'].values()
    for declaration in module['declarations']
    if declaration['proof_text_changed']
]
receipt['status'] = 'PASS_EXACT_CONTRACTS_AND_DEFINITIONS_UNCHANGED'
(ROOT / 'contract-comparison.json').write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps({
    key: receipt[key] for key in [
        'status', 'total_theorems', 'total_non_theorem_declarations', 'changed_proof_declarations'
    ]
}, indent=2))
