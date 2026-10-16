#!/usr/bin/env python3
"""Validate retained canonical output; never edit proof sources or checker output."""
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path('/workspace/scratch/4b20b8469eb3/p196-algorithm')
BASE = Path('/workspace/scratch/4b20b8469eb3/agent10-eight/canonical-build-004')
RECEIPT = BASE.with_name(BASE.name + '-specialist-validation.json')
COMMIT = 'f156ea95f4f64609da218632820f71378c815411'
PROJECT = 'agent10-nine-carry-sharp'
CHECKER = 'proofs/verify_project__214bf7673efe116b.py'
REGISTRY = 'proofs/Agent10NineCarrySharp.registry.json'
ALLOWED = {'Classical.choice', 'Quot.sound', 'propext'}
if len(sys.argv) != 2 or re.fullmatch(r'[0-9a-f]{64}', sys.argv[1]) is None:
    raise SystemExit('usage: validate_canonical_gate_004.py EXPECTED_REPORT_SHA256')
EXPECTED_REPORT_SHA256 = sys.argv[1]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def git_bytes(path):
    return subprocess.check_output(['git', 'show', COMMIT + ':' + path], cwd=ROOT)


def axs(text):
    return sorted(x.strip() for x in text.strip()[1:-1].split(',') if x.strip())


report_bytes = (BASE / 'verification.json').read_bytes()
report = json.loads(report_bytes)
pr = report['projects'][PROJECT]
assert report['status'] == pr['status'] == 'PASS'
assert report['source_commit'] == COMMIT and report['source_tree_clean']
assert report['agent'] == 'Agent #1'
assert report['mathematical_proof_check'] is True
assert report['repository_wide_pass'] is False
assert report['catalogue_complete'] is False

registry_bytes = (ROOT / REGISTRY).read_bytes()
assert registry_bytes == git_bytes(REGISTRY)
assert sha(registry_bytes) == report['registry_sha256'] == '01cac4b7bf8094d50a368e3798fefa548b85b911c3bab58a788e8d3f9ee5ab72'
registry = json.loads(registry_bytes)
spec = registry['projects'][PROJECT]
checker_bytes = (ROOT / CHECKER).read_bytes()
assert checker_bytes == git_bytes(CHECKER)

manifest_bytes = (BASE / 'FILES.json').read_bytes()
manifest = json.loads(manifest_bytes)
actual_files = {str(p.relative_to(BASE)) for p in BASE.rglob('*')
                if p.is_file() and p.suffix != '.olean' and p.name != 'FILES.json'}
assert actual_files == set(manifest)
for rel, item in manifest.items():
    data = (BASE / rel).read_bytes()
    assert len(data) == item['bytes'] and sha(data) == item['sha256'], rel
assert len(manifest) == 35

sources = {}
for name, pin in spec['modules'].items():
    current = (ROOT / pin['path']).read_bytes()
    staged = (BASE / PROJECT / 'source' / (name + '.lean')).read_bytes()
    assert current == staged == git_bytes(pin['path']), name
    assert sha(current) == pin['sha256'] == pr['sources'][name]['sha256']
    assert sha(staged) == pr['sources'][name]['build_sha256']
    blob = hashlib.sha1(f'blob {len(current)}\0'.encode() + current).hexdigest()
    assert blob == pin['git_blob'], name
    assert not pin.get('adapter') and not pr['sources'][name].get('adapter')
    sources[name] = dict(path=pin['path'], sha256=sha(current), git_blob=blob,
                         bytes=len(current), commit_worktree_build_identical=True)
assert len(sources) == 16
assert [c['label'] for c in pr['commands']] == pr['build_order'] + ['ProjectAudit']
assert len(pr['commands']) == 17
for command in pr['commands']:
    assert command['exit_code'] == 0
    assert sha((BASE / command['log']).read_bytes()) == command['log_sha256']

audit_path = BASE / PROJECT / 'logs' / 'ProjectAudit.log'
audit_bytes = audit_path.read_bytes()
audit = audit_bytes.decode()
records = re.findall(r'^AUDIT_THEOREM (\S+) (\S+) :\s*(\[[^\]]*\])', audit, re.M)
headers = re.findall(r'^AUDIT_THEOREM (\S+) (\S+) :', audit, re.M)
summary = re.findall(r'^FULL_MODULE_AUDIT theorems=(\d+) union=(\[[^\]]*\])$', audit, re.M)
assert len(summary) == 1
assert len(records) == len(headers) == int(summary[0][0]) == pr['theorem_count']
assert len({name for _, name, _ in records}) == len(records)
assert {(mod, name) for mod, name, _ in records} == set(headers)
by_name = {name: {'origin_module': mod, 'axioms': axs(used)} for mod, name, used in records}
counts = dict(sorted(Counter(mod for mod, _, _ in records).items()))
assert set(counts) == set(sources)
union = set()
for mod, name, used in records:
    deps = set(axs(used))
    assert deps <= ALLOWED, name
    union.update(deps)
assert union == set(axs(summary[0][1])) == set(axs(pr['axiom_union'])) == ALLOWED
assert not re.search(r'^(CUSTOM_AXIOM|DISALLOWED_AXIOMS)', audit, re.M)
unsafe = re.findall(r'^UNSAFE_IMPLEMENTATION_AXIOM (\S+) (\S+)$', audit, re.M)
assert len(unsafe) == 13 and len(set(unsafe)) == len(unsafe)
assert all(mod == 'Lychrel196Research' for mod, _ in unsafe)
assert [list(x) for x in unsafe] == pr['unsafe_implementation_axioms']
assert not {name for _, name in unsafe}.intersection(union)

endpoints = [e for claim in registry['claims'] if claim['project'] == PROJECT
             for e in claim.get('endpoints', [])]
assert len(endpoints) == len(set(endpoints)) == 122
assert endpoints == pr['endpoints']
audit_source = (BASE / PROJECT / 'source' / 'ProjectAudit.lean').read_text()
assert re.findall(r'^#check (\S+)$', audit_source, re.M) == endpoints
audit_start = re.search(r'^(?:AUDIT_THEOREM|UNSAFE_IMPLEMENTATION_AXIOM) ', audit, re.M).start()
positions = []
for endpoint in endpoints:
    found = list(re.finditer(r'^' + re.escape(endpoint) + r'(?=\s|:)', audit, re.M))
    assert len(found) == 1 and found[0].start() < audit_start, endpoint
    positions.append(found[0].start())
assert positions == sorted(positions)
endpoint_records = []
EXHAUSTIVE_ONLY = {
    'Agent10ThreeColumnExclusion.observedBit3_value',
    'Agent10ThreeColumnExclusion.state3_valid',
}
explicit_print_count = 0
for index, endpoint in enumerate(endpoints):
    end = positions[index + 1] if index + 1 < len(positions) else audit_start
    formatted_type = audit[positions[index]:end].strip()
    item = by_name[endpoint]
    assert item['origin_module'] == endpoint.split('.')[0]
    module_log = (BASE / PROJECT / 'logs' / (item['origin_module'] + '.log')).read_text()
    pattern = r"^'" + re.escape(endpoint) + r"' (?:depends on axioms:\s*(\[[^\]]*\])|does not depend on any axioms)"
    printed = re.findall(pattern, module_log, re.M)
    module_source = (BASE / PROJECT / 'source' / (item['origin_module'] + '.lean')).read_text()
    source_print_names = re.findall(r'^#print axioms (\S+)\s*$', module_source, re.M)
    source_prints = [name for name in source_print_names
                     if name == endpoint or item['origin_module'] + '.' + name == endpoint]
    has_explicit_print = endpoint not in EXHAUSTIVE_ONLY
    assert len(source_prints) == int(has_explicit_print), endpoint
    assert len(printed) == int(has_explicit_print), endpoint
    if has_explicit_print:
        assert axs(printed[0] or '[]') == item['axioms'], endpoint
        explicit_print_count += 1
    endpoint_records.append(dict(name=endpoint, **item, type_output=formatted_type,
        type_output_sha256=sha(formatted_type.encode()),
        type_log_line_1_based=audit.count('\n', 0, positions[index]) + 1,
        exhaustive_axiom_audit_present=True,
        explicit_source_print_axioms_present=has_explicit_print,
        print_axioms_matches_exhaustive_audit=True if has_explicit_print else None))
assert explicit_print_count == 120
assert {e['name'] for e in endpoint_records if not e['explicit_source_print_axioms_present']} == EXHAUSTIVE_ONLY

types = {e['name']: e['type_output'] for e in endpoint_records}
count_type = types['Agent10SevenStepCount.actual_seven_step_count_all_widths']
assert '(ha : FoldedDecimal.Admissible L q)' in count_type
assert '3 ≤ CarryObservabilityActual.orbitCount q L 7' in count_type
assert '(hL :' not in count_type
for suffix in ['small_difference', 'initial_nonoverflow']:
    text = types['Agent10EightCarry.eight_carry_words_determine_pair_sums_of_' + suffix]
    assert 't < 8' in text and 'i ≤ (OverflowCarryNormalization.iterPairs q L t).fst' in text
    assert 'orbitCount' not in text and '(i : Nat) : i < L → q i = r i' in text
numeric = types['Agent10EightCarry.eight_carry_words_determine_next_integer_of_initial_nonoverflow']
assert 'DecimalDigits.Canonical n d L' in numeric and 'DecimalDigits.Canonical m e L' in numeric
assert '(ho : DecimalDigits.carry (DecimalDigits.columnSum d L) L = 0)' in numeric
assert numeric.endswith('Lychrel196.step n = Lychrel196.step m')
for name in ['rank_seven_minimum_fin', 'singleton_seven_count']:
    assert by_name['Agent10SevenStepCount.' + name]['axioms'] == []

exterior = ' '.join(types['Agent10PrefixExclusion.eight_carries_determine_exterior_pair'].split())
assert 't < 8' in exterior and exterior.endswith(': q 0 = r 0')
assert 'orbitCount' not in exterior and '(ho :' not in exterior
counterexample = ' '.join(types['Agent10SixCarryCounterexample.six_carry_counterexample'].split())
assert 'Canonical 80000571539' in counterexample and 'Canonical 70000817069' in counterexample
assert 't < 6' in counterexample and 'i ≤' in counterexample
assert 'Lychrel196.step 80000571539 ≠ Lychrel196.step 70000817069' in counterexample
six_next = types['Agent10SixCarryCounterexample.next_integer_values']
assert '173518071547' in six_next and '166072617076' in six_next
for short in ['left_canonical', 'right_canonical', 'initial_pair_sums_differ', 'next_integer_values', 'next_integers_differ']:
    assert by_name['Agent10SixCarryCounterexample.' + short]['axioms'] == []

for index in range(18):
    assert by_name[f'Agent10ThreeColumnExclusion.exclusion_p{index}']['axioms'] == []
assert by_name['Agent10ThreeColumnExclusion.seven_three_prefix_survival']['axioms'] == []
second = ' '.join(types['Agent10ThreeColumnCarry.eight_carries_determine_second_pair'].split())
assert '(hL : 2 ≤ L)' in second and 't < 8' in second and second.endswith(': q 1 = r 1')
assert 'orbitCount' not in second and '(ho :' not in second
first_two = ' '.join(types['Agent10ThreeColumnCarry.eight_carries_determine_first_two_pairs'].split())
assert '(hL : 2 ≤ L)' in first_two and 't < 8' in first_two
assert first_two.endswith(': q 0 = r 0 ∧ q 1 = r 1')
active_two = ' '.join(types['Agent10ThreeColumnCarry.eight_carries_determine_first_two_active_pairs'].split())
assert 't < 8' in active_two and '(hL :' not in active_two
assert active_two.endswith(': i < 2 → i < L → q i = r i')
assert '(ho :' not in active_two and 'orbitCount' not in active_two
assert sha(report_bytes) == EXPECTED_REPORT_SHA256
assert len(records) > 1244
assert counts['Agent10EightCarryCounterexample'] == 48

seven = ' '.join(types['Agent10SevenCarryCounterexample.seven_carry_counterexample'].split())
assert 'Canonical 900000058163209' in seven and 'Canonical 900000082716109' in seven
assert 't < 7' in seven and 'i ≤' in seven
assert seven.endswith('Lychrel196.step 900000058163209 ≠ Lychrel196.step 900000082716109')
eight = ' '.join(types['Agent10EightCarryCounterexample.eight_carry_counterexample'].split())
assert 'Canonical 90000000560706169' in eight and 'Canonical 90000000806235169' in eight
assert 'leftDigits 17' in eight and 'rightDigits 17' in eight
assert 't < 8' in eight and 'i ≤' in eight
assert 'leftColumns 3 ≠' in eight and 'rightColumns 3' in eight
assert eight.endswith('Lychrel196.step 90000000560706169 ≠ Lychrel196.step 90000000806235169')
next_values = types['Agent10EightCarryCounterexample.next_integer_values']
assert '186160707060706178' in next_values and '186153261606235178' in next_values
separation = ' '.join(types['Agent10EightCarryCounterexample.first_separation_at_eight'].split())
assert 't < 8' in separation and '∃ i,' in separation and 'leftColumns 17 8' in separation
assert 'i ≤' in separation and '≠' in separation
mismatch = ' '.join(types['Agent10EightCarryCounterexample.ninth_carry_differs'].split())
assert 'leftColumns 17 8' in mismatch and ').snd 4 = 1' in mismatch
assert 'rightColumns 17 8' in mismatch and mismatch.endswith(').snd 4 = 0')
palindrome_values = types['Agent10EightCarryCounterexample.palindrome_values_at_four']
assert '16999899899899899961' in palindrome_values and '16989989999998998961' in palindrome_values
first_palindromes = ' '.join(types['Agent10EightCarryCounterexample.first_palindromes_at_four'].split())
assert 't < 4' in first_palindromes
assert first_palindromes.endswith('Lychrel196.Palindrome (Lychrel196.orbit 90000000806235169 4)')
for suffix in ['left_canonical','right_canonical','initial_pair_sums_differ',
               'initial_pair_difference_active','next_integer_values','next_integers_differ',
               'palindrome_values_at_four','first_palindromes_at_four']:
    assert by_name['Agent10EightCarryCounterexample.'+suffix]['axioms'] == []
for suffix in ['digit_bounds_fin','initial_trace_fin','trace_width_bound_fin',
               'trace_steps_fin','trace_carries_fin','palindrome_prefix_fin']:
    finite = [record for name,record in by_name.items()
              if record['origin_module']=='Agent10EightCarryCounterexample' and name.endswith('.'+suffix)]
    assert len(finite)==1 and finite[0]['axioms']==[],suffix
pair_iff = ' '.join(types['Agent10NineCarrySharp.uniform_pair_reconstruction_iff'].split())
next_iff = ' '.join(types['Agent10NineCarrySharp.uniform_next_integer_reconstruction_iff'].split())
assert pair_iff.endswith('Agent10NineCarrySharp.UniformPairReconstruction K ↔ 9 ≤ K')
assert next_iff.endswith('Agent10NineCarrySharp.UniformNextIntegerReconstruction K ↔ 9 ≤ K')
sharp = ' '.join(types['Agent10NineCarrySharp.nine_is_exact_uniform_threshold'].split())
assert '∀ (K : Nat), Agent10NineCarrySharp.UniformPairReconstruction K ↔ 9 ≤ K' in sharp
assert '∀ (K : Nat), Agent10NineCarrySharp.UniformNextIntegerReconstruction K ↔ 9 ≤ K' in sharp
sharp_source = (BASE/PROJECT/'source/Agent10NineCarrySharp.lean').read_text()
pair_predicate = sharp_source.split('def UniformPairReconstruction',1)[1].split('/--',1)[0].strip()
next_predicate = sharp_source.split('def UniformNextIntegerReconstruction',1)[1].split('theorem ',1)[0].strip()
assert 'Admissible L q → Admissible L r →' in pair_predicate
assert 'i ≤ (iterPairs q L t).1' in pair_predicate
assert '∀ i, i < L → q i = r i' in pair_predicate
assert 'Canonical n d L → Canonical m e L →' in next_predicate
assert 'i ≤ (iterPairs (columnSum d L) L t).1' in next_predicate
assert 'Lychrel196.step n = Lychrel196.step m' in next_predicate
assert 'Palindrome' not in pair_predicate+next_predicate
assert sources['Agent10EightCarryCounterexample']['sha256']=='5da46ec31d7641307a6d8c1a5f81bd3b8bdfb097a39b5afa73145e062683d739'
assert sources['Agent10NineCarrySharp']['sha256']=='98e587d22229bdead323dc922b80760cdf79f3b27c14f3a1addaa4df2fb78266'

assert (BASE / 'verification.json').read_bytes() == report_bytes
assert (BASE / 'FILES.json').read_bytes() == manifest_bytes
receipt = {
    'status': 'PASS',
    'canonical_build_executor': 'Agent #10 parent /root',
    'validation_executor': 'Agent #10 specialist /root/formalization_scout',
    'attribution_note': 'The parent launched canonical build-004. The specialist authored and executed this read-only validation of the retained output; no Lean rerun was performed.',
    'validator_derived_from': '/workspace/scratch/4b20b8469eb3/agent10-count/validate_canonical_gate_003.py',
    'validator_base_preserved_sha256': '004433487b4ff3bb84cc4b39274f1521d6fad36a837f955a46d6a2a93f29d2ba',
    'checker_inherited_agent_field': report['agent'],
    'checker_output_modified': False,
    'independent_external_acceptance': False,
    'source_commit': COMMIT,
    'expected_verification_report_sha256': EXPECTED_REPORT_SHA256,
    'validation_command': ['python3', str(Path(__file__).resolve()), EXPECTED_REPORT_SHA256],
    'project': PROJECT,
    'canonical_build_directory': str(BASE),
    'source_registry_sha256': sha(registry_bytes),
    'canonical_checker_path': CHECKER,
    'canonical_checker_sha256': sha(checker_bytes),
    'verification_report_sha256': sha(report_bytes),
    'files_manifest_sha256': sha(manifest_bytes),
    'audit_log_sha256': sha(audit_bytes),
    'manifest_entries_validated': len(manifest),
    'fresh_module_builds_passed': 16,
    'exhaustive_audit_passed': True,
    'successful_lean_commands': 17,
    'theorem_count': len(records),
    'theorem_count_includes_generated_theorems': True,
    'theorem_counts_by_origin_module': counts,
    'theorem_axiom_union': sorted(union),
    'unsafe_generated_implementation_declarations': [dict(origin_module=m, name=n) for m, n in unsafe],
    'unsafe_generated_declarations_occurring_in_theorem_axiom_union': [],
    'endpoint_count': len(endpoint_records),
    'all_endpoint_types_present': True,
    'all_endpoint_exhaustive_axiom_records_present': True,
    'explicit_source_print_axioms_endpoint_count': explicit_print_count,
    'explicit_source_print_axioms_matching_log_and_audit_count': explicit_print_count,
    'endpoints_without_explicit_source_print_axioms': sorted(EXHAUSTIVE_ONLY),
    'endpoint_axiom_coverage_note': 'All 122 endpoint axioms are checked by the exhaustive module-origin audit; 120 additionally have an explicit source #print axioms and matching module-log output. The two unprinted helper endpoints are listed separately.',
    'endpoint_records': endpoint_records,
    'sources': sources,
    'uniform_pair_predicate_source': pair_predicate,
    'uniform_next_integer_predicate_source': next_predicate,
    'semantic_checks': [
        'All-width count has only initial admissibility, including width one.',
        'Both combined pair-sum endpoints require all eight complete carry words and no count premise.',
        'The numeric endpoint uses a shared canonical width and initial nonoverflow; its conclusion is equality of the next ordinary step.',
        'The symmetric smoothing counterexample is abstract; it does not assert an actual eight-carry collision.',
        'The exterior pair is recovered universally by eight words, with no initial nonoverflow or count premise.',
        'The explicit width-eleven inputs collide for six complete words and have unequal next integers; the seventh observation separates them.',
        'The three-column finite exclusion is split into 18 axiom-free kernel certificates; its assembled theorem is audited separately.',
        'The Seven source certifies a concrete width-fifteen seven-word collision with unequal next integers.',
        'The Eight source certifies a concrete width-seventeen eight-word collision, an active initial coefficient difference at index three, and first carry separation at time eight at index four.',
        'Both Eight inputs first reach palindromes at time four, with exact values and absence of earlier palindromes explicitly certified.',
        'The Sharp predicates quantify over a common initial width, include terminal carries, and impose no palindrome-avoidance restriction.',
        'The two uniform reconstruction predicates hold exactly when nine is at most the observation count; the numerical conclusion concerns equality of the next integer.',
        'Eight complete carry words recover the second pair at widths at least two without initial nonoverflow; the active-index endpoint covers every positive width and indices below both two and the width.',
    ],
    'validation_script_sha256': sha(Path(__file__).read_bytes()),
    'original_validation_script_preserved_sha256': '36c71472841f341ba4d4be392c11636920a1fb7809c14ffdb06adb8afa48ced8',
    'validated_at_utc': datetime.now(timezone.utc).isoformat(),
}
with RECEIPT.open('x') as stream:
    stream.write(json.dumps(receipt, indent=2, ensure_ascii=False) + '\n')
print(json.dumps({
    'status': receipt['status'], 'receipt': str(RECEIPT),
    'receipt_sha256': sha(RECEIPT.read_bytes()), 'theorem_count': len(records),
    'theorem_counts_by_origin_module': counts, 'axiom_union': sorted(union),
    'endpoints': len(endpoint_records), 'explicit_print_axioms_endpoints': explicit_print_count,
    'manifest_entries': len(manifest),
    'checker_sha256': sha(checker_bytes),
}, indent=2))
