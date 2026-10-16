#!/usr/bin/env python3
"""保留审计工具失败记录后，独立重跑修复后的公理审计；不修改数学源码。"""
import argparse
import datetime as dt
import json
import os
from pathlib import Path
import subprocess
import sys
import time

sys.dont_write_bytecode = True
from rebuild_review import sha


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('manifest', type=Path)
    parser.add_argument('audit', type=Path)
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[5])
    parser.add_argument('--lean', type=Path, default=Path('/workspace/scratch/94808c4aecb2/agent107-runtime/lean-4.19.0-linux/bin/lean'))
    args = parser.parse_args()
    data = json.loads(args.manifest.read_text())
    build, logs = Path(data['build_dir']), args.manifest.parent
    assert data['build_dir_initially_empty']
    for entry in data['source_files']:
        assert sha(args.repo / entry['source']) == entry['sha256']
        assert sha(build / (entry['module'] + '.lean')) == entry['copied_sha256'] == entry['sha256']
        assert any(x['name'] == 'build-' + entry['module'] and x['exit_code'] == 0 for x in data['executions'])
    command = [str(args.lean), '--trust=0', '-j1', '-DElab.async=false', str(args.audit.resolve())]
    start = time.monotonic()
    result = subprocess.run(command, cwd=build, env=dict(os.environ, LEAN_PATH=str(build)), text=True, capture_output=True)
    name = args.audit.stem
    (logs / (name + '.stdout.log')).write_text(result.stdout)
    (logs / (name + '.stderr.log')).write_text(result.stderr)
    data['executions'].append({
        'name': name, 'command': command, 'cwd': str(build),
        'exit_code': result.returncode, 'elapsed_seconds': time.monotonic() - start,
        'stdout_log': name + '.stdout.log', 'stderr_log': name + '.stderr.log',
        'audit_source_sha256': sha(args.audit),
        'reason': '修复模块来源审计工具的Name打印类型推断；全部数学模块已独立编译成功。',
    })
    if result.returncode == 0:
        data.setdefault('recovered_tool_errors', []).append(data.get('error'))
        data['status'] = 'INDEPENDENT_CLEAN_REBUILD_AND_AXIOM_AUDIT_PASS'
        data['finished_utc'] = dt.datetime.now(dt.timezone.utc).isoformat()
        data['extensions'][-1]['finished_utc'] = data['finished_utc']
        data['extensions'][-1]['audit_recovery'] = name
    else:
        data['status'] = 'FAILED_REAUDIT'
    args.manifest.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'status': data['status'], 'exit_code': result.returncode,
                      'evidence_dir': str(logs), 'audit': name}, ensure_ascii=False))
    return result.returncode


if __name__ == '__main__':
    raise SystemExit(main())
