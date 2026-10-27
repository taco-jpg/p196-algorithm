#!/usr/bin/env python3
"""Whole-language invariant replay and fail-closed corruption controls.

Build center_regular.cpp and check_regular_invariant.cpp independently, then:
  python3 calculation/agent-113/test_regular_invariant.py \
    --engine /tmp/a113_center_regular --checker /tmp/a113-check-regular-invariant \
    --sanitize

One untrusted text certificate is captured in memory. Mutations change only
certificate structure, not a copy of the arithmetic/checker implementation.
--sanitize builds a temporary ASan/UBSan wrapper around the same checker.
It preserves state/operation/time guards and bypasses only RLIMIT_AS, because
ASan needs a large virtual address reservation. LeakSanitizer is disabled for
containers where it cannot inspect the process tree. The wrapper is deleted
after its full-invariant replay.
"""
from __future__ import annotations

import argparse
from copy import deepcopy
from dataclasses import dataclass
import json
import os
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory


@dataclass
class Certificate:
    base: int
    period: int
    e: str
    g: str
    v: str
    segments: list[list[int]]
    alphabet: list[tuple[int, int, list[tuple[int, int, int]]]]
    initial: int
    states: list[tuple[int, list[tuple[int, int]]]]

    @classmethod
    def parse(cls, text):
        tokens = iter(text.split())
        if next(tokens) != "A113REG1":
            raise RuntimeError("engine did not emit a text certificate")
        base, period = int(next(tokens)), int(next(tokens))
        e, g, v = next(tokens), next(tokens), next(tokens)
        segment_count, symbol_count = int(next(tokens)), int(next(tokens))
        segments = []
        for _ in range(segment_count):
            segments.append([int(next(tokens)) for _ in range(int(next(tokens)))])
        alphabet = []
        for _ in range(symbol_count):
            kind, z = int(next(tokens)), int(next(tokens))
            cells = [tuple(int(next(tokens)) for _ in range(3))
                     for _ in segments[kind]]
            alphabet.append((kind, z, cells))
        count, initial = int(next(tokens)), int(next(tokens))
        states = []
        for _ in range(count):
            final, degree = int(next(tokens)), int(next(tokens))
            states.append((final, [(int(next(tokens)), int(next(tokens)))
                                  for _ in range(degree)]))
        if next(tokens) != "END" or next(tokens, None) is not None:
            raise RuntimeError("unexpected text certificate suffix")
        return cls(base, period, e, g, v, segments, alphabet, initial, states)

    def text(self):
        rows = ["A113REG1", f"{self.base} {self.period}", self.e, self.g, self.v,
                f"{len(self.segments)} {len(self.alphabet)}"]
        rows += [" ".join(map(str, [len(segment), *segment]))
                 for segment in self.segments]
        for kind, z, cells in self.alphabet:
            rows.append(" ".join(map(str, [kind, z, *(x for cell in cells for x in cell)])))
        rows.append(f"{len(self.states)} {self.initial}")
        for final, edges in self.states:
            rows.append(" ".join(map(str, [final, len(edges), *(x for edge in edges for x in edge)])))
        return "\n".join(rows) + "\nEND\n"


def execute(command, *, text=None, seconds=180, env=None):
    return subprocess.run(command, input=text, text=True, capture_output=True,
                          timeout=seconds+5, check=False, env=env)


def verdict(run, expected, code, obligation=None):
    try:
        records = [json.loads(line) for line in run.stdout.splitlines() if line.strip()]
    except json.JSONDecodeError as error:
        raise RuntimeError("checker emitted malformed JSON") from error
    if (run.returncode != code or not records or
            records[-1].get("status") != expected):
        raise RuntimeError(f"expected {expected}/exit{code}, got exit{run.returncode}: "
                           f"{run.stdout[-3000:]} {run.stderr[-1000:]}")
    if obligation is not None and not any(
            row.get("name") == obligation and row.get("passed") is False
            for row in records):
        raise RuntimeError(f"missing failed obligation {obligation}")
    return records[-1]


def sanitizer_replay(text, seconds):
    source = Path(__file__).resolve().with_name("check_regular_invariant.cpp")
    with TemporaryDirectory(prefix="a113-invariant-sanitizer-") as directory:
        wrapper = Path(directory) / "wrapper.cpp"
        binary = Path(directory) / "checker"
        wrapper.write_text(
            "#define main certificate_cli_main\n"
            f"#include {json.dumps(str(source))}\n"
            "#undef main\n"
            "int main(int argc, char** argv) {\n"
            "  using namespace independent;\n"
            "  Options o = options(argc, argv);\n"
            "  std::signal(SIGALRM, alarm_handler); alarm(o.seconds);\n"
            "  Budget budget(o); Checker checker(budget);\n"
            "  checker.read(std::cin);\n"
            "  bool passed = checker.check(); budget.check(); alarm(0);\n"
            "  std::cout << (passed ? \"{\\\"status\\\":\\\"VERIFIED_INVARIANT\\\"}\\n\"\n"
            "                       : \"{\\\"status\\\":\\\"REJECTED\\\"}\\n\");\n"
            "  return passed ? 0 : 1;\n"
            "}\n")
        built = execute([
            "c++", "-O1", "-g", "-std=c++17", "-fsanitize=address,undefined",
            "-fno-omit-frame-pointer", "-fno-sanitize-recover=all",
            str(wrapper), "-o", str(binary)], seconds=seconds)
        if built.returncode:
            raise RuntimeError(f"sanitizer wrapper build failed: {built.stderr[-3000:]}")
        environment = dict(os.environ, ASAN_OPTIONS="detect_leaks=0")
        verdict(execute([str(binary), "--seconds", str(seconds)], text=text,
                        seconds=seconds, env=environment), "VERIFIED_INVARIANT", 0)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--engine")
    source.add_argument("--certificate", type=Path)
    parser.add_argument("--checker", required=True)
    sanitizer = parser.add_mutually_exclusive_group()
    sanitizer.add_argument("--sanitize", action="store_true",
                           help="build a temporary ASan/UBSan checker and replay the invariant")
    sanitizer.add_argument("--sanitized-checker")
    parser.add_argument("--seconds", type=int, default=180)
    args = parser.parse_args()
    if not 1 <= args.seconds <= 1800:
        parser.error("seconds must be 1..1800")
    if args.engine:
        generated = execute([
            args.engine, "10", "10100110011", "11100010000", "01000010000",
            "--text-depth", "5", "--depth", "5", "--states", "1000000",
            "--edges", "20000000", "--ops", "1000000000", "--seconds", str(args.seconds),
            "--memory-mib", "2048"], seconds=args.seconds)
        if generated.returncode:
            raise RuntimeError(f"certificate generation failed: {generated.stdout[-1000:]}")
        original_text = generated.stdout
    else:
        original_text = args.certificate.read_text()
    certificate = Certificate.parse(original_text)
    command = [args.checker, "-", "--seconds", str(args.seconds), "--memory-mib", "2048"]
    positive = verdict(execute(command, text=original_text, seconds=args.seconds),
                       "VERIFIED_INVARIANT", 0)
    corruption_count = 0

    def mutated(change, expected="INVALID", code=2, obligation=None):
        nonlocal corruption_count
        candidate = deepcopy(certificate)
        change(candidate)
        verdict(execute(command, text=candidate.text(), seconds=args.seconds),
                expected, code, obligation)
        corruption_count += 1

    def accepting_initial(c):
        _, edges = c.states[c.initial]
        c.states[c.initial] = (1, edges)

    def empty_initial_edges(c):
        final, _ = c.states[c.initial]
        c.states[c.initial] = (final, [])

    def wrong_order(c):
        c.segments[0][0], c.segments[0][1] = c.segments[0][1], c.segments[0][0]

    def duplicate_symbol(c):
        c.alphabet[1] = deepcopy(c.alphabet[0])

    def bad_carry(c):
        kind, z, cells = c.alphabet[0]
        _, r, rd = cells[0]
        cells[0] = (2, r, rd)
        c.alphabet[0] = (kind, z, cells)

    def bad_pending(c):
        kind, _, cells = c.alphabet[0]
        c.alphabet[0] = (kind, 19, cells)

    def bad_target(c):
        final, edges = c.states[c.initial]
        edges[0] = (edges[0][0], len(c.states))
        c.states[c.initial] = (final, edges)

    def bad_label(c):
        final, edges = c.states[c.initial]
        edges[0] = (len(c.alphabet), edges[0][1])
        c.states[c.initial] = (final, edges)

    def nondeterministic(c):
        c.states[c.initial][1].append(c.states[c.initial][1][0])

    mutated(accepting_initial, "REJECTED", 1, "word_shapes")
    mutated(empty_initial_edges, "REJECTED", 1, "first_image_subset")
    mutated(lambda c: setattr(c, "e", "00100110011"))
    mutated(wrong_order)
    mutated(duplicate_symbol)
    mutated(bad_carry)
    mutated(bad_pending)
    mutated(bad_target)
    mutated(bad_label)
    mutated(nondeterministic)
    for text in (original_text.rsplit("END", 1)[0], original_text + "TRAILING\n"):
        verdict(execute(command, text=text, seconds=args.seconds), "INVALID", 2)
        corruption_count += 1
    for option in ("--states", "--ops"):
        verdict(execute(command+[option, "1"], text=original_text, seconds=args.seconds),
                "UNDECIDED", 3)
    sanitized = False
    if args.sanitize:
        sanitizer_replay(original_text, args.seconds)
        sanitized = True
    elif args.sanitized_checker:
        verdict(execute([args.sanitized_checker], text=original_text, seconds=args.seconds),
                "VERIFIED_INVARIANT", 0)
        sanitized = True
    print(json.dumps(dict(status="PASS", positive_invariants=1, corruptions=corruption_count,
                          resource_guards=2, sanitized=sanitized,
                          invariant_states=len(certificate.states),
                          invariant_edges=sum(len(edges) for _, edges in certificate.states),
                          product_peak=positive.get("peak_states")), sort_keys=True))


if __name__ == "__main__":
    main()
