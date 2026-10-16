"""Record one immutable, strict Lean check of the owned weights module."""

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import shlex
import subprocess
import sys


source = Path('/workspace/scratch/d43e317f00d9/p196/proofs/Agent14SpectralWeights.lean')
root = Path(__file__).resolve().parent
attempt = root / sys.argv[1]
attempt.mkdir()
snapshot = attempt / source.name
snapshot.write_bytes(source.read_bytes())
lean = '/workspace/scratch/f8aedc6d7adf/runtime-agent6/lean-4.19.0-linux/bin/lean'
command = [lean, '--trust=0', '-j1', '-DElab.async=false', '-o',
           str(attempt / 'Agent14SpectralWeights.olean'), str(snapshot)]
record = {
    'source': str(source),
    'snapshot': str(snapshot),
    'source_sha256': hashlib.sha256(snapshot.read_bytes()).hexdigest(),
    'command': command,
    'cwd': str(attempt),
    'started_at_utc': datetime.now(timezone.utc).isoformat(),
}
(attempt / 'command.txt').write_text(shlex.join(command) + '\n', encoding='utf-8')
try:
    completed = subprocess.run(command, cwd=attempt, stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT, check=False)
    (attempt / 'compiler.log').write_bytes(completed.stdout)
    record['exit_status'] = completed.returncode
except Exception as error:
    (attempt / 'compiler.log').write_text(repr(error) + '\n', encoding='utf-8')
    record['execution_exception'] = repr(error)
    record['exit_status'] = None
record['finished_at_utc'] = datetime.now(timezone.utc).isoformat()
(attempt / 'result.json').write_text(json.dumps(record, indent=2) + '\n', encoding='utf-8')
print(json.dumps(record, indent=2))
sys.exit(0 if record['exit_status'] == 0 else 1)
