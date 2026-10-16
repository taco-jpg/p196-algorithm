"""Source-pinned local development build; every invocation retains source and log."""
from pathlib import Path
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[6]
HERE = Path(__file__).resolve().parent
BUILD = Path('/tmp/agent105-normalize-8f1107db019a')
LEAN = Path('/tmp/p196-agent105-toolchain/lean-4.19.0-linux/bin/lean')

def main():
    attempt_root = HERE / 'attempts'
    attempt_root.mkdir(exist_ok=True)
    attempt = attempt_root / ('attempt-%03d' % (len(list(attempt_root.glob('attempt-*'))) + 1))
    attempt.mkdir()
    fresh = '--fresh' in sys.argv
    if '--reuse' in sys.argv:
        assert not fresh
        build = Path(sys.argv[sys.argv.index('--reuse')+1])
    else:
        build = BUILD.with_name(BUILD.name + '-' + attempt.name) if fresh else BUILD
    build.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ, LEAN_PATH=str(build))
    registry = json.loads((HERE/'dependency-pins.json').read_text())
    (attempt/'dependency-pins.json').write_text(json.dumps(registry,indent=2)+'\n')
    (attempt/'run-config.json').write_text(json.dumps({
        'fresh_build': fresh, 'build_path': str(build), 'lean_path': str(LEAN),
        'lean_sha256': hashlib.sha256(LEAN.read_bytes()).hexdigest(),
        'lean_version': subprocess.run([str(LEAN),'--version'],capture_output=True,text=True,check=True).stdout.strip()
    },indent=2)+'\n')
    rows = []
    dependency_state = hashlib.sha256()
    for module, pin in registry['modules'].items():
        source = ROOT / pin['path']
        data = source.read_bytes()
        assert hashlib.sha256(data).hexdigest() == pin['sha256'], source
        dependency_state.update(module.encode()+b'\0'+data)
        expected_stamp = dependency_state.hexdigest()
        stamp = build/(module+'.dependency-stamp')
        target = build / (module+'.lean')
        if not target.exists() or target.read_bytes() != data:
            target.write_bytes(data)
            (build/(module+'.olean')).unlink(missing_ok=True)
        if not stamp.exists() or stamp.read_text() != expected_stamp:
            (build/(module+'.olean')).unlink(missing_ok=True)
        if (build/(module+'.olean')).exists():
            rows.append({'module':module,'cached_source_sha256':pin['sha256']})
            continue
        start = time.monotonic()
        result = subprocess.run([str(LEAN), '-o', module+'.olean', module+'.lean'], cwd=build, env=env, capture_output=True, text=True)
        (attempt/(module+'.log')).write_text(result.stdout+result.stderr)
        rows.append({'module':module,'exit':result.returncode,'seconds':time.monotonic()-start,'sha256':pin['sha256']})
        print(json.dumps(rows[-1]), flush=True)
        if result.returncode:
            (attempt/'result.json').write_text(json.dumps(rows,indent=2)+'\n')
            print(result.stdout+result.stderr,flush=True)
            return result.returncode
        stamp.write_text(expected_stamp)
    source = ROOT/'proofs/Agent105AffineNormalize.lean'
    data = source.read_bytes()
    (build/source.name).write_bytes(data)
    (attempt/source.name).write_bytes(data)
    result = subprocess.run([str(LEAN),'-o','Agent105AffineNormalize.olean','Agent105AffineNormalize.lean'],cwd=build,env=env,capture_output=True,text=True)
    (attempt/'Agent105AffineNormalize.log').write_text(result.stdout+result.stderr)
    rows.append({'module':'Agent105AffineNormalize','exit':result.returncode,'sha256':hashlib.sha256(data).hexdigest()})
    (attempt/'result.json').write_text(json.dumps(rows,indent=2)+'\n')
    print(result.stdout+result.stderr,flush=True)
    print(json.dumps({'attempt':str(attempt),'exit':result.returncode}),flush=True)
    return result.returncode

if __name__ == '__main__':
    sys.exit(main())
