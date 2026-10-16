#!/usr/bin/env python3
"""Pin the two frozen sources and their attributed thirteen-module baseline."""

from pathlib import Path
import json
import re
import sys

sys.dont_write_bytecode = True
from source_identity import code_only, digest, git_blob

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[4]
CONTRIBUTION = HERE.parent


def main():
    inherited_path = CONTRIBUTION/'author/raw-prefix/inherited-artifacts.json'
    inherited = json.loads(inherited_path.read_text())
    records, declarations, endpoints = {}, {}, []
    paths = [(item['module'], item['repository_source'], item['source_sha256'], item['git_blob'])
             for item in inherited['modules'] + inherited['new_arithmetic_dependencies']]
    frozen = {'RawPrefixStreams': '348bd1acf180a35b4cc60a805d417f7ee07a949fcf91761232f682aa5f5ddee6',
              'OrdinaryStreamStep': 'ef186b6f9f631231cbd7fcb7d074f2ad6461783f25bb11672577eb3b29c38177'}
    for module, expected in frozen.items():
        path = CONTRIBUTION/(module+'.lean')
        paths.append((module, str(path.relative_to(REPO)), expected, git_blob(path.read_bytes())))
    for module, path, expected_sha, expected_blob in paths:
        data = (REPO/path).read_bytes()
        assert digest(data) == expected_sha and git_blob(data) == expected_blob, module
        code = code_only(data.decode())
        forbidden = re.findall(r'\b(?:sorry|admit|native_decide|sorryAx|axiom|ofReduceBool|skipKernelTC|unsafe)\b', code)
        assert not forbidden, (module, forbidden)
        imports = [part for line in re.findall(r'^\s*import\s+([^\n]+)', code, re.M) for part in line.split()]
        records[module] = {'path': path, 'sha256': expected_sha, 'git_blob': expected_blob, 'imports': imports}
        if module in frozen:
            found = list(re.finditer(r'^theorem\s+(\w+)', code, re.M))
            declarations[module] = []
            for index, match in enumerate(found):
                end = found[index+1].start() if index+1 < len(found) else len(code)
                text = code[match.start():end]
                delimiter = re.search(r':=\s+by\b', text)
                assert delimiter is not None
                contract = text[:delimiter.start()].strip()
                name = 'Agent5.OrdinaryStreamPrefix.' + match.group(1)
                endpoints.append(name)
                declarations[module].append({'name': name, 'contract': contract,
                                             'contract_sha256': digest(contract.encode())})
    assert len(records) == 15 and len(endpoints) == 6
    order, seen, active = [], set(), set()

    def visit(module):
        if module not in records:
            assert module.split('.')[0] in {'Init', 'Std', 'Lean'}
            return
        assert module not in active
        if module in seen:
            return
        active.add(module)
        for dep in records[module]['imports']:
            visit(dep)
        active.remove(module)
        seen.add(module)
        order.append(module)

    visit('OrdinaryStreamStep')
    assert seen == set(records) and order[-2:] == list(frozen)
    registry = {'schema_version': 1, 'catalogue_complete': False,
                'catalogue_blockers': ['Independent scoped two-module review; no repository-wide claim.'],
                'toolchain': {'version': '4.19.0', 'commit': '6caaee842e94',
                              'allowed_axioms': ['propext', 'Classical.choice', 'Quot.sound']},
                'projects': {'agent5-ordinary-stream-prefix': {
                    'scope': 'Exact one-step raw pair prefix of length B.length+1 under the original surrounded shape with bands gap+2; canonical numeral conclusions bundled under DecimalDigits and PositiveLast.',
                    'roots': ['OrdinaryStreamStep'], 'modules': records}},
                'claims': [{'id': 'A5-ORDINARY-RAW-PREFIX', 'project': 'agent5-ordinary-stream-prefix', 'endpoints': endpoints}]}
    registry_data = (json.dumps(registry, indent=2)+'\n').encode()
    (HERE/'registry.json').write_bytes(registry_data)
    prior_audit = REPO/'proofs/contributions/agent-5/exact-digit-streams-20261016/verification/canonical-prepublication/agent5-exact-digit-streams/source/ProjectAudit.lean'
    prior_text = prior_audit.read_text()
    body = prior_text[prior_text.index('  let allowed : List Name :='):]
    audit = 'import OrdinaryStreamStep\nimport Lean\nopen Lean Elab Command\nset_option maxRecDepth 100000\nset_option maxHeartbeats 0\n' + '\n'.join('#check '+e for e in endpoints) + '\nrun_cmd do\n  let env ← getEnv\n  let selected : List String := ' + json.dumps(order) + '\n' + body
    (HERE/'ProjectAudit.lean').write_text(audit)
    inventory = {'status': 'PASS_INDEPENDENT_SOURCE_AND_CONTRACT_REVIEW',
                 'claim_commit_supplied_by_parent': 'e981de251ef29b24578dfe8bd79cdd2ba36c24f4',
                 'reviewer': 'Agent #5 /root/semantic_review', 'authored_any_reviewed_theorem': False,
                 'registry_origin': 'Reviewer-generated snapshot from author source pins plus the two frozen new modules; does not replace parent canonical registry.',
                 'registry_sha256': digest(registry_data), 'modules': records, 'build_order': order,
                 'new_source_contracts': declarations, 'new_exports': endpoints,
                 'inherited_module_count': 13, 'new_module_count': 2,
                 'source_forbidden_token_scan': 'PASS on all fifteen exact source modules',
                 'inherited_artifact_index_path': str(inherited_path.relative_to(REPO)),
                 'inherited_artifact_index_sha256': digest(inherited_path.read_bytes()),
                 'audit_template_path': str(prior_audit.relative_to(REPO)),
                 'audit_template_sha256': digest(prior_audit.read_bytes()),
                 'audit_body_unchanged': True, 'audit_source_sha256': digest(audit.encode()),
                 'blocking_semantic_defects': [],
                 'shape_convention': 'surrounded B c gap W = B ++ replicate (gap+2) c ++ W ++ replicate (gap+2) c ++ B.reverse',
                 'raw_endpoint_scope': 'Structural word equality, no DecimalDigits or PositiveLast assumption; does not itself identify an arbitrary input word with its canonical integer expansion.',
                 'ordinary_bundle_scope': 'All original reverseAddDigits_correct conclusions plus the exact raw pair prefix, under DecimalDigits D and PositiveLast D.',
                 'unproved_scope': ['Longer actual stream prefixes without further gap hypotheses', 'Shape persistence through another step', 'All-time finite integer realization', 'Infinite safe orbit', 'Palindrome avoidance', '196 or Lychrel conclusions']}
    (HERE/'semantic-source-inventory.json').write_text(json.dumps(inventory, indent=2)+'\n')
    print(json.dumps({'status': inventory['status'], 'modules': len(records), 'new_exports': len(endpoints),
                      'registry_sha256': digest(registry_data), 'audit_sha256': digest(audit.encode())}))


if __name__ == '__main__':
    main()
