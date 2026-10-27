#!/usr/bin/env python3
"""Compare WideCount arithmetic with independent Python arbitrary integers.

Only a temporary C++ program is compiled. The header's public API constructs
counts from four uint64 limbs by repeated self-addition; no internal limb
access, decimal parser, Boost, or external Python dependency is used.

Checks cover decimal conversion, zero/boolean behavior, comparisons to uint64,
implicit small constructors, addition and self-addition, all carry-chain
lengths 1..256, randomized operands, repeated sums, and overflow exceptions.
Overflow must leave the accumulator unchanged. Outputs are checked explicitly,
so Python -O and C++ -DNDEBUG do not disable the tests.

    python3 calculation/agent-108/count_checks.py
    python3 calculation/agent-108/count_checks.py --sanitize

The numeric bound used by the exterior MDD is D = 10**G * 2**(2*P)
< 2**(2*P+4*G) <= 2**240 for G>=1. Every exact suffix-language count
and accepting subset is at most D, hence fits 256 bits. This does not bound
cumulative counts over an unbounded number of layers. P=48, G=16 has budget160.
"""
from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
import random
import shlex
import subprocess
import tempfile


MASK64 = (1 << 64) - 1
MAX256 = (1 << 256) - 1

DRIVER = r'''
#include "wide_count.hpp"
#include <array>
#include <cstdint>
#include <iostream>
#include <stdexcept>
#include <string>
#include <type_traits>
using agent108::WideCount;
static_assert(std::is_convertible<std::uint64_t, WideCount>::value,
              "uint64 construction must be implicit");
static_assert(!std::is_convertible<WideCount, bool>::value,
              "boolean conversion must be explicit");
static_assert(!static_cast<bool>(WideCount{}), "default count must be zero");
static_assert(!(WideCount{7} > 7) && WideCount{7} > 6, "small comparison");

static WideCount read_count() {
  std::array<std::uint64_t, 4> words{};
  for (auto& word : words)
    if (!(std::cin >> word)) throw std::runtime_error("missing count limb");
  WideCount result = words[0];
  for (unsigned i = 1; i < words.size(); ++i) {
    for (unsigned bit = 0; bit < 64; ++bit) result += result;
    result += words[i];
  }
  return result;
}
static std::uint64_t read_small() {
  std::uint64_t value;
  if (!(std::cin >> value)) throw std::runtime_error("missing uint64 operand");
  return value;
}
static void show(const WideCount& value, std::uint64_t limit) {
  std::cout << value.decimal() << ' ' << static_cast<bool>(value)
            << ' ' << (value > limit);
}
int main() {
  try {
    char operation;
    while (std::cin >> operation) {
      if (operation == 'Q') {
        const auto count = read_small();
        WideCount sum;
        std::uint64_t overflow_at = 0;
        for (std::uint64_t i = 0; i < count; ++i) {
          const auto term = read_count();
          if (!overflow_at) {
            try { sum += term; }
            catch (const std::overflow_error&) { overflow_at = i + 1; }
          }
        }
        std::cout << overflow_at << ' ' << sum.decimal() << '\n';
        continue;
      }
      auto value = read_count();
      if (operation == 'D') {
        const auto limit = read_small();
        show(value, limit);
        std::cout << '\n';
        continue;
      }
      if (operation == 'S') {
        bool overflow = false;
        try { value += value; }
        catch (const std::overflow_error&) { overflow = true; }
        std::cout << (overflow ? "OVERFLOW " : "OK ");
        show(value, UINT64_MAX);
        std::cout << '\n';
        continue;
      }
      if (operation == 'A') {
        const auto other = read_count();
        const auto limit = read_small();
        bool overflow = false;
        try { value += other; }
        catch (const std::overflow_error&) { overflow = true; }
        std::cout << (overflow ? "OVERFLOW " : "OK ");
        show(value, limit);
        std::cout << ' ' << other.decimal() << '\n';
        continue;
      }
      if (operation == 'C') {
        const auto other = read_small();
        bool overflow = false;
        try { value += other; }
        catch (const std::overflow_error&) { overflow = true; }
        std::cout << (overflow ? "OVERFLOW " : "OK ");
        show(value, other);
        std::cout << '\n';
        continue;
      }
      throw std::runtime_error("unknown operation");
    }
  } catch (const std::exception& error) {
    std::cerr << error.what() << '\n';
    return 1;
  }
}
'''


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def limbs(value):
    require(0 <= value <= MAX256, "test count outside uint256 range")
    return " ".join(str((value >> shift) & MASK64) for shift in (192, 128, 64, 0))


def shown(value, limit):
    return f"{value} {int(bool(value))} {int(value > limit)}"


def cases(seed, random_cases):
    rng = random.Random(seed)
    result, totals = [], Counter()

    def add(line, expected):
        result.append((line, expected))
        totals[line[0]] += 1

    edges = {0, 1, 2, 9, 10, 11, MAX256}
    for bit in range(257):
        for delta in (-1, 0, 1):
            value = (1 << bit) + delta
            if 0 <= value <= MAX256:
                edges.add(value)
    for value in sorted(edges):
        for limit in (0, 1, MASK64, min(value, MASK64)):
            add(f"D {limbs(value)} {limit}", shown(value, limit))
        doubled = value * 2
        expected = value if doubled > MAX256 else doubled
        add(f"S {limbs(value)}",
            ("OVERFLOW " if doubled > MAX256 else "OK ") + shown(expected, MASK64))

    def addition(left, right, limit):
        total = left + right
        overflow = total > MAX256
        expected = left if overflow else total
        add(f"A {limbs(left)} {limbs(right)} {limit}",
            ("OVERFLOW " if overflow else "OK ") + shown(expected, limit) + f" {right}")

    # Every possible binary carry-chain length, including the 256-bit overflow.
    for width in range(1, 257):
        top = (1 << width) - 1
        addition(top, 1, MASK64)
        addition(1, top, MASK64)
        addition(top, top, MASK64)
    for offset in (0, 1, 2, 9, MASK64, 1 << 64, 1 << 128, 1 << 192):
        addition(MAX256 - offset, offset, MASK64)
        addition(MAX256 - offset, offset + 1, MASK64)

    for _ in range(random_cases):
        # Mix full-width random values with narrow and limb-aligned operands.
        left = rng.getrandbits(rng.choice((1, 32, 64, 65, 128, 192, 255, 256)))
        right = rng.getrandbits(rng.choice((1, 32, 64, 65, 128, 192, 255, 256)))
        limit = rng.getrandbits(64)
        addition(left, right, limit)
        add(f"D {limbs(left)} {limit}", shown(left, limit))
        small = rng.getrandbits(64)
        total = left + small
        overflow = total > MAX256
        add(f"C {limbs(left)} {small}",
            ("OVERFLOW " if overflow else "OK ")
            + shown(left if overflow else total, small))

    sequences = [[], [0] * 64, [MAX256, 0, 0], [MAX256, 1, 7],
                 [1 << 192] * 128, [1 << 255, 1 << 255],
                 [1 << 239] * 1024]
    for _ in range(128):
        width = rng.choice((32, 64, 128, 192, 240, 248, 256))
        sequences.append([rng.getrandbits(width) for _ in range(rng.randrange(2, 129))])
    for sequence in sequences:
        total, overflow_at = 0, 0
        for i, term in enumerate(sequence):
            if total + term > MAX256:
                overflow_at = i + 1
                break
            total += term
        add(f"Q {len(sequence)} " + " ".join(limbs(term) for term in sequence),
            f"{overflow_at} {total}")
    return result, totals


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cxx", default="g++", help="C++17 compiler command")
    parser.add_argument("--seed", type=int, default=108256)
    parser.add_argument("--cases", type=int, default=4096, help="random operand pairs")
    parser.add_argument("--sanitize", action="store_true", help="enable UndefinedBehaviorSanitizer")
    args = parser.parse_args()
    require(0 <= args.cases <= 1_000_000, "random case count outside 0..1000000")
    test_cases, totals = cases(args.seed, args.cases)
    header_dir = Path(__file__).resolve().parent
    with tempfile.TemporaryDirectory(prefix="agent108-count-") as temporary:
        source = Path(temporary) / "count_driver.cpp"
        binary = Path(temporary) / "count_driver"
        source.write_text(DRIVER, encoding="utf-8")
        command = shlex.split(args.cxx) + ["-std=c++17", "-O2", "-Wall", "-Wextra",
                  "-Werror", "-DNDEBUG", "-I", str(header_dir), str(source), "-o", str(binary)]
        if args.sanitize:
            command += ["-fsanitize=undefined", "-fno-sanitize-recover=undefined"]
        compiled = subprocess.run(command, text=True, capture_output=True, timeout=60)
        require(compiled.returncode == 0, "C++ compile failed:\n" + compiled.stderr)
        payload = "\n".join(line for line, _ in test_cases) + "\n"
        run = subprocess.run([str(binary)], input=payload, text=True, capture_output=True, timeout=60)
        require(run.returncode == 0, f"C++ driver exited {run.returncode}:\n{run.stderr}")
        require(not run.stderr, "unexpected C++ diagnostics:\n" + run.stderr)
        output = run.stdout.splitlines()
        require(len(output) == len(test_cases),
                f"output length mismatch: {len(output)} versus {len(test_cases)}")
        for index, (actual, (line, expected)) in enumerate(zip(output, test_cases)):
            require(actual == expected,
                    f"case {index} mismatch\ninput: {line}\nexpected: {expected}\nactual: {actual}")
    print(f"PASS WideCount: {len(test_cases)} Python/C++ cases; seed={args.seed}; "
          f"roundtrip/comparison={totals['D']}; addition={totals['A']}; "
          f"self-add={totals['S']}; implicit-small-add={totals['C']}; sums={totals['Q']}; "
          f"ubsan={args.sanitize}")
    print("PASS all carry chains 1..256, zero, 2^64/2^128/2^192, near 2^256, "
          "overflow exceptions with unchanged accumulator")
    print("ALL WIDE COUNT CHECKS PASSED")


if __name__ == "__main__":
    main()
