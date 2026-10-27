#!/usr/bin/env python3
"""Decimal local prefix lifts with cyclic width and modulo-99 conditions.

The input prefix loop comes from prefix_extension.  Each individual edge is
completed independently to a full symmetric center and replayed with the
repository mirror.  A separate seam check exposes the missing global cycle.
The construction can prescribe every modulo-99 value compatible with symmetry
once the middle length is at least four (and hence at least five when odd).
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import neutral_band_search as mirror
from prefix_extension import refine_old_loop


def require(condition, message):
    if not condition:
        raise ValueError(message)


def value(word):
    return sum(x * 10 ** i for i, x in enumerate(word))


def middle(length, exit_carry, residue):
    """Construct a symmetric middle with the given value modulo 99.

    Its output carry is exit_carry for either incoming bit.  An odd physical
    center coefficient is even.  For even length, residue must be 0 modulo 11.
    """
    if not isinstance(length, int) or length < 4 or exit_carry not in (0, 1):
        raise ValueError("middle length >= 4 and a carry bit required")
    require(isinstance(residue, int), "residue must be an integer")
    residue %= 99
    reset = 10 * exit_carry
    if length % 2 == 0:
        if residue % 11:
            raise ValueError("an even symmetric word has value 0 modulo 11")
        coefficient = (residue // 11 - reset) % 9
        core = [reset, coefficient, coefficient, reset]
        padding = (length - 4) // 2
    else:
        padding = (length - 5) // 2
        # For odd words, adding a neutral pair maps R to 10*R+18 (mod 99).
        # Thus padding p pairs maps R to 9 + 10**p*(R-9); this map is its own
        # inverse because 10**(2*p) = 1 (mod 99).
        core_residue = (9 + pow(10, padding, 99) * (residue - 9)) % 99
        quotient = (50 * core_residue - reset) % 99  # 50 is inverse of 2.
        coefficient, half_center = divmod(quotient, 10)
        core = [reset, coefficient, 2 * half_center, coefficient, reset]
    result = [9] * padding + core + [9] * padding
    require(len(result) == length and result == result[::-1], "bad middle shape")
    require(all(0 <= x <= 18 for x in result), "middle coefficient out of range")
    require(value(result) % 99 == residue, "wrong middle residue")
    require(all(mirror.norm(10, result, incoming)[1] == exit_carry
                for incoming in (0, 1)), "middle does not reset the carry")
    if length % 2:
        require(result[length // 2] % 2 == 0, "odd middle has an odd midpoint")
    return result


def complete(source_extension, width, exit_carry, residue):
    """Complete X to C = X ++ middle ++ reverse(X) at a prescribed width."""
    x = list(source_extension)
    require(bool(x), "source extension must be nonempty")
    require(all(isinstance(c, int) and 0 <= c <= 18 for c in x),
            "source extension coefficient out of range")
    require(x[0] != 9, "source extension must have a nonneutral head")
    require(isinstance(width, int) and isinstance(residue, int),
            "width and residue must be integers")
    require(width % 2 or residue % 11 == 0,
            "even symmetric source requires residue 0 modulo 11")
    size = len(x)
    middle_length = width - 2 * size
    if middle_length < 4:
        raise ValueError("source width must be at least 2*len(X)+4")
    fixed = (value(x) + pow(10, size + middle_length, 99) * value(x[::-1])) % 99
    wanted = pow(10, size, 99) * (residue - fixed) % 99
    core = middle(middle_length, exit_carry, wanted)
    center = x + core + x[::-1]
    require(len(center) == width and value(center) % 99 == residue % 99,
            "completed source has the wrong width or residue")
    return center


def cyclic_mod9(path):
    """S_next = 2*S + 4*e - 2 modulo 9, independent of overflow and trim."""
    possibilities = []
    for start in range(9):
        residues = [start]
        for edge in path:
            residues.append((2 * residues[-1] + 4 * edge['e'] - 2) % 9)
        if residues[-1] == start:
            possibilities.append(residues[:-1])
    if not possibilities:
        raise ValueError("the driver has no cyclic center residue modulo 9")
    return possibilities


def combined_residue(mod9, width):
    """Use Q=0 mod11 at even width, Q=9 mod11 at odd width."""
    mod11 = 9 if width % 2 else 0
    return mod11 + 11 * ((5 * (mod9 - mod11)) % 9)


def test_middle():
    count = 0
    for length in range(4, 16):
        residues = range(99) if length % 2 else range(0, 99, 11)
        for exit_carry in (0, 1):
            for residue in residues:
                middle(length, exit_carry, residue)
                count += 1
    print(json.dumps({'middle_residue_constructions': count,
                      'incoming_carries_per_construction': 2, 'status': 'PASS'}))


def audit(label, e, g, repetitions, initial_width, seconds, show_centers=False):
    result = refine_old_loop(depth=4, e=e, g=g, repetitions=repetitions,
                             seconds=seconds, base=10)
    if result['status'] != 'OLD_LOOP_LOCALLY_LIFTED':
        raise RuntimeError(result)
    path = result['path']
    expected_e = list(map(int, e)) * repetitions
    expected_g = list(map(int, g)) * repetitions
    require(len(path) == len(expected_e) == len(expected_g) and bool(path),
            "wrong refined path period")
    for phase, edge in enumerate(path):
        require(edge['t'] == phase and edge['e'] == expected_e[phase] and
                edge['g'] == expected_g[phase], "driver phase mismatch")
        require(isinstance(edge['v'], int) and edge['v'] >= 0,
                "trim count must be a nonnegative integer")
        require(len(edge['source']) == len(edge['target']) == 4 and
                len(edge['extension']) == edge['v'], "wrong boundary extension length")
        require(edge['deep_carry'] in (0, 1), "deep carry must be a bit")
    residues9 = cyclic_mod9(path)
    offsets, offset = [], 0
    for edge in path:
        offsets.append(offset)
        offset += edge['g'] - 2 * edge['v']
    require(offset == 0, "the cyclic width schedule does not close")
    widths = [initial_width + offset for offset in offsets]
    residues = [combined_residue(s, width)
                for s, width in zip(residues9[0], widths)]
    centers, images = [], []
    # These exteriors realize each prescribed pair (entry carry, overflow),
    # solely for independent replay of one center edge.
    exterior = {(0, 0): [1, 0], (0, 1): [10, 0],
                (1, 0): [1, 0, 10], (1, 1): [10]}
    for t, edge in enumerate(path):
        x = edge['source'] + edge['extension']
        center = complete(x, widths[t], edge['deep_carry'], residues[t])
        block = exterior[edge['e'], edge['g']]
        require(center == center[::-1] and center[0] != 9, "source is not canonical symmetric")
        require(center[:4] == edge['source'], "wrong source prefix")
        if len(center) % 2:
            require(center[len(center) // 2] % 2 == 0, "source midpoint is odd")
        require(mirror.hyp(10, block, center), "source violates the mirror Hyp")
        require((mirror.e1(10, block), mirror.gam(10, block, center)) ==
                (edge['e'], edge['g']), "wrong driver pair")
        raw = mirror.nextC(10, block, center)
        _, image, _, trim = mirror.trim(10, [], raw)
        nt = (t + 1) % len(path)
        require(trim == edge['v'] and image[:4] == edge['target'],
                "mirror image has the wrong trim or target prefix")
        require(edge['target'] == path[nt]['source'], "prefix loop does not close")
        require(len(image) == widths[nt], "target width mismatch")
        require(value(image) % 99 == residues[nt], "next-phase residue mismatch")
        require(image == image[::-1] and image[0] != 9, "image is not canonical symmetric")
        if len(image) % 2:
            require(image[len(image) // 2] % 2 == 0, "image midpoint is odd")
        centers.append(center)
        images.append(image)
    matches = [t for t in range(len(path)) if images[t] == centers[(t + 1) % len(path)]]
    summary = {'case': label, 'status': 'LOCAL_MOD99_LIFTS_PASS',
               'depth': 4, 'period': len(path), 'initial_width': initial_width,
               'width_min': min(widths), 'width_max': max(widths),
               'local_edges_checked': len(path),
               'trim_sum': sum(edge['v'] for edge in path),
               'cyclic_mod9_choices': len(residues9),
               'mod9_phase0': residues9[0][0],
               'source_values_mod99': residues,
               'full_center_seam_matches': matches,
               'full_center_seam_mismatches': len(path) - len(matches),
               'full_center_cycle': len(matches) == len(path)}
    if show_centers or summary['full_center_cycle']:
        summary['centers'] = centers
        summary['images'] = images
    print(json.dumps(summary))
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--seconds', type=float, default=30.0)
    parser.add_argument('--initial-width', type=int, default=16)
    parser.add_argument('--show-centers', action='store_true')
    args = parser.parse_args()
    test_middle()
    audit('p11_k1', '10100110011', '11100010000', 1,
          args.initial_width, args.seconds, args.show_centers)
    audit('p12_k2', '101010010101', '100010001000', 2,
          args.initial_width, args.seconds, args.show_centers)


if __name__ == '__main__':
    main()
