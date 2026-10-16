#!/usr/bin/env python3
"""Execute only the complete literal audit against the pinned verified oleans."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time

parser = argparse.ArgumentParser()
parser.add_argument('--lean', type=Path, required=True)
parser.add_argument('--build', type=Path, required=True)
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
base = Path(__file__).resolve().parent
build = args.build.resolve()
lean = args.lean.resolve()
output = args.output.resolve()
if output.exists():
    parser.error('output must not already exist')
inputs = json.loads((base / 'INPUT_RECEIPT.json').read_text())
source = base / 'LiteralAudit.lean'
registry_path = base / 'Agent102AllParameters.registry.json'
assert hashlib.sha256(source.read_bytes()).hexdigest() == inputs['literal_sha256']
assert hashlib.sha256(registry_path.read_bytes()).hexdigest() == inputs['registry_sha256']
registry = json.loads(registry_path.read_text())
main_names = registry['claims'][0]['endpoints']
extra_names = registry['literal_audit_extra_endpoints']
expected = main_names + extra_names
commands = re.findall(r'^#print axioms (\S+)\s*$', source.read_text(), re.M)
assert len(main_names) == 144 and len(extra_names) == 2
assert len(commands) == len(set(commands)) == 146
assert set(commands) == set(expected)
objects = json.loads((base / 'VERIFIED_OLEANS.json').read_text())
for entry in objects:
    module = entry['module']
    assert hashlib.sha256((build / (module + '.lean')).read_bytes()).hexdigest() == entry['source_sha256']
    assert hashlib.sha256((build / (module + '.olean')).read_bytes()).hexdigest() == entry['sha256']
lean_sha = hashlib.sha256(lean.read_bytes()).hexdigest()
assert lean_sha == '92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
output.mkdir(parents=True)
command = [str(lean), '--trust=0', '-j1', '-DElab.async=false', str(source)]
record = {'argv': command, 'cwd': str(output), 'LEAN_PATH': str(build),
          'lean_sha256': lean_sha, 'kind': 'incremental complete literal audit',
          'dependency_modules_recompiled': 0, 'reused_verified_olean_count': len(objects),
          'output_olean_requested': False}
(output / 'COMMAND.json').write_text(json.dumps(record, indent=2) + '\n')
env = os.environ.copy()
env['LEAN_PATH'] = str(build)
started = time.monotonic()
logfile = output / 'LiteralAudit.log'
with logfile.open('w') as log:
    result = subprocess.run(command, cwd=output, env=env, stdout=log,
                            stderr=subprocess.STDOUT, timeout=60)
record.update({'returncode': result.returncode,
               'seconds': round(time.monotonic() - started, 3),
               'log_sha256': hashlib.sha256(logfile.read_bytes()).hexdigest()})
(output / 'EXECUTION_RECEIPT.json').write_text(json.dumps(record, indent=2) + '\n')
assert result.returncode == 0, logfile.read_text()
logtext = logfile.read_text()
pattern = re.compile(r"^'([^']+)' (?:depends on axioms:\s*\[([^\]]*)\]|(does not depend on any axioms))\s*$", re.M)
matches = list(pattern.finditer(logtext))
assert not pattern.sub('', logtext).strip(), 'unexpected unparsed compiler output'
parsed = []
allowed = set(registry['toolchain']['allowed_axioms'])
for match in matches:
    name = match.group(1)
    axioms = [] if match.group(3) else [a.strip() for a in match.group(2).split(',') if a.strip()]
    assert set(axioms) <= allowed, (name, axioms)
    parsed.append({'name': name, 'axioms': axioms,
                   'registry_group': 'main' if name in main_names else 'literal-extra'})
names = [entry['name'] for entry in parsed]
assert len(names) == len(set(names)) == 146 and set(names) == set(expected)
assert names == commands, 'literal output order differs from the actual source'
for entry in objects:
    assert hashlib.sha256((build / (entry['module'] + '.olean')).read_bytes()).hexdigest() == entry['sha256']
(output / 'PARSED_AXIOMS.json').write_text(json.dumps(parsed, indent=2) + '\n')
summary = {'result': 'PASS', 'kind': 'incremental complete literal audit; not a clean build',
           'source_modules_byte_matched': 10, 'dependency_modules_recompiled': 0,
           'registry_main_count': 144, 'literal_extra_count': 2, 'literal_result_count': len(parsed),
           'source_command_and_output_order_equal': True, 'names_equal_registry_union': True,
           'empty_axiom_count': sum(not item['axioms'] for item in parsed),
           'axiom_union': sorted({a for item in parsed for a in item['axioms']}),
           'literal_extra_results': [item for item in parsed if item['registry_group'] == 'literal-extra'],
           'verified_oleans_unchanged_after_run': True, 'lean_returncode': result.returncode}
(output / 'RESULT.json').write_text(json.dumps(summary, indent=2) + '\n')
print(json.dumps(summary, indent=2))
