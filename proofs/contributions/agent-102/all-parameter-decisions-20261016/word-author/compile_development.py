"""开发阶段仅复用已亲自核对源 SHA 的已有依赖，不修改共享产物。"""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys

base = Path('/workspace/scratch/fb513c1676b0')
work = base / 'agent102-word-intervals/universal-author'
snapshot = base / 'agent102-word-intervals/full-review-001'
dependency_build = base / 'agent102-word-intervals/full-review-001-empty-build'
label = sys.argv[1]
evidence = work / label
build = work / f'{label}-build'
evidence.mkdir(exist_ok=False)
build.mkdir(exist_ok=False)
digest = lambda path: hashlib.sha256(path.read_bytes()).hexdigest()
dependencies = {}
for name in ['Agent102RunDefs', 'Agent102RunWord']:
    original = base / 'p196-agent102-universal/proofs' / f'{name}.lean'
    frozen = snapshot / f'{name}.lean'
    assert digest(original) == digest(frozen), name
    shutil.copyfile(frozen, evidence / f'{name}.lean')
    dependencies[name] = {
        'source_sha256': digest(frozen),
        'reused_olean': str(dependency_build / f'{name}.olean'),
        'reused_olean_sha256': digest(dependency_build / f'{name}.olean'),
    }
source = base / 'p196-agent102-universal/proofs/Agent102RunDecision.lean'
target = evidence / source.name
shutil.copyfile(source, target)
lean = base / 'agent102-runtime/lean-4.19.0-linux/bin/lean'
env = os.environ.copy()
env['LEAN_PATH'] = str(dependency_build)
command = [str(lean), '--trust=0', '-j1', '-DElab.async=false',
           '-o', str(build / 'Agent102RunDecision.olean'), str(target)]
process = subprocess.run(command, cwd=evidence, env=env, text=True,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
(evidence / 'Agent102RunDecision.log').write_text(process.stdout)
result = {
    'author': '/root/word_intervals',
    'command': command,
    'returncode': process.returncode,
    'source_sha256': digest(target),
    'verified_reused_dependencies': dependencies,
}
(evidence / 'manifest.json').write_text(json.dumps(result, indent=2) + '\n')
print(process.stdout, end='')
print(f'开发编译返回码：{process.returncode}')
sys.exit(process.returncode)
