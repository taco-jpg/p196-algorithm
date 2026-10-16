#!/usr/bin/env python3
"""Validate the complete, possibly multiline #print axioms receipt."""
from pathlib import Path
import hashlib
import json
import re

dev = Path('/workspace/scratch/f8aedc6d7adf/landscape-agent6/checker-dev')
attempt = dev / 'attempt-001'
source = attempt / 'CertificateCoordinates.lean'
data = source.read_bytes()
text = data.decode()
log_path = attempt / 'compile.log'
log = log_path.read_text()
compile_result = json.loads((attempt / 'compile-result.json').read_text())
assert compile_result['exit_code'] == 0
assert hashlib.sha256(data).hexdigest() == compile_result['source_sha256']

namespace = 'Agent6.CertificateCoordinates.'
public = [namespace + n for n in re.findall(r'^theorem ([A-Za-z0-9_]+)', text, re.M)]
printed = re.findall(r'^#print axioms (\S+)', text, re.M)
assert len(public) == len(set(public)) == 11
assert len(printed) == len(set(printed)) == 11
assert set(public) == set(printed)

# The bracket body spans line breaks.  A first-line-only parser would lose
# Classical.choice and Quot.sound from two of the exported receipts.
pattern = re.compile(
    r"^'(?P<name>[^']+)'\s+(?:depends on axioms:\s*\[(?P<axioms>[^\]]*)\]"
    r"|does not depend on any axioms(?:\.)?)", re.M)
found = {}
for match in pattern.finditer(log):
    name = match.group('name')
    assert name not in found, ('duplicate receipt', name)
    found[name] = [a.strip() for a in (match.group('axioms') or '').split(',') if a.strip()]
assert set(found) == set(public), ('missing or unexpected receipt', set(found), set(public))
assert len(re.findall(r'depends on axioms:|does not depend on any axioms', log)) == len(found)
allowed = {'propext', 'Classical.choice', 'Quot.sound'}
unexpected = {n: [a for a in xs if a not in allowed]
              for n, xs in found.items() if any(a not in allowed for a in xs)}
assert not unexpected, unexpected
assert not re.search(r'\b(sorry|admit|native_decide)\b', text)
assert not re.search(r'^\s*axiom\b', text, re.M)

record = {
    'status': 'PASS', 'source_sha256': hashlib.sha256(data).hexdigest(),
    'log_sha256': hashlib.sha256(log_path.read_bytes()).hexdigest(),
    'parser_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'public_theorem_count': len(public),
    'private_theorem_count': len(re.findall(r'^private theorem ', text, re.M)),
    'definition_count': len(re.findall(r'^def ', text, re.M)),
    'axioms': found, 'unexpected_axioms': unexpected,
    'axiom_union': sorted({a for xs in found.values() for a in xs}),
    'coverage': 'Every public theorem has a complete #print axioms result. All three private helpers feed these exports. The independent runtime audit separately checks the module origin and full closure.'
}
assert record['private_theorem_count'] == record['definition_count'] == 3
(dev / 'axiom-audit.json').write_text(json.dumps(record, indent=2) + '\n')
print(json.dumps(record, indent=2))
