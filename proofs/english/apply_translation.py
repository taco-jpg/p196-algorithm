#!/usr/bin/env python3
"""Apply reviewed English text patches without executing research code.

Original research archives remain byte-identical. English archive views are
reading copies, not substitute build inputs or new verification records.
"""
from __future__ import annotations
import ast, hashlib, json, os, pathlib, re, subprocess, sys

BASE = '1f4ed4c5033754521c198506ad4b669232cad09f'
FIRST = '3ff54bb56819f346f1165bc7184362a1e5807729'
ROOT = pathlib.Path.cwd()
OWN = ROOT / 'proofs/english'
CJK = re.compile(r'[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uac00-\ud7af\u0400-\u052f\u0600-\u06ff]')
LANDING = {'AGENTS.md', 'README.md', 'proofs/README.md', 'proofs/STATUS.md', 'proofs/OPEN_PROBLEMS.md', 'calculation/README.md'}

def git(*args):
    return subprocess.check_output(['git', *args])

def digest(data):
    return hashlib.sha256(data).hexdigest()

def read_blob(oid):
    return git('cat-file', 'blob', oid)

def tree(ref):
    rows = {}
    for entry in git('ls-tree', '-rz', '--full-tree', ref).split(b'\0'):
        if not entry:
            continue
        meta, path = entry.split(b'\t', 1)
        mode, kind, oid = meta.decode().split()
        rows[path.decode()] = {'mode': mode, 'type': kind, 'oid': oid}
    return rows

def masked_ast(text):
    parsed = ast.parse(text)
    class Mask(ast.NodeTransformer):
        def visit_Constant(self, node):
            if isinstance(node.value, str):
                node.value = '<reviewed-text>'
            return node
    return ast.dump(Mask().visit(parsed), include_attributes=False)

def main():
    source_tree = tree(BASE)
    first_tree = tree(FIRST)
    head_tree = tree('HEAD')
    previous_path = OWN / 'translation_manifest.json'
    previous = json.loads(previous_path.read_text()) if previous_path.exists() else {}
    owned_hashes = {r['output_path']: r['output_sha256'] for r in previous.get('translations', [])}
    patches = {}
    for file in sorted(OWN.glob('*-patches.json')):
        for prefix, changes in json.loads(file.read_text()).items():
            if prefix in patches:
                raise RuntimeError('Duplicate source patch: ' + prefix)
            matches = {r['oid'] for r in source_tree.values() if r['oid'].startswith(prefix)}
            if len(matches) != 1:
                raise RuntimeError('Source prefix is not unique: ' + prefix)
            patches[prefix] = changes
    # Reuse translations only for byte-identical original lines. This includes
    # identical older README paragraphs and duplicate preserved source copies.
    memory = {}
    for prefix, changes in patches.items():
        oid = next(r['oid'] for r in source_tree.values() if r['oid'].startswith(prefix))
        lines = read_blob(oid).decode('utf-8').splitlines()
        for index, translated in changes.items():
            old = lines[int(index) - 1]
            if not CJK.search(old):
                raise RuntimeError('Patch does not identify non-English text: ' + prefix + ':' + index)
            if CJK.search(translated):
                raise RuntimeError('Untranslated script in reviewed patch')
            if old in memory and memory[old] != translated:
                raise RuntimeError('Conflicting translation of identical source text')
            memory[old] = translated
    written = []
    records = []
    pending = []
    binary = []
    current_changes = {}
    def write(path, data, source_oid=None):
        target = ROOT / path
        if target.is_symlink():
            raise RuntimeError('Refusing symlink output: ' + path)
        if target.exists():
            old = target.read_bytes()
            if old == data:
                return
            allowed = owned_hashes.get(path)
            is_source = source_oid is not None and path in head_tree and head_tree[path]['oid'] == source_oid
            if not is_source and (allowed is None or digest(old) != allowed):
                raise RuntimeError('Unrecognized concurrent output: ' + path)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        written.append(path)
    for path, meta in source_tree.items():
        if meta['type'] != 'blob' or meta['mode'] == '120000':
            continue
        raw = read_blob(meta['oid'])
        try:
            text = raw.decode('utf-8')
            if '\0' in text:
                raise UnicodeError('binary')
        except UnicodeError:
            binary.append(path)
            continue
        if not CJK.search(text):
            continue
        if path in LANDING:
            output = (ROOT / path).read_bytes()
            if head_tree[path]['oid'] != first_tree[path]['oid']:
                raise RuntimeError('Landing page changed after the reviewed translation: ' + path)
            records.append({'source_path': path, 'source_blob': meta['oid'], 'source_sha256': digest(raw), 'output_path': path, 'output_sha256': digest(output), 'kind': 'current_translation', 'verification': 'Previously published exact English translation; original retained separately.'})
            continue
        lines = []
        for line in text.splitlines(keepends=True):
            body = line.rstrip('\r\n')
            ending = line[len(body):]
            if body in memory:
                body = memory[body]
            elif set(CJK.findall(body)) == {'\u548c'}:
                body = body.replace('\u548c', 'and')
            lines.append(body + ending)
        translated = ''.join(lines)
        if path == 'proofs/RESULTS.md':
            if meta['oid'] != '8e815c9946fb2fe6c91a761480a122953fc1dc48b':
                # The immutable BASE and exact table shape are also checked;
                # the prefix avoids trusting an unobserved full object ID.
                if not meta['oid'].startswith('8e815c9946'):
                    raise RuntimeError('Unexpected results source')
            src = text.splitlines()
            if sum(line.startswith('| [') for line in src) != 2570:
                raise RuntimeError('Unexpected results table size')
            translated_lines = []
            for line in src:
                if line.startswith('# '):
                    line = '# Research results and current source'
                elif line.startswith('| ['):
                    cells = line.split('|')
                    if len(cells) != 5:
                        raise RuntimeError('Unexpected results row')
                    line = cells[0] + '|' + cells[1] + '| Classified by original path; the owner waived content review for that reorganization | Not rechecked in that reorganization; original claims retained |'
                elif line.startswith('| ') and CJK.search(line):
                    line = '| Current file | Review performed in the reorganization | Original evidence classification |'
                elif CJK.search(line):
                    line = 'The owner waived content review and build checks for the reorganization. The classification below follows original paths only; the original claims were not rechecked in that pass.'
                translated_lines.append(line)
            translated = '\n'.join(translated_lines) + '\n'
        remaining = [i for i, line in enumerate(translated.splitlines(), 1) if CJK.search(line)]
        if remaining:
            pending.append({'source_path': path, 'source_blob': meta['oid'], 'remaining_lines': remaining})
            continue
        if path.endswith('.py'):
            if masked_ast(text) != masked_ast(translated):
                raise RuntimeError('Executable structure changed: ' + path)
            compile(translated, path, 'exec')
            check = 'Python parsed successfully; AST unchanged after masking reviewed text literals. Diagnostic/docstring/title/scope text may change; no arithmetic or control-flow changes.'
        elif path.endswith('.json'):
            json.loads(translated)
            check = 'JSON parses; English reading copy only, not original verification evidence.'
        else:
            check = 'Only reviewed non-English lines and the isolated English conjunction were translated; other lines retained.'
        archive = path.startswith('proofs/archive/')
        output_path = 'proofs/english/views/' + path if archive else path
        data = translated.encode('utf-8')
        write(output_path, data, None if archive else meta['oid'])
        if not archive:
            current_changes[path] = digest(data)
            backup = 'proofs/archive/english-translation-originals/' + BASE + '/' + path
            if backup in head_tree and head_tree[backup]['oid'] != meta['oid']:
                raise RuntimeError('Original backup mismatch: ' + backup)
            if backup not in head_tree:
                write(backup, raw)
        records.append({'source_path': path, 'source_blob': meta['oid'], 'source_sha256': digest(raw), 'output_path': output_path, 'output_sha256': digest(data), 'kind': 'archive_reading_copy' if archive else 'current_translation', 'verification': check})
    # A translated source must never be passed off as the exact historical bytes.
    # Original-layout replay uses preserved originals for those five paths;
    # unchanged numerical source hashes and every historical record stay intact.
    map_path = ROOT / 'proofs/SOURCE_MAP.json'
    mapping = json.loads(read_blob(source_tree['proofs/SOURCE_MAP.json']['oid']))
    adjusted = []
    for old, info in mapping['paths'].items():
        current = info.get('current')
        if current in current_changes:
            info['current'] = None
            info['english_current'] = current
            info['english_sha256'] = current_changes[current]
            info['english_note'] = 'Language-only reading/current presentation; replay the preserved source for the original exact-byte verification record.'
            adjusted.append(old)
    map_bytes = (json.dumps(mapping, ensure_ascii=False, indent=2) + '\n').encode()
    if map_path.read_bytes() != map_bytes:
        if 'proofs/SOURCE_MAP.json' not in owned_hashes and head_tree['proofs/SOURCE_MAP.json']['oid'] != source_tree['proofs/SOURCE_MAP.json']['oid']:
            raise RuntimeError('Source mapping changed concurrently')
        owned_hashes['proofs/SOURCE_MAP.json'] = digest(map_path.read_bytes())
        write('proofs/SOURCE_MAP.json', map_bytes)
    records.append({'source_path': 'proofs/SOURCE_MAP.json', 'source_blob': source_tree['proofs/SOURCE_MAP.json']['oid'], 'output_path': 'proofs/SOURCE_MAP.json', 'output_sha256': digest(map_bytes), 'kind': 'historical_replay_mapping', 'verification': 'Historical hashes preserved; only translated current paths are routed to their immutable originals for historical replay.', 'adjusted_paths': adjusted})
    status = 'TEXT_TRANSLATION_COMPLETE' if not pending else 'IN_PROGRESS'
    manifest = {'agent': 'Agent #1', 'baseline': BASE, 'status': status, 'translations': records, 'pending': pending, 'binary_files_preserved_without_repacking': binary, 'scope': 'Tracked UTF-8 text containing the inventoried non-English scripts. Mathematical symbols, original archives, binary data, and published Git history are preserved. English archive views are translations, not new builds.'}
    manifest_bytes = (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode()
    previous_path.parent.mkdir(parents=True, exist_ok=True)
    previous_path.write_bytes(manifest_bytes)
    written.append('proofs/english/translation_manifest.json')
    index = ['# English repository reading index', '', 'Current entry pages and completed current-file translations are English. Historical originals remain immutable; English archive views below are reading copies, not replacement verification records.', '', 'Translation does not independently verify or upgrade any mathematical claim. Relative links inside historical reading copies retain the original document layout; use each original source link when a target has not yet received an English view.', '', 'Status: **' + status + '**. Baseline: `' + BASE + '`.', '', '## Available English texts', '']
    for r in records:
        if r['kind'] == 'historical_replay_mapping':
            continue
        output = os.path.relpath(ROOT / r['output_path'], OWN)
        original = 'https://github.com/taco-jpg/p196-algorithm/blob/' + BASE + '/' + r['source_path']
        index.append('- [' + r['source_path'] + '](' + output + ') — [original](' + original + ').')
    if pending:
        index += ['', '## Remaining text translation', '']
        index += ['- `' + r['source_path'] + '` (' + str(len(r['remaining_lines'])) + ' non-English lines remain).' for r in pending]
    (OWN / 'README.md').write_text('\n'.join(index) + '\n')
    written.append('proofs/english/README.md')
    record_path = ROOT / 'proofs/ENGLISH_TRANSLATION.json'
    role = json.loads(record_path.read_text())
    role.update({'status': status, 'current_translation_files': sum(r['kind'] == 'current_translation' for r in records), 'archive_reading_copies': sum(r['kind'] == 'archive_reading_copy' for r in records), 'pending_text_files': len(pending), 'manifest': 'proofs/english/translation_manifest.json', 'room_status': 'ROOM_ACCESS_BLOCKED', 'room_messages_delivered': 0, 'mathematical_verification_claim': 'None; source-language validation only. Historical evidence bytes and classifications preserved.'})
    record_path.write_text(json.dumps(role, indent=2) + '\n')
    written.append('proofs/ENGLISH_TRANSLATION.json')
    # Generated changes may touch only declared current outputs and new views,
    # never the immutable original archive or an existing workflow.
    changed = git('diff', '--name-only').decode().splitlines()
    if any(path not in written for path in changed):
        raise RuntimeError('Unexpected existing-file changes: ' + repr(changed))
    deleted = git('diff', '--name-only', '--diff-filter=D')
    if deleted:
        raise RuntimeError('Deletion forbidden')
    git('add', '--', *sorted(set(written)))
    git('diff', '--cached', '--check')
    print(json.dumps({'status': status, 'current_translations': role['current_translation_files'], 'archive_views': role['archive_reading_copies'], 'pending_files': len(pending), 'changed_paths': sorted(set(written))}, indent=2))

if __name__ == '__main__':
    main()
