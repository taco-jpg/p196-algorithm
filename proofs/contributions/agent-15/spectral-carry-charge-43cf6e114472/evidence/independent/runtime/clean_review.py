#!/usr/bin/env python3
"""Independent clean Lean closure build and complete declaration audit.

This tool never writes Git objects or changes the reviewed source tree. It uses
only explicitly selected source modules and official Init/Std imports. Source
acceptance still requires the separate semantic review against the original
claim; a PASS here is compilation/axiom evidence, not that semantic judgment.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import time
import traceback

NAME = re.compile(r'[A-Za-z_][A-Za-z_0-9]*(?:\.[A-Za-z_][A-Za-z_0-9]*)*\Z')
FULL_HASH = re.compile(r'[0-9a-f]{40}\Z')
ALLOWED_AXIOMS = {'propext', 'Classical.choice', 'Quot.sound'}
CORE_IMPORT_ROOTS = {'Init', 'Std'}
FORBIDDEN = re.compile(r"(?<![\w'])\b(?:sorry|admit|axiom|sorryAx|native_decide|ofReduceBool|skipKernelTC|unsafe|partial)\b(?![\w'])")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256(path: Path) -> str:
    with path.open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()


def git_blob(data: bytes) -> str:
    return hashlib.sha1(f'blob {len(data)}\0'.encode() + data).hexdigest()


def mask_comments_and_strings(text: str) -> str:
    """Retain source positions while masking nested Lean comments and strings."""
    out: list[str] = []
    i = depth = 0
    quoted = False
    while i < len(text):
        pair = text[i:i + 2]
        if depth:
            if pair == '/-':
                depth += 1; out.extend('  '); i += 2
            elif pair == '-/':
                depth -= 1; out.extend('  '); i += 2
            else:
                out.append('\n' if text[i] == '\n' else ' '); i += 1
        elif quoted:
            if text[i] == '\\':
                out.extend('  '); i += 2
            else:
                quoted = text[i] != '"'
                out.append('\n' if text[i] == '\n' else ' '); i += 1
        elif pair == '/-':
            depth = 1; out.extend('  '); i += 2
        elif pair == '--':
            end = text.find('\n', i)
            end = len(text) if end < 0 else end
            out.extend(' ' * (end - i)); i = end
        elif text[i] == '"':
            quoted = True; out.append(' '); i += 1
        else:
            out.append(text[i]); i += 1
    if depth or quoted:
        raise ValueError('Unterminated source comment or string')
    return ''.join(out)


def source_imports(code: str, module: str) -> list[str]:
    imports: list[str] = []
    for line_number, line in enumerate(code.splitlines(), 1):
        stripped = line.strip()
        if re.match(r'import\b', stripped):
            fields = stripped.split()
            if len(fields) < 2 or any(not NAME.fullmatch(x) for x in fields[1:]):
                raise ValueError(f'Unsupported import syntax in {module}:{line_number}')
            imports.extend(fields[1:])
    if len(imports) != len(set(imports)):
        raise ValueError('Duplicate imports in ' + module)
    return imports


def audit_source(roots: list[str], modules: list[str], required: list[str]) -> str:
    header = '\n'.join('import ' + name for name in roots)
    return header + '\nimport Lean\n\n' + '''
open Lean Elab Command
set_option pp.universes true
set_option pp.fullNames true
set_option pp.explicit true
set_option maxRecDepth 100000
set_option maxHeartbeats 0

run_cmd do
  let env ← getEnv
  let selected : List String := __SELECTED_MODULES__
  let required : List String := __REQUIRED_DECLARATIONS__
  let allowed : List Name := [``propext, ``Classical.choice, ``Quot.sound]
  let mut names : List String := []
  let mut safeNames : List String := []
  let mut safeCount := 0
  let mut implementationCount := 0
  let mut axiomUnion : List Name := []
  let mut count := 0
  for (name, info) in env.constants.toList do
    if let some idx := env.getModuleIdxFor? name then
      let origin := env.allImportedModuleNames[idx.toNat]!
      if selected.contains origin.toString then
        unless (env.checked.get.find? name).isSome do
          throwError m!"UNCHECKED_DECLARATION {origin} {name}"
        let implementationOnly := info.isUnsafe || info.isPartial
        let kind : String := match info with
          | .axiomInfo _ => "axiom"
          | .defnInfo _ => "definition"
          | .thmInfo _ => "theorem"
          | .opaqueInfo _ => "opaque"
          | .quotInfo _ => "quotient"
          | .inductInfo _ => "inductive"
          | .ctorInfo _ => "constructor"
          | .recInfo _ => "recursor"
        if kind == "axiom" && !implementationOnly then
          throwError m!"NEW_AXIOM {origin} {name}"
        let axioms := (← liftCoreM (Lean.collectAxioms name)).qsort Name.lt
        let axl := axioms.toList
        if !implementationOnly && axl.any (fun ax => !(allowed.contains ax)) then
          throwError m!"DISALLOWED_AXIOMS {origin} {name} : {axl}"
        if implementationOnly then
          implementationCount := implementationCount + 1
        else
          safeCount := safeCount + 1
          safeNames := name.toString :: safeNames
          for ax in axl do
            unless axiomUnion.contains ax do
              axiomUnion := ax :: axiomUnion
        names := name.toString :: names
        count := count + 1
        let record := Json.mkObj [
          ("module", toJson origin.toString),
          ("name", toJson name.toString),
          ("kind", toJson kind),
          ("private", toJson (Lean.isPrivateName name)),
          ("implementation_only", toJson implementationOnly),
          ("unsafe", toJson info.isUnsafe),
          ("partial", toJson info.isPartial),
          ("axioms", toJson (axioms.map Name.toString))]
        logInfo m!"AUDIT_DECL_JSON {record.compress}"
        logInfo m!"SIGNATURE_BEGIN {name}"
        logInfo m!"{name} : {info.type}"
        logInfo m!"SIGNATURE_END {name}"
        elabCommand (← `(#print axioms $(mkIdent name)))
  for name in required do
    unless safeNames.contains name do
      throwError m!"MISSING_REQUIRED_DECLARATION {name}"
  if count == 0 then
    throwError "EMPTY_PROJECT_DECLARATION_AUDIT"
  let summary := Json.mkObj [
    ("count", toJson count),
    ("safe_count", toJson safeCount),
    ("implementation_count", toJson implementationCount),
    ("axiom_union", toJson ((axiomUnion.toArray.qsort Name.lt).map Name.toString))]
  logInfo m!"AUDIT_SUMMARY_JSON {summary.compress}"
'''.replace('__SELECTED_MODULES__', json.dumps(modules)).replace('__REQUIRED_DECLARATIONS__', json.dumps(required))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--lean', type=Path, required=True)
    parser.add_argument('--repo-root', type=Path, required=True)
    parser.add_argument('--source-root', type=Path, required=True)
    parser.add_argument('--source-commit', required=True)
    parser.add_argument('--evidence', type=Path, required=True)
    parser.add_argument('--module', action='append', required=True)
    parser.add_argument('--required-declaration', action='append', required=True)
    parser.add_argument('--exact-module', action='append', default=[])
    parser.add_argument('--public-exports', type=Path, required=True)
    parser.add_argument('--expected-public-export-count', type=int, required=True)
    args = parser.parse_args()
    evidence = args.evidence.absolute()
    evidence.mkdir(parents=True, exist_ok=False)
    logs = evidence / 'logs'; logs.mkdir()
    build = evidence / 'source'; build.mkdir()
    report = {
        'schema_version': 1, 'status': 'RUNNING',
        'review_role': 'Independent nonauthor build and declaration audit',
        'semantic_acceptance': 'SEPARATE_REVIEW_REQUIRED',
        'source_commit': args.source_commit,
        'roots': args.module, 'required_declarations': args.required_declaration,
        'project_objects_reused': False,
        'standard_toolchain_objects_reused': True,
        'allowed_axioms': sorted(ALLOWED_AXIOMS),
        'source_records': {}, 'commands': [],
        'runner_sha256': sha256(Path(__file__)),
        'started_at_epoch': time.time(),
    }

    def save() -> None:
        (evidence / 'verification.json').write_text(json.dumps(report, indent=2) + '\n')

    def run(label: str, argv: list[str], cwd: Path, env: dict[str, str], timeout: int = 600) -> str:
        log = logs / (label + '.log')
        started = time.monotonic()
        with log.open('wb') as stream:
            try:
                code = subprocess.run(argv, cwd=cwd, env=env, stdout=stream,
                                      stderr=subprocess.STDOUT, timeout=timeout).returncode
            except subprocess.TimeoutExpired:
                code = 124
        report['commands'].append({
            'label': label, 'argv': argv, 'cwd': str(cwd),
            'environment': env, 'exit_code': code,
            'elapsed_seconds': time.monotonic() - started,
            'log': str(log.relative_to(evidence)), 'log_sha256': sha256(log),
        })
        save()
        print(f'{label}: exit {code}; {log}', flush=True)
        if code:
            raise RuntimeError('Command failed: ' + label)
        return log.read_text()

    save()
    try:
        repo = args.repo_root.resolve(strict=True)
        source_root = args.source_root.resolve(strict=True)
        lean = args.lean.resolve(strict=True)
        if not source_root.is_relative_to(repo):
            raise ValueError('Source root must belong to the specified repository')
        if not FULL_HASH.fullmatch(args.source_commit):
            raise ValueError('Require a full immutable source commit hash')
        if any(not NAME.fullmatch(x) for x in [*args.module, *args.exact_module, *args.required_declaration]):
            raise ValueError('Unsupported module or declaration name')
        if len(args.module) != len(set(args.module)):
            raise ValueError('Duplicate root modules')
        exports_data = args.public_exports.read_bytes()
        exports_text = exports_data.decode('utf-8').strip()
        public_exports = json.loads(exports_text) if exports_text.startswith('[') else [line.strip() for line in exports_text.splitlines() if line.strip() and not line.lstrip().startswith('#')]
        if not isinstance(public_exports, list) or any(not isinstance(name, str) or not NAME.fullmatch(name) for name in public_exports):
            raise ValueError('Invalid expected public-export list')
        if len(public_exports) != len(set(public_exports)) or len(public_exports) != args.expected_public_export_count:
            raise ValueError('Expected public-export count is missing, duplicated, or changed')
        (evidence / 'expected-public-exports.json').write_text(json.dumps(public_exports, indent=2) + '\n')
        report['public_exports_file'] = str(args.public_exports)
        report['public_exports_source_sha256'] = sha256_bytes(exports_data)
        report['expected_public_exports'] = public_exports
        env = {'PATH': str(lean.parent) + ':/usr/bin:/bin', 'LANG': 'C.UTF-8', 'LEAN_PATH': str(build)}
        git_env = {'PATH': '/usr/bin:/bin', 'LANG': 'C.UTF-8',
                   'GIT_OPTIONAL_LOCKS': '0', 'GIT_TERMINAL_PROMPT': '0',
                   'GIT_NO_LAZY_FETCH': '1'}
        version = run('version', [str(lean), '--version'], build, env).strip()
        if not re.search(r'version 4\.19\.0,.*commit 6caaee842e94, Release', version):
            raise ValueError('Wrong official Lean version: ' + version)
        prefix = Path(run('compiler-prefix', [str(lean), '--print-prefix'], build, env).strip()).resolve(strict=True)
        if prefix / 'bin/lean' != lean:
            raise ValueError('Compiler prefix does not identify the given executable')
        compiler_paths = [lean, *sorted((prefix / 'lib/lean').glob('*.so'))]
        report['compiler'] = {'version': version, 'files': {str(p): sha256(p) for p in compiler_paths}}
        source_bytes: dict[str, bytes] = {}
        source_paths: dict[str, Path] = {}
        imports: dict[str, list[str]] = {}
        standard_imports: dict[str, dict[str, str]] = {}
        order: list[str] = []
        visiting: set[str] = set()

        def visit(module: str) -> None:
            if module.split('.')[0] in {'Init', 'Std', 'Lean'}:
                raise ValueError('Project module shadows a standard-library namespace: ' + module)
            if module in visiting:
                raise ValueError('Local import cycle: ' + module)
            if module in source_bytes:
                return
            path = source_root / (module.replace('.', '/') + '.lean')
            if path.is_symlink() or not path.resolve(strict=True).is_relative_to(source_root):
                raise ValueError('Unsafe source path: ' + str(path))
            data = path.read_bytes()
            code = mask_comments_and_strings(data.decode('utf-8'))
            hits = [{'token': m.group(), 'line': code[:m.start()].count('\n') + 1}
                    for m in FORBIDDEN.finditer(code)]
            if hits:
                raise ValueError(f'Forbidden source constructs in {module}: {hits}')
            deps = source_imports(code, module)
            visiting.add(module)
            for dep in deps:
                local = source_root / (dep.replace('.', '/') + '.lean')
                if local.is_file():
                    visit(dep)
                elif dep.split('.')[0] not in CORE_IMPORT_ROOTS:
                    raise ValueError('Non-Std external import: ' + dep)
                else:
                    official = prefix / 'lib/lean' / (dep.replace('.', '/') + '.olean')
                    if not official.is_file():
                        raise ValueError('Missing official core import: ' + dep)
                    standard_imports[dep] = {'path': str(official), 'sha256': sha256(official)}
            visiting.remove(module)
            source_bytes[module] = data
            source_paths[module] = path
            imports[module] = deps
            order.append(module)

        for module in args.module:
            visit(module)
        if args.exact_module and set(args.exact_module) != set(order):
            raise ValueError('Actual import closure differs from expected modules')
        report['build_order'] = order
        report['standard_direct_imports'] = standard_imports
        relative_paths = [str(source_paths[name].relative_to(repo)) for name in order]
        actual_commit = run('source-commit', ['git', '-C', str(repo), 'rev-parse', '--verify',
                           args.source_commit + '^{commit}'], build, git_env).strip()
        if actual_commit != args.source_commit:
            raise ValueError('Source commit did not resolve exactly')
        tree = run('source-tree', ['git', '-C', str(repo), 'ls-tree', '-r', '--full-tree',
                   args.source_commit, '--', *relative_paths], build, git_env)
        tracked = {}
        for line in tree.splitlines():
            metadata, path = line.split('\t', 1)
            mode, kind, blob = metadata.split()
            tracked[path] = (mode, kind, blob)
        for module in order:
            data = source_bytes[module]
            relative = str(source_paths[module].relative_to(repo))
            mode, kind, blob = tracked.get(relative, ('', '', ''))
            if mode not in {'100644', '100755'} or kind != 'blob' or blob != git_blob(data):
                raise ValueError('Working source differs from frozen commit: ' + relative)
            dest = build / (module.replace('.', '/') + '.lean')
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_bytes(data)
            report['source_records'][module] = {
                'repository_path': relative, 'git_blob': blob,
                'sha256': sha256_bytes(data), 'imports': imports[module],
                'bytes': len(data), 'build_path': str(dest.relative_to(evidence)),
            }
        save()
        flags = ['-j1', '-DElab.async=false', '--trust=0']
        for module in order:
            stem = module.replace('.', '/')
            run('build-' + module, [str(lean), *flags, '-o', stem + '.olean', stem + '.lean'], build, env)
        audit_name = 'IndependentDeclarationAudit'
        if audit_name in order:
            raise ValueError('Reserved independent audit module name')
        all_required = list(dict.fromkeys([*args.required_declaration, *public_exports]))
        generated = audit_source(args.module, order, all_required)
        (build / (audit_name + '.lean')).write_text(generated)
        audit_log = run('all-declarations', [str(lean), *flags, '-o', audit_name + '.olean',
                        audit_name + '.lean'], build, env)
        declarations = [json.loads(line.split(' ', 1)[1]) for line in audit_log.splitlines()
                        if line.startswith('AUDIT_DECL_JSON ')]
        summaries = [json.loads(line.split(' ', 1)[1]) for line in audit_log.splitlines()
                     if line.startswith('AUDIT_SUMMARY_JSON ')]
        if len(summaries) != 1 or not declarations or summaries[0]['count'] != len(declarations):
            raise ValueError('Missing or inconsistent complete declaration audit')
        if len({d['name'] for d in declarations}) != len(declarations):
            raise ValueError('Duplicate declaration audit entries')
        if any(set(d['axioms']) - ALLOWED_AXIOMS for d in declarations if not d['implementation_only']):
            raise ValueError('Disallowed axiom found in reported declarations')
        if not set(args.required_declaration) <= {d['name'] for d in declarations if not d['implementation_only']}:
            raise ValueError('Required endpoints absent from final declaration inventory')
        printed_axioms = re.findall(r"^'(.+)' (?:does not depend on any axioms|depends on axioms: .*)$", audit_log, re.M)
        if set(printed_axioms) != {d['name'] for d in declarations} or len(printed_axioms) != len(declarations):
            raise ValueError('Actual #print axioms commands do not cover every inventoried declaration')
        public_safe = {d['name'] for d in declarations if not d['private'] and not d['implementation_only']}
        if not set(public_exports) <= public_safe:
            raise ValueError('An expected public export is not a safe public project declaration')
        export_module = 'IndependentPublicExports'
        if export_module in order:
            raise ValueError('Reserved public-export audit module name')
        export_source = '\n'.join('import ' + m for m in args.module) + '\n\nset_option pp.universes true\nset_option pp.fullNames true\n\n'
        export_source += '\n'.join('#print ' + name + '\n#print axioms ' + name for name in public_exports) + '\n'
        (build / (export_module + '.lean')).write_text(export_source)
        exports_log = run('public-exports', [str(lean), *flags, '-o', export_module + '.olean', export_module + '.lean'], build, env)
        export_axioms = re.findall(r"^'(.+)' (?:does not depend on any axioms|depends on axioms: .*)$", exports_log, re.M)
        if set(export_axioms) != set(public_exports) or len(export_axioms) != len(public_exports):
            raise ValueError('Actual public-export #print axioms coverage differs from the expected list')
        if args.public_exports.read_bytes() != exports_data:
            raise ValueError('Expected public-export list changed during review')
        report['explicit_public_exports_printed'] = len(public_exports)
        for module in order:
            if source_paths[module].read_bytes() != source_bytes[module]:
                raise ValueError('Original source changed during review: ' + module)
            if (build / (module.replace('.', '/') + '.lean')).read_bytes() != source_bytes[module]:
                raise ValueError('Copied source changed during review: ' + module)
        if any(sha256(Path(path)) != digest for path, digest in report['compiler']['files'].items()):
            raise ValueError('Compiler identity changed during review')
        if any(sha256(Path(item['path'])) != item['sha256'] for item in standard_imports.values()):
            raise ValueError('Official standard-library import changed during review')
        (evidence / 'declarations.json').write_text(json.dumps(declarations, indent=2) + '\n')
        report['declaration_count'] = len(declarations)
        report['safe_declaration_count'] = summaries[0]['safe_count']
        report['implementation_declaration_count'] = summaries[0]['implementation_count']
        report['public_mathematical_declaration_count'] = sum(not d['private'] and not d['implementation_only'] for d in declarations)
        report['implementation_artifacts'] = [d for d in declarations if d['implementation_only']]
        report['axiom_union'] = summaries[0]['axiom_union']
        report['status'] = 'PASS_CLEAN_BUILD_AND_ALL_DECLARATIONS'
        return 0
    except Exception as error:
        report['status'] = 'FAIL'
        report['error'] = str(error)
        (evidence / 'failure.txt').write_text(traceback.format_exc())
        print('FAIL:', error, flush=True)
        return 1
    finally:
        report['finished_at_epoch'] = time.time()
        report['artifacts'] = {str(p.relative_to(evidence)): {'bytes': p.stat().st_size, 'sha256': sha256(p)}
                               for p in sorted(evidence.rglob('*'))
                               if p.is_file() and p.name != 'verification.json'}
        save()


if __name__ == '__main__':
    raise SystemExit(main())
