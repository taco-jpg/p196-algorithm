#!/usr/bin/env python3
"""Targeted cache-provenance fixture; never invokes Lean or real builds.

A fake compiler produces deterministic dependency-sensitive marker objects.
Only temporary copies of the runner, Lean sources, and build manifest change.
"""

from hashlib import sha256
from pathlib import Path
import json
import shutil
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent
FORMAL = HERE.parent / '2026-10-14-seven-step-extension-formal'
MODULES = ['RankData'] + [f'RankChecks{i}' for i in range(7)] + ['RankChecks','RankCertificate']


def digest(path):
    return sha256(path.read_bytes()).hexdigest()


def main():
    results = []
    with tempfile.TemporaryDirectory(prefix='p196-resume-negative-fixture-') as tmp:
        root = Path(tmp)
        source, build = root/'source', root/'build'
        source.mkdir()
        build.mkdir()
        verifier = source/'verify_rank_certificate.py'
        shutil.copyfile(FORMAL/verifier.name, verifier)
        for module in MODULES:
            shutil.copyfile(FORMAL/(module+'.lean'), source/(module+'.lean'))
        for module in ('LychrelDigitSums','BoundaryTransducer','SixPrefix'):
            (build/(module+'.lean')).write_text('-- synthetic fixture dependency '+module+'\n')
            (build/(module+'.olean')).write_text('fixture object '+module+'\n')
        compiler = root/'fake_lean.py'
        compiler.write_text('#!'+sys.executable+'\n'+'''from pathlib import Path
from hashlib import sha256
import re, sys
source = Path(sys.argv[-1])
output = Path(sys.argv[sys.argv.index('-o')+1])
content = source.read_bytes()
imports = re.findall(r'^import (\\w+)$', content.decode(), re.M)
for module in imports:
    content += Path(module+'.olean').read_bytes()
output.write_bytes(sha256(content).digest())
with Path('compiler_calls.txt').open('a') as stream:
    stream.write(source.stem+'\\n')
''')
        compiler.chmod(0o755)

        def run(label, resume):
            callfile = build/'compiler_calls.txt'
            if callfile.exists():
                callfile.unlink()
            cmd = [sys.executable, str(verifier), '--build', str(build),
                   '--lean', str(compiler), '--workers', '1']
            if resume:
                cmd.append('--resume')
            proc = subprocess.run(cmd, capture_output=True, text=True, check=True)
            manifest = json.loads((build/'rank_build.json').read_text())
            calls = callfile.read_text().splitlines() if callfile.exists() else []
            assert manifest['status'] == 'PASS'
            assert all(row['dependencies_unchanged'] for row in manifest['modules'].values())
            reused = [name for name in MODULES if manifest['modules'][name].get('reused_from_verified_same_build')]
            results.append(dict(case=label, actual_compile_calls=calls, reused_modules=reused,
                                successful=True, stdout_sha256=sha256(proc.stdout.encode()).hexdigest()))
            return manifest, calls, reused

        _, calls, reused = run('initial_marker_build', False)
        assert calls == MODULES and reused == []
        baseline, calls, reused = run('unchanged_resume', True)
        assert calls == [] and reused == MODULES

        # Keep every phase-check source, object, log, and command unchanged.
        # Only RankData changes; a valid cache must reject all stale dependents.
        rankdata = source/'RankData.lean'
        rankdata.write_bytes(rankdata.read_bytes()+b'\n-- temporary stale-dependency fixture\n')
        for name in MODULES[1:]:
            assert digest(source/(name+'.lean')) == baseline['modules'][name]['source_sha256']
            assert digest(build/(name+'.olean')) == baseline['modules'][name]['olean_sha256']
            assert digest(build/(name+'.log')) == baseline['modules'][name]['log_sha256']
        changed, calls, reused = run('changed_rankdata_rejects_stale_dependents', True)
        assert calls == MODULES and reused == []
        assert all(changed['modules'][f'RankChecks{i}']['dependency_fingerprints'] !=
                   baseline['modules'][f'RankChecks{i}']['dependency_fingerprints'] for i in range(7))

        # An old record with no dependency provenance is not silently blessed.
        old = json.loads((build/'rank_build.json').read_text())
        old['modules']['RankChecks0'].pop('dependency_fingerprints')
        old['modules']['RankChecks0'].pop('dependencies_unchanged')
        (build/'rank_build.json').write_text(json.dumps(old))
        _, calls, reused = run('legacy_chunk_record_rejected', True)
        assert calls == ['RankChecks0']
        assert reused == [name for name in MODULES if name != 'RankChecks0']

    report = dict(status='PASS_TARGETED_PROVENANCE_FIXTURE',
        verifier_sha256=digest(FORMAL/'verify_rank_certificate.py'), cases=results,
        real_build_or_sources_modified=False, lean_compiler_invoked=False,
        scope='Exercises public verifier CLI and exact dependency-reuse decisions with synthetic marker objects; does not certify Lean proof terms or retroactively establish legacy-build provenance.')
    (HERE/'resume_provenance_controls.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
