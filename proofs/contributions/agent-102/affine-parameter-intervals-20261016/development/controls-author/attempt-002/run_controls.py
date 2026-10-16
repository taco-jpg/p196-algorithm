from pathlib import Path
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import time


ROOT = Path('/workspace/scratch/fb513c1676b0')
REPO = ROOT / 'p196-agent102-intervals' / 'proofs'
CHECKS = ROOT / 'agent102-interval-checks'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


parser = argparse.ArgumentParser()
parser.add_argument('attempt')
args = parser.parse_args()
attempt = Path(__file__).resolve().parent / args.attempt
attempt.mkdir(parents=True, exist_ok=False)
source = REPO / 'Agent102ParameterSetControls.lean'
shutil.copyfile(source, attempt / source.name)
shutil.copyfile(__file__, attempt / 'run_controls.py')
pins = json.loads((CHECKS / 'attempt-005-decisions' / 'dependency-pins.json').read_text())
evidence = []
for pin in pins:
    name = pin['module']
    saved = CHECKS / 'attempt-004' / (name + '.lean')
    compiled = CHECKS / 'attempt-004' / (name + '.olean')
    assert digest(saved) == pin['sha256'], name
    assert digest(REPO / (name + '.lean')) == pin['sha256'], name
    assert compiled.is_file(), name
    evidence.append({
        'module': name, 'source_sha256': pin['sha256'],
        'source_bytes': saved.stat().st_size,
        'olean_sha256': digest(compiled),
        'source_directory': str(saved.parent),
        'parent_reported_exit_code': pin['exit_code'],
        'current_source_matches': True,
    })
helper = 'Agent102ParameterSetDecisions'
helper_receipt = json.loads((CHECKS / 'attempt-005-decisions' / 'receipt.json').read_text())
helper_source = CHECKS / 'attempt-005-decisions' / (helper + '.lean')
helper_olean = CHECKS / 'attempt-005-decisions' / (helper + '.olean')
assert digest(helper_source) == helper_receipt['source_sha256']
assert digest(REPO / (helper + '.lean')) == helper_receipt['source_sha256']
assert helper_olean.is_file()
evidence.append({
    'module': helper, 'source_sha256': helper_receipt['source_sha256'],
    'source_bytes': helper_source.stat().st_size,
    'olean_sha256': digest(helper_olean),
    'source_directory': str(helper_source.parent),
    'parent_reported_exit_code': helper_receipt['exit_code'],
    'current_source_matches': True,
})
(attempt / 'dependency-pins.json').write_text(json.dumps(evidence, ensure_ascii=False, indent=2) + '\n')
lean_path = str(CHECKS / 'attempt-005-decisions') + ':' + str(CHECKS / 'attempt-004')
command = [
    str(ROOT / 'agent102-runtime' / 'lean-4.19.0-linux' / 'bin' / 'lean'),
    '--trust=0', '-j1', '-DElab.async=false',
    '-o', 'Agent102ParameterSetControls.olean', 'Agent102ParameterSetControls.lean',
]
receipt = {
    'kind': '控制文件作者的实际增量叶子编译；未重复编译依赖',
    'source_sha256': digest(source), 'source_bytes': source.stat().st_size,
    'command': command, 'working_directory': str(attempt),
    'lean_path': lean_path, 'dependencies_byte_checked': len(evidence),
    'launcher_note': '使用受支持的提升权限执行；普通沙箱无法定位Lean应用，保留于attempt-001。',
}
(attempt / 'receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
env = os.environ.copy()
env['LEAN_PATH'] = lean_path
start = time.monotonic()
proc = subprocess.run(command, cwd=attempt, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
(attempt / 'stdout.log').write_text(proc.stdout)
(attempt / 'stderr.log').write_text(proc.stderr)
receipt.update({
    'exit_code': proc.returncode, 'seconds': time.monotonic() - start,
    'stdout_sha256': digest(attempt / 'stdout.log'),
    'stderr_sha256': digest(attempt / 'stderr.log'),
})
(attempt / 'receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n')
print(json.dumps(receipt, ensure_ascii=False, indent=2))
print(proc.stdout)
print(proc.stderr)
