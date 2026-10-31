#!/usr/bin/env python3
"""Independent necessary head projection and tuple-state B transfer search.

The projection is only necessary: its closed walks need not lift to B cycles.
The transfer search is exact for a fixed overflow word and all B widths when
EXHAUSTED; a time/state cap is UNDECIDED. No center or Lychrel result follows.
Uses only the Python standard library; does not import the repository mirror.
"""
import argparse
import collections
import itertools
import json
import time


def head_edges(base):
    """x is B[0], or base-1 for an empty B; c is an inward carry."""
    edges = {x: {0: set(), 1: set()} for x in range(1, 2 * base - 1)}
    for x in edges:
        for c in (0, 1):
            g = (x + c) // base
            y = 2 * x + c if g == 0 else x % base + 1
            edges[x][g].add(y)
    return edges


def closed_heads(base, word):
    edges = head_edges(base)
    allowed = []
    for initial in edges:
        frontier = {initial}
        for g in word:
            frontier = {y for x in frontier for y in edges[x][g]}
            if not frontier:
                break
        if initial in frontier:
            allowed.append(initial)
    return allowed


def necklaces(period):
    for word in itertools.product((0, 1), repeat=period):
        if all(word <= word[k:] + word[:k] for k in range(1, period)):
            yield word


def census(base, pmin, pmax):
    result = []
    for period in range(pmin, pmax + 1):
        count = 0
        survivors = []
        for word in necklaces(period):
            count += 1
            heads = closed_heads(base, word)
            if heads:
                survivors.append({"g": "".join(map(str, word)), "heads": heads})
        result.append({"base": base, "period": period, "necklaces": count,
                       "survivors": len(survivors), "words": survivors})
    return result


def normalize(base, word, carry):
    digits = []
    for coefficient in word:
        carry, digit = divmod(coefficient + carry, base)
        digits.append(digit)
    return digits, carry


def direct_b_step(base, word):
    left, e = normalize(base, word, 0)
    right, g = normalize(base, word[::-1], 1 - e)
    if g:
        left += [(base - 1) * (1 - e)]
        right = right[::-1]
        right.insert(0, 1)
    else:
        right.reverse()
    return tuple(a + b for a, b in zip(left, right)), e, g


def selftest(base, width):
    edges = head_edges(base)
    states = transitions = 0
    for length in range(width + 1):
        for word in itertools.product(range(2 * base - 1), repeat=length):
            if word and word[0] == 0:
                continue
            raw, _, g = direct_b_step(base, word)
            x = word[0] if word else base - 1
            states += 1
            while True:
                y = raw[0] if raw else base - 1
                if y not in edges[x][g]:
                    raise AssertionError((base, word, raw, g, x, y))
                transitions += 1
                if not raw or raw[-1] != base - 1:
                    break
                raw = raw[:-1]
    if base == 10:
        for text in ("11100010000", "100010001000"):
            if not closed_heads(base, tuple(map(int, text))):
                raise AssertionError("known exterior stream rejected")
    return {"status": "PASS", "base": base, "max_width": width,
            "direct_states": states, "all_trim_edges": transitions}


def transfer(base, word, max_states, seconds):
    """Independent uncompressed all-width positional automaton.

    At each spatial column, close its coefficient trajectory in time. L[t]
    is its incoming low-side carry, H[t] its required outgoing high-side
    carry, and Y[t] the previous column's reverse digit on overflow steps.
    """
    period = len(word)
    zero = (0,) * period
    start = (zero, tuple(word), tuple(1 if g else -1 for g in word))
    seen = {start}
    queue = collections.deque([(start, 0)])
    accepted = {}
    maximum_depth = 0
    begin = time.monotonic()
    deadline = begin + seconds
    status = "EXHAUSTED"
    processed = 0
    column_nodes = 0

    class BudgetExceeded(Exception):
        pass

    def successors(state, first):
        nonlocal column_nodes
        left, right, previous = state
        for initial in range(1 if first else 0, 2 * base - 1):
            stack = [(0, initial, (), (), ())]
            while stack:
                column_nodes += 1
                if column_nodes % 4096 == 0 and time.monotonic() > deadline:
                    raise BudgetExceeded
                t, coefficient, new_left, new_right, new_previous = stack.pop()
                if t == period:
                    if coefficient == initial:
                        yield (new_left, new_right, new_previous)
                    continue
                if first and coefficient == 0:
                    continue
                for inward in (0, 1):
                    high_out, high_digit = divmod(coefficient + inward, base)
                    if high_out != right[t]:
                        continue
                    low_out, low_digit = divmod(coefficient + left[t], base)
                    following = low_digit + (previous[t] if word[t] else high_digit)
                    stack.append((t + 1, following,
                                  new_left + (low_out,), new_right + (inward,),
                                  new_previous + (high_digit if word[t] else -1,)))

    while queue:
        if time.monotonic() > deadline:
            status = "TIMEOUT_UNDECIDED"
            break
        state, depth = queue.popleft()
        processed += 1
        maximum_depth = max(maximum_depth, depth)
        left, right, previous = state
        if (all(a + b == 1 for a, b in zip(left, right)) and
                all(not g or previous[t] == (base - 1) * left[t]
                    for t, g in enumerate(word))):
            accepted.setdefault("".join(map(str, left)), depth)
        try:
            for following in successors(state, depth == 0):
                if following not in seen:
                    if len(seen) >= max_states:
                        status = "STATE_CAP_UNDECIDED"
                        break
                    seen.add(following)
                    queue.append((following, depth + 1))
                if time.monotonic() > deadline:
                    status = "TIMEOUT_UNDECIDED"
                    break
        except BudgetExceeded:
            status = "TIMEOUT_UNDECIDED"
        if status != "EXHAUSTED":
            break
    return {"base": base, "period": period, "g": "".join(map(str, word)),
            "status": status, "states": len(seen), "processed": processed,
            "max_depth": maximum_depth, "accept_e_minwidth": accepted,
            "elapsed_seconds": round(time.monotonic() - begin, 6)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    cp = sub.add_parser("census")
    cp.add_argument("--base", type=int, default=20)
    cp.add_argument("--pmin", type=int, default=1)
    cp.add_argument("--pmax", type=int, default=12)
    cp.add_argument("--summary", action="store_true")
    sp = sub.add_parser("selftest")
    sp.add_argument("--base", type=int, default=20)
    sp.add_argument("--width", type=int, default=3)
    tp = sub.add_parser("transfer")
    tp.add_argument("--base", type=int, default=20)
    tp.add_argument("--g", required=True)
    tp.add_argument("--cap", type=int, default=200000)
    tp.add_argument("--seconds", type=float, default=30)
    bp = sub.add_parser("batch")
    bp.add_argument("--base", type=int, default=20)
    bp.add_argument("--pmin", type=int, default=1)
    bp.add_argument("--pmax", type=int, default=12)
    bp.add_argument("--cap", type=int, default=200000)
    bp.add_argument("--seconds", type=float, default=10)
    bp.add_argument("--total-seconds", type=float, default=300)
    args = parser.parse_args()
    if args.base < 2:
        parser.error("base must be at least 2")
    if args.command in ("census", "batch"):
        if not 1 <= args.pmin <= args.pmax <= 20:
            parser.error("require 1 <= pmin <= pmax <= 20")
        output = census(args.base, args.pmin, args.pmax)
        if args.command == "batch":
            if args.cap < 1 or args.seconds <= 0 or args.total_seconds <= 0:
                parser.error("cap and time budgets must be positive")
            deadline = time.monotonic() + args.total_seconds
            decisions = []
            for row in output:
                for item in row["words"]:
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        decision = {"base": args.base, "period": row["period"],
                                    "g": item["g"], "status": "UNPROCESSED_UNDECIDED"}
                    else:
                        decision = transfer(args.base, tuple(map(int, item["g"])),
                                            args.cap, min(args.seconds, remaining))
                    decisions.append(decision)
                    print(json.dumps(decision, sort_keys=True), flush=True)
            output = {"base": args.base, "pmin": args.pmin, "pmax": args.pmax,
                      "necklaces": sum(row["necklaces"] for row in output),
                      "head_survivors": len(decisions),
                      "status_counts": dict(collections.Counter(
                          row["status"] for row in decisions)),
                      "B_accepted_words": sum(bool(row.get("accept_e_minwidth"))
                                              for row in decisions)}
        elif args.summary:
            output = [{k: v for k, v in row.items() if k != "words"} for row in output]
    elif args.command == "selftest":
        if args.width < 0:
            parser.error("width must be nonnegative")
        output = selftest(args.base, args.width)
    else:
        if not args.g or any(c not in "01" for c in args.g):
            parser.error("g must be a nonempty binary string")
        if args.cap < 1 or args.seconds <= 0:
            parser.error("cap and seconds must be positive")
        output = transfer(args.base, tuple(map(int, args.g)), args.cap, args.seconds)
    print(json.dumps(output, sort_keys=True))


if __name__ == "__main__":
    main()
