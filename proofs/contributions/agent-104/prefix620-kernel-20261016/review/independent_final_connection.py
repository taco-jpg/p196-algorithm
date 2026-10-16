#!/usr/bin/env python3
"""Independent data/assembly and immutable Git linkage control for 620.

No generator, predecessor search, or Lean compiler is imported. This is a
finite control, not kernel acceptance. Source files are read only. The output
records content-addressed Git linkage separately from selected byte readbacks.
"""
from __future__ import annotations

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import subprocess


COMMIT = 'dc2123ae4a4513acfe75e0a6cd21c3b6a044bec4'
MANIFEST_SHA = 'd2b92c7139f59fe1cb8268addd0d10073780275f06b109bc3cf72933f9170c03'
CERTIFICATE_SHA = 'e6c447fa7efa26e94d1a8064a9336922d3eeb2e1e55176f8043e1cd9dbe3cea5'


def require(test: bool, detail: object) -> None:
    if not test:
        raise AssertionError(detail)


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def blob_id(data: bytes) -> str:
    return hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()


class LiteralParser:
    """Only the constructors printed in these frozen source literals."""

    def __init__(self, text: str, proof: bool = False):
        pattern = (r'rows_leaf\d{4}|row_branch\d{4}|[⟨⟩,]' if proof else
                   r'\.node|\.empty|leaf\d{4}|\d+|[()]')
        matches = list(re.finditer(pattern, text))
        last = 0
        for match in matches:
            require(not text[last:match.start()].strip(), ('unexpected literal', text[last:match.start()]))
            last = match.end()
        require(not text[last:].strip(), ('literal trailing text', text[last:]))
        self.tokens = [m.group() for m in matches]
        self.i = 0

    def take(self) -> str:
        require(self.i < len(self.tokens), 'unexpected literal end')
        token = self.tokens[self.i]
        self.i += 1
        return token

    def expect(self, token: str) -> None:
        require(self.take() == token, ('expected token', token, self.i))

    def tree(self):
        token = self.take()
        if token == '(':
            result = self.tree()
            self.expect(')')
            return result
        if token == '.empty':
            return None
        if token.startswith('leaf'):
            return token
        require(token == '.node', ('expected constructor', token))
        code, rank = self.take(), self.take()
        require(code.isdecimal() and rank.isdecimal(), ('non-Nat node', code, rank))
        return int(code), int(rank), self.tree(), self.tree()

    def proof(self):
        token = self.take()
        if token.startswith('rows_leaf'):
            return token
        require(token == '⟨', ('expected conjunction', token))
        left = self.proof()
        self.expect(',')
        branch = self.take()
        require(branch.startswith('row_branch'), ('expected branch theorem', branch))
        self.expect(',')
        right = self.proof()
        self.expect('⟩')
        return left, branch, right

    def done(self) -> None:
        require(self.i == len(self.tokens), ('unconsumed tokens', len(self.tokens) - self.i))


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', type=Path, default=Path(__file__).resolve().parents[5])
    parser.add_argument('--commit', default=COMMIT)
    parser.add_argument('--output', type=Path, default=Path(__file__).with_suffix('.json'))
    args = parser.parse_args()
    repo = args.repo.resolve()
    contribution = repo / 'proofs/contributions/agent-104/prefix620-kernel-20261016'
    manifest_path = contribution / 'generator/GENERATION_MANIFEST.json'
    manifest_bytes = manifest_path.read_bytes()
    require(sha(manifest_bytes) == MANIFEST_SHA, 'frozen manifest changed')
    manifest = json.loads(manifest_bytes)
    sources: dict[str, bytes] = {}
    paths: dict[str, str] = {}
    for name, record in manifest['sources'].items():
        # Manifest paths reflect the author checkout; module names provide the
        # published flat layout, allowing a different --repo on replay.
        path = repo / 'proofs' / (name + '.lean')
        data = path.read_bytes()
        require(sha(data) == record['sha256'] and len(data) == record['bytes'], ('manifest source', name))
        sources[name] = data
        paths[name] = str(path.relative_to(repo))
    require(len(sources) == 510, 'generated module count')

    # Parse the actual literal tree, including all leaf definitions. This does
    # not rerun the author's tree construction algorithm.
    definitions = {}
    for name, data in sources.items():
        if re.fullmatch(r'Agent104Prefix620Data\d{3}', name) or name.endswith('DataTree'):
            for symbol, literal in re.findall(r'^def (leaf\d{4}|ranks) : CodeTree := (.+)$', data.decode(), re.M):
                require(symbol not in definitions, ('duplicate definition', symbol))
                reader = LiteralParser(literal)
                definitions[symbol] = reader.tree()
                reader.done()
    require(set(definitions) == {'ranks'} | {f'leaf{i:04d}' for i in range(256)}, 'tree definition domain')
    leaf_uses = Counter()
    ordered = []

    def walk(tree):
        if tree is None:
            return
        if isinstance(tree, str):
            leaf_uses[tree] += 1
            require(leaf_uses[tree] == 1, ('repeated or cyclic leaf reference', tree))
            walk(definitions[tree])
            return
        code, rank, left, right = tree
        walk(left)
        ordered.append((code, rank))
        walk(right)

    walk(definitions['ranks'])
    require(set(leaf_uses) == {f'leaf{i:04d}' for i in range(256)}, 'unused leaf')
    require(len(ordered) == 59189, 'rank tree node count')
    require(all(ordered[i][0] < ordered[i + 1][0] for i in range(len(ordered) - 1)), 'tree in-order key uniqueness/order')
    certificate_path = repo / ('proofs/archive/source-trees/2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/'
                              'proofs/contributions/2026-10-15-seven-column-prefix/certificate_620.json')
    certificate_bytes = certificate_path.read_bytes()
    require(sha(certificate_bytes) == CERTIFICATE_SHA, 'frozen certificate changed')
    certificate = json.loads(certificate_bytes)
    expected = []
    for node in certificate['nodes']:
        word = node['word']
        require(all(type(d) is int and 0 <= d < 19 for d in word), 'word coefficient domain')
        # Independent positional formula, with the original leading marker 1.
        code = 19 ** len(word) + sum(d * 19 ** (len(word) - 1 - i) for i, d in enumerate(word))
        expected.append((code, node['rank']))
    require(ordered == sorted(expected), 'literal code/rank table differs from frozen JSON')

    # Independently match every conjunction component to the same tree shape.
    rows = sources['Agent104Prefix620RowsAll'].decode()
    proof_text = rows.split('theorem allRowsAll :', 1)[1].split(':=', 1)[1].split('theorem allRows :', 1)[0].strip()
    reader = LiteralParser(proof_text, proof=True)
    proof = reader.proof()
    reader.done()
    branch_source = sources['Agent104Prefix620RowsBranch'].decode()
    branches = {name: (int(code), int(rank)) for name, code, rank in re.findall(
        r'theorem (row_branch\d{4}) : rowOK ranks 7 (\d+) (\d+) = true := by\s+decide \+kernel', branch_source)}
    require(set(branches) == {f'row_branch{i:04d}' for i in range(255)}, 'branch checker domain')
    branch_uses = Counter()
    assembly_leaf_uses = Counter()

    def match(tree, assembled):
        if isinstance(tree, str):
            require(assembled == 'rows_' + tree, ('wrong leaf theorem', tree, assembled))
            assembly_leaf_uses[tree] += 1
            return
        require(tree is not None and isinstance(assembled, tuple), 'root assembly shape')
        code, rank, left, right = tree
        lproof, branch, rproof = assembled
        require(branches[branch] == (code, rank), ('wrong branch theorem', branch, code, rank))
        branch_uses[branch] += 1
        match(left, lproof)
        match(right, rproof)

    match(definitions['ranks'], proof)
    require(assembly_leaf_uses == leaf_uses, 'assembly leaf coverage')
    require(branch_uses == Counter({key: 1 for key in branches}), 'assembly branch coverage')
    for i in range(256):
        source = sources[f'Agent104Prefix620Rows{i:03d}'].decode()
        statement = (f'theorem rows_leaf{i:04d} : leaf{i:04d}.All '
                     '(fun c r => rowOK ranks 7 c r = true) :=\n'
                     '  allRowsC_sound (by decide +kernel)')
        require(statement in source, ('leaf checker contract', i))
        require('import Agent104Prefix620DataTree\n' in source, ('leaf rank tree import', i))
    require('theorem allRows : RowsClosed 7 (R ranks) := rowsClosed_of_all (by decide +kernel) allRowsAll' in rows,
            'long-row final interface')

    # Pin all 510 generated sources, all 13 reviewed foundations, and the two
    # published freeze documents plus frozen input to the published Git tree.
    payloads = {paths[name]: data for name, data in sources.items()}
    base_pins = json.loads((contribution / 'review/source-pins.json').read_text())
    for name, record in base_pins['modules'].items():
        data = (repo / record['path']).read_bytes()
        require(sha(data) == record['sha256'], ('base source pin', name))
        payloads[record['path']] = data
    for path in [manifest_path, contribution / 'generator/SOURCE_FREEZE.json', certificate_path]:
        payloads[str(path.relative_to(repo))] = path.read_bytes()
    require(len(payloads) == 526, 'published source/artifact count')
    result = subprocess.run(['git', '-C', str(repo), 'ls-tree', '-r', '-z', args.commit, '--', *payloads],
                            check=True, stdout=subprocess.PIPE)
    tree_ids = {}
    for entry in result.stdout.split(b'\0'):
        if entry:
            info, path = entry.split(b'\t', 1)
            mode, kind, object_id = info.decode().split()
            require(kind == 'blob', ('not a published blob', path.decode()))
            tree_ids[path.decode()] = object_id
    require(set(tree_ids) == set(payloads), ('published path domain', set(payloads) - set(tree_ids)))
    linked = {}
    for path, data in payloads.items():
        require(tree_ids[path] == blob_id(data), ('published content mismatch', path))
        linked[path] = {'bytes': len(data), 'sha256': sha(data), 'git_blob': tree_ids[path]}

    slice_control = json.loads((contribution / 'review/independent_slice_control.json').read_text())
    require(slice_control['manifest_sha256'] == MANIFEST_SHA, 'slice control concerns different source')
    selected = list(slice_control['targeted_source_pins']) + [
        'Agent104Prefix620DataTree', 'Agent104Prefix620RowsAll', 'Agent104Prefix620RowsBranch']
    readback_paths = [paths[name] for name in selected] + [
        str(manifest_path.relative_to(repo)),
        str((contribution / 'generator/SOURCE_FREEZE.json').relative_to(repo))]
    for path in readback_paths:
        data = subprocess.run(['git', '-C', str(repo), 'cat-file', 'blob', tree_ids[path]],
                              check=True, stdout=subprocess.PIPE).stdout
        require(data == payloads[path], ('selected byte readback mismatch', path))
    # Catch source changes while this control runs.
    require(manifest_path.read_bytes() == manifest_bytes, 'manifest changed during check')
    for name, data in sources.items():
        require((repo / paths[name]).read_bytes() == data, ('source changed during check', name))

    output = {
        'schema_version': 1,
        'status': 'PASS_FINITE_TREE_ASSEMBLY_AND_PUBLISHED_SOURCE_LINKAGE_ONLY',
        'evidence_level': 'Independent finite control and Git source identity; not Lean kernel acceptance.',
        'reviewer': '/root/strategy_review',
        'executed_at_utc': datetime.now(timezone.utc).isoformat(),
        'script_sha256': sha(Path(__file__).read_bytes()),
        'published_commit': args.commit,
        'manifest_sha256': MANIFEST_SHA,
        'literal_rank_nodes': len(ordered),
        'literal_rank_table_equals_frozen_json': True,
        'code_key_formula': '19^length + sum_i word[i]*19^(length-1-i)',
        'unique_sorted_code_keys': True,
        'allRowsAll_tree_shape_match': True,
        'leaf_checker_contracts': 256,
        'branch_checker_contracts': 255,
        'published_content_addressed_paths': len(linked),
        'selected_byte_readback_paths': readback_paths,
        'published_source_links': linked,
        'all_lean_compilation_and_axiom_acceptance_remains_separate': True,
    }
    args.output.write_text(json.dumps(output, indent=2) + '\n')
    print(json.dumps({key: output[key] for key in [
        'status', 'literal_rank_nodes', 'leaf_checker_contracts',
        'branch_checker_contracts', 'published_content_addressed_paths']}))


if __name__ == '__main__':
    main()
