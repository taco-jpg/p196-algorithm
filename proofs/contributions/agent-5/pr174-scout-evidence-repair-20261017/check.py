#!/usr/bin/env python3
"""Fresh immutable-source census. Standard library + Git; never executes source."""
import argparse
from collections import Counter
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import resource
import subprocess
import sys
import traceback

COORD = '4c9e6e7aa08147f3798ffad8657c08512e7774c8'
SOURCE = 'c42dd0b6accedd27424a9511f8c06b651d21779e'
HEAD = '790ee166caf3c60c7176d53209e3e755e7ed9a9d'
TREES = {'coord': '1956c527dd28622f5af4e3b4f03f6e240724e479',
         'source': '02899f94d687aa09bcbe893367fb8333abaf0621'}
REPORT = 'proofs/contributions/agent-1/periodic-nine-control-20261017/scope/source-census.md'
REPORT_SHA256 = 'f233d4b20ab3c5010d0fb8e21e59d680e07057fd8ca2ca3bef39aa78d2031bec'
TASK_PREFIX = 'proofs/coordination/tasks/'
PYTHON_SOURCE = 'proofs/periodic_word_quotient__8404d0a63dd1fa13.py'
PINS = {
    'proofs/Agent1PeriodicGuard.lean': '4ba3877f27250e066bbe19dd066b55fa667576281e8dc984334b9a9b82fcee91',
    'proofs/Agent1PeriodicDigits.lean': 'dc6cc1dadb74c4927f0635107fdc1eb62cebac3038dea4e97ad4229fc8703eab',
    'proofs/Agent1PeriodicCenterStrip.lean': '566c7c5eac1fa54b98a9150a21f7ac61c403d8b0391b7aa92c1dbdea51c300c3',
    'proofs/Agent1PeriodicQuotient.lean': '562ad271c282a8a246de344b5fa9ea7e96bd64f74098c3799c839853e792a9a4',
    'proofs/Agent1PeriodicNines.lean': 'b8aae1033e8e90c78f48888ea698e5d345c21e6b99970842dc5a9f3341cd193c',
    'proofs/contributions/agent-1/periodic-block-strip-20261016/center-author/CenterControls.lean': '12a79173d4ac5979ff8c951d80b541f5cbce3cc98ed0c509d8bf7cbe95c59f05',
    'proofs/Agent1PeriodicSafetyBoundary.lean': '41ff84ccf6b5affdf74540c1c4d9e2377876d08f1916dab55151336c8d54df31',
}
# Explicit NEW selection, not an inference about the missing eleven-file list.
EXTRA_SOURCES = [PYTHON_SOURCE, 'proofs/Agent1PeriodicCenterWrap.lean']
API_TERMS = ['stripPeriodCenter', 'stripPeriodCenterAux',
             'stripPeriodCenter_decomposition', 'stripPeriodCenter_maximal',
             'stripPeriodCenter_length', 'centerPeriods', 'quotientCenter',
             'ValidPeriodic', 'leftEntry', 'leftCarry', 'rightEntry',
             'rawGamma', 'rawOuter', 'rawPeriod', 'rawCenter', 'quotientOuter',
             'absorbed_center_pairs', 'two_nonsymmetric_periods', 'tens_quotient']
LITERAL_H = '[9,9,9,14,18,18,14,9,9,9]'
SPACED_H = r'\[\s*9\s*,\s*9\s*,\s*9\s*,\s*14\s*,\s*18\s*,\s*18\s*,\s*14\s*,\s*9\s*,\s*9\s*,\s*9\s*\]'
OWNERSHIP_PATTERNS = {
    'periodic_context': r'periodic',
    'center_strip_context': r'cent(?:er|re)[ _-]*strip|strip[ _-]*cent(?:er|re)',
    'nine_context': r'\bnines?\b|nine[-_]',
    'finite_control_context': r'finite[\s_-]+control|counterexample',
    'extra_removal_context': r'extra[\s_-]+(?:remov|strip)|multiple[\s_-]+strip',
    'strip_bound_context': r'centerPeriods|strip.{0,30}bound|bound.{0,30}strip',
    'closest_controls': r'two_nonsymmetric_periods|tens_quotient',
    'exact_H_allow_whitespace': SPACED_H,
}
LIMIT = 384 * 1024 * 1024


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def git_hash(kind, data):
    return hashlib.sha1(kind.encode() + b' ' + str(len(data)).encode() + b'\0' + data).hexdigest()


def dump(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False, sort_keys=True) + '\n', encoding='utf-8')


def safe_path(path):
    p = PurePosixPath(path)
    require(not p.is_absolute() and '..' not in p.parts and path != '', 'Unsafe tree path: ' + path)
    return path


class Checker:
    def __init__(self, repo, output):
        self.repo = repo.resolve()
        self.out = output.resolve()
        require(not self.out.exists(), '--output must name a new directory')
        self.out.mkdir(parents=True, exist_ok=False)
        (self.out / 'raw').mkdir()
        self.env = {**os.environ, 'GIT_NO_LAZY_FETCH': '1', 'GIT_TERMINAL_PROMPT': '0',
                    'LC_ALL': 'C', 'GIT_OPTIONAL_LOCKS': '0'}
        self.commands = []
        self.batch = None
        self.batch_stderr = None
        self.requests = None
        self.responses = None

    def command(self, label, tail):
        argv = ['git', '-C', str(self.repo), *tail]
        p = subprocess.run(argv, capture_output=True, env=self.env)
        (self.out / ('raw/' + label + '.stdout')).write_bytes(p.stdout)
        (self.out / ('raw/' + label + '.stderr')).write_bytes(p.stderr)
        self.commands.append({'label': label, 'argv': argv, 'exit': p.returncode,
                              'stdout_sha256': sha256(p.stdout), 'stderr_sha256': sha256(p.stderr)})
        dump(self.out / 'commands.json', self.commands)
        require(p.returncode == 0, 'Git command failed: ' + label)
        return p.stdout

    def tree(self, label, commit):
        raw_commit = self.command(label + '-commit', ['cat-file', 'commit', commit])
        require(git_hash('commit', raw_commit) == commit, 'Commit identity mismatch')
        root = raw_commit.splitlines()[0].decode().split(' ', 1)[1]
        if label in TREES:
            require(root == TREES[label], 'Unexpected immutable tree')
        raw = self.command(label + '-tree', ['ls-tree', '-r', '-z', '--full-tree', commit])
        rows = []
        for record in raw.split(b'\0'):
            if not record:
                continue
            meta, pathbytes = record.split(b'\t', 1)
            mode, kind, oid = meta.decode('ascii').split()
            path = safe_path(pathbytes.decode('utf-8'))
            rows.append({'path': path, 'mode': mode, 'type': kind, 'git_blob': oid})
        require(len(rows) == len({r['path'] for r in rows}), 'Duplicate tree path')
        dump(self.out / ('trees/' + label + '.json'), {'commit': commit, 'tree': root, 'entries': rows})
        return {r['path']: r for r in rows}

    def start_batch(self):
        argv = ['git', '-C', str(self.repo), 'cat-file', '--batch']
        self.batch_stderr = (self.out / 'raw/blob-batch.stderr').open('wb')
        self.requests = (self.out / 'raw/blob-batch.requests').open('wb')
        self.responses = (self.out / 'raw/blob-batch.responses.jsonl').open('w', encoding='utf-8')
        self.batch = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                      stderr=self.batch_stderr, env=self.env)
        self.commands.append({'label': 'blob-batch', 'argv': argv, 'exit': None,
                              'request_file': 'raw/blob-batch.requests',
                              'response_file': 'raw/blob-batch.responses.jsonl',
                              'payload_retention': 'All tasks and selected sources; complete search matches and all blob identities'})
        dump(self.out / 'commands.json', self.commands)

    def blob(self, oid):
        request = oid.encode('ascii') + b'\n'
        self.requests.write(request)
        self.batch.stdin.write(request)
        self.batch.stdin.flush()
        header = self.batch.stdout.readline()
        require(header.endswith(b'\n'), 'Incomplete Git batch header')
        fields = header.decode('ascii').strip().split()
        require(len(fields) == 3 and fields[:2] == [oid, 'blob'], 'Missing or wrong Git blob: ' + header.decode())
        length = int(fields[2])
        require(length <= 64 * 1024 * 1024, 'Unexpectedly large source blob')
        data = self.batch.stdout.read(length)
        require(len(data) == length and self.batch.stdout.read(1) == b'\n', 'Truncated Git batch object')
        require(git_hash('blob', data) == oid, 'Git blob hash mismatch')
        self.responses.write(json.dumps({'git_blob': oid, 'type': 'blob', 'bytes': length, 'sha256': sha256(data)}, sort_keys=True) + '\n')
        return data

    def finish_batch(self):
        if self.batch is None:
            return
        self.batch.stdin.close()
        status = self.batch.wait()
        self.batch_stderr.close()
        self.requests.close()
        self.responses.close()
        self.commands[-1]['exit'] = status
        dump(self.out / 'commands.json', self.commands)
        self.batch = None
        require(status == 0, 'Git batch returned failure')

    def write_bytes(self, path, data):
        target = self.out / safe_path(path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)

    def run(self):
        coord = self.tree('coord', COORD)
        source = self.tree('source', SOURCE)
        head = self.tree('head', HEAD)
        tasks = [coord[p] for p in sorted(coord) if p.startswith(TASK_PREFIX)]
        corpus = [source[p] for p in sorted(source) if p.endswith(('.lean', '.py', '.md'))]
        require(tasks, 'Empty immutable task tree')
        require(all(r['type'] == 'blob' and r['mode'] in ('100644', '100755') for r in tasks + corpus), 'Non-regular selected path')
        require(REPORT in head, 'Missing published census report')
        require(all(p in source for p in PINS), 'A principal pin is absent at SOURCE')
        require(all(p in source for p in EXTRA_SOURCES), 'An explicitly selected extra source is absent')
        self.start_batch()
        report = self.blob(head[REPORT]['git_blob'])
        require(sha256(report) == REPORT_SHA256, 'Unexpected source-census bytes')
        self.write_bytes('historical-report/source-census.md', report)
        dump(self.out / 'historical-report/identity.json', {**head[REPORT], 'commit': HEAD,
             'sha256': sha256(report), 'bytes': len(report), 'classification': 'Actual published historical report; lost referenced bundle not recovered'})
        ownership_res = {k: re.compile(v, re.IGNORECASE) for k, v in OWNERSHIP_PATTERNS.items()}
        task_manifest = []
        candidates = []
        ownership_matches = []
        for row in tasks:
            raw = self.blob(row['git_blob'])
            text = raw.decode('utf-8')
            parsed = json.loads(text)
            require(isinstance(parsed, dict), 'Task JSON is not an object')
            stored = 'task-records/' + row['path']
            self.write_bytes(stored, raw)
            task_manifest.append({**row, 'commit': COORD, 'bytes': len(raw), 'sha256': sha256(raw), 'stored_path': stored})
            labels = [name for name, rx in ownership_res.items() if rx.search(row['path'] + '\n' + text)]
            if labels:
                candidates.append({'path': row['path'], 'git_blob': row['git_blob'], 'labels': labels,
                                   'task_id': parsed.get('task_id', parsed.get('id')),
                                   'status': parsed.get('status'),
                                   'owner': parsed.get('owner', parsed.get('agent'))})
            for n, line in enumerate(text.splitlines(), 1):
                matches = [name for name, rx in ownership_res.items() if rx.search(line)]
                if matches:
                    ownership_matches.append({'path': row['path'], 'line': n, 'labels': matches, 'text': line})
        dump(self.out / 'task-manifest.json', task_manifest)
        dump(self.out / 'ownership-candidates.json', candidates)
        with (self.out / 'ownership.matches.jsonl').open('w', encoding='utf-8') as f:
            for row in ownership_matches:
                f.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + '\n')
        # Each unique content blob is read once for corpus searching; every tree path is indexed separately.
        by_oid = {}
        for row in corpus:
            by_oid.setdefault(row['git_blob'], []).append(row)
        searches = ['api', 'literal-H', 'whitespace-H']
        match_files = {name: (self.out / (name + '.matches.jsonl')).open('w', encoding='utf-8') for name in searches}
        indexes = {name: [] for name in searches}
        counts = {name: 0 for name in searches}
        source_manifest = []
        corpus_manifest = []
        whitespace_rx = re.compile(SPACED_H)
        for oid in sorted(by_oid):
            raw = self.blob(oid)
            text = raw.decode('utf-8')
            require(b'\0' not in raw, 'Binary NUL in selected text source: ' + oid)
            lines = text.splitlines()
            matches = {'api': [], 'literal-H': [], 'whitespace-H': []}
            for n, line in enumerate(lines, 1):
                terms = [term for term in API_TERMS if term in line]
                if terms:
                    matches['api'].append({'line': n, 'terms': terms, 'text': line})
                if LITERAL_H in line:
                    matches['literal-H'].append({'line': n, 'text': line})
            # This supplementary search also covers whitespace/newlines between coefficients.
            for m in whitespace_rx.finditer(text):
                matches['whitespace-H'].append({'line': text.count('\n', 0, m.start()) + 1,
                    'character_start': m.start(), 'character_end': m.end(), 'text': m.group(0)})
            for row in sorted(by_oid[oid], key=lambda x: x['path']):
                item = {**row, 'commit': SOURCE, 'bytes': len(raw), 'sha256': sha256(raw), 'utf8': True, 'binary_nul': False}
                corpus_manifest.append(item)
                for name in searches:
                    eligible = name != 'api' or row['path'].endswith(('.lean', '.py'))
                    found = matches[name] if eligible else []
                    indexes[name].append({'path': row['path'], 'git_blob': oid,
                         'searched': eligible, 'match_count': len(found),
                         'match_lines': [m['line'] for m in found]})
                    for match in found:
                        match_files[name].write(json.dumps({'path': row['path'], 'git_blob': oid, **match}, ensure_ascii=False, sort_keys=True) + '\n')
                    counts[name] += len(found)
                if row['path'] in PINS or row['path'] in EXTRA_SOURCES:
                    principal = row['path'] in PINS
                    if principal:
                        require(sha256(raw) == PINS[row['path']], 'Report SHA256 pin mismatch: ' + row['path'])
                        require(PINS[row['path']].encode() in report, 'Hardcoded pin absent from original report')
                        require(row['path'] in head and head[row['path']]['git_blob'] == oid, 'Principal source differs at H')
                    stored = 'source-files/' + row['path']
                    self.write_bytes(stored, raw)
                    source_manifest.append({**item, 'stored_path': stored,
                         'selection': 'principal explicitly named in historical report' if principal else 'NEW explicit supporting selection, not missing eleven-file membership',
                         'report_sha256': PINS.get(row['path']),
                         'same_blob_at_H': row['path'] in head and head[row['path']]['git_blob'] == oid})
        for f in match_files.values():
            f.close()
        self.finish_batch()
        require(len(source_manifest) == len(PINS) + len(EXTRA_SOURCES), 'Selected source count mismatch')
        for name in searches:
            indexes[name].sort(key=lambda r: r['path'])
            dump(self.out / (name + '.index.json'), indexes[name])
        dump(self.out / 'source-manifest.json', sorted(source_manifest, key=lambda r: r['path']))
        dump(self.out / 'search-corpus-manifest.json', sorted(corpus_manifest, key=lambda r: r['path']))
        specification = {
            'classification': 'Fresh replacement data verification, not recovery/reproduction of original scout execution',
            'coord_commit': COORD, 'source_commit': SOURCE, 'original_PR_head': HEAD,
            'task_selection': 'Every recursive regular blob under proofs/coordination/tasks/; JSON must parse',
            'ownership_selection': {'patterns': OWNERSHIP_PATTERNS, 'flags': ['IGNORECASE'],
                 'scope': 'path plus full unmodified task JSON text; candidate selection is not a semantic non-overlap proof'},
            'api_search': {'extensions': ['.lean', '.py'], 'case_sensitive': True,
                 'method': 'Fixed substring OR over API_TERMS; each physical text line emitted once with all matching terms',
                 'terms': API_TERMS, 'splitlines': 'Python str.splitlines; UTF-8 strict; includes comments/strings/archive snapshots'},
            'literal_search': {'extensions': ['.lean', '.py', '.md'], 'case_sensitive': True,
                 'method': 'Exact fixed substring per line', 'literal': LITERAL_H},
            'supplementary_whitespace_search': {'extensions': ['.lean', '.py', '.md'],
                 'pattern': SPACED_H, 'method': 'Python re.finditer over entire UTF-8 file; occurrence count, not line count'},
            'ordering': 'Blob SHA1 ascending, then path ascending, then line/offset; indexes sorted by path',
            'network_during_check': False, 'memory_limit_bytes': LIMIT,
            'execution': 'One Python process, one sequential Git subprocess at a time; no retained source executed',
            'exact_historical_query_known': False,
        }
        dump(self.out / 'search-specification.json', specification)
        search_results = {}
        for name in searches:
            searched = [r for r in indexes[name] if r['searched']]
            search_results[name] = {'searched_paths': len(searched),
                'matching_paths': sum(r['match_count'] > 0 for r in searched),
                'matches': counts[name], 'status': 'MATCHES' if counts[name] else 'NO_MATCHES',
                'complete': True, 'not_historical_query_reproduction': True}
        summary = {'result': 'PASS: fresh data checks only', 'task_records': len(tasks),
             'task_count_equals_report_245': len(tasks) == 245,
             'task_status_counts': dict(sorted(Counter(str(json.loads((self.out / r['stored_path']).read_text()).get('status')) for r in task_manifest).items())),
             'ownership_candidates': len(candidates), 'searches': search_results,
             'principal_report_pins_verified': len(PINS), 'new_supporting_source_selections': len(EXTRA_SOURCES),
             'source_corpus_unique_blobs': len(by_oid),
             'original_scout_bundle': 'NOT_RECOVERED', 'original_eleven_file_selection': 'NOT_RECOVERED',
             'original_raw_search_and_index_failure': 'NOT_RECOVERED',
             'historical_branch_pages_and_API_readbacks': 'NOT_RECOVERED',
             'current_ownership': 'OUT_OF_SCOPE; use parent current ownership audit',
             'math_review': 'Reused unchanged qualification; no Lean or mathematical evaluation',
             'publication_gap_closed': False,
             'parent_independent_review': 'REQUIRED before delivery interpretation'}
        dump(self.out / 'result.json', summary)
        lines = ['# Fresh immutable data checks', '',
             'This is newly generated replacement evidence. It does not recover the original scout bundle,',
             'historical HTTP responses, branch pages, failed/corrected index, or eleven-file selection.', '',
             f'- Coordination: `{COORD}`; actual task records: **{len(tasks)}**.',
             f'- Source: `{SOURCE}`; original report head: `{HEAD}`.',
             f'- Principal report SHA256 pins checked: **{len(PINS)}**; explicitly new supporting selections: **{len(EXTRA_SOURCES)}**.',
             f'- Ownership candidates selected by declared text patterns: **{len(candidates)}**.', '',
             '## Complete fresh search statuses', '', '| Search | Searched paths | Matching paths | Matches | Status |', '| --- | ---: | ---: | ---: | --- |']
        for name, result in search_results.items():
            lines.append(f"| {name} | {result['searched_paths']} | {result['matching_paths']} | {result['matches']} | {result['status']} |")
        lines += ['', 'The API and exact-literal counts are matching lines per Git path. The whitespace search counts occurrences.',
                  'Repeated evidence snapshots are counted separately by path; unique blobs are identified separately.',
                  'All selected files decoded as UTF-8 without NULs. An unreadable file is a failing run, not a skipped file.',
                  'These counts do not certify the historical 3334 lines / 245 files or its unknown query.', '',
                  '## Bounded ownership candidates', '',
                  'A candidate is a task text/path match, not a competing claim. Complete exact task bytes and matched lines are retained.',
                  'Human source/scope comparison is in the package-level FINDINGS.md. No current claim is inferred.', '',
                  '| Task record | Recorded status | Pattern labels |', '| --- | --- | --- |']
        for row in candidates:
            lines.append('| ' + row['path'].removeprefix(TASK_PREFIX) + ' | ' + str(row['status']) + ' | ' + ', '.join(row['labels']) + ' |')
        (self.out / 'REPORT.md').write_text('\n'.join(lines) + '\n', encoding='utf-8')
        manifest = []
        for path in sorted(self.out.rglob('*')):
            if path.is_file():
                data = path.read_bytes()
                manifest.append({'path': path.relative_to(self.out).as_posix(), 'bytes': len(data),
                                 'sha256': sha256(data), 'filesystem_mode': oct(path.stat().st_mode & 0o777)})
        dump(self.out / 'FILES.json', {'excludes': ['FILES.json'], 'files': manifest})
        print(json.dumps(summary, indent=2, sort_keys=True))


def main():
    if sys.flags.optimize:
        raise SystemExit('Refusing optimized Python: run without -O / -OO')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    resource.setrlimit(resource.RLIMIT_AS, (LIMIT, LIMIT))
    checker = Checker(args.repo, args.output)
    try:
        checker.run()
    except BaseException as exc:
        try:
            checker.finish_batch()
        except BaseException:
            pass
        dump(checker.out / 'FAILED.json', {'result': 'FAILED', 'error': repr(exc), 'traceback': traceback.format_exc()})
        raise


if __name__ == '__main__':
    main()
