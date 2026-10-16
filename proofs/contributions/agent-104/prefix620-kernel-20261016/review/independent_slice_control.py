#!/usr/bin/env python3
"""Independent finite control of 620 structural slice data and references.

This checks literal data, index coverage, local equality statements and assembly
references. It is not a Lean proof and does not replace the clean kernel build.
No author generator or predecessor implementation is imported.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter
from datetime import datetime, timezone
import hashlib
from itertools import product
import json
from pathlib import Path
import re


CERTIFICATE_SHA = 'e6c447fa7efa26e94d1a8064a9336922d3eeb2e1e55176f8043e1cd9dbe3cea5'
HELPER_SHA = 'd8d672edcda4b39d14247927ee7c7eef221e1da71bee68a0bb67f233006115f5'


def require(condition: bool, detail: object) -> None:
    if not condition:
        raise AssertionError(detail)


def blocks(text: str, prefix: str) -> dict[int, list[list[int]]]:
    pattern = (r'noncomputable def ' + prefix +
               r'_block(\d{3}) : List \(List Nat\) := (\[\]|\[\n.*?\n\])')
    parsed = re.findall(pattern, text, re.S)
    result = {}
    for index, literal in parsed:
        number = int(index)
        require(number not in result, ('duplicate block', prefix, number))
        value = ast.literal_eval(literal)
        require(isinstance(value, list), ('non-list block', prefix, number))
        require(all(isinstance(word, list) and
                    all(type(x) is int and 0 <= x < 19 for x in word)
                    for word in value), ('non-numeric literal', prefix, number))
        result[number] = value
    return result


def symmetric_words(width: int, first: int | None = None) -> list[list[int]]:
    half_size = (width + 1) // 2
    candidates = (product(range(19), repeat=half_size) if first is None else
                  ((first, *tail) for tail in product(range(19), repeat=half_size - 1)))
    result = []
    for half in candidates:
        if half[0] == 0 or (width % 2 and half[-1] % 2):
            continue
        result.append(list(half + half[:width // 2][::-1]))
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path(__file__).with_suffix('.json'))
    args = parser.parse_args()
    project_root = Path(__file__).resolve().parents[5]
    contribution = Path(__file__).resolve().parents[1]
    manifest_path = contribution / 'generator/GENERATION_MANIFEST.json'
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes)
    require(len(manifest['sources']) == 510, 'expected structural 510-module instance')
    source_bytes = {}
    for name, record in manifest['sources'].items():
        path = Path(record['path'])
        require(path.resolve().is_relative_to(project_root), ('outside source root', name))
        data = path.read_bytes()
        require(hashlib.sha256(data).hexdigest() == record['sha256'], ('source hash', name))
        require(len(data) == record['bytes'], ('source bytes', name))
        source_bytes[name] = data
    helper = source_bytes['Agent104Prefix620DataCoverage']
    require(hashlib.sha256(helper).hexdigest() == HELPER_SHA, 'reviewed helper changed')

    def source(name: str) -> str:
        return source_bytes['Agent104Prefix620' + name].decode()

    initials = blocks(source('DataInitialWords'), 'initial')
    shorts = blocks(source('DataShortWords'), 'short')
    require(list(initials) == list(range(101)), 'initial block IDs')
    require(list(shorts) == list(range(78)), 'short block IDs')
    require(initials[0] == [[6, 2, 0, 2, 6], [6, 2, 0, 0, 2, 6]], 'short initials')
    initial_map = []
    for a, b in product(range(10), repeat=2):
        index = 1 + 10 * a + b
        expected = [[6, 2, 0, a, b, c, d] for c, d in product(range(10), repeat=2)]
        require(initials[index] == expected, ('initial slice contents/order', a, b))
        initial_map.append((a, b, index))
    require(shorts[0] == symmetric_words(1), 'width-one direct block')
    require(shorts[1] == symmetric_words(2), 'width-two direct block')
    short_map = []
    by_width = {0: 0, 1: len(shorts[0]), 2: len(shorts[1])}
    for width in range(3, 7):
        offset = 2 + 19 * (width - 3)
        m = (width + 1) // 2 - 1
        combined = []
        for first in range(19):
            index = offset + first
            expected = symmetric_words(width, first)
            require(shorts[index] == expected, ('short slice contents/order', width, first))
            short_map.append((width, m, first, index))
            combined.extend(shorts[index])
        require(combined == symmetric_words(width), ('whole short domain', width))
        by_width[width] = len(combined)
    require(by_width == {0: 0, 1: 9, 2: 18, 3: 180, 4: 342, 5: 3420, 6: 6498},
            ('width counts', by_width))
    require([len(initials[i]) for i in range(101)] ==
            manifest['finite_partition']['initial_block_sizes'], 'initial manifest sizes')
    require([len(shorts[i]) for i in range(78)] ==
            manifest['finite_partition']['short_block_sizes'], 'short manifest sizes')

    initial_coverage = source('InitialCoverage')
    require(re.search(r'theorem initial_cover_short : initialShortWords = initial_block000 := by\s+rfl',
                      initial_coverage) is not None, 'short initial equality')
    initial_equalities = re.findall(
        r'theorem initial_cover_(\d+)_(\d+) : initialSlice (\d+) (\d+) = initial_block(\d{3}) := by\s+rfl',
        initial_coverage)
    require([(int(a), int(b), int(index)) for a, b, aa, bb, index in initial_equalities
             if a == aa and b == bb] == initial_map, 'all 100 local initial equalities')
    require(len(initial_equalities) == 100, 'initial equality count')
    short_coverage = source('ShortCoverage')
    for width, index in [(1, 0), (2, 1)]:
        require(re.search(rf'theorem short_cover_w{width} : symWords {width} = short_block{index:03d} := by\s+rfl',
                          short_coverage) is not None, ('direct short equality', width))
    short_equalities = re.findall(
        r'theorem short_cover_w(\d+)_(\d+) : shortSlice (\d+) (\d+) (\d+) = short_block(\d{3}) := by\s+rfl',
        short_coverage)
    require([(int(n), int(m), int(a), int(index)) for n, a, nn, m, aa, index in short_equalities
             if n == nn and a == aa] == short_map, 'all 76 local short slice equalities')
    require(len(short_equalities) == 76, 'short equality count')

    initial_all = source('InitialAll')
    require('apply initial_all_of_slices (initOKC ranks 11)' in initial_all,
            'initial helper connection')
    require(re.search(r'rw \[initial_cover_short\]\s+exact initial_ok000', initial_all) is not None,
            'short initial aggregate reference')
    initial_refs = re.findall(r'rw \[initial_cover_(\d+)_(\d+)\]\s+exact initial_ok(\d{3})',
                             initial_all)
    require([tuple(map(int, row)) for row in initial_refs] == initial_map,
            'initial aggregate slice-to-check references')
    initial_imports = re.findall(r'^import Agent104Prefix620Initial(\d{3})$', initial_all, re.M)
    require(list(map(int, initial_imports)) == list(range(101)), 'initial imports')
    short_all = source('ShortAll')
    require(re.search(r'theorem short_w0 : \(symWords 0\).all \(shortOKC ranks\) = true := by\s+decide \+kernel',
                      short_all) is not None, 'explicit width-zero check')
    for width in range(3, 7):
        m = (width + 1) // 2 - 1
        require(f'apply short_all_of_slices (shortOKC ranks) {width} {m} (by decide +kernel)'
                in short_all, ('short helper connection', width))
    short_refs = re.findall(r'rw \[short_cover_w(\d+)_(\d+)\]\s+exact short_ok(\d{3})', short_all)
    require([tuple(map(int, row)) for row in short_refs] ==
            [(n, a, i) for n, m, a, i in short_map], 'short aggregate slice-to-check references')
    short_imports = re.findall(r'^import Agent104Prefix620Short(\d{3})$', short_all, re.M)
    require(list(map(int, short_imports)) == list(range(78)), 'short imports')
    require('theorem short : ShortClosed 7 (R ranks) := shortClosed_of_widths' in short_all,
            'original short-closed endpoint')
    for width in range(7):
        require(f'exact short_w{width}' in short_all, ('final short width reference', width))
    for kind, number, predicate in [('initial', 101, 'initOKC ranks 11'),
                                     ('short', 78, 'shortOKC ranks')]:
        for index in range(number):
            body = source(kind.title() + f'{index:03d}')
            proposition = (f'theorem {kind}_ok{index:03d} : {kind}_block{index:03d}.all '
                           f'({predicate}) = true := by\n  decide +kernel')
            require(proposition in body, ('block check contract', kind, index))
            require('import Agent104Prefix620DataTree' in body, ('shared rank tree', kind, index))

    certificate_path = project_root / ('proofs/archive/source-trees/' +
        '2eb05ef47671d6b1883e54fec9f6a4f8de9ed8f5/proofs/contributions/' +
        '2026-10-15-seven-column-prefix/certificate_620.json')
    certificate_bytes = certificate_path.read_bytes()
    require(hashlib.sha256(certificate_bytes).hexdigest() == CERTIFICATE_SHA, 'certificate hash')
    certificate = json.loads(certificate_bytes)
    all_initials = [tuple(word) for group in initials.values() for word in group]
    require(Counter(all_initials) == Counter(tuple(word) for word in certificate['initial']),
            'initial literal domain versus frozen certificate')
    ranks = {tuple(row['word']): row['rank'] for row in certificate['nodes']}
    require(len(all_initials) == 10002 and max(ranks[w] for w in all_initials) == 11,
            'full initial rank bound')
    short_edges = []
    for group in shorts.values():
        for word in group:
            old = tuple(word)
            value = sum(digit * 10 ** i for i, digit in enumerate(old))
            digits = tuple(map(int, str(value)[::-1]))
            new = tuple(a + b for a, b in zip(digits, digits[::-1]))
            if new in ranks:
                require(old in ranks and ranks[old] < ranks[new], ('short rank descent', old, new))
                short_edges.append({'source': old, 'source_rank': ranks[old],
                                    'target': new, 'target_rank': ranks[new]})
    require(len(short_edges) == 6, 'six short boundary edges')
    require(manifest_path.read_bytes() == manifest_bytes, 'manifest changed during control')
    for name, data in source_bytes.items():
        require(Path(manifest['sources'][name]['path']).read_bytes() == data,
                ('source changed during control', name))
    key_modules = ['Agent104Prefix620' + suffix for suffix in [
        'DataCoverage', 'DataInitialWords', 'DataShortWords', 'InitialCoverage',
        'ShortCoverage', 'InitialAll', 'ShortAll', '']]
    result = {
        'schema_version': 1,
        'status': 'PASS_STRUCTURAL_LITERAL_DATA_AND_REFERENCE_CONTROL_ONLY',
        'evidence_level': 'Independent finite data/reference control; not Lean kernel acceptance.',
        'reviewer': '/root/strategy_review',
        'executed_at_utc': datetime.now(timezone.utc).isoformat(),
        'script_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'manifest_sha256': hashlib.sha256(manifest_bytes).hexdigest(),
        'all_generated_source_hashes_verified': len(source_bytes),
        'initial_blocks': len(initials), 'initial_words': len(all_initials),
        'max_initial_rank_in_frozen_json': 11,
        'short_blocks': len(shorts), 'short_words': sum(by_width.values()),
        'short_words_by_width': by_width,
        'explicit_empty_first_coefficient_slices': [2, 21, 40, 59],
        'local_initial_equalities': 101, 'local_short_equalities': 78,
        'block_checker_contracts_checked': 179,
        'short_edges_against_frozen_json': short_edges,
        'targeted_source_pins': {name: manifest['sources'][name] for name in key_modules},
        'lean_build_evidence_must_be_checked_separately': True,
    }
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({key: result[key] for key in ['status', 'initial_blocks',
                      'initial_words', 'short_blocks', 'short_words',
                      'all_generated_source_hashes_verified']}))


if __name__ == '__main__':
    main()
