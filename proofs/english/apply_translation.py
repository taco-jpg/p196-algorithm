#!/usr/bin/env python3
"""Publish reviewed English prose without executing research code.

Immutable historical archives remain the original evidence. English views are
reading copies, not new builds or substitutes for hash-pinned original inputs.
"""
from __future__ import annotations
import ast
import hashlib
import json
import os
import pathlib
import re
import subprocess

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

def load_reviewed_patch(file, written, encoding_repairs):
    raw = file.read_text()
    # A failed unpublished manuscript batch used literal LaTeX backslashes
    # inside JSON strings. Canonicalize that transport representation, keeping
    # every TeX backslash, including doubled row endings. An odd final slash
    # before a quotation mark remains the JSON quotation escape.
    literal_tex = re.search(r'(?<!\\)\\(?:[()\[\]{}]|text\b|underbrace\b|forall\b|quad\b|operatorname\b|mathbb\b)', raw)
    if literal_tex:
        def escape_run(match):
            n = len(match.group())
            quote = match.end() < len(raw) and raw[match.end()] == '"'
            return '\\' * (2 * n - 1 if quote and n % 2 else 2 * n)
        before = digest(raw.encode())
        value = json.loads(re.sub(r'\\+', escape_run, raw))
        canonical = json.dumps(value, ensure_ascii=False, indent=2) + '\n'
        file.write_text(canonical)
        written.append(str(file.relative_to(ROOT)))
        encoding_repairs.append({'path': str(file.relative_to(ROOT)), 'input_sha256': before, 'output_sha256': digest(canonical.encode()), 'reason': 'Canonical JSON encoding of reviewed literal LaTeX; no translation content changed.'})
    else:
        value = json.loads(raw)
    if not isinstance(value, dict):
        raise RuntimeError('Patch root must be a dictionary: ' + str(file))
    for changes in value.values():
        if not isinstance(changes, dict):
            raise RuntimeError('Patch lines must be a dictionary')
        for index, translated in changes.items():
            if not index.isdigit() or not isinstance(translated, str):
                raise RuntimeError('Invalid patch line')
            if any(ord(ch) < 32 for ch in translated):
                raise RuntimeError('Control character in translated line: ' + str(file) + ':' + index)
    return value

def main():
    source_tree = tree(BASE)
    first_tree = tree(FIRST)
    head_tree = tree('HEAD')
    previous_path = OWN / 'translation_manifest.json'
    previous = json.loads(previous_path.read_text()) if previous_path.exists() else {}
    owned_hashes = {r['output_path']: r['output_sha256'] for r in previous.get('translations', [])}
    written, encoding_repairs = [], []
    patches = {}
    for file in sorted(OWN.glob('*-patches.json')):
        for prefix, changes in load_reviewed_patch(file, written, encoding_repairs).items():
            matches = {r['oid'] for r in source_tree.values() if r['oid'].startswith(prefix)}
            if len(matches) != 1:
                raise RuntimeError('Source prefix is not unique: ' + prefix)
            oid = matches.pop()
            if oid in patches:
                raise RuntimeError('Duplicate source patch: ' + prefix)
            patches[oid] = changes
    variants, heading_variants = {}, {}
    for oid, changes in patches.items():
        lines = read_blob(oid).decode('utf-8').splitlines()
        for index, translated in changes.items():
            old = lines[int(index) - 1]
            if not CJK.search(old):
                raise RuntimeError('Patch does not identify non-English text: ' + oid + ':' + index)
            if CJK.search(translated):
                raise RuntimeError('Untranslated script in reviewed patch')
            variants.setdefault(old, set()).add(translated)
            if re.match(r'^#{1,6}\s+', old) and re.match(r'^#{1,6}\s+', translated):
                a = re.sub(r'^#{1,6}\s+', '', old)
                b = re.sub(r'^#{1,6}\s+', '', translated)
                heading_variants.setdefault(a, set()).add(b)
    # Ambiguous reusable wording never overrides source-specific reviewed text.
    memory = {a: next(iter(b)) for a, b in variants.items() if len(b) == 1}
    headings = {a: next(iter(b)) for a, b in heading_variants.items() if len(b) == 1}
    records, pending, binary = [], [], []
    current_changes = {}
    def write(path, data, source_oid=None):
        target = ROOT / path
        if target.is_symlink():
            raise RuntimeError('Refusing symlink output: ' + path)
        if target.exists():
            old = target.read_bytes()
            if old == data:
                return
            is_source = source_oid is not None and path in head_tree and head_tree[path]['oid'] == source_oid
            if not is_source and digest(old) != owned_hashes.get(path):
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
                raise RuntimeError('Landing page changed after reviewed translation: ' + path)
            records.append({'source_path': path, 'source_blob': meta['oid'], 'source_sha256': digest(raw), 'output_path': path, 'output_sha256': digest(output), 'kind': 'current_translation', 'verification': 'Previously published exact English translation; original retained separately.'})
            continue
        lines = []
        explicit = patches.get(meta['oid'], {})
        for index, line in enumerate(text.splitlines(keepends=True), 1):
            body = line.rstrip('\r\n')
            ending = line[len(body):]
            if str(index) in explicit:
                body = explicit[str(index)]
            elif body in memory:
                body = memory[body]
            elif body.startswith('- ') and body[2:] in headings:
                body = '- ' + headings[body[2:]]
            elif set(CJK.findall(body)) == {'\u548c'}:
                body = body.replace('\u548c', 'and')
            lines.append(body + ending)
        translated = ''.join(lines)
        if path == 'proofs/RESULTS.md':
            if meta['oid'] != '8e815c9946c6c5ec9da48c9fcef073a023ef0ce8':
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
            check = 'Reviewed non-English lines translated; unambiguous exact-line/heading translations reused; other lines retained.'
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
    records.append({'source_path': 'proofs/SOURCE_MAP.json', 'source_blob': source_tree['proofs/SOURCE_MAP.json']['oid'], 'output_path': 'proofs/SOURCE_MAP.json', 'output_sha256': digest(map_bytes), 'kind': 'historical_replay_mapping', 'verification': 'Historical hashes preserved; translated current paths use immutable originals for historical replay.', 'adjusted_paths': adjusted})
    status = 'TEXT_TRANSLATION_COMPLETE' if not pending else 'IN_PROGRESS'
    manifest = {'agent': 'Agent #1', 'baseline': BASE, 'status': status, 'translations': records, 'pending': pending, 'patch_encoding_repairs': encoding_repairs, 'binary_files_preserved_without_repacking': binary, 'scope': 'Tracked UTF-8 text containing the inventoried non-English scripts. Mathematical symbols, original archives, binary data and published Git history are preserved. English archive views are translations, not new builds.'}
    previous_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
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
    role.update({'status': status, 'current_translation_files': sum(r['kind'] == 'current_translation' for r in records), 'archive_reading_copies': sum(r['kind'] == 'archive_reading_copy' for r in records), 'pending_text_files': len(pending), 'manifest': 'proofs/english/translation_manifest.json', 'room_status': 'ROOM_ACCESS_BLOCKED', 'room_messages_delivered': 0, 'mathematical_verification_claim': 'None; source-language validation only. Historical evidence bytes and classifications preserved.', 'coordination_recheck': 'The p196/coordination branch was recreated during translation. At 82ca526693013ae91898fcefcaa391c8ad791d9b its live coordination directory contained tasks only, no integration role. Existing scoped translation writer and exact-main guards remain; no research task is reassigned.'})
    record_path.write_text(json.dumps(role, indent=2) + '\n')
    written.append('proofs/ENGLISH_TRANSLATION.json')
    changed = git('diff', '--name-only').decode().splitlines()
    if any(path not in written for path in changed):
        raise RuntimeError('Unexpected existing-file changes: ' + repr(changed))
    if git('diff', '--name-only', '--diff-filter=D'):
        raise RuntimeError('Deletion forbidden')
    git('add', '--', *sorted(set(written)))
    git('diff', '--cached', '--check')
    print(json.dumps({'status': status, 'current_translations': role['current_translation_files'], 'archive_views': role['archive_reading_copies'], 'pending_files': len(pending), 'patch_encoding_repairs': encoding_repairs, 'changed_paths': sorted(set(written))}, indent=2))

if __name__ == '__main__':
    main()
