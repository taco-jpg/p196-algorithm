#!/usr/bin/env python3
"""Exercise real interruption/resource paths, optionally the packed-key oracle."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import shlex
import subprocess
import tempfile

import extend_cauto as runtime


def limits_test() -> None:
    binary = runtime.build()
    fixed = ['10', '10100110011', '11100010000', '1', '1', '-v',
             '11000000000', '-allm']
    cases = [
        ('local cap', fixed + ['-cap', '1'], 10, 512, 'UNDECIDED'),
        ('generic layer budget', fixed + ['-jgen', '1'], 10, 512, 'UNDECIDED'),
        ('wall timeout', fixed, 0.000001, 512, 'UNDECIDED'),
        ('malformed trim', fixed[:-3] + ['-v', '1100000000', '-allm'], 10, 512, 'INVALID'),
        ('in-product state cap', ['10', '10100110011' * 2, '11100010000' * 2,
                                 '1', '1', '-v', '00000100001' * 2,
                                 '-allm', '-cap', '10000'], 10, 512, 'UNDECIDED'),
        ('address-space cap', ['10', '10100110011' * 3, '11100010000' * 3,
                               '1', '1', '-v', '1' * 6 + '0' * 27,
                               '-allm', '-cap', '100000000'], 20, 64, 'UNDECIDED'),
    ]
    for name, command, seconds, memory, expected in cases:
        result = runtime.run(binary, command, seconds, memory, False)
        if result['status'] != expected:
            raise AssertionError((name, result))
        print(f"LIMIT PASS {name}: {json.dumps(result, sort_keys=True)}", flush=True)
    print(f"resource_paths={len(cases)} PASS")


def packing_test() -> None:
    source = Path(__file__).with_name('test_packing.cpp')
    with tempfile.TemporaryDirectory(prefix='a113-packing-') as directory:
        directory = Path(directory)
        generated = directory / 'cauto_p48.cpp'
        generated.write_text(runtime.extended_source())
        binary = directory / 'packing'
        flags = ['-std=c++17', '-O1', '-g', '-fsanitize=address,undefined',
                 '-fno-omit-frame-pointer', '-fno-sanitize-recover=all',
                 '-DA113_CAUTO_SOURCE=' + json.dumps(str(generated)),
                 str(source), '-o', str(binary)]
        subprocess.run(shlex.split(os.environ.get('CXX', 'c++')) + flags,
                       check=True, timeout=120)
        env = dict(os.environ)
        # LSAN cannot inspect /proc tasks inside this sandbox. Address/UB
        # instrumentation remains enabled; no leak-check result is claimed.
        env['ASAN_OPTIONS'] = env.get('ASAN_OPTIONS', '') + ':detect_leaks=0'
        subprocess.run([str(binary)], check=True, timeout=60, env=env)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--packing', action='store_true')
    opts = parser.parse_args()
    if opts.packing:
        packing_test()
    else:
        limits_test()


if __name__ == '__main__':
    main()
