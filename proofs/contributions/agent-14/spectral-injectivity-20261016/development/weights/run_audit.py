"""Audit every explicit declaration in the successfully compiled weights source."""

from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys


root = Path(__file__).resolve().parent
compiled = root / 'attempt-002'
source = compiled / 'Agent14SpectralWeights.lean'
current = Path('/workspace/scratch/d43e317f00d9/p196/proofs/Agent14SpectralWeights.lean')
assert current.read_bytes() == source.read_bytes()
declarations = re.findall(r'^(?:@\[simp\] )?(def|theorem) ([A-Za-z_][A-Za-z0-9_]*)',
                          source.read_text(), re.MULTILINE)
audit_dir = root / 'audit-001'
audit_dir.mkdir()
audit = audit_dir / 'AuditWeights.lean'
audit.write_text('import Agent14SpectralWeights\n\n' + ''.join(
    f'#print axioms Agent14.Spectral.{name}\n' for _, name in declarations), encoding='utf-8')
lean = '/workspace/scratch/f8aedc6d7adf/runtime-agent6/lean-4.19.0-linux/bin/lean'
command = [lean, '--trust=0', '-j1', '-DElab.async=false', str(audit)]
environment = os.environ.copy()
environment['LEAN_PATH'] = str(compiled)
record = {
    'verification_scope': 'Author audit of every explicit declaration; imports the successful author object.',
    'independent_review': False,
    'source_sha256': hashlib.sha256(source.read_bytes()).hexdigest(),
    'compiled_object_sha256': hashlib.sha256((compiled / 'Agent14SpectralWeights.olean').read_bytes()).hexdigest(),
    'source_matches_successful_snapshot': True,
    'declarations': [{'kind': kind, 'name': 'Agent14.Spectral.' + name} for kind, name in declarations],
    'theorem_count': sum(kind == 'theorem' for kind, _ in declarations),
    'definition_count': sum(kind == 'def' for kind, _ in declarations),
    'command': command,
    'LEAN_PATH': str(compiled),
    'cwd': str(audit_dir),
    'started_at_utc': datetime.now(timezone.utc).isoformat(),
}
(audit_dir / 'command.txt').write_text('LEAN_PATH=' + shlex.quote(str(compiled)) + ' ' +
                                      shlex.join(command) + '\n', encoding='utf-8')
completed = subprocess.run(command, cwd=audit_dir, env=environment, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, check=False)
(audit_dir / 'compiler.log').write_bytes(completed.stdout)
record['exit_status'] = completed.returncode
record['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
(audit_dir / 'result.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
print(json.dumps({key: value for key, value in record.items() if key != 'declarations'}, indent=2))
sys.exit(completed.returncode)
