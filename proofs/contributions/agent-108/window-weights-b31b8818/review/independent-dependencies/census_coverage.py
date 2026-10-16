#!/usr/bin/env python3
"""Read-only retrospective census of the historical 112-name audit.

This is a comment-aware source census, not a Lean parser or a kernel audit.
It never edits the historical driver, source copies, logs, or manifests.
"""
from pathlib import Path
import argparse
import collections
import datetime
import hashlib
import json
import re


def strip_comments_and_strings(source):
    """Preserve offsets/newlines while blanking nested Lean comments/strings."""
    out = []
    i = depth = 0
    quote = False
    while i < len(source):
        if depth:
            if source.startswith('/-', i):
                out.extend('  ')
                depth += 1
                i += 2
            elif source.startswith('-/', i):
                out.extend('  ')
                depth -= 1
                i += 2
            else:
                out.append('\n' if source[i] == '\n' else ' ')
                i += 1
        elif quote:
            if source[i] == '\\' and i + 1 < len(source):
                out.extend('  ')
                i += 2
            elif source[i] == '"':
                out.append(' ')
                quote = False
                i += 1
            else:
                out.append('\n' if source[i] == '\n' else ' ')
                i += 1
        elif source.startswith('/-', i):
            out.extend('  ')
            depth = 1
            i += 2
        elif source.startswith('--', i):
            j = source.find('\n', i)
            if j < 0:
                j = len(source)
            out.extend(' ' * (j - i))
            i = j
        elif source[i] == '"':
            out.append(' ')
            quote = True
            i += 1
        else:
            out.append(source[i])
            i += 1
    assert depth == 0 and not quote
    assert len(out) == len(source)
    return ''.join(out)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dependencies', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    evidence = Path(__file__).resolve().parent
    dep = args.dependencies.resolve()
    modules = dep / 'modules'
    order = ['LychrelDigitSums', 'Trace', 'WholeWord', 'Safety', 'Indexing',
             'FiniteWords', 'FamilyStates', 'Products', 'Obstruction', 'CarryPath']
    old_regex = r'^(?:noncomputable )?(?:def|theorem|abbrev)\s+([A-Za-z0-9_]+)'
    expanded_regex = (
        r'^[ \t]*(?:@\[[^\]\n]*\][ \t]*)*'
        r'(?P<modifiers>(?:(?:private|protected|noncomputable|unsafe|partial)[ \t]+)*)'
        r'(?P<kind>def|theorem|lemma|abbrev|axiom|opaque|instance|inductive|structure|class)'
        r'[ \t]+(?P<name>[^\s({:]+)'
    )
    expanded = re.compile(expanded_regex, re.M)
    manifest = json.loads((evidence / 'REVIEW_MANIFEST.json').read_text())
    old_evidence_checks = []
    for relative, expected in manifest['files'].items():
        actual = sha256(evidence / relative)
        old_evidence_checks.append({'file': relative, 'expected_sha256': expected,
                                    'actual_sha256': actual, 'unchanged': actual == expected})
    assert all(x['unchanged'] for x in old_evidence_checks)
    source_map = json.loads((dep / 'source-map.json').read_text())
    sources = {Path(x['module_copy']).stem: x for x in source_map['files']}
    records = []
    generated_names = []
    for module in order:
        path = modules / (module + '.lean')
        source = path.read_text()
        actual_hash = sha256(path)
        assert actual_hash == sources[module]['sha256']
        stripped = strip_comments_and_strings(source)
        old_matches = list(re.finditer(old_regex, source, re.M))
        old_lines = {source.count('\n', 0, m.start()) + 1 for m in old_matches}
        declared = []
        for m in expanded.finditer(stripped):
            line = source.count('\n', 0, m.start()) + 1
            declared.append({'line': line, 'kind': m['kind'], 'name': m['name'],
                             'modifiers': m['modifiers'].split(),
                             'in_old_generated_audit': module != order[0] and line in old_lines})
        if module != order[0]:
            namespace = ('Agent13BufferedFamily' if module == 'CarryPath' else
                         'Agent13ProductWeights' if module in
                         ['FiniteWords', 'FamilyStates', 'Products', 'Obstruction'] else
                         'Agent13FoldedFamily')
            generated_names.extend(namespace + '.' + m.group(1) for m in old_matches)
        records.append({
            'module': module,
            'source_commit': sources[module]['source_commit'],
            'repo_path': sources[module]['repo_path'],
            'git_blob': sources[module]['git_blob'],
            'sha256': actual_hash,
            'compiled_by_old_driver': True,
            'selected_by_old_enumeration': module != order[0],
            'old_regex_raw_matches': len(old_matches),
            'old_generated_audit_count': len(old_matches) if module != order[0] else 0,
            'comment_aware_explicit_count': len(declared),
            'kind_counts': dict(collections.Counter(x['kind'] for x in declared)),
            'private_explicit_count': sum('private' in x['modifiers'] for x in declared),
            'source_embedded_print_axioms_count': len(re.findall(r'^\s*#print axioms ', stripped, re.M)),
            'declarations': declared,
        })
    audit_source = (evidence / 'IndependentDependencyAudit.lean').read_text()
    historical_names = re.findall(r'^#print axioms (\S+)$', audit_source, re.M)
    assert generated_names == historical_names
    assert len(generated_names) == 112
    old_results = json.loads((evidence / 'build-results-approved02.json').read_text())
    assert old_results['all_pass'] and old_results['audited_declarations'] == 112
    assert all(x['exit_code'] == 0 for x in old_results['records'])
    assert not any('--trust=0' in x['command'] for x in old_results['records'])
    output = {
        'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'scope': 'Retrospective source enumeration only; no new compilation or kernel audit.',
        'old_strategy': 'order[1:], then original column-zero def/theorem/abbrev regex',
        'old_regex': old_regex,
        'comment_aware_regex': expanded_regex,
        'old_generated_audit_exactly_reproduced': generated_names == historical_names,
        'old_generated_audit_count': len(generated_names),
        'old_commands_explicit_trust_zero': False,
        'core_seven_explicit_count': sum(x['comment_aware_explicit_count'] for x in records[:7]),
        'core_seven_old_generated_audit_count': sum(x['old_generated_audit_count'] for x in records[:7]),
        'ten_modules_explicit_count': sum(x['comment_aware_explicit_count'] for x in records),
        'ten_modules_absent_from_old_generated_audit': sum(
            sum(not d['in_old_generated_audit'] for d in x['declarations']) for x in records),
        'old_evidence_checks': old_evidence_checks,
        'modules': records,
        'generated_names': generated_names,
        'limitations': [
            'This lexical source census does not enumerate generated Lean environment constants.',
            'Source-embedded #print axioms outputs remain in the historical compile logs; absence '
            'from the generated 112-name file does not mean a declaration never appeared in any log.',
            'The separate recovered Lychrel196Research file was not an eleventh compiled module; '
            'its original text is incorporated in the pinned LychrelDigitSums source.',
        ],
    }
    with args.output.open('x') as f:
        json.dump(output, f, indent=2)
        f.write('\n')
    print(json.dumps({k: output[k] for k in [
        'old_generated_audit_exactly_reproduced', 'old_generated_audit_count',
        'core_seven_explicit_count', 'core_seven_old_generated_audit_count',
        'ten_modules_explicit_count', 'ten_modules_absent_from_old_generated_audit']}))


if __name__ == '__main__':
    main()
