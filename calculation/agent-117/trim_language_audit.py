#!/usr/bin/env python3
"""Independent exact arithmetic audit of the decimal normalized-center trim language.

No mirror/automaton implementation is imported.  The center image is obtained
by evaluating the coefficient word as an integer, extracting its base digits,
and pairing those digits.  The six-transition local language is checked against
every normalized symmetric coefficient word through the requested width.

Run from the repository root:
  python3 calculation/agent-117/trim_language_audit.py
The default exhaustive width is eight.  This is a COMPUTED audit, not Lean.
"""

import argparse
import itertools
import re
from pathlib import Path


HEADS = tuple(range(9)) + tuple(range(10, 19))
# (left entering carry, right outgoing carry), coefficient -> inner carries.
NINE = {
    ((1, 0), 4): (0, 0),
    ((0, 0), 4): (0, 1),
    ((0, 1), 14): (1, 1),
    ((1, 1), 14): (1, 0),
    ((1, 0), 9): (1, 0),
    ((0, 1), 9): (0, 1),
}


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def integer_normalization(base, word, incoming):
    value = incoming
    power = 1
    for coefficient in word:
        value += coefficient * power
        power *= base
    digits = []
    for _ in word:
        value, digit = divmod(value, base)
        digits.append(digit)
    return digits, value


def center_image(base, center, incoming, overflow):
    digits, outgoing = integer_normalization(base, center, incoming)
    require(outgoing == 1 - incoming, "center does not flip its carry")
    if overflow:
        digits.append((base - 1) * incoming)
    return [a + b for a, b in zip(digits, reversed(digits))]


def canonical(base, center):
    neutral = base - 1
    count = 0
    while len(center) >= 2 and center[0] == neutral and center[-1] == neutral:
        center = center[1:-1]
        count += 1
    return center, count


def carry_chain(center, incoming):
    chain = [incoming]
    for coefficient in center:
        chain.append((coefficient + chain[-1]) // 10)
    return chain


def local_exit(state, coefficient, right_in):
    left, right_out = state
    if (coefficient + right_in) // 10 != right_out:
        return None
    left_out, left_digit = divmod(coefficient + left, 10)
    right_digit = (coefficient + right_in) % 10
    return left_digit + right_digit, (left_out, right_in)


def classified_positive_trim(incoming, count, target_head):
    if incoming not in (0, 1) or count < 1 or target_head not in HEADS:
        return False
    return not (count == 2 and target_head == (18 if incoming else 0))


def constructive_witness(incoming, count, target_head, parity):
    """Realize every permitted positive-trim head edge with a finite center.

    parity=0 produces an even center; parity=1 produces an odd center with an
    even middle coefficient and alternating coefficient sum 9 modulo 11.
    Thus the one-edge head relation survives those known cycle invariants.
    """
    if not classified_positive_trim(incoming, count, target_head):
        return None
    first = 4 if incoming else 14
    opposite = 18 - first
    prefix = ([first] if count == 1 else [first, first] if count == 2
              else [first, first] + [9] * (count - 3) + [opposite])
    state = (incoming, 1 - incoming)
    for coefficient in prefix:
        state = NINE[state, coefficient]
    for coefficient in range(19):
        for right_in in (0, 1):
            result = local_exit(state, coefficient, right_in)
            if result is None or result[0] != target_head:
                continue
            outside = prefix + [coefficient]
            if parity == 0:
                inner = [10 * right_in] * 2
            else:
                inner = None
                for inner_head in (range(10, 19) if right_in else range(9)):
                    for middle in range(0, 19, 2):
                        candidate = outside + [inner_head, middle, inner_head] + outside[::-1]
                        if sum((-1) ** j * c for j, c in enumerate(candidate)) % 11 == 9:
                            inner = [inner_head, middle, inner_head]
                            break
                    if inner is not None:
                        break
                require(inner is not None, "no invariant-compatible core")
            return outside + inner + outside[::-1]
    raise AssertionError("claimed head edge lacks a local exit")


def table_audit():
    actual = {}
    exit_sets = {}
    for state in itertools.product((0, 1), repeat=2):
        exit_sets[state] = set()
        for coefficient in range(19):
            for right_in in (0, 1):
                out = local_exit(state, coefficient, right_in)
                if out is None:
                    continue
                head, inner = out
                if head == 9:
                    actual[state, coefficient] = inner
                else:
                    exit_sets[state].add(head)
    require(actual == NINE, "six-transition language mismatch")
    require(exit_sets[(0, 0)] == set(HEADS), "00 exit set")
    require(exit_sets[(1, 1)] == set(HEADS), "11 exit set")
    require(exit_sets[(0, 1)] == set(HEADS) - {18}, "01 exit set")
    require(exit_sets[(1, 0)] == set(HEADS) - {0}, "10 exit set")
    return len(actual)


def exhaustive_audit(max_width):
    words = images = trim_prefix_columns = empty_images = positive_trims = 0
    for width in range(1, max_width + 1):
        for half in itertools.product(range(19), repeat=(width + 1) // 2):
            if half[0] == 9:
                continue
            center = list(half) + list(half[:width // 2][::-1])
            incoming = int(center[0] < 9)
            carries = carry_chain(center, incoming)
            digits, outgoing = integer_normalization(10, center, incoming)
            require(outgoing == 1 - incoming, "normalized endpoint carry")
            require(digits == [(c + carries[j]) % 10 for j, c in enumerate(center)],
                    "integer and column normalizations disagree")
            raw = center_image(10, center, incoming, 0)
            words += 1
            for j in range(width // 2):
                outer = carries[j], carries[width - j]
                inner = carries[j + 1], carries[width - j - 1]
                require((NINE.get((outer, center[j])) == inner) == (raw[j] == 9),
                        "9-column language disagrees with integer normalization")
                trim_prefix_columns += 1
            if width % 2:
                require(raw[width // 2] % 2 == 0, "odd midpoint must be even")
            else:
                require(carries[width // 2] == carries[width - width // 2],
                        "even midpoint carry closure")
            for overflow in (0, 1):
                image = center_image(10, center, incoming, overflow)
                target, count = canonical(10, image)
                images += 1
                if not target:
                    empty_images += 1
                    require(overflow == 0, "overflow cannot trim to empty")
                    continue
                require(target[0] != 9, "all-neutral odd center image")
                if overflow:
                    require(count == 0, "positive overflow trim")
                    require(target[0] == center[0] + (10 if incoming else -10),
                            "overflow head formula")
                elif count:
                    positive_trims += 1
                    require(center[0] == (4 if incoming else 14), "trim-source head")
                    require(classified_positive_trim(incoming, count, target[0]),
                            "positive trim classification")
                else:
                    wanted = (2 * center[0] + 1 if incoming
                              else 2 * (center[0] - 10))
                    require(target[0] in (wanted, wanted + 1), "untrimmed head formula")
    return words, images, trim_prefix_columns, empty_images, positive_trims


def witness_audit(max_trim):
    accepted = rejected = 0
    for incoming, count, head, parity in itertools.product((0, 1), range(1, max_trim + 1), HEADS, (0, 1)):
        word = constructive_witness(incoming, count, head, parity)
        if word is None:
            rejected += 1
            continue
        require(len(word) % 2 == parity and word == word[::-1], "witness shape")
        if parity:
            require(word[len(word) // 2] % 2 == 0, "witness even midpoint")
            require(sum((-1) ** j * c for j, c in enumerate(word)) % 11 == 9,
                    "witness odd-center invariant")
        target, found = canonical(10, center_image(10, word, incoming, 0))
        require(found == count and target and target[0] == head, "witness realization")
        if parity:
            require(target[len(target) // 2] % 2 == 0, "target even midpoint")
            require(sum((-1) ** j * c for j, c in enumerate(target)) % 11 == 9,
                    "target odd-center invariant")
        next_incoming = int(head < 9)
        require(integer_normalization(10, target, next_incoming)[1] == 1 - next_incoming,
                "witness successor carry")
        accepted += 1
    return accepted, rejected


def read_certificates(root):
    paths = [root / "lean/P196/Drafts/Agent120NeutralBandCalibration/A120PowerTwo.lean",
             root / "lean/P196/Agent213KnownBaseMechanisms/KnownBases.lean"]
    certificates = []
    for path in paths:
        source = path.read_text()
        constants = {name: [int(x) for x in re.findall(r"\d+", body)] for name, body in
                     re.findall(r"def\s+(\w+)\s*:\s*List Nat\s*:=\s*\[([^\]]*)\]", source)}
        for base, body in re.findall(r"def cert(\d+)\s*:\s*List Edge\s*:=\s*(.*?)\n\n", source, re.S):
            edges = []
            for entry in re.findall(r"⟨(.*?)⟩", body):
                fields = re.findall(r"\[[^\]]*\]|\w+", entry)
                require(len(fields) == 6, "unexpected Lean certificate syntax")
                lists = [constants[token] if not token.startswith("[") else
                         [int(x) for x in re.findall(r"\d+", token)] for token in fields[:4]]
                edges.append((*lists, int(fields[4]), int(fields[5])))
            certificates.append((int(base), edges))
    return sorted(certificates)


def source_controls(root):
    counts = []
    for base, edges in read_certificates(root):
        for exterior, center, _, target, _, trim in edges:
            incoming = integer_normalization(base, exterior, 0)[1]
            overflow = integer_normalization(base, exterior[::-1], 1 - incoming)[1]
            raw = center_image(base, center, incoming, overflow)
            require(raw == [base - 1] * trim + target + [base - 1] * trim,
                    "source certificate center edge")
            core, removed = canonical(base, center)
            target_core, _ = canonical(base, target)
            reduced_raw = center_image(base, core, incoming, overflow)
            reduced_target, reduced_trim = canonical(base, reduced_raw)
            require(reduced_target == target_core and core and core[0] != base - 1,
                    "source canonical center")
            require(raw == [base - 1] * removed + reduced_raw + [base - 1] * removed,
                    "source padding identity")
            if overflow:
                require(reduced_trim == 0, "source normalized overflow trim")
        counts.append((base, len(edges)))
    require([b for b, _ in counts] == [2, 4, 8, 11, 16, 17, 26, 32], "source base coverage")
    return counts


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-width", type=int, default=8)
    parser.add_argument("--max-trim", type=int, default=128)
    args = parser.parse_args()
    if not 1 <= args.max_width <= 8 or not 1 <= args.max_trim <= 1024:
        parser.error("max-width must be 1..8 and max-trim 1..1024")
    print("local_neutral_transitions", table_audit())
    counts = exhaustive_audit(args.max_width)
    print("exhaustive max_width=%d words=%d images=%d paired_columns=%d empty_images=%d positive_trims=%d"
          % (args.max_width, *counts))
    accepted, rejected = witness_audit(args.max_trim)
    print("constructive max_trim=%d accepted=%d excluded=%d" % (args.max_trim, accepted, rejected))
    controls = source_controls(Path(__file__).resolve().parents[2])
    print("source_controls", controls, "total_edges", sum(n for _, n in controls))
    print("COMPUTED AUDIT PASSED")


if __name__ == "__main__":
    main()
