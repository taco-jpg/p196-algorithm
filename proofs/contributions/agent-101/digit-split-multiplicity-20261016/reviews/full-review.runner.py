from pathlib import Path
import ast
import datetime
import hashlib
import json
import os
import re
import subprocess
import tempfile
import time

ROOT = Path('/workspace/scratch/2a8a87fd78df/p196-agent101')
EVIDENCE = Path(__file__).resolve().parent
RUNTIME = Path('/workspace/scratch/2a8a87fd78df/agent101-runtime')
LEAN = RUNTIME / 'toolchain/lean-4.19.0-linux/bin/lean'
EXPECTED = {
    'Lychrel196Research': ('Lychrel196Research__c696e0ea3db39d92.lean', 'f8950d138fa4231b536059e2334d36b6496de3d25a806f4cf3925941aa05144c'),
    'Agent101DigitPairs': ('Agent101DigitPairs.lean', '5c76eae97efd2f30d1775650f7feca477c269419af1c02809800a95ca62821f8'),
    'Agent101MultiplicityBounds': ('Agent101MultiplicityBounds.lean', '8fd487ce8025cfe7cbda3dc51b6a02595c856fbe3dd065a8781cea60b7e6b5c3'),
    'Agent101SplitEnumeration': ('Agent101SplitEnumeration.lean', '8ce57c88984df3a965e33c181f4d8f138258fe48b14e2b835333fe6c30d79684'),
    'Agent101NumericFibers': ('Agent101NumericFibers.lean', 'bba80a597345f7f3bd207698a6e6b338ee20335e647f518604fa43654b13fd97'),
}
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def write_once(path, data):
    with path.open('xb') as stream:
        stream.write(data)


def axiom_records(text):
    found = {}
    for match in re.finditer(r"^'([^']+)' (?:does not depend on any axioms|depends on axioms:\s*\[([^\]]*)\])", text, re.M):
        name = match.group(1)
        assert name not in found, ('duplicate axiom record', name)
        values = sorted(x.strip() for x in (match.group(2) or '').split(',') if x.strip())
        assert set(values) <= ALLOWED, (name, values)
        found[name] = values
    return found


def main():
    report_path = EVIDENCE / 'full-review.json'
    assert not report_path.exists(), 'Preserve existing review evidence; use a new record for another run.'
    build = Path(tempfile.mkdtemp(prefix='full-independent-', dir=RUNTIME))
    report = {
        'status': 'RUNNING',
        'timestamp_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'reviewer': 'Agent #101 runtime specialist',
        'authorship_disclosure': 'Reviewer authored Agent101DigitPairs, not MultiplicityBounds, SplitEnumeration, NumericFibers, or the preserved base. Compilation is fresh for all five.',
        'fresh_build_dir': str(build),
        'sources': {},
        'commands': [],
        'allowed_axioms': sorted(ALLOWED),
        'exceptions': [],
    }

    def save():
        report_path.write_text(json.dumps(report, indent=2) + '\n')

    environment = dict(os.environ)
    for key in ['LEAN_PATH', 'LEAN_SRC_PATH', 'LEAN_SYSROOT']:
        environment.pop(key, None)
    environment['LEAN_PATH'] = str(build)
    report['lean_path'] = str(build)
    report['preload'] = environment.get('LD_PRELOAD', '')

    def run(label, arguments):
        print('RUN ' + label, flush=True)
        command = [str(LEAN), *arguments]
        start = time.monotonic()
        proc = subprocess.run(command, cwd=build, env=environment, text=True, capture_output=True)
        output = proc.stdout + proc.stderr
        log = EVIDENCE / ('full-review.' + label + '.log')
        write_once(log, output.encode())
        report['commands'].append({'label': label, 'command': command, 'cwd': str(build),
            'exit_code': proc.returncode, 'seconds': round(time.monotonic() - start, 6),
            'log': str(log), 'log_sha256': digest(output.encode())})
        save()
        assert proc.returncode == 0, ('command failed', label, proc.returncode, str(log))
        return output

    save()
    try:
        new_exports = []
        for module, (filename, expected) in EXPECTED.items():
            source = ROOT / 'proofs' / filename
            data = source.read_bytes()
            assert digest(data) == expected, ('source pin mismatch', module)
            (build / (module + '.lean')).write_bytes(data)
            write_once(EVIDENCE / ('full-review.' + module + '.lean'), data)
            public = re.findall(r'^(?:def|theorem|lemma|abbrev)\s+(\w+)', data.decode(), re.M)
            report['sources'][module] = {'path': str(source), 'source_sha256': expected,
                'snapshot': str(build / (module + '.lean')), 'bytes': len(data)}
            if module.startswith('Agent101'):
                names = ['Agent101.' + name for name in public]
                report['sources'][module]['public_exports'] = names
                new_exports.extend(names)

        report['lean_sha256'] = digest(LEAN.read_bytes())
        assert report['lean_sha256'] == '92c3d35b5bfaa5e0fea413a775d504cf46cd95e1345df61c2274f76779e7e023'
        report['lean_version'] = run('version', ['--version']).strip()
        assert 'version 4.19.0,' in report['lean_version'] and 'commit 6caaee842e94,' in report['lean_version']
        for module in EXPECTED:
            run(module, ['-j1', '-DElab.async=false', '-o', module + '.olean', module + '.lean'])
            report['sources'][module]['olean_sha256'] = digest((build / (module + '.olean')).read_bytes())

        checker = ROOT / 'proofs/check__4f76e6046a854590.py'
        code = checker.read_text()
        tree = ast.parse(code)
        generator = next(node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == 'audit_source')
        namespace = {'json': json}
        exec(compile(ast.Module(body=[generator], type_ignores=[]), str(checker), 'exec'), namespace)
        report['audit_generator_source_sha256'] = digest(checker.read_bytes())
        audit = namespace['audit_source'](list(EXPECTED))
        (build / 'FullCompiledAudit.lean').write_text(audit)
        write_once(EVIDENCE / 'full-review.compiled-audit.lean', audit.encode())
        compiled_output = run('compiled-audit', ['--trust=0', '-j1', '-DElab.async=false', 'FullCompiledAudit.lean'])
        inventory = re.findall(r'^AUDIT_THEOREM (\S+) (\S+)$', compiled_output, re.M)
        compiled_axioms = axiom_records(compiled_output)
        assert len(inventory) == len({name for _, name in inventory})
        assert set(compiled_axioms) == {name for _, name in inventory}
        assert set(EXPECTED) <= set(re.findall(r'^AUDIT_IMPORT (\S+)$', compiled_output, re.M))
        report['compiled_theorem_count'] = len(inventory)
        report['compiled_theorems_per_module'] = {module: sum(m == module for m, _ in inventory) for module in EXPECTED}
        report['compiled_theorem_axioms'] = compiled_axioms
        report['unsafe_implementation_axioms'] = re.findall(r'^UNSAFE_IMPLEMENTATION_AXIOM (\S+) (\S+)$', compiled_output, re.M)

        public_audit = 'import Agent101NumericFibers\n\n' + '\n'.join('#print axioms ' + name for name in new_exports) + '\n'
        (build / 'NewPublicExportsAudit.lean').write_text(public_audit)
        write_once(EVIDENCE / 'full-review.public-audit.lean', public_audit.encode())
        public_output = run('public-audit', ['--trust=0', '-j1', '-DElab.async=false', 'NewPublicExportsAudit.lean'])
        public_axioms = axiom_records(public_output)
        assert set(public_axioms) == set(new_exports)
        report['new_public_export_count'] = len(public_axioms)
        report['new_public_export_axioms'] = public_axioms
        report['axiom_union'] = sorted({a for values in list(compiled_axioms.values()) + list(public_axioms.values()) for a in values})
        for record in report['sources'].values():
            assert digest(Path(record['path']).read_bytes()) == record['source_sha256'], 'Live source changed during review.'
            assert digest(Path(record['snapshot']).read_bytes()) == record['source_sha256'], 'Build source changed during review.'
        report['source_identity_rechecked_at_end'] = True
        report['status'] = 'PASS'
    except Exception as error:
        report['status'] = 'FAIL'
        report['exceptions'].append(repr(error))
        raise
    finally:
        save()
        print(json.dumps({key: report[key] for key in ['status', 'fresh_build_dir', 'exceptions']}, indent=2), flush=True)
    print('PUBLIC EXPORTS', report['new_public_export_count'], 'COMPILED THEOREMS', report['compiled_theorem_count'], flush=True)


if __name__ == '__main__':
    main()
