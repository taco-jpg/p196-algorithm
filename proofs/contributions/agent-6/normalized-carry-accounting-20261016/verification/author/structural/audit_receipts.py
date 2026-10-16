"""Parse every literal axiom receipt, including multiline axiom lists."""
from pathlib import Path
import hashlib
import json
import re

BASE = Path('/workspace/scratch/f8aedc6d7adf/landscape-agent6/carry-dev')
ATTEMPT = BASE / 'attempt-001'
source = (ATTEMPT / 'NormalizedCarry.lean').read_text()
result = json.loads((ATTEMPT / 'compile-result.json').read_text())
log_raw = (ATTEMPT / 'compile.log').read_bytes()
log = log_raw.decode()
expected = re.findall(r'^#print axioms\s+([^\s]+)\s*$', source, flags=re.M)
pattern = re.compile(
    r"^'(?P<name>[^']+)'\s+(?:depends on axioms:\s*\[(?P<axioms>[^\]]*)\]"
    r"|does not depend on any axioms(?:\.)?)", re.M)
receipts = []
for match in pattern.finditer(log):
    receipts.append({'name': match.group('name'),
                     'axioms': [x.strip() for x in (match.group('axioms') or '').split(',')
                                if x.strip()],
                     'raw_receipt': match.group(0)})
allowed = {'propext', 'Classical.choice', 'Quot.sound'}
assert result['exit_code'] == 0
assert hashlib.sha256(log_raw).hexdigest() == result['compile_log_sha256']
assert expected == [r['name'] for r in receipts]
assert len(expected) == len(set(expected)) == 3
assert all(set(r['axioms']) <= allowed for r in receipts)
current = Path(result['source_pin']['source']).read_bytes()
assert current == (ATTEMPT / 'NormalizedCarry.lean').read_bytes()
assert hashlib.sha256(current).hexdigest() == result['source_pin']['sha256']
decls = re.findall(r'^(private\s+)?theorem\s+(\w+)', source, re.M)
public = [name for private, name in decls if not private]
private = [name for privacy, name in decls if privacy]
assert public == [name.split('.')[-1] for name in expected]
assert not private
assert not re.search(r'^\s*(?:noncomputable\s+)?def\s+', source, re.M)
assert not re.search(r'^\s*(?:private\s+)?(?:axiom|opaque)\s+', source, re.M)
assert not re.search(r'\b(?:sorry|admit|native_decide)\b', source)
audit = {'status': 'PASS_AUTHOR_LITERAL_AXIOM_AUDIT',
         'source_sha256': result['source_pin']['sha256'],
         'source_git_blob': result['source_pin']['git_blob'],
         'compile_log_sha256': result['compile_log_sha256'],
         'parser': str(Path(__file__).resolve()),
         'parser_supports_multiline_axiom_lists': True,
         'expected_literal_print_count': len(expected),
         'parsed_receipt_count': len(receipts),
         'public_theorem_count': len(public), 'private_theorem_count': len(private),
         'definition_count': 0, 'receipts': receipts,
         'allowed_axioms': sorted(allowed),
         'actual_axiom_union': sorted(set().union(*(set(r['axioms']) for r in receipts))),
         'source_matches_frozen_attempt': True,
         'admissions_or_new_axioms_found': False,
         'independent_review': False}
(BASE / 'axiom-audit.json').write_text(json.dumps(audit, indent=2) + '\n')
print(json.dumps(audit, indent=2))
