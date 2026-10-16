"""Check only UniformReturnPlain; reuse byte-matched dependency artifacts.

This author harness never rebuilds a dependency. A missing exact artifact is
a recorded failure, so it cannot accidentally start a memory-heavy build.
"""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[6]
HERE = Path(__file__).resolve().parent
LEAN = Path('/tmp/p196-agent105-toolchain/lean-4.19.0-linux/bin/lean')
BUILD = Path('/tmp/agent105-uniform-plain-8f1107db019a')
CACHES = [
    Path('/workspace/scratch/8f1107db019a/agent105-work/zip-build'),
    Path('/tmp/p196-agent105-toolchain/affine-orbit/source'),
    Path('/tmp/agent105-normalize-8f1107db019a-attempt-005'),
]
MODULE = 'Agent105UniformReturnPlain'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def main():
    attempts = HERE / 'attempts'
    attempts.mkdir(exist_ok=True)
    attempt = attempts / ('attempt-%03d' % (len(list(attempts.glob('attempt-*'))) + 1))
    attempt.mkdir()
    BUILD.mkdir(exist_ok=True)
    base = json.loads((HERE.parent/'shape/dependency-pins.json').read_text())
    modules = {}

    def visit(module):
        if module == 'Std' or module in modules:
            return
        path = base['modules'].get(module, {}).get('path', 'proofs/'+module+'.lean')
        data = (ROOT/path).read_bytes()
        imports = [name for line in data.decode().splitlines()
                   if line.startswith('import ') for name in line[7:].split()]
        for dependency in imports:
            visit(dependency)
        modules[module] = {
            'path': path, 'sha256': digest(data),
            'git_blob': hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest(),
            'imports': imports,
        }

    visit(MODULE)
    pins = {key: value for key, value in base.items() if key != 'modules'}
    pins['modules'] = {key: value for key, value in modules.items() if key != MODULE}
    (HERE/'dependency-pins.json').write_text(json.dumps(pins, indent=2)+'\n')
    (attempt/'dependency-pins.json').write_text(json.dumps(pins, indent=2)+'\n')
    origins = []
    for module, pin in pins['modules'].items():
        data = (ROOT/pin['path']).read_bytes()
        matches = [cache for cache in CACHES
                   if (cache/(module+'.lean')).is_file()
                   and (cache/(module+'.lean')).read_bytes() == data
                   and (cache/(module+'.olean')).is_file()]
        if not matches:
            failure = {'status':'MISSING_EXACT_CACHED_DEPENDENCY', 'module':module,
                       'expected_source_sha256':pin['sha256']}
            (attempt/'result.json').write_text(json.dumps(failure, indent=2)+'\n')
            print(json.dumps(failure), flush=True)
            return 2
        cache = matches[0]
        (BUILD/(module+'.lean')).write_bytes(data)
        shutil.copyfile(cache/(module+'.olean'), BUILD/(module+'.olean'))
        origins.append({'module':module, 'cache':str(cache),
                        'source_sha256':pin['sha256'],
                        'olean_sha256':digest((BUILD/(module+'.olean')).read_bytes())})
    (attempt/'reused-artifacts.json').write_text(json.dumps(origins, indent=2)+'\n')
    data = (ROOT/'proofs'/(MODULE+'.lean')).read_bytes()
    (BUILD/(MODULE+'.lean')).write_bytes(data)
    (attempt/(MODULE+'.lean')).write_bytes(data)
    command = [str(LEAN), '--trust=0', '-j1', '-DElab.async=false',
               '-o', MODULE+'.olean', MODULE+'.lean']
    result = subprocess.run(command, cwd=BUILD,
                            env=dict(os.environ, LEAN_PATH=str(BUILD)),
                            capture_output=True, text=True)
    (attempt/'compile.log').write_text(result.stdout+result.stderr)
    receipt = {'module':MODULE, 'source_sha256':digest(data),
               'command':command, 'cwd':str(BUILD), 'exit_code':result.returncode,
               'dependency_policy':'exact-source cache reuse, no dependency compilation',
               'lean_version':subprocess.run([str(LEAN),'--version'],capture_output=True,
                                             text=True,check=True).stdout.strip()}
    (attempt/'result.json').write_text(json.dumps(receipt, indent=2)+'\n')
    print(result.stdout+result.stderr, flush=True)
    print(json.dumps(receipt), flush=True)
    return result.returncode


if __name__ == '__main__':
    sys.exit(main())
